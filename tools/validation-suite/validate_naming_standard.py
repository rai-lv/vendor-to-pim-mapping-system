#!/usr/bin/env python3
"""
Naming Standard Validator

Validates repository elements against the naming standard defined in:
docs/standards/naming_standard.md

Checks:
1. Job IDs: snake_case pattern ^[a-z][a-z0-9_]{2,62}$
2. Job Groups: snake_case pattern ^[a-z][a-z0-9_]{2,62}$
3. Script Filenames: glue_script.py as entrypoint
4. Artifact Filenames: snake_case with proper extensions
5. Documentation Filenames: layer-specific patterns
6. Placeholder Syntax: ${NAME} format
7. Parameter Names: UPPER_SNAKE_CASE or snake_case
8. Reserved Words: Check against AWS/Python keywords
9. Length Constraints: 256 chars max, 128 for parameters
10. Empty Markers: TBD or NONE (not other variations)

Per naming_standard.md Sections 3 and 4.
"""
import re
import sys
import yaml
from pathlib import Path
from typing import List, Set, Tuple

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.config import TOOL_PATHS, REPO_ROOT


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


# Reserved words from naming_standard.md Section 3.5
PYTHON_KEYWORDS = {
    'class', 'def', 'import', 'for', 'if', 'while', 'return', 'try', 'except',
    'finally', 'with', 'as', 'from', 'lambda', 'yield', 'global', 'nonlocal',
    'assert', 'break', 'continue', 'del', 'elif', 'else', 'pass', 'raise'
}

AWS_RESERVED = {
    'JOB_NAME', 'JOB_RUN_ID', 'TempDir', 'scriptLocation'
}

SYSTEM_TERMS_ALONE = {'temp', 'tmp', 'cache', 'log', 'test'}


def validate_job_id(job_id: str, path: Path) -> List[Violation]:
    """Validate job ID follows naming_standard.md Section 4.1."""
    violations = []
    
    # Pattern: ^[a-z][a-z0-9_]{2,62}$
    # Length 3-63, starts with lowercase letter, snake_case
    pattern = r'^[a-z][a-z0-9_]{2,62}$'
    legacy_pattern = r'^[a-z][a-z0-9][a-zA-Z0-9]{1,61}$'  # camelCase grandfathered
    
    if not re.match(pattern, job_id):
        # Check if it's legacy camelCase (grandfathered)
        if not re.match(legacy_pattern, job_id):
            violations.append(Violation(
                "naming", path, "invalid_job_id",
                f"Job ID '{job_id}' must match ^[a-z][a-z0-9_]{{2,62}}$ (snake_case, 3-63 chars)"
            ))
        elif any(c.isupper() for c in job_id):
            # It's camelCase - note it but don't fail (grandfathered)
            violations.append(Violation(
                "naming", path, "legacy_job_id",
                f"Job ID '{job_id}' uses legacy camelCase (grandfathered). New jobs should use snake_case"
            ))
    
    # Check length constraints
    if len(job_id) > 256:
        violations.append(Violation(
            "naming", path, "job_id_too_long",
            f"Job ID '{job_id}' exceeds 256 character limit"
        ))
    
    # Check reserved words
    if job_id in PYTHON_KEYWORDS or job_id in SYSTEM_TERMS_ALONE:
        violations.append(Violation(
            "naming", path, "reserved_word",
            f"Job ID '{job_id}' uses reserved word"
        ))
    
    return violations


def validate_job_group(group: str, path: Path) -> List[Violation]:
    """Validate job group follows naming_standard.md Section 4.2."""
    violations = []
    
    # Pattern: ^[a-z][a-z0-9_]{2,62}$
    pattern = r'^[a-z][a-z0-9_]{2,62}$'
    
    if not re.match(pattern, group):
        violations.append(Violation(
            "naming", path, "invalid_job_group",
            f"Job group '{group}' must match ^[a-z][a-z0-9_]{{2,62}}$ (snake_case, 3-63 chars)"
        ))
    
    return violations


def validate_script_filename(filename: str, path: Path, is_entrypoint: bool = False) -> List[Violation]:
    """Validate script filename follows naming_standard.md Section 4.3."""
    violations = []
    
    if is_entrypoint:
        # Entrypoint must be glue_script.py
        if filename != "glue_script.py":
            violations.append(Violation(
                "naming", path, "invalid_entrypoint",
                f"Entrypoint script must be named 'glue_script.py', not '{filename}'"
            ))
    else:
        # Supporting scripts: snake_case with .py extension
        pattern = r'^[a-z][a-z0-9_]+\.py$'
        if not re.match(pattern, filename):
            violations.append(Violation(
                "naming", path, "invalid_script_name",
                f"Script '{filename}' must match ^[a-z][a-z0-9_]+\\.py$ (snake_case)"
            ))
    
    return violations


def validate_artifact_filename(filename: str, path: Path) -> List[Violation]:
    """Validate artifact filename follows naming_standard.md Section 4.4."""
    violations = []
    
    # Remove placeholders for pattern matching
    filename_clean = re.sub(r'\$\{[^}]+\}', '', filename)
    
    # Remove any _norm suffix from the cleaned filename
    filename_clean = re.sub(r'_norm$', '', filename_clean)
    
    # Strip leading underscores left by placeholder removal
    filename_clean = filename_clean.lstrip('_')
    
    # If filename becomes empty or just extension after cleanup, skip validation
    if not filename_clean or filename_clean.startswith('.'):
        return violations
    
    # Pattern: ^[a-z][a-z0-9_]+\.(json|ndjson|csv|xml|parquet|txt)$
    pattern = r'^[a-z][a-z0-9_]*\.(json|ndjson|csv|xml|parquet|txt)$'
    
    # Also allow files without extension (for directory patterns)
    pattern_no_ext = r'^[a-z][a-z0-9_]*$'
    
    if not (re.match(pattern, filename_clean) or re.match(pattern_no_ext, filename_clean)):
        violations.append(Violation(
            "naming", path, "invalid_artifact_name",
            f"Artifact '{filename}' must use snake_case with extension (json|ndjson|csv|xml|parquet|txt)"
        ))
    
    # Check for disallowed patterns (camelCase, PascalCase)
    name_part = filename_clean.split('.')[0] if '.' in filename_clean else filename_clean
    if re.search(r'[A-Z]', name_part):
        violations.append(Violation(
            "naming", path, "artifact_casing",
            f"Artifact '{filename}' contains uppercase letters (should use snake_case)"
        ))
    
    # Check for hyphens
    if '-' in name_part:
        violations.append(Violation(
            "naming", path, "artifact_hyphen",
            f"Artifact '{filename}' uses hyphen (should use underscore for snake_case)"
        ))
    
    return violations


def validate_doc_filename(filename: str, layer: str, path: Path) -> List[Violation]:
    """Validate documentation filename follows naming_standard.md Section 4.5."""
    violations = []
    
    # Special cases that are exempted
    exempted = ['README.md']
    if filename in exempted:
        return violations
    
    # Agent profiles can use kebab-case or .agent.md suffix
    if layer == ".github/agents":
        # Agent profiles: <agent-name>.md or <agent-name>.agent.md with kebab-case allowed
        pattern = r'^[a-z][a-z0-9-]+(\.agent)?\.md$'
        if not re.match(pattern, filename):
            violations.append(Violation(
                "naming", path, "invalid_agent_profile",
                r"Agent profile '{}' must match ^[a-z][a-z0-9-]+(\.agent)?\.md$ (kebab-case or snake_case)".format(filename)
            ))
        return violations
    
    # Decision records: DR-NNNN-slug.md
    if layer == "decisions":
        pattern = r'^DR-\d{4}-[a-z0-9-]+\.md$'
        if not re.match(pattern, filename):
            violations.append(Violation(
                "naming", path, "invalid_decision_record",
                f"Decision record '{filename}' must match DR-NNNN-slug.md format"
            ))
        return violations
    
    # Per-job docs: bus_description_<job_id>.md or script_card_<job_id>.md
    # Note: typo bus_desription is also checked
    if layer == "per-job":
        if not (filename.startswith('bus_description_') or 
                filename.startswith('script_card_') or
                filename.startswith('bus_desription_')):  # Common typo
            violations.append(Violation(
                "naming", path, "invalid_job_doc",
                f"Job document '{filename}' must start with 'bus_description_' or 'script_card_'"
            ))
        # Check for common typo
        if filename.startswith('bus_desription_'):
            violations.append(Violation(
                "naming", path, "typo_in_filename",
                f"Job document '{filename}' has typo: 'desription' should be 'description'"
            ))
        return violations
    
    # Allow ALL_CAPS.md for ops documentation (like VALIDATOR_CI_INTEGRATION.md)
    if layer == "ops":
        all_caps_pattern = r'^[A-Z][A-Z0-9_]+\.md$'
        if re.match(all_caps_pattern, filename):
            return violations  # ALL_CAPS is acceptable for ops docs
    
    # Standard docs: snake_case.md
    pattern = r'^[a-z][a-z0-9_]+\.md$'
    if not re.match(pattern, filename):
        violations.append(Violation(
            "naming", path, "invalid_doc_name",
            f"Document '{filename}' must use snake_case.md format"
        ))
    
    # Check for disallowed patterns (but don't double-report)
    if '-' in filename.replace('.md', '') and layer != "ops":
        violations.append(Violation(
            "naming", path, "doc_hyphen",
            f"Document '{filename}' uses hyphen (should use underscore for snake_case)"
        ))
    
    return violations


def validate_placeholder_syntax(placeholder: str, path: Path) -> List[Violation]:
    """Validate placeholder follows naming_standard.md Section 4.6."""
    violations = []
    
    # Pattern: ${NAME} - no spaces, alphanumeric and underscore only
    pattern = r'^\$\{[A-Za-z][A-Za-z0-9_]*\}$'
    
    if not re.match(pattern, placeholder):
        violations.append(Violation(
            "naming", path, "invalid_placeholder",
            f"Placeholder '{placeholder}' must match ${{NAME}} format (no spaces, starts with letter)"
        ))
    
    return violations


def validate_parameter_name(param_name: str, path: Path) -> List[Violation]:
    """Validate parameter name follows naming_standard.md Section 4.7."""
    violations = []
    
    # Two allowed patterns:
    # 1. UPPER_SNAKE_CASE for AWS system parameters
    # 2. snake_case for user-defined parameters
    
    upper_pattern = r'^[A-Z][A-Z0-9_]+$'
    lower_pattern = r'^[a-z][a-z0-9_]+$'
    
    if not (re.match(upper_pattern, param_name) or re.match(lower_pattern, param_name)):
        violations.append(Violation(
            "naming", path, "invalid_parameter",
            f"Parameter '{param_name}' must use UPPER_SNAKE_CASE or snake_case"
        ))
    
    # Check length
    if len(param_name) > 128:
        violations.append(Violation(
            "naming", path, "parameter_too_long",
            f"Parameter '{param_name}' exceeds 128 character AWS Glue constraint"
        ))
    
    # Warn if using UPPER_SNAKE_CASE for non-reserved parameters
    if re.match(upper_pattern, param_name) and param_name not in AWS_RESERVED:
        violations.append(Violation(
            "naming", path, "uppercase_user_parameter",
            f"Parameter '{param_name}' uses UPPER_SNAKE_CASE (reserved for AWS system parameters)"
        ))
    
    return violations


def validate_empty_marker(value: str, path: Path, field_name: str) -> List[Violation]:
    """Validate empty marker follows naming_standard.md Section 3.7."""
    violations = []
    
    # Must be scalar 'TBD' or 'NONE', not variations
    if value.strip() in ['[]', '[ ]', 'null', 'NULL', 'None', 'tbd', 'none']:
        violations.append(Violation(
            "naming", path, "invalid_empty_marker",
            f"Field '{field_name}' uses '{value}' (should be 'TBD' or 'NONE')"
        ))
    
    return violations


def validate_job_structure(jobs_dir: Path) -> List[Violation]:
    """Validate all jobs follow naming standard."""
    violations = []
    
    if not jobs_dir.exists():
        return violations
    
    # Iterate through job groups
    for group_dir in jobs_dir.iterdir():
        if not group_dir.is_dir() or group_dir.name.startswith('.'):
            continue
        
        # Validate job group name
        violations.extend(validate_job_group(group_dir.name, group_dir))
        
        # Iterate through jobs in group
        for job_dir in group_dir.iterdir():
            if not job_dir.is_dir() or job_dir.name.startswith('.'):
                continue
            
            # Validate job ID
            violations.extend(validate_job_id(job_dir.name, job_dir))
            
            # Check for glue_script.py
            entrypoint = job_dir / "glue_script.py"
            if not entrypoint.exists():
                violations.append(Violation(
                    "naming", job_dir, "missing_entrypoint",
                    f"Job must have glue_script.py entrypoint"
                ))
            
            # Validate other python scripts
            for script in job_dir.glob("*.py"):
                if script.name == "glue_script.py":
                    continue  # Already checked
                violations.extend(validate_script_filename(script.name, script, is_entrypoint=False))
            
            # Validate manifest if present
            manifest_path = job_dir / "job_manifest.yaml"
            if manifest_path.exists():
                violations.extend(validate_manifest_naming(manifest_path))
            
            # Validate per-job docs
            for doc in job_dir.glob("*.md"):
                violations.extend(validate_doc_filename(doc.name, "per-job", doc))
    
    return violations


def validate_manifest_naming(manifest_path: Path) -> List[Violation]:
    """Validate naming elements within a job manifest."""
    violations = []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        return violations  # Structural validation handled elsewhere
    
    # Validate job_id
    if 'job_id' in manifest:
        violations.extend(validate_job_id(manifest['job_id'], manifest_path))
    
    # Validate parameters
    if 'parameters' in manifest:
        for param in manifest['parameters']:
            if isinstance(param, dict) and 'name' in param:
                violations.extend(validate_parameter_name(param['name'], manifest_path))
    
    # Validate placeholders in outputs
    if 'outputs' in manifest:
        for output in manifest['outputs']:
            if isinstance(output, dict):
                # Check key_pattern for placeholders
                if 'key_pattern' in output:
                    placeholders = re.findall(r'\$\{[^}]+\}', output['key_pattern'])
                    for ph in placeholders:
                        violations.extend(validate_placeholder_syntax(ph, manifest_path))
                    
                    # Extract filename and validate
                    key_pattern = output['key_pattern']
                    # Get terminal filename (after last /)
                    if '/' in key_pattern:
                        filename = key_pattern.split('/')[-1]
                    else:
                        filename = key_pattern
                    
                    # Validate artifact filename
                    violations.extend(validate_artifact_filename(filename, manifest_path))
    
    # Validate placeholders in inputs
    if 'inputs' in manifest:
        for inp in manifest['inputs']:
            if isinstance(inp, dict) and 'key_pattern' in inp:
                placeholders = re.findall(r'\$\{[^}]+\}', inp['key_pattern'])
                for ph in placeholders:
                    violations.extend(validate_placeholder_syntax(ph, manifest_path))
    
    # Check empty markers in manifest
    for field in ['consumers', 'producers']:
        if field in manifest:
            value = str(manifest[field])
            if value in ['[]', 'null', 'None']:
                violations.extend(validate_empty_marker(value, manifest_path, field))
    
    return violations


def validate_docs_structure(docs_dir: Path) -> List[Violation]:
    """Validate documentation filenames follow naming standard."""
    violations = []
    
    if not docs_dir.exists():
        return violations
    
    # Map directory names to layers
    layer_map = {
        'context': 'context',
        'standards': 'standards',
        'process': 'process',
        'ops': 'ops',
        'agents': 'agents',
        'catalogs': 'catalogs',
        'decisions': 'decisions'
    }
    
    for layer_dir in docs_dir.iterdir():
        if not layer_dir.is_dir() or layer_dir.name not in layer_map:
            continue
        
        layer = layer_map[layer_dir.name]
        
        for doc in layer_dir.glob("*.md"):
            violations.extend(validate_doc_filename(doc.name, layer, doc))
    
    # Check .github/agents/
    github_agents = TOOL_PATHS.github_agents
    if github_agents.exists():
        for doc in github_agents.glob("*.md"):
            violations.extend(validate_doc_filename(doc.name, ".github/agents", doc))
    
    # Check README.md at root
    readme = TOOL_PATHS.readme
    if readme.exists():
        # README.md is exempted, validation handled in validate_doc_filename
        pass
    
    return violations


def validate_naming_standard() -> List[Violation]:
    """Run all naming standard validations."""
    violations = []
    
    # Validate jobs structure
    jobs_dir = TOOL_PATHS.jobs_root
    violations.extend(validate_job_structure(jobs_dir))
    
    # Validate documentation structure
    docs_dir = TOOL_PATHS.docs_root
    violations.extend(validate_docs_structure(docs_dir))
    
    return violations


def main():
    violations = validate_naming_standard()
    
    for violation in violations:
        print(violation.format())
    
    # Count files validated
    jobs_dir = TOOL_PATHS.jobs_root
    docs_dir = TOOL_PATHS.docs_root
    
    job_count = sum(1 for _ in jobs_dir.glob("*/*")) if jobs_dir.exists() else 0
    doc_count = sum(1 for _ in docs_dir.glob("**/*.md")) if docs_dir.exists() else 0
    
    validated_count = job_count + doc_count
    fail_count = len(violations)
    pass_count = validated_count if fail_count == 0 else 0
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

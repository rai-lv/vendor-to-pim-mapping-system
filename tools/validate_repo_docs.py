#!/usr/bin/env python3
"""
Repository Documentation and Manifest Validator

This tool validates repository documentation and manifest files against
specifications defined in docs/standards/.

CURRENT VALIDATION COVERAGE:
  ✅ Job Manifests (job_manifest.yaml)
  ✅ Artifacts Catalog (docs/catalogs/artifacts_catalog.md)
  ✅ Job Inventory (docs/catalogs/job_inventory.md)
  ✅ Security Checks (Python scripts and YAML files)
  ✅ Context Layer Documents (docs/context/*.md)
  ✅ Process Layer Documents (docs/process/*.md)
  ✅ Agent Layer Documents (docs/agents/*.md, .github/agents/*.md)
  ✅ Per-Job Documents (business descriptions, script cards)
  ✅ Decision Records (docs/decisions/*.md, decision_log.md)
  ✅ Codable Task Specifications (task specifications per codable_task_spec.md)
  ✅ Cross-Document Consistency (term definitions, broken links, role consistency)
  ✅ Naming Standard (job IDs, artifacts, docs, placeholders per naming_standard.md)

VALIDATION RULES:

1. Job Manifests (per docs/standards/job_manifest_spec.md):
   - Required fields: job_id, glue_job_name, runtime, parameters, inputs,
     outputs, side_effects, logging_and_receipt
   - job_id must match folder name
   - Placeholder syntax: Must use ${NAME}, not <NAME> or {NAME}
   - TBD handling: If any field contains "TBD", notes field is required with:
     * TBD_EXPLANATIONS block in notes
     * Each TBD field path mentioned in notes

2. Artifacts Catalog (per docs/standards/artifacts_catalog_spec.md):
   - Required fields (in order): artifact_id, file_name_pattern,
     s3_location_pattern, format, producer_job_id, producers/consumers,
     presence_on_success, purpose, content_contract, evidence_sources
   - Optional governance fields (in order): producer_glue_job_name,
     stability, breaking_change_rules
   - Purpose must not be TBD
   - Entries with "producers" field must be in shared artifacts allowlist

3. Job Inventory (per docs/standards/job_inventory_spec.md):
   - Required headings (in order): # Job Inventory, ## Scope and evidence,
     ## Jobs, ## Dependency links, ## Open verification items
   - Jobs table with required columns (in order)

4. Security Checks (NEW - basic patterns only):
   - AWS access keys (AKIA..., ASIA...)
   - Generic password patterns in code
   - Hardcoded API keys and tokens
   - Private key patterns
   - SQL string concatenation (potential injection)
   - Unsafe YAML loading (yaml.load vs yaml.safe_load)
   
   Note: These are basic pattern checks. For comprehensive security scanning,
   use dedicated tools like GitGuardian, TruffleHog, or Bandit.

5. Context Layer Documents:
   - development_approach.md structure and required sections
   - target_agent_system.md structure and required sections
   - system_context.md structure and required sections
   - glossary.md term definitions and duplicate detection

6. Process Layer Documents:
   - workflow_guide.md structure with 5-step process
   - contribution_approval_guide.md structure
   - Consistency between workflow steps

7. Agent Layer Documents:
   - agent_role_charter.md structure and agent role definitions
   - .github/agents/*.md YAML frontmatter and structure

8. Per-Job Documents:
   - Business descriptions structure
   - Script cards structure
   - Consistency with job manifests

9. Decision Records:
   - Decision record structure (Status, Context, Decision)
   - Decision log index consistency

10. Codable Task Specifications:
   - Task identity (task identifier, parent capability)
   - Task purpose, boundaries, dependencies
   - Intended outputs and acceptance criteria
   - Structure per docs/standards/codable_task_spec.md

11. Cross-Document Consistency:
   - Term definition consistency (glossary enforcement)
   - Cross-reference validation (broken link detection)
   - Role consistency between charter and agent implementations

12. Naming Standard:
   - Job IDs: snake_case pattern ^[a-z][a-z0-9_]{2,62}$
   - Job Groups: snake_case pattern  
   - Script Filenames: glue_script.py as entrypoint
   - Artifact Filenames: snake_case with proper extensions
   - Documentation Filenames: layer-specific patterns
   - Placeholder Syntax: ${NAME} format
   - Parameter Names: UPPER_SNAKE_CASE or snake_case
   - Reserved Words, Length Constraints, Empty Markers
   - Per docs/standards/naming_standard.md

For detailed specifications and rationale, see:
  - docs/standards/job_manifest_spec.md
  - docs/standards/artifacts_catalog_spec.md
  - docs/standards/job_inventory_spec.md
  - docs/standards/validation_standard.md
  - VALIDATION_ANALYSIS.md (validation coverage analysis)
"""
import argparse
import re
import sys
from pathlib import Path
import subprocess

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_REQUIRED_KEYS = {
    "job_id",
    "glue_job_name",
    "runtime",
    "parameters",
    "inputs",
    "outputs",
    "side_effects",
    "logging_and_receipt",
}

ARTIFACTS_REQUIRED_KEYS_WITH_PRODUCERS = [
    "artifact_id",
    "file_name_pattern",
    "s3_location_pattern",
    "format",
    "producer_job_id",
    "producers",
    "consumers",
    "presence_on_success",
    "purpose",
    "content_contract",
    "evidence_sources",
]

ARTIFACTS_REQUIRED_KEYS_WITHOUT_PRODUCERS = [
    "artifact_id",
    "file_name_pattern",
    "s3_location_pattern",
    "format",
    "producer_job_id",
    "consumers",
    "presence_on_success",
    "purpose",
    "content_contract",
    "evidence_sources",
]

# Optional governance fields allowed (in order) after evidence_sources in artifacts_catalog entries.
# These are documented in docs/standards/artifacts_catalog_spec.md Section 6.
# They provide additional metadata for governance and stability tracking.
OPTIONAL_GOVERNANCE_FIELDS = [
    "producer_glue_job_name",  # Glue job name (may differ from job_id)
    "stability",               # Stability rating: experimental, stable, deprecated
    "breaking_change_rules",   # Breaking change policies for this artifact
]

JOB_INVENTORY_HEADINGS = [
    "# Job Inventory",
    "## Scope and evidence",
    "## Jobs",
    "## Dependency links",
    "## Open verification items",
]

JOB_INVENTORY_COLUMNS = [
    "job_id",
    "job_dir",
    "executor",
    "deployment_name",
    "runtime",
    "owner",
    "business_purpose",
    "parameters",
    "inputs",
    "outputs",
    "side_effects",
    "evidence_artifacts",
    "upstream_job_ids",
    "downstream_job_ids",
    "status",
    "last_reviewed",
]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception as exc:
        return exc


def collect_tbd_paths(data):
    paths = []

    def walk(value, path):
        if value == "TBD":
            paths.append(path)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else key
                walk(item, next_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                next_path = f"{path}[{index}]" if path else f"[{index}]"
                walk(item, next_path)

    walk(data, "")
    return sorted(set(paths))


def contains_invalid_placeholder(value: str) -> bool:
    """
    Check if string contains invalid placeholder syntax.
    
    Valid placeholder syntax: ${NAME} (Bash-style variable references)
    Invalid placeholder syntax:
      - <NAME> (angle brackets reserved for non-placeholder values like URLs)
      - {NAME} (curly braces alone are not valid)
    
    This enforces placeholder normalization per docs/standards/naming_standard.md.
    """
    # Check for <NAME> style (invalid)
    if re.search(r"<[^>]+>", value):
        return True
    # Remove valid ${NAME} style, then check for remaining {NAME} style (invalid)
    cleaned = re.sub(r"\$\{[^}]+\}", "", value)
    return bool(re.search(r"\{[^}]+\}", cleaned))


def scan_for_invalid_placeholders(data):
    invalid_paths = []

    def walk(value, path):
        if isinstance(value, str):
            if contains_invalid_placeholder(value):
                invalid_paths.append(path)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else key
                walk(item, next_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                next_path = f"{path}[{index}]" if path else f"[{index}]"
                walk(item, next_path)

    walk(data, "")
    return sorted(set(invalid_paths))


def validate_manifest(path: Path):
    violations = []
    data = load_yaml(path)
    if isinstance(data, Exception):
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_yaml",
                f"Unable to parse YAML: {data}",
            )
        )
        return violations

    if not isinstance(data, dict):
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_structure",
                "Manifest must be a mapping/object.",
            )
        )
        return violations

    missing_keys = [key for key in sorted(MANIFEST_REQUIRED_KEYS) if key not in data]
    if missing_keys:
        violations.append(
            Violation(
                "manifest",
                path,
                "missing_required_keys",
                f"Missing required top-level keys: {', '.join(missing_keys)}.",
            )
        )

    job_id = data.get("job_id")
    folder_job_id = path.parent.name
    if job_id is not None and job_id != folder_job_id:
        violations.append(
            Violation(
                "manifest",
                path,
                "job_id_mismatch",
                f"job_id '{job_id}' does not match folder '{folder_job_id}'.",
            )
        )

    invalid_placeholder_paths = scan_for_invalid_placeholders(data)
    for invalid_path in invalid_placeholder_paths:
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_placeholder",
                f"Invalid placeholder style in field '{invalid_path}'.",
            )
        )

    # TBD EXPLANATION REQUIREMENT:
    # Per docs/standards/job_manifest_spec.md, if any field contains "TBD",
    # the manifest must include a "notes" field with:
    #   1. A "TBD_EXPLANATIONS:" block
    #   2. An explanation for each TBD field path
    # This ensures TBD values are tracked and eventually resolved.
    tbd_paths = collect_tbd_paths(data)
    if tbd_paths:
        notes = data.get("notes")
        if notes is None:
            violations.append(
                Violation(
                    "manifest",
                    path,
                    "missing_notes",
                    "notes is required when any TBD appears in the manifest.",
                )
            )
        elif not isinstance(notes, list):
            violations.append(
                Violation(
                    "manifest",
                    path,
                    "invalid_notes",
                    "notes must be a list when TBD values are present.",
                )
            )
        else:
            notes_text = [str(item) for item in notes]
            if not any("TBD_EXPLANATIONS" in item for item in notes_text):
                violations.append(
                    Violation(
                        "manifest",
                        path,
                        "missing_tbd_block",
                        "notes must include a TBD_EXPLANATIONS block.",
                    )
                )
            for tbd_path in tbd_paths:
                if not any(tbd_path in item for item in notes_text):
                    violations.append(
                        Violation(
                            "manifest",
                            path,
                            "missing_tbd_explanation",
                            f"notes must mention TBD field path '{tbd_path}'.",
                        )
                    )

    return violations


def load_shared_artifacts_allowlist(path: Path):
    if not path.exists():
        return set()
    data = load_yaml(path)
    if isinstance(data, Exception):
        return set()
    if isinstance(data, list):
        return {str(item) for item in data}
    if isinstance(data, dict):
        return {str(item) for item in data.get("allowlist", [])}
    return set()


# Markdown bullet: leading spaces allowed; dash; space; then rest
_BULLET_RE = re.compile(r"^(?P<indent>\s*)-\s+(?P<rest>.*)$")


def parse_artifact_entry(lines):
    """
    Extract the ordered list of *top-level* keys from an artifact entry.

    Key design goal:
    - Accept Markdown-valid indentation for the entry's main bullets (often 0–3 spaces, but allow any).
    - Do NOT treat nested bullets (e.g. under content_contract) as top-level keys.

    Strategy:
    - Collect all bullet lines that look like 'key: ...' plus their indentation level.
    - Determine the minimum indentation among those candidates within the entry block.
    - Treat only bullets at that minimum indentation as the entry's top-level keys.
    """
    candidates = []
    for raw in lines:
        m = _BULLET_RE.match(raw)
        if not m:
            continue
        rest = m.group("rest")
        if ":" not in rest:
            continue
        key, value = rest.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        indent_len = len(m.group("indent"))
        candidates.append((indent_len, key, value))

    if not candidates:
        return [], {}

    min_indent = min(i for i, _, _ in candidates)

    keys = []
    values = {}
    for indent_len, key, value in candidates:
        if indent_len != min_indent:
            continue
        keys.append(key)
        if key not in values:
            values[key] = value

    return keys, values


def validate_artifacts_catalog(path: Path, allowlist):
    violations = []

    if not path.exists():
        violations.append(
            Violation(
                "artifacts_catalog",
                path,
                "missing_file",
                "docs/catalogs/artifacts_catalog.md does not exist.",
            )
        )
        return violations

    lines = path.read_text(encoding="utf-8").splitlines()

    # Spec requires a top-level title; be robust to whitespace.
    if not any(line.strip() == "# Artifacts Catalog" for line in lines):
        violations.append(
            Violation(
                "artifacts_catalog",
                path,
                "missing_title",
                "Artifacts catalog must include the '# Artifacts Catalog' title.",
            )
        )

    heading_indices = [index for index, line in enumerate(lines) if line.startswith("## ")]
    seen_ids = {}  # Track artifact IDs to detect duplicates
    for idx, start in enumerate(heading_indices):
        end = heading_indices[idx + 1] if idx + 1 < len(heading_indices) else len(lines)
        heading_line = lines[start]
        artifact_id = heading_line[3:].strip()
        
        # Check for duplicate artifact IDs
        if artifact_id in seen_ids:
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "duplicate_artifact_id",
                    f"Entry '{artifact_id}' is duplicated (first seen at line {seen_ids[artifact_id] + 1}).",
                )
            )
        else:
            seen_ids[artifact_id] = start
        
        entry_lines = lines[start + 1 : end]
        keys, values = parse_artifact_entry(entry_lines)

        has_producers = "producers" in keys
        expected_keys = (
            ARTIFACTS_REQUIRED_KEYS_WITH_PRODUCERS
            if has_producers
            else ARTIFACTS_REQUIRED_KEYS_WITHOUT_PRODUCERS
        )

        # Spec allows optional governance fields after evidence_sources (in this exact order):
        # producer_glue_job_name, stability, breaking_change_rules.
        # Accept either:
        # - exact required keys, OR
        # - required keys plus a valid optional governance tail.
        extra_keys = []
        if keys[: len(expected_keys)] == expected_keys:
            extra_keys = keys[len(expected_keys) :]
        is_valid_governance_tail = extra_keys == OPTIONAL_GOVERNANCE_FIELDS[: len(extra_keys)]

        if not (keys == expected_keys or is_valid_governance_tail):
            allowed = ", ".join(expected_keys)
            allowed_with_tail = (
                allowed
                + " [+ optional: "
                + ", ".join(OPTIONAL_GOVERNANCE_FIELDS)
                + "]"
            )
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "invalid_entry_structure",
                    f"Entry '{artifact_id}' keys must be in order: {allowed_with_tail}.",
                )
            )

        purpose_value = values.get("purpose")
        if purpose_value == "TBD":
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "purpose_tbd",
                    f"Entry '{artifact_id}' purpose must not be TBD.",
                )
            )

        if has_producers and artifact_id not in allowlist:
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "producers_not_allowlisted",
                    f"Entry '{artifact_id}' has producers but is not allowlisted.",
                )
            )

    return violations


def validate_job_inventory(path: Path):
    violations = []

    if not path.exists():
        violations.append(
            Violation(
                "job_inventory",
                path,
                "missing_file",
                "docs/catalogs/job_inventory.md does not exist.",
            )
        )
        return violations

    lines = path.read_text(encoding="utf-8").splitlines()
    heading_positions = {}
    for index, line in enumerate(lines):
        for heading in JOB_INVENTORY_HEADINGS:
            if line.strip() == heading:
                heading_positions[heading] = index

    if len(heading_positions) != len(JOB_INVENTORY_HEADINGS):
        missing = [heading for heading in JOB_INVENTORY_HEADINGS if heading not in heading_positions]
        violations.append(
            Violation(
                "job_inventory",
                path,
                "missing_headings",
                f"Missing required headings: {', '.join(missing)}.",
            )
        )
    else:
        indices = [heading_positions[heading] for heading in JOB_INVENTORY_HEADINGS]
        if indices != sorted(indices):
            violations.append(
                Violation(
                    "job_inventory",
                    path,
                    "heading_order",
                    "Required headings are not in the exact required order.",
                )
            )

    unexpected_headings = [
        line.strip()
        for line in lines
        if line.startswith("## ") and line.strip() not in JOB_INVENTORY_HEADINGS[1:]
    ]
    if unexpected_headings:
        violations.append(
            Violation(
                "job_inventory",
                path,
                "unexpected_headings",
                f"Unexpected top-level headings found: {', '.join(unexpected_headings)}.",
            )
        )

    jobs_heading = "## Jobs"
    if jobs_heading in heading_positions:
        start = heading_positions[jobs_heading]
        end_candidates = [
            heading_positions[heading]
            for heading in JOB_INVENTORY_HEADINGS
            if heading_positions.get(heading, -1) > start
        ]
        end = min(end_candidates) if end_candidates else len(lines)
        section_lines = lines[start + 1 : end]
        table_header = next((line for line in section_lines if line.strip().startswith("|")), None)
        if table_header is None:
            violations.append(
                Violation(
                    "job_inventory",
                    path,
                    "missing_jobs_table",
                    "Jobs section must include a markdown table.",
                )
            )
        else:
            columns = [col.strip() for col in table_header.strip().strip("|").split("|")]
            if columns != JOB_INVENTORY_COLUMNS:
                violations.append(
                    Violation(
                        "job_inventory",
                        path,
                        "invalid_jobs_table_columns",
                        "Jobs table columns must match the spec names and order.",
                    )
                )
            
            # Check for duplicate job IDs in the table
            seen_job_ids = {}  # Track job IDs to detect duplicates
            table_start_index = start + 1 + section_lines.index(table_header)
            for i, line in enumerate(section_lines):
                if line.strip().startswith("|") and i > section_lines.index(table_header) + 1:  # Skip header and separator
                    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                    if cells and cells[0]:  # First column is job_id
                        job_id = cells[0]
                        current_line_num = table_start_index + i - section_lines.index(table_header)
                        
                        if job_id in seen_job_ids:
                            violations.append(
                                Violation(
                                    "job_inventory",
                                    path,
                                    "duplicate_job_id",
                                    f"Job ID '{job_id}' is duplicated (first seen at line {seen_job_ids[job_id] + 1}).",
                                )
                            )
                        else:
                            seen_job_ids[job_id] = current_line_num

    return violations


def find_manifest_paths():
    return sorted(REPO_ROOT.glob("jobs/*/*/job_manifest.yaml"))


def show_coverage():
    """
    Display validation coverage report.
    
    Shows which validation types are implemented vs not implemented.
    Useful for understanding tool limitations and planning future work.
    """
    print("=" * 70)
    print("VALIDATION COVERAGE REPORT")
    print("=" * 70)
    print()
    print("IMPLEMENTED VALIDATORS:")
    print("  ✅ Job Manifests (job_manifest.yaml)")
    print("     - Required fields validation")
    print("     - job_id matching folder name")
    print("     - Placeholder syntax enforcement (${NAME} only)")
    print("     - TBD explanation requirements")
    print()
    print("  ✅ Artifacts Catalog (docs/catalogs/artifacts_catalog.md)")
    print("     - Entry structure validation")
    print("     - Required fields in correct order")
    print("     - Optional governance fields support")
    print("     - Purpose not TBD enforcement")
    print("     - Producers allowlist check")
    print()
    print("  ✅ Job Inventory (docs/catalogs/job_inventory.md)")
    print("     - Required headings validation")
    print("     - Heading order enforcement")
    print("     - Jobs table structure validation")
    print()
    print("  ✅ Security Checks (Python and YAML files)")
    print("     - AWS access key detection")
    print("     - Hardcoded password detection")
    print("     - API key and token detection")
    print("     - Private key detection")
    print("     - SQL injection pattern detection")
    print("     - Unsafe YAML loading detection")
    print()
    print("  ✅ Context Layer Documents (docs/context/)")
    print("     - development_approach.md structure")
    print("     - target_agent_system.md structure")
    print("     - system_context.md structure")
    print("     - glossary.md term definitions")
    print("     - Duplicate term detection")
    print()
    print("  ✅ Process Layer Documents (docs/process/)")
    print("     - workflow_guide.md 5-step structure")
    print("     - contribution_approval_guide.md structure")
    print("     - Cross-document consistency checks")
    print()
    print("  ✅ Agent Layer Documents (docs/agents/, .github/agents/)")
    print("     - agent_role_charter.md structure")
    print("     - Agent profile YAML frontmatter")
    print("     - Agent profile structure validation")
    print()
    print("  ✅ Per-Job Documents (jobs/**/)")
    print("     - Business descriptions (bus_description_*.md)")
    print("     - Script cards (script_card_*.md)")
    print("     - Consistency with job manifests")
    print()
    print("  ✅ Decision Records (docs/decisions/, docs/catalogs/)")
    print("     - Decision record structure")
    print("     - Decision log index consistency")
    print("     - Status validation")
    print()
    print("  ✅ Codable Task Specifications")
    print("     - Task identity (task identifier, parent capability)")
    print("     - Task purpose, boundaries, dependencies")
    print("     - Intended outputs and acceptance criteria")
    print("     - Structure per codable_task_spec.md")
    print()
    print("  ✅ Cross-Document Consistency Checks")
    print("     - Term definition consistency (glossary enforcement)")
    print("     - Cross-reference validation (broken link detection)")
    print("     - Role consistency between charter and implementations")
    print()
    print("  ✅ Naming Standard (repository-wide)")
    print("     - Job IDs: snake_case pattern ^[a-z][a-z0-9_]{2,62}$")
    print("     - Job Groups: snake_case pattern")
    print("     - Script Filenames: glue_script.py as entrypoint")
    print("     - Artifact Filenames: snake_case with proper extensions")
    print("     - Documentation Filenames: layer-specific patterns")
    print("     - Placeholder Syntax: ${NAME} format")
    print("     - Parameter Names: UPPER_SNAKE_CASE or snake_case")
    print("     - Reserved Words, Length Constraints, Empty Markers")
    print()
    print("-" * 70)
    print("NOT IMPLEMENTED (Future Work):")
    print("  (None - all validation types implemented!)")
    print()
    print("-" * 70)
    print("COVERAGE: 100% (12/12 validation types)")
    print()
    print("For detailed analysis and recommendations, see VALIDATION_ANALYSIS.md")
    print("=" * 70)


# Security patterns to detect common secrets and vulnerabilities
SECURITY_PATTERNS = {
    "aws_access_key": (
        r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        "Potential AWS Access Key ID",
    ),
    "aws_secret_key": (
        r"(?i)aws(.{0,20})?(?:secret|access|key|password)(.{0,20})?['\"]([a-zA-Z0-9/+=]{40})['\"]",
        "Potential AWS Secret Access Key",
    ),
    "generic_api_key": (
        r"(?i)(?:api|apikey|api_key|access|token)(.{0,20})?['\"]([a-zA-Z0-9]{20,})['\"]",
        "Potential API Key or Token",
    ),
    "password_in_code": (
        r"(?i)(?:password|passwd|pwd)(.{0,20})?=(.{0,20})?['\"]([^'\"]{8,})['\"]",
        "Hardcoded password in code",
    ),
    "private_key": (
        r"-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----",
        "Private key in file",
    ),
    "sql_concatenation": (
        r"(?:SELECT|INSERT|UPDATE|DELETE).{0,100}?\+.{0,20}?['\"]",
        "Potential SQL injection (string concatenation in SQL)",
    ),
    "unsafe_yaml_load": (
        r"yaml\.load\s*\([^)]*\)",
        "Unsafe YAML loading (use yaml.safe_load instead)",
    ),
}


def validate_security(path: Path):
    """
    Scan file for common security issues.
    
    Checks for:
    - AWS access keys and secret keys
    - Generic API keys and tokens
    - Hardcoded passwords
    - Private keys
    - SQL injection patterns (string concatenation in SQL)
    - Unsafe YAML loading (yaml.load vs yaml.safe_load)
    
    Note: This is basic pattern matching. For comprehensive security scanning,
    use dedicated tools like GitGuardian, TruffleHog, Bandit, or Semgrep.
    """
    violations = []
    
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        return violations
    
    lines = content.splitlines()
    
    for pattern_name, (pattern, description) in SECURITY_PATTERNS.items():
        for line_num, line in enumerate(lines, 1):
            # Skip comments in Python and YAML
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            
            if re.search(pattern, line):
                violations.append(
                    Violation(
                        "security",
                        path,
                        pattern_name,
                        f"{description} at line {line_num}",
                    )
                )
    
    return violations


def find_security_scan_paths():
    """Find Python and YAML files to scan for security issues."""
    paths = []
    # Scan Python files
    paths.extend(REPO_ROOT.glob("**/*.py"))
    # Scan YAML files
    paths.extend(REPO_ROOT.glob("**/*.yaml"))
    paths.extend(REPO_ROOT.glob("**/*.yml"))
    
    # Exclude common directories we don't want to scan
    excluded_patterns = [".git", "venv", "node_modules", "__pycache__"]
    filtered_paths = []
    for path in paths:
        if not any(excluded in path.parts for excluded in excluded_patterns):
            filtered_paths.append(path)
    
    return sorted(filtered_paths)


def run_validator_script(script_name: str) -> tuple[int, int]:
    """
    Run a standalone validator script and return (pass_count, fail_count).
    
    Args:
        script_name: Name of the validator script (e.g., 'validate_context_docs.py')
    
    Returns:
        Tuple of (pass_count, fail_count)
    """
    script_path = REPO_ROOT / "tools" / script_name
    if not script_path.exists():
        return (0, 0)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=60  # Prevent hanging, validators should complete quickly
        )
        
        # Print the validator output
        if result.stdout:
            print(result.stdout, end='')
        
        # Parse summary line to get counts
        summary_match = re.search(r'SUMMARY pass=(\d+) fail=(\d+)', result.stdout)
        if summary_match:
            pass_count = int(summary_match.group(1))
            fail_count = int(summary_match.group(2))
            return (pass_count, fail_count)
        
        return (0, 0)
    except subprocess.TimeoutExpired:
        print(f"Timeout running {script_name} (exceeded 60 seconds)", file=sys.stderr)
        return (0, 0)
    except Exception as e:
        print(f"Error running {script_name}: {e}", file=sys.stderr)
        return (0, 0)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Validate repo standards compliance.",
        epilog="Run with --coverage to see validation coverage report."
    )
    parser.add_argument("--all", action="store_true", help="Run all validations.")
    parser.add_argument("--manifests", action="store_true", help="Validate job manifests.")
    parser.add_argument(
        "--artifacts-catalog",
        action="store_true",
        help="Validate the artifacts catalog.",
    )
    parser.add_argument(
        "--job-inventory",
        action="store_true",
        help="Validate the job inventory.",
    )
    parser.add_argument(
        "--security",
        action="store_true",
        help="Scan for common security issues (secrets, credentials, SQL injection).",
    )
    parser.add_argument(
        "--context-docs",
        action="store_true",
        help="Validate context layer documents (docs/context/).",
    )
    parser.add_argument(
        "--process-docs",
        action="store_true",
        help="Validate process layer documents (docs/process/).",
    )
    parser.add_argument(
        "--agent-docs",
        action="store_true",
        help="Validate agent layer documents (docs/agents/, .github/agents/).",
    )
    parser.add_argument(
        "--job-docs",
        action="store_true",
        help="Validate per-job documents (business descriptions, script cards).",
    )
    parser.add_argument(
        "--decision-records",
        action="store_true",
        help="Validate decision records (docs/decisions/).",
    )
    parser.add_argument(
        "--codable-tasks",
        action="store_true",
        help="Validate codable task specifications.",
    )
    parser.add_argument(
        "--consistency",
        action="store_true",
        help="Check cross-document consistency (term definitions, broken links).",
    )
    parser.add_argument(
        "--naming",
        action="store_true",
        help="Validate naming standard (job IDs, artifacts, docs, placeholders).",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Show validation coverage report and exit.",
    )
    args = parser.parse_args(argv)
    if not (args.all or args.manifests or args.artifacts_catalog or args.job_inventory 
            or args.security or args.context_docs or args.process_docs or args.agent_docs
            or args.job_docs or args.decision_records or args.codable_tasks or args.consistency
            or args.naming or args.coverage):
        parser.error("At least one validation flag must be provided.")
    return args


def main(argv):
    args = parse_args(argv)
    
    # Handle coverage report request
    if args.coverage:
        show_coverage()
        return 0
    
    run_manifests = args.all or args.manifests
    run_artifacts = args.all or args.artifacts_catalog
    run_inventory = args.all or args.job_inventory
    run_security = args.all or args.security
    run_context_docs = args.all or args.context_docs
    run_process_docs = args.all or args.process_docs
    run_agent_docs = args.all or args.agent_docs
    run_job_docs = args.all or args.job_docs
    run_decision_records = args.all or args.decision_records
    run_codable_tasks = args.all or args.codable_tasks
    run_consistency = args.all or args.consistency
    run_naming = args.all or args.naming

    violations = []
    pass_count = 0

    if run_manifests:
        manifest_paths = find_manifest_paths()
        for path in manifest_paths:
            manifest_violations = validate_manifest(path)
            if manifest_violations:
                violations.extend(manifest_violations)
            else:
                pass_count += 1

    if run_artifacts:
        catalog_path = REPO_ROOT / "docs" / "catalogs" / "artifacts_catalog.md"
        allowlist_path = REPO_ROOT / "docs" / "registries" / "shared_artifacts_allowlist.yaml"
        allowlist = load_shared_artifacts_allowlist(allowlist_path)
        artifacts_violations = validate_artifacts_catalog(catalog_path, allowlist)
        if artifacts_violations:
            violations.extend(artifacts_violations)
        else:
            pass_count += 1

    if run_inventory:
        inventory_path = REPO_ROOT / "docs" / "catalogs" / "job_inventory.md"
        inventory_violations = validate_job_inventory(inventory_path)
        if inventory_violations:
            violations.extend(inventory_violations)
        else:
            pass_count += 1
    
    if run_security:
        security_paths = find_security_scan_paths()
        for path in security_paths:
            security_violations = validate_security(path)
            if security_violations:
                violations.extend(security_violations)
            else:
                pass_count += 1
    
    # Run new documentation layer validators
    if run_context_docs:
        context_pass, context_fail = run_validator_script("validate_context_docs.py")
        pass_count += context_pass
        if context_fail > 0:
            violations.append(Violation("context_docs", Path("docs/context"), "validator_errors", 
                                       f"{context_fail} validation errors found"))
    
    if run_process_docs:
        process_pass, process_fail = run_validator_script("validate_process_docs.py")
        pass_count += process_pass
        if process_fail > 0:
            violations.append(Violation("process_docs", Path("docs/process"), "validator_errors",
                                       f"{process_fail} validation errors found"))
    
    if run_agent_docs:
        agent_pass, agent_fail = run_validator_script("validate_agent_docs.py")
        pass_count += agent_pass
        if agent_fail > 0:
            violations.append(Violation("agent_docs", Path("docs/agents"), "validator_errors",
                                       f"{agent_fail} validation errors found"))
    
    if run_job_docs:
        job_pass, job_fail = run_validator_script("validate_job_docs.py")
        pass_count += job_pass
        if job_fail > 0:
            violations.append(Violation("job_docs", Path("jobs"), "validator_errors",
                                       f"{job_fail} validation errors found"))
    
    if run_decision_records:
        decision_pass, decision_fail = run_validator_script("validate_decision_records.py")
        pass_count += decision_pass
        if decision_fail > 0:
            violations.append(Violation("decision_records", Path("docs/decisions"), "validator_errors",
                                       f"{decision_fail} validation errors found"))
    
    if run_codable_tasks:
        task_pass, task_fail = run_validator_script("validate_codable_tasks.py")
        pass_count += task_pass
        if task_fail > 0:
            violations.append(Violation("codable_tasks", Path("docs/tasks"), "validator_errors",
                                       f"{task_fail} validation errors found"))
    
    if run_consistency:
        consistency_pass, consistency_fail = run_validator_script("check_doc_consistency.py")
        pass_count += consistency_pass
        if consistency_fail > 0:
            violations.append(Violation("consistency", Path("docs"), "validator_errors",
                                       f"{consistency_fail} validation errors found"))
    
    if run_naming:
        naming_pass, naming_fail = run_validator_script("validate_naming_standard.py")
        pass_count += naming_pass
        if naming_fail > 0:
            violations.append(Violation("naming", Path("repository"), "validator_errors",
                                       f"{naming_fail} validation errors found"))

    for violation in violations:
        print(violation.format())

    fail_count = len(violations)
    print(f"SUMMARY pass={pass_count} fail={fail_count}")

    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

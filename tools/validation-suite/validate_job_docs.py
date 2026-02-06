#!/usr/bin/env python3
"""
Per-Job Document Validator

Validates per-job documentation:
- Business job descriptions (bus_description_*.md)
- Script cards (script_card_*.md)
- Consistency between manifest and descriptions

Per-job documents provide business and operational context for individual jobs.
"""
import re
import sys
from pathlib import Path
from typing import List, Set

import yaml

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


def validate_business_description(path: Path) -> List[Violation]:
    """Validate business job description structure per business_job_description_spec.md Section 2.
    
    The spec requires 8 numbered sections in exact order:
    1. Business purpose and context
    2. Inputs (business view)
    3. Outputs (business view)
    4. Processing logic (business flow)
    5. Business rules and controls
    6. What the job does not do
    7. Operational notes (optional)
    8. Evidence notes and assumptions
    """
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections per spec Section 2
    required_sections = [
        (r"## 1\).*[Bb]usiness purpose", "## 1) Business purpose and context"),
        (r"## 2\).*[Ii]nputs", "## 2) Inputs (business view)"),
        (r"## 3\).*[Oo]utputs", "## 3) Outputs (business view)"),
        (r"## 4\).*[Pp]rocessing logic", "## 4) Processing logic (business flow)"),
        (r"## 5\).*[Bb]usiness rules", "## 5) Business rules and controls"),
        (r"## 6\).*[Dd]oes not do", "## 6) What the job does not do"),
        (r"## 8\).*[Ee]vidence", "## 8) Evidence notes and assumptions"),
    ]
    
    # Section 7 is optional, so we don't check for it
    
    # Check for title (# header)
    if not re.search(r"^# ", content, re.MULTILINE):
        violations.append(Violation(
            "job_docs", path, "missing_title",
            "Business description must have a top-level title (# header)"
        ))
    
    # Check each required section
    for pattern, section_name in required_sections:
        if not re.search(pattern, content):
            violations.append(Violation(
                "job_docs", path, "missing_required_section",
                f"Business description must include section: {section_name}"
            ))
    
    # Check section order (sections should appear in numbered order)
    # Extract all numbered section headings
    section_matches = list(re.finditer(r"## (\d+)\)", content))
    if section_matches:
        section_numbers = [int(m.group(1)) for m in section_matches]
        # Check if they are in ascending order (allowing gaps for optional sections)
        for i in range(len(section_numbers) - 1):
            if section_numbers[i] >= section_numbers[i + 1]:
                violations.append(Violation(
                    "job_docs", path, "section_order",
                    f"Sections must be in numbered order: found section {section_numbers[i]} before {section_numbers[i + 1]}"
                ))
                break
    
    return violations


def validate_script_card(path: Path) -> List[Violation]:
    """Validate script card structure per script_card_spec.md Section 2.
    
    The spec requires 10 sections (9 MUST + 1 OPTIONAL):
    2.1 Identity (MUST) - 5 required fields
    2.2 Purpose (MUST)
    2.3 Trigger and Parameters (MUST)
    2.3A Configuration Files (OPTIONAL)
    2.4 Interface: Inputs (MUST)
    2.5 Interface: Outputs (MUST)
    2.6 Side Effects (MUST)
    2.7 Runtime Behavior (MUST)
    2.8 Invariants (MUST)
    2.9 Failure Modes and Observability (MUST)
    2.10 References (MUST)
    """
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Check for title
    if not re.search(r"^# ", content, re.MULTILINE):
        violations.append(Violation(
            "job_docs", path, "missing_title",
            "Script card must have a top-level title (# header)"
        ))
    
    # Required sections per spec
    required_sections = [
        (r"## Identity|## 2\.1", "## Identity (or ## 2.1)"),
        (r"## Purpose|## 2\.2", "## Purpose (or ## 2.2)"),
        (r"## Trigger and [Pp]arameters|## 2\.3", "## Trigger and Parameters (or ## 2.3)"),
        (r"## Interface:? Inputs|## 2\.4", "## Interface: Inputs (or ## 2.4)"),
        (r"## Interface:? Outputs|## 2\.5", "## Interface: Outputs (or ## 2.5)"),
        (r"## Side [Ee]ffects|## 2\.6", "## Side Effects (or ## 2.6)"),
        (r"## Runtime [Bb]ehavior|## 2\.7", "## Runtime Behavior (or ## 2.7)"),
        (r"## Invariants|## 2\.8", "## Invariants (or ## 2.8)"),
        (r"## Failure [Mm]odes|## 2\.9", "## Failure Modes and Observability (or ## 2.9)"),
        (r"## References|## 2\.10", "## References (or ## 2.10)"),
    ]
    
    for pattern, section_name in required_sections:
        if not re.search(pattern, content):
            violations.append(Violation(
                "job_docs", path, "missing_required_section",
                f"Script card must include section: {section_name}"
            ))
    
    # Check Identity section has required fields (if section exists)
    if re.search(r"## Identity|## 2\.1", content):
        identity_fields = [
            (r"job_id", "job_id"),
            (r"glue_job_name", "glue_job_name"),
            (r"runtime", "runtime"),
            (r"repo_path", "repo_path"),
            (r"manifest_path", "manifest_path"),
        ]
        for field_pattern, field_name in identity_fields:
            if not re.search(field_pattern, content):
                violations.append(Violation(
                    "job_docs", path, "missing_identity_field",
                    f"Identity section must include field: {field_name}"
                ))
    
    return violations


def check_manifest_consistency(job_dir: Path) -> List[Violation]:
    """Check consistency between manifest and per-job descriptions."""
    violations = []
    
    manifest_path = job_dir / "job_manifest.yaml"
    if not manifest_path.exists():
        return violations
    
    # Load manifest
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        return violations  # Manifest validation is handled elsewhere
    
    if not isinstance(manifest, dict):
        return violations
    
    job_id = manifest.get("job_id")
    if not job_id:
        return violations
    
    # Check for business description
    expected_bus_desc = job_dir / f"bus_description_{job_id}.md"
    if not expected_bus_desc.exists():
        # Business descriptions are not required for all jobs yet
        # This is informational rather than an error
        pass
    
    # Check for script card
    expected_script_card = job_dir / f"script_card_{job_id}.md"
    if not expected_script_card.exists():
        # Script cards are not required for all jobs yet
        pass
    
    return violations


def validate_job_docs() -> List[Violation]:
    """Validate all per-job documentation."""
    violations = []
    
    jobs_base = TOOL_PATHS.jobs_root
    
    if not jobs_base.exists():
        return violations
    
    # Find all job directories (those with job_manifest.yaml)
    for manifest_path in jobs_base.glob("*/*/job_manifest.yaml"):
        job_dir = manifest_path.parent
        
        # Validate business descriptions
        for bus_desc in job_dir.glob("bus_description_*.md"):
            violations.extend(validate_business_description(bus_desc))
        
        # Validate script cards
        for script_card in job_dir.glob("script_card_*.md"):
            violations.extend(validate_script_card(script_card))
        
        # Check consistency
        violations.extend(check_manifest_consistency(job_dir))
    
    return violations


def main():
    violations = validate_job_docs()
    
    for violation in violations:
        print(violation.format())
    
    # Count files that were successfully validated (exist and have no violations)
    jobs_base = TOOL_PATHS.jobs_root
    job_doc_files = []
    if jobs_base.exists():
        job_doc_files.extend(jobs_base.glob("*/*/bus_description_*.md"))
        job_doc_files.extend(jobs_base.glob("*/*/script_card_*.md"))
    
    files_with_violations = set(v.path for v in violations)
    pass_count = sum(1 for f in job_doc_files if f.exists() and f not in files_with_violations)
    fail_count = len(violations)
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

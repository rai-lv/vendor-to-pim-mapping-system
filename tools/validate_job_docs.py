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

REPO_ROOT = Path(__file__).resolve().parents[1]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def validate_business_description(path: Path) -> List[Violation]:
    """Validate business job description structure per spec."""
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections based on business_job_description_spec.md
    # Section 1: Business purpose and context
    # Section 2-7: Variable depending on the document
    # At minimum, we check for:
    # - A title (# header)
    # - Business purpose section
    # - Inputs/outputs sections
    # - Boundary statement
    
    # Check for a title (# or ## header at start)
    if not re.search(r"^##? ", content, re.MULTILINE):
        violations.append(Violation(
            "job_docs", path, "missing_title",
            "Business description must have a title (# or ## header)"
        ))
    
    # Check for business purpose (flexible pattern)
    has_purpose = (
        re.search(r"## .*[Pp]urpose", content) or
        re.search(r"[Bb]usiness purpose", content)
    )
    if not has_purpose:
        violations.append(Violation(
            "job_docs", path, "missing_business_purpose",
            "Business description should include business purpose section"
        ))
    
    # Check for inputs section
    has_inputs = re.search(r"## .*[Ii]nputs", content)
    if not has_inputs:
        violations.append(Violation(
            "job_docs", path, "missing_inputs_section",
            "Business description should include inputs section"
        ))
    
    # Check for outputs section (flexible patterns)
    has_outputs = (
        re.search(r"## .*[Oo]utputs?", content) or
        re.search(r"## .*[Oo]utput files?", content)
    )
    if not has_outputs:
        violations.append(Violation(
            "job_docs", path, "missing_outputs_section",
            "Business description should include outputs section"
        ))
    
    # Check for boundary statement (flexible patterns)
    has_boundary = (
        re.search(r"[Dd]oes not", content) or
        re.search(r"[Bb]oundary", content) or
        re.search(r"not do", content, re.IGNORECASE)
    )
    if not has_boundary:
        violations.append(Violation(
            "job_docs", path, "missing_boundary",
            "Business description should include explicit boundary statement"
        ))
    
    return violations


def validate_script_card(path: Path) -> List[Violation]:
    """Validate script card structure per spec."""
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections based on script_card_spec.md
    # Script cards document operational behavior
    
    if not re.search(r"^# ", content, re.MULTILINE):
        violations.append(Violation(
            "job_docs", path, "missing_title",
            "Script card must have a title (# header)"
        ))
    
    # Check for key operational sections
    operational_sections = [
        r"## .*[Rr]untime",
        r"## .*[Ff]ailure",
        r"## .*[Ii]nvariants",
    ]
    
    for pattern in operational_sections:
        if not re.search(pattern, content):
            violations.append(Violation(
                "job_docs", path, "missing_operational_section",
                f"Script card should include operational section matching pattern: {pattern}"
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
    
    jobs_base = REPO_ROOT / "jobs"
    
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
    jobs_base = REPO_ROOT / "jobs"
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

#!/usr/bin/env python3
"""
Decision Records Validator

Validates decision records structure and consistency:
- Individual decision records (docs/decisions/*.md)
- Decision log index (docs/catalogs/decision_log.md)

Decision records document significant architectural and design decisions.
"""
import re
import sys
from pathlib import Path
from typing import List, Set, Dict

REPO_ROOT = Path(__file__).resolve().parents[1]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def validate_decision_record(path: Path) -> List[Violation]:
    """Validate individual decision record structure."""
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections for decision records (based on common ADR format)
    required_sections = [
        "# ",  # Title
        "## Status",
        "## Context",
        "## Decision",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "decision_records", path, "missing_section",
                f"Missing required section: {section.strip()}"
            ))
    
    # Check status value (if Status section exists)
    if "## Status" in content:
        status_section_start = content.find("## Status")
        status_section_end = content.find("\n## ", status_section_start + 10)
        if status_section_end == -1:
            status_section = content[status_section_start:]
        else:
            status_section = content[status_section_start:status_section_end]
        
        # Common status values
        valid_statuses = ["proposed", "accepted", "rejected", "deprecated", "superseded"]
        has_valid_status = any(status.lower() in status_section.lower() for status in valid_statuses)
        
        if not has_valid_status:
            violations.append(Violation(
                "decision_records", path, "invalid_status",
                f"Status should be one of: {', '.join(valid_statuses)}"
            ))
    
    return violations


def validate_decision_log(path: Path) -> List[Violation]:
    """Validate decision_log.md structure and index consistency."""
    violations = []
    
    if not path.exists():
        # Decision log is optional if no decisions exist
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Check for required structure
    if "# Decision Log" not in content:
        violations.append(Violation(
            "decision_records", path, "missing_title",
            "Decision log must have '# Decision Log' title"
        ))
    
    return violations


def check_decision_log_consistency(log_path: Path, decisions_dir: Path) -> List[Violation]:
    """Check that decision_log.md index is consistent with actual decision files."""
    violations = []
    
    if not log_path.exists() or not decisions_dir.exists():
        return violations
    
    log_content = log_path.read_text(encoding="utf-8")
    
    # Find all decision record files
    decision_files = set()
    if decisions_dir.exists():
        for file_path in decisions_dir.glob("*.md"):
            if file_path.name != "README.md":
                decision_files.add(file_path.name)
    
    # Check if decision files are referenced in the log
    # This is a basic check - we look for the filename or a link to it
    for decision_file in decision_files:
        if decision_file not in log_content:
            violations.append(Violation(
                "decision_records", log_path, "missing_log_entry",
                f"Decision file '{decision_file}' not referenced in decision log"
            ))
    
    return violations


def validate_decision_records() -> List[Violation]:
    """Validate all decision records and the decision log."""
    violations = []
    
    decisions_dir = REPO_ROOT / "docs" / "decisions"
    log_path = REPO_ROOT / "docs" / "catalogs" / "decision_log.md"
    
    # Validate decision log
    violations.extend(validate_decision_log(log_path))
    
    # Validate individual decision records
    if decisions_dir.exists():
        for decision_path in decisions_dir.glob("*.md"):
            if decision_path.name != "README.md":
                violations.extend(validate_decision_record(decision_path))
    
    # Check consistency between log and individual records
    violations.extend(check_decision_log_consistency(log_path, decisions_dir))
    
    return violations


def main():
    violations = validate_decision_records()
    
    for violation in violations:
        print(violation.format())
    
    # Count files
    decisions_dir = REPO_ROOT / "docs" / "decisions"
    decision_count = 0
    if decisions_dir.exists():
        decision_count = len([f for f in decisions_dir.glob("*.md") if f.name != "README.md"])
    
    log_path = REPO_ROOT / "docs" / "catalogs" / "decision_log.md"
    total_files = decision_count + (1 if log_path.exists() else 0)
    
    files_with_violations = len(set(v.path for v in violations))
    pass_count = total_files - files_with_violations
    fail_count = len(violations)
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

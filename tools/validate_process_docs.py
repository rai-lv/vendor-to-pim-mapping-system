#!/usr/bin/env python3
"""
Process Layer Documentation Validator

Validates the structure and consistency of process layer documents in docs/process/:
- workflow_guide.md
- contribution_approval_guide.md

These documents define workflows, approval gates, and contribution processes.
"""
import re
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def validate_workflow_guide(path: Path) -> List[Violation]:
    """Validate workflow_guide.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "process_docs", path, "missing_file",
            "workflow_guide.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required top-level sections
    required_sections = [
        "## Purpose statement",
        "## Scope and non-goals",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "process_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    # Check for 5 workflow steps (## 2 through ## 6)
    step_sections = []
    for i in range(1, 6):
        # Pattern: "## N) Step M" where N = i+1, M = i
        pattern = f"## {i+1}) Step {i}"
        if pattern not in content:
            violations.append(Violation(
                "process_docs", path, "missing_step",
                f"Missing workflow step: Step {i}"
            ))
        else:
            step_sections.append(i)
    
    # Each step should have standard subsections
    required_subsections = [
        "### Practical goal",
        "### Entry criteria",
        "### What to do",
        "### Exit criteria",
        "### Approval gate",
        "### Escalation triggers",
    ]
    
    for step_num in step_sections:
        # Find the step section
        step_pattern = f"## {step_num+1}) Step {step_num}"
        if step_pattern in content:
            step_start = content.find(step_pattern)
            # Find next ## section at start of line
            search_from = step_start + len(step_pattern)
            next_section_pos = -1
            while True:
                pos = content.find("\n##", search_from)
                if pos == -1:
                    break
                # Check if it's actually a ## at start of line (not ###)
                if pos + 3 < len(content) and content[pos+3] != '#':
                    next_section_pos = pos
                    break
                search_from = pos + 1
            
            if next_section_pos == -1:
                step_content = content[step_start:]
            else:
                step_content = content[step_start:next_section_pos]
            
            # Check for required subsections (allow for variations like "Exit criteria (human-checkable)")
            for subsection in required_subsections:
                # Be flexible - just check if the key part is present
                key_text = subsection.replace("###", "").strip()
                if f"### {key_text}" not in step_content:
                    violations.append(Violation(
                        "process_docs", path, "missing_subsection",
                        f"Step {step_num} missing required subsection: {key_text}"
                    ))
    
    return violations


def validate_contribution_approval_guide(path: Path) -> List[Violation]:
    """Validate contribution_approval_guide.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "process_docs", path, "missing_file",
            "contribution_approval_guide.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections
    required_sections = [
        "# Contribution and Approval Guide",
        "## Purpose Statement",
        "# 1. What Constitutes a Contribution",
        "# 2. Approval Gate Requirements Per Workflow Step",
        "# 3. Approval Evidence Expectations",
        "# 4. Review Expectations",
        "# 5. Decision Recording Guidance",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "process_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    # Check for per-step approval requirements (2.1 through 2.5)
    for i in range(1, 6):
        pattern = f"## 2.{i}"
        if pattern not in content:
            violations.append(Violation(
                "process_docs", path, "missing_step_approval",
                f"Missing approval requirements for workflow step {i} (section 2.{i})"
            ))
    
    return violations


def check_conflicting_procedures(workflow_path: Path, approval_path: Path) -> List[Violation]:
    """Check for conflicting procedures between workflow_guide and contribution_approval_guide."""
    violations = []
    
    if not workflow_path.exists() or not approval_path.exists():
        return violations
    
    # This is a basic check - we can expand it later with more sophisticated analysis
    # For now, just ensure both documents reference the same 5-step process
    
    workflow_content = workflow_path.read_text(encoding="utf-8")
    approval_content = approval_path.read_text(encoding="utf-8")
    
    # Check that both documents reference the same steps
    for i in range(1, 6):
        step_in_workflow = f"Step {i}" in workflow_content
        step_in_approval = f"step {i}" in approval_content.lower() or f"Step {i}" in approval_content
        
        if step_in_workflow and not step_in_approval:
            violations.append(Violation(
                "process_docs", approval_path, "missing_step_reference",
                f"Approval guide does not reference Step {i} mentioned in workflow guide"
            ))
    
    return violations


def validate_process_layer() -> List[Violation]:
    """Validate all process layer documents."""
    violations = []
    
    process_dir = REPO_ROOT / "docs" / "process"
    
    # Validate each document
    workflow_path = process_dir / "workflow_guide.md"
    approval_path = process_dir / "contribution_approval_guide.md"
    
    violations.extend(validate_workflow_guide(workflow_path))
    violations.extend(validate_contribution_approval_guide(approval_path))
    
    # Check for conflicts between documents
    violations.extend(check_conflicting_procedures(workflow_path, approval_path))
    
    return violations


def main():
    violations = validate_process_layer()
    
    for violation in violations:
        print(violation.format())
    
    # Count files that were successfully validated (exist and have no violations)
    process_dir = REPO_ROOT / "docs" / "process"
    process_files = [
        process_dir / "workflow_guide.md",
        process_dir / "contribution_approval_guide.md",
    ]
    
    files_with_violations = set(v.path for v in violations)
    pass_count = sum(1 for f in process_files if f.exists() and f not in files_with_violations)
    fail_count = len(violations)
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

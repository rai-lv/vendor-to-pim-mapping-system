#!/usr/bin/env python3
"""
Codable Task Specification Validator

Validates codable task specifications per docs/standards/codable_task_spec.md.

Codable tasks are bounded units of implementation work created during Step 3
(Capability Planning) and executed during Step 4 (Execute Development Tasks).

Required structure per spec:
- Task identity (task identifier, parent capability)
- Task purpose (1-3 sentences)
- Task boundaries (in-scope, out-of-scope)
- Dependencies (prerequisite tasks, required inputs, external dependencies)
- Intended outputs (artifacts, changes, states)
- Acceptance criteria (evaluable pass/fail conditions)
"""
import re
import sys
from pathlib import Path
from typing import List

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


def validate_codable_task(path: Path) -> List[Violation]:
    """Validate a codable task specification file."""
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections per codable_task_spec.md Section 2
    required_patterns = [
        (r"[Tt]ask identifier:", "task_identity", "Task identifier field"),
        (r"[Pp]arent capability:", "parent_capability", "Parent capability field"),
        (r"[Tt]ask purpose", "task_purpose", "Task purpose section"),
        (r"[Ii]n scope:|[Ww]hat .* does:", "in_scope", "In-scope boundaries"),
        (r"[Oo]ut of scope|does NOT|does not do", "out_of_scope", "Out-of-scope boundaries"),
        (r"[Dd]ependencies", "dependencies", "Dependencies section"),
        (r"[Ii]ntended outputs", "outputs", "Intended outputs section"),
        (r"[Aa]cceptance criteria", "acceptance_criteria", "Acceptance criteria section"),
    ]
    
    for pattern, rule_id, description in required_patterns:
        if not re.search(pattern, content, re.IGNORECASE):
            violations.append(Violation(
                "codable_task", path, f"missing_{rule_id}",
                f"Missing required {description}"
            ))
    
    # Check for task purpose length (should be 1-3 sentences, roughly 50-300 chars)
    purpose_match = re.search(r"[Tt]ask purpose[:\s]+(.*?)(?=\n\n|\n#|\Z)", content, re.DOTALL | re.IGNORECASE)
    if purpose_match:
        purpose_text = purpose_match.group(1).strip()
        # Count sentences (rough heuristic: count periods, exclamation marks, question marks)
        # Note: This will miscount abbreviations (e.g., U.S., Dr.) but serves as a rough check
        sentence_count = len(re.findall(r'[.!?]', purpose_text))
        if sentence_count > 5:
            violations.append(Violation(
                "codable_task", path, "verbose_purpose",
                f"Task purpose should be 1-3 sentences, found ~{sentence_count} sentences"
            ))
    
    # Check acceptance criteria exist and are structured
    ac_match = re.search(r"[Aa]cceptance criteria[:\s]+(.*?)(?=\n\n#|\Z)", content, re.DOTALL | re.IGNORECASE)
    if ac_match:
        ac_text = ac_match.group(1).strip()
        # Count numbered or bulleted items
        criteria_count = len(re.findall(r'^\s*[\d\-\*]+[\.\):]?\s+', ac_text, re.MULTILINE))
        if criteria_count == 0:
            violations.append(Violation(
                "codable_task", path, "unstructured_criteria",
                "Acceptance criteria should be a numbered or bulleted list"
            ))
    
    return violations


def find_codable_task_files() -> List[Path]:
    """Find all codable task specification files in the repository."""
    search_patterns = [
        TOOL_PATHS.docs_tasks,
        TOOL_PATHS.jobs_root,
    ]
    
    task_files = []
    for base_path in search_patterns:
        if base_path.exists():
            # Find files with task-related names
            task_files.extend(base_path.glob("**/codable_task_*.md"))
            task_files.extend(base_path.glob("**/task_*.md"))
            # Also check for tasks directories
            for tasks_dir in base_path.glob("**/tasks"):
                if tasks_dir.is_dir():
                    task_files.extend(tasks_dir.glob("*.md"))
    
    # Remove duplicates and filter out README files
    return [f for f in set(task_files) if f.name.lower() != "readme.md"]


def validate_codable_tasks() -> List[Violation]:
    """Validate all codable task specification files in the repository."""
    violations = []
    
    task_files = find_codable_task_files()
    
    for task_file in task_files:
        violations.extend(validate_codable_task(task_file))
    
    return violations


def main():
    violations = validate_codable_tasks()
    
    for violation in violations:
        print(violation.format())
    
    # Count files that were successfully validated
    task_files = find_codable_task_files()
    
    files_with_violations = set(v.path for v in violations)
    pass_count = sum(1 for f in task_files if f not in files_with_violations)
    fail_count = len(violations)
    
    if not task_files:
        print("INFO: No codable task files found (validator ready for when tasks are created)")
        pass_count = 0
        fail_count = 0
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

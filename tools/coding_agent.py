#!/usr/bin/env python3
"""
Coding Agent - Code Implementation Helper

This agent assists with implementing code tasks from specifications, ensuring
adherence to repository standards and best practices (DRY, SOLID).

Trigger: Approval of subsystem specifications
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
JOBS_DIR = REPO_ROOT / "jobs"

# Constants
MIN_FILE_SIZE_FOR_DUPLICATE_CHECK = 100  # bytes


def get_specification(spec_name: str) -> dict:
    """Load a specification file."""
    spec_path = SPECIFICATIONS_DIR / f"{spec_name}.yaml"
    
    if not spec_path.exists():
        raise FileNotFoundError(f"Specification not found: {spec_path}")
    
    with spec_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_coding_tasks(spec_name: str) -> int:
    """
    List all coding tasks from a specification.
    
    Args:
        spec_name: Name of the specification (without .yaml extension)
        
    Returns:
        0 on success, 1 on error
    """
    try:
        spec = get_specification(spec_name)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Failed to load specification: {e}", file=sys.stderr)
        return 1
    
    tasks = spec.get("coding_tasks", [])
    
    if not tasks:
        print(f"No coding tasks found in specification: {spec_name}")
        return 0
    
    print(f"Coding tasks for: {spec.get('subsystem_name', spec_name)}")
    print("=" * 80)
    
    for task in tasks:
        task_id = task.get("task_id", "?")
        description = task.get("description", "No description")
        complexity = task.get("estimated_complexity", "unknown")
        dependencies = task.get("dependencies", [])
        files = task.get("files_affected", [])
        
        print(f"\nTask {task_id}: {description}")
        print(f"  Complexity: {complexity}")
        if dependencies:
            print(f"  Depends on: {', '.join(map(str, dependencies))}")
        if files:
            print(f"  Files: {', '.join(files)}")
        
        acceptance = task.get("acceptance_criteria", [])
        if acceptance:
            print(f"  Acceptance criteria:")
            for criterion in acceptance:
                print(f"    - {criterion}")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(tasks)} task(s)")
    
    return 0


def validate_code() -> int:
    """
    Run repository validation checks.
    
    Returns:
        0 if validation passes, 1 if validation fails
    """
    validator_path = REPO_ROOT / "tools" / "validate_repo_docs.py"
    
    if not validator_path.exists():
        print("Warning: validate_repo_docs.py not found, skipping validation", file=sys.stderr)
        return 0
    
    print("Running repository validation...")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(validator_path), "--all"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print("-" * 60)
            print("✓ Validation passed")
        else:
            print("-" * 60)
            print("✗ Validation failed")
        
        return result.returncode
    except Exception as e:
        print(f"Error: Failed to run validation: {e}", file=sys.stderr)
        return 1


def check_best_practices() -> int:
    """
    Run basic best practices checks.
    
    Returns:
        0 on success, 1 on warnings found
    """
    print("Checking best practices...")
    print("-" * 60)
    
    warnings = []
    
    # Check for Python files with TODO comments
    python_files = list(JOBS_DIR.rglob("*.py"))
    
    for py_file in python_files:
        try:
            content = py_file.read_text(encoding="utf-8")
            if "TODO" in content:
                warnings.append(f"TODO found in {py_file.relative_to(REPO_ROOT)}")
        except:
            pass
    
    # Check for duplicate code (simple heuristic: files with same size)
    file_sizes = {}
    for py_file in python_files:
        size = py_file.stat().st_size
        if size > MIN_FILE_SIZE_FOR_DUPLICATE_CHECK:
            if size in file_sizes:
                file_sizes[size].append(py_file)
            else:
                file_sizes[size] = [py_file]
    
    for size, files in file_sizes.items():
        if len(files) > 1:
            warnings.append(f"Potential duplicate code (same size {size}): {', '.join(f.name for f in files)}")
    
    if warnings:
        print("⚠ Best practice warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print("\nNote: These are informational warnings, not errors.")
        return 1
    else:
        print("✓ No obvious best practice issues found")
    
    print("-" * 60)
    return 0


def generate_codex_task_outline(spec_name: str, task_id: int) -> int:
    """
    Generate a Codex task outline for a specific coding task.
    
    Args:
        spec_name: Name of the specification
        task_id: ID of the coding task
        
    Returns:
        0 on success, 1 on error
    """
    try:
        spec = get_specification(spec_name)
    except Exception as e:
        print(f"Error: Failed to load specification: {e}", file=sys.stderr)
        return 1
    
    tasks = spec.get("coding_tasks", [])
    task = None
    
    for t in tasks:
        if t.get("task_id") == task_id:
            task = t
            break
    
    if not task:
        print(f"Error: Task {task_id} not found in specification", file=sys.stderr)
        return 1
    
    print(f"# Codex Task Outline: {spec.get('subsystem_name')} - Task {task_id}")
    print("=" * 80)
    print()
    print(f"## Task Description")
    print(f"{task.get('description', 'No description')}")
    print()
    print(f"## Objective")
    print(f"{spec.get('objective', {}).get('description', 'See specification')}")
    print()
    print(f"## Files to Modify/Create")
    for file_path in task.get("files_affected", []):
        print(f"- {file_path}")
    print()
    print(f"## Acceptance Criteria")
    for criterion in task.get("acceptance_criteria", []):
        print(f"- {criterion}")
    print()
    print(f"## Dependencies")
    dependencies = task.get("dependencies", [])
    if dependencies:
        print(f"Must complete tasks: {', '.join(map(str, dependencies))}")
    else:
        print("No dependencies")
    print()
    print(f"## Quality Gates")
    print("- Code must pass `python tools/validate_repo_docs.py --all`")
    print("- Follow DRY (Don't Repeat Yourself) principle")
    print("- Follow SOLID principles where applicable")
    print("- Add appropriate error handling")
    print("- Update relevant documentation")
    print()
    print(f"## Estimated Complexity")
    print(f"{task.get('estimated_complexity', 'unknown').upper()}")
    
    return 0


def main():
    """Main entry point for the coding agent."""
    parser = argparse.ArgumentParser(
        description="Coding Agent - Code implementation helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List coding tasks from a specification
  python coding_agent.py tasks vendor_ingestion_pipeline
  
  # Validate repository code and documentation
  python coding_agent.py validate
  
  # Check best practices
  python coding_agent.py check
  
  # Generate Codex task outline
  python coding_agent.py codex-task vendor_ingestion_pipeline 1
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Tasks command
    tasks_parser = subparsers.add_parser("tasks", help="List coding tasks from a specification")
    tasks_parser.add_argument("spec_name", help="Specification name (without .yaml)")
    
    # Validate command
    subparsers.add_parser("validate", help="Run repository validation")
    
    # Check command
    subparsers.add_parser("check", help="Run best practices checks")
    
    # Codex task command
    codex_parser = subparsers.add_parser("codex-task", help="Generate Codex task outline")
    codex_parser.add_argument("spec_name", help="Specification name (without .yaml)")
    codex_parser.add_argument("task_id", type=int, help="Task ID")
    
    args = parser.parse_args()
    
    if args.command == "tasks":
        return list_coding_tasks(args.spec_name)
    elif args.command == "validate":
        return validate_code()
    elif args.command == "check":
        return check_best_practices()
    elif args.command == "codex-task":
        return generate_codex_task_outline(args.spec_name, args.task_id)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

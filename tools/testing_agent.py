#!/usr/bin/env python3
"""
Testing Agent - Code Validation and Testing

This agent validates code contributions by inferring test cases from objectives
and specifications, ensuring adherence to CI requirements.

Output: logs/tests_logs/<test_run_timestamp>.log
Trigger: New code submissions
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
TESTS_LOGS_DIR = REPO_ROOT / "logs" / "tests_logs"
JOBS_DIR = REPO_ROOT / "jobs"


def run_validation_tests() -> tuple[int, str]:
    """
    Run repository validation tests.
    
    Returns:
        Tuple of (return_code, output)
    """
    validator_path = REPO_ROOT / "tools" / "validate_repo_docs.py"
    
    if not validator_path.exists():
        return 1, "Error: validate_repo_docs.py not found"
    
    try:
        result = subprocess.run(
            [sys.executable, str(validator_path), "--all"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        output = result.stdout + "\n" + result.stderr
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 1, "Error: Validation timed out after 5 minutes"
    except Exception as e:
        return 1, f"Error: Failed to run validation: {e}"


def check_python_syntax() -> tuple[int, str]:
    """
    Check Python syntax for all job scripts.
    
    Returns:
        Tuple of (return_code, output)
    """
    python_files = list(JOBS_DIR.rglob("*.py"))
    
    if not python_files:
        return 0, "No Python files found in jobs directory"
    
    errors = []
    for py_file in python_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(f"{py_file.relative_to(REPO_ROOT)}: {result.stderr}")
        except Exception as e:
            errors.append(f"{py_file.relative_to(REPO_ROOT)}: {e}")
    
    if errors:
        return 1, "Python syntax errors:\n" + "\n".join(errors)
    else:
        return 0, f"✓ All {len(python_files)} Python files have valid syntax"


def check_yaml_syntax() -> tuple[int, str]:
    """
    Check YAML syntax for manifests and specifications.
    
    Returns:
        Tuple of (return_code, output)
    """
    yaml_files = []
    yaml_files.extend(JOBS_DIR.rglob("*.yaml"))
    yaml_files.extend(JOBS_DIR.rglob("*.yml"))
    if SPECIFICATIONS_DIR.exists():
        yaml_files.extend(SPECIFICATIONS_DIR.rglob("*.yaml"))
        yaml_files.extend(SPECIFICATIONS_DIR.rglob("*.yml"))
    
    if not yaml_files:
        return 0, "No YAML files found"
    
    errors = []
    for yaml_file in yaml_files:
        try:
            with yaml_file.open("r", encoding="utf-8") as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"{yaml_file.relative_to(REPO_ROOT)}: {e}")
        except Exception as e:
            errors.append(f"{yaml_file.relative_to(REPO_ROOT)}: {e}")
    
    if errors:
        return 1, "YAML syntax errors:\n" + "\n".join(errors)
    else:
        return 0, f"✓ All {len(yaml_files)} YAML files have valid syntax"


def infer_tests_from_specification(spec_name: str) -> tuple[int, str]:
    """
    Infer test requirements from a specification.
    
    Args:
        spec_name: Name of the specification (without .yaml extension)
        
    Returns:
        Tuple of (return_code, output)
    """
    spec_path = SPECIFICATIONS_DIR / f"{spec_name}.yaml"
    
    if not spec_path.exists():
        return 1, f"Error: Specification not found: {spec_path}"
    
    try:
        with spec_path.open("r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        return 1, f"Error: Failed to load specification: {e}"
    
    output = [f"Test Requirements for: {spec.get('subsystem_name', spec_name)}"]
    output.append("=" * 80)
    
    # Extract test requirements
    test_reqs = spec.get("testing_requirements", {})
    
    unit_tests = test_reqs.get("unit_tests", [])
    if unit_tests:
        output.append("\nUnit Tests:")
        for test in unit_tests:
            output.append(f"  - {test}")
    
    integration_tests = test_reqs.get("integration_tests", [])
    if integration_tests:
        output.append("\nIntegration Tests:")
        for test in integration_tests:
            output.append(f"  - {test}")
    
    test_data = test_reqs.get("test_data", "")
    if test_data:
        output.append(f"\nTest Data: {test_data}")
    
    # Extract acceptance criteria from coding tasks
    tasks = spec.get("coding_tasks", [])
    if tasks:
        output.append("\n\nAcceptance Criteria by Task:")
        for task in tasks:
            task_id = task.get("task_id", "?")
            description = task.get("description", "No description")
            output.append(f"\nTask {task_id}: {description}")
            
            criteria = task.get("acceptance_criteria", [])
            if criteria:
                for criterion in criteria:
                    output.append(f"  ✓ {criterion}")
    
    return 0, "\n".join(output)


def run_full_test_suite(spec_name: str = None, log: bool = True) -> int:
    """
    Run the full test suite.
    
    Args:
        spec_name: Optional specification to validate against
        log: Whether to write results to log file
        
    Returns:
        0 if all tests pass, 1 if any test fails
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []
    
    print("Running full test suite...")
    print("=" * 80)
    
    # Run validation tests
    print("\n1. Repository Validation Tests")
    print("-" * 60)
    code, output = run_validation_tests()
    print(output)
    results.append(("Validation", code, output))
    
    # Check Python syntax
    print("\n2. Python Syntax Checks")
    print("-" * 60)
    code, output = check_python_syntax()
    print(output)
    results.append(("Python Syntax", code, output))
    
    # Check YAML syntax
    print("\n3. YAML Syntax Checks")
    print("-" * 60)
    code, output = check_yaml_syntax()
    print(output)
    results.append(("YAML Syntax", code, output))
    
    # Specification-based tests
    if spec_name:
        print(f"\n4. Specification Tests ({spec_name})")
        print("-" * 60)
        code, output = infer_tests_from_specification(spec_name)
        print(output)
        results.append(("Specification Tests", code, output))
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary:")
    print("-" * 60)
    
    passed = sum(1 for _, code, _ in results if code == 0)
    failed = sum(1 for _, code, _ in results if code != 0)
    
    for name, code, _ in results:
        status = "✓ PASS" if code == 0 else "✗ FAIL"
        print(f"{status} {name}")
    
    print("-" * 60)
    print(f"Passed: {passed}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    
    # Write log file
    if log:
        TESTS_LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_path = TESTS_LOGS_DIR / f"test_run_{timestamp}.log"
        
        log_content = [
            f"Test Run: {timestamp}",
            f"Specification: {spec_name if spec_name else 'N/A'}",
            "=" * 80,
            ""
        ]
        
        for name, code, output in results:
            log_content.append(f"\n{'=' * 80}")
            log_content.append(f"{name} - {'PASS' if code == 0 else 'FAIL'}")
            log_content.append(f"{'=' * 80}")
            log_content.append(output)
        
        log_content.append(f"\n{'=' * 80}")
        log_content.append(f"Summary: {passed} passed, {failed} failed")
        log_content.append(f"{'=' * 80}")
        
        log_path.write_text("\n".join(log_content), encoding="utf-8")
        print(f"\n✓ Test log written to: {log_path.relative_to(REPO_ROOT)}")
    
    return 0 if failed == 0 else 1


def list_test_logs() -> int:
    """List all test logs."""
    if not TESTS_LOGS_DIR.exists():
        print("No test logs found (tests_logs directory does not exist).")
        return 0
    
    logs = sorted(TESTS_LOGS_DIR.glob("*.log"), reverse=True)
    
    if not logs:
        print("No test logs found.")
        return 0
    
    print("Recent test logs:")
    print("-" * 80)
    for log_path in logs[:10]:  # Show last 10
        size = log_path.stat().st_size
        mtime = datetime.fromtimestamp(log_path.stat().st_mtime)
        print(f"{log_path.name:<40} {mtime.strftime('%Y-%m-%d %H:%M:%S')} ({size} bytes)")
    
    if len(logs) > 10:
        print(f"... and {len(logs) - 10} more")
    
    print("-" * 80)
    print(f"Total: {len(logs)} log(s)")
    
    return 0


def main():
    """Main entry point for the testing agent."""
    parser = argparse.ArgumentParser(
        description="Testing Agent - Validate code contributions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full test suite
  python testing_agent.py run
  
  # Run tests for a specific specification
  python testing_agent.py run --spec vendor_ingestion_pipeline
  
  # Infer test requirements from specification
  python testing_agent.py infer vendor_ingestion_pipeline
  
  # List test logs
  python testing_agent.py logs
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run full test suite")
    run_parser.add_argument("--spec", "-s", help="Specification name to validate against")
    run_parser.add_argument("--no-log", action="store_true", help="Don't write log file")
    
    # Infer command
    infer_parser = subparsers.add_parser("infer", help="Infer test requirements from specification")
    infer_parser.add_argument("spec_name", help="Specification name (without .yaml)")
    
    # Logs command
    subparsers.add_parser("logs", help="List test logs")
    
    args = parser.parse_args()
    
    if args.command == "run":
        return run_full_test_suite(args.spec, not args.no_log)
    elif args.command == "infer":
        code, output = infer_tests_from_specification(args.spec_name)
        print(output)
        return code
    elif args.command == "logs":
        return list_test_logs()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

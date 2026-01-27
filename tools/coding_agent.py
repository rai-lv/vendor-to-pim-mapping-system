#!/usr/bin/env python3
"""
Coding Agent - Decompose and Create Codex Tasks

This agent handles:
- Step 3: Decompose capability into PR-sized development elements
- Step 4: Create Codex tasks with standards references and quality gates

Trigger: Approval of capability plans (Step 2b)
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
JOBS_DIR = REPO_ROOT / "jobs"
STANDARDS_DIR = REPO_ROOT / "docs" / "standards"

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


def decompose_capability(cap_name: str) -> int:
    """
    Step 3: Decompose capability into PR-sized development elements.
    
    Args:
        cap_name: Name of the capability plan (without .yaml extension)
        
    Returns:
        0 on success, 1 on error
    """
    try:
        cap_path = SPECIFICATIONS_DIR / f"{cap_name}.yaml"
        if not cap_path.exists():
            # Try with _capability suffix
            cap_path = SPECIFICATIONS_DIR / f"{cap_name}_capability.yaml"
        
        if not cap_path.exists():
            raise FileNotFoundError(f"Capability plan not found: {cap_name}")
        
        with cap_path.open("r", encoding="utf-8") as f:
            capability = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Failed to load capability plan: {e}", file=sys.stderr)
        return 1
    
    print(f"# Step 3: Decompose Capability into Development Elements")
    print("=" * 80)
    print(f"\nCapability: {capability.get('capability_name', cap_name)}")
    print(f"Pipeline Reference: {capability.get('pipeline_reference', 'N/A')}")
    print()
    print("## Decomposition Guidelines")
    print()
    print("Break this capability into elements where EACH element:")
    print("- Can be completed in ONE pull request")
    print("- Has a clear, testable scope")
    print("- Specifies exact files to modify/create")
    print("- Includes acceptance criteria")
    print("- Has minimal dependencies on other elements")
    print()
    print("=" * 80)
    print()
    print("## Suggested Development Elements")
    print()
    
    # Extract information from capability plan
    high_level_steps = capability.get("processing_logic", {}).get("high_level_steps", [])
    
    element_id = 1
    print(f"Based on the capability plan, consider these elements:")
    print()
    
    # Suggest elements based on processing steps
    for step in high_level_steps:
        print(f"### Element {element_id}: [Derived from: {step[:50]}...]")
        print()
        print(f"**Target Repo Paths:**")
        print(f"- TODO: Specify exact paths (e.g., jobs/<group>/<job_id>/glue_script.py)")
        print()
        print(f"**Allowed Changes:**")
        print(f"- TODO: List specific files that can be created/modified")
        print(f"- TODO: Be explicit about what can and cannot be changed")
        print()
        print(f"**Acceptance Criteria:**")
        print(f"- TODO: Define testable criteria for this element")
        print(f"- TODO: Each criterion should be verifiable from repo contents")
        print()
        print(f"**Dependencies:**")
        print(f"- TODO: List element IDs this depends on (if any)")
        print()
        print(f"**Estimated Effort:** TODO: Small / Medium / Large")
        print()
        element_id += 1
    
    # Suggest infrastructure elements
    print(f"### Element {element_id}: Job Manifest")
    print()
    print(f"**Target Repo Paths:**")
    print(f"- jobs/<job_group>/<job_id>/job_manifest.yaml")
    print()
    print(f"**Allowed Changes:**")
    print(f"- Create or update job_manifest.yaml only")
    print(f"- Must follow manifest spec: docs/standards/job_manifest_spec.md")
    print()
    print(f"**Acceptance Criteria:**")
    print(f"- Manifest validates with: python tools/validate_repo_docs.py --all")
    print(f"- Uses ${{PLACEHOLDER}} style for parameter substitution")
    print(f"- All inputs/outputs from capability plan are represented")
    print()
    print(f"**Dependencies:** Core implementation element(s)")
    print()
    element_id += 1
    
    print(f"### Element {element_id}: Documentation")
    print()
    print(f"**Target Repo Paths:**")
    print(f"- docs/script_cards/<job_id>.md")
    print(f"- docs/business_job_descriptions/<job_id>.md")
    print()
    print(f"**Allowed Changes:**")
    print(f"- Create documentation files only")
    print(f"- Must follow specs in docs/standards/")
    print()
    print(f"**Acceptance Criteria:**")
    print(f"- Documentation validates with: python tools/validate_repo_docs.py --all")
    print(f"- Aligns with capability plan objectives and acceptance criteria")
    print()
    print(f"**Dependencies:** All implementation elements")
    print()
    
    print("=" * 80)
    print()
    print("## Next Steps")
    print()
    print("1. Review suggested elements and adjust as needed")
    print("2. Ensure each element can be completed in one PR")
    print("3. Define explicit file restrictions for each element")
    print("4. Create acceptance criteria that can be tested from repo")
    print("5. Once decomposition is agreed, proceed to Step 4:")
    print("   Use 'codex-task' command to generate Codex task for each element")
    
    return 0


def generate_codex_task_outline(spec_name: str, element_id: int) -> int:
    """
    Step 4: Generate Codex task for a development element.
    
    Args:
        spec_name: Name of the capability plan
        element_id: ID of the development element
        
    Returns:
        0 on success, 1 on error
    """
    try:
        cap_path = SPECIFICATIONS_DIR / f"{spec_name}.yaml"
        if not cap_path.exists():
            cap_path = SPECIFICATIONS_DIR / f"{spec_name}_capability.yaml"
        
        if not cap_path.exists():
            raise FileNotFoundError(f"Capability plan not found: {spec_name}")
        
        with cap_path.open("r", encoding="utf-8") as f:
            capability = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Failed to load capability plan: {e}", file=sys.stderr)
        return 1
    
    # List available standards
    standards = []
    if STANDARDS_DIR.exists():
        standards = sorted([s.name for s in STANDARDS_DIR.glob("*.md")])
    
    print(f"# Step 4: Codex Task - Element {element_id}")
    print("=" * 80)
    print()
    print(f"**Capability:** {capability.get('capability_name', spec_name)}")
    print(f"**Element ID:** {element_id}")
    print(f"**Created:** {datetime.now().strftime('%Y-%m-%d')}")
    print()
    print("=" * 80)
    print()
    print("## Objective")
    print()
    print(f"Implement Element {element_id} from the decomposed capability plan.")
    print(f"Capability objective: {capability.get('capability_objective', {}).get('description', 'See capability plan')}")
    print()
    print("## Standards References")
    print()
    print("This implementation MUST comply with the following standards:")
    print()
    if standards:
        for standard in standards:
            print(f"- `docs/standards/{standard}`")
    else:
        print("- docs/standards/ (check for relevant specs)")
    print()
    print("Key standards to review:")
    print("- `naming-standard.md` - for naming conventions")
    print("- `job_manifest_spec.md` - if creating/updating manifests")
    print("- `script_card_spec.md` - if creating script cards")
    print("- `business_job_description_spec.md` - if creating business descriptions")
    print()
    print("## Target Script/Path (Explicit)")
    print()
    print("**TARGET_SCRIPT:** TODO: Specify ONCE the primary file being created/modified")
    print()
    print("Examples:")
    print("- `jobs/vendor_onboarding/ingest_bmecat/glue_script.py`")
    print("- `jobs/vendor_onboarding/ingest_bmecat/job_manifest.yaml`")
    print()
    print("## File Restrictions (Explicit)")
    print()
    print("ONLY the following files may be created or modified:")
    print()
    print("**Allowed file list:**")
    print("- TODO: List exact file paths that can be changed")
    print("- TODO: Be restrictive - list ONLY files relevant to this element")
    print()
    print("**Forbidden:**")
    print("- Any file not in the allowed list above")
    print("- Existing code that works correctly")
    print()
    print("## Implementation Requirements")
    print()
    print("### From Capability Plan")
    print()
    
    # Extract relevant sections from capability plan
    inputs = capability.get("inputs", {})
    outputs = capability.get("outputs", {})
    business_rules = capability.get("processing_logic", {}).get("business_rules", [])
    
    if inputs.get("required_inputs"):
        print("**Required Inputs:**")
        for inp in inputs.get("required_inputs", []):
            print(f"- {inp.get('name', 'N/A')}: {inp.get('meaning', 'N/A')}")
        print()
    
    if outputs.get("primary_outputs"):
        print("**Expected Outputs:**")
        for out in outputs.get("primary_outputs", []):
            print(f"- {out.get('name', 'N/A')}: {out.get('meaning', 'N/A')}")
        print()
    
    if business_rules:
        print("**Business Rules to Enforce:**")
        for rule in business_rules:
            print(f"- {rule}")
        print()
    
    print("### Technical Requirements")
    print()
    print("- Follow DRY (Don't Repeat Yourself) principle")
    print("- Follow SOLID principles where applicable")
    print("- Add appropriate error handling")
    print("- Include logging for key operations")
    print("- Use type hints for Python code")
    print()
    print("## Acceptance Criteria (From Decomposition)")
    print()
    
    acceptance = capability.get("acceptance_criteria", {})
    if acceptance.get("functional"):
        print("**Functional:**")
        for criterion in acceptance.get("functional", []):
            print(f"- [ ] {criterion}")
        print()
    
    if acceptance.get("quality"):
        print("**Quality:**")
        for criterion in acceptance.get("quality", []):
            print(f"- [ ] {criterion}")
        print()
    
    print("**Element-Specific:**")
    print("- [ ] TODO: Add element-specific acceptance criteria")
    print("- [ ] TODO: Each criterion must be testable from repo contents")
    print()
    print("## Quality Gates (Must Pass)")
    print()
    print("These checks MUST pass before the PR is merged:")
    print()
    print("```bash")
    print("# Repository validation")
    print("python tools/validate_repo_docs.py --all")
    print()
    print("# Python syntax check (if applicable)")
    print("python -m py_compile <TARGET_SCRIPT>")
    print()
    print("# Best practices check")
    print("python tools/coding_agent.py check")
    print("```")
    print()
    print("## Dependencies")
    print()
    print("**Element Dependencies:**")
    print("- TODO: List element IDs that must be completed first")
    print()
    
    dep_caps = capability.get("dependencies", {}).get("upstream_capabilities", [])
    if dep_caps:
        print("**Capability Dependencies:**")
        for dep in dep_caps:
            print(f"- {dep.get('capability', 'N/A')}: {dep.get('dependency', 'N/A')}")
        print()
    
    print("## Testing Strategy")
    print()
    print("**Unit Tests:**")
    print("- TODO: Define unit tests for this element")
    print()
    print("**Integration Tests:**")
    print("- TODO: Define integration tests if applicable")
    print()
    print("**Manual Verification:**")
    print("- TODO: Define manual checks to verify correctness")
    print()
    print("## Boundaries (What This Element Does NOT Do)")
    print()
    boundaries = capability.get("boundaries", {}).get("what_this_does_not_do", [])
    if boundaries:
        for boundary in boundaries:
            print(f"- {boundary}")
    else:
        print("- TODO: State explicitly what is out of scope")
    print()
    print("=" * 80)
    print()
    print("## Instructions for Codex")
    print()
    print("1. Read and comply with ALL standards in docs/standards/")
    print("2. Implement ONLY the files in the allowed file list")
    print("3. Follow the TARGET_SCRIPT pattern strictly")
    print("4. Ensure all acceptance criteria can be verified")
    print("5. Run all quality gates before considering the task complete")
    print("6. Do not modify existing working code outside the allowed list")
    print()
    print("=" * 80)
    
    return 0


def main():
    """Main entry point for the coding agent."""
    parser = argparse.ArgumentParser(
        description="Coding Agent - Decompose capabilities and create Codex tasks (Steps 3 & 4)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Step 3: Decompose capability into PR-sized elements
  python coding_agent.py decompose data_ingestion_capability
  
  # Step 4: Generate Codex task for a specific element
  python coding_agent.py codex-task data_ingestion_capability 1
  
  # Validate repository code and documentation
  python coding_agent.py validate
  
  # Check best practices
  python coding_agent.py check

Workflow:
  Step 3: decompose -> Review elements -> Adjust as needed
  Step 4: codex-task -> Create PR for each element
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Decompose command (Step 3)
    decompose_parser = subparsers.add_parser("decompose", help="Step 3: Decompose capability into development elements")
    decompose_parser.add_argument("capability_name", help="Capability plan name (without .yaml)")
    
    # Codex task command (Step 4)
    codex_parser = subparsers.add_parser("codex-task", help="Step 4: Generate Codex task for an element")
    codex_parser.add_argument("capability_name", help="Capability plan name (without .yaml)")
    codex_parser.add_argument("element_id", type=int, help="Element ID")
    
    # Validate command
    subparsers.add_parser("validate", help="Run repository validation")
    
    # Check command
    subparsers.add_parser("check", help="Run best practices checks")
    
    args = parser.parse_args()
    
    if args.command == "decompose":
        return decompose_capability(args.capability_name)
    elif args.command == "codex-task":
        return generate_codex_task_outline(args.capability_name, args.element_id)
    elif args.command == "validate":
        return validate_code()
    elif args.command == "check":
        return check_best_practices()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

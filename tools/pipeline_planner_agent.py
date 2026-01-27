#!/usr/bin/env python3
"""
Pipeline Planner Agent - Overarching Plan (Pipeline-Level)

This agent creates end-to-end pipeline plans for objectives, defining the
sequence of capabilities/steps, decision points, and conceptual artifacts.

Output: docs/roadmaps/<objective_name>_pipeline_plan.md
Trigger: After Step 1 (Define Objective) is approved
Workflow Step: Step 2a - Overarching Plan (Pipeline-Level)
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAPS_DIR = REPO_ROOT / "docs" / "roadmaps"


def generate_pipeline_plan_template(objective_name: str, objective_ref: str = "") -> str:
    """Generate a pipeline-level plan template for Step 2a."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Pipeline Plan: {objective_name}

**Date:** {timestamp}
**Status:** Draft
**Workflow Step:** Step 2a - Overarching Plan (Pipeline-Level)
**Objective Reference:** {objective_ref if objective_ref else "TODO: Link to Step 1 objective document"}

---

## Pipeline Overview

### Purpose
TODO: Brief description of what this pipeline achieves end-to-end

### Scope
- **Start Point:** TODO: Where does data/processing begin?
- **End Point:** TODO: What is the final output/outcome?

---

## Processing Sequence (First → Last)

List capabilities/steps in intended processing order:

### Step 1: [Capability Name]
- **Purpose:** TODO: What does this step do?
- **Input:** TODO: What does it receive? (conceptual, not S3 paths)
- **Output:** TODO: What does it produce? (conceptual, not S3 paths)
- **Existing Job:** TODO: Does an existing job cover this? If yes, which one?
- **Status:** TODO: New / Existing / Modified

### Step 2: [Capability Name]
- **Purpose:** TODO: What does this step do?
- **Input:** TODO: What does it receive?
- **Output:** TODO: What does it produce?
- **Existing Job:** TODO: Does an existing job cover this?
- **Status:** TODO: New / Existing / Modified

### Step 3: [Capability Name]
- **Purpose:** TODO: What does this step do?
- **Input:** TODO: What does it receive?
- **Output:** TODO: What does it produce?
- **Existing Job:** TODO: Does an existing job cover this?
- **Status:** TODO: New / Existing / Modified

_Add more steps as needed..._

---

## Decision Points and Fallback Paths

### Decision Point 1: [Name]
- **Condition:** TODO: What triggers this decision?
- **Option A:** TODO: What happens if condition is true?
- **Option B:** TODO: What happens if condition is false?
- **Fallback:** TODO: What happens if processing cannot continue?

### Decision Point 2: [Name]
- **Condition:** TODO: What triggers this decision?
- **Option A:** TODO: What happens if condition is true?
- **Option B:** TODO: What happens if condition is false?
- **Fallback:** TODO: What happens if processing cannot continue?

_Add more decision points as needed..._

---

## Conceptual Artifacts

Define artifacts exchanged between steps (names + meaning, not storage details):

### Artifact 1: [Name]
- **Produced By:** TODO: Which step creates this?
- **Consumed By:** TODO: Which step(s) use this?
- **Meaning:** TODO: What does this artifact represent?
- **Key Attributes:** TODO: What key information does it contain?

### Artifact 2: [Name]
- **Produced By:** TODO: Which step creates this?
- **Consumed By:** TODO: Which step(s) use this?
- **Meaning:** TODO: What does this artifact represent?
- **Key Attributes:** TODO: What key information does it contain?

_Add more artifacts as needed..._

---

## Existing Job Mapping

Map existing jobs to pipeline steps:

| Existing Job ID | Covers Pipeline Step(s) | Modifications Needed |
|-----------------|-------------------------|----------------------|
| TODO            | TODO                    | None / Minor / Major |
| TODO            | TODO                    | None / Minor / Major |

### New Jobs Required
- TODO: List steps that require new job creation

---

## Unknowns and Open Decisions

### Technical Unknowns
- TODO: What technical details are still uncertain?
- TODO: What research or prototyping is needed?

### Business Decisions Pending
- TODO: What business decisions need to be made?
- TODO: Who needs to provide input?

### Dependencies to Clarify
- TODO: What external dependencies need confirmation?

### Assumptions Being Made
- TODO: What assumptions are we making? (mark clearly as assumptions)
- TODO: What validation is needed for these assumptions?

---

## Pipeline Validation

### End-to-End Flow Check
- [ ] All steps from start to end are defined
- [ ] Decision points and fallbacks are identified
- [ ] Artifacts flow logically between steps
- [ ] Existing jobs are mapped where applicable

### Completeness Check
- [ ] No gaps in processing sequence
- [ ] All inputs have a source
- [ ] All outputs have a consumer or are final outputs
- [ ] Error handling and fallback paths are defined

---

## Approval and Next Steps

### Stakeholder Sign-off
- [ ] Pipeline sequence reviewed and approved
- [ ] Decision points confirmed
- [ ] Existing job mapping validated
- [ ] Unknowns and open decisions documented

### Next Step
Once approved, proceed to **Step 2b: Capability Plan (Step-Level)** for each capability
using the Capability Planner Agent. Start with the highest-priority capability.

---

## Notes

- TODO: Add any additional context or considerations
- This pipeline plan focuses on the "what" and "sequence", not the "how"
- Detailed implementation plans are created in Step 2b for each capability
"""


def create_pipeline_plan(objective_name: str, objective_ref: str = "", overwrite: bool = False) -> int:
    """
    Create a new pipeline plan document.
    
    Args:
        objective_name: Name of the objective
        objective_ref: Optional reference to objective document
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    # Ensure roadmaps directory exists
    ROADMAPS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    safe_name = objective_name.lower().replace(" ", "_").replace("/", "_")
    output_path = ROADMAPS_DIR / f"{safe_name}_pipeline_plan.md"
    
    # Check if file already exists
    if output_path.exists() and not overwrite:
        print(f"Error: Pipeline plan already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    # Generate and write template
    content = generate_pipeline_plan_template(objective_name, objective_ref)
    
    try:
        output_path.write_text(content, encoding="utf-8")
        print(f"✓ Created pipeline plan: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Edit the document to fill in all TODO sections")
        print(f"2. Define the complete processing sequence (first → last)")
        print(f"3. Identify decision points and fallback paths")
        print(f"4. Map conceptual artifacts between steps")
        print(f"5. Map existing jobs to pipeline steps")
        print(f"6. Document unknowns and open decisions explicitly")
        print(f"7. Review and approve with stakeholders")
        print(f"8. Once approved, create Capability Plans (Step 2b) for each step")
        return 0
    except Exception as e:
        print(f"Error: Failed to create pipeline plan: {e}", file=sys.stderr)
        return 1


def list_pipeline_plans() -> int:
    """List all existing pipeline plans."""
    if not ROADMAPS_DIR.exists():
        print("No pipeline plans found (roadmaps directory does not exist).")
        return 0
    
    # Get all pipeline plan files (exclude README.md and objective files)
    pipeline_plans = sorted([p for p in ROADMAPS_DIR.glob("*_pipeline_plan.md")])
    
    if not pipeline_plans:
        print("No pipeline plans found.")
        return 0
    
    print("Existing pipeline plans:")
    print("-" * 60)
    for doc in pipeline_plans:
        # Try to extract status from the file
        try:
            content = doc.read_text(encoding="utf-8")
            status_match = content.split("**Status:**", 1)
            if len(status_match) > 1:
                status = status_match[1].split("\n", 1)[0].strip()
            else:
                status = "Unknown"
        except:
            status = "Unknown"
        
        print(f"{doc.name:<50} Status: {status}")
    print("-" * 60)
    print(f"Total: {len(pipeline_plans)} pipeline plan(s)")
    
    return 0


def main():
    """Main entry point for the pipeline planner agent."""
    parser = argparse.ArgumentParser(
        description="Pipeline Planner Agent - Generate overarching pipeline plans (Step 2a)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new pipeline plan
  python pipeline_planner_agent.py create "vendor_onboarding" --objective-ref "vendor_onboarding.md"
  
  # List all pipeline plans
  python pipeline_planner_agent.py list
  
  # Overwrite existing pipeline plan
  python pipeline_planner_agent.py create "vendor_onboarding" --overwrite

Note: This is Step 2a in the workflow. Use this after Step 1 (Define Objective) is approved.
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new pipeline plan")
    create_parser.add_argument("objective_name", help="Name of the objective")
    create_parser.add_argument("--objective-ref", "-o", default="", help="Reference to objective document")
    create_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file if present")
    
    # List command
    subparsers.add_parser("list", help="List all pipeline plans")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return create_pipeline_plan(args.objective_name, args.objective_ref, args.overwrite)
    elif args.command == "list":
        return list_pipeline_plans()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

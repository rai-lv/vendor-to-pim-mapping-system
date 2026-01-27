#!/usr/bin/env python3
"""
Capability Planner Agent - Capability Plan (Step-Level)

This agent creates detailed capability plans for individual pipeline steps,
specifying inputs/outputs, rules/logic, acceptance criteria, and boundaries.

Output: docs/specifications/<capability_name>_capability.yaml
Trigger: After Step 2a (Pipeline Plan) is approved
Workflow Step: Step 2b - Capability Plan (Step-Level)
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
ROADMAPS_DIR = REPO_ROOT / "docs" / "roadmaps"


def generate_capability_plan_template(capability_name: str, pipeline_ref: str = "") -> dict:
    """Generate a capability plan template for Step 2b."""
    return {
        "capability_name": capability_name,
        "version": "1.0.0",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "draft",
        "workflow_step": "Step 2b - Capability Plan (Step-Level)",
        "pipeline_reference": pipeline_ref if pipeline_ref else "TODO: Link to Step 2a pipeline plan",
        
        "capability_objective": {
            "description": "TODO: What does this capability do? (specific, actionable)",
            "business_value": "TODO: Why is this capability needed?",
            "pipeline_step": "TODO: Which step in the pipeline plan does this implement?"
        },
        
        "inputs": {
            "description": "Define inputs by meaning, not storage details",
            "required_inputs": [
                {
                    "name": "TODO: Input name",
                    "meaning": "TODO: What does this input represent?",
                    "content": "TODO: What information does it contain?",
                    "source": "TODO: Which upstream capability/step produces this?",
                    "format_note": "TODO: Expected format (CSV/JSON/Parquet/etc.)"
                }
            ],
            "optional_inputs": [
                {
                    "name": "TODO: Optional input name",
                    "meaning": "TODO: What does this optional input represent?",
                    "content": "TODO: What information does it contain?",
                    "source": "TODO: Which upstream capability produces this?",
                    "when_used": "TODO: Under what conditions is this used?"
                }
            ]
        },
        
        "outputs": {
            "description": "Define outputs by meaning, not storage details",
            "primary_outputs": [
                {
                    "name": "TODO: Output name",
                    "meaning": "TODO: What does this output represent?",
                    "content": "TODO: What information does it contain?",
                    "consumers": "TODO: Which downstream capabilities use this?",
                    "format_note": "TODO: Output format"
                }
            ],
            "secondary_outputs": [
                {
                    "name": "TODO: Secondary output (logs, metrics, etc.)",
                    "meaning": "TODO: What does this represent?",
                    "purpose": "TODO: Why is this produced?"
                }
            ]
        },
        
        "processing_logic": {
            "high_level_steps": [
                "TODO: Step 1 - Describe processing step",
                "TODO: Step 2 - Describe processing step",
                "TODO: Step 3 - Describe processing step"
            ],
            "business_rules": [
                "TODO: Rule 1 - State business rule that must be enforced",
                "TODO: Rule 2 - State business rule that must be enforced"
            ],
            "decision_logic": [
                {
                    "condition": "TODO: If [condition]",
                    "action": "TODO: Then [action]",
                    "fallback": "TODO: Else [fallback action]"
                }
            ],
            "error_handling": "TODO: How are errors detected and handled?"
        },
        
        "constraints": {
            "technical": [
                "TODO: Platform constraints (AWS Glue, Lambda, etc.)",
                "TODO: Runtime constraints (memory, timeout, etc.)",
                "TODO: Data volume constraints"
            ],
            "business": [
                "TODO: Processing window requirements",
                "TODO: Data retention policies",
                "TODO: Compliance requirements"
            ],
            "performance": [
                "TODO: Expected processing time",
                "TODO: Throughput requirements",
                "TODO: Latency requirements"
            ]
        },
        
        "acceptance_criteria": {
            "functional": [
                "TODO: Testable criterion 1 - System must...",
                "TODO: Testable criterion 2 - Output must...",
                "TODO: Testable criterion 3 - Processing must..."
            ],
            "quality": [
                "TODO: Data quality threshold (e.g., accuracy > 95%)",
                "TODO: Error rate threshold (e.g., < 1% failures)",
                "TODO: Performance threshold (e.g., complete within 10 minutes)"
            ],
            "validation_methods": [
                "TODO: How will functional criteria be tested?",
                "TODO: How will quality criteria be measured?"
            ]
        },
        
        "boundaries": {
            "what_this_does": [
                "TODO: Explicitly state what this capability does"
            ],
            "what_this_does_not_do": [
                "TODO: Explicitly state what is NOT handled by this capability",
                "TODO: Clarify responsibilities of other capabilities"
            ],
            "deferred_to_other_capabilities": [
                "TODO: What is delegated to upstream capabilities?",
                "TODO: What is delegated to downstream capabilities?"
            ]
        },
        
        "dependencies": {
            "upstream_capabilities": [
                {
                    "capability": "TODO: Name of upstream capability",
                    "dependency": "TODO: What does this capability depend on?",
                    "criticality": "blocking / non-blocking"
                }
            ],
            "downstream_consumers": [
                {
                    "capability": "TODO: Name of downstream capability",
                    "consumes": "TODO: What output does it consume?",
                    "requirement": "TODO: What does the consumer require?"
                }
            ],
            "external_systems": [
                {
                    "system": "TODO: External system name",
                    "interaction": "TODO: How does this capability interact with it?",
                    "criticality": "blocking / non-blocking"
                }
            ]
        },
        
        "open_questions": {
            "technical_unknowns": [
                "TODO: What technical details need clarification?"
            ],
            "business_decisions": [
                "TODO: What business decisions are pending?"
            ],
            "assumptions": [
                "TODO: What assumptions are being made? (mark clearly)"
            ]
        },
        
        "approval_checklist": {
            "completeness": [
                "[ ] Inputs and outputs defined by meaning",
                "[ ] Processing logic and rules specified",
                "[ ] Acceptance criteria are testable",
                "[ ] Boundaries explicitly stated",
                "[ ] Dependencies identified"
            ],
            "stakeholder_signoff": [
                "[ ] Business logic reviewed and approved",
                "[ ] Technical approach validated",
                "[ ] Acceptance criteria agreed upon"
            ]
        },
        
        "next_steps": "Once approved, proceed to Step 3 (Decompose into Development Elements) using Coding Agent"
    }


def create_capability_plan(capability_name: str, pipeline_ref: str = "", overwrite: bool = False) -> int:
    """
    Create a new capability plan.
    
    Args:
        capability_name: Name of the capability
        pipeline_ref: Optional reference to pipeline plan
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    # Ensure specifications directory exists
    SPECIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    safe_name = capability_name.lower().replace(" ", "_").replace("/", "_")
    output_path = SPECIFICATIONS_DIR / f"{safe_name}_capability.yaml"
    
    # Check if file already exists
    if output_path.exists() and not overwrite:
        print(f"Error: Capability plan already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    # Generate template
    capability = generate_capability_plan_template(capability_name, pipeline_ref)
    
    try:
        with output_path.open("w", encoding="utf-8") as f:
            yaml.dump(capability, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✓ Created capability plan: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Fill in all TODO sections based on pipeline plan")
        print(f"2. Define inputs/outputs by meaning (not storage)")
        print(f"3. Specify processing logic and business rules")
        print(f"4. Create testable acceptance criteria")
        print(f"5. Explicitly state boundaries (what it does/doesn't do)")
        print(f"6. Identify all dependencies")
        print(f"7. Review and approve with stakeholders")
        print(f"8. Once approved, use Coding Agent to decompose into development elements")
        return 0
    except Exception as e:
        print(f"Error: Failed to create capability plan: {e}", file=sys.stderr)
        return 1


def list_capability_plans() -> int:
    """List all existing capability plans."""
    if not SPECIFICATIONS_DIR.exists():
        print("No capability plans found (specifications directory does not exist).")
        return 0
    
    # Get all capability plan files
    capabilities = sorted([p for p in SPECIFICATIONS_DIR.glob("*_capability.yaml")])
    
    if not capabilities:
        print("No capability plans found.")
        return 0
    
    print("Existing capability plans:")
    print("-" * 80)
    for cap_path in capabilities:
        try:
            with cap_path.open("r", encoding="utf-8") as f:
                cap = yaml.safe_load(f)
            
            name = cap.get("capability_name", "Unknown")
            status = cap.get("status", "Unknown")
            version = cap.get("version", "Unknown")
            
            print(f"{cap_path.name:<50} Status: {status:<10} Version: {version}")
        except Exception as e:
            print(f"{cap_path.name:<50} Status: Error (invalid YAML)")
    
    print("-" * 80)
    print(f"Total: {len(capabilities)} capability plan(s)")
    
    return 0


def validate_capability_plan(cap_path: Path) -> int:
    """
    Validate a capability plan file.
    
    Args:
        cap_path: Path to capability plan file
        
    Returns:
        0 if valid, 1 if invalid
    """
    required_keys = [
        "capability_name", "version", "created_date", "status",
        "capability_objective", "inputs", "outputs", "processing_logic",
        "constraints", "acceptance_criteria", "boundaries", "dependencies"
    ]
    
    try:
        with cap_path.open("r", encoding="utf-8") as f:
            cap = yaml.safe_load(f)
        
        if not isinstance(cap, dict):
            print(f"Error: Capability plan must be a YAML dictionary", file=sys.stderr)
            return 1
        
        missing_keys = [key for key in required_keys if key not in cap]
        
        if missing_keys:
            print(f"Error: Missing required keys: {', '.join(missing_keys)}", file=sys.stderr)
            return 1
        
        print(f"✓ Capability plan is valid: {cap_path.relative_to(REPO_ROOT)}")
        print(f"  Capability: {cap['capability_name']}")
        print(f"  Version: {cap['version']}")
        print(f"  Status: {cap['status']}")
        
        return 0
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Failed to validate capability plan: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the capability planner agent."""
    parser = argparse.ArgumentParser(
        description="Capability Planner Agent - Generate capability plans (Step 2b)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new capability plan
  python capability_planner_agent.py create "data_ingestion" --pipeline-ref "vendor_onboarding_pipeline_plan.md"
  
  # List all capability plans
  python capability_planner_agent.py list
  
  # Validate a capability plan
  python capability_planner_agent.py validate docs/specifications/data_ingestion_capability.yaml

Note: This is Step 2b in the workflow. Use this after Step 2a (Pipeline Plan) is approved.
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new capability plan")
    create_parser.add_argument("capability_name", help="Name of the capability")
    create_parser.add_argument("--pipeline-ref", "-p", default="", help="Reference to pipeline plan")
    create_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file if present")
    
    # List command
    subparsers.add_parser("list", help="List all capability plans")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a capability plan file")
    validate_parser.add_argument("cap_file", type=Path, help="Path to capability plan file")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return create_capability_plan(args.capability_name, args.pipeline_ref, args.overwrite)
    elif args.command == "list":
        return list_capability_plans()
    elif args.command == "validate":
        return validate_capability_plan(args.cap_file)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

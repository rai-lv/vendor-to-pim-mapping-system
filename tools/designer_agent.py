#!/usr/bin/env python3
"""
Designer Agent - Subsystem Specification and Design

This agent breaks down high-level plans into actionable subsystem specifications,
detailing objectives, constraints, inputs/outputs, and coding tasks.

Output: docs/specifications/<subsystem>.yaml
Trigger: Completion of a planning phase
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
ROADMAPS_DIR = REPO_ROOT / "docs" / "roadmaps"


def generate_specification_template(subsystem_name: str, planning_phase: str = "") -> dict:
    """Generate a subsystem specification template."""
    return {
        "subsystem_name": subsystem_name,
        "version": "1.0.0",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "draft",
        "planning_phase": planning_phase if planning_phase else "TODO: Reference planning document",
        
        "objective": {
            "description": "TODO: Define the specific objective this subsystem achieves",
            "business_value": "TODO: Explain the business value delivered",
            "success_criteria": [
                "TODO: Define measurable success criteria"
            ]
        },
        
        "constraints": {
            "technical": [
                "TODO: List technical constraints (e.g., AWS Glue limitations, runtime requirements)"
            ],
            "business": [
                "TODO: List business constraints (e.g., data retention policies, processing windows)"
            ],
            "dependencies": [
                "TODO: List dependencies on other subsystems or external systems"
            ]
        },
        
        "inputs": [
            {
                "name": "TODO: Input name",
                "type": "TODO: Data type (e.g., CSV, JSON, Parquet)",
                "source": "TODO: S3 location or system",
                "required": True,
                "schema_reference": "TODO: Link to schema definition or inline schema"
            }
        ],
        
        "outputs": [
            {
                "name": "TODO: Output name",
                "type": "TODO: Data type",
                "destination": "TODO: S3 location or system",
                "purpose": "TODO: What this output is used for",
                "schema_reference": "TODO: Link to schema definition or inline schema"
            }
        ],
        
        "processing_logic": {
            "high_level_steps": [
                "TODO: Step 1",
                "TODO: Step 2",
                "TODO: Step 3"
            ],
            "business_rules": [
                "TODO: Key business rules that must be enforced"
            ],
            "error_handling": "TODO: Describe error handling strategy"
        },
        
        "coding_tasks": [
            {
                "task_id": 1,
                "description": "TODO: Specific coding task",
                "files_affected": ["TODO: List files to create or modify"],
                "acceptance_criteria": [
                    "TODO: Define acceptance criteria for this task"
                ],
                "estimated_complexity": "low",  # low, medium, high
                "dependencies": []  # Task IDs this depends on
            }
        ],
        
        "testing_requirements": {
            "unit_tests": [
                "TODO: Define unit test requirements"
            ],
            "integration_tests": [
                "TODO: Define integration test requirements"
            ],
            "test_data": "TODO: Describe test data requirements"
        },
        
        "documentation_requirements": [
            "TODO: Business job description",
            "TODO: Script card",
            "TODO: Job manifest"
        ],
        
        "notes": "TODO: Add any additional context, assumptions, or open questions"
    }


def create_specification(subsystem_name: str, planning_phase: str = "", overwrite: bool = False) -> int:
    """
    Create a new subsystem specification.
    
    Args:
        subsystem_name: Name of the subsystem
        planning_phase: Optional reference to planning document
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    # Ensure specifications directory exists
    SPECIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    safe_name = subsystem_name.lower().replace(" ", "_").replace("/", "_")
    output_path = SPECIFICATIONS_DIR / f"{safe_name}.yaml"
    
    # Check if file already exists
    if output_path.exists() and not overwrite:
        print(f"Error: Specification already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    # Generate template
    spec = generate_specification_template(subsystem_name, planning_phase)
    
    try:
        with output_path.open("w", encoding="utf-8") as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✓ Created specification: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Edit the specification to fill in all TODO sections")
        print(f"2. Define clear objectives, constraints, and I/O contracts")
        print(f"3. Break down into specific coding tasks")
        print(f"4. Review and approve the specification")
        print(f"5. Once approved, trigger the Coding Agent to implement tasks")
        return 0
    except Exception as e:
        print(f"Error: Failed to create specification: {e}", file=sys.stderr)
        return 1


def list_specifications() -> int:
    """List all existing specifications."""
    if not SPECIFICATIONS_DIR.exists():
        print("No specifications found (specifications directory does not exist).")
        return 0
    
    specs = sorted(SPECIFICATIONS_DIR.glob("*.yaml"))
    
    if not specs:
        print("No specifications found.")
        return 0
    
    print("Existing specifications:")
    print("-" * 80)
    for spec_path in specs:
        try:
            with spec_path.open("r", encoding="utf-8") as f:
                spec = yaml.safe_load(f)
            
            name = spec.get("subsystem_name", "Unknown")
            status = spec.get("status", "Unknown")
            version = spec.get("version", "Unknown")
            
            print(f"{spec_path.name:<40} Status: {status:<10} Version: {version}")
        except Exception as e:
            print(f"{spec_path.name:<40} Status: Error (invalid YAML)")
    
    print("-" * 80)
    print(f"Total: {len(specs)} specification(s)")
    
    return 0


def validate_specification(spec_path: Path) -> int:
    """
    Validate a specification file.
    
    Args:
        spec_path: Path to specification file
        
    Returns:
        0 if valid, 1 if invalid
    """
    required_keys = [
        "subsystem_name", "version", "created_date", "status",
        "objective", "constraints", "inputs", "outputs",
        "processing_logic", "coding_tasks", "testing_requirements",
        "documentation_requirements"
    ]
    
    try:
        with spec_path.open("r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        
        if not isinstance(spec, dict):
            print(f"Error: Specification must be a YAML dictionary", file=sys.stderr)
            return 1
        
        missing_keys = [key for key in required_keys if key not in spec]
        
        if missing_keys:
            print(f"Error: Missing required keys: {', '.join(missing_keys)}", file=sys.stderr)
            return 1
        
        print(f"✓ Specification is valid: {spec_path.relative_to(REPO_ROOT)}")
        print(f"  Subsystem: {spec['subsystem_name']}")
        print(f"  Version: {spec['version']}")
        print(f"  Status: {spec['status']}")
        print(f"  Coding tasks: {len(spec.get('coding_tasks', []))}")
        
        return 0
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Failed to validate specification: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the designer agent."""
    parser = argparse.ArgumentParser(
        description="Designer Agent - Generate subsystem specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new specification
  python designer_agent.py create "vendor_ingestion_pipeline" --planning-phase "Q1 2026 Features"
  
  # List all specifications
  python designer_agent.py list
  
  # Validate a specification
  python designer_agent.py validate docs/specifications/vendor_ingestion_pipeline.yaml
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new specification")
    create_parser.add_argument("subsystem_name", help="Name of the subsystem")
    create_parser.add_argument("--planning-phase", "-p", default="", help="Reference to planning document")
    create_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file if present")
    
    # List command
    subparsers.add_parser("list", help="List all specifications")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a specification file")
    validate_parser.add_argument("spec_file", type=Path, help="Path to specification file")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return create_specification(args.subsystem_name, args.planning_phase, args.overwrite)
    elif args.command == "list":
        return list_specifications()
    elif args.command == "validate":
        return validate_specification(args.spec_file)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

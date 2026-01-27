#!/usr/bin/env python3
"""
Planner Agent - High-Level Planning and Objective Definition

This agent defines overarching objectives, constraints, and necessary information
for project phases. It generates high-level planning documents that guide the
development process.

Output: docs/roadmaps/<planning_phase>.md
Trigger: Manually invoked
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAPS_DIR = REPO_ROOT / "docs" / "roadmaps"


def generate_planning_template(phase_name: str, description: str = "") -> str:
    """Generate a planning document template."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Planning Phase: {phase_name}

**Date:** {timestamp}
**Status:** Draft

## Objective

{description if description else "TODO: Define the high-level objective for this planning phase."}

## Scope

### In Scope
- TODO: Define what is included in this planning phase

### Out of Scope
- TODO: Define what is explicitly excluded

## Constraints

### Technical Constraints
- TODO: List technical limitations or requirements

### Business Constraints
- TODO: List business requirements or limitations

### Resource Constraints
- TODO: List resource availability or limitations

## Required Information

### Data Requirements
- TODO: Identify needed data sources or artifacts

### Stakeholder Input
- TODO: Identify decisions or information needed from stakeholders

### Dependencies
- TODO: List dependencies on other systems or projects

## Success Criteria

- TODO: Define measurable success criteria for this planning phase

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| TODO | TODO   | TODO        | TODO       |

## Next Steps

1. TODO: Define the immediate next steps
2. Review and validate objectives with stakeholders
3. Create detailed specifications via Designer Agent

## Notes

- TODO: Add any additional context or considerations
"""


def create_planning_document(phase_name: str, description: str = "", overwrite: bool = False) -> int:
    """
    Create a new planning document.
    
    Args:
        phase_name: Name of the planning phase
        description: Optional description of the objective
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    # Ensure roadmaps directory exists
    ROADMAPS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    safe_name = phase_name.lower().replace(" ", "_").replace("/", "_")
    output_path = ROADMAPS_DIR / f"{safe_name}.md"
    
    # Check if file already exists
    if output_path.exists() and not overwrite:
        print(f"Error: Planning document already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    # Generate and write template
    content = generate_planning_template(phase_name, description)
    
    try:
        output_path.write_text(content, encoding="utf-8")
        print(f"✓ Created planning document: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Edit the document to fill in all TODO sections")
        print(f"2. Review objectives and constraints with stakeholders")
        print(f"3. Once approved, trigger the Designer Agent to create specifications")
        return 0
    except Exception as e:
        print(f"Error: Failed to create planning document: {e}", file=sys.stderr)
        return 1


def list_planning_documents() -> int:
    """List all existing planning documents."""
    if not ROADMAPS_DIR.exists():
        print("No planning documents found (roadmaps directory does not exist).")
        return 0
    
    # Get all .md files except README.md
    planning_docs = sorted([p for p in ROADMAPS_DIR.glob("*.md") if p.name != "README.md"])
    
    if not planning_docs:
        print("No planning documents found.")
        return 0
    
    print("Existing planning documents:")
    print("-" * 60)
    for doc in planning_docs:
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
        
        print(f"{doc.name:<40} Status: {status}")
    print("-" * 60)
    print(f"Total: {len(planning_docs)} document(s)")
    
    return 0


def main():
    """Main entry point for the planner agent."""
    parser = argparse.ArgumentParser(
        description="Planner Agent - Generate high-level planning documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new planning document
  python planner_agent.py create "Q1 2026 Features" --description "Plan Q1 feature development"
  
  # List all planning documents
  python planner_agent.py list
  
  # Overwrite existing planning document
  python planner_agent.py create "Q1 2026 Features" --overwrite
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new planning document")
    create_parser.add_argument("phase_name", help="Name of the planning phase")
    create_parser.add_argument("--description", "-d", default="", help="Brief description of the objective")
    create_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file if present")
    
    # List command
    subparsers.add_parser("list", help="List all planning documents")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return create_planning_document(args.phase_name, args.description, args.overwrite)
    elif args.command == "list":
        return list_planning_documents()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

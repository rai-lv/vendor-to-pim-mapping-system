#!/usr/bin/env python3
"""
Documentation Agent - Project Documentation Maintenance

This agent updates and maintains project documentation, generating script cards,
business descriptions, and glossary updates based on finalized plans, code, or tests.

Trigger: Finalized plans, code, or tests
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATIONS_DIR = REPO_ROOT / "docs" / "specifications"
BUSINESS_DESC_DIR = REPO_ROOT / "docs" / "business_job_descriptions"
SCRIPT_CARDS_DIR = REPO_ROOT / "docs" / "script_cards"
GLOSSARY_PATH = REPO_ROOT / "docs" / "glossary.md"
JOB_INVENTORY_PATH = REPO_ROOT / "docs" / "job_inventory.md"
JOBS_DIR = REPO_ROOT / "jobs"


def generate_script_card_template(job_id: str, spec_name: str = None) -> str:
    """
    Generate a script card template.
    
    Args:
        job_id: Job ID
        spec_name: Optional specification to reference
        
    Returns:
        Script card template as string
    """
    spec_ref = f"Based on specification: {spec_name}" if spec_name else "TODO: Reference specification or planning document"
    
    return f"""# Script Card: {job_id}

**Version:** 1.0.0  
**Last Updated:** {datetime.now().strftime("%Y-%m-%d")}  
**Status:** Draft  
**Specification:** {spec_ref}

---

## Job Identification

- **job_id:** `{job_id}`
- **Glue Job Name:** `TODO: AWS Glue job name`
- **Runtime:** `TODO: e.g., AWS Glue 4.0 (Python 3.10, Spark 3.3.0)`
- **Executor:** AWS Glue

---

## Purpose (One-Line Summary)

TODO: Brief one-line description of what this job does.

---

## Parameters

| Parameter Name | Type | Required | Default | Description |
|----------------|------|----------|---------|-------------|
| TODO           | TODO | Yes/No   | TODO    | TODO        |

---

## Inputs

### Input 1: TODO

- **S3 Location Pattern:** `TODO: s3://bucket/prefix/pattern`
- **File Pattern:** `TODO: file_pattern*.ext`
- **Format:** TODO (e.g., CSV, JSON, Parquet)
- **Required:** Yes/No
- **Purpose:** TODO: What this input provides

---

## Outputs

### Output 1: TODO

- **S3 Location Pattern:** `TODO: s3://bucket/prefix/pattern`
- **File Pattern:** `TODO: output_pattern*.ext`
- **Format:** TODO (e.g., CSV, JSON, Parquet)
- **Purpose:** TODO: What this output provides
- **Content Contract:** See [Artifacts Catalog](../artifacts_catalog.md#TODO)

---

## Side Effects

TODO: Describe any side effects (deletes, overwrites, external system updates)

---

## Processing Logic (High Level)

1. TODO: Step 1
2. TODO: Step 2
3. TODO: Step 3

---

## Invariants and Constraints

- TODO: Key invariants that must always hold
- TODO: Constraints on data or processing

---

## Failure Modes

| Failure Mode | Cause | Impact | Recovery |
|--------------|-------|--------|----------|
| TODO         | TODO  | TODO   | TODO     |

---

## Operator Checks

**Pre-run:**
- TODO: What to verify before running

**Post-run:**
- TODO: What to verify after successful run
- Check run receipt for counters and status

---

## Dependencies

**Upstream Jobs:**
- TODO: List jobs that must run before this one

**Downstream Jobs:**
- TODO: List jobs that depend on this one's outputs

---

## Notes

- TODO: Additional context, assumptions, or considerations
"""


def generate_business_description_template(job_id: str, spec_name: str = None) -> str:
    """
    Generate a business job description template.
    
    Args:
        job_id: Job ID
        spec_name: Optional specification to reference
        
    Returns:
        Business description template as string
    """
    spec_ref = f"Based on specification: {spec_name}" if spec_name else "TODO: Reference specification or planning document"
    
    return f"""# Business Job Description: {job_id}

**Version:** 1.0.0  
**Last Updated:** {datetime.now().strftime("%Y-%m-%d")}  
**Status:** Draft  
**Specification:** {spec_ref}

---

## Purpose

TODO: Explain **why** this job exists and what business problem it solves.

---

## Business Objective

TODO: Define the business objective this job achieves. What value does it deliver to the organization or stakeholders?

---

## Inputs (Business Meaning)

### Input 1: TODO

**Business Meaning:** TODO: What this input represents from a business perspective (not technical storage details)

---

## Outputs (Business Meaning)

### Output 1: TODO

**Business Meaning:** TODO: What this output represents and how it's used by downstream processes or stakeholders

---

## Business Rules and Controls

1. TODO: Key business rule or control
2. TODO: Data quality requirements
3. TODO: Business logic constraints

---

## Boundaries (Non-Goals)

**What this job does NOT do:**
- TODO: Explicit exclusions
- TODO: Out of scope items

---

## Success Criteria (Business Perspective)

- TODO: How success is measured from a business perspective
- TODO: Key performance indicators or quality metrics

---

## Stakeholders

- **Owner:** TODO: Team or person responsible
- **Consumers:** TODO: Who uses the outputs
- **Reviewers:** TODO: Who reviews or approves

---

## Notes

- TODO: Additional business context, historical context, or future considerations
"""


def create_script_card(job_id: str, spec_name: str = None, overwrite: bool = False) -> int:
    """
    Create a script card for a job.
    
    Args:
        job_id: Job ID
        spec_name: Optional specification name
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    SCRIPT_CARDS_DIR.mkdir(parents=True, exist_ok=True)
    
    output_path = SCRIPT_CARDS_DIR / f"{job_id}.md"
    
    if output_path.exists() and not overwrite:
        print(f"Error: Script card already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    content = generate_script_card_template(job_id, spec_name)
    
    try:
        output_path.write_text(content, encoding="utf-8")
        print(f"✓ Created script card: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Fill in all TODO sections based on job implementation")
        print(f"2. Ensure parameters, inputs, outputs match job_manifest.yaml")
        print(f"3. Run validation: python tools/validate_repo_docs.py --all")
        return 0
    except Exception as e:
        print(f"Error: Failed to create script card: {e}", file=sys.stderr)
        return 1


def create_business_description(job_id: str, spec_name: str = None, overwrite: bool = False) -> int:
    """
    Create a business job description.
    
    Args:
        job_id: Job ID
        spec_name: Optional specification name
        overwrite: Whether to overwrite existing file
        
    Returns:
        0 on success, 1 on error
    """
    BUSINESS_DESC_DIR.mkdir(parents=True, exist_ok=True)
    
    output_path = BUSINESS_DESC_DIR / f"{job_id}.md"
    
    if output_path.exists() and not overwrite:
        print(f"Error: Business description already exists at {output_path}", file=sys.stderr)
        print("Use --overwrite to replace it.", file=sys.stderr)
        return 1
    
    content = generate_business_description_template(job_id, spec_name)
    
    try:
        output_path.write_text(content, encoding="utf-8")
        print(f"✓ Created business description: {output_path.relative_to(REPO_ROOT)}")
        print(f"\nNext steps:")
        print(f"1. Fill in all TODO sections with business context")
        print(f"2. Focus on 'why' not 'how'")
        print(f"3. Review with business stakeholders")
        return 0
    except Exception as e:
        print(f"Error: Failed to create business description: {e}", file=sys.stderr)
        return 1


def update_glossary_from_spec(spec_name: str) -> int:
    """
    Extract potential glossary terms from a specification.
    
    Args:
        spec_name: Name of the specification
        
    Returns:
        0 on success, 1 on error
    """
    spec_path = SPECIFICATIONS_DIR / f"{spec_name}.yaml"
    
    if not spec_path.exists():
        print(f"Error: Specification not found: {spec_path}", file=sys.stderr)
        return 1
    
    try:
        with spec_path.open("r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Failed to load specification: {e}", file=sys.stderr)
        return 1
    
    print(f"Suggested glossary terms from specification: {spec.get('subsystem_name', spec_name)}")
    print("=" * 80)
    print("\nReview these terms and add to docs/glossary.md if they are shared across jobs:")
    print()
    
    # Extract potential terms from inputs
    inputs = spec.get("inputs", [])
    if inputs:
        print("From Inputs:")
        for inp in inputs:
            name = inp.get("name", "")
            if name:
                print(f"  - {name}: {inp.get('purpose', 'TODO: Define term')}")
    
    # Extract potential terms from outputs
    outputs = spec.get("outputs", [])
    if outputs:
        print("\nFrom Outputs:")
        for out in outputs:
            name = out.get("name", "")
            if name:
                print(f"  - {name}: {out.get('purpose', 'TODO: Define term')}")
    
    # Extract from business rules
    business_rules = spec.get("processing_logic", {}).get("business_rules", [])
    if business_rules:
        print("\nFrom Business Rules:")
        for rule in business_rules:
            # Extract capitalized terms (potential domain terms)
            terms = re.findall(r'\b[A-Z][A-Za-z]+\b', rule)
            if terms:
                print(f"  - Consider terms from: {rule}")
    
    print("\n" + "=" * 80)
    print("\nNote: These are suggestions. Only add terms to glossary.md if they are:")
    print("  - Shared across multiple jobs")
    print("  - Business domain terms")
    print("  - Not obvious from context")
    
    return 0


def validate_documentation() -> int:
    """
    Run documentation validation.
    
    Returns:
        0 if validation passes, 1 if validation fails
    """
    validator_path = REPO_ROOT / "tools" / "validate_repo_docs.py"
    
    if not validator_path.exists():
        print("Error: validate_repo_docs.py not found", file=sys.stderr)
        return 1
    
    print("Running documentation validation...")
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
            print("✓ Documentation validation passed")
        else:
            print("-" * 60)
            print("✗ Documentation validation failed")
        
        return result.returncode
    except Exception as e:
        print(f"Error: Failed to run validation: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the documentation agent."""
    parser = argparse.ArgumentParser(
        description="Documentation Agent - Maintain project documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create script card for a job
  python documentation_agent.py script-card my_job_id --spec my_subsystem
  
  # Create business description for a job
  python documentation_agent.py business-desc my_job_id --spec my_subsystem
  
  # Suggest glossary terms from specification
  python documentation_agent.py glossary my_subsystem
  
  # Validate all documentation
  python documentation_agent.py validate
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Script card command
    script_parser = subparsers.add_parser("script-card", help="Create script card")
    script_parser.add_argument("job_id", help="Job ID")
    script_parser.add_argument("--spec", "-s", help="Specification name")
    script_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file")
    
    # Business description command
    business_parser = subparsers.add_parser("business-desc", help="Create business description")
    business_parser.add_argument("job_id", help="Job ID")
    business_parser.add_argument("--spec", "-s", help="Specification name")
    business_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file")
    
    # Glossary command
    glossary_parser = subparsers.add_parser("glossary", help="Suggest glossary terms from specification")
    glossary_parser.add_argument("spec_name", help="Specification name (without .yaml)")
    
    # Validate command
    subparsers.add_parser("validate", help="Validate all documentation")
    
    args = parser.parse_args()
    
    if args.command == "script-card":
        return create_script_card(args.job_id, args.spec, args.overwrite)
    elif args.command == "business-desc":
        return create_business_description(args.job_id, args.spec, args.overwrite)
    elif args.command == "glossary":
        return update_glossary_from_spec(args.spec_name)
    elif args.command == "validate":
        return validate_documentation()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

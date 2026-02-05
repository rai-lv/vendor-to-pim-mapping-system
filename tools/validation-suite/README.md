# Validation Suite

This directory contains the repository validation tools that enforce documentation standards and quality requirements.

## Overview

The validation suite consists of:
- **Main orchestrator**: `validate_repo_docs.py` - Coordinates all validators and provides unified interface
- **Specialized validators**: Individual validators for different document types and standards
- **Consistency checker**: Cross-document consistency validation

## Main Validator

**`validate_repo_docs.py`** - Main validation orchestrator with 12 validation modes.

Usage: See `docs/ops/tooling_reference.md` for detailed usage and `docs/agents/agent_tool_interaction_guide.md` for guidance on when agents should use validation tools.

```bash
# Run all validations
python tools/validation-suite/validate_repo_docs.py --all

# Run specific validations
python tools/validation-suite/validate_repo_docs.py --manifests
python tools/validation-suite/validate_repo_docs.py --context-docs
python tools/validation-suite/validate_repo_docs.py --security

# Show validation coverage
python tools/validation-suite/validate_repo_docs.py --coverage
```

## Specialized Validators

These validators are called by `validate_repo_docs.py` but can also be run independently:

- **`validate_context_docs.py`** - Validates context layer documents (development_approach.md, target_agent_system.md, system_context.md, glossary.md)
- **`validate_process_docs.py`** - Validates process layer documents (workflow_guide.md, contribution_approval_guide.md)
- **`validate_agent_docs.py`** - Validates agent layer documents (agent_role_charter.md, .github/agents/*.md)
- **`validate_job_docs.py`** - Validates per-job documents (business descriptions, script cards)
- **`validate_decision_records.py`** - Validates decision records and decision log
- **`validate_codable_tasks.py`** - Validates codable task specifications
- **`validate_naming_standard.py`** - Validates naming conventions across the repository
- **`check_doc_consistency.py`** - Detects contradictions and "double truth" across documentation

## Integration

All validators are integrated into CI/CD via `.github/workflows/pr_validation.yml` and run on every PR to ensure standards compliance.

See `docs/ops/VALIDATOR_CI_INTEGRATION.md` for CI integration details.

## Requirements

- Python 3.8+
- PyYAML (for manifest parsing)
- Standard library only otherwise

## Documentation

- **Validation standard**: `docs/standards/validation_standard.md`
- **Tooling reference**: `docs/ops/tooling_reference.md`
- **Agent usage guidance**: `docs/agents/agent_tool_interaction_guide.md`
- **CI integration**: `docs/ops/VALIDATOR_CI_INTEGRATION.md`

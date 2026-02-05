# Repository Tools

This directory contains automation tools that support the development workflow.

## Tool Categories

Per `docs/context/target_agent_system.md`, tools are categorized by their purpose:

### Scaffolding Tools

Tools that generate structured starting points and reduce manual effort.

- **`manifest-generator/`** - Generates draft `job_manifest.yaml` files from `glue_script.py` analysis
  - Extracts job parameters, I/O operations, runtime type
  - Produces ~80% complete drafts requiring human review
  - See `manifest-generator/README.md` for details

### Validation Tools

Tools that check conformance to repository standards deterministically.

- **`validation-suite/`** - Comprehensive validation tools for documentation and artifacts
  - Main orchestrator: `validate_repo_docs.py` with 12 validation modes
  - Specialized validators for each documentation layer
  - Integrated into CI/CD workflows
  - See `validation-suite/README.md` for details

### Evidence Tools

*(To be added as evidence tools are created)*

Tools that produce deterministic, reviewable outputs for verification.

## Documentation

- **Tooling reference**: `docs/ops/tooling_reference.md` - Complete operational manual for all tools
- **Agent guidance**: `docs/agents/agent_tool_interaction_guide.md` - How agents should use tools
- **Target agent system**: `docs/context/target_agent_system.md` - Conceptual framework for tools vs agents

## Usage Principles

1. **Tools generate drafts, not final answers** - Scaffolding outputs require human review
2. **Validation before approval** - Run validators before requesting human approval
3. **Evidence-based verification** - Use tools to produce reviewable evidence
4. **Agents use tools** - Tools don't replace agent judgment or human decisions

See `docs/agents/agent_tool_interaction_guide.md` for complete usage guidance.

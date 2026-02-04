# Vendor-to-PIM Mapping System

## What is this repository?

This repository is an **AI-supported development system** for building and maintaining automation components (primarily jobs and scripts) in the domain of **vendor → PIM mapping**.

"AI-supported" means:
- Humans remain the decision-makers (approval gates)
- Agents accelerate drafting, review, and implementation under human oversight
- Tools provide deterministic scaffolding, validation, and evidence

## Where to start

### For New Contributors

1. **Understand the system context**: Start with [`docs/context/system_context.md`](docs/context/system_context.md) to understand what this repository is and its scope boundaries

2. **Learn the development approach**: Read [`docs/context/development_approach.md`](docs/context/development_approach.md) to understand the 5-step working approach

3. **Review the workflow**: Consult [`docs/process/workflow_guide.md`](docs/process/workflow_guide.md) for step-by-step execution procedures

4. **Check standards**: Review relevant standards in `docs/standards/` for schemas and required fields

### Quick Reference

- **Documentation system overview**: [`docs/context/documentation_system_catalog.md`](docs/context/documentation_system_catalog.md)
- **Glossary**: [`docs/context/glossary.md`](docs/context/glossary.md)
- **Workflow guide**: [`docs/process/workflow_guide.md`](docs/process/workflow_guide.md)
- **Agent roles**: [`docs/agents/agent_role_charter.md`](docs/agents/agent_role_charter.md)
- **Standards**: `docs/standards/`

## Repository Structure

```
.
├── docs/              # Documentation system
│   ├── context/       # System context and intent
│   ├── process/       # Workflow and execution guides
│   ├── standards/     # Schemas and enforceable rules
│   ├── ops/           # Tooling and operational references
│   ├── agents/        # Agent roles and interaction guides
│   ├── catalogs/      # Living catalogs (artifacts, jobs, decisions)
│   └── registries/    # Registered resources
├── jobs/              # Job implementations
└── tools/             # Automation and validation tooling
```

## Documentation System

This repository uses a layered documentation system to prevent duplication and maintain a single source of truth:

- **Context layer**: Intent, shared meaning, and system framing
- **Standards layer**: Enforceable rules and schemas (validator-enforceable)
- **Agent documentation layer**: Agent roles and interaction guidance
- **Process layer**: How-to guidance for executing the workflow
- **Ops layer**: Technical manuals for tools and automation
- **Living catalogs and per-job docs**: Instance data and job-local documentation

For complete documentation catalog, see [`docs/context/documentation_system_catalog.md`](docs/context/documentation_system_catalog.md).

### Agent Roles

The system uses specialized agent roles to accelerate development under human oversight:

**Planning Support (Steps 1-3):**
- **Objective Support Agent**: Refines objectives with clear scope and success criteria (Step 1)
- **Pipeline Support Agent**: Decomposes objectives into ordered capabilities (Step 2)
- **Capability Support Agent**: Defines detailed capability specifications with acceptance criteria (Step 3)

**Execution Support (Steps 4-5):**
- **Coding Agent**: Implements approved codable tasks (Step 4)
- **Validation Support Agent**: Assembles evidence against acceptance criteria (Step 5)

**Continuous Support:**
- **Documentation Support Agent**: Maintains documentation consistency across all steps

For detailed agent responsibilities, see [`docs/agents/agent_role_charter.md`](docs/agents/agent_role_charter.md).  
For the agent operating model, see [`docs/context/target_agent_system.md`](docs/context/target_agent_system.md).

## How to Contribute

Follow the workflow defined in [`docs/process/workflow_guide.md`](docs/process/workflow_guide.md). Key principles:

- Human decision-makers with agent assistance
- Iterative planning and validation
- Explicit approval gates
- Evidence-based verification

For contribution approval process, see [`docs/process/contribution_approval_guide.md`](docs/process/contribution_approval_guide.md).

## Standards and Governance

Key standards documents:
- [Documentation Specification](docs/standards/documentation_spec.md)
- [Job Manifest Specification](docs/standards/job_manifest_spec.md)
- [Script Card Specification](docs/standards/script_card_spec.md)
- [Validation Standard](docs/standards/validation_standard.md)

All standards are enforced through automated validation and CI checks.

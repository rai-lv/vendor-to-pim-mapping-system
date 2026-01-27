# Documentation Index

Welcome to the vendor-to-pim-mapping-system documentation. This index provides a comprehensive guide to all documentation resources.

## Quick Links

### Getting Started
- **[5-Step Workflow](workflows/WORKFLOW_5_STEPS.md)** - Complete development process guide
- **[Agent Setup](workflows/AGENTS_SETUP.md)** - Install and use automation agents
- **[Workflow Diagram](workflows/WORKFLOW_DIAGRAM.md)** - Visual workflow overview

### Core Context
- **[Agent System Context](context_packs/agent_system_context.md)** - Detailed agent roles and workflows
- **[System Context](context_packs/system_context.md)** - Repository structure and standards
- **[GitHub Integration](context_packs/github_element_map.md)** - GitHub integration guide

## Documentation Structure

```
docs/
├── README.md                      # This file - documentation index
├── workflows/                     # Workflow and process documentation
│   ├── WORKFLOW_5_STEPS.md       # 5-step development process (authoritative)
│   ├── WORKFLOW_DIAGRAM.md       # Visual workflow diagrams
│   └── AGENTS_SETUP.md           # Agent installation and usage guide
├── context_packs/                # System context and standards
│   ├── agent_system_context.md   # Agent roles and workflows (authoritative)
│   ├── system_context.md         # Repository standards and structure
│   └── github_element_map.md     # GitHub integration patterns
├── roadmaps/                     # Planning documents (Steps 1 & 2a)
│   └── README.md                 # Roadmap creation guide
├── specifications/               # Capability specifications (Step 2b)
│   └── README.md                 # Specification creation guide
├── standards/                    # Documentation standards and specs
│   ├── job_manifest_spec.md
│   ├── script_card_spec.md
│   ├── business_job_description_spec.md
│   └── ...
├── script_cards/                 # Operational documentation
├── business_job_descriptions/    # Business intent documentation
├── codex-tasks/                  # Codex task templates
└── glossary.md                   # Shared terminology
```

## Documentation by Purpose

### For Planning (Steps 1-2)

**Define Objectives and Design Pipelines**

1. **[5-Step Workflow](workflows/WORKFLOW_5_STEPS.md)** - Understand the complete workflow
2. **[Roadmaps Guide](roadmaps/README.md)** - Create objective definitions (Step 1) and pipeline plans (Step 2a)
3. **[Specifications Guide](specifications/README.md)** - Create capability specifications (Step 2b)
4. **[Agent System Context](context_packs/agent_system_context.md)** - Understand agent roles in planning

### For Implementation (Steps 3-5)

**Decompose, Plan Tasks, and Write Code**

1. **[5-Step Workflow](workflows/WORKFLOW_5_STEPS.md)** - Steps 3-5 details
2. **[Agent Setup](workflows/AGENTS_SETUP.md)** - Use Coding Agent for decomposition and Codex tasks
3. **[Standards Directory](standards/)** - Follow documentation standards
4. **[System Context](context_packs/system_context.md)** - Understand repository structure

### For Documentation

**Create Script Cards and Business Descriptions**

1. **[Script Card Spec](standards/script_card_spec.md)** - Operational documentation standard
2. **[Business Job Description Spec](standards/business_job_description_spec.md)** - Business intent documentation standard
3. **[Job Manifest Spec](standards/job_manifest_spec.md)** - Job interface documentation
4. **[Glossary](glossary.md)** - Shared terminology (add new terms here)

### For Understanding the System

**Learn About Repository Architecture**

1. **[System Context](context_packs/system_context.md)** - Repository structure and development workflow
2. **[Agent System Context](context_packs/agent_system_context.md)** - Agent roles and automation
3. **[Workflow Diagram](workflows/WORKFLOW_DIAGRAM.md)** - Visual representation
4. **[GitHub Integration](context_packs/github_element_map.md)** - GitHub workflows and patterns

## Documentation Standards

All documentation in this repository follows strict standards defined in `standards/`:

- **[Naming Standard](standards/naming-standard.md)** - File and component naming conventions
- **[Job Manifest Spec](standards/job_manifest_spec.md)** - Job interface documentation
- **[Script Card Spec](standards/script_card_spec.md)** - Operational documentation
- **[Business Job Description Spec](standards/business_job_description_spec.md)** - Business intent documentation
- **[Job Inventory Spec](standards/job_inventory_spec.md)** - Job catalog structure
- **[Artifacts Catalog Spec](standards/artifacts_catalog_spec.md)** - Cross-job artifacts

## Validation

All documentation changes must pass validation:

```bash
python tools/validate_repo_docs.py --all
```

This validation runs automatically in CI via `.github/workflows/validate_standards.yml`.

## Key Principles

### Truth Hierarchy

1. **Code Truth**: `jobs/<job_group>/<job_id>/glue_script.py` - authoritative for runtime behavior
2. **Interface Truth**: `jobs/<job_group>/<job_id>/job_manifest.yaml` - authoritative for parameters and I/O
3. **Standards Truth**: `docs/standards/` - override everything for naming and structure
4. **Planning Truth**: `docs/roadmaps/` (Steps 1 & 2a) - authoritative for objectives and pipeline design
5. **Specification Truth**: `docs/specifications/` (Step 2b) - authoritative for capability details

### Documentation Guidelines

1. **No Duplication**: Shared terms belong in `glossary.md`, not in individual documents
2. **Evidence-Based**: Derive manifests and documentation from actual code, not assumptions
3. **Standards Compliance**: Follow specs in `docs/standards/` for all documentation types
4. **Cross-References**: Link related documents appropriately
5. **Version Control**: Update documentation as code changes

## Workflow Overview

This repository uses a **5-step development workflow**:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan / Pipeline-Level (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
   ↓
Step 4: Create Codex Tasks (Coding Agent)
   ↓
Step 5: Code Creation (PR Process)
```

**See:** [WORKFLOW_5_STEPS.md](workflows/WORKFLOW_5_STEPS.md) for complete details.

## Contributing

When adding or updating documentation:

1. **Follow Standards**: Check `docs/standards/` for the relevant spec
2. **Use Glossary**: Add shared terms to `glossary.md`, don't duplicate
3. **Validate Early**: Run `python tools/validate_repo_docs.py --all` after changes
4. **Cross-Reference**: Link related documents appropriately
5. **Get Review**: Have documentation reviewed by team members
6. **Update Index**: Update this README if adding new documentation categories

## Support

### Finding Documentation

- Use this README as your starting point
- Check the relevant section based on your task (Planning, Implementation, Documentation, Understanding)
- Follow cross-references to related documents

### Getting Help

1. **Workflow Questions**: See [WORKFLOW_5_STEPS.md](workflows/WORKFLOW_5_STEPS.md)
2. **Agent Usage**: See [AGENTS_SETUP.md](workflows/AGENTS_SETUP.md)
3. **Standards Questions**: Check `docs/standards/` for relevant spec
4. **Architecture Questions**: See [System Context](context_packs/system_context.md)

## Recent Changes

### Documentation Reorganization (2026-01-27)

- **Created** `docs/workflows/` directory for workflow documentation
- **Moved** `WORKFLOW_5_STEPS.md`, `WORKFLOW_DIAGRAM.md`, `AGENTS_SETUP.md` from root to `docs/workflows/`
- **Updated** `WORKFLOW_DIAGRAM.md` to align with 5-step workflow and current agent naming
- **Updated** `docs/roadmaps/README.md` to focus on roadmap-specific content
- **Updated** `docs/specifications/README.md` to align with Capability Planner Agent terminology
- **Updated** all cross-references to point to new file locations
- **Created** this documentation index (`docs/README.md`)

**Rationale**: Centralize workflow documentation in a dedicated directory for better organization and discoverability.

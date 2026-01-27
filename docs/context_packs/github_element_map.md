# GitHub Element Map

**Version:** 1.1 (Aligned with Development Approach)  
**Last Updated:** 2026-01-27

---

## Purpose

This document maps the GitHub repository's physical structure to the conceptual documentation and workflow elements defined in [`development_approach.md`](development_approach.md) and [`system_context.md`](system_context.md).

**Key Relationships:**
- **Governance Framework**: [`development_approach.md`](development_approach.md) defines principles and workflows
- **Repository Context**: [`system_context.md`](system_context.md) defines structure and standards
- **Physical Structure**: This document shows where concepts are stored in GitHub

---

## Repository Structure Overview

```
vendor-to-pim-mapping-system/
  README.md                         # Repository introduction and quick start
  .gitignore                        # Git exclusions

  docs/                             # Documentation root (5 functional layers)
    README.md                       # Documentation index and navigation guide

    context_packs/                  # CONTEXT LAYER — Foundation documents
      development_approach.md       # Core principles, governance, agent collaboration model
      system_context.md             # Repository structure, workflows, truth hierarchy
      agent_system_context.md       # Agent roles, responsibilities, detailed workflows
      github_element_map.md         # THIS FILE — GitHub structure mapping
      documentation_system.md       # Documentation catalog and metadata

    workflows/                      # PROCESS LAYER — Workflow guides
      WORKFLOW_5_STEPS.md           # Complete 5-step development process
      WORKFLOW_DIAGRAM.md           # Visual workflow overview and integration
      AGENTS_SETUP.md               # Agent installation and usage guide

    roadmaps/                       # PLANNING LAYER — Objectives and pipeline plans
      README.md                     # Planning guide (Steps 1, 2a)
      <objective>.md                # Step 1: Objective definitions (Planner Agent)
      <objective>_pipeline_plan.md  # Step 2a: Pipeline plans (Pipeline Planner Agent)

    specifications/                 # SPECIFICATION LAYER — Capability plans
      README.md                     # Specification guide (Step 2b)
      <capability>_capability.yaml  # Step 2b: Capability specifications (Capability Planner Agent)

    standards/                      # GOVERNANCE LAYER — Normative specifications
      job_manifest_spec.md          # Job manifest schema and rules
      script_card_spec.md           # Script card structure requirements
      business_job_description_spec.md  # Business description requirements
      job_inventory_spec.md         # Job inventory derivation rules
      artifacts_catalog_spec.md     # Artifacts catalog structure rules
      naming-standard.md            # Naming conventions (TBD/sparse)

    business_job_descriptions/      # ARTIFACT LAYER — Business intent docs
      <job_id>.md                   # Business purpose, rules, boundaries per job

    script_cards/                   # ARTIFACT LAYER — Operational reference docs
      <job_id>.md                   # Operational interface, parameters, I/O per job

    codex-tasks/                    # IMPLEMENTATION LAYER — Task templates
      pr_review_checklist.md        # PR review criteria
      <task>.md                     # Codex task specifications (Step 4)

    job_inventory.md                # CATALOG — Authoritative job index
    artifacts_catalog.md            # CATALOG — Cross-job artifacts catalog
    glossary.md                     # CATALOG — Shared terminology definitions

  jobs/                             # Code artifacts (truth hierarchy: Code > Manifests)
    <job_group>/                    # Logical job grouping
      <job_id>/                     # Individual job directory
        glue_script.py              # CODE TRUTH — Runtime behavior (authoritative)
        job_manifest.yaml           # INTERFACE TRUTH — Parameters, I/O, side effects
        configs/                    # Optional: S3 config mirrors
        samples/                    # Optional: Redacted examples

  tools/                            # Agent tools and validation (implements 5 agent functions)
    planner_agent.py                # Planning Function — Step 1: Objective definitions
    pipeline_planner_agent.py       # Planning Function — Step 2a: Pipeline plans
    capability_planner_agent.py     # Specification Function — Step 2b: Capability specs
    coding_agent.py                 # Implementation Function — Steps 3-4: Decompose and tasks
    testing_agent.py                # Validation Function — Step 5: Testing and validation
    documentation_agent.py          # Documentation Function — Step 5: Doc maintenance
    designer_agent.py               # (Legacy/deprecated)
    validate_repo_docs.py           # Standards validation (CI gate)

  .github/                          # GitHub integration and CI/CD
    copilot-instructions.md         # GitHub Copilot guidance (repository conventions)
    workflows/                      # GitHub Actions workflows
      WORKFLOWS_README.md           # Workflow documentation and guide
      WORKFLOW_DIAGRAM.md           # Workflow visual diagrams
      IMPLEMENTATION_SUMMARY.md     # Workflow implementation decisions
      planner_workflow.yml          # Step 1 automation
      pipeline_planner_workflow.yml # Step 2a automation
      capability_planner_workflow.yml # Step 2b automation
      coding_workflow.yml           # Steps 3-4 automation
      testing_workflow.yml          # Step 5 validation automation
      documentation_workflow.yml    # Step 5 documentation automation
      pr_validation.yml             # PR quality gates
      validate_standards.yml        # Standards compliance CI gate
      designer_workflow.yml         # (Legacy/deprecated)

  logs/                             # Testing and execution logs
    tests_logs/                     # Test execution logs
      README.md                     # Log format and usage guide
```

---

## Conceptual Mapping: Workflows to Files

### Development Approach → Physical Locations

| Concept (development_approach.md) | Physical Location | Agent Tool | Output Artifact |
|-----------------------------------|-------------------|------------|-----------------|
| **Step 1: Define Objective** | `docs/roadmaps/` | `tools/planner_agent.py` | `<objective>.md` |
| **Step 2a: Pipeline Plan** | `docs/roadmaps/` | `tools/pipeline_planner_agent.py` | `<objective>_pipeline_plan.md` |
| **Step 2b: Capability Plan** | `docs/specifications/` | `tools/capability_planner_agent.py` | `<capability>_capability.yaml` |
| **Step 3: Decompose** | (Console output) | `tools/coding_agent.py` | Development elements list |
| **Step 4: Codex Tasks** | `docs/codex-tasks/` | `tools/coding_agent.py` | `<task>.md` |
| **Step 5: Code Creation** | `jobs/` | Human/Codex | Python scripts, manifests |
| **Step 5: Validation** | `logs/tests_logs/` | `tools/testing_agent.py` | Test logs |
| **Step 5: Documentation** | `docs/business_job_descriptions/`<br/>`docs/script_cards/` | `tools/documentation_agent.py` | Business descriptions, script cards |

### Agent Functions → Agent Tools

| Agent Function (development_approach.md) | Agent Tools | Location |
|------------------------------------------|-------------|----------|
| **Planning Function** | Planner Agent<br/>Pipeline Planner Agent | `tools/planner_agent.py`<br/>`tools/pipeline_planner_agent.py` |
| **Specification Function** | Capability Planner Agent | `tools/capability_planner_agent.py` |
| **Implementation Function** | Coding Agent | `tools/coding_agent.py` |
| **Validation Function** | Testing Agent | `tools/testing_agent.py` |
| **Documentation Function** | Documentation Agent | `tools/documentation_agent.py` |

### Truth Hierarchy → Physical Sources

| Truth Level (system_context.md) | Physical Location | Authority |
|----------------------------------|-------------------|-----------|
| **Governance Truth** | `docs/context_packs/development_approach.md` | Human inputs > Standards > Automation |
| **Code Truth** | `jobs/<job_group>/<job_id>/glue_script.py` | Runtime behavior |
| **Interface Truth** | `jobs/<job_group>/<job_id>/job_manifest.yaml` | Parameters, I/O, side effects |
| **Standards Truth** | `docs/standards/*.md` | Structure, naming, validation rules |
| **Business Truth** | `docs/business_job_descriptions/<job_id>.md` | Business intent, why |
| **Operational Truth** | `docs/script_cards/<job_id>.md` | Operational interface, how |

---

## Documentation Layers Mapping

Per [`documentation_system.md`](documentation_system.md), documentation is organized into 5 functional layers:

### 1. Context Layer (Foundation)
**Location**: `docs/context_packs/`
- `development_approach.md` — Core principles and governance
- `system_context.md` — Repository structure and workflows
- `agent_system_context.md` — Agent roles and implementation
- `github_element_map.md` — This file (structure mapping)
- `documentation_system.md` — Documentation catalog

### 2. Process Layer (Workflows)
**Location**: `docs/workflows/`
- `WORKFLOW_5_STEPS.md` — Complete development process
- `WORKFLOW_DIAGRAM.md` — Visual workflow representations
- `AGENTS_SETUP.md` — Agent installation and usage

### 3. Governance Layer (Standards)
**Location**: `docs/standards/`
- Normative specifications controlling structure and compliance
- Enforced via `tools/validate_repo_docs.py` in CI

### 4. Planning & Implementation Layer (Guides)
**Location**: `docs/roadmaps/`, `docs/specifications/`
- Guides for creating planning and specification documents
- Outputs from agent-assisted workflow (Steps 1, 2a, 2b)

### 5. Artifact Layer (Job Documentation & Catalogs)
**Location**: `docs/business_job_descriptions/`, `docs/script_cards/`, `docs/job_inventory.md`, `docs/artifacts_catalog.md`
- Job-specific documentation
- Cross-job catalogs and inventories
- Operational guides

---

## Governance Enforcement

### Manual Checkpoints (Human Oversight)

Per [`development_approach.md`](development_approach.md) § Manual Oversight and Checkpoints:

| Checkpoint | Approval Required | Document | Approver Role |
|------------|-------------------|----------|---------------|
| **Step 1 → Step 2a** | Objective definition approved | `docs/roadmaps/<objective>.md` | Product Owner + Stakeholders |
| **Step 2a → Step 2b** | Pipeline plan approved | `docs/roadmaps/<objective>_pipeline_plan.md` | Tech Lead + Stakeholders |
| **Step 2b → Step 3** | Capability specification approved | `docs/specifications/<capability>_capability.yaml` | Business + Tech Leads |
| **Step 4 → Step 5** | Codex task approved | `docs/codex-tasks/<task>.md` | Developer |
| **Step 5 → Merge** | PR approved + tests pass | PR in GitHub | Code Reviewer |

### Automated Quality Gates

| Gate | Tool | Location | Enforces |
|------|------|----------|----------|
| **Standards Validation** | `tools/validate_repo_docs.py` | CI (`.github/workflows/validate_standards.yml`) | Truth hierarchy, format compliance |
| **Testing Validation** | `tools/testing_agent.py` | CI (`.github/workflows/testing_workflow.yml`) | Specification-based testing |
| **PR Validation** | GitHub Actions | CI (`.github/workflows/pr_validation.yml`) | Quality criteria, acceptance tests |

---

## Integration Points

### GitHub Actions Workflow Triggers

| Workflow | Trigger | Agent | Implements |
|----------|---------|-------|------------|
| `planner_workflow.yml` | Manual dispatch | Planner Agent | Step 1 (Planning Function) |
| `pipeline_planner_workflow.yml` | Manual dispatch | Pipeline Planner Agent | Step 2a (Planning Function) |
| `capability_planner_workflow.yml` | Manual dispatch | Capability Planner Agent | Step 2b (Specification Function) |
| `coding_workflow.yml` | Manual dispatch | Coding Agent | Steps 3-4 (Implementation Function) |
| `testing_workflow.yml` | PR creation, manual | Testing Agent | Step 5 (Validation Function) |
| `documentation_workflow.yml` | Manual dispatch | Documentation Agent | Step 5 (Documentation Function) |
| `pr_validation.yml` | PR creation | Validation scripts | Quality gates |
| `validate_standards.yml` | PR creation | `validate_repo_docs.py` | Standards enforcement |

---

## Navigation Guide

### For Developers

- **Starting a new feature**: [`docs/workflows/WORKFLOW_5_STEPS.md`](../workflows/WORKFLOW_5_STEPS.md)
- **Understanding workflows**: [`docs/context_packs/development_approach.md`](development_approach.md)
- **Repository structure**: [`docs/context_packs/system_context.md`](system_context.md)
- **Agent usage**: [`docs/workflows/AGENTS_SETUP.md`](../workflows/AGENTS_SETUP.md)

### For Agents/Copilot

- **Core principles**: [`docs/context_packs/development_approach.md`](development_approach.md)
- **Agent roles**: [`docs/context_packs/agent_system_context.md`](agent_system_context.md)
- **Repository conventions**: [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)
- **Standards**: [`docs/standards/`](../standards/)

### For Documentation

- **Documentation system**: [`docs/context_packs/documentation_system.md`](documentation_system.md)
- **Job documentation**: [`docs/standards/script_card_spec.md`](../standards/script_card_spec.md), [`docs/standards/business_job_description_spec.md`](../standards/business_job_description_spec.md)
- **Glossary**: [`docs/glossary.md`](../glossary.md)

---

## Related Documentation

- **[Development Approach](development_approach.md)** — Core principles and governance framework
- **[System Context](system_context.md)** — Repository structure and workflows  
- **[Agent System Context](agent_system_context.md)** — Agent roles and implementation
- **[Documentation System](documentation_system.md)** — Documentation catalog and metadata

---

**Version History:**
- **v1.1 (2026-01-27):** Updated to reflect current structure, aligned with development_approach.md, added governance and workflow mappings
- **v1.0:** Initial version (outdated)

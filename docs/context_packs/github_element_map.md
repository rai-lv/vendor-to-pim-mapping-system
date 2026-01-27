# GitHub Element Map — Repository Structure and Governance

**Version:** 1.1  
**Last Updated:** 2026-01-27  
**Purpose:** Map GitHub repository structure to conceptual documentation elements and governance hierarchy

---

## Overview

This document maps the physical GitHub repository structure to the logical organization of documentation, code, and governance artifacts. It reflects the **governance hierarchy** where human-defined inputs and standards take precedence over agent-generated outputs.

---

## Repository Structure

```
vendor-to-pim-mapping-system/
  README.md                         # Entry point for repository
  CHANGELOG.md                      # Version history
  
  docs/
    # Foundation Layer (Human-Defined Governance)
    context_packs/
      development_approach.md       # 🔒 LOCKED TRUTH: Core principles and governance
      system_context.md             # Master context: structure, workflows, truth hierarchy
      agent_system_context.md       # Agent-assisted workflows with human oversight
      github_element_map.md         # THIS FILE
      documentation_system.md       # Documentation metadata and organization
    
    # Standards Layer (Normative Specifications - Human Authority)
    standards/
      job_manifest_spec.md          # Manifest schema and validation rules
      business_job_description_spec.md  # Business documentation standard
      script_card_spec.md           # Operational documentation standard
      artifacts_catalog_spec.md     # Cross-job artifacts specification
      job_inventory_spec.md         # Job catalog specification
      naming-standard.md            # Naming conventions
    
    # Planning Layer (Human-Approved with Agent Assistance)
    roadmaps/                       # Step 1 & 2a outputs (require human approval)
      <objective>.md                # Step 1: Objective definitions (agent-assisted, human-approved)
      <objective>_pipeline_plan.md  # Step 2a: Pipeline plans (agent-assisted, human-approved)
    
    specifications/                 # Step 2b outputs (require human approval)
      <capability>_capability.yaml  # Step 2b: Capability specs (agent-assisted, human-approved)
    
    # Implementation Guidance Layer (Templates and Checklists)
    codex-tasks/
      context_header_template.md    # Template for Codex task context
      task_template.md              # Template for PR-sized tasks
      pr_review_checklist.md        # Human review checklist for PRs
    
    workflows/
      WORKFLOW_5_STEPS.md           # Complete 5-step development process
      WORKFLOW_DIAGRAM.md           # Visual workflow representations
      AGENTS_SETUP.md               # Agent installation and usage guide
    
    # Documentation Layer (Evidence-Based, Human-Validated)
    job_inventory.md                # Factual index of jobs (derived from manifests)
    artifacts_catalog.md            # Factual catalog of artifacts (cross-job references)
    glossary.md                     # Canonical term definitions (shared across jobs)
    
    business_job_descriptions/      # Business intent (human-defined "why")
      <job_id>.md                   # Business purpose, rules, boundaries
    
    script_cards/                   # Operational reference (evidence-based "what")
      <job_id>.md                   # Factual I/O + side effects + invariants
    
    # Governance Artifacts
    registries/
      shared_artifacts_allowlist.yaml  # Normative registry for shared artifacts
    
    decisions/
      ADR-0001-monorepo.md          # Architectural decision records
  
  # Code Layer (Source of Truth for Runtime Behavior)
  jobs/
    <job_group>/
      <job_id>/
        glue_script.py              # 🔒 CODE TRUTH: Runtime behavior (authoritative)
        job_manifest.yaml           # 🔒 INTERFACE TRUTH: Parameters, I/O, side effects
        configs/                    # Job-specific configuration files
        samples/                    # Optional: Redacted sample data
  
  # Agent Tools (Assistant Scripts - Subject to Human Direction)
  tools/
    planner_agent.py                # Step 1: Assists with objective definition
    pipeline_planner_agent.py       # Step 2a: Assists with pipeline planning
    capability_planner_agent.py     # Step 2b: Assists with capability specs
    coding_agent.py                 # Steps 3-4: Assists with decomposition and tasks
    testing_agent.py                # Assists with validation (results reviewed by humans)
    documentation_agent.py          # Assists with docs (outputs reviewed by humans)
    validate_repo_docs.py           # Automated standards validation
  
  # CI/CD and GitHub Integration
  .github/
    workflows/
      validate_standards.yml        # CI gate: Standards validation (automated)
      planner_workflow.yml          # GitHub Actions: Step 1 automation
      pipeline_planner_workflow.yml # GitHub Actions: Step 2a automation
      capability_planner_workflow.yml # GitHub Actions: Step 2b automation
      pr_validation.yml             # PR validation (automated checks, human review)
    
    copilot-instructions.md         # Instructions for GitHub Copilot
    pull_request_template.md        # PR template enforcing documentation + scope discipline
  
  # Logs and Artifacts
  logs/
    tests_logs/                     # Test execution logs (for human review)
```

---

## Governance Hierarchy in Repository Structure

The repository structure reflects the **truth hierarchy** from `development_approach.md`:

### Level 1: Human-Defined Inputs (Highest Authority)
- **Location:** `docs/roadmaps/`, `docs/specifications/`
- **Content:** Objectives, pipeline plans, capability specifications
- **Governance:** Requires explicit human approval at each step
- **Agent Role:** Propose drafts; humans decide and approve

### Level 2: Standards and Criteria
- **Location:** `docs/standards/`, `docs/context_packs/development_approach.md`
- **Content:** Normative specifications, core principles
- **Governance:** Define validation rules; override all other sources in conflicts
- **Agent Role:** None; standards are human-defined

### Level 3: Code and Interface Truth
- **Location:** `jobs/<job_group>/<job_id>/glue_script.py`, `job_manifest.yaml`
- **Content:** Runtime behavior, parameters, I/O contracts
- **Governance:** Authoritative for implementation behavior
- **Agent Role:** May propose changes via Codex tasks; humans review PRs

### Level 4: Documentation (Evidence-Based)
- **Location:** `docs/business_job_descriptions/`, `docs/script_cards/`
- **Content:** Business intent and operational reference
- **Governance:** Must derive from and align with code/manifests
- **Agent Role:** May generate drafts; humans validate accuracy

### Level 5: Automated Outputs
- **Location:** Agent-generated proposals, test reports, validation results
- **Content:** Recommendations, test results, validation reports
- **Governance:** Subordinate to all above levels; require human review
- **Agent Role:** Generate outputs for human review and decision

---

## Human Approval Artifacts

The following artifacts capture **explicit human approval** and governance decisions:

| Artifact | Purpose | Human Approval Captured |
|----------|---------|-------------------------|
| `docs/roadmaps/<objective>.md` | Step 1: Objective definition | Manual discussion and consensus documented |
| `docs/roadmaps/<objective>_pipeline_plan.md` | Step 2a: Pipeline architecture | Architecture approval documented |
| `docs/specifications/<capability>.yaml` | Step 2b: Capability specification | Specification approval documented |
| `.github/pull_request_template.md` | PR review checklist | Forces documentation of changes and scope |
| Git commit messages and PR descriptions | Change rationale | Captures human decision-making |
| PR review comments and approvals | Code review | Human validation before merge |

---

## Agent-Generated vs. Human-Defined Content

### Human-Defined (Authoritative)
- Core principles (`development_approach.md`)
- Standards and specifications (`docs/standards/`)
- Approved objectives, plans, and specifications
- Code implementations (via human-reviewed PRs)
- Final documentation (after human validation)

### Agent-Assisted (Proposal/Draft Stage)
- Initial planning artifacts (require approval)
- Codex task proposals (require review)
- Test results (require human interpretation)
- Documentation drafts (require validation)
- Validation reports (inform human decisions)

---

## Navigation Guide

### For Understanding Repository Purpose
1. Start: `README.md`
2. Then: `docs/context_packs/system_context.md`
3. Deep dive: `docs/context_packs/development_approach.md`

### For Agent-Assisted Development
1. Governance: `docs/context_packs/development_approach.md`
2. Agent details: `docs/context_packs/agent_system_context.md`
3. Workflow: `docs/workflows/WORKFLOW_5_STEPS.md`
4. Setup: `docs/workflows/AGENTS_SETUP.md`

### For Understanding Jobs
1. Overview: `docs/job_inventory.md`
2. Business context: `docs/business_job_descriptions/<job_id>.md`
3. Operations: `docs/script_cards/<job_id>.md`
4. Code: `jobs/<job_group>/<job_id>/glue_script.py`

### For Standards Compliance
1. Relevant spec: `docs/standards/<type>_spec.md`
2. Validation: `python tools/validate_repo_docs.py --all`

---

**Version History:**
- v1.1 (2026-01-27): Enhanced to reflect governance hierarchy and human oversight mechanisms
- v1.0 (Initial): Basic repository structure map
```

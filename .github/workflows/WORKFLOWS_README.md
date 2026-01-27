# GitHub Actions Workflows Documentation

## Overview

This repository uses GitHub Actions workflows to automate and enforce the agent-driven 5-step development process. Workflows are designed to:

1. **Automate agent execution** at appropriate steps
2. **Enforce manual approval gates** for planning phases
3. **Validate quality standards** throughout the development process
4. **Provide clear guidance** on next steps in the workflow

## Workflow Architecture

### Workflow Categories

#### 1. Planning Workflows (Steps 1-2)
These workflows assist in the planning phase but **require manual approval** before proceeding to the next step.

- **Planner Agent Workflow** (Step 1)
- **Pipeline Planner Agent Workflow** (Step 2a)
- **Capability Planner Agent Workflow** (Step 2b)

#### 2. Implementation Workflows (Steps 3-4)
These workflows support decomposition and task creation.

- **Coding Agent Workflow** (Steps 3-4)

#### 3. Validation Workflows (Step 5)
These workflows enforce quality gates and standards.

- **PR Validation and Quality Gates** (comprehensive PR validation)
- **Testing Agent Workflow** (automated testing)
- **Documentation Agent Workflow** (documentation validation)
- **Standards Validation** (repository standards)

#### 4. Legacy/Alternative Workflows
- **Designer Agent Workflow** (alternative to Pipeline/Capability Planner workflows)

---

## Detailed Workflow Descriptions

### 1. Planner Agent Workflow (Step 1)

**File:** `.github/workflows/planner_workflow.yml`

**Purpose:** Create objective definition documents for new development initiatives.

**When to Use:** At the start of any new project or major feature.

**Trigger:** Manual (`workflow_dispatch`)

**Inputs:**
- `phase_name`: Planning phase name (e.g., "Q1 2026 Features")
- `description`: Brief description of the planning objective
- `overwrite`: Overwrite existing document if it exists (default: false)

**Process:**
1. Creates initial objective document at `docs/roadmaps/<phase_name>.md`
2. Validates document structure
3. Commits document to repository
4. Displays next steps and manual approval requirements

**Manual Approval Required:**
- ✓ Review objective document
- ✓ Fill in all TODO sections
- ✓ Review with stakeholders (Product Owner, Tech Lead, Business)
- ✓ Obtain explicit approval
- ✓ Lock document before proceeding to Step 2a

**Next Step:** Pipeline Planner Agent Workflow (Step 2a)

---

### 2. Pipeline Planner Agent Workflow (Step 2a)

**File:** `.github/workflows/pipeline_planner_workflow.yml`

**Purpose:** Create end-to-end pipeline plan showing processing sequence and conceptual artifacts.

**When to Use:** After Step 1 objective is approved.

**Trigger:** Manual (`workflow_dispatch`)

**Inputs:**
- `objective_name`: Objective name (must match approved Step 1 document)
- `objective_file`: Objective filename (e.g., "vendor_onboarding.md")
- `overwrite`: Overwrite existing pipeline plan if it exists (default: false)

**Process:**
1. **Validates Step 1 prerequisites** (objective document exists and is complete)
2. Creates pipeline plan at `docs/roadmaps/<objective_name>_pipeline_plan.md`
3. Validates pipeline plan structure
4. Commits pipeline plan to repository
5. Displays next steps and manual approval requirements

**Manual Approval Required:**
- ✓ Review pipeline plan
- ✓ Define complete processing sequence
- ✓ Identify decision points and fallback paths
- ✓ Define conceptual artifacts (by meaning, NOT S3 paths)
- ✓ Map existing jobs to pipeline steps
- ✓ Review with stakeholders (Tech Lead, Architect)
- ✓ Obtain explicit approval
- ✓ Lock document before proceeding to Step 2b

**Next Step:** Capability Planner Agent Workflow (Step 2b) for EACH capability

---

### 3. Capability Planner Agent Workflow (Step 2b)

**File:** `.github/workflows/capability_planner_workflow.yml`

**Purpose:** Create detailed capability specification for ONE pipeline step.

**When to Use:** After Step 2a pipeline plan is approved, repeat for each capability.

**Trigger:** Manual (`workflow_dispatch`)

**Inputs:**
- `capability_name`: Capability name (e.g., "data_validation")
- `pipeline_plan_file`: Pipeline plan filename (e.g., "vendor_onboarding_pipeline_plan.md")
- `overwrite`: Overwrite existing specification if it exists (default: false)

**Process:**
1. **Validates Step 2a prerequisites** (pipeline plan exists and is complete)
2. Creates capability specification at `docs/specifications/<capability_name>_capability.yaml`
3. Validates specification structure
4. Commits specification to repository
5. Displays next steps and manual approval requirements

**Manual Approval Required:**
- ✓ Review capability specification
- ✓ Define inputs/outputs (by MEANING, not S3 paths)
- ✓ Define business rules and logic
- ✓ Define testable acceptance criteria
- ✓ Define explicit boundaries
- ✓ Review with stakeholders (Tech Lead, QA Lead)
- ✓ Obtain explicit approval
- ✓ Lock document before proceeding to Step 3

**Next Step:** 
- If more capabilities remain: Repeat Step 2b
- If all capabilities complete: Coding Agent Workflow (Step 3)

---

### 4. Coding Agent Workflow (Steps 3-4)

**File:** `.github/workflows/coding_workflow.yml`

**Purpose:** Decompose capabilities into development elements and generate Codex tasks.

**When to Use:** After all Step 2b capability specifications are approved.

**Trigger:** 
- Manual (`workflow_dispatch`)
- Automatic on specification changes (validation only)

**Actions:**
- `list_tasks`: List development tasks for a capability (Step 3 - Decompose)
- `validate`: Validate repository code and documentation
- `check_practices`: Check coding best practices
- `generate_codex_task`: Generate Codex task specification (Step 4)

**Inputs:**
- `action`: Action to perform (required)
- `spec_name`: Specification name (required for list_tasks and generate_codex_task)
- `task_id`: Task ID (required for generate_codex_task)

**Process:**
1. **Validates Step 2b prerequisites** (capability specification exists)
2. Executes requested action
3. Displays output and next steps

**Prerequisites Validated:**
- ✓ Step 1 objective is approved
- ✓ Step 2a pipeline plan is approved
- ✓ Step 2b capability specification is approved
- ✓ Step 3 decomposition is complete (for Step 4)

**Next Step:** Create PR using Codex task (Step 5)

---

### 5. PR Validation and Quality Gates

**File:** `.github/workflows/pr_validation.yml`

**Purpose:** Comprehensive validation of all pull requests before merge.

**When to Use:** Automatically triggered on all PRs.

**Trigger:** Automatic on `pull_request` events (opened, synchronize, reopened, ready_for_review)

**Validation Jobs:**

#### Job 1: Syntax Validation
- Validates Python syntax for all `.py` files
- Validates YAML syntax for all `.yaml` and `.yml` files
- **Critical:** PR cannot merge if syntax validation fails

#### Job 2: Standards Compliance
- Runs `python tools/validate_repo_docs.py --all`
- Validates manifest placeholder style (`${NAME}` required)
- **Critical:** PR cannot merge if standards validation fails

#### Job 3: Planning Artifacts Validation
- Validates Step 1 objective definitions (required sections)
- Validates Step 2a pipeline plans (required sections)
- Validates Step 2b capability specifications (required fields)
- Triggered only if planning artifacts are modified

#### Job 4: Quality Gates
- Checks for TODO comments
- Runs best practices check (`python tools/coding_agent.py check`)
- Triggered only if code changes are detected

#### Job 5: Testing Validation
- Runs `python tools/testing_agent.py run --no-log`
- Uploads test results as artifacts
- Triggered only if code or specification changes are detected

#### Job 6: Documentation Validation
- Runs `python tools/documentation_agent.py validate`
- Checks for documentation updates when code changes
- Triggered only if documentation or code changes are detected

#### Job 7: Validation Summary
- Summarizes all validation results
- Fails PR if critical validations fail
- Displays warnings for non-critical issues

**Next Step:** Review and merge PR if all validations pass

---

### 6. Testing Agent Workflow

**File:** `.github/workflows/testing_workflow.yml`

**Purpose:** Automated testing and validation.

**When to Use:**
- Manually: Before committing code
- Automatically: On PRs and merges to main

**Trigger:**
- Manual (`workflow_dispatch`)
- Automatic on PRs (paths: `jobs/**/*.py`, `jobs/**/*.yaml`, `tools/**/*.py`, `docs/specifications/*.yaml`)
- Automatic on push to main (paths: `jobs/**/*.py`, `jobs/**/*.yaml`, `tools/**/*.py`)

**Actions:**
- `run_tests`: Run test suite (optionally for specific specification)
- `infer_tests`: Infer test requirements from specification
- `list_logs`: List test logs

**Inputs:**
- `action`: Action to perform (required)
- `spec_name`: Specification name (optional for run_tests, required for infer_tests)
- `no_log`: Skip writing log file (default: false)

**Process:**
1. Runs requested action
2. On PRs: Runs tests without logging
3. On push to main: Runs tests with logging and commits logs
4. Uploads test logs as artifacts

---

### 7. Documentation Agent Workflow

**File:** `.github/workflows/documentation_workflow.yml`

**Purpose:** Generate and validate documentation artifacts.

**When to Use:**
- Manually: To generate documentation for new/modified jobs
- Automatically: On PRs (reminder) and merges to main (validation)

**Trigger:**
- Manual (`workflow_dispatch`)
- Automatic on push to main (paths: `jobs/**/*.py`, `jobs/**/*.yaml`, `docs/specifications/*.yaml`)
- Automatic on PRs (paths: `jobs/**/*.py`, `jobs/**/*.yaml`)
- Automatic on workflow completion (Planner, Designer workflows)

**Actions:**
- `create_script_card`: Create operational reference documentation
- `create_business_desc`: Create business intent documentation
- `suggest_glossary`: Suggest glossary terms from specification
- `validate`: Validate documentation compliance

**Inputs:**
- `action`: Action to perform (required)
- `job_id`: Job ID (required for create_script_card and create_business_desc)
- `spec_name`: Specification name (optional reference)
- `overwrite`: Overwrite existing file (default: false)

**Process:**
1. Executes requested action
2. On PRs: Displays documentation reminder
3. On push: Validates documentation
4. Commits generated documentation to repository

---

### 8. Standards Validation

**File:** `.github/workflows/validate_standards.yml`

**Purpose:** Validate repository standards compliance on all PRs.

**When to Use:** Automatically triggered on all PRs.

**Trigger:** Automatic on `pull_request` events

**Process:**
1. Checks for BOM (Byte Order Mark) issues
2. Runs `python tools/validate_repo_docs.py --all`
3. **Critical:** PR cannot merge if validation fails

---

### 9. Designer Agent Workflow (Legacy/Alternative)

**File:** `.github/workflows/designer_workflow.yml`

**Purpose:** Create subsystem specifications (alternative to Pipeline/Capability Planner workflows).

**Status:** Legacy workflow, consider using Pipeline Planner and Capability Planner workflows instead.

**When to Use:** For simple subsystems that don't require full pipeline planning.

**Trigger:**
- Manual (`workflow_dispatch`)
- Automatic on planning document updates (notification only)

**Inputs:**
- `subsystem_name`: Subsystem name (e.g., "vendor_ingestion_pipeline")
- `planning_phase`: Planning phase reference (optional)
- `overwrite`: Overwrite existing specification (default: false)

---

## Workflow Integration with 5-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Define Objective                                    │
│ Workflow: planner_workflow.yml                              │
│ Output: docs/roadmaps/<objective>.md                         │
│ ✋ MANUAL APPROVAL REQUIRED                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2a: Pipeline Plan                                      │
│ Workflow: pipeline_planner_workflow.yml                     │
│ Output: docs/roadmaps/<objective>_pipeline_plan.md          │
│ ✋ MANUAL APPROVAL REQUIRED                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2b: Capability Specification                           │
│ Workflow: capability_planner_workflow.yml                   │
│ Output: docs/specifications/<capability>_capability.yaml    │
│ ✋ MANUAL APPROVAL REQUIRED (repeat for each capability)     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Decompose into Development Elements                 │
│ Workflow: coding_workflow.yml (action: list_tasks)          │
│ Output: Console output                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Create Codex Tasks                                  │
│ Workflow: coding_workflow.yml (action: generate_codex_task) │
│ Output: Console output                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Code Creation (PR Process)                          │
│ Workflows:                                                   │
│   - pr_validation.yml (comprehensive validation)             │
│   - testing_workflow.yml (automated testing)                 │
│   - documentation_workflow.yml (documentation validation)    │
│   - validate_standards.yml (standards validation)            │
│ Quality Gates: ALL must pass before merge                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Manual vs Automated Steps

### Manual Steps (Human Decision Required)

**Steps 1-2: Planning Phase**
- ✋ **Step 1 Approval:** Review and approve objective definition
- ✋ **Step 2a Approval:** Review and approve pipeline plan
- ✋ **Step 2b Approval:** Review and approve capability specification (for each capability)

**Workflows Assist, Humans Decide:**
- Workflows create initial templates
- Stakeholders review, discuss, and refine
- Explicit approval required before proceeding
- Workflows enforce prerequisites but cannot bypass approvals

### Automated Steps (Workflows Execute)

**Steps 3-5: Implementation and Validation**
- ✓ **Step 3:** Coding Agent suggests decomposition
- ✓ **Step 4:** Coding Agent generates Codex tasks
- ✓ **Step 5:** Multiple workflows validate PRs automatically

**Quality Gates (Automated):**
- Syntax validation (Python, YAML)
- Standards compliance
- Testing validation
- Documentation validation
- Best practices checks

---

## Usage Examples

### Example 1: New Development Initiative

```bash
# Step 1: Define Objective
Go to: Actions → Planner Agent Workflow → Run workflow
Input: phase_name="vendor_onboarding", description="Implement vendor onboarding pipeline"

# Edit and approve: docs/roadmaps/vendor_onboarding.md
# ✋ MANUAL APPROVAL REQUIRED

# Step 2a: Create Pipeline Plan
Go to: Actions → Pipeline Planner Agent Workflow → Run workflow
Input: objective_name="vendor_onboarding", objective_file="vendor_onboarding.md"

# Edit and approve: docs/roadmaps/vendor_onboarding_pipeline_plan.md
# ✋ MANUAL APPROVAL REQUIRED

# Step 2b: Create Capability Specification (for each capability)
Go to: Actions → Capability Planner Agent Workflow → Run workflow
Input: capability_name="data_ingestion", pipeline_plan_file="vendor_onboarding_pipeline_plan.md"

# Edit and approve: docs/specifications/data_ingestion_capability.yaml
# ✋ MANUAL APPROVAL REQUIRED
# Repeat for all capabilities

# Step 3: Decompose Capability
Go to: Actions → Coding Agent Workflow → Run workflow
Input: action="list_tasks", spec_name="data_ingestion_capability"
# Review console output for suggested decomposition

# Step 4: Generate Codex Task
Go to: Actions → Coding Agent Workflow → Run workflow
Input: action="generate_codex_task", spec_name="data_ingestion_capability", task_id="1"
# Use Codex task output to create PR

# Step 5: Create PR
# PR triggers automatic validation workflows:
#   - pr_validation.yml (comprehensive checks)
#   - testing_workflow.yml (automated testing)
#   - documentation_workflow.yml (documentation checks)
#   - validate_standards.yml (standards compliance)
# All quality gates must pass before merge
```

### Example 2: Update Existing Job

```bash
# Create PR with code changes
# Workflows automatically trigger:

# 1. PR Validation (pr_validation.yml)
#    - Validates Python/YAML syntax
#    - Checks standards compliance
#    - Runs quality gates
#    - Validates testing
#    - Validates documentation

# 2. Testing (testing_workflow.yml)
#    - Runs automated test suite

# 3. Documentation Reminder (documentation_workflow.yml)
#    - Reminds to update documentation

# Review validation results and address any failures
# Once all checks pass, merge PR

# After merge to main:
# - testing_workflow.yml runs full test suite with logging
# - documentation_workflow.yml validates documentation
```

---

## Quality Gates Summary

### Critical Gates (Must Pass for Merge)

1. **Python Syntax Validation** ✓
   - All `.py` files must have valid syntax

2. **YAML Syntax Validation** ✓
   - All `.yaml`/`.yml` files must have valid syntax

3. **Standards Compliance** ✓
   - `python tools/validate_repo_docs.py --all` must pass
   - Manifests must use `${NAME}` placeholder style

### Non-Critical Gates (Warnings Only)

4. **TODO Comments Check** ⚠️
   - Warns if TODO comments found in code

5. **Best Practices Check** ⚠️
   - `python tools/coding_agent.py check` may show warnings

6. **Documentation Updates** ⚠️
   - Reminds to update documentation for code changes

---

## Workflow Maintenance

### Adding New Workflows

1. Create workflow file in `.github/workflows/`
2. Define triggers (`on:` section)
3. Define jobs with clear names
4. Add validation steps
5. Add next steps guidance
6. Update this documentation

### Modifying Existing Workflows

1. Review current workflow behavior
2. Make minimal changes
3. Test workflow triggers
4. Update this documentation
5. Create PR with changes
6. Review and merge after validation

### Best Practices

- **Clear naming:** Use descriptive job and step names
- **Fail fast:** Validate prerequisites early
- **Clear output:** Use echo statements to guide users
- **Error handling:** Provide actionable error messages
- **Documentation:** Keep this file updated with changes

---

## Troubleshooting

### Workflow Not Triggering

**Problem:** Workflow doesn't run when expected

**Solutions:**
1. Check trigger conditions (`on:` section)
2. Verify file paths in `paths:` filters
3. Ensure branch matches (usually `main`)
4. Check if workflow is disabled in Actions settings

### Validation Failing

**Problem:** PR validation fails with errors

**Solutions:**
1. Read error messages carefully
2. Run validation locally: `python tools/validate_repo_docs.py --all`
3. Fix syntax errors in Python/YAML files
4. Ensure manifests use `${NAME}` placeholder style
5. Complete required sections in planning documents

### Prerequisites Not Met

**Problem:** Workflow fails with "prerequisites not met" error

**Solutions:**
1. Ensure previous steps are completed and approved
2. Check that required files exist (objective, pipeline plan, capability spec)
3. Verify file naming matches expected patterns
4. Complete all required sections in planning documents

---

## Related Documentation

- **[System Context](../docs/context_packs/system_context.md)** — Repository structure and workflows
- **[Agent System Context](../docs/context_packs/agent_system_context.md)** — Detailed agent roles and responsibilities
- **[5-Step Workflow](../docs/workflows/WORKFLOW_5_STEPS.md)** — Complete development process guide
- **[Agents Setup](../docs/workflows/AGENTS_SETUP.md)** — Agent installation and usage

---

**Last Updated:** 2026-01-27  
**Version:** 2.0 (Enhanced with comprehensive PR validation and agent integration)

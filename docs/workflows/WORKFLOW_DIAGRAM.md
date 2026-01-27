# 5-Step Workflow - Visual Overview

## Development Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     5-Step Development Workflow                      │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  STEP 1: DEFINE OBJECTIVE                                            │
│  Planner Agent                                                       │
│  ────────────────                                                    │
│  Manual Trigger | Manual Discussion & Approval Required             │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Creates: docs/roadmaps/<objective>.md
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 2a: OVERARCHING PLAN (Pipeline-Level)                          │
│  Pipeline Planner Agent                                              │
│  ───────────────────────                                             │
│  Manual Trigger | Manual Discussion & Approval Required             │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Creates: docs/roadmaps/<objective>_pipeline_plan.md
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 2b: CAPABILITY PLAN (Step-Level)                               │
│  Capability Planner Agent                                            │
│  ─────────────────────────                                           │
│  Manual Trigger | Manual Discussion & Approval Required             │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Creates: docs/specifications/<capability>_capability.yaml
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 3: DECOMPOSE INTO DEVELOPMENT ELEMENTS                         │
│  Coding Agent (decompose command)                                    │
│  ─────────────────────────────────                                   │
│  Manual Trigger | Review & Adjust Decomposition                      │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Outputs: Console - Suggested PR-sized elements
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 4: CREATE CODEX TASKS                                          │
│  Coding Agent (codex-task command)                                   │
│  ──────────────────────────────────                                  │
│  Manual Trigger | Create Task for Each Element                       │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Outputs: Console - Codex task with standards refs
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 5: CODE CREATION                                               │
│  GitHub Copilot / Manual Development                                 │
│  ───────────────────────────────────                                 │
│  PR Process | Quality Gates | Testing | Documentation                │
└────────┬─────────────────────────────────────────────────────────────┘
         │ Creates: jobs/**/*.py, job_manifest.yaml, docs updates
         ▼
┌──────────────────┐
│   DEPLOYMENT     │
│   (Manual)       │
└──────────────────┘
```

## Agent Flow and Dependencies

```
┌─────────────────┐
│  Step 1         │
│  Planner Agent  │
└────────┬────────┘
         │ Objective approved
         ▼
┌──────────────────────┐
│  Step 2a             │
│  Pipeline Planner    │
│  Agent               │
└────────┬─────────────┘
         │ Pipeline plan approved
         ▼
┌──────────────────────┐
│  Step 2b             │
│  Capability Planner  │
│  Agent               │
└────────┬─────────────┘
         │ Capability spec approved
         ▼
┌──────────────────────┐      ┌─────────────────┐
│  Step 3              │      │  Testing        │
│  Coding Agent        │────→ │  Agent          │
│  (decompose)         │      │  (validation)   │
└────────┬─────────────┘      └─────────────────┘
         │                              │
         ▼                              │
┌──────────────────────┐                │
│  Step 4              │                │
│  Coding Agent        │                │
│  (codex-task)        │                │
└────────┬─────────────┘                │
         │                              │
         ▼                              ▼
┌──────────────────────┐      ┌─────────────────┐
│  Step 5              │      │  Documentation  │
│  Code Creation       │────→ │  Agent          │
│  (PR Process)        │      │  (script cards) │
└──────────────────────┘      └─────────────────┘
```

## Trigger Matrix

| Step | Agent | Manual | Auto | Approval Gate | Output |
|------|-------|--------|------|---------------|--------|
| 1 | Planner | ✅ | - | ✅ Stakeholder | Objective doc |
| 2a | Pipeline Planner | ✅ | - | ✅ Stakeholder | Pipeline plan |
| 2b | Capability Planner | ✅ | - | ✅ Stakeholder | Capability spec |
| 3 | Coding (decompose) | ✅ | - | ✅ Review | Decomposition |
| 4 | Coding (codex-task) | ✅ | - | - | Codex task |
| 5 | GitHub Copilot/Manual | ✅ | - | ✅ PR Review | Code changes |
| - | Testing | ✅ | ✅ PR/Merge | - | Test logs |
| - | Documentation | ✅ | ✅ Post-merge | - | Script cards |

## File Flow

```
Step 1: Define Objective
  └─> docs/roadmaps/
        └─> <objective>.md

Step 2a: Pipeline Plan
  └─> docs/roadmaps/
        └─> <objective>_pipeline_plan.md

Step 2b: Capability Plan
  └─> docs/specifications/
        └─> <capability>_capability.yaml

Step 3: Decompose
  └─> Console output (suggested elements)

Step 4: Codex Task
  └─> Console output (task details)

Step 5: Code Creation
  └─> jobs/
        └─> <job_group>/<job_id>/
              ├─> glue_script.py
              └─> job_manifest.yaml
  └─> docs/script_cards/
        └─> <job_id>.md
  └─> docs/business_job_descriptions/
        └─> <job_id>.md

Testing (Continuous)
  └─> logs/tests_logs/
        └─> test_run_<timestamp>.log
```

## Quality Gates

```
Every Step
    │
    ▼
┌────────────────┐
│  Manual        │  ✓ Stakeholder review (Steps 1, 2a, 2b)
│  Approval      │  ✓ Team review (Steps 3, 4)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Standards     │  ✓ validate_repo_docs.py --all
│  Validation    │  ✓ Manifest/spec compliance
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Python Syntax │  ✓ All .py files compile
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  YAML Syntax   │  ✓ All .yaml files parse
└───────┬────────┘
        │
        ▼
    Proceed OK
```

## Agent Automation Levels

### 🔴 Manual Only (Planning Phase)
- **Step 1: Planner Agent** - Manual trigger, manual discussion
- **Step 2a: Pipeline Planner Agent** - Manual trigger, manual discussion
- **Step 2b: Capability Planner Agent** - Manual trigger, manual discussion
- **Step 3: Coding Agent (decompose)** - Manual trigger, manual review
- **Step 4: Coding Agent (codex-task)** - Manual trigger

**Why Manual?** Planning requires human judgment, stakeholder consensus, and business context that agents cannot provide.

### 🟡 Semi-Automated (Implementation Phase)
- **Step 5: Code Creation** - Manual coding with agent assistance
- **Testing Agent** - Automated validation, manual trigger for full test suite
- **Documentation Agent** - Automated reminders, manual generation

**Why Semi-Automated?** Implementation requires human judgment on code quality and documentation clarity.

### 🟢 Fully Automated (Validation Phase)
- **Testing on PR** - Runs automatically, validates changes
- **Testing on Merge** - Runs automatically, generates logs
- **Standards Validation** - Runs on all PRs via CI

**Why Fully Automated?** Validation is objective and can be fully automated.

## Directory Ownership

| Directory | Owner | Purpose | Step |
|-----------|-------|---------|------|
| `docs/roadmaps/` | Planner + Pipeline Planner | Objectives & pipeline plans | 1, 2a |
| `docs/specifications/` | Capability Planner | Capability specifications | 2b |
| `jobs/` | Human + Copilot | Job implementations | 5 |
| `docs/script_cards/` | Documentation Agent | Operational docs | Post-5 |
| `docs/business_job_descriptions/` | Documentation Agent | Business docs | Post-5 |
| `logs/tests_logs/` | Testing Agent | Test logs | Continuous |

## Workflow Enforcement Rules

### Two Planning Layers Required

Before ANY code change:
1. **Step 2a must be completed and approved** (pipeline-level plan)
2. **Step 2b must be completed and approved** (capability-level plan)

### No Assumptions

- All unknowns must be explicitly marked
- Open decisions must be documented
- DO NOT proceed with assumptions - clarify first

### Explicit Boundaries

At every step, explicitly state:
- What IS included
- What is NOT included
- What is deferred to other capabilities/steps

### Evidence-Based

- Map existing jobs to pipeline steps where applicable
- Define artifacts by meaning (what they represent)
- Storage details (S3 paths) come LATER in implementation

## Success Metrics

Each step tracks:
- ✅ Documents/artifacts created
- ✅ Approvals obtained
- ✅ Validations passed
- ✅ Standards compliance
- ⚠ Warnings identified
- ❌ Errors found

## Integration with Existing System

The 5-step workflow integrates with existing repository infrastructure:

1. **Standards Validation**: Uses existing `validate_repo_docs.py`
2. **CI/CD**: Extends existing GitHub Actions setup
3. **Documentation Structure**: Follows existing specs in `docs/standards/`
4. **Job Structure**: Works with existing `jobs/` layout

## Next Steps After Setup

1. **Step 1**: Create first objective definition
2. **Step 2a**: Design pipeline plan from objective
3. **Step 2b**: Create capability specifications for each pipeline step
4. **Step 3**: Decompose capabilities into PR-sized elements
5. **Step 4**: Generate Codex tasks for each element
6. **Step 5**: Implement code following Codex tasks

All agents ready to use! 🚀

## See Also

- **Complete Workflow:** `WORKFLOW_5_STEPS.md`
- **Agent System:** `../context_packs/agent_system_context.md`
- **Agent Setup:** `AGENTS_SETUP.md`
- **Repository Context:** `../context_packs/system_context.md`

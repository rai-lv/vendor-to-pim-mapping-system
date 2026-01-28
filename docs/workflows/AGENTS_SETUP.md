# GitHub Workflow Agents - Setup Guide

This document provides a comprehensive guide to the automated workflow agents implemented in this repository.

## ⚠️ Important: Use the 5-Step Workflow

This repository follows a 5-step development workflow. See `WORKFLOW_5_STEPS.md` for complete workflow details and `docs/context_packs/agent_system_context.md` for governance principles.

**Quick Reference:**
1. **Define Objective** (Planner Agent)
2. **Overarching Plan / Pipeline-Level** (Pipeline Planner Agent)  
3. **Capability Plan / Step-Level** (Capability Planner Agent)
4. **Decompose into Elements** (Coding Agent - decompose)
5. **Create Codex Tasks** (Coding Agent - codex-task)

## Overview

Six specialized agents have been implemented to automate the 5-step development workflow:

1. **Planner Agent** - Step 1: Define objectives with testable success criteria
2. **Pipeline Planner Agent** - Step 2a: Create overarching pipeline plans
3. **Capability Planner Agent** - Step 2b: Create detailed capability specifications
4. **Coding Agent** - Steps 3 & 4: Decompose and create Codex tasks
5. **Testing Agent** - Automated validation and testing
6. **Documentation Agent** - Documentation generation and maintenance

**Note:** The repository also contains a legacy `designer_agent.py` script that predates the current 5-step workflow. New development should use the Pipeline Planner Agent (Step 2a) and Capability Planner Agent (Step 2b) instead.

Each agent consists of:
- A Python script in `tools/` directory
- A GitHub Actions workflow in `.github/workflows/` (where applicable)
- Dedicated output directories

## Quick Start (5-Step Workflow)

### Step 1: Define Objective

**Agent:** Planner Agent  
**Purpose:** Define what must be achieved with explicit boundaries and testable criteria

Via CLI:
```bash
python tools/planner_agent.py create "vendor_onboarding" \
  --description "Implement vendor onboarding pipeline"
```

**Output:** `docs/roadmaps/vendor_onboarding.md`

### Step 2a: Overarching Plan (Pipeline-Level)

**Agent:** Pipeline Planner Agent  
**Purpose:** Create end-to-end pipeline plan with processing sequence and decision points

Via CLI:
```bash
python tools/pipeline_planner_agent.py create "vendor_onboarding" \
  --objective-ref "vendor_onboarding.md"
```

**Output:** `docs/roadmaps/vendor_onboarding_pipeline_plan.md`

### Step 2b: Capability Plan (Step-Level)

**Agent:** Capability Planner Agent  
**Purpose:** Specify ONE capability from pipeline plan in detail

Via CLI:
```bash
python tools/capability_planner_agent.py create "data_ingestion" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"
```

**Output:** `docs/specifications/data_ingestion_capability.yaml`

### Step 3: Decompose into Development Elements

**Agent:** Coding Agent  
**Purpose:** Break capability into PR-sized elements

Via CLI:
```bash
python tools/coding_agent.py decompose data_ingestion_capability
```

**Output:** Console output with suggested elements

### Step 4: Create Codex Tasks

**Agent:** Coding Agent  
**Purpose:** Generate Codex task for each element

Via CLI:
```bash
python tools/coding_agent.py codex-task data_ingestion_capability 1
```

**Output:** Console output with Codex task details

## Additional Workflow Support

### Testing

**Run full test suite:**

```bash
python tools/testing_agent.py run
```

**Run tests for specific specification:**

```bash
python tools/testing_agent.py run --spec vendor_ingestion_pipeline
```

**View test logs:**

```bash
python tools/testing_agent.py logs
```

### Documentation

**Create script card:**

```bash
python tools/documentation_agent.py script-card my_job_id \
  --spec vendor_ingestion_pipeline
```

**Create business description:**

```bash
python tools/documentation_agent.py business-desc my_job_id \
  --spec vendor_ingestion_pipeline
```

**Validate documentation:**

```bash
python tools/documentation_agent.py validate
```

## Workflow Automation

### Automatic Triggers

1. **Pipeline Planner Agent / Capability Planner Agent**
   - Triggered when planning documents are updated in `docs/roadmaps/`
   - Provides notification to create specifications

2. **Coding Agent**
   - Triggered when specifications are updated in `docs/specifications/`
   - Runs validation automatically

3. **Testing Agent**
   - Triggered on pull requests (validation only, no logs)
   - Triggered on merge to main (with logs)
   - Runs on code changes in `jobs/` directory

4. **Documentation Agent**
   - Triggered when code is merged to main
   - Triggered when specifications are finalized
   - Provides reminder to update documentation

### Manual Triggers

All agents can be manually triggered via GitHub Actions:

1. Navigate to: Repository → Actions
2. Select the desired workflow
3. Click "Run workflow"
4. Fill in required inputs
5. Click "Run workflow"

## Directory Structure

```
.
├── .github/
│   └── workflows/
│       ├── planner_workflow.yml          # Planner automation (Step 1)
│       ├── designer_workflow.yml         # Pipeline/Capability Planner automation (Steps 2a & 2b)
│       ├── coding_workflow.yml           # Coding assistance (Steps 3 & 4)
│       ├── testing_workflow.yml          # Testing automation
│       ├── documentation_workflow.yml    # Documentation automation
│       └── validate_standards.yml        # Standards validation
│
├── tools/
│   ├── planner_agent.py                  # Step 1: Define Objective
│   ├── pipeline_planner_agent.py         # Step 2a: Pipeline Plan
│   ├── capability_planner_agent.py       # Step 2b: Capability Plan
│   ├── coding_agent.py                   # Steps 3 & 4: Decompose + Codex
│   ├── testing_agent.py                  # Testing automation
│   ├── documentation_agent.py            # Documentation automation
│   └── validate_repo_docs.py             # Standards validation
│
├── docs/
│   ├── roadmaps/                         # Step 1 & 2a outputs
│   │   └── README.md                     # Roadmaps guide
│   ├── specifications/                   # Step 2b outputs
│   │   └── README.md                     # Specifications guide
│   ├── script_cards/                     # Operational docs
│   ├── business_job_descriptions/        # Business docs
│   ├── standards/                        # Repository standards
│   ├── context_packs/                    # Context documents
│   └── glossary.md                       # Shared terms
│
├── logs/
│   └── tests_logs/                       # Test execution logs
│       └── README.md                     # Logs guide
│
└── jobs/                                 # Job implementations (Step 5)
```

## Agent Details

### Planner Agent (Step 1)

**Purpose:** Define objectives with testable success criteria and explicit boundaries

**Commands:**
- `create <objective_name>` - Create objective definition
- `list` - List all objectives

**Workflow:** `.github/workflows/planner_workflow.yml`

**Outputs:** `docs/roadmaps/<objective_name>.md`

**Key Features:**
- Testable success criteria
- Explicit out-of-scope boundaries
- Risk assessment and unknowns

### Pipeline Planner Agent (Step 2a)

**Purpose:** Create end-to-end pipeline plans with processing sequence

**Commands:**
- `create <objective_name>` - Create pipeline plan
- `list` - List all pipeline plans

**Workflow:** Not yet implemented (manual for now)

**Outputs:** `docs/roadmaps/<objective_name>_pipeline_plan.md`

**Key Features:**
- Processing sequence (first → last)
- Decision points and fallback paths
- Conceptual artifacts (by meaning, not storage)
- Existing job mapping
- Explicit unknowns

### Capability Planner Agent (Step 2b)

**Purpose:** Create detailed capability specifications for pipeline steps

**Commands:**
- `create <capability_name>` - Create capability plan
- `list` - List all capability plans
- `validate <file>` - Validate capability plan

**Workflow:** Not yet implemented (manual for now)

**Outputs:** `docs/specifications/<capability_name>_capability.yaml`

**Key Features:**
- Inputs/outputs by meaning (not storage)
- Business rules and acceptance criteria
- Explicit boundaries (what it does/doesn't do)
- Dependencies mapping

### Coding Agent (Steps 3 & 4)

**Purpose:** Decompose capabilities and create Codex tasks

**Commands:**
- `decompose <capability>` - Step 3: Break into PR-sized elements
- `codex-task <capability> <element_id>` - Step 4: Generate Codex task
- `validate` - Run repository validation
- `check` - Check best practices

**Workflow:** `.github/workflows/coding_workflow.yml`

**Key Features:**
- Step 3: Decomposition into PR-sized elements
- Step 4: Codex tasks with standards references, TARGET_SCRIPT, file restrictions
- Quality gates enforcement

### Testing Agent

**Purpose:** Automated testing and validation

**Commands:**
- `run` - Run full test suite
- `run --spec <spec>` - Run tests for specification
- `infer <spec>` - Infer test requirements
- `logs` - List test logs

**Workflow:** `.github/workflows/testing_workflow.yml`

**Outputs:** `logs/tests_logs/test_run_<timestamp>.log`

### Documentation Agent

**Purpose:** Generate and maintain documentation

**Commands:**
- `script-card <job_id>` - Create script card
- `business-desc <job_id>` - Create business description
- `glossary <spec>` - Suggest glossary terms
- `validate` - Validate documentation

**Workflow:** `.github/workflows/documentation_workflow.yml`

**Outputs:** `docs/script_cards/`, `docs/business_job_descriptions/`

## Development Workflow

### 5-Step Workflow (Required)

See `WORKFLOW_5_STEPS.md` for complete workflow details and `docs/context_packs/agent_system_context.md` for governance principles. Summary:

```
Step 1: Define Objective (Planner Agent)
   ↓
Step 2a: Pipeline Plan (Pipeline Planner Agent)
   ↓
Step 2b: Capability Plan (Capability Planner Agent)
   ↓
Step 3: Decompose (Coding Agent - decompose)
   ↓
Step 4: Codex Task (Coding Agent - codex-task)
   ↓
Step 5: Code Creation (PR process)
   ↓
Testing (Testing Agent - automatic)
   ↓
Documentation (Documentation Agent)
```

## Troubleshooting

### Common Issues

**Issue:** Agent script not found
```bash
# Ensure you're in the repository root
cd /path/to/vendor-to-pim-mapping-system

# Verify tools directory exists
ls tools/
```

**Issue:** Workflow not triggering
```bash
# Check workflow file syntax
cat .github/workflows/<workflow>.yml

# Verify trigger conditions are met
git log --oneline -5
```

**Issue:** Validation fails
```bash
# Run validation to see errors
python tools/validate_repo_docs.py --all

# Fix reported issues
# Re-run validation
```

**Issue:** Test logs not created
```bash
# Ensure directory exists
mkdir -p logs/tests_logs

# Run without --no-log flag
python tools/testing_agent.py run
```

## Getting Help

### Documentation
- Agent-specific: See READMEs in output directories
- Repository standards: `docs/context_packs/system_context.md`
- Specifications: `docs/standards/`

### Command Help
```bash
# Get help for any agent
python tools/<agent>.py --help
python tools/<agent>.py <command> --help
```

### Examples

See `docs/roadmaps/README.md` for comprehensive examples of:
- Creating planning documents
- Creating specifications
- Running tests
- Generating documentation

## Contributing

When adding or modifying agents:

1. Update the Python script in `tools/`
2. Update the GitHub Actions workflow in `.github/workflows/`
3. Test locally before committing
4. Update relevant README files
5. Run validation: `python tools/validate_repo_docs.py --all`
6. Update this guide if workflow changes

## Summary

This agent system provides:
- ✅ Automated workflow management
- ✅ Consistent documentation generation
- ✅ Continuous validation and testing
- ✅ Clear development lifecycle
- ✅ Reduced manual overhead

All agents are designed to work together as a cohesive system while also being independently useful for specific tasks.

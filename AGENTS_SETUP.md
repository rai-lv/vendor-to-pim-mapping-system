# GitHub Workflow Agents - Setup Guide

This document provides a comprehensive guide to the automated workflow agents implemented in this repository.

## Overview

Five specialized agents have been implemented to automate the development lifecycle:

1. **Planner Agent** - High-level planning and objectives
2. **Designer Agent** - Subsystem specifications and design
3. **Coding Agent** - Code implementation assistance
4. **Testing Agent** - Automated validation and testing
5. **Documentation Agent** - Documentation generation and maintenance

Each agent consists of:
- A Python script in `tools/` directory
- A GitHub Actions workflow in `.github/workflows/`
- Dedicated output directories

## Quick Start

### 1. Planning Phase

**Create a planning document:**

Via CLI:
```bash
python tools/planner_agent.py create "Q1 2026 Features" \
  --description "Plan Q1 feature development"
```

Via GitHub Actions:
1. Go to: Actions → Planner Agent Workflow
2. Click "Run workflow"
3. Enter phase name and description
4. Click "Run workflow"

**Output:** `docs/roadmaps/q1_2026_features.md`

### 2. Design Phase

**Create a subsystem specification:**

Via CLI:
```bash
python tools/designer_agent.py create "vendor_ingestion_pipeline" \
  --planning-phase "Q1 2026 Features"
```

Via GitHub Actions:
1. Go to: Actions → Designer Agent Workflow
2. Click "Run workflow"
3. Enter subsystem name and planning phase
4. Click "Run workflow"

**Output:** `docs/specifications/vendor_ingestion_pipeline.yaml`

### 3. Coding Phase

**List coding tasks:**

```bash
python tools/coding_agent.py tasks vendor_ingestion_pipeline
```

**Generate Codex task outline:**

```bash
python tools/coding_agent.py codex-task vendor_ingestion_pipeline 1
```

**Validate code:**

```bash
python tools/coding_agent.py validate
```

### 4. Testing Phase

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

### 5. Documentation Phase

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

1. **Designer Agent**
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
│       ├── planner_workflow.yml          # Planner automation
│       ├── designer_workflow.yml         # Designer automation
│       ├── coding_workflow.yml           # Coding assistance
│       ├── testing_workflow.yml          # Testing automation
│       ├── documentation_workflow.yml    # Documentation automation
│       └── validate_standards.yml        # Existing validation
│
├── tools/
│   ├── planner_agent.py                  # Planning automation
│   ├── designer_agent.py                 # Design automation
│   ├── coding_agent.py                   # Coding assistance
│   ├── testing_agent.py                  # Testing automation
│   ├── documentation_agent.py            # Documentation automation
│   └── validate_repo_docs.py             # Existing validation
│
├── docs/
│   ├── roadmaps/                         # Planning documents
│   │   └── README.md                     # Roadmaps guide
│   ├── specifications/                   # Design specifications
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
└── jobs/                                 # Job implementations
```

## Agent Details

### Planner Agent

**Purpose:** Create high-level planning documents

**Commands:**
- `create <phase_name>` - Create planning document
- `list` - List all planning documents

**Workflow:** `.github/workflows/planner_workflow.yml`

**Outputs:** `docs/roadmaps/<phase_name>.md`

### Designer Agent

**Purpose:** Create subsystem specifications

**Commands:**
- `create <subsystem>` - Create specification
- `list` - List all specifications
- `validate <file>` - Validate specification

**Workflow:** `.github/workflows/designer_workflow.yml`

**Outputs:** `docs/specifications/<subsystem>.yaml`

### Coding Agent

**Purpose:** Assist with code implementation

**Commands:**
- `tasks <spec>` - List coding tasks
- `validate` - Run repository validation
- `check` - Check best practices
- `codex-task <spec> <task_id>` - Generate Codex task outline

**Workflow:** `.github/workflows/coding_workflow.yml`

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

### Standard Flow

```
1. Plan (Planner Agent)
   ↓
2. Design (Designer Agent)
   ↓
3. Implement (Coding Agent)
   ↓
4. Test (Testing Agent)
   ↓
5. Document (Documentation Agent)
```

### Iteration Flow

```
Code Changes
   ↓
Testing Agent (automatic on PR)
   ↓
Review Results
   ↓
Fix Issues
   ↓
Merge (automatic testing + logging)
   ↓
Documentation Agent (reminder)
```

## Best Practices

1. **Start with Planning**
   - Always create a planning document first
   - Define clear objectives and constraints
   - Get stakeholder approval before proceeding

2. **Detailed Specifications**
   - Break down plans into focused subsystems
   - Define clear I/O contracts
   - Create specific, testable tasks

3. **Validate Frequently**
   - Run validation after each change
   - Check test results before merging
   - Review documentation for completeness

4. **Use Automation**
   - Leverage GitHub Actions for consistency
   - Let agents handle boilerplate
   - Focus human effort on logic and decisions

5. **Document Continuously**
   - Update documentation as you code
   - Keep script cards and business descriptions in sync
   - Add new terms to glossary

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

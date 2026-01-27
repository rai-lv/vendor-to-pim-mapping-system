# GitHub Workflow Agents

This directory contains automated workflow agents that support the development lifecycle for this repository. Each agent has a corresponding Python script in `tools/` and a GitHub Actions workflow.

## Agent Overview

### 1. Planner Agent
**Purpose:** Define high-level planning and objectives for project phases.

**Script:** `tools/planner_agent.py`  
**Workflow:** `.github/workflows/planner_workflow.yml`  
**Output:** `docs/roadmaps/<planning_phase>.md`  
**Trigger:** Manual (workflow_dispatch)

**Usage:**
```bash
# Via CLI
python tools/planner_agent.py create "Q1 2026 Features" --description "Plan Q1 development"
python tools/planner_agent.py list

# Via GitHub Actions
# Go to: Actions → Planner Agent Workflow → Run workflow
```

### 2. Designer Agent
**Purpose:** Break down high-level plans into actionable subsystem specifications.

**Script:** `tools/designer_agent.py`  
**Workflow:** `.github/workflows/designer_workflow.yml`  
**Output:** `docs/specifications/<subsystem>.yaml`  
**Trigger:** Manual or when planning documents are updated

**Usage:**
```bash
# Via CLI
python tools/designer_agent.py create "vendor_ingestion_pipeline" --planning-phase "Q1 2026"
python tools/designer_agent.py list
python tools/designer_agent.py validate docs/specifications/my_spec.yaml

# Via GitHub Actions
# Go to: Actions → Designer Agent Workflow → Run workflow
```

### 3. Coding Agent
**Purpose:** Assist with code implementation, validation, and best practices.

**Script:** `tools/coding_agent.py`  
**Workflow:** `.github/workflows/coding_workflow.yml`  
**Trigger:** Manual or when specifications are updated

**Usage:**
```bash
# Via CLI
python tools/coding_agent.py tasks vendor_ingestion_pipeline
python tools/coding_agent.py validate
python tools/coding_agent.py check
python tools/coding_agent.py codex-task vendor_ingestion_pipeline 1

# Via GitHub Actions
# Go to: Actions → Coding Agent Workflow → Run workflow
```

### 4. Testing Agent
**Purpose:** Validate code contributions and run automated tests.

**Script:** `tools/testing_agent.py`  
**Workflow:** `.github/workflows/testing_workflow.yml`  
**Output:** `logs/tests_logs/<timestamp>.log`  
**Trigger:** Manual, on pull requests, or code changes

**Usage:**
```bash
# Via CLI
python tools/testing_agent.py run
python tools/testing_agent.py run --spec vendor_ingestion_pipeline
python tools/testing_agent.py infer vendor_ingestion_pipeline
python tools/testing_agent.py logs

# Via GitHub Actions
# Automatically runs on PRs
# Or go to: Actions → Testing Agent Workflow → Run workflow
```

### 5. Documentation Agent
**Purpose:** Generate and maintain project documentation.

**Script:** `tools/documentation_agent.py`  
**Workflow:** `.github/workflows/documentation_workflow.yml`  
**Output:** Script cards, business descriptions, glossary updates  
**Trigger:** Manual or when code/specs are finalized

**Usage:**
```bash
# Via CLI
python tools/documentation_agent.py script-card my_job_id --spec my_subsystem
python tools/documentation_agent.py business-desc my_job_id --spec my_subsystem
python tools/documentation_agent.py glossary my_subsystem
python tools/documentation_agent.py validate

# Via GitHub Actions
# Go to: Actions → Documentation Agent Workflow → Run workflow
```

## Workflow Sequence

The typical development flow using these agents:

```
1. Planner Agent
   └─> Create planning document
       └─> Review and approve

2. Designer Agent
   └─> Create specification(s)
       └─> Define objectives, I/O, tasks
           └─> Review and approve

3. Coding Agent
   └─> List tasks
       └─> Generate Codex task outlines
           └─> Implement code
               └─> Validate

4. Testing Agent
   └─> Infer test requirements
       └─> Run tests
           └─> Review results

5. Documentation Agent
   └─> Create script cards
       └─> Create business descriptions
           └─> Update glossary
               └─> Validate
```

## Directory Structure

```
docs/
├── roadmaps/              # Planning documents (Planner Agent)
├── specifications/        # Subsystem specs (Designer Agent)
├── script_cards/          # Operational docs (Documentation Agent)
├── business_job_descriptions/  # Business intent docs (Documentation Agent)
└── glossary.md           # Shared terms

logs/
└── tests_logs/           # Test execution logs (Testing Agent)

tools/
├── planner_agent.py      # Planning automation
├── designer_agent.py     # Design automation
├── coding_agent.py       # Coding assistance
├── testing_agent.py      # Testing automation
└── documentation_agent.py  # Documentation automation

.github/workflows/
├── planner_workflow.yml      # Planner Agent CI/CD
├── designer_workflow.yml     # Designer Agent CI/CD
├── coding_workflow.yml       # Coding Agent CI/CD
├── testing_workflow.yml      # Testing Agent CI/CD
└── documentation_workflow.yml  # Documentation Agent CI/CD
```

## Best Practices

1. **Start with Planning:** Always begin with the Planner Agent to define objectives clearly
2. **One Spec per Subsystem:** Keep specifications focused on single subsystems
3. **Validate Early:** Run validation after each significant change
4. **Use Automation:** Leverage GitHub Actions for consistent workflows
5. **Document as You Go:** Use Documentation Agent throughout development, not just at the end
6. **Review Test Logs:** Check `logs/tests_logs/` for detailed test results

## Troubleshooting

### Issue: Workflow fails with "file already exists"
**Solution:** Use the `--overwrite` flag or `overwrite: true` in workflow inputs

### Issue: Validation fails
**Solution:** Run `python tools/validate_repo_docs.py --all` locally to see specific errors

### Issue: Can't find specification
**Solution:** Ensure specification name doesn't include `.yaml` extension when using CLI

### Issue: Tests fail on PR
**Solution:** Check the test logs artifact in the GitHub Actions run for details

## Contributing

When adding new agents or modifying existing ones:

1. Update the corresponding Python script in `tools/`
2. Update the GitHub Actions workflow in `.github/workflows/`
3. Test locally before committing
4. Update this README with new functionality
5. Run validation: `python tools/validate_repo_docs.py --all`

## Support

For questions or issues:
1. Check the agent script's help: `python tools/<agent>.py --help`
2. Review workflow logs in GitHub Actions
3. Consult `docs/context_packs/system_context.md` for repository standards

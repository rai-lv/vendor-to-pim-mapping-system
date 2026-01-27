# GitHub Workflow Agents - Visual Overview

## Agent Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Development Lifecycle                            │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  1. PLANNING     │
│  Planner Agent   │
│  ──────────────  │
│  Manual Trigger  │
└────────┬─────────┘
         │ Creates: docs/roadmaps/<phase>.md
         ▼
┌──────────────────┐
│  2. DESIGN       │
│  Designer Agent  │
│  ──────────────  │
│  Manual/Auto     │
│  (on roadmap     │
│   updates)       │
└────────┬─────────┘
         │ Creates: docs/specifications/<subsystem>.yaml
         ▼
┌──────────────────┐
│  3. CODING       │
│  Coding Agent    │
│  ──────────────  │
│  Manual/Auto     │
│  (on spec        │
│   updates)       │
└────────┬─────────┘
         │ Validates & assists with: jobs/**/*.py
         ▼
┌──────────────────┐
│  4. TESTING      │
│  Testing Agent   │
│  ──────────────  │
│  Auto on PR      │
│  Auto on merge   │
└────────┬─────────┘
         │ Creates: logs/tests_logs/test_run_<timestamp>.log
         ▼
┌──────────────────┐
│  5. DOCUMENTATION│
│  Doc Agent       │
│  ──────────────  │
│  Manual/Auto     │
│  (on code merge) │
└────────┬─────────┘
         │ Creates: docs/script_cards/<job>.md
         │          docs/business_job_descriptions/<job>.md
         ▼
┌──────────────────┐
│   DEPLOYMENT     │
│   (Manual)       │
└──────────────────┘
```

## Agent Interactions

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Planner    │─────>│  Designer   │─────>│   Coding    │
│   Agent     │      │    Agent    │      │   Agent     │
└─────────────┘      └─────────────┘      └──────┬──────┘
                                                   │
                     ┌─────────────┐              │
                     │   Testing   │<─────────────┘
                     │    Agent    │
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │  Documentation │
                     │     Agent    │
                     └─────────────┘
```

## Trigger Matrix

| Agent         | Manual | Planning Update | Spec Update | Code Change | PR     | Merge  |
|---------------|--------|-----------------|-------------|-------------|--------|--------|
| Planner       | ✅     | -               | -           | -           | -      | -      |
| Designer      | ✅     | ✅ (notify)     | -           | -           | -      | -      |
| Coding        | ✅     | -               | ✅          | -           | -      | -      |
| Testing       | ✅     | -               | -           | -           | ✅     | ✅     |
| Documentation | ✅     | -               | -           | ✅ (notify) | -      | ✅     |

## File Flow

```
Planning Phase
  └─> docs/roadmaps/
        └─> phase_name.md

Design Phase
  └─> docs/specifications/
        └─> subsystem.yaml

Coding Phase
  └─> jobs/
        └─> <job_group>/
              └─> <job_id>/
                    ├─> glue_script.py
                    └─> job_manifest.yaml

Testing Phase
  └─> logs/tests_logs/
        └─> test_run_YYYYMMDD_HHMMSS.log

Documentation Phase
  ├─> docs/script_cards/
  │     └─> job_id.md
  └─> docs/business_job_descriptions/
        └─> job_id.md
```

## Automation Levels

### 🟢 Fully Automated
- **Testing on PR**: Runs automatically, validates changes
- **Testing on Merge**: Runs automatically, generates logs
- **Validation**: Runs on all PRs via existing workflow

### 🟡 Semi-Automated
- **Designer on Planning Update**: Notifies but doesn't create specs
- **Coding on Spec Update**: Validates but doesn't write code
- **Documentation on Merge**: Reminds but doesn't generate docs

### 🔴 Manual Only
- **Planner**: Must be manually triggered to create plans
- **All Generation**: Must manually trigger to create new artifacts

## Agent Scripts Summary

| Script                    | Lines | Features                              |
|---------------------------|-------|---------------------------------------|
| planner_agent.py          | ~200  | Create, list planning documents       |
| designer_agent.py         | ~300  | Create, list, validate specifications |
| coding_agent.py           | ~280  | Tasks, validate, check, codex-task    |
| testing_agent.py          | ~350  | Run tests, infer, logs                |
| documentation_agent.py    | ~450  | Script cards, business desc, glossary |

## Workflow Files Summary

| Workflow                     | Triggers                    | Outputs                |
|------------------------------|-----------------------------|------------------------|
| planner_workflow.yml         | workflow_dispatch           | Planning docs          |
| designer_workflow.yml        | workflow_dispatch, push     | Specifications         |
| coding_workflow.yml          | workflow_dispatch, push     | Validation results     |
| testing_workflow.yml         | workflow_dispatch, PR, push | Test logs              |
| documentation_workflow.yml   | workflow_dispatch, push     | Script cards, bus desc |

## Quality Gates

```
Every Change
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
┌────────────────┐
│  Validation    │  ✓ Standards compliance
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Best Practices│  ⚠ Check DRY, SOLID
└───────┬────────┘
        │
        ▼
    Merge OK
```

## Directory Ownership

| Directory                         | Owner Agent         | Purpose                    |
|-----------------------------------|---------------------|----------------------------|
| `docs/roadmaps/`                  | Planner             | Planning documents         |
| `docs/specifications/`            | Designer            | Design specifications      |
| `jobs/`                           | Coding (human-led)  | Job implementations        |
| `logs/tests_logs/`                | Testing             | Test execution logs        |
| `docs/script_cards/`              | Documentation       | Operational docs           |
| `docs/business_job_descriptions/` | Documentation       | Business intent docs       |
| `docs/glossary.md`                | Documentation       | Shared terminology         |

## Success Metrics

Each agent tracks:
- ✅ Documents created
- ✅ Validations passed
- ✅ Tests executed
- ✅ Standards compliance
- ⚠ Warnings identified
- ❌ Errors found

## Integration with Existing System

The agents integrate with existing repository infrastructure:

1. **Standards Validation**: Uses existing `validate_repo_docs.py`
2. **CI/CD**: Extends existing GitHub Actions setup
3. **Documentation Structure**: Follows existing specs
4. **Job Structure**: Works with existing `jobs/` layout

## Next Steps

After setup:
1. Create first planning document
2. Generate specifications from plans
3. Implement code following specs
4. Run tests continuously
5. Maintain documentation

All agents ready to use! 🚀

# Roadmaps Directory

## Purpose

This directory contains **planning artifacts** from Steps 1 and 2 of the 5-step workflow:

- **Objective Definitions (Step 1):** High-level statements of intent for what the system aims to achieve
- **Pipeline Plans (Step 2):** Breakdown of objectives into ordered capabilities with dependencies

## Document Types

### Objective Definitions

**Naming pattern:** `<objective_name>.md` (avoid `_pipeline_plan` suffix)

**Required sections:**
- Objective Statement
- Expected Outcomes  
- Out-of-Scope
- Success Criteria

**Reference:** `docs/context/documentation_system_catalog.md` entry #22

### Pipeline Plans

**Naming pattern:** `<objective_name>_pipeline_plan.md`

**Required sections:**
- Processing Sequence
- Conceptual Artifacts (or Artifacts section)
- Capability identification and ordering
- Dependencies between capabilities

**Reference:** `docs/context/documentation_system_catalog.md` entry #23

## Validation

Planning artifacts in this directory are validated by:
- CI workflow: `.github/workflows/pr_validation.yml` (job: `planning_validation`)
- Manual review against workflow guide: `docs/process/workflow_guide.md`

## Related Documentation

- **Documentation System Catalog:** `docs/context/documentation_system_catalog.md`
- **Workflow Guide:** `docs/process/workflow_guide.md` (Steps 1-2)
- **Contribution Guide:** `docs/process/contribution_approval_guide.md`

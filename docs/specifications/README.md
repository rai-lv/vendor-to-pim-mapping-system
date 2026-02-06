# Specifications Directory

## Purpose

This directory contains **capability specification documents** from Step 3 of the 5-step workflow.

Capability specifications define individual capabilities with acceptance criteria and codable task breakdowns. They provide approved, bounded specifications for implementation and enable traceability from capability to tasks to code.

## Document Types

### Capability Specifications (Step 3 Planning Artifacts)

**Naming pattern:** `<capability_name>_capability.yaml` or `<capability_name>_capability.md`

**Required elements:**
- Capability boundary statement (what it does and does NOT do)
- Acceptance criteria (evaluable)
- Codable task breakdown following `docs/standards/codable_task_spec.md`:
  - Task identity (identifier and parent capability reference)
  - Task purpose
  - Task boundaries
  - Dependencies
  - Intended outputs
  - Acceptance criteria
  - Unknowns/assumptions (if present)

**Reference:** `docs/context/documentation_system_catalog.md` entry #24

## Storage Alternatives

According to `docs/process/workflow_guide.md`, capability plans can be stored in one of three locations:

1. **This directory (`docs/specifications/`)** — For detailed or multi-capability planning
2. **GitHub Issues** — For ongoing work tracked in issue form  
3. **PR descriptions** — For smaller capabilities implemented in a single PR

This directory is the canonical location for capability specifications that need to be stored in-repository.

## Validation

Capability specifications in this directory are validated by:
- CI workflow: `.github/workflows/pr_validation.yml` (job: `planning_validation`)
- YAML structure validation for `*_capability.yaml` files
- Manual review against workflow guide: `docs/process/workflow_guide.md`

## YAML Format for Capability Specifications

For `*_capability.yaml` files, the following fields are required:

```yaml
objective: "Reference to parent objective/pipeline plan"
inputs: ["List of inputs required"]
outputs: ["List of outputs produced"]
acceptance_criteria:
  - "Evaluable criterion 1"
  - "Evaluable criterion 2"
```

Additional recommended fields: `boundary`, `tasks`, `assumptions`, `dependencies`

## Related Documentation

- **Documentation System Catalog:** `docs/context/documentation_system_catalog.md`
- **Workflow Guide:** `docs/process/workflow_guide.md` (Step 3)
- **Codable Task Spec:** `docs/standards/codable_task_spec.md`
- **Contribution Guide:** `docs/process/contribution_approval_guide.md`

# Specifications

This directory contains capability specifications created during **Step 2b** of the 5-step development workflow.

## Purpose

Specifications define individual capabilities from the pipeline plan in detail. Each specification breaks down ONE capability/step into actionable implementation requirements with testable criteria.

## When to Create Specifications

Specifications are created during **Step 2b: Capability Plan** after:
1. Step 1 objective definition is approved
2. Step 2a pipeline plan is approved
3. A specific capability from the pipeline plan needs detailed specification

## Specification Structure

Each specification is a YAML file with the following structure:

```yaml
subsystem_name: "Name of the subsystem"
version: "1.0.0"
created_date: "YYYY-MM-DD"
status: "draft|approved|implemented"
planning_phase: "Reference to planning document"

objective:
  description: "What this subsystem achieves"
  business_value: "Business value delivered"
  success_criteria:
    - "Measurable success criteria"

constraints:
  technical:
    - "Technical constraints"
  business:
    - "Business constraints"
  dependencies:
    - "Dependencies on other systems"

inputs:
  - name: "Input name"
    type: "Data type"
    source: "S3 location or system"
    required: true/false
    schema_reference: "Schema definition"

outputs:
  - name: "Output name"
    type: "Data type"
    destination: "S3 location or system"
    purpose: "What this output is used for"
    schema_reference: "Schema definition"

processing_logic:
  high_level_steps:
    - "Step 1"
    - "Step 2"
  business_rules:
    - "Business rules"
  error_handling: "Error handling strategy"

coding_tasks:
  - task_id: 1
    description: "Specific coding task"
    files_affected:
      - "files to create/modify"
    acceptance_criteria:
      - "Acceptance criteria"
    estimated_complexity: "low|medium|high"
    dependencies: []

testing_requirements:
  unit_tests:
    - "Unit test requirements"
  integration_tests:
    - "Integration test requirements"
  test_data: "Test data requirements"

documentation_requirements:
  - "Documentation to create/update"

notes: "Additional context"
```

## Creating a Specification

### Via CLI:
```bash
# Create capability specification (requires approved Step 2a pipeline plan)
python tools/capability_planner_agent.py create "capability_name" \
  --pipeline-ref "objective_name_pipeline_plan.md"

# Output: docs/specifications/capability_name_capability.yaml
```

### Via GitHub Actions:
1. Go to: Actions → Capability Planner Agent Workflow → Run workflow
2. Enter capability name and pipeline plan reference
3. Click "Run workflow"

## Listing Specifications

```bash
# List all capability specifications
python tools/capability_planner_agent.py list
```

## Validating a Specification

```bash
python tools/capability_planner_agent.py validate docs/specifications/capability_name_capability.yaml
```

## Workflow

1. **Create**: Generate specification from pipeline plan (Step 2a)
2. **Fill**: Complete all sections with detailed requirements
3. **Review**: Validate structure, content, and alignment with pipeline plan
4. **Approve**: Get stakeholder consensus; change status to "approved"
5. **Decompose**: Use Coding Agent to break into development elements (Step 3)
6. **Implement**: Execute via Steps 4-5 of the workflow
7. **Complete**: Update status to "implemented"

## Workflow Integration

Capability specifications are part of the **5-step development workflow**:

```
Step 2a: Pipeline Plan (approved)
   ↓
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
   ↓
Step 4: Create Codex Tasks (Coding Agent)
   ↓
Step 5: Code Creation (PR process)
```

**See:** `docs/workflows/WORKFLOW_5_STEPS.md` for complete workflow details

## Best Practices

- Focus each specification on ONE capability from the pipeline plan
- Define inputs/outputs by **meaning**, not storage details (S3 paths come later)
- State explicit boundaries: what this capability does and does NOT do
- Break down into small, testable tasks suitable for individual PRs
- Link to pipeline plan for context and upstream/downstream dependencies
- Update status as work progresses through the workflow
- Reference specifications in job manifests and documentation

## Key Principles

1. **One Capability per Specification:** Each specification covers exactly one pipeline step
2. **Define by Meaning:** Inputs/outputs described conceptually, not by S3 location/format
3. **Explicit Boundaries:** Clearly state what IS and is NOT included
4. **Testable Criteria:** All acceptance criteria must be objectively verifiable
5. **Evidence-Based:** Reference existing jobs and capabilities; mark gaps explicitly

## Status Values

- **draft**: Initial creation, needs review and completion
- **approved**: Reviewed, complete, and ready for decomposition (Step 3)
- **implemented**: All coding tasks completed and deployed
- **deprecated**: No longer in use

## Related Documentation

- **Complete Workflow:** `docs/workflows/WORKFLOW_5_STEPS.md`
- **Agent System:** `docs/context_packs/agent_system_context.md`
- **Agent Setup:** `docs/workflows/AGENTS_SETUP.md`
- **Pipeline Plans:** `docs/roadmaps/` (Step 2a outputs)
- **Repository Context:** `docs/context_packs/system_context.md`

# Specifications

This directory contains subsystem specifications created by the Designer Agent. Each specification breaks down a high-level plan into actionable coding tasks.

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
python tools/designer_agent.py create "subsystem_name" --planning-phase "Q1 2026"
```

### Via GitHub Actions:
1. Go to: Actions → Designer Agent Workflow → Run workflow
2. Enter subsystem name and optional planning phase
3. Click "Run workflow"

## Listing Specifications

```bash
python tools/designer_agent.py list
```

## Validating a Specification

```bash
python tools/designer_agent.py validate docs/specifications/subsystem_name.yaml
```

## Workflow

1. **Create**: Generate specification from planning document
2. **Fill**: Complete all TODO sections
3. **Review**: Validate structure and content
4. **Approve**: Change status to "approved"
5. **Implement**: Use Coding Agent to break down into tasks
6. **Complete**: Update status to "implemented"

## Best Practices

- Keep specifications focused on single subsystems
- Define clear input/output contracts
- Break down into small, testable tasks
- Link to planning documents for context
- Update status as work progresses
- Reference specifications in job manifests and documentation

## Status Values

- **draft**: Initial creation, needs review
- **approved**: Reviewed and ready for implementation
- **implemented**: All coding tasks completed
- **deprecated**: No longer in use

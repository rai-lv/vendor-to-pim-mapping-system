# Agent Tools Reference — Technical Specifications and CLI Usage

## Overview

This document provides detailed technical specifications, command-line interface documentation, and troubleshooting guidance for agent tools used in the AI-assisted development workflow.

**For high-level governance and workflow integration**, see `docs/context_packs/agent_system_context.md`.  
**For example templates and step-by-step guides**, see `docs/workflows/agent_workflow_templates.md`.

---

## Tool Inventory

| Tool | Location | Workflow Step | Purpose |
|------|----------|---------------|---------|
| Planner Agent | `tools/planner_agent.py` | Step 1 | Define business objectives |
| Pipeline Planner Agent | `tools/pipeline_planner_agent.py` | Step 2a | Design end-to-end pipeline architecture |
| Capability Planner Agent | `tools/capability_planner_agent.py` | Step 2b | Break down into technical specifications |
| Coding Agent | `tools/coding_agent.py` | Steps 3-4 | Decompose and create Codex tasks |
| Testing Agent | `tools/testing_agent.py` | Step 6 | Validate code changes |
| Documentation Agent | `tools/documentation_agent.py` | Step 6 | Update documentation |

---

## Prerequisites

### System Requirements

- Python 3.9+
- AWS CLI configured with appropriate permissions
- Access to repository standards in `docs/standards/`
- Repository validation tool: `tools/validate_repo_docs.py`

### Environment Setup

```bash
# Install required dependencies
pip install -r requirements.txt

# Verify agent tools are accessible
python tools/planner_agent.py --version
python tools/pipeline_planner_agent.py --version
python tools/capability_planner_agent.py --version
```

### Validation Setup

Before using any agent tool, ensure repository validation is configured per `docs/standards/validation_standard.md`:

```bash
# Run full repository validation
python tools/validate_repo_docs.py --all

# Expected output: All checks pass
```

---

## Planner Agent (Step 1)

### Purpose

Assists in creating structured objective definitions with explicit boundaries, success criteria, and risk assessment.

### Command Syntax

```bash
python tools/planner_agent.py <command> [options]
```

### Commands

#### `create` - Create New Objective

Creates a new objective definition document.

**Syntax:**
```bash
python tools/planner_agent.py create "<objective_name>" \
  --description "<brief_description>" \
  [--output <path>] \
  [--template <template_name>]
```

**Parameters:**
- `objective_name` (required): Short, hyphenated name for the objective
- `--description` (required): Brief description of what must be achieved
- `--output` (optional): Custom output path (default: `docs/roadmaps/<objective_name>.md`)
- `--template` (optional): Template name for specific objective types (default: `standard`)

**Example:**
```bash
python tools/planner_agent.py create "vendor_onboarding" \
  --description "Implement automated vendor onboarding pipeline"
```

**Output:**
```
✓ Created objective definition: docs/roadmaps/vendor_onboarding.md
→ Next step: Review with stakeholders and iterate based on feedback
→ Approval required before proceeding to Step 2a
```

#### `validate` - Validate Objective Definition

Validates an existing objective definition against standards.

**Syntax:**
```bash
python tools/planner_agent.py validate <objective_file>
```

**Example:**
```bash
python tools/planner_agent.py validate docs/roadmaps/vendor_onboarding.md
```

**Output:**
```
Validating: docs/roadmaps/vendor_onboarding.md
✓ Objective statement present
✓ Expected outcomes defined
✓ Out-of-scope boundaries documented
✓ Success criteria testable
⚠ Warning: 3 unknowns marked as TBD (resolve before approval)
→ Status: READY FOR REVIEW (3 warnings)
```

#### `status` - Check Objective Status

Checks the approval status and readiness of an objective.

**Syntax:**
```bash
python tools/planner_agent.py status <objective_file>
```

### Output Format

Creates a markdown file at `docs/roadmaps/<objective_name>.md` with the following structure:

```markdown
# Objective: <Name>

## Objective Statement
[Clear description of what must be achieved]

## Expected Outcomes
- [Specific, measurable result 1]
- [Specific, measurable result 2]

## Out-of-Scope
- [Explicit boundary 1]
- [Explicit boundary 2]

## Success Criteria
### Functional Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

### Quality Criteria
- [ ] [Quality metric 1]
- [ ] [Quality metric 2]

## Constraints
### Technical
- [Constraint 1]

### Business
- [Deadline/budget constraint]

## Risk Assessment
### Known Risks
- [Risk + mitigation]

### Unknowns
- TBD: [Unknown requiring investigation]
- OPEN QUESTION: [Decision point]

## Dependencies
- [External dependency 1]
```

### Troubleshooting

**Problem:** `Error: Objective name contains invalid characters`

**Solution:** Use only lowercase letters, numbers, and hyphens. No spaces or special characters.
```bash
# ✗ Invalid
python tools/planner_agent.py create "Vendor Onboarding"

# ✓ Valid
python tools/planner_agent.py create "vendor_onboarding"
```

**Problem:** `Warning: Output file already exists`

**Solution:** Use `--force` flag to overwrite or choose a different name.
```bash
python tools/planner_agent.py create "vendor_onboarding" --force
```

**Problem:** `Validation failed: Missing success criteria`

**Solution:** Add both functional and quality success criteria sections to the document.

---

## Pipeline Planner Agent (Step 2a)

### Purpose

Assists in designing end-to-end pipeline architecture showing processing sequence, decision points, and conceptual artifacts.

### Command Syntax

```bash
python tools/pipeline_planner_agent.py <command> [options]
```

### Commands

#### `create` - Create Pipeline Plan

Creates a pipeline plan from an approved objective.

**Syntax:**
```bash
python tools/pipeline_planner_agent.py create \
  --objective <objective_file> \
  [--output <path>]
```

**Parameters:**
- `--objective` (required): Path to approved objective definition
- `--output` (optional): Custom output path (default: `docs/roadmaps/<objective>_pipeline_plan.md`)

**Example:**
```bash
python tools/pipeline_planner_agent.py create \
  --objective docs/roadmaps/vendor_onboarding.md
```

**Output:**
```
✓ Analyzed objective: vendor_onboarding
✓ Created pipeline plan: docs/roadmaps/vendor_onboarding_pipeline_plan.md
→ Next step: Review architecture with technical lead
→ Approval required before proceeding to Step 2b
```

#### `validate` - Validate Pipeline Plan

Validates pipeline plan structure and completeness.

**Syntax:**
```bash
python tools/pipeline_planner_agent.py validate <pipeline_file>
```

#### `analyze` - Analyze Complexity

Analyzes pipeline complexity and provides recommendations.

**Syntax:**
```bash
python tools/pipeline_planner_agent.py analyze <pipeline_file>
```

**Example Output:**
```
Pipeline Complexity Analysis:
- Processing steps: 8
- Decision points: 3
- Conceptual artifacts: 12
- Estimated Glue jobs: 5-7
⚠ Recommendation: Consider breaking into 2 capabilities for Steps 3-5
```

### Output Format

Creates a markdown file at `docs/roadmaps/<objective>_pipeline_plan.md`:

```markdown
# Pipeline Plan: <Objective>

## Processing Sequence
1. [Conceptual Step 1]
2. [Conceptual Step 2]
3. [Decision Point] → Branch A / Branch B

## Detailed Step Descriptions
### Step 1: [Name]
- **Inputs:** [Data sources]
- **Processing:** [What happens]
- **Outputs:** [Artifacts produced]

## Conceptual Artifacts
- [Artifact 1]: [Purpose and format]

## Decision Points
- [Point 1]: [Criteria for branching]

## Existing Job Mapping
- Step 1 → Potentially maps to `jobs/group/existing_job`

## Unknowns and Open Decisions
- TBD: [Technical decision needed]
```

### Troubleshooting

**Problem:** `Error: Objective not approved`

**Solution:** Ensure the objective definition has approval markers before creating pipeline plan.

**Problem:** `Warning: Pipeline complexity high (>10 steps)`

**Solution:** Consider breaking objective into multiple capabilities.

---

## Capability Planner Agent (Step 2b)

### Purpose

Assists in breaking down pipeline steps into detailed technical capability specifications ready for implementation.

### Command Syntax

```bash
python tools/capability_planner_agent.py <command> [options]
```

### Commands

#### `create` - Create Capability Specification

Creates a detailed capability specification from pipeline plan.

**Syntax:**
```bash
python tools/capability_planner_agent.py create \
  --pipeline <pipeline_file> \
  --capability-name "<name>" \
  [--steps <step_numbers>] \
  [--output <path>]
```

**Parameters:**
- `--pipeline` (required): Path to approved pipeline plan
- `--capability-name` (required): Short name for this capability
- `--steps` (optional): Which pipeline steps this capability covers (e.g., "1-3,5")
- `--output` (optional): Custom output path (default: `docs/specifications/<capability>.yaml`)

**Example:**
```bash
python tools/capability_planner_agent.py create \
  --pipeline docs/roadmaps/vendor_onboarding_pipeline_plan.md \
  --capability-name "vendor_data_validation" \
  --steps "2-4"
```

**Output:**
```
✓ Analyzed pipeline: vendor_onboarding_pipeline_plan.md
✓ Extracted steps: 2-4
✓ Created specification: docs/specifications/vendor_data_validation.yaml
→ Next step: Review with technical lead
→ Approval required before proceeding to Step 3
```

#### `validate` - Validate Capability Spec

Validates capability specification against standards.

**Syntax:**
```bash
python tools/capability_planner_agent.py validate <spec_file>
```

**Validation Checks:**
- Format compliance with `docs/standards/` specifications
- Input/output specifications complete
- Processing requirements defined
- Success criteria testable
- Assumptions explicitly labeled
- Dependencies documented

### Output Format

Creates a YAML file at `docs/specifications/<capability>.yaml`:

```yaml
capability_name: vendor_data_validation
objective: |
  Validate vendor-submitted product data against PIM schema requirements
  
scope:
  includes:
    - Schema validation for product attributes
    - Data type checking and normalization
    - Business rule validation
  excludes:
    - Data enrichment (handled by separate capability)
    - Historical data migration
    
inputs:
  - name: vendor_submission_file
    type: S3 Object
    format: CSV/Excel/JSON
    location: s3://bucket/vendor-submissions/
    
outputs:
  - name: validated_products
    type: S3 Object
    format: Parquet
    location: s3://bucket/validated/
    
  - name: validation_errors
    type: S3 Object
    format: JSON
    location: s3://bucket/errors/
    
processing_requirements:
  - Validate against PIM schema version 2.1
  - Apply business rules per vendor contract
  - Generate detailed error reports
  
parameters:
  - name: vendor_id
    type: string
    required: true
    description: Unique vendor identifier
    
success_criteria:
  functional:
    - All valid records pass validation
    - Invalid records logged with specific error codes
    - 100% of submissions processed
  quality:
    - Processing completes within 30-minute SLA
    - Zero data loss during validation
    - Error messages actionable by vendors
    
dependencies:
  - PIM schema definitions (S3)
  - Vendor contract rules database
  
assumptions:
  - ASSUMPTION: Vendor files <5GB (requires approval)
  - ASSUMPTION: Max 100K products per submission (requires approval)
```

### Troubleshooting

**Problem:** `Error: Pipeline plan not approved`

**Solution:** Ensure pipeline plan has approval before creating capability specifications.

**Problem:** `Warning: Assumptions detected without approval markers`

**Solution:** Add "(requires approval)" or "(approved: YYYY-MM-DD)" to all assumption statements.

**Problem:** `Validation error: Missing success criteria`

**Solution:** Add both functional and quality success criteria to the specification.

---

## Coding Agent (Steps 3-4)

### Purpose

Assists in decomposing capability specifications into development elements and creating Codex tasks.

### Command Syntax

```bash
python tools/coding_agent.py <command> [options]
```

### Commands

#### `decompose` - Decompose Capability (Step 3)

Analyzes capability spec and proposes development element decomposition.

**Syntax:**
```bash
python tools/coding_agent.py decompose \
  --capability <spec_file> \
  [--output <path>]
```

**Example:**
```bash
python tools/coding_agent.py decompose \
  --capability docs/specifications/vendor_data_validation.yaml
```

**Output:**
```
✓ Analyzed capability: vendor_data_validation
✓ Proposed decomposition:
  1. Schema validation module (150 LOC estimated)
  2. Business rules engine (200 LOC estimated)
  3. Error reporting module (100 LOC estimated)
  4. Integration tests (50 LOC estimated)
→ Review decomposition before proceeding to Step 4
```

#### `create-tasks` - Create Codex Tasks (Step 4)

Creates Codex task definitions from approved decomposition.

**Syntax:**
```bash
python tools/coding_agent.py create-tasks \
  --capability <spec_file> \
  --decomposition <decomp_file> \
  [--output-dir <path>]
```

**Example:**
```bash
python tools/coding_agent.py create-tasks \
  --capability docs/specifications/vendor_data_validation.yaml \
  --decomposition vendor_data_validation_decomposition.md \
  --output-dir docs/codex-tasks/
```

**Output:**
```
✓ Created 4 Codex tasks:
  - docs/codex-tasks/schema_validation_001.md
  - docs/codex-tasks/business_rules_002.md
  - docs/codex-tasks/error_reporting_003.md
  - docs/codex-tasks/integration_tests_004.md
→ Review tasks before assigning to implementation
```

### Codex Task Format

Each task is created as a markdown file following the repository standard:

```markdown
# Codex Task: [Task Name]

## Objective
[What this task accomplishes]

## Standards References
- See `docs/standards/script_card_spec.md` for documentation requirements
- See `docs/standards/job_manifest_spec.md` for manifest format

## Target Script/Path (Explicit)
`jobs/vendor_processing/schema_validation/glue_script.py`

## File Restrictions (Explicit)
**Allowed to modify:**
- `jobs/vendor_processing/schema_validation/*`

**NOT allowed to modify:**
- Any files outside target directory

## Implementation Requirements
1. [Requirement 1]
2. [Requirement 2]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Quality Gates (Must Pass)
- Run validation per `docs/standards/validation_standard.md`
- All tests pass
- Documentation updated

## Boundaries (What This Element Does NOT Do)
- Does not handle [out-of-scope item]
```

### Troubleshooting

**Problem:** `Error: Capability spec not approved`

**Solution:** Ensure capability has approval markers before decomposition.

**Problem:** `Warning: Decomposition produces >10 tasks`

**Solution:** Consider breaking capability into smaller capabilities or consolidating related tasks.

**Problem:** `Error: Task file restrictions conflict`

**Solution:** Review file restrictions to ensure no overlapping modification permissions between tasks.

---

## Testing Agent (Step 6)

### Purpose

Assists in validating code changes meet acceptance criteria and quality standards.

### Command Syntax

```bash
python tools/testing_agent.py <command> [options]
```

### Commands

#### `validate` - Run Validation

Runs repository validation per `docs/standards/validation_standard.md`.

**Syntax:**
```bash
python tools/testing_agent.py validate \
  [--scope <all|changed|specific>] \
  [--path <path>]
```

**Example:**
```bash
# Validate all documentation
python tools/testing_agent.py validate --scope all

# Validate only changed files
python tools/testing_agent.py validate --scope changed

# Validate specific path
python tools/testing_agent.py validate --scope specific --path docs/specifications/
```

#### `test` - Run Tests

Executes test suite for code changes.

**Syntax:**
```bash
python tools/testing_agent.py test \
  --job <job_path> \
  [--coverage]
```

**Example:**
```bash
python tools/testing_agent.py test \
  --job jobs/vendor_processing/schema_validation/ \
  --coverage
```

### Troubleshooting

**Problem:** `Validation failed: Standards not met`

**Solution:** Review validation output and address each failing check. See `docs/standards/validation_standard.md` for requirements.

**Problem:** `Test execution failed`

**Solution:** Check test logs in `test_output/` directory for detailed error messages.

---

## Documentation Agent (Step 6)

### Purpose

Assists in updating documentation to reflect code changes.

### Command Syntax

```bash
python tools/documentation_agent.py <command> [options]
```

### Commands

#### `generate` - Generate Documentation

Proposes documentation updates based on code changes.

**Syntax:**
```bash
python tools/documentation_agent.py generate \
  --job <job_path> \
  [--types <card|description|manifest>]
```

**Example:**
```bash
python tools/documentation_agent.py generate \
  --job jobs/vendor_processing/schema_validation/ \
  --types card,description
```

**Output:**
```
✓ Analyzed job: schema_validation
✓ Proposed updates:
  - Script card: jobs/vendor_processing/schema_validation/script_card.md
  - Business description: docs/business_job_descriptions/schema_validation.md
→ Review proposed changes before committing
```

#### `validate` - Validate Documentation

Validates documentation compliance with standards.

**Syntax:**
```bash
python tools/documentation_agent.py validate \
  --job <job_path>
```

### Troubleshooting

**Problem:** `Error: Documentation template not found`

**Solution:** Ensure `docs/standards/script_card_spec.md` and `docs/standards/business_job_description_spec.md` exist and are accessible.

**Problem:** `Warning: Documentation out of sync with code`

**Solution:** Run `generate` command to propose updates, then review and commit.

---

## Common Issues and Solutions

### Installation Issues

**Problem:** `ModuleNotFoundError: No module named 'package_name'`

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Permission Issues

**Problem:** `Error: Unable to write to docs/ directory`

**Solution:** Check file permissions and ensure you have write access to the repository.

### Validation Issues

**Problem:** `Multiple validation errors across repository`

**Solution:** Run validation with verbose output to see all issues:
```bash
python tools/validate_repo_docs.py --all --verbose
```

Then address each issue systematically.

### Agent Tool Version Mismatches

**Problem:** `Error: Agent tool version incompatible`

**Solution:** Update all agent tools to latest versions:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## Best Practices

### Before Running Any Agent Tool

1. **Pull latest changes**: `git pull origin main`
2. **Run validation**: `python tools/validate_repo_docs.py --all`
3. **Review standards**: Check `docs/standards/` for any updates
4. **Review governance**: See `docs/context_packs/agent_system_context.md` for approval requirements

### During Agent Tool Usage

1. **Validate frequently**: Run validation after each significant change
2. **Review outputs**: Carefully examine all agent-generated content
3. **Document issues**: Note any errors or unexpected behavior
4. **Use version control**: Commit incremental changes for easy rollback

### After Agent Tool Usage

1. **Run validation**: Ensure all standards are met with `python tools/validate_repo_docs.py --all`
2. **Test outputs**: Verify generated files match expected format
3. **Commit with context**: Include clear commit messages describing changes
4. **Update documentation**: Keep related documentation in sync

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial extraction from agent_system_context.md - detailed technical specifications |

---

## See Also

- `docs/context_packs/agent_system_context.md` - High-level governance and workflow integration
- `docs/workflows/agent_workflow_templates.md` - Example templates and step-by-step guides
- `docs/standards/validation_standard.md` - Validation procedures and requirements
- `docs/standards/` - All repository standards and specifications


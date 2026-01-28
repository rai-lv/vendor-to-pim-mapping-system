# Agent Workflow Templates — Example Templates and Step-by-Step Guides

## Overview

This document provides example templates, step-by-step workflow guides, and best practices for using agents in the development workflow. These templates demonstrate expected output formats and help ensure consistency across agent-assisted development activities.

**For high-level governance and workflow integration**, see `docs/context_packs/agent_system_context.md`.  
**For detailed CLI commands and troubleshooting**, see `docs/workflows/agent_tools_reference.md`.

---

## Template Catalog

| Template | Workflow Step | Purpose | Location in This Doc |
|----------|---------------|---------|----------------------|
| Objective Definition | Step 1 | Define business objectives | [Section 1](#step-1-objective-definition-template) |
| Pipeline Plan | Step 2a | Document pipeline architecture | [Section 2](#step-2a-pipeline-plan-template) |
| Capability Specification | Step 2b | Detail technical specifications | [Section 3](#step-2b-capability-specification-template) |
| Codex Task Definition | Step 4 | Create implementation tasks | [Section 4](#step-4-codex-task-template) |

---

## Step 1: Objective Definition Template

### Template Overview

**Purpose:** Document business objectives with clear boundaries, testable criteria, and risk assessment.  
**Output Location:** `docs/roadmaps/<objective>.md`  
**Approval Required:** Yes - explicit stakeholder approval before Step 2a

### Template Structure

```markdown
# Objective: [Objective Name]

## Objective Statement

[1-2 paragraphs clearly describing what must be achieved. Focus on business value and measurable outcomes.]

Example:
"Implement an automated pipeline for onboarding new vendors into the PIM system. The pipeline must process vendor-submitted product data, validate against PIM schema requirements, and create PIM records within 24 hours of submission. This objective aims to reduce manual data entry time by 80% and improve data accuracy to 99%."

## Expected Outcomes

- [Specific, measurable outcome 1 - what will exist when this is done]
- [Specific, measurable outcome 2 - what capability will be available]
- [Specific, measurable outcome 3 - what problem will be solved]

Example:
- Vendors can submit product data via standardized CSV/Excel/JSON formats
- System automatically validates and normalizes vendor data per PIM schema v2.1
- Approved vendor products appear in PIM within 24 hours with 99% data accuracy
- Manual data entry workload reduced from 40 hours/week to <8 hours/week

## Out-of-Scope

[Explicit list of what is NOT included in this objective. Critical for preventing scope creep.]

- [Out-of-scope item 1 - and why it's excluded]
- [Out-of-scope item 2 - reference to separate initiative if applicable]
- [Out-of-scope item 3]

Example:
- Manual vendor data entry (remains as backup process for edge cases)
- Historical vendor data migration (separate Q3 2026 initiative)
- Vendor payment processing (handled by existing finance system)
- Real-time product updates (<24 hour SLA; future enhancement)

## Success Criteria

### Functional Criteria

- [ ] [Testable criterion 1 - can be verified with yes/no]
- [ ] [Testable criterion 2 - specific feature or capability]
- [ ] [Testable criterion 3 - integration or workflow completion]

Example:
- [ ] Pipeline processes vendor submission files end-to-end without manual intervention
- [ ] Data validation rules reject invalid submissions with clear, actionable error messages
- [ ] Successfully processed submissions create PIM records that match vendor source data
- [ ] Error handling provides vendor-friendly diagnostics for failed submissions

### Quality Criteria

- [ ] [Performance metric with specific target]
- [ ] [Reliability metric with specific target]
- [ ] [Data quality metric with specific target]

Example:
- [ ] Pipeline completes processing within 2-hour SLA for standard submissions (<5GB)
- [ ] 99% data accuracy for automated field mappings (measured via spot checks)
- [ ] Zero data loss during processing (100% of submitted records accounted for)
- [ ] <1% false positive rejection rate on valid vendor submissions

## Constraints

### Technical Constraints

- [Infrastructure or technology limitation 1]
- [API or system limitation 2]
- [Data or performance limitation 3]

Example:
- Must integrate with existing PIM API v2.1 (no schema modifications allowed)
- S3 storage limit: 100GB per vendor submission (AWS account quota)
- AWS Glue 2.0 runtime environment (Glue 3.0 migration planned Q3 2026)
- Processing must use existing AWS Glue job framework

### Business Constraints

- [Timeline or deadline constraint]
- [Budget or resource constraint]
- [Stakeholder or approval constraint]

Example:
- Go-live target: End of Q2 2026 (June 30, 2026)
- Support for 3 vendor formats initially: Excel (.xlsx), CSV, JSON
- Budget: $15K infrastructure costs (S3, Glue compute)
- Must not disrupt existing manual entry process during rollout

### Process Constraints

- [Workflow or approval requirement]
- [Compliance or regulatory requirement]
- [Testing or validation requirement]

Example:
- Requires approval from Data Governance team for PIM schema mappings
- Must pass security review before production deployment
- Requires 2-week pilot with 3 test vendors before full rollout

## Risk Assessment

### Known Risks

- [Risk 1: Description] → **Mitigation:** [How we'll address it]
- [Risk 2: Description] → **Mitigation:** [How we'll address it]

Example:
- **Risk:** Vendor data quality varies significantly across vendors → **Mitigation:** Implement robust validation layer with configurable rules per vendor contract
- **Risk:** PIM API rate limits (100 req/min) may impact throughput → **Mitigation:** Implement batch processing with queue management and retry logic
- **Risk:** Vendor formats may evolve over time → **Mitigation:** Design modular parser layer allowing format updates without pipeline changes

### Unknowns

[List items that need investigation or clarification before full planning]

- **TBD:** [Unknown that requires research or data gathering]
- **OPEN QUESTION:** [Decision point requiring stakeholder input]

Example:
- **TBD:** Average vendor submission file size (need 1-month baseline data)
- **TBD:** Expected vendor submission frequency (daily vs weekly vs ad-hoc)
- **OPEN QUESTION:** Should we support real-time processing or batch-only? (impacts architecture)
- **OPEN QUESTION:** Who owns vendor format specification documentation? (Business vs IT)

## Dependencies

### External Dependencies

- [System or API dependency]
- [Team or resource dependency]
- [Data or documentation dependency]

Example:
- PIM API access and documentation (Owner: PIM team)
- S3 bucket provisioning and permissions (Owner: DevOps team)
- Vendor format specifications (Owner: Business team)
- AWS Glue job deployment pipeline (Owner: Data Engineering team)

### Prerequisites

- [Work that must be completed first]
- [Access or permissions that must be granted]

Example:
- AWS account access for development and testing environments
- PIM API sandbox access for integration testing
- Sample vendor data files for validation testing (minimum 3 vendors)

## Approval Status

**Status:** [DRAFT | REVIEW | APPROVED]  
**Approved By:** [Name, Role, Date]  
**Approval Date:** [YYYY-MM-DD]  
**Next Review Date:** [YYYY-MM-DD]

---

**Signed:**
- Product Owner: _________________ Date: _______
- Technical Lead: _________________ Date: _______
- Business Stakeholder: _________________ Date: _______
```

### Step 1 Workflow Guide

1. **Initial Draft (Day 1)**
   - Run: `python tools/planner_agent.py create "objective_name" --description "brief description"`
   - Agent generates initial template at `docs/roadmaps/<objective>.md`
   - Review generated content for completeness

2. **Stakeholder Discussion (Days 2-3)**
   - Schedule meeting with Product Owner, Tech Lead, Business Stakeholders
   - Walk through each section of the objective definition
   - Capture feedback and open questions
   - Iterate on document based on discussion

3. **Risk and Constraint Review (Days 3-4)**
   - Technical review: Identify technical constraints and risks
   - Business review: Confirm deadlines, budget, resources
   - Document all unknowns that need resolution

4. **Success Criteria Definition (Days 4-5)**
   - Define specific, testable functional criteria
   - Set measurable quality targets with stakeholders
   - Ensure criteria align with business objectives

5. **Final Approval (Day 5-7)**
   - Circulate final draft for stakeholder review
   - Address any final comments or concerns
   - Collect explicit approvals (signatures or email confirmations)
   - Mark document status as APPROVED
   - Archive in `docs/roadmaps/` as authoritative reference

6. **Validation Before Next Step**
   - Run: `python tools/planner_agent.py validate docs/roadmaps/<objective>.md`
   - Ensure all sections complete and no unresolved TBDs
   - Proceed to Step 2a only after approval

---

## Step 2a: Pipeline Plan Template

### Template Overview

**Purpose:** Document end-to-end pipeline architecture showing processing flow, decision points, and artifacts.  
**Output Location:** `docs/roadmaps/<objective>_pipeline_plan.md`  
**Approval Required:** Yes - technical lead and architect approval before Step 2b

### Template Structure

```markdown
# Pipeline Plan: [Objective Name]

## Processing Sequence

[High-level numbered list of conceptual processing steps. Focus on WHAT happens, not HOW.]

1. [Step 1: Verb + Noun - e.g., "Ingest vendor submission files"]
2. [Step 2: Processing action]
3. [Decision Point] → Branch A / Branch B
4. [Step 4: Output generation]

Example:
1. Ingest vendor submission files from S3 landing zone
2. Parse and normalize vendor data to common schema
3. Validate data against PIM schema and business rules
4. [DECISION] Valid data → Continue to Step 5 | Invalid data → Generate error report
5. Transform validated data to PIM format
6. Load data into PIM via API
7. Generate processing summary and success confirmation

## Detailed Step Descriptions

### Step 1: [Step Name]

**Inputs:**
- [Input 1: Source and format]
- [Input 2: Configuration or reference data]

**Processing:**
- [What happens in this step - business logic]
- [Key transformations or validations]
- [Error handling approach]

**Outputs:**
- [Output 1: Artifact name, format, destination]
- [Output 2: Metadata or logs]

**Example:**
### Step 3: Validate Data Against Schema

**Inputs:**
- Normalized vendor data (Parquet format from Step 2)
- PIM schema definition (S3://schemas/pim_v2.1.json)
- Vendor-specific business rules (DynamoDB table)

**Processing:**
- Validate each record against PIM schema (required fields, data types, value ranges)
- Apply vendor-specific business rules (e.g., category mappings, price validation)
- Generate detailed error messages for validation failures
- Track validation statistics (pass rate, error types, processing time)

**Outputs:**
- Validated records (Parquet format) → S3://validated/<vendor>/
- Validation errors (JSON format) → S3://errors/<vendor>/
- Validation summary (JSON) → CloudWatch Logs

## Conceptual Artifacts

[List of all significant data artifacts produced by the pipeline]

| Artifact Name | Format | Purpose | Retention |
|---------------|--------|---------|-----------|
| [Artifact 1] | [Format] | [What it's for] | [How long kept] |

Example:
| Artifact Name | Format | Purpose | Retention |
|---------------|--------|---------|-----------|
| Normalized Vendor Data | Parquet | Standardized input for validation | 90 days |
| Validation Errors | JSON | Vendor feedback on failed records | 1 year |
| Validated Products | Parquet | Input for PIM load | 30 days |
| Processing Summary | JSON | Audit trail and monitoring | 1 year |
| PIM Load Results | JSON | Confirmation of PIM updates | 1 year |

## Decision Points

[Critical points where processing branches based on conditions]

### Decision Point 1: [Name]

**Condition:** [What determines the branch]  
**Branch A:** [Action if condition true] → Continue to [Step X]  
**Branch B:** [Action if condition false] → Continue to [Step Y]

**Example:**
### Decision Point 1: Data Validation Result

**Condition:** All records pass PIM schema validation AND business rule validation  
**Branch A (Valid):** Continue to Step 5 (Transform to PIM format)  
**Branch B (Invalid):** Generate error report → Email vendor → End processing

**Business Rule:** Partial failures allowed if >95% of records valid (load valid records, report errors)

## Existing Job Mapping

[Map pipeline steps to existing Glue jobs where applicable]

| Pipeline Step | Existing Job | Notes |
|---------------|--------------|-------|
| Step 1 | `jobs/ingestion/s3_file_ingest` | Can reuse with config changes |
| Step 3 | New job required | No existing validation framework |

**TBD:** Review feasibility of reusing existing jobs vs creating new ones

## Unknowns and Open Decisions

### Unknowns Requiring Investigation

- **TBD:** [Technical unknown that needs research]
- **TBD:** [Performance characteristic that needs testing]

Example:
- **TBD:** PIM API throughput limits under load (need load testing)
- **TBD:** Optimal Glue worker configuration for file parsing (need benchmarking)

### Open Decisions Requiring Stakeholder Input

- **OPEN QUESTION:** [Decision point requiring business input]
- **OPEN QUESTION:** [Architecture choice requiring technical input]

Example:
- **OPEN QUESTION:** Should validation errors stop entire batch or allow partial processing?
- **OPEN QUESTION:** How to handle duplicate vendor submissions (reject vs merge)?

## Next Steps

1. [Immediate next action after approval]
2. [Follow-up investigation needed]
3. [Stakeholder decision required]

Example:
1. **Get architecture approval** from Technical Lead and Data Architect
2. **Investigate unknowns:** Conduct PIM API load testing, benchmark Glue configurations
3. **Resolve open questions:** Schedule decision meeting with Product Owner
4. **Proceed to Step 2b:** Break down into capability specifications

## Approval Status

**Status:** [DRAFT | REVIEW | APPROVED]  
**Approved By:** [Technical Lead, Architect]  
**Approval Date:** [YYYY-MM-DD]

---

**Signed:**
- Technical Lead: _________________ Date: _______
- Data Architect: _________________ Date: _______
```

### Step 2a Workflow Guide

1. **Generate Initial Plan (Day 1)**
   - Run: `python tools/pipeline_planner_agent.py create --objective docs/roadmaps/<objective>.md`
   - Agent generates initial pipeline plan
   - Review for completeness and logical flow

2. **Technical Review (Days 2-3)**
   - Review with Technical Lead and Architect
   - Validate processing sequence makes sense
   - Identify reusable existing jobs
   - Document technical unknowns

3. **Refine Decision Points (Days 3-4)**
   - Clarify branching logic and conditions
   - Define error handling approaches
   - Document business rules affecting flow

4. **Artifact Review (Day 4-5)**
   - Validate all conceptual artifacts identified
   - Confirm retention policies with compliance
   - Ensure artifacts support audit requirements

5. **Final Approval (Days 5-7)**
   - Address all review comments
   - Resolve or document unknowns
   - Collect technical approvals
   - Proceed to Step 2b

---

## Step 2b: Capability Specification Template

### Template Overview

**Purpose:** Detail technical specifications for implementing a specific capability.  
**Output Location:** `docs/specifications/<capability>.yaml`  
**Approval Required:** Yes - technical lead approval before Step 3

### Template Structure

```yaml
# Capability Specification
# Generated: YYYY-MM-DD
# Status: [DRAFT | REVIEW | APPROVED]

capability_name: descriptive_capability_name
  
objective: |
  Clear, concise statement of what this capability accomplishes.
  Focus on business value and technical outcome.
  
  Example:
  "Validate vendor-submitted product data against PIM schema requirements and business rules.
  This capability ensures data quality before PIM load, reducing manual cleanup by 90%."

scope:
  includes:
    - [Specific functionality 1 that IS in scope]
    - [Specific functionality 2 that IS in scope]
    - [Specific functionality 3 that IS in scope]
  excludes:
    - [Specific functionality that is NOT in scope]
    - [Why it's excluded or reference to other capability]

# Example:
scope:
  includes:
    - PIM schema validation (required fields, data types, value ranges)
    - Vendor-specific business rule validation per contract
    - Detailed error reporting with actionable messages
    - Validation statistics and metrics
  excludes:
    - Data enrichment (handled by separate enrichment capability)
    - Duplicate detection (handled upstream in normalization)
    - Historical data validation (one-time migration, separate process)

inputs:
  - name: input_name_1
    type: [S3 Object | DynamoDB Table | API Response | etc.]
    format: [Parquet | JSON | CSV | etc.]
    location: s3://bucket/path/ or other location
    description: |
      What this input contains and how it's used
    schema_reference: path/to/schema/if/applicable
    
  - name: input_name_2
    type: Configuration
    format: JSON
    location: s3://config/validation_rules.json
    description: |
      Validation rules configuration per vendor

# Example:
inputs:
  - name: normalized_vendor_data
    type: S3 Object
    format: Parquet
    location: s3://vendor-data/normalized/{vendor_id}/{date}/
    description: |
      Vendor product data normalized to common schema by upstream process.
      Contains product attributes, pricing, and categorization.
    schema_reference: s3://schemas/normalized_vendor_schema_v1.parquet
    
  - name: pim_schema_definition
    type: S3 Object
    format: JSON Schema
    location: s3://schemas/pim_v2.1.json
    description: |
      PIM schema definition including required fields, data types, and validation rules
    
  - name: vendor_business_rules
    type: DynamoDB Table
    format: Key-Value
    location: table:vendor_rules
    description: |
      Vendor-specific business rules and contract requirements

outputs:
  - name: output_name_1
    type: [S3 Object | Database Record | etc.]
    format: [Format]
    location: destination
    description: |
      What this output contains and its purpose
    schema_reference: path/to/schema/if/applicable
    
  - name: output_name_2
    type: S3 Object
    format: JSON
    location: s3://errors/validation/{vendor_id}/{date}/
    description: |
      Validation error details for failed records

# Example:
outputs:
  - name: validated_products
    type: S3 Object
    format: Parquet
    location: s3://vendor-data/validated/{vendor_id}/{date}/
    description: |
      Product records that passed all validation checks, ready for PIM load
    schema_reference: s3://schemas/pim_ready_schema_v1.parquet
    
  - name: validation_errors
    type: S3 Object
    format: JSON
    location: s3://errors/validation/{vendor_id}/{date}/
    description: |
      Detailed validation errors with record IDs, field names, error types, and actionable messages
      
  - name: validation_summary
    type: CloudWatch Logs
    format: JSON
    location: log-group:/aws/glue/validation
    description: |
      Processing statistics: records processed, pass rate, error types, processing time

processing_requirements:
  - [Specific processing rule or logic 1]
  - [Specific processing rule or logic 2]
  - [Business rule or calculation 3]

# Example:
processing_requirements:
  - Validate all records against PIM schema v2.1 (required fields, data types, ranges)
  - Apply vendor-specific business rules from DynamoDB configuration
  - Generate detailed error messages specifying field name, current value, expected value
  - Track validation statistics per vendor and error type
  - Process in batches of 10,000 records for memory efficiency
  - Implement retry logic for transient DynamoDB read failures

parameters:
  - name: parameter_name
    type: [string | integer | boolean | etc.]
    required: [true | false]
    default: default_value_if_optional
    description: |
      What this parameter controls and valid values

# Example:
parameters:
  - name: vendor_id
    type: string
    required: true
    description: |
      Unique vendor identifier (format: VEN-XXXXX)
      
  - name: processing_date
    type: string
    required: true
    description: |
      Date of vendor submission (format: YYYY-MM-DD)
      
  - name: strict_mode
    type: boolean
    required: false
    default: false
    description: |
      If true, reject entire batch on any validation error.
      If false, process valid records and report errors separately.
      
  - name: error_threshold_pct
    type: integer
    required: false
    default: 5
    description: |
      Maximum percentage of errors allowed before failing batch (range: 0-100)

success_criteria:
  functional:
    - [Testable functional criterion 1]
    - [Testable functional criterion 2]
  quality:
    - [Performance or quality metric 1]
    - [Performance or quality metric 2]

# Example:
success_criteria:
  functional:
    - All valid records pass validation without errors
    - Invalid records identified with specific error codes and field-level details
    - 100% of input records accounted for (validated or errored, no data loss)
    - Validation follows PIM schema v2.1 exactly (no schema drift)
  quality:
    - Processing completes within 30-minute SLA for files <5GB
    - Memory usage stays under 10GB per worker
    - Zero data loss during validation process
    - Error messages actionable by vendors (field name, current value, expected format)

dependencies:
  prerequisites:
    - [System or resource that must exist first]
    - [Access or permission required]
  runtime_dependencies:
    - [Service or system called during execution]

# Example:
dependencies:
  prerequisites:
    - PIM schema definition available at s3://schemas/pim_v2.1.json
    - Vendor business rules configured in DynamoDB table:vendor_rules
    - S3 buckets created: validated/, errors/
    - CloudWatch log group created: /aws/glue/validation
  runtime_dependencies:
    - DynamoDB table:vendor_rules (read access)
    - S3 read/write permissions for input and output buckets
    - PIM schema definition (S3 read access)

assumptions:
  - ASSUMPTION: Vendor files are <5GB per submission (requires approval) [APPROVED: 2026-01-15]
  - ASSUMPTION: Max 100K products per submission (requires approval) [APPROVED: 2026-01-15]
  - ASSUMPTION: PIM schema updates occur quarterly with 30-day notice (requires approval) [PENDING]

# Note: All assumptions must be explicitly labeled and require human approval before implementation
# Format: "ASSUMPTION: [statement] (requires approval) [APPROVED: date | PENDING | REJECTED]"

notes: |
  Additional context, constraints, or considerations not captured elsewhere.
  
  Example:
  - Consider implementing caching for PIM schema to reduce S3 reads
  - Vendor X requires special handling for category codes (see ticket #1234)
  - Performance testing required before production deployment

approval_status:
  status: DRAFT  # or REVIEW or APPROVED
  approved_by: null  # Technical Lead name after approval
  approval_date: null  # YYYY-MM-DD after approval
  reviewer_comments: |
    Space for reviewer feedback during review process
```

### Step 2b Workflow Guide

1. **Generate Initial Spec (Day 1)**
   - Run: `python tools/capability_planner_agent.py create --pipeline <pipeline_plan> --capability-name "<name>"`
   - Agent generates initial YAML specification
   - Review for completeness

2. **Technical Specification Review (Days 2-4)**
   - Review with Technical Lead
   - Validate input/output specifications
   - Confirm processing requirements are clear
   - Define all parameters needed

3. **Dependency and Assumption Review (Days 4-5)**
   - Document all external dependencies
   - Identify all assumptions
   - Get approval for critical assumptions
   - Validate prerequisites are achievable

4. **Success Criteria Definition (Day 5-6)**
   - Define specific, testable functional criteria
   - Set measurable quality targets
   - Ensure criteria align with capability objective

5. **Final Approval (Days 6-7)**
   - Address all review comments
   - Validate spec against standards: `python tools/capability_planner_agent.py validate <spec_file>`
   - Collect technical lead approval
   - Proceed to Step 3

---

## Step 4: Codex Task Template

### Template Overview

**Purpose:** Define a discrete development task for implementation.  
**Output Location:** `docs/codex-tasks/<task_id>.md`  
**Approval Required:** Yes - review before assigning to implementation

### Template Structure

```markdown
# Codex Task: [Task Name]

## Objective

[Clear, concise statement of what this specific task accomplishes. Should be completable in 1-3 hours.]

Example:
"Implement PIM schema validation module that validates vendor product records against PIM schema v2.1, returning detailed error messages for invalid fields."

## Standards References

- See `docs/standards/script_card_spec.md` for script card documentation requirements
- See `docs/standards/business_job_description_spec.md` for business description format
- See `docs/standards/job_manifest_spec.md` for manifest format requirements
- See `docs/standards/validation_standard.md` for validation procedures

## Target Script/Path (Explicit)

`jobs/vendor_processing/validation/glue_script.py`

## File Restrictions (Explicit)

**Allowed to modify:**
- `jobs/vendor_processing/validation/*` (all files in this directory)
- `jobs/vendor_processing/shared/schema_utils.py` (if adding shared utilities)

**NOT allowed to modify:**
- Any files outside `jobs/vendor_processing/` directory
- Existing job manifests or configurations
- Files in `jobs/vendor_processing/normalization/` (separate capability)

**Rationale:** Restricts changes to validation capability only, prevents unintended side effects on other jobs.

## Implementation Requirements

1. [Specific requirement 1 with acceptance criterion]
2. [Specific requirement 2 with acceptance criterion]
3. [Specific requirement 3 with acceptance criterion]

Example:
1. Load PIM schema from `s3://schemas/pim_v2.1.json` at job startup
2. Validate each product record against schema:
   - Check required fields present
   - Validate data types match schema
   - Validate values within allowed ranges/enums
3. Generate detailed error messages format:
   ```json
   {
     "record_id": "12345",
     "field_name": "price",
     "error_type": "INVALID_TYPE",
     "current_value": "abc",
     "expected": "numeric value >= 0"
   }
   ```
4. Return tuple: (valid_records_df, error_records_df)
5. Log validation statistics to CloudWatch

## Acceptance Criteria

- [ ] [Testable criterion 1 - can verify with yes/no]
- [ ] [Testable criterion 2 - specific behavior or output]
- [ ] [Testable criterion 3 - integration or error handling]

Example:
- [ ] Valid records pass validation without errors
- [ ] Invalid records generate detailed error messages with field name, current value, expected format
- [ ] Schema loaded successfully from S3 at job startup
- [ ] Validation statistics logged to CloudWatch (records processed, pass rate, error types)
- [ ] Unit tests cover all validation rules (>90% code coverage)
- [ ] Integration test processes sample vendor file successfully

## Quality Gates (Must Pass)

1. **Code Quality:**
   - Follows repository coding standards
   - Includes docstrings for all functions
   - No hard-coded values (use parameters)

2. **Testing:**
   - Unit tests pass with >90% coverage
   - Integration tests pass with sample data
   - Error handling tested with invalid inputs

3. **Documentation:**
   - Script card created/updated per `docs/standards/script_card_spec.md`
   - Inline comments explain complex logic
   - README updated if new dependencies added

4. **Validation:**
   - Run validation per `docs/standards/validation_standard.md`
   - All validation checks pass
   - No new validation warnings introduced

## Boundaries (What This Element Does NOT Do)

- Does NOT handle data normalization (separate task/capability)
- Does NOT perform duplicate detection (out of scope for validation)
- Does NOT transform data to PIM format (separate task - PIM transformation)
- Does NOT load data into PIM (separate task - PIM loader)

**Rationale:** Keep task focused on single responsibility (validation only), prevents scope creep.

## Related Tasks

- Depends on: `normalization_001` (provides normalized input data)
- Depended on by: `pim_transformation_003` (consumes validated data)
- Related: `error_reporting_004` (uses validation errors for reporting)

## Notes

[Additional context, edge cases, or implementation hints]

Example:
- PIM schema includes complex nested structures - use recursive validation
- Some vendor-specific rules stored in DynamoDB - cache for performance
- Error messages must be vendor-friendly (non-technical language)
- Consider batch processing for large files (process 10K records at a time)

## Approval Status

**Status:** [DRAFT | READY | APPROVED | IN_PROGRESS | COMPLETED]  
**Assigned To:** [Agent/Developer name after approval]  
**Created:** [YYYY-MM-DD]  
**Approved:** [YYYY-MM-DD]  
**Completed:** [YYYY-MM-DD]
```

### Step 4 Workflow Guide

1. **Generate Tasks from Capability (Day 1)**
   - Run: `python tools/coding_agent.py create-tasks --capability <spec_file>`
   - Agent generates tasks from approved capability spec
   - Review proposed task decomposition

2. **Task Review (Days 2-3)**
   - Review each task for clarity and scope
   - Ensure file restrictions prevent conflicts
   - Validate acceptance criteria are testable
   - Confirm boundaries prevent scope creep

3. **Dependency Check (Day 3-4)**
   - Verify task dependencies are correct
   - Ensure tasks can be completed in logical order
   - Identify any parallel execution opportunities

4. **Approval and Assignment (Days 4-5)**
   - Get approval for task set
   - Assign tasks to implementation
   - Track progress and completion

---

## Best Practices

### For All Templates

1. **Be Specific:** Avoid vague language; use concrete, measurable terms
2. **Label Unknowns:** Mark TBD and OPEN QUESTION items explicitly
3. **Document Assumptions:** Label all assumptions and track approval status
4. **Link Standards:** Reference relevant `docs/standards/` specifications
5. **Seek Approval:** Don't skip approval gates - they prevent rework

### For Iterative Refinement

1. **Start Simple:** Initial draft doesn't need to be perfect
2. **Iterate Quickly:** Multiple short review cycles better than one long cycle
3. **Capture Feedback:** Document all review comments and resolutions
4. **Version Control:** Use git commits to track template evolution
5. **Learn from History:** Review previous similar objectives/capabilities

### For Workflow Progression

1. **Don't Skip Steps:** Complete each step before moving to next
2. **Validate Frequently:** Run validation tools after each significant change
3. **Maintain Traceability:** Link documents (objective → pipeline → capability → tasks)
4. **Communicate Changes:** Alert stakeholders when templates updated
5. **Archive Approvals:** Keep records of who approved what and when

---

## Troubleshooting

### Template Validation Failures

**Problem:** "Template missing required sections"

**Solution:** Compare your template against the structure in this document. Ensure all mandatory sections present.

**Problem:** "Assumptions not properly labeled"

**Solution:** All assumptions must follow format: `ASSUMPTION: [statement] (requires approval) [STATUS]`

### Approval Delays

**Problem:** Stakeholders not responding to approval requests

**Solution:**
1. Set clear deadlines when requesting approval
2. Escalate to project sponsor if delays persist
3. Document approval status in weekly project updates

**Problem:** Multiple rounds of revisions after "final" review

**Solution:**
1. Conduct incremental reviews (don't wait for complete draft)
2. Use checklists to ensure completeness before final review
3. Get early alignment on contentious decisions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial extraction from agent_system_context.md - example templates and workflow guides |

---

## See Also

- `docs/context_packs/agent_system_context.md` - High-level governance and workflow integration
- `docs/workflows/agent_tools_reference.md` - Detailed CLI specifications and troubleshooting
- `docs/standards/` - Authoritative standards for all templates and specifications
- `docs/workflows/WORKFLOW_5_STEPS.md` - Complete workflow documentation


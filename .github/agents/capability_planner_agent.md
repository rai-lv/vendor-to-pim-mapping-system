# Capability Planner Agent Profile

## Name
Capability Planner Agent (Step 2b: Capability Plan / Step-Level)

## Description
The Capability Planner Agent creates detailed specifications for individual capabilities identified in the pipeline plan. It translates high-level pipeline steps into actionable specifications with clear inputs, outputs, business rules, acceptance criteria, and boundaries. The agent ensures that each capability is well-defined before decomposition and implementation, focusing on the "what" (requirements) rather than the "how" (implementation details). It facilitates structured discussions to achieve stakeholder consensus on each capability's scope, logic, and success criteria.

## Task Scope
The Capability Planner Agent operates at **Step 2b** of the 5-step development workflow and is responsible for:

1. **Capability Specification**: Creating detailed specifications for ONE capability/step from the approved pipeline plan, defining its purpose, scope, and requirements.

2. **Input/Output Definition**: Specifying inputs and outputs by MEANING (what the data represents) rather than by storage details (S3 paths, file formats, schemas).

3. **Business Rules Documentation**: Defining validation rules, transformation logic, decision criteria, and error handling rules that the capability must enforce.

4. **Acceptance Criteria Definition**: Establishing testable functional and quality criteria that objectively determine when the capability is successfully implemented.

5. **Boundary Clarification**: Explicitly defining what the capability DOES and does NOT do to prevent scope creep and ensure clear handoffs to other capabilities.

6. **Dependency Mapping**: Identifying upstream capabilities (data producers), downstream capabilities (data consumers), and external systems required for this capability.

7. **Unknown Identification**: Explicitly documenting unknowns that must be resolved before implementation, with no assumptions presented as facts.

8. **Discussion Facilitation**: Supporting structured manual discussions to ensure technical and business alignment on capability requirements.

9. **Specification Documentation**: Creating the authoritative capability specification at `docs/specifications/<capability_name>_capability.yaml` in structured YAML format.

**Critical Rules:**
- Define inputs/outputs by **meaning**, NOT by S3 location, file format, or schema details (deferred to implementation)
- Explicitly state boundaries — what this capability does and does NOT do
- Capability plan cannot be created without approved Step 2a pipeline plan
- Changes to Step 2a require re-validation of affected Step 2b capability plans
- Manual approval required before proceeding to Step 3 (Decomposition)
- One capability plan per capability; repeat Step 2b for each capability in the pipeline

## Inputs

### Primary Input
**Approved Step 2a Pipeline Plan**: `docs/roadmaps/<objective_name>_pipeline_plan.md`

The agent requires a completed and stakeholder-approved pipeline plan from the Pipeline Planner Agent (Step 2a).

### Capability Selection
**Specific Capability/Step**: The agent must be told which capability from the pipeline plan to specify (e.g., "data_validation", "data_normalization").

### Discussion Inputs
The agent facilitates gathering the following through manual stakeholder discussions:

1. **Business Rules**: Validation rules, transformation logic, quality standards that must be enforced
2. **Input Requirements**: What data/artifacts this capability consumes and what they represent
3. **Output Requirements**: What data/artifacts this capability produces and what they represent
4. **Acceptance Criteria**: Functional and quality criteria for successful implementation
5. **Boundary Definitions**: Clear in-scope vs. out-of-scope boundaries
6. **Dependencies**: Upstream data producers, downstream consumers, external systems/APIs
7. **Error Handling**: How errors should be detected, reported, and handled

## Outputs

### Primary Output
**Capability Specification Document**: `docs/specifications/<capability_name>_capability.yaml`

The capability specification is a structured YAML document including:

1. **Metadata**:
   - `capability_name`: Unique identifier for this capability
   - `description`: Clear, concise purpose statement
   - `pipeline_reference`: Path to Step 2a pipeline plan document
   - `pipeline_step`: Which step in the pipeline this capability implements

2. **Inputs** (defined by meaning):
   - `name`: Conceptual artifact name (from pipeline plan)
   - `meaning`: What the input represents in business context
   - `producer`: Which upstream capability/step creates this input
   - `required`: true/false
   - `business_context`: Extended description of business significance

3. **Outputs** (defined by meaning):
   - `name`: Conceptual artifact name (from pipeline plan)
   - `meaning`: What the output represents in business context
   - `consumer`: Which downstream capability/step uses this output
   - `type`: `always_produced`, `produced_on_success`, `produced_on_failure`
   - `business_context`: Extended description of business significance

4. **Business Rules**:
   - `rule_id`: Unique identifier (e.g., VR-001, TR-002)
   - `description`: Rule name/summary
   - `logic`: Detailed rule logic and conditions
   - `error_handling`: What happens when rule is violated

5. **Acceptance Criteria**:
   - `functional`: List of functional criteria with verification methods
   - `quality`: List of quality criteria (performance, accuracy, etc.) with verification methods

6. **Boundaries**:
   - `in_scope`: Explicit list of what this capability DOES
   - `out_of_scope`: Explicit list of what this capability does NOT do

7. **Dependencies**:
   - `upstream`: Upstream capabilities with dependency details
   - `downstream`: Downstream capabilities with dependency details
   - `external_systems`: External APIs/services/databases with connection details

8. **Unknowns**: List of unknowns requiring resolution:
   - `id`: Unknown identifier (e.g., UNK-001)
   - `description`: What is unknown
   - `impact`: How this affects implementation
   - `resolution_target`: When this must be resolved

### Process Outputs
- **Discussion Checkpoints**: Structured agendas and outcomes for capability requirement alignment
- **Approval Gate**: Stakeholder sign-off indicating readiness to proceed to Step 3 (Decomposition)

## Supported Commands

### Create Capability Specification
```bash
python tools/capability_planner_agent.py create "capability_name" \
  --pipeline-ref "objective_name_pipeline_plan.md"
```

**Purpose**: Creates a capability specification at `docs/specifications/<capability_name>_capability.yaml`

**Parameters**:
- `capability_name`: Unique name for this capability (used in filename, matches capability from pipeline plan)
- `--pipeline-ref`: Filename of the Step 2a pipeline plan in `docs/roadmaps/`

**Validation**: Agent verifies that:
- The referenced pipeline plan exists
- The capability name corresponds to a step/capability in the pipeline plan

**Output**: Creates the capability specification with template sections ready for collaborative refinement

### Additional Operations
The Capability Planner Agent script may support additional commands for:
- Viewing existing capability specifications
- Validating capability specification structure (YAML syntax, required fields)
- Listing capabilities from a pipeline plan that need specifications

## Integration

### Workflow Position
The Capability Planner Agent operates at **Step 2b** in the 5-step development workflow:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan (Capability Planner Agent) ← THIS AGENT
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
```

**Note**: Step 2b is **repeated for EACH capability** identified in the Step 2a pipeline plan. Each capability gets its own specification document and approval process.

### Manual Discussion Process
The Capability Planner Agent supports a structured discussion process with defined checkpoints:

**Checkpoint 1: Input/Output Definition (Day 1)**
- **Participants**: Tech Lead, Data Architect, Business Analyst
- **Focus**: Define inputs/outputs by business meaning, establish producer/consumer relationships, document business context
- **Output**: Complete inputs/outputs specification (conceptual, not storage-focused)

**Checkpoint 2: Business Rules and Logic (Day 2-3)**
- **Participants**: Business Analyst, Product Owner, Tech Lead
- **Focus**: Define validation rules, transformation logic, error handling, decision criteria
- **Output**: Complete business rules catalog with error handling strategies

**Checkpoint 3: Acceptance Criteria Definition (Day 3-4)**
- **Participants**: QA Lead, Tech Lead, Product Owner
- **Focus**: Define testable functional criteria, establish quality metrics (performance, accuracy), specify verification methods
- **Output**: Testable acceptance criteria with clear verification approaches

**Checkpoint 4: Boundaries and Scope (Day 4)**
- **Participants**: Tech Lead, Architect, Product Owner
- **Focus**: Explicitly define in-scope responsibilities, document out-of-scope items, clarify gray areas
- **Output**: Clear boundary definitions preventing scope creep

**Checkpoint 5: Dependencies and Unknowns (Day 5)**
- **Participants**: Tech Lead, Integration Architect, DevOps
- **Focus**: Map upstream/downstream dependencies, identify external system requirements, document unknowns requiring resolution
- **Output**: Complete dependency map and prioritized unknowns list

**Final Approval Checkpoint**
- **Participants**: All stakeholders
- **Deliverable**: Signed-off capability specification ready for Step 3 decomposition
- **Gate**: Document becomes locked and authoritative for implementation planning

### Dependency Chain
- **Prerequisites**: 
  - Approved Step 2a pipeline plan (`docs/roadmaps/<objective_name>_pipeline_plan.md`)
  - Approved Step 1 objective (transitively required through Step 2a)
- **Dependents**: Coding Agent (Step 3) uses approved capability specifications for decomposition and Codex task generation
- **Validation**: Agent verifies Step 2a document exists and references the specified capability
- **Authority**: The capability specification serves as the authoritative requirements document for implementation

### Quality Gates
- Step 2a pipeline plan must be approved before any Step 2b capability plans can begin
- Manual stakeholder approval required for each capability specification before proceeding to Step 3
- All unknowns explicitly documented (no assumptions)
- Acceptance criteria must be testable and verifiable
- Boundaries must be clear and agreed upon by stakeholders
- Inputs/outputs defined by meaning (not by storage implementation)

### Integration with Repository Structure
The capability specification:
- **References**: Pipeline plan from `docs/roadmaps/`
- **Used By**: Coding Agent for decomposition (`tools/coding_agent.py decompose`)
- **Informs**: Documentation Agent for creating business descriptions and script cards
- **Validated By**: Testing Agent for specification-based test inference

## Example Usage

### Scenario: Create Capability Specification for Data Validation

**Context**: The vendor onboarding pipeline plan (Step 2a) identified "Data Validation" as a new capability requiring full specification.

**Step 1: Invoke Capability Planner Agent**
```bash
python tools/capability_planner_agent.py create "data_validation" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"
```

**Output**: Creates `docs/specifications/data_validation_capability.yaml` with initial template

**Step 2: Collaborative Capability Specification**

The team conducts structured discussions to complete the specification:

**Input/Output Discussion (Day 1):**
- Input identified: `staged_raw_data` (unprocessed vendor data from ingestion step)
- Outputs identified:
  - `validation_report` (always produced, consumed by notification)
  - `validated_data` (produced only on success, consumed by normalization)
- Business context documented for each artifact
- Outcome: Complete input/output specification by meaning

**Business Rules Discussion (Day 2-3):**
- Rules defined:
  - VR-001: SKU uniqueness check (reject submission if duplicates found)
  - VR-002: Required field validation (name, SKU, price, category mandatory)
  - VR-003: Price range validation ($0.01 to $999,999.99)
  - VR-004: Category mapping validation (vendor category must map to PIM)
  - VR-005: Data completeness check (≥80% pass rate required)
- Error handling documented for each rule
- Outcome: Complete business rules catalog

**Acceptance Criteria Discussion (Day 3-4):**
- Functional criteria:
  - ✓ Validates all required fields per business rules
  - ✓ Detects duplicate SKUs within submission
  - ✓ Produces detailed validation report with row-level errors
  - ✓ Only passes validated data to downstream step (excludes invalid rows)
- Quality criteria:
  - ✓ Processes 10,000 row submission within 5 minutes
  - ✓ Validation accuracy ≥99.9% (no false positives/negatives)
  - ✓ Zero data loss (input row count = report row count)
- Verification methods defined for each criterion
- Outcome: Testable acceptance criteria with verification approaches

**Boundaries Discussion (Day 4):**
- In-scope:
  - Validate data against defined business rules
  - Generate detailed validation reports
  - Pass validated data to normalization
  - Reject submissions below quality threshold
- Out-of-scope:
  - Data transformation/normalization (Step 3 responsibility)
  - Direct PIM integration (Step 4 responsibility)
  - Vendor notification (Step 5 responsibility)
  - Historical data validation (current submissions only)
  - Category mapping creation (use existing mappings only)
- Outcome: Clear scope boundaries preventing overlap

**Dependencies Discussion (Day 5):**
- Upstream: Data Ingestion provides `staged_raw_data`
- Downstream: Data Normalization consumes `validated_data`, Notification consumes `validation_report`
- External: PIM Category Mapping Service (API endpoint TBD, required for VR-004)
- Unknowns identified:
  - UNK-001: PIM Category Mapping Service API endpoint and auth
  - UNK-002: Expected average submission file size
  - UNK-003: Vendor notification preferences (affects report format)
- Outcome: Complete dependency map and unknowns list

**Step 3: Final Approval and Handoff**
- All stakeholders review complete capability specification
- Sign-off obtained
- Document locked as authoritative reference
- Ready for Step 3 decomposition by Coding Agent

### Expected Document Structure

```yaml
capability_name: data_validation
description: Validate vendor submission data against business rules and data quality standards
pipeline_reference: docs/roadmaps/vendor_onboarding_pipeline_plan.md
pipeline_step: "Step 2: Data Validation"

inputs:
  - name: staged_raw_data
    meaning: Unprocessed vendor data staged for validation
    producer: data_ingestion (Step 1)
    required: true
    business_context: |
      Raw vendor-submitted product catalog data including SKUs, descriptions,
      pricing, inventory levels, and vendor metadata. Data may be in various
      formats (CSV, JSON, Excel) and has not been validated or transformed.
      This is the untrusted input that must be rigorously checked before
      further processing.

outputs:
  - name: validation_report
    meaning: Detailed report of validation errors, warnings, and data quality issues
    consumer: notification (Step 5), manual_review_queue
    type: always_produced
    business_context: |
      Row-level validation results indicating which data elements passed or failed
      business rules. Includes error codes, human-readable error messages, row
      identifiers, and suggested fixes for vendors to correct their submissions.
      Produced regardless of validation outcome (success or failure).
  
  - name: validated_data
    meaning: Vendor data confirmed to meet all business rules and quality standards
    consumer: data_normalization (Step 3)
    type: produced_on_success
    business_context: |
      Subset of staged raw data that passed all validation rules and meets the
      ≥80% quality threshold. Contains only valid rows ready for transformation
      to PIM schema. Only produced when validation succeeds; not produced when
      submission fails validation.

business_rules:
  - rule_id: VR-001
    description: SKU uniqueness check
    logic: |
      Each vendor SKU must be unique within a single submission. No duplicate
      SKU values are permitted in the same vendor submission file.
    error_handling: |
      If duplicate SKUs are detected, reject the entire submission with error
      code "DUPLICATE_SKU" and list all duplicate SKU values in the validation
      report. Submission cannot proceed to normalization.
  
  - rule_id: VR-002
    description: Required field validation
    logic: |
      The following fields are mandatory for every product row:
      - product_name (non-empty string)
      - vendor_sku (non-empty string)
      - price (numeric value)
      - category (non-empty string)
    error_handling: |
      Mark row as invalid with error code "MISSING_REQUIRED_FIELD" and specify
      which field(s) are missing. Invalid rows are excluded from validated_data
      but submission can proceed if ≥80% of rows are valid.
  
  - rule_id: VR-003
    description: Price range validation
    logic: |
      Price field must be a positive numeric value between $0.01 and $999,999.99
      inclusive. Prices of $0.00 or negative values are invalid. Prices above
      $999,999.99 are flagged for manual review.
    error_handling: |
      Mark row as invalid with error code "PRICE_OUT_OF_RANGE" and specify the
      invalid value. Invalid rows excluded from validated_data output.
  
  - rule_id: VR-004
    description: Category mapping validation
    logic: |
      Vendor category value must have a corresponding mapping in the PIM Category
      Mapping Service. Category must be an exact match (case-insensitive) to an
      existing mapping entry.
    error_handling: |
      If no mapping exists, mark row with error code "CATEGORY_UNMAPPED" and flag
      for manual review. Row is excluded from validated_data but does not fail
      the submission if ≥80% of rows pass.
  
  - rule_id: VR-005
    description: Data completeness check
    logic: |
      At least 80% of rows in the submission must pass all validation rules
      (VR-001 through VR-004) for the submission to be considered successful.
      Calculate pass rate as: (valid_row_count / total_row_count) * 100.
    error_handling: |
      If pass rate is below 80%, reject the entire submission with error code
      "INSUFFICIENT_DATA_QUALITY". No validated_data output is produced. Vendor
      must fix errors and resubmit.

acceptance_criteria:
  functional:
    - criterion: Validates all required fields per business rules
      verification: |
        Test with sample data missing each required field (name, SKU, price,
        category). Verify that each missing field is detected and reported
        with error code MISSING_REQUIRED_FIELD.
    
    - criterion: Detects duplicate SKUs within submission
      verification: |
        Test with intentionally duplicated SKU data (e.g., SKU "ABC123" appears
        in rows 5 and 12). Verify that validation report identifies both rows
        and submission is rejected with error code DUPLICATE_SKU.
    
    - criterion: Produces detailed validation report with row-level errors
      verification: |
        Test with mixed valid/invalid data. Verify that validation report
        contains: row identifiers, error codes, field names, invalid values,
        and suggested corrections for each error.
    
    - criterion: Only passes validated data to downstream step
      verification: |
        Test with 100-row submission where 20 rows are invalid. Confirm that
        validated_data output contains exactly 80 rows (valid rows only) and
        invalid rows are excluded.
    
    - criterion: Enforces 80% quality threshold
      verification: |
        Test with submission where 75% of rows are valid (below threshold).
        Verify that submission is rejected, no validated_data is produced, and
        validation report contains error code INSUFFICIENT_DATA_QUALITY.
  
  quality:
    - criterion: Processes 10,000 row submission within 5 minutes
      verification: |
        Performance test with 10,000-row sample file containing realistic data
        distribution (90% valid, 10% invalid). Measure total processing time
        from input to validation report generation. Must complete within 300s.
    
    - criterion: Validation accuracy ≥99.9% (no false positives/negatives)
      verification: |
        Compare validation results against manual review baseline using 1,000-row
        test dataset with known valid/invalid rows. Calculate accuracy as:
        (correct_validations / total_rows) * 100. Must achieve ≥99.9% accuracy.
    
    - criterion: Zero data loss during validation processing
      verification: |
        For any submission, verify that row count in validation report equals
        row count in input data. Every row must be accounted for (either in
        validated_data or in validation report as invalid). No rows silently
        dropped.

boundaries:
  in_scope:
    - Validate vendor data against defined business rules (VR-001 through VR-005)
    - Generate detailed validation reports with row-level error details
    - Pass validated data (successful rows) to normalization step
    - Reject submissions below 80% quality threshold
    - Check category mappings against PIM Category Mapping Service
    - Handle various input formats (CSV, JSON, Excel) from staging area
  
  out_of_scope:
    - Data transformation or normalization (handled by Step 3: Data Normalization)
    - Direct PIM system integration (handled by Step 4: PIM Integration)
    - Vendor notification of validation results (handled by Step 5: Notification)
    - Historical data validation (only validates current/new submissions)
    - Creation of new category mappings (only validates against existing mappings)
    - Format conversion (expects data already staged in consistent format)
    - Duplicate detection across multiple submissions (only within single submission)

dependencies:
  upstream:
    - capability: data_ingestion
      dependency_type: data_producer
      artifact: staged_raw_data
      notes: |
        Requires data ingestion to provide staged vendor data in standardized
        format. Ingestion step must handle initial format conversion (CSV/JSON/
        Excel to consistent structure).
  
  downstream:
    - capability: data_normalization
      dependency_type: data_consumer
      artifact: validated_data
      notes: |
        Normalization step expects validated data only (no invalid rows). If
        validation fails, normalization should not be invoked.
    
    - capability: notification
      dependency_type: data_consumer
      artifact: validation_report
      notes: |
        Notification step uses validation report to inform vendor of success/
        failure. Report must include actionable error messages.
  
  external_systems:
    - system: PIM Category Mapping Service
      purpose: Validate vendor categories against PIM taxonomy
      api_endpoint: TBD (see UNK-001)
      authentication: TBD (see UNK-001)
      notes: |
        Required for VR-004 rule enforcement. Must provide lookup capability
        for vendor category → PIM category mapping validation. Service must
        support case-insensitive matching.

unknowns:
  - id: UNK-001
    description: PIM Category Mapping Service API endpoint and authentication method
    impact: |
      Cannot implement VR-004 (category mapping validation) without API access.
      May need to defer this validation rule or implement placeholder logic.
    resolution_target: Before Step 3 decomposition
  
  - id: UNK-002
    description: Expected average submission file size and row count distribution
    impact: |
      Affects performance testing baseline and infrastructure sizing (Glue DPU
      allocation). Without this data, cannot accurately test QC-001 (10K rows
      in 5 minutes) with realistic scenarios.
    resolution_target: Before Step 5 implementation (can use estimates for Step 3-4)
  
  - id: UNK-003
    description: Vendor notification preferences (email vs. API callback)
    impact: |
      May affect validation report format requirements if vendors consume reports
      via automated API rather than email. Could require additional structured
      output format.
    resolution_target: Before Step 3 decomposition (affects validation report schema)
```

### Use Case Variations

**Simple Data Transformation Capability:**
```bash
python tools/capability_planner_agent.py create "price_currency_conversion" \
  --pipeline-ref "international_pricing_pipeline_plan.md"
```
Use for straightforward transformation capabilities with minimal business rules.

**Complex Multi-System Integration:**
```bash
python tools/capability_planner_agent.py create "inventory_sync_orchestration" \
  --pipeline-ref "omnichannel_inventory_pipeline_plan.md"
```
Use for capabilities requiring coordination across multiple external systems.

**Quality Assurance Capability:**
```bash
python tools/capability_planner_agent.py create "product_image_quality_check" \
  --pipeline-ref "media_asset_pipeline_plan.md"
```
Use for capabilities focused on quality checks and validation with detailed acceptance criteria.

**Enhancement of Existing Capability:**
```bash
python tools/capability_planner_agent.py create "enhanced_vendor_normalization" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"
```
Use when enhancing existing jobs (as identified in Step 2a job mapping) to support new requirements.

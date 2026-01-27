# Agent System Context — AI-supported Development Workflow

## Overview
This document defines and describes the roles, responsibilities, workflows, and outputs of the agents embedded in the development workflow for the `vendor-to-pim-mapping-system` repository. It ensures alignment between the agent-based approach, the broader system context (defined in `system_context.md`), and repository-wide standards.

The agent workflows are structured to enable alignment with the 5-step development process outlined in `WORKFLOW_5_STEPS.md`.

---

## Objectives of the Agent System
The agent system is designed to:
- Streamline the development workflow through automation where feasible.
- Maintain manual oversight during critical planning phases (Steps 1–2b).
- Enforce repository standards via automated quality gates.
- Dynamically maintain documentation artifacts as tasks evolve.
- Provide modular, self-contained scripts for executing specific roles in the workflow.

---

## Workflow Context: Steps 1–2 (Planning Phase)

The planning phase of the development workflow consists of **three sequential steps** with strict dependency requirements:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan / Pipeline-Level (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements
```

**Critical Rules:**
1. **Sequential Execution:** Each step must be completed and approved before proceeding to the next.
2. **Manual Discussion Required:** Each planning step output requires human review, discussion, and explicit approval.
3. **No Assumptions:** All unknowns must be explicitly marked; assumptions are not permitted.
4. **Evidence-Based:** Plans must reference existing code/jobs where applicable and mark unknowns explicitly.

---

## Agent Roles — Planning Agents (Steps 1–2)

### 1. Planner Agent (Step 1: Define Objective)

**Role:** Define the business objective with explicit boundaries, testable success criteria, and risk assessment.

**Script Location:** `tools/planner_agent.py`

**Workflow Position:** Step 1 of the 5-step workflow

#### Purpose and Responsibilities

The Planner Agent is responsible for creating structured objective definitions that answer:
- **What must be achieved?** Specific, measurable goals and expected outcomes.
- **What is out-of-scope?** Explicit boundaries preventing scope creep.
- **How do we know we succeeded?** Testable functional and quality criteria.
- **What are the constraints?** Technical, business, time, and resource limitations.
- **What are the risks?** Known risks, unknowns, and open questions requiring resolution.

The Planner Agent facilitates **manual discussion** between stakeholders to ensure consensus on objectives before any design or implementation work begins.

#### Inputs

- **Primary Input:** Human-provided objective name and description.
- **Discussion Inputs:** 
  - Business requirements and expected outcomes
  - Stakeholder priorities and constraints
  - Known technical or business limitations
  - Risk factors and open questions

#### Outputs

**Primary Output:** Objective definition document at `docs/roadmaps/<objective_name>.md`

The objective definition must include:
1. **Objective Statement:** Clear description of what must be achieved.
2. **Expected Outcomes:** Specific, measurable results.
3. **Out-of-Scope Boundaries:** Explicit list of what is NOT included.
4. **Success Criteria:** Testable functional and quality criteria for completion validation.
5. **Constraints:**
   - Technical constraints (systems, APIs, data limitations)
   - Business constraints (deadlines, budget, resources)
   - Process constraints (approval workflows, dependencies)
6. **Risk Assessment:**
   - Known risks and mitigation strategies
   - Unknowns requiring investigation
   - Open questions requiring stakeholder decisions
7. **Dependencies:** External systems, teams, or prerequisites.

#### Workflow Integration

**Trigger:** Manual invocation via CLI or GitHub Actions workflow.

**Command:**
```bash
python tools/planner_agent.py create "objective_name" \
  --description "Brief objective description"
```

**Process Flow:**
1. Agent creates initial objective document template.
2. **Manual Discussion Phase:**
   - Stakeholders review initial template.
   - Collaborative discussion to refine objectives, boundaries, and criteria.
   - Risk assessment and unknowns identification.
   - Consensus on success criteria.
3. Document is iteratively updated based on discussions.
4. **Approval Gate:** Stakeholders approve the objective definition.
5. Once approved, the document becomes the authoritative source for Step 2a.

**Next Step:** Only after approval → Proceed to **Step 2a: Pipeline Planner Agent**.

#### Dependency Handling

**Prerequisites:**
- None (Step 1 is the entry point for all new development work).

**Dependents:**
- Step 2a (Pipeline Planner Agent) depends on approved Step 1 output.
- All subsequent steps trace back to this objective definition.

**Dependency Rules:**
- No code changes are permitted without an approved Step 1 objective.
- Changes to the objective require re-validation of all downstream plans (Steps 2a, 2b).

#### Example Usage

**Scenario:** Define objective for vendor onboarding pipeline.

```bash
# Create initial objective document
python tools/planner_agent.py create "vendor_onboarding" \
  --description "Implement automated vendor onboarding pipeline"

# Output: docs/roadmaps/vendor_onboarding.md created
```

**Expected Output Structure:**
```markdown
# Objective: Vendor Onboarding

## Objective Statement
Implement an automated pipeline for onboarding new vendors into the PIM system...

## Expected Outcomes
- Vendors can submit product data via standardized format
- System validates and normalizes vendor data automatically
- Approved vendor products appear in PIM within 24 hours

## Out-of-Scope
- Manual vendor data entry (remains manual process)
- Historical vendor data migration (separate project)
- Vendor payment processing (handled by finance system)

## Success Criteria
### Functional Criteria
- [ ] Pipeline processes vendor submission files end-to-end
- [ ] Data validation rules reject invalid submissions with clear error messages
- [ ] Successful submissions create PIM records matching vendor data

### Quality Criteria
- [ ] Pipeline completes within 2-hour SLA for standard submissions
- [ ] 99% data accuracy for automated mappings
- [ ] Zero data loss during processing

## Constraints
### Technical
- Must integrate with existing PIM API (v2.1)
- S3 storage limits: 100GB per vendor submission
- AWS Glue 2.0 runtime environment

### Business
- Go-live date: Q2 2026
- Support for 3 vendor formats initially (Excel, CSV, JSON)
- Budget: $15K infrastructure costs

## Risk Assessment
### Known Risks
- Vendor data quality varies significantly (Mitigation: robust validation layer)
- PIM API rate limits may impact throughput (Mitigation: batch processing strategy)

### Unknowns
- TBD: Average vendor submission file size
- TBD: Expected vendor submission frequency
- OPEN QUESTION: Do we support real-time or batch processing?

## Dependencies
- PIM API access and documentation
- S3 bucket provisioning from DevOps team
- Vendor format specifications from business team
```

#### Manual Discussion Steps and Outputs

**Discussion Checkpoint 1: Initial Objective Review (Day 1)**
- **Participants:** Product Owner, Tech Lead, Business Stakeholders
- **Questions:**
  - Is the objective statement clear and aligned with business goals?
  - Are the expected outcomes realistic and measurable?
  - Are there additional out-of-scope items to document?
- **Output:** Refined objective statement and outcomes.

**Discussion Checkpoint 2: Success Criteria Definition (Day 2-3)**
- **Participants:** Tech Lead, QA Lead, Product Owner
- **Questions:**
  - Are success criteria testable and objective?
  - Do we have the data/tools to verify these criteria?
  - Are there missing quality or functional criteria?
- **Output:** Complete, testable success criteria list.

**Discussion Checkpoint 3: Risk and Constraint Review (Day 3-5)**
- **Participants:** Tech Lead, Architect, Business Analyst
- **Questions:**
  - Are all technical constraints documented?
  - What are the highest-priority unknowns?
  - Which open questions require immediate resolution?
- **Output:** Complete risk assessment with mitigation strategies and prioritized unknowns.

**Final Approval Checkpoint:**
- **Participants:** All stakeholders
- **Deliverable:** Signed-off objective definition ready for Step 2a.
- **Gate:** Document is locked and becomes the authoritative reference.

---

### 2. Pipeline Planner Agent (Step 2a: Overarching Plan / Pipeline-Level)

**Role:** Design the end-to-end pipeline plan showing processing sequence, decision points, and conceptual artifacts.

**Script Location:** `tools/pipeline_planner_agent.py`

**Workflow Position:** Step 2a of the 5-step workflow

#### Purpose and Responsibilities

The Pipeline Planner Agent creates the **overarching pipeline plan** that defines:
- **Processing Sequence:** Ordered list of capabilities/steps (first → last).
- **Decision Points:** Conditional logic and fallback paths.
- **Conceptual Artifacts:** Data artifacts exchanged between steps (by meaning, NOT storage details).
- **Existing Job Mapping:** Which existing jobs (if any) cover which pipeline steps.
- **Unknowns:** Explicitly marked unknowns and open decisions.

**Critical Rule:** Pipeline plans define **"what" and "sequence"**, NOT **"how"** each step works. Implementation details are deferred to Step 2b (Capability Plans).

The Pipeline Planner Agent facilitates **manual discussion** to ensure consensus on the pipeline architecture before detailed capability specifications are created.

#### Inputs

**Primary Input:** Approved Step 1 objective definition document.

**Required Reference:**
- File: `docs/roadmaps/<objective_name>.md` (from Step 1)

**Discussion Inputs:**
- Business process flow and sequencing requirements
- Decision logic and branching scenarios
- Existing job capabilities and reusability
- Data flow and artifact requirements

#### Outputs

**Primary Output:** Pipeline plan document at `docs/roadmaps/<objective_name>_pipeline_plan.md`

The pipeline plan must include:
1. **Processing Sequence:** Ordered list of capabilities/steps:
   ```
   Step 1: [Capability Name] → Step 2: [Capability Name] → ...
   ```
2. **Decision Points:** Conditional logic with fallback paths:
   ```
   If [condition], proceed to Step X
   Else, fallback to Step Y
   ```
3. **Conceptual Artifacts:** Data exchanged between steps:
   - **Artifact Name:** Descriptive name (e.g., "Validated Vendor Data")
   - **Meaning:** What the artifact represents (business context)
   - **Producer/Consumer:** Which steps create/consume it
   - **NOT included:** S3 paths, file formats, schemas (deferred to implementation)
4. **Existing Job Mapping:** 
   - Map existing jobs to pipeline steps where applicable
   - Mark gaps where new jobs are needed
5. **Unknowns and Open Decisions:**
   - Explicitly mark unknowns (TBD items)
   - Document open decisions requiring stakeholder input
   - NO assumptions presented as facts

#### Workflow Integration

**Trigger:** Manual invocation after Step 1 approval.

**Command:**
```bash
python tools/pipeline_planner_agent.py create "objective_name" \
  --objective-ref "objective_name.md"
```

**Process Flow:**
1. Agent reads approved Step 1 objective document.
2. Agent creates initial pipeline plan template.
3. **Manual Discussion Phase:**
   - Stakeholders review processing sequence.
   - Identify decision points and fallback paths.
   - Define conceptual artifacts and data flow.
   - Map existing jobs to pipeline steps.
   - Identify gaps requiring new capabilities.
4. Document is iteratively updated based on discussions.
5. **Approval Gate:** Stakeholders approve the pipeline plan.
6. Once approved, the document becomes the authoritative source for Step 2b.

**Next Step:** Only after approval → Proceed to **Step 2b: Capability Planner Agent** for EACH capability identified in the pipeline plan.

#### Dependency Handling

**Prerequisites:**
- **Required:** Approved Step 1 objective definition (`docs/roadmaps/<objective_name>.md`).
- **Validation:** Agent verifies Step 1 document exists before proceeding.

**Dependents:**
- Step 2b (Capability Planner Agent) depends on approved Step 2a pipeline plan.
- Each capability in the pipeline plan may require its own Step 2b specification.

**Dependency Rules:**
- Pipeline plan cannot be created without approved Step 1 objective.
- Changes to Step 1 objective require re-validation of Step 2a pipeline plan.
- Step 2b capability plans must reference the Step 2a pipeline plan.

#### Example Usage

**Scenario:** Create pipeline plan for vendor onboarding objective.

```bash
# Create pipeline plan (requires approved Step 1)
python tools/pipeline_planner_agent.py create "vendor_onboarding" \
  --objective-ref "vendor_onboarding.md"

# Output: docs/roadmaps/vendor_onboarding_pipeline_plan.md created
```

**Expected Output Structure:**
```markdown
# Pipeline Plan: Vendor Onboarding

**Objective Reference:** `docs/roadmaps/vendor_onboarding.md`

## Processing Sequence

1. **Data Ingestion** → 2. **Data Validation** → 3. **Data Normalization** → 4. **PIM Integration** → 5. **Notification**

## Detailed Step Descriptions

### Step 1: Data Ingestion
**Purpose:** Receive and stage vendor submission files.
**Input:** Vendor submission files (various formats).
**Output:** Staged raw data artifacts.

### Step 2: Data Validation
**Purpose:** Validate vendor data against business rules.
**Input:** Staged raw data artifacts.
**Output:** Validation report + validated data artifacts.
**Decision Point:** If validation fails → trigger notification and halt.

### Step 3: Data Normalization
**Purpose:** Transform vendor data to PIM schema.
**Input:** Validated data artifacts.
**Output:** Normalized PIM-ready data artifacts.

### Step 4: PIM Integration
**Purpose:** Load normalized data into PIM system.
**Input:** Normalized PIM-ready data artifacts.
**Output:** PIM record IDs.
**Decision Point:** If PIM API fails → retry with exponential backoff (3 attempts), then fallback to manual queue.

### Step 5: Notification
**Purpose:** Notify vendor and stakeholders of processing results.
**Input:** Processing status (success/failure) + PIM record IDs (if success).
**Output:** Email notifications.

## Conceptual Artifacts

### 1. Vendor Submission File
- **Meaning:** Raw data submitted by vendor (product catalog, pricing, inventory).
- **Producer:** External vendor.
- **Consumer:** Data Ingestion (Step 1).

### 2. Staged Raw Data
- **Meaning:** Unprocessed vendor data stored for validation.
- **Producer:** Data Ingestion (Step 1).
- **Consumer:** Data Validation (Step 2).

### 3. Validation Report
- **Meaning:** List of validation errors/warnings with row-level details.
- **Producer:** Data Validation (Step 2).
- **Consumer:** Notification (Step 5) + manual review queue.

### 4. Validated Data
- **Meaning:** Vendor data confirmed to meet business rules.
- **Producer:** Data Validation (Step 2).
- **Consumer:** Data Normalization (Step 3).

### 5. Normalized PIM-Ready Data
- **Meaning:** Vendor data transformed to PIM schema format.
- **Producer:** Data Normalization (Step 3).
- **Consumer:** PIM Integration (Step 4).

### 6. PIM Record IDs
- **Meaning:** Unique identifiers for created/updated PIM records.
- **Producer:** PIM Integration (Step 4).
- **Consumer:** Notification (Step 5).

## Decision Points

### Decision 1: Validation Pass/Fail
- **Condition:** Data passes all validation rules?
- **Pass:** Proceed to Step 3 (Data Normalization).
- **Fail:** Skip to Step 5 (Notification) with failure status.

### Decision 2: PIM API Success/Retry/Fail
- **Condition:** PIM API responds successfully?
- **Success:** Proceed to Step 5 (Notification) with success status.
- **Transient Error:** Retry with exponential backoff (3 attempts max).
- **Permanent Failure:** Route to manual queue + notify stakeholders.

## Existing Job Mapping

| Pipeline Step | Existing Job | Status | Notes |
|---------------|--------------|--------|-------|
| Data Ingestion | `s3_file_intake_job` | ✅ Exists | Supports CSV, JSON, Excel |
| Data Validation | — | ❌ New | Needs creation |
| Data Normalization | `vendor_to_pim_mapper_v2` | ⚠️ Partial | Requires enhancement for new vendor formats |
| PIM Integration | `pim_batch_loader` | ✅ Exists | Requires configuration update |
| Notification | `email_notification_job` | ✅ Exists | Reusable as-is |

## Unknowns and Open Decisions

### Unknowns (TBD)
- **TBD:** Maximum vendor file size and processing time SLA.
- **TBD:** Frequency of vendor submissions (real-time vs. batch).
- **TBD:** Retention policy for staged raw data.

### Open Decisions (Require Stakeholder Input)
- **OPEN:** Should we support real-time processing or daily batch?
- **OPEN:** What is the retry strategy for PIM API failures?
- **OPEN:** Do we archive validation failure data for audit?

## Next Steps

1. Resolve open decisions with stakeholders.
2. Create Step 2b capability plans for:
   - Data Validation (new capability)
   - Data Normalization enhancements
3. Reuse existing jobs: Data Ingestion, PIM Integration, Notification.
```

#### Manual Discussion Steps and Outputs

**Discussion Checkpoint 1: Processing Sequence Review (Day 1)**
- **Participants:** Tech Lead, Architect, Business Analyst
- **Questions:**
  - Is the processing sequence logical and complete?
  - Are there missing steps in the pipeline?
  - Does the sequence align with business process flow?
- **Output:** Validated processing sequence.

**Discussion Checkpoint 2: Decision Points and Fallback Paths (Day 2)**
- **Participants:** Tech Lead, Product Owner, DevOps
- **Questions:**
  - What are the critical decision points?
  - What fallback/retry strategies are needed?
  - How do we handle failure scenarios?
- **Output:** Complete decision logic with fallback paths.

**Discussion Checkpoint 3: Conceptual Artifacts Definition (Day 3)**
- **Participants:** Tech Lead, Data Architect, Business Analyst
- **Questions:**
  - What data artifacts are exchanged between steps?
  - What does each artifact represent (business meaning)?
  - Which steps produce/consume each artifact?
- **Output:** Complete conceptual artifacts catalog.

**Discussion Checkpoint 4: Existing Job Mapping (Day 4)**
- **Participants:** Tech Lead, Development Team
- **Questions:**
  - Which existing jobs can be reused?
  - Which jobs require enhancement?
  - Which capabilities require new jobs?
- **Output:** Job mapping table with reuse/gap analysis.

**Discussion Checkpoint 5: Unknowns and Open Decisions Resolution (Day 5)**
- **Participants:** All stakeholders
- **Questions:**
  - Which unknowns can be resolved now?
  - Which open decisions require immediate resolution?
  - Which decisions can be deferred to Step 2b?
- **Output:** Prioritized unknowns and decision resolution plan.

**Final Approval Checkpoint:**
- **Participants:** All stakeholders
- **Deliverable:** Signed-off pipeline plan ready for Step 2b.
- **Gate:** Document is locked and becomes the authoritative reference for capability planning.

---

### 3. Capability Planner Agent (Step 2b: Capability Plan / Step-Level)

**Role:** Create detailed capability specifications for individual pipeline steps, defining inputs, outputs, business rules, and acceptance criteria.

**Script Location:** `tools/capability_planner_agent.py`

**Workflow Position:** Step 2b of the 5-step workflow

#### Purpose and Responsibilities

The Capability Planner Agent creates **detailed capability specifications** for ONE capability/step from the approved pipeline plan. It defines:
- **Inputs/Outputs:** By MEANING (conceptual), NOT storage details (S3 paths, formats).
- **Business Rules and Logic:** Rules that must be enforced by this capability.
- **Acceptance Criteria:** Testable functional and quality criteria.
- **Boundaries:** Explicitly state what this capability does and does NOT do.
- **Dependencies:** Upstream capabilities (data producers), downstream consumers, external systems.

**Critical Rule:** Capability plans define inputs/outputs by **meaning** (what the data represents), NOT by implementation details (S3 locations, file formats, schemas). Storage details are deferred to Step 3-5 (implementation).

The Capability Planner Agent facilitates **manual discussion** to ensure consensus on each capability's scope, logic, and boundaries before decomposition and implementation.

#### Inputs

**Primary Input:** Approved Step 2a pipeline plan document.

**Required Reference:**
- File: `docs/roadmaps/<objective_name>_pipeline_plan.md` (from Step 2a)

**Discussion Inputs:**
- Specific capability/step from pipeline plan to detail
- Business rules and validation logic
- Input/output requirements by meaning
- Acceptance criteria and quality requirements
- Boundary definitions (what is/isn't included)

#### Outputs

**Primary Output:** Capability specification document at `docs/specifications/<capability_name>_capability.yaml`

The capability specification must include:
1. **Capability Name and Description:** Clear, concise capability name and purpose.
2. **Pipeline Reference:** Link to Step 2a pipeline plan and specific step.
3. **Inputs (by Meaning):**
   - Input name (conceptual artifact name from pipeline plan)
   - Business meaning (what the input represents)
   - Producer (which upstream step creates this input)
   - Required vs. optional
4. **Outputs (by Meaning):**
   - Output name (conceptual artifact name from pipeline plan)
   - Business meaning (what the output represents)
   - Consumer (which downstream step uses this output)
   - Success vs. failure outputs
5. **Business Rules and Logic:**
   - Validation rules
   - Transformation logic
   - Decision criteria
   - Error handling rules
6. **Acceptance Criteria:**
   - Functional criteria (what must work)
   - Quality criteria (performance, accuracy, reliability)
   - Testable, verifiable criteria
7. **Boundaries:**
   - **What this capability DOES:** Explicit scope.
   - **What this capability does NOT do:** Out-of-scope items.
8. **Dependencies:**
   - Upstream capabilities (data producers)
   - Downstream capabilities (data consumers)
   - External systems (APIs, databases, services)
9. **Unknowns:** Explicitly marked unknowns requiring resolution.

#### Workflow Integration

**Trigger:** Manual invocation after Step 2a approval, once per capability.

**Command:**
```bash
python tools/capability_planner_agent.py create "capability_name" \
  --pipeline-ref "objective_name_pipeline_plan.md"
```

**Process Flow:**
1. Agent reads approved Step 2a pipeline plan.
2. Agent creates initial capability specification template for the specified capability.
3. **Manual Discussion Phase:**
   - Stakeholders review inputs/outputs (by meaning).
   - Define business rules and validation logic.
   - Establish acceptance criteria.
   - Explicitly define boundaries (in-scope vs. out-of-scope).
   - Identify dependencies and unknowns.
4. Document is iteratively updated based on discussions.
5. **Approval Gate:** Stakeholders approve the capability specification.
6. Once approved, the document becomes the authoritative source for Step 3 (Decomposition).

**Next Step:** Only after approval → Proceed to **Step 3: Decompose into Development Elements** for this capability.

**Iteration:** Repeat Step 2b for EACH capability identified in the Step 2a pipeline plan.

#### Dependency Handling

**Prerequisites:**
- **Required:** Approved Step 2a pipeline plan (`docs/roadmaps/<objective_name>_pipeline_plan.md`).
- **Required:** Step 1 objective definition (transitively through Step 2a).
- **Validation:** Agent verifies Step 2a document exists and references the capability.

**Dependents:**
- Step 3 (Decomposition) depends on approved Step 2b capability specification.
- Subsequent implementation (Steps 4-5) requires this capability specification.

**Dependency Rules:**
- Capability plan cannot be created without approved Step 2a pipeline plan.
- Changes to Step 2a pipeline plan require re-validation of affected Step 2b capability plans.
- Multiple Step 2b capability plans may be created for different capabilities in the same pipeline.

#### Example Usage

**Scenario:** Create capability plan for "Data Validation" step from vendor onboarding pipeline.

```bash
# Create capability plan (requires approved Step 2a)
python tools/capability_planner_agent.py create "data_validation" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"

# Output: docs/specifications/data_validation_capability.yaml created
```

**Expected Output Structure:**
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
      formats (CSV, JSON, Excel) and has not been validated.

outputs:
  - name: validation_report
    meaning: Detailed report of validation errors, warnings, and data quality issues
    consumer: notification (Step 5), manual_review_queue
    type: always_produced
    business_context: |
      Row-level validation results indicating which data elements passed/failed
      business rules. Includes error codes, error messages, and suggested fixes.
  
  - name: validated_data
    meaning: Vendor data confirmed to meet all business rules and quality standards
    consumer: data_normalization (Step 3)
    type: produced_on_success
    business_context: |
      Subset of staged raw data that passed all validation rules. Ready for
      transformation to PIM schema. Only produced if validation succeeds.

business_rules:
  - rule_id: VR-001
    description: SKU uniqueness check
    logic: Each vendor SKU must be unique within the submission
    error_handling: Reject entire submission if duplicate SKUs found
  
  - rule_id: VR-002
    description: Required field validation
    logic: Product name, SKU, price, and category are mandatory fields
    error_handling: Mark row as invalid; allow partial submission processing
  
  - rule_id: VR-003
    description: Price range validation
    logic: Price must be positive number between $0.01 and $999,999.99
    error_handling: Mark row as invalid with out-of-range error
  
  - rule_id: VR-004
    description: Category mapping validation
    logic: Vendor category must map to valid PIM category
    error_handling: Flag for manual review if no mapping exists
  
  - rule_id: VR-005
    description: Data completeness check
    logic: At least 80% of rows must pass validation for submission to proceed
    error_handling: Reject entire submission if below 80% pass rate

acceptance_criteria:
  functional:
    - criterion: Validates all required fields per business rules
      verification: Test with sample data missing required fields
    - criterion: Detects duplicate SKUs within submission
      verification: Test with intentionally duplicated SKU data
    - criterion: Produces detailed validation report with row-level errors
      verification: Verify report contains error codes, messages, and row IDs
    - criterion: Only passes validated data to downstream step
      verification: Confirm invalid rows are excluded from validated_data output
  
  quality:
    - criterion: Processes 10,000 row submission within 5 minutes
      verification: Performance test with 10K row sample file
    - criterion: Validation accuracy ≥99.9% (no false positives/negatives)
      verification: Compare validation results against manual review baseline
    - criterion: Zero data loss during validation processing
      verification: Row count in = row count in validation report

boundaries:
  in_scope:
    - Validate data against defined business rules
    - Generate detailed validation reports with row-level errors
    - Pass validated data to normalization step
    - Reject submissions below quality threshold (80% pass rate)
  
  out_of_scope:
    - Data transformation or normalization (handled by Step 3)
    - Direct PIM integration (handled by Step 4)
    - Vendor notification (handled by Step 5)
    - Historical data validation (current submissions only)
    - Category mapping creation (use existing mappings only)

dependencies:
  upstream:
    - capability: data_ingestion
      dependency_type: data_producer
      artifact: staged_raw_data
      notes: Requires standardized staging format from ingestion step
  
  downstream:
    - capability: data_normalization
      dependency_type: data_consumer
      artifact: validated_data
      notes: Normalization expects validated data only
    
    - capability: notification
      dependency_type: data_consumer
      artifact: validation_report
      notes: Notification uses report for vendor communication
  
  external_systems:
    - system: PIM Category Mapping Service
      purpose: Validate vendor categories against PIM taxonomy
      api_endpoint: TBD
      authentication: TBD
      notes: Required for VR-004 rule enforcement

unknowns:
  - id: UNK-001
    description: PIM Category Mapping Service API endpoint and authentication
    impact: Cannot implement VR-004 rule without this information
    resolution_target: Before Step 3 decomposition
  
  - id: UNK-002
    description: Expected average submission file size
    impact: Affects performance testing baseline and infrastructure sizing
    resolution_target: Before Step 5 implementation
  
  - id: UNK-003
    description: Vendor notification preferences (email vs. API callback)
    impact: May affect validation report format requirements
    resolution_target: Before Step 3 decomposition
```

#### Manual Discussion Steps and Outputs

**Discussion Checkpoint 1: Input/Output Definition (Day 1)**
- **Participants:** Tech Lead, Data Architect, Business Analyst
- **Questions:**
  - What inputs does this capability consume (by meaning)?
  - What outputs does this capability produce (by meaning)?
  - What is the business context for each input/output?
  - Which capabilities produce inputs? Which consume outputs?
- **Output:** Complete inputs/outputs specification (conceptual, not storage).

**Discussion Checkpoint 2: Business Rules and Logic (Day 2-3)**
- **Participants:** Business Analyst, Product Owner, Tech Lead
- **Questions:**
  - What validation rules must this capability enforce?
  - What transformation logic is required?
  - How should errors be handled?
  - What are the pass/fail criteria?
- **Output:** Complete business rules catalog with error handling.

**Discussion Checkpoint 3: Acceptance Criteria Definition (Day 3-4)**
- **Participants:** QA Lead, Tech Lead, Product Owner
- **Questions:**
  - What functional criteria must be met?
  - What quality criteria (performance, accuracy) apply?
  - How will each criterion be verified/tested?
- **Output:** Testable acceptance criteria with verification methods.

**Discussion Checkpoint 4: Boundaries and Scope (Day 4)**
- **Participants:** Tech Lead, Architect, Product Owner
- **Questions:**
  - What is explicitly in-scope for this capability?
  - What is explicitly out-of-scope?
  - Are there gray areas requiring clarification?
- **Output:** Clear boundary definitions preventing scope creep.

**Discussion Checkpoint 5: Dependencies and Unknowns (Day 5)**
- **Participants:** Tech Lead, Integration Architect, DevOps
- **Questions:**
  - What upstream capabilities does this depend on?
  - What downstream capabilities consume our outputs?
  - What external systems are required?
  - What unknowns must be resolved before implementation?
- **Output:** Complete dependency map and prioritized unknowns list.

**Final Approval Checkpoint:**
- **Participants:** All stakeholders
- **Deliverable:** Signed-off capability specification ready for Step 3 decomposition.
- **Gate:** Document is locked and becomes the authoritative reference for implementation.

---

## Summary: Planning Phase Workflow (Steps 1–2)

The planning phase ensures **no code is written until consensus is achieved** on objectives, pipeline architecture, and capability specifications. This prevents rework, scope creep, and implementation misalignment.

### Workflow Sequence

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Define Objective (Planner Agent)           │
│ Output: docs/roadmaps/<objective>.md                │
│ Manual Discussion → Approval Required               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2a: Pipeline Plan (Pipeline Planner Agent)    │
│ Output: docs/roadmaps/<objective>_pipeline_plan.md  │
│ Manual Discussion → Approval Required               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2b: Capability Plan (Capability Planner Agent)│
│ Output: docs/specifications/<capability>.yaml       │
│ Manual Discussion → Approval Required               │
│ Repeat for EACH capability in pipeline plan        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: Decompose into Development Elements        │
│ (Coding Agent - outside scope of this document)    │
└─────────────────────────────────────────────────────┘
```

### Key Principles

1. **Sequential Execution:** Each step must complete and receive approval before the next begins.
2. **Manual Oversight:** AI agents assist but humans make final decisions at each checkpoint.
3. **Evidence-Based Planning:** Reference existing jobs, mark unknowns explicitly, no assumptions.
4. **Explicit Boundaries:** At every level, clearly define what IS and is NOT included.
5. **Defer Implementation Details:** Storage paths, formats, schemas come later in Steps 3-5.

### Transition to Implementation

Once all required capability plans (Step 2b) are approved:
- **Proceed to Step 3:** Decompose each capability into PR-sized development elements.
- **Authority Chain:** Step 1 → Step 2a → Step 2b documents form the authoritative specification chain.
- **Change Management:** Changes to any planning document require re-validation of dependent documents.

---

## See Also

- `WORKFLOW_5_STEPS.md` — Complete 5-step workflow documentation
- `docs/context_packs/system_context.md` — Repository context and structure
- `AGENTS_SETUP.md` — Agent installation and usage guide
- `docs/standards/` — Repository standards and specifications
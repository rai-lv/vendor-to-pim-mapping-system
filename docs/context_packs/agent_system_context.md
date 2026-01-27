# Agent System Context — AI-Assisted Development Workflow

## Overview
This document defines and describes the roles, responsibilities, workflows, and outputs of the agents that assist in the development workflow for the `vendor-to-pim-mapping-system` repository. It ensures alignment between the agent-assisted approach, the broader system context (defined in `system_context.md`), and repository-wide standards.

**Key Principle**: Agents are **collaborators, not autonomous actors**. Their role is to assist in refining outputs based on human feedback, automate repetitive tasks, and enhance human decision-making rather than replace it.

The agent workflows are structured to support the 5-step development process outlined in `docs/workflows/WORKFLOW_5_STEPS.md`, with mandatory human oversight and approval at each critical stage.

---

## Objectives of the Agent System
The agent system is designed to:
- **Assist humans** in streamlining the development workflow through selective automation of well-defined tasks.
- **Support human decision-making** with structured drafts and proposals at each stage.
- Maintain mandatory **manual oversight** during critical planning phases (Steps 1–2b).
- Enforce repository standards via automated quality gates, **subject to human review**.
- Propose documentation updates as tasks evolve, **requiring human approval before integration**.
- Provide modular, self-contained scripts that **support** specific roles in the workflow.

---

## Human Oversight and Governance Principles

This agent system operates under strict governance principles aligned with `development_approach.md`:

### Core Governance Principles

1. **Human-Agent Collaboration**
   - Agents are **collaborators, not autonomous actors**
   - Agents **assist** in refining outputs based on human feedback
   - Agents **automate** repetitive tasks to enhance, not replace, human decision-making
   - Collaboration is a **feedback loop** where agents iteratively improve outputs with human guidance

2. **Mandatory Manual Checkpoints**
   - **Every planning step (Steps 1, 2a, 2b)** requires explicit human approval before progression
   - Humans provide feedback, refine decisions, and validate results at each stage
   - No automated progression between major workflow stages
   - Manual sign-off captured in planning artifacts (objectives, pipeline plans, capability specs)

3. **Governance Hierarchy**
   - **Human-defined inputs** and validated objectives take precedence over all agent outputs
   - **Repository standards and criteria** guide all agent proposals
   - **Automated agent outputs** remain subordinate to human-defined rules and validations
   - Agent proposals require human validation before becoming authoritative

4. **Balance of Automation and Oversight**
   - Automation enforces standards, consistency, and efficiency for **well-defined tasks**
   - Human judgment provides critical oversight for **open-ended, high-stakes, or creative decisions**
   - Automation **complements** human intelligence; it never bypasses or replaces it

### Approval Gates

| Stage | Agent Role | Human Approval Required | Documentation |
|-------|-----------|-------------------------|---------------|
| **Step 1** | Planner Agent proposes objective | ✅ Explicit approval | Captured in `docs/roadmaps/<objective>.md` |
| **Step 2a** | Pipeline Planner proposes architecture | ✅ Explicit approval | Captured in `docs/roadmaps/<objective>_pipeline_plan.md` |
| **Step 2b** | Capability Planner proposes specification | ✅ Explicit approval | Captured in `docs/specifications/<capability>.yaml` |
| **Step 3** | Coding Agent proposes decomposition | ✅ Review and approval | Reviewed before task creation |
| **Step 4** | Coding Agent proposes Codex tasks | ✅ Review and approval | Reviewed before PR creation |
| **Step 5** | Testing/Documentation Agents propose results | ✅ Review before merge | PR review process |

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
3. **Explicit Unknowns and Assumptions:** All unknowns must be explicitly marked as TBD; assumptions must be explicitly labeled and require human approval before being used as planning inputs.
4. **Evidence-Based:** Plans must reference existing code/jobs where applicable and mark unknowns explicitly.

---

## Agent Roles — Planning Agents (Steps 1–2)

### 1. Planner Agent (Step 1: Define Objective)

**Role:** Assist humans in defining business objectives with explicit boundaries, testable success criteria, and risk assessment.

**Script Location:** `tools/planner_agent.py`

**Workflow Position:** Step 1 of the 5-step workflow

#### Purpose and Responsibilities

The Planner Agent **assists** in creating structured objective definitions that answer:
- **What must be achieved?** Specific, measurable goals and expected outcomes.
- **What is out-of-scope?** Explicit boundaries preventing scope creep.
- **How do we know we succeeded?** Testable functional and quality criteria.
- **What are the constraints?** Technical, business, time, and resource limitations.
- **What are the risks?** Known risks, unknowns, and open questions requiring resolution.

The Planner Agent **facilitates and supports** manual discussion between stakeholders to ensure consensus on objectives before any design or implementation work begins. **Humans make final decisions and provide explicit approval.**

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
1. Agent **proposes** initial objective document template.
2. **Manual Discussion Phase (Human-Led):**
   - Stakeholders review agent-generated template.
   - Collaborative discussion to refine objectives, boundaries, and criteria.
   - Risk assessment and unknowns identification.
   - Consensus on success criteria.
   - Humans provide feedback; agent iterates on drafts.
3. Document is iteratively updated based on **human feedback and direction**.
4. **Approval Gate (Human Decision):** Stakeholders explicitly approve the objective definition.
5. Once approved by humans, the document becomes the authoritative source for Step 2a.

**Next Step:** Only after **human approval** → Proceed to **Step 2a: Pipeline Planner Agent**.

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

**Role:** Assist humans in designing the end-to-end pipeline plan showing processing sequence, decision points, and conceptual artifacts.

**Script Location:** `tools/pipeline_planner_agent.py`

**Workflow Position:** Step 2a of the 5-step workflow

#### Purpose and Responsibilities

The Pipeline Planner Agent **assists in creating** the **overarching pipeline plan** that defines:
- **Processing Sequence:** Ordered list of capabilities/steps (first → last).
- **Decision Points:** Conditional logic and fallback paths.
- **Conceptual Artifacts:** Data artifacts exchanged between steps (by meaning, NOT storage details).
- **Existing Job Mapping:** Which existing jobs (if any) cover which pipeline steps.
- **Unknowns:** Explicitly marked unknowns and open decisions.

**Critical Rule:** Pipeline plans define **"what" and "sequence"**, NOT **"how"** each step works. Implementation details are deferred to Step 2b (Capability Plans).

The Pipeline Planner Agent **facilitates and supports** manual discussion to ensure consensus on the pipeline architecture before detailed capability specifications are created. **Humans make final architectural decisions and provide explicit approval.**

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
   - Explicitly label any assumptions and flag them for human approval

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

**Role:** Assist humans in creating detailed capability specifications for individual pipeline steps, defining inputs, outputs, business rules, and acceptance criteria.

**Script Location:** `tools/capability_planner_agent.py`

**Workflow Position:** Step 2b of the 5-step workflow

#### Purpose and Responsibilities

The Capability Planner Agent **assists in creating** detailed capability specifications for ONE capability/step from the approved pipeline plan. It helps define:
- **Inputs/Outputs:** By MEANING (conceptual), NOT storage details (S3 paths, formats).
- **Business Rules and Logic:** Rules that must be enforced by this capability.
- **Acceptance Criteria:** Testable functional and quality criteria.
- **Boundaries:** Explicitly state what this capability does and does NOT do.
- **Dependencies:** Upstream capabilities (data producers), downstream consumers, external systems.

**Critical Rule:** Capability plans define inputs/outputs by **meaning** (what the data represents), NOT by implementation details (S3 locations, file formats, schemas). Storage details are deferred to Step 3-5 (implementation).

The Capability Planner Agent **facilitates and supports** manual discussion to ensure consensus on each capability's scope, logic, and boundaries before decomposition and implementation. **Humans make final specification decisions and provide explicit approval.**

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

**Primary Output:** Capability specification document at `docs/specifications/<capability_name>.yaml`

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

# Output: docs/specifications/data_validation.yaml created
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
3. **Evidence-Based Planning:** Reference existing jobs, mark unknowns explicitly as TBD, label assumptions explicitly for human approval.
4. **Explicit Boundaries:** At every level, clearly define what IS and is NOT included.
5. **Defer Implementation Details:** Storage paths, formats, schemas come later in Steps 3-5.

### Transition to Implementation

Once all required capability plans (Step 2b) are approved:
- **Proceed to Step 3:** Decompose each capability into PR-sized development elements.
- **Authority Chain:** Step 1 → Step 2a → Step 2b documents form the authoritative specification chain.
- **Change Management:** Changes to any planning document require re-validation of dependent documents.

---

## Agent Roles — Implementation Agents (Steps 3–5)

### 4. Coding Agent (Steps 3–4: Decompose and Create Codex Tasks)

**Role:** Assist humans in decomposing approved capability plans into PR-sized development elements and generating Codex task specifications with quality gates.

**Script Location:** `tools/coding_agent.py`

**Workflow Position:** Steps 3 and 4 of the 5-step workflow

#### Purpose and Responsibilities

The Coding Agent **assists** in bridging the gap between planning (Steps 1–2) and implementation (Step 5) by:
- **Step 3: Decompose Capability** — **Proposing** breakdown of approved capability plans into small, PR-sized development elements **for human review and approval**
- **Step 4: Create Codex Tasks** — **Generating draft** Codex task specifications with standards references, file restrictions, and quality gates **for human validation**

**Critical Rules:**
- Each development element must be completable in ONE pull request
- File changes must be explicitly restricted (allowed file list)
- All tasks must reference relevant repository standards
- Quality gates (validation, syntax checks) must be defined
- Acceptance criteria must be testable from repository contents
- **Human approval required** before proceeding to PR creation

#### Inputs

**Primary Input (Step 3):** Approved Step 2b capability specification

**Required Reference:**
- File: `docs/specifications/<capability_name>.yaml` (from Step 2b)

**Primary Input (Step 4):** Development element definition from Step 3

#### Outputs

**Step 3 Output:** Development elements decomposition (printed to console)
- List of PR-sized development elements
- File paths to be modified/created for each element
- Acceptance criteria per element
- Dependencies between elements

**Step 4 Output:** Codex task specification (printed to console)
- Objective and capability reference
- Standards compliance requirements
- Explicit file restrictions (allowed file list)
- Implementation requirements from capability plan
- Acceptance criteria (element-specific and from capability)
- Quality gates that must pass
- Testing strategy
- Boundaries (what element does NOT do)

#### Workflow Integration

**Trigger:** Manual invocation after Step 2b approval (for Step 3) or after decomposition (for Step 4)

**Step 3 Command:**
```bash
python tools/coding_agent.py decompose data_validation_capability
```

**Step 4 Command:**
```bash
python tools/coding_agent.py codex-task data_validation_capability 1
```

**Additional Commands:**
```bash
# Validate repository code and documentation
python tools/coding_agent.py validate

# Check best practices (TODO comments, duplicate code)
python tools/coding_agent.py check
```

**Process Flow (Step 3):**
1. Agent reads approved Step 2b capability specification
2. Agent suggests development elements based on:
   - High-level processing steps from capability plan
   - Infrastructure elements (manifest, documentation)
   - Dependencies between elements
3. Developer reviews and adjusts decomposition
4. Each element is defined with:
   - Target repository paths (exact files)
   - Allowed changes (explicit file restrictions)
   - Acceptance criteria (testable from repo)
   - Dependencies on other elements

**Process Flow (Step 4):**
1. For each development element from Step 3
2. Agent generates Codex task specification including:
   - Capability objective and element scope
   - Standards references (naming, manifest, documentation specs)
   - Explicit file restrictions (allowed list)
   - Implementation requirements from capability plan
   - Acceptance criteria
   - Quality gates (must pass before PR merge)
   - Testing strategy
3. Developer uses Codex task specification to create PR
4. PR must pass all quality gates before merge

**Next Step:** After Codex tasks are defined → Proceed to **Step 5: Execute PR** (implementation by developer or Codex)

#### Dependency Handling

**Prerequisites:**
- **Required (Step 3):** Approved Step 2b capability specification
- **Required (Step 4):** Completed Step 3 decomposition

**Validation:**
- Step 3: Verifies capability specification exists and is valid YAML
- Step 4: Uses decomposition from Step 3 output

**Quality Gates:**
- Repository validation: `python tools/validate_repo_docs.py --all`
- Python syntax check: `python -m py_compile <script>`
- Best practices check: `python tools/coding_agent.py check`

#### Example Usage

**Scenario:** Decompose "data_validation" capability and create Codex task for first element.

```bash
# Step 3: Decompose capability into development elements
python tools/coding_agent.py decompose data_validation_capability

# Output: Suggested development elements with file restrictions and criteria
# Review and adjust as needed

# Step 4: Generate Codex task for element 1 (core validation logic)
python tools/coding_agent.py codex-task data_validation_capability 1

# Output: Codex task specification with standards, restrictions, quality gates

# Validate before starting implementation
python tools/coding_agent.py validate

# Check best practices
python tools/coding_agent.py check
```

**Expected Step 3 Output (Console):**
```
# Step 3: Decompose Capability into Development Elements
================================================================================

Capability: data_validation

## Suggested Development Elements

### Element 1: Core Validation Logic
**Target Repo Paths:**
- jobs/vendor_onboarding/validate_vendor_data/glue_script.py

**Allowed Changes:**
- Create jobs/vendor_onboarding/validate_vendor_data/glue_script.py
- Create jobs/vendor_onboarding/validate_vendor_data/ directory structure

**Acceptance Criteria:**
- Script implements all business rules from capability plan (VR-001 to VR-005)
- Script produces validation_report and validated_data outputs
- Python syntax is valid
- Passes repository validation

### Element 2: Job Manifest
**Target Repo Paths:**
- jobs/vendor_onboarding/validate_vendor_data/job_manifest.yaml

**Allowed Changes:**
- Create job_manifest.yaml only
- Must follow manifest spec: docs/standards/job_manifest_spec.md

**Acceptance Criteria:**
- Manifest validates with: python tools/validate_repo_docs.py --all
- Uses ${PLACEHOLDER} style for parameter substitution
- All inputs/outputs from capability plan are represented

### Element 3: Documentation
**Target Repo Paths:**
- docs/script_cards/validate_vendor_data.md
- docs/business_job_descriptions/validate_vendor_data.md

**Allowed Changes:**
- Create documentation files only
- Must follow specs in docs/standards/

**Acceptance Criteria:**
- Documentation validates with: python tools/validate_repo_docs.py --all
- Aligns with capability plan objectives and acceptance criteria
```

**Expected Step 4 Output (Console):**
```markdown
# Step 4: Codex Task - Element 1
================================================================================

**Capability:** data_validation
**Element ID:** 1

## Objective

Implement Element 1 from the decomposed capability plan.
Capability objective: Validate vendor submission data against business rules

## Standards References

This implementation MUST comply with the following standards:

- `docs/standards/naming-standard.md`
- `docs/standards/job_manifest_spec.md`
- `docs/standards/script_card_spec.md`

## Target Script/Path (Explicit)

**TARGET_SCRIPT:** `jobs/vendor_onboarding/validate_vendor_data/glue_script.py`

## File Restrictions (Explicit)

ONLY the following files may be created or modified:

**Allowed file list:**
- jobs/vendor_onboarding/validate_vendor_data/glue_script.py
- jobs/vendor_onboarding/validate_vendor_data/__init__.py (if needed)

**Forbidden:**
- Any file not in the allowed list above
- Existing code that works correctly

## Implementation Requirements

### From Capability Plan

**Required Inputs:**
- staged_raw_data: Unprocessed vendor data staged for validation

**Expected Outputs:**
- validation_report: Detailed report of validation errors
- validated_data: Vendor data confirmed to meet business rules

**Business Rules to Enforce:**
- VR-001: SKU uniqueness check
- VR-002: Required field validation
- VR-003: Price range validation
- VR-004: Category mapping validation
- VR-005: Data completeness check

## Acceptance Criteria

**Functional:**
- [ ] Validates all required fields per business rules
- [ ] Detects duplicate SKUs within submission
- [ ] Produces detailed validation report with row-level errors

**Quality:**
- [ ] Processes 10,000 row submission within 5 minutes
- [ ] Validation accuracy ≥99.9%

## Quality Gates (Must Pass)

```bash
# Repository validation
python tools/validate_repo_docs.py --all

# Python syntax check
python -m py_compile jobs/vendor_onboarding/validate_vendor_data/glue_script.py

# Best practices check
python tools/coding_agent.py check
```

## Boundaries (What This Element Does NOT Do)

- Data transformation or normalization (handled by other elements)
- Direct PIM integration (handled by other jobs)
```

---

### 5. Testing Agent (Validation and Testing)

**Role:** Assist humans in validating code contributions through automated testing, syntax checking, and specification-based test inference, **with results subject to human review and approval**.

**Script Location:** `tools/testing_agent.py`

**Workflow Position:** Step 5 (PR execution) and continuous validation

#### Purpose and Responsibilities

The Testing Agent **assists** in ensuring code quality and adherence to specifications by:
- Running repository-wide validation tests
- Checking Python and YAML syntax
- Inferring test requirements from capability specifications
- **Generating test reports for human review**
- Providing pre-commit and CI validation results

**Critical Rules:**
- All tests must pass before PR merge
- Test failures must be logged with timestamps
- Specification-based tests are derived from acceptance criteria
- Validation includes standards compliance
- **Human review and approval of test results required before progression**

#### Inputs

**Primary Inputs:**
- Repository code (Python scripts in `jobs/` directory)
- YAML files (manifests in `jobs/`, specifications in `docs/specifications/`)
- Optional: Capability specification for test inference

**Validation Script:**
- Uses `tools/validate_repo_docs.py` for standards validation

#### Outputs

**Console Output:**
- Test execution results (pass/fail)
- Summary of passed and failed tests
- Detailed error messages for failures

**Log File Output:**
- Written to: `logs/tests_logs/test_run_<timestamp>.log`
- Contains: Test run timestamp, all test results, summary

#### Workflow Integration

**Trigger:** 
- Manual invocation before committing code
- Automated execution in CI pipeline
- On-demand for specification validation

**Commands:**
```bash
# Run full test suite
python tools/testing_agent.py run

# Run tests for specific specification
python tools/testing_agent.py run --spec data_validation_capability

# Infer test requirements from specification
python tools/testing_agent.py infer data_validation_capability

# List test logs
python tools/testing_agent.py logs
```

**Process Flow:**
1. **Repository Validation:** Runs `validate_repo_docs.py --all`
2. **Python Syntax Check:** Validates all `.py` files in `jobs/` directory
3. **YAML Syntax Check:** Validates all `.yaml`/`.yml` files
4. **Specification Tests (if --spec provided):** Extracts and verifies acceptance criteria
5. **Generate Summary:** Reports passed/failed counts
6. **Write Log:** Saves detailed results to log file

#### Test Execution Details

**1. Repository Validation:**
- Executes: `python tools/validate_repo_docs.py --all`
- Validates: Manifests, script cards, business descriptions against standards
- Timeout: 300 seconds

**2. Python Syntax Check:**
- For each `.py` file in `jobs/` directory
- Executes: `python -m py_compile <file>`
- Reports: Syntax errors with file path

**3. YAML Syntax Check:**
- For each `.yaml` / `.yml` file in `jobs/` and `docs/specifications/`
- Validates: YAML structure using `yaml.safe_load()`
- Reports: Parse errors with file path

**4. Specification-Based Tests:**
- Reads capability specification YAML
- Extracts: `testing_requirements`, `coding_tasks` with `acceptance_criteria`
- Displays: Required unit tests, integration tests, and acceptance criteria
- Does NOT execute tests (inference only)

#### Example Usage

**Scenario:** Validate repository before PR and infer test requirements for data_validation capability.

```bash
# Run full test suite
python tools/testing_agent.py run

# Output:
# Running full test suite...
# ================================================================================
# 
# 1. Repository Validation Tests
# ------------------------------------------------------------
# [Output from validate_repo_docs.py]
# 
# 2. Python Syntax Checks
# ------------------------------------------------------------
# ✓ All 15 Python files have valid syntax
# 
# 3. YAML Syntax Checks
# ------------------------------------------------------------
# ✓ All 8 YAML files have valid syntax
# 
# ================================================================================
# Test Summary:
# ------------------------------------------------------------
# ✓ PASS Validation
# ✓ PASS Python Syntax
# ✓ PASS YAML Syntax
# ------------------------------------------------------------
# Passed: 3/3
# Failed: 0/3
# 
# ✓ Test log written to: logs/tests_logs/test_run_20260127_103000.log

# Infer test requirements from specification
python tools/testing_agent.py infer data_validation_capability

# Output:
# Test Requirements for: data_validation
# ================================================================================
# 
# Unit Tests:
#   - Test SKU uniqueness validation (VR-001)
#   - Test required field validation (VR-002)
#   - Test price range validation (VR-003)
# 
# Integration Tests:
#   - Test end-to-end validation with sample vendor data
#   - Test validation report generation
# 
# Acceptance Criteria by Task:
# 
# Task 1: Core Validation Logic
#   ✓ Validates all required fields per business rules
#   ✓ Detects duplicate SKUs within submission
#   ✓ Produces detailed validation report with row-level errors

# List recent test logs
python tools/testing_agent.py logs

# Output:
# Recent test logs:
# --------------------------------------------------------------------------------
# test_run_20260127_103000.log             2026-01-27 10:30:00 (12543 bytes)
# test_run_20260127_092000.log             2026-01-27 09:20:00 (11234 bytes)
# --------------------------------------------------------------------------------
# Total: 2 log(s)
```

**Expected Test Log Contents:**
```
Test Run: 20260127_103000
Specification: N/A
================================================================================

================================================================================
Validation - PASS
================================================================================
[Detailed validation output]

================================================================================
Python Syntax - PASS
================================================================================
✓ All 15 Python files have valid syntax

================================================================================
YAML Syntax - PASS
================================================================================
✓ All 8 YAML files have valid syntax

================================================================================
Summary: 3 passed, 0 failed
================================================================================
```

#### Dependency Handling

**Prerequisites:**
- `tools/validate_repo_docs.py` must exist for repository validation
- Python interpreter for syntax checking
- YAML library for YAML parsing

**Integration Points:**
- **CI Pipeline:** Automated execution on PR creation
- **Pre-commit:** Local validation before committing
- **Coding Agent:** References testing agent for quality gates

---

### 6. Documentation Agent (Documentation Maintenance)

**Role:** Assist humans in generating and maintaining project documentation including script cards, business descriptions, and glossary updates, **with all outputs requiring human review and approval**.

**Script Location:** `tools/documentation_agent.py`

**Workflow Position:** Post-implementation (after Step 5) and ongoing maintenance

#### Purpose and Responsibilities

The Documentation Agent **assists humans** in ensuring documentation stays aligned with code by:
- **Generating draft** script cards (operational reference for jobs) **for human review**
- **Creating draft** business job descriptions (business context and purpose) **for human validation**
- **Suggesting** glossary terms from specifications **for human approval**
- Validating documentation against repository standards
- **Proposing** consistency improvements between code and documentation

**Critical Rules:**
- Script cards must match job manifests (parameters, inputs, outputs)
- Business descriptions focus on "why" (business value), not "how" (technical details)
- Shared terms belong in `docs/glossary.md`, not duplicated per job
- All documentation must pass standards validation
- **All generated documentation requires human review and approval before integration**

#### Inputs

**For Script Cards and Business Descriptions:**
- Job ID (from `jobs/` directory structure)
- Optional: Capability specification reference

**For Glossary Suggestions:**
- Capability specification (`docs/specifications/<name>.yaml`)

#### Outputs

**Script Card:**
- File: `docs/script_cards/<job_id>.md`
- Contents: Job identification, purpose, parameters, inputs, outputs, side effects, processing logic, failure modes, operator checks, dependencies

**Business Description:**
- File: `docs/business_job_descriptions/<job_id>.md`
- Contents: Purpose (why job exists), business objective, inputs/outputs by business meaning, business rules, boundaries, success criteria, stakeholders

**Glossary Suggestions:**
- Console output: Suggested terms from specification inputs, outputs, and business rules
- Recommendation: Add to `docs/glossary.md` if shared across jobs

**Validation Output:**
- Console output: Results of documentation standards validation

#### Workflow Integration

**Trigger:**
- Manual invocation after job implementation
- Part of PR checklist for new jobs
- Ongoing maintenance for documentation updates

**Commands:**
```bash
# Create script card for a job
python tools/documentation_agent.py script-card validate_vendor_data --spec data_validation_capability

# Create business description for a job
python tools/documentation_agent.py business-desc validate_vendor_data --spec data_validation_capability

# Suggest glossary terms from specification
python tools/documentation_agent.py glossary data_validation_capability

# Validate all documentation
python tools/documentation_agent.py validate
```

**Process Flow (Script Card):**
1. Create `docs/script_cards/` directory if needed
2. Generate script card template with:
   - Job identification (job_id, Glue job name, runtime)
   - Purpose (one-line summary)
   - Parameters table (name, type, required, default, description)
   - Inputs section (S3 location patterns, file patterns, formats)
   - Outputs section (S3 location patterns, content contracts)
   - Side effects
   - Processing logic (high-level steps)
   - Failure modes table
   - Operator checks (pre-run, post-run)
   - Dependencies (upstream/downstream jobs)
3. Write template to file
4. Prompt developer to fill in TODO sections

**Process Flow (Business Description):**
1. Create `docs/business_job_descriptions/` directory if needed
2. Generate business description template with:
   - Purpose (why job exists, business problem it solves)
   - Business objective
   - Inputs/outputs by business meaning (NOT technical storage)
   - Business rules and controls
   - Boundaries (non-goals, explicit exclusions)
   - Success criteria (business perspective)
   - Stakeholders (owner, consumers, reviewers)
3. Write template to file
4. Prompt developer to fill in TODO sections with business context

**Process Flow (Glossary Suggestions):**
1. Read capability specification YAML
2. Extract potential terms from:
   - Input names and purposes
   - Output names and purposes
   - Business rules (capitalized domain terms)
3. Display suggestions with recommendation:
   - Add to `docs/glossary.md` if shared across multiple jobs
   - Add to `docs/glossary.md` if business domain terms
   - Do NOT add if obvious from context

#### Example Usage

**Scenario:** Create documentation for "validate_vendor_data" job after implementation.

```bash
# Create script card
python tools/documentation_agent.py script-card validate_vendor_data \
  --spec data_validation_capability

# Output:
# ✓ Created script card: docs/script_cards/validate_vendor_data.md
# 
# Next steps:
# 1. Fill in all TODO sections based on job implementation
# 2. Ensure parameters, inputs, outputs match job_manifest.yaml
# 3. Run validation: python tools/validate_repo_docs.py --all

# Create business description
python tools/documentation_agent.py business-desc validate_vendor_data \
  --spec data_validation_capability

# Output:
# ✓ Created business description: docs/business_job_descriptions/validate_vendor_data.md
# 
# Next steps:
# 1. Fill in all TODO sections with business context
# 2. Focus on 'why' not 'how'
# 3. Review with business stakeholders

# Suggest glossary terms
python tools/documentation_agent.py glossary data_validation_capability

# Output:
# Suggested glossary terms from specification: data_validation
# ================================================================================
# 
# Review these terms and add to docs/glossary.md if they are shared across jobs:
# 
# From Inputs:
#   - staged_raw_data: Unprocessed vendor data staged for validation
# 
# From Outputs:
#   - validation_report: Detailed report of validation errors
#   - validated_data: Vendor data confirmed to meet business rules
# 
# From Business Rules:
#   - Consider terms from: Each vendor SKU must be unique within the submission
# 
# ================================================================================
# 
# Note: These are suggestions. Only add terms to glossary.md if they are:
#   - Shared across multiple jobs
#   - Business domain terms
#   - Not obvious from context

# Validate documentation
python tools/documentation_agent.py validate

# Output:
# Running documentation validation...
# ------------------------------------------------------------
# [Output from validate_repo_docs.py --all]
# ------------------------------------------------------------
# ✓ Documentation validation passed
```

**Expected Script Card Template:**
```markdown
# Script Card: validate_vendor_data

**Version:** 1.0.0  
**Last Updated:** 2026-01-27  
**Status:** Draft  
**Specification:** Based on specification: data_validation_capability

---

## Job Identification

- **job_id:** `validate_vendor_data`
- **Glue Job Name:** `TODO: AWS Glue job name`
- **Runtime:** `TODO: e.g., AWS Glue 4.0 (Python 3.10, Spark 3.3.0)`
- **Executor:** AWS Glue

---

## Purpose (One-Line Summary)

TODO: Brief one-line description of what this job does.

---

## Parameters

| Parameter Name | Type | Required | Default | Description |
|----------------|------|----------|---------|-------------|
| TODO           | TODO | Yes/No   | TODO    | TODO        |

[... rest of template sections ...]
```

**Expected Business Description Template:**
```markdown
# Business Job Description: validate_vendor_data

**Version:** 1.0.0  
**Last Updated:** 2026-01-27  
**Status:** Draft  
**Specification:** Based on specification: data_validation_capability

---

## Purpose

TODO: Explain **why** this job exists and what business problem it solves.

---

## Business Objective

TODO: Define the business objective this job achieves.

[... rest of template sections ...]
```

#### Dependency Handling

**Prerequisites:**
- `tools/validate_repo_docs.py` for documentation validation
- Capability specification (optional, for reference context)

**Integration Points:**
- **Coding Agent (Step 4):** Codex tasks include documentation requirements
- **Standards:** Must comply with specs in `docs/standards/`
  - `script_card_spec.md` for script cards
  - `business_job_description_spec.md` for business descriptions
- **Glossary:** Shared terms go to `docs/glossary.md`

---

## Summary: Implementation Phase Workflow (Steps 3–5)

The implementation phase transforms approved capability plans into working code with proper testing and documentation.

### Workflow Sequence

```
┌─────────────────────────────────────────────────────┐
│ Step 3: Decompose (Coding Agent)                   │
│ Output: Development elements (console)              │
│ Review and adjust decomposition                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: Create Codex Tasks (Coding Agent)          │
│ Output: Codex task specifications (console)         │
│ For each development element                        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: Execute PR (Developer/Codex)               │
│ - Implement code per Codex task                    │
│ - Run Testing Agent for validation                 │
│ - Run Documentation Agent for docs                 │
│ - Pass all quality gates                           │
│ - Create PR for review                             │
└─────────────────────────────────────────────────────┘
```

### Quality Gates (Must Pass Before PR Merge)

All PRs must pass these gates:

1. **Repository Validation:**
   ```bash
   python tools/validate_repo_docs.py --all
   ```

2. **Testing Agent Validation:**
   ```bash
   python tools/testing_agent.py run
   ```

3. **Syntax and Best Practices:**
   ```bash
   python tools/coding_agent.py check
   ```

4. **Documentation Validation:**
   ```bash
   python tools/documentation_agent.py validate
   ```

### Key Principles

1. **Small, Focused PRs:** Each development element = one PR
2. **Explicit File Restrictions:** Codex tasks specify exact allowed file changes
3. **Standards Compliance:** All agents reference and enforce repository standards
4. **Testable Acceptance Criteria:** Criteria must be verifiable from repository contents
5. **Quality Before Merge:** All quality gates must pass

---

## Agent Deprecation Notice

### Designer Agent

**Script Location:** `tools/designer_agent.py`

**Status:** DEPRECATED / LEGACY

**Reason:** The Designer Agent creates "subsystem specifications" which overlap with the current planning workflow:
- Step 1 (Planner Agent) defines objectives
- Step 2a (Pipeline Planner Agent) creates pipeline plans
- Step 2b (Capability Planner Agent) creates detailed capability specifications

The Designer Agent appears to be from an earlier workflow iteration and creates specifications that duplicate or conflict with the current Step 2b (Capability Planner) output.

**Recommendation:**
- **DO NOT USE** Designer Agent for new work
- **USE** the current 5-step workflow: Planner → Pipeline Planner → Capability Planner → Coding Agent
- **MIGRATION:** If existing subsystem specifications created by Designer Agent exist, migrate them to capability specifications following Step 2b format
- **FUTURE:** Consider removing `designer_agent.py` after confirming no active dependencies

**Migration Path (if needed):**
```bash
# Instead of (DEPRECATED):
python tools/designer_agent.py create "subsystem_name"

# Use (CURRENT):
# Step 1: Define objective
python tools/planner_agent.py create "objective_name"

# Step 2a: Create pipeline plan
python tools/pipeline_planner_agent.py create "objective_name"

# Step 2b: Create capability plan for each step
python tools/capability_planner_agent.py create "capability_name"
```

---

## Complete Agent Workflow Summary

### Full 5-Step Workflow with Agents

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Define Objective                           │
│ Agent: Planner Agent                                │
│ Output: docs/roadmaps/<objective>.md                │
│ Manual Discussion → Approval Required               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2a: Overarching Plan (Pipeline-Level)         │
│ Agent: Pipeline Planner Agent                       │
│ Output: docs/roadmaps/<objective>_pipeline_plan.md  │
│ Manual Discussion → Approval Required               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2b: Capability Plan (Step-Level)              │
│ Agent: Capability Planner Agent                     │
│ Output: docs/specifications/<capability>.yaml       │
│ Manual Discussion → Approval Required               │
│ Repeat for EACH capability in pipeline             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: Decompose into Development Elements        │
│ Agent: Coding Agent                                 │
│ Output: Development elements (console)              │
│ Review and adjust decomposition                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: Create Codex Tasks                         │
│ Agent: Coding Agent                                 │
│ Output: Codex task specifications (console)         │
│ For each development element from Step 3            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: Execute PR (Implementation)                │
│ Agents: Testing Agent, Documentation Agent          │
│ - Implement code per Codex task                    │
│ - Run tests (Testing Agent)                        │
│ - Generate docs (Documentation Agent)              │
│ - Pass all quality gates                           │
│ - Create PR for review                             │
└─────────────────────────────────────────────────────┘
```

### Agent Command Reference

**Planning Phase (Steps 1–2):**
```bash
# Step 1: Define Objective
python tools/planner_agent.py create "objective_name"
python tools/planner_agent.py list

# Step 2a: Create Pipeline Plan
python tools/pipeline_planner_agent.py create "objective_name" --objective-ref "objective_name.md"
python tools/pipeline_planner_agent.py list

# Step 2b: Create Capability Plan (repeat for each capability)
python tools/capability_planner_agent.py create "capability_name" --pipeline-ref "objective_pipeline_plan.md"
python tools/capability_planner_agent.py list
python tools/capability_planner_agent.py validate docs/specifications/capability_name.yaml
```

**Implementation Phase (Steps 3–5):**
```bash
# Step 3: Decompose Capability
python tools/coding_agent.py decompose capability_name

# Step 4: Create Codex Task
python tools/coding_agent.py codex-task capability_name element_id

# Step 5: Validation and Testing
python tools/coding_agent.py validate
python tools/coding_agent.py check
python tools/testing_agent.py run
python tools/testing_agent.py run --spec capability_name
python tools/testing_agent.py infer capability_name
python tools/testing_agent.py logs

# Step 5: Documentation
python tools/documentation_agent.py script-card job_id --spec capability_name
python tools/documentation_agent.py business-desc job_id --spec capability_name
python tools/documentation_agent.py glossary capability_name
python tools/documentation_agent.py validate
```

---

## See Also

- `docs/workflows/WORKFLOW_5_STEPS.md` — Complete 5-step workflow documentation
- `docs/context_packs/system_context.md` — Repository context and structure
- `docs/workflows/AGENTS_SETUP.md` — Agent installation and usage guide
- `docs/standards/` — Repository standards and specifications
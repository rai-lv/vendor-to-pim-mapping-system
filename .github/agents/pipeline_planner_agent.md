# Pipeline Planner Agent Profile

## Name
Pipeline Planner Agent (Step 2a: Overarching Plan / Pipeline-Level)

## Description
The Pipeline Planner Agent creates end-to-end pipeline plans that define the complete processing sequence for achieving approved objectives. It focuses on the "what" and "sequence" of capabilities without diving into implementation details. The agent facilitates structured manual discussions between technical and business stakeholders to design the pipeline architecture, identify decision points, define conceptual data artifacts, and map existing jobs to pipeline steps. This ensures consensus on the overall pipeline structure before detailed capability specifications are created.

## Task Scope
The Pipeline Planner Agent operates at **Step 2a** of the 5-step development workflow and is responsible for:

1. **Processing Sequence Design**: Defining an ordered list of capabilities/steps that form the complete pipeline from start to finish (first → last).

2. **Decision Point Identification**: Identifying conditional logic, branching scenarios, and fallback paths within the pipeline flow.

3. **Conceptual Artifact Definition**: Defining data artifacts exchanged between pipeline steps by their business meaning (not storage details like S3 paths or schemas).

4. **Existing Job Mapping**: Analyzing which existing jobs can be reused, which require enhancement, and which capabilities need new job implementations.

5. **Unknown Documentation**: Explicitly marking unknowns and open decisions that require stakeholder input or investigation.

6. **Discussion Facilitation**: Supporting structured manual discussions to ensure technical and business alignment on pipeline architecture.

7. **Pipeline Plan Documentation**: Creating the authoritative pipeline plan document at `docs/roadmaps/<objective_name>_pipeline_plan.md` that serves as the foundation for capability-level planning (Step 2b).

**Critical Rules:**
- Pipeline plans define **"what" and "sequence"**, NOT **"how"** each step works (implementation details deferred to Step 2b)
- Conceptual artifacts defined by **meaning**, NOT by storage (S3 paths, formats, schemas)
- Pipeline plan cannot be created without approved Step 1 objective
- Changes to Step 1 objective require re-validation of Step 2a pipeline plan
- Manual approval required before proceeding to Step 2b

## Inputs

### Primary Input
**Approved Step 1 Objective Definition**: `docs/roadmaps/<objective_name>.md`

The agent requires a completed and stakeholder-approved objective definition from the Planner Agent (Step 1).

### Discussion Inputs
The agent facilitates gathering the following through manual stakeholder discussions:

1. **Business Process Flow**: The logical sequence of business operations required to achieve the objective
2. **Decision Logic**: Conditional branching scenarios, success/failure paths, retry strategies
3. **Data Flow Requirements**: What data moves between steps and what it represents (conceptual meaning)
4. **Existing Capabilities**: Which jobs already exist in the repository and can be leveraged
5. **Integration Points**: External systems, APIs, or services involved in the pipeline
6. **Quality Requirements**: Performance, reliability, scalability considerations at the pipeline level

## Outputs

### Primary Output
**Pipeline Plan Document**: `docs/roadmaps/<objective_name>_pipeline_plan.md`

The pipeline plan document includes the following required sections:

1. **Objective Reference**: Link to the Step 1 objective definition document

2. **Processing Sequence**: Ordered list of pipeline steps/capabilities
   - Format: `Step 1: [Capability Name] → Step 2: [Capability Name] → ...`
   - Clear indication of sequence and dependencies

3. **Detailed Step Descriptions**: For each step in the pipeline:
   - **Purpose**: What this step accomplishes
   - **Input**: Conceptual artifact consumed (by meaning, not storage)
   - **Output**: Conceptual artifact produced (by meaning, not storage)
   - **Decision Points**: Conditional logic affecting flow (if applicable)

4. **Decision Points**: Conditional logic with fallback paths:
   - **Condition**: What triggers the decision
   - **Success Path**: Next step on success
   - **Failure/Alternative Path**: Fallback behavior on failure
   - **Retry Logic**: Retry strategies if applicable

5. **Conceptual Artifacts Catalog**: For each artifact exchanged between steps:
   - **Artifact Name**: Descriptive name (e.g., "Validated Vendor Data")
   - **Meaning**: What the artifact represents in business context
   - **Producer**: Which step creates this artifact
   - **Consumer**: Which step(s) consume this artifact
   - **NOT included**: S3 paths, file formats, detailed schemas (deferred to implementation)

6. **Existing Job Mapping**: Table showing:
   - **Pipeline Step**: Step from processing sequence
   - **Existing Job**: Job ID from `jobs/` directory (if applicable)
   - **Status**: ✅ Exists (reusable), ⚠️ Partial (requires enhancement), ❌ New (needs creation)
   - **Notes**: Reusability details or gaps

7. **Unknowns and Open Decisions**:
   - **Unknowns (TBD)**: Items requiring investigation before implementation
   - **Open Decisions**: Items requiring stakeholder input and decision
   - All marked explicitly (no assumptions presented as facts)

8. **Next Steps**: Immediate action items, including which capabilities need Step 2b planning

### Process Outputs
- **Discussion Checkpoints**: Structured agendas and outcomes for pipeline architecture alignment
- **Approval Gate**: Stakeholder sign-off indicating readiness to proceed to Step 2b

## Supported Commands

### Create Pipeline Plan
```bash
python tools/pipeline_planner_agent.py create "objective_name" \
  --objective-ref "objective_name.md"
```

**Purpose**: Creates a pipeline plan document at `docs/roadmaps/<objective_name>_pipeline_plan.md`

**Parameters**:
- `objective_name`: Name matching the Step 1 objective (used for filename)
- `--objective-ref`: Filename of the Step 1 objective document in `docs/roadmaps/`

**Validation**: Agent verifies that the referenced objective document exists before proceeding

**Output**: Creates the pipeline plan document with template sections ready for collaborative refinement

### Additional Operations
The Pipeline Planner Agent script may support additional commands for:
- Viewing existing pipeline plans
- Validating pipeline plan structure
- Visualizing pipeline flow (if visualization features are implemented)

## Integration

### Workflow Position
The Pipeline Planner Agent operates at **Step 2a** in the 5-step development workflow:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan (Pipeline Planner Agent) ← THIS AGENT
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
```

### Manual Discussion Process
The Pipeline Planner Agent supports a structured discussion process with defined checkpoints:

**Checkpoint 1: Processing Sequence Review (Day 1)**
- **Participants**: Tech Lead, Architect, Business Analyst
- **Focus**: Validate processing sequence logic, identify missing steps, ensure alignment with business process flow
- **Output**: Validated and complete processing sequence

**Checkpoint 2: Decision Points and Fallback Paths (Day 2)**
- **Participants**: Tech Lead, Product Owner, DevOps
- **Focus**: Define critical decision points, establish fallback/retry strategies, document failure handling
- **Output**: Complete decision logic with well-defined fallback paths

**Checkpoint 3: Conceptual Artifacts Definition (Day 3)**
- **Participants**: Tech Lead, Data Architect, Business Analyst
- **Focus**: Define data artifacts by business meaning, map producer/consumer relationships, ensure data flow completeness
- **Output**: Complete conceptual artifacts catalog

**Checkpoint 4: Existing Job Mapping (Day 4)**
- **Participants**: Tech Lead, Development Team
- **Focus**: Identify reusable jobs, document required enhancements, identify gaps requiring new development
- **Output**: Job mapping table with clear reuse/enhancement/new-development classification

**Checkpoint 5: Unknowns and Open Decisions Resolution (Day 5)**
- **Participants**: All stakeholders
- **Focus**: Categorize unknowns by priority, resolve critical open decisions, defer non-critical items to Step 2b
- **Output**: Prioritized unknowns with resolution plan

**Final Approval Checkpoint**
- **Participants**: All stakeholders
- **Deliverable**: Signed-off pipeline plan ready for Step 2b capability planning
- **Gate**: Document becomes locked and authoritative for capability-level specifications

### Dependency Chain
- **Prerequisites**: Approved Step 1 objective definition (`docs/roadmaps/<objective_name>.md`)
- **Dependents**: Capability Planner Agent (Step 2b) requires approved Step 2a pipeline plan
- **Validation**: Agent verifies Step 1 document exists before creating Step 2a plan
- **Authority**: The pipeline plan serves as the authoritative architecture for all capability specifications

### Quality Gates
- Step 1 objective must be approved before Step 2a can begin
- Manual stakeholder approval required before proceeding to Step 2b
- All unknowns explicitly documented (no assumptions)
- Processing sequence must be complete and logical
- Decision points must have defined fallback paths

### Integration with Repository Structure
The pipeline plan references:
- **Existing Jobs**: Jobs in `jobs/<job_group>/<job_id>/` that can be reused or enhanced
- **Job Manifests**: `job_manifest.yaml` files to understand existing job interfaces
- **Capability Specifications**: Plans for which capabilities need Step 2b specifications

## Example Usage

### Scenario: Create Pipeline Plan for Vendor Onboarding

**Step 1: Invoke Pipeline Planner Agent**
```bash
python tools/pipeline_planner_agent.py create "vendor_onboarding" \
  --objective-ref "vendor_onboarding.md"
```

**Output**: Creates `docs/roadmaps/vendor_onboarding_pipeline_plan.md` with initial template

**Step 2: Collaborative Pipeline Architecture Design**

The team conducts structured discussions to design the pipeline:

**Processing Sequence Discussion (Day 1):**
- Identify steps: Data Ingestion → Data Validation → Data Normalization → PIM Integration → Notification
- Validate completeness: Are all required processing steps included?
- Outcome: 5-step pipeline sequence agreed upon

**Decision Points Discussion (Day 2):**
- Validation failure handling: If validation fails → skip to Notification with failure status
- PIM API failure handling: Retry 3 times with exponential backoff → if all fail, route to manual queue
- Outcome: Decision logic documented with clear fallback paths

**Conceptual Artifacts Discussion (Day 3):**
- Define artifacts:
  - "Vendor Submission File" (external → ingestion)
  - "Staged Raw Data" (ingestion → validation)
  - "Validation Report" (validation → notification)
  - "Validated Data" (validation → normalization)
  - "Normalized PIM-Ready Data" (normalization → PIM integration)
  - "PIM Record IDs" (PIM integration → notification)
- Outcome: Complete data flow documented by business meaning

**Existing Job Mapping (Day 4):**
- Review existing jobs in `jobs/` directory
- Map findings:
  - Data Ingestion: `s3_file_intake_job` ✅ Exists (reusable)
  - Data Validation: ❌ New (needs creation)
  - Data Normalization: `vendor_to_pim_mapper_v2` ⚠️ Partial (needs enhancement for new formats)
  - PIM Integration: `pim_batch_loader` ✅ Exists (needs configuration update)
  - Notification: `email_notification_job` ✅ Exists (reusable as-is)
- Outcome: Clear understanding of what to build vs. reuse

**Unknowns Resolution (Day 5):**
- TBD items identified:
  - Maximum vendor file size (impacts infrastructure sizing)
  - Vendor submission frequency (affects batch vs. real-time decision)
  - Data retention policy for staged files
- Open decisions:
  - Real-time vs. daily batch processing mode?
  - Retry count and backoff strategy for PIM API?
  - Archive policy for validation failures?
- Outcome: Unknowns documented, critical decisions scheduled for resolution

**Step 3: Final Approval and Handoff**
- All stakeholders review complete pipeline plan
- Sign-off obtained
- Document locked as authoritative reference
- Ready for Step 2b capability planning

### Expected Document Structure

```markdown
# Pipeline Plan: Vendor Onboarding

**Objective Reference:** `docs/roadmaps/vendor_onboarding.md`

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-01-27

---

## Processing Sequence

```
Step 1: Data Ingestion 
   → Step 2: Data Validation 
   → Step 3: Data Normalization 
   → Step 4: PIM Integration 
   → Step 5: Notification
```

---

## Detailed Step Descriptions

### Step 1: Data Ingestion
**Purpose:** Receive and stage vendor submission files for processing.

**Input:** Vendor submission files from external vendor portal (various formats: Excel, CSV, JSON).

**Output:** Staged raw data artifacts ready for validation.

**Notes:** Handles multiple vendor formats; performs initial file validation (format, size limits).

---

### Step 2: Data Validation
**Purpose:** Validate vendor data against business rules and data quality standards.

**Input:** Staged raw data artifacts from Step 1.

**Output:** 
- Validation report (always produced)
- Validated data artifacts (produced only on success)

**Decision Point:** 
- **Condition:** Does data pass all validation rules?
- **Pass:** Proceed to Step 3 (Data Normalization)
- **Fail:** Skip to Step 5 (Notification) with failure status and validation report

**Notes:** Enforces business rules for SKU uniqueness, required fields, price ranges, category mappings.

---

### Step 3: Data Normalization
**Purpose:** Transform validated vendor data to PIM schema format.

**Input:** Validated data artifacts from Step 2.

**Output:** Normalized PIM-ready data artifacts.

**Notes:** Maps vendor-specific formats to standardized PIM schema; handles category mapping.

---

### Step 4: PIM Integration
**Purpose:** Load normalized data into PIM system via API.

**Input:** Normalized PIM-ready data artifacts from Step 3.

**Output:** PIM record IDs for created/updated products.

**Decision Point:**
- **Condition:** PIM API responds successfully?
- **Success:** Proceed to Step 5 (Notification) with success status
- **Transient Error:** Retry with exponential backoff (3 attempts max)
- **Permanent Failure:** Route to manual queue and notify stakeholders

**Notes:** Batch processing to manage PIM API rate limits; idempotent operations.

---

### Step 5: Notification
**Purpose:** Notify vendor and stakeholders of processing results.

**Input:** Processing status (success/failure) + relevant artifacts (PIM record IDs or validation report).

**Output:** Email notifications to vendor and internal stakeholders.

**Notes:** Different notification templates for success vs. failure scenarios.

---

## Decision Points

### Decision 1: Validation Pass/Fail
**Location:** After Step 2 (Data Validation)

**Condition:** Data passes all validation rules and quality thresholds (≥80% pass rate)?

**Pass Path:** Proceed to Step 3 (Data Normalization)

**Fail Path:** Skip Steps 3-4, proceed directly to Step 5 (Notification) with:
- Failure status
- Validation report with detailed errors
- No PIM integration attempted

**Rationale:** Invalid data should not proceed to PIM; vendor must correct and resubmit.

---

### Decision 2: PIM API Success/Retry/Fail
**Location:** During Step 4 (PIM Integration)

**Condition:** PIM API responds successfully to batch load request?

**Success Path:** 
- Capture PIM record IDs
- Proceed to Step 5 (Notification) with success status

**Transient Error Path (e.g., timeout, rate limit):**
- Retry with exponential backoff: 5s, 15s, 45s (3 attempts total)
- If retry succeeds: Follow success path
- If all retries fail: Follow permanent failure path

**Permanent Failure Path (e.g., authentication error, malformed data):**
- Route normalized data to manual processing queue
- Proceed to Step 5 (Notification) with:
  - Failure status
  - Error details
  - Manual queue ticket ID

**Rationale:** Transient errors are common with API integrations; retries improve reliability. Permanent errors require human intervention.

---

## Conceptual Artifacts

### 1. Vendor Submission File
**Meaning:** Raw product catalog data submitted by vendor (SKUs, descriptions, pricing, inventory).

**Producer:** External vendor (submitted via vendor portal).

**Consumer:** Data Ingestion (Step 1).

**Business Context:** Unprocessed vendor data in various formats (Excel, CSV, JSON). May contain errors or incomplete data.

---

### 2. Staged Raw Data
**Meaning:** Unprocessed vendor data stored in staging area awaiting validation.

**Producer:** Data Ingestion (Step 1).

**Consumer:** Data Validation (Step 2).

**Business Context:** Copy of vendor submission file in normalized storage location for pipeline processing.

---

### 3. Validation Report
**Meaning:** Detailed report of validation errors, warnings, and data quality issues with row-level details.

**Producer:** Data Validation (Step 2).

**Consumer:** Notification (Step 5), Manual Review Queue.

**Business Context:** Row-by-row breakdown of which data passed/failed validation rules, including error codes, messages, and suggested fixes.

---

### 4. Validated Data
**Meaning:** Vendor data confirmed to meet all business rules and quality standards.

**Producer:** Data Validation (Step 2).

**Consumer:** Data Normalization (Step 3).

**Business Context:** Subset of staged raw data that passed validation. Only produced when validation succeeds (≥80% pass rate).

---

### 5. Normalized PIM-Ready Data
**Meaning:** Vendor data transformed to match PIM system schema and field requirements.

**Producer:** Data Normalization (Step 3).

**Consumer:** PIM Integration (Step 4).

**Business Context:** Validated data mapped to PIM fields (categories, attributes, pricing structure) ready for API ingestion.

---

### 6. PIM Record IDs
**Meaning:** Unique identifiers for products created or updated in PIM system.

**Producer:** PIM Integration (Step 4).

**Consumer:** Notification (Step 5).

**Business Context:** Confirmation that products are successfully loaded in PIM with unique record identifiers for tracking.

---

## Existing Job Mapping

| Pipeline Step | Existing Job | Status | Notes |
|---------------|--------------|--------|-------|
| Data Ingestion | `s3_file_intake_job` | ✅ Exists | Supports CSV, JSON, Excel. Reusable as-is. |
| Data Validation | — | ❌ New | Needs full implementation. No existing job covers vendor validation rules. |
| Data Normalization | `vendor_to_pim_mapper_v2` | ⚠️ Partial | Exists but requires enhancement for new vendor formats (Excel support needed). |
| PIM Integration | `pim_batch_loader` | ✅ Exists | Reusable with configuration update for new vendor data schema. |
| Notification | `email_notification_job` | ✅ Exists | Reusable as-is. Supports templated emails. |

**Summary:**
- **Reusable (3)**: Data Ingestion, PIM Integration, Notification
- **Enhancement Required (1)**: Data Normalization
- **New Development (1)**: Data Validation

**Next Steps:**
- Step 2b capability planning required for: Data Validation (new), Data Normalization (enhancement)
- Configuration updates needed for: PIM Integration (schema mapping)

---

## Unknowns and Open Decisions

### Unknowns (TBD - Require Investigation)
1. **TBD:** Maximum vendor file size and expected processing time
   - **Impact:** Affects infrastructure sizing (Glue DPU allocation, timeout settings)
   - **Resolution Target:** Before Step 3 decomposition

2. **TBD:** Expected vendor submission frequency (daily, weekly, on-demand)
   - **Impact:** Affects batch vs. real-time processing decision
   - **Resolution Target:** Before Step 3 decomposition

3. **TBD:** Data retention policy for staged raw data and validation reports
   - **Impact:** Affects S3 lifecycle policies and compliance requirements
   - **Resolution Target:** Before Step 5 implementation

4. **TBD:** Average number of concurrent vendor submissions
   - **Impact:** Affects pipeline concurrency settings and queue management
   - **Resolution Target:** Before Step 3 decomposition

### Open Decisions (Require Stakeholder Input)
1. **OPEN:** Real-time processing vs. daily batch mode?
   - **Context:** Should submissions process immediately or in scheduled batches?
   - **Impact:** Major architecture decision affecting cost, complexity, and latency
   - **Decision Needed By:** End of Step 2a (before Step 2b)

2. **OPEN:** Retry strategy parameters for PIM API failures
   - **Context:** How many retries? What backoff strategy? When to escalate?
   - **Current Proposal:** 3 retries with exponential backoff (5s, 15s, 45s)
   - **Decision Needed By:** During Data Normalization capability plan (Step 2b)

3. **OPEN:** Archive policy for validation failures
   - **Context:** Do we keep failed submissions for compliance audit? For how long?
   - **Impact:** Affects storage costs and compliance capabilities
   - **Decision Needed By:** During Data Validation capability plan (Step 2b)

4. **OPEN:** Escalation process for repeated vendor submission failures
   - **Context:** What happens if same vendor fails validation 3+ times?
   - **Impact:** Affects notification logic and vendor relationship management
   - **Decision Needed By:** During Notification capability plan (Step 2b)

---

## Next Steps

### Immediate Actions
1. **Resolve Critical Open Decisions:**
   - Schedule stakeholder meeting to decide on real-time vs. batch processing
   - Confirm retry strategy with DevOps and PIM team

2. **Proceed to Step 2b (Capability Planning):**
   - Create capability specification for **Data Validation** (new development)
   - Create capability specification for **Data Normalization** (enhancement)

3. **Configuration Planning:**
   - Document PIM Integration configuration requirements
   - Plan S3 bucket structure for staged data

### Dependencies to Track
- Vendor format specifications delivery (due: March 15, 2026)
- PIM API rate limit documentation from PIM team
- S3 bucket provisioning from DevOps (due: May 1, 2026)
```

### Use Case Variations

**Simple Sequential Pipeline:**
```bash
python tools/pipeline_planner_agent.py create "daily_price_update" \
  --objective-ref "daily_price_update.md"
```
Use for straightforward pipelines with minimal branching (e.g., extract → transform → load).

**Complex Decision-Driven Pipeline:**
```bash
python tools/pipeline_planner_agent.py create "smart_product_routing" \
  --objective-ref "smart_product_routing.md"
```
Use for pipelines with multiple decision points and complex routing logic.

**Parallel Processing Pipeline:**
```bash
python tools/pipeline_planner_agent.py create "multi_source_data_aggregation" \
  --objective-ref "multi_source_data_aggregation.md"
```
Use for pipelines where multiple capabilities can run in parallel before converging.

# Planner Agent Profile

## Name
Planner Agent (Step 1: Define Objective)

## Description
The Planner Agent is responsible for defining business objectives with explicit boundaries, testable success criteria, and comprehensive risk assessment. It serves as the entry point for all new development work in the repository, ensuring consensus on objectives before any design or implementation begins. The agent facilitates structured manual discussions between stakeholders to align on what must be achieved, what is out of scope, and how success will be measured.

## Task Scope
The Planner Agent operates at **Step 1** of the 5-step development workflow and is responsible for:

1. **Objective Definition**: Creating structured objective definitions that clearly state what must be achieved with specific, measurable goals and expected outcomes.

2. **Boundary Setting**: Explicitly defining what is out-of-scope to prevent scope creep and ensure stakeholder alignment on project boundaries.

3. **Success Criteria Establishment**: Defining testable functional and quality criteria that enable objective validation of project completion.

4. **Constraint Documentation**: Identifying and documenting technical, business, time, and resource constraints that impact the project.

5. **Risk Assessment**: Cataloging known risks with mitigation strategies, identifying unknowns requiring investigation, and documenting open questions requiring stakeholder decisions.

6. **Discussion Facilitation**: Supporting manual discussion phases with stakeholders to ensure consensus is reached before proceeding to pipeline planning.

7. **Documentation Generation**: Creating the authoritative objective definition document at `docs/roadmaps/<objective_name>.md` that serves as the foundation for all subsequent planning steps.

**Critical Rules:**
- No code changes are permitted without an approved Step 1 objective
- All unknowns must be explicitly marked (no assumptions presented as fact)
- Changes to the objective require re-validation of all downstream plans (Steps 2a, 2b)
- Sequential execution required: Step 1 must complete and receive approval before Step 2a begins

## Inputs

### Primary Input
- **Objective Name**: Human-provided name for the objective (e.g., "vendor_onboarding")
- **Brief Description**: Short description of the objective to initialize the planning process

### Discussion Inputs
The agent facilitates gathering the following information through manual stakeholder discussions:

1. **Business Requirements**: Expected outcomes, business goals, stakeholder priorities
2. **Constraints**: Technical limitations (systems, APIs, data), business constraints (deadlines, budget, resources), process constraints (approval workflows, dependencies)
3. **Risk Factors**: Known risks, potential blockers, uncertainty areas
4. **Open Questions**: Items requiring stakeholder decisions or clarification
5. **Dependencies**: External systems, teams, or prerequisites needed for success

## Outputs

### Primary Output
**Objective Definition Document**: `docs/roadmaps/<objective_name>.md`

The objective definition document includes the following required sections:

1. **Objective Statement**: Clear, concise description of what must be achieved

2. **Expected Outcomes**: Specific, measurable results that define project success

3. **Out-of-Scope Boundaries**: Explicit list of what is NOT included in this objective to prevent scope creep

4. **Success Criteria**:
   - **Functional Criteria**: Testable criteria defining required functionality
   - **Quality Criteria**: Performance, accuracy, reliability, and other quality metrics

5. **Constraints**:
   - **Technical Constraints**: Systems, APIs, data limitations
   - **Business Constraints**: Deadlines, budget, resource availability
   - **Process Constraints**: Approval workflows, team dependencies

6. **Risk Assessment**:
   - **Known Risks**: Identified risks with mitigation strategies
   - **Unknowns**: Items requiring investigation (marked as TBD)
   - **Open Questions**: Decisions requiring stakeholder input

7. **Dependencies**: External systems, teams, or prerequisites

### Process Outputs
- **Discussion Checkpoints**: Structured discussion agendas and outcomes for stakeholder alignment
- **Approval Gate**: Stakeholder sign-off indicating readiness to proceed to Step 2a

## Supported Commands

### Create Objective
```bash
python tools/planner_agent.py create "objective_name" \
  --description "Brief objective description"
```

**Purpose**: Creates an initial objective document template at `docs/roadmaps/<objective_name>.md`

**Parameters**:
- `objective_name`: Unique identifier for the objective (used in filename and references)
- `--description`: Optional brief description to populate the initial template

**Output**: Creates the objective definition document with template sections ready for collaborative refinement

### Additional Operations
The Planner Agent script may support additional commands for:
- Viewing existing objectives
- Validating objective structure
- Checking dependencies and references

## Integration

### Workflow Position
The Planner Agent is the **entry point** of the 5-step development workflow:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
```

### Manual Discussion Process
The Planner Agent supports a structured discussion process with defined checkpoints:

**Checkpoint 1: Initial Objective Review (Day 1)**
- **Participants**: Product Owner, Tech Lead, Business Stakeholders
- **Focus**: Validate objective statement clarity, expected outcomes, initial out-of-scope items
- **Output**: Refined objective statement and outcomes

**Checkpoint 2: Success Criteria Definition (Day 2-3)**
- **Participants**: Tech Lead, QA Lead, Product Owner
- **Focus**: Define testable success criteria, verify measurement capabilities
- **Output**: Complete, testable success criteria list

**Checkpoint 3: Risk and Constraint Review (Day 3-5)**
- **Participants**: Tech Lead, Architect, Business Analyst
- **Focus**: Document all constraints, identify high-priority unknowns, resolve critical open questions
- **Output**: Complete risk assessment with mitigation strategies

**Final Approval Checkpoint**
- **Participants**: All stakeholders
- **Deliverable**: Signed-off objective definition
- **Gate**: Document becomes locked and authoritative for Step 2a

### Dependency Chain
- **Prerequisites**: None (Step 1 is the entry point)
- **Dependents**: Pipeline Planner Agent (Step 2a) requires approved Step 1 output
- **Authority**: The objective definition serves as the authoritative reference for all subsequent planning and implementation work

### Quality Gates
- Manual stakeholder approval required before proceeding to Step 2a
- All unknowns must be explicitly documented (no assumptions)
- Success criteria must be testable and verifiable
- Boundaries must be clear and agreed upon by stakeholders

## Example Usage

### Scenario: Define Objective for Vendor Onboarding Pipeline

**Step 1: Create Initial Objective Document**
```bash
python tools/planner_agent.py create "vendor_onboarding" \
  --description "Implement automated vendor onboarding pipeline"
```

**Output**: Creates `docs/roadmaps/vendor_onboarding.md` with initial template

**Step 2: Collaborative Refinement**

The team conducts structured discussions to populate the template:

**Initial Discussion (Day 1):**
- Review: Is "automated vendor onboarding pipeline" clear?
- Outcome: Refined to "Implement automated pipeline for onboarding new vendors into the PIM system with standardized data submission and validation"

**Success Criteria Discussion (Day 2-3):**
- Define functional criteria:
  - ✓ Pipeline processes vendor submission files end-to-end
  - ✓ Data validation rules reject invalid submissions with clear error messages
  - ✓ Successful submissions create PIM records matching vendor data
- Define quality criteria:
  - ✓ Pipeline completes within 2-hour SLA for standard submissions
  - ✓ 99% data accuracy for automated mappings
  - ✓ Zero data loss during processing

**Risk Review (Day 3-5):**
- Known risks identified:
  - Vendor data quality varies significantly → Mitigation: robust validation layer
  - PIM API rate limits may impact throughput → Mitigation: batch processing strategy
- Unknowns documented:
  - TBD: Average vendor submission file size
  - TBD: Expected vendor submission frequency
  - OPEN QUESTION: Real-time vs. batch processing mode?

**Step 3: Final Approval**
- All stakeholders review complete objective definition
- Sign-off obtained
- Document locked as authoritative reference

**Step 4: Handoff to Pipeline Planner**
The approved objective definition is now ready for Step 2a (Pipeline Planner Agent)

### Expected Document Structure

```markdown
# Objective: Vendor Onboarding

## Objective Statement
Implement an automated pipeline for onboarding new vendors into the PIM system 
with standardized data submission, validation, and integration capabilities.

## Expected Outcomes
- Vendors can submit product data via standardized format (Excel, CSV, JSON)
- System validates and normalizes vendor data automatically against business rules
- Approved vendor products appear in PIM within 24 hours of submission
- 95% of valid vendor submissions process without manual intervention

## Out-of-Scope
- Manual vendor data entry workflows (remains separate manual process)
- Historical vendor data migration (separate project scheduled for Q3 2026)
- Vendor payment processing (handled by finance system)
- Vendor relationship management (handled by CRM system)

## Success Criteria

### Functional Criteria
- [ ] Pipeline processes vendor submission files end-to-end without errors
- [ ] Data validation rules reject invalid submissions with clear, actionable error messages
- [ ] Successful submissions create PIM records with 100% data accuracy
- [ ] Failed submissions generate detailed error reports for vendor correction

### Quality Criteria
- [ ] Pipeline completes within 2-hour SLA for standard submissions (<10,000 rows)
- [ ] 99% data accuracy for automated field mappings
- [ ] Zero data loss during processing (input row count = processed row count)
- [ ] System handles concurrent submissions from up to 50 vendors

## Constraints

### Technical
- Must integrate with existing PIM API (v2.1) without modifications
- S3 storage limits: 100GB per vendor submission batch
- AWS Glue 2.0 runtime environment required for compatibility
- Must support existing vendor formats: Excel (.xlsx), CSV, JSON

### Business
- Go-live date: End of Q2 2026 (June 30, 2026)
- Initial support for 3 vendor formats (expandable to 5 in Q3)
- Budget: $15K infrastructure costs (AWS Glue, S3, data transfer)
- Support 10 pilot vendors in phase 1, scale to 50 vendors in phase 2

### Process
- Security review required before production deployment
- Business stakeholder UAT approval required
- DevOps team must provision S3 buckets and IAM roles

## Risk Assessment

### Known Risks
1. **Vendor Data Quality Variability**
   - Risk: Vendor-submitted data quality varies significantly between vendors
   - Impact: High error rates could delay onboarding
   - Mitigation: Implement robust validation layer with detailed error reporting

2. **PIM API Rate Limits**
   - Risk: PIM API rate limits may impact throughput for large submissions
   - Impact: Processing delays during peak submission periods
   - Mitigation: Implement batch processing strategy with queue management

3. **Vendor Format Diversity**
   - Risk: Vendors may submit data in unexpected formats or structures
   - Impact: Parser failures requiring manual intervention
   - Mitigation: Strict format specification and validation at ingestion

### Unknowns (Requiring Investigation)
- **TBD**: Average vendor submission file size and row count
- **TBD**: Expected vendor submission frequency (daily, weekly, on-demand)
- **TBD**: Peak submission periods and concurrency requirements
- **TBD**: Vendor notification preferences and SLAs

### Open Questions (Requiring Stakeholder Decisions)
- **OPEN**: Should system support real-time processing or daily batch mode?
- **OPEN**: What is the retry strategy for PIM API failures (3 attempts? exponential backoff?)
- **OPEN**: Do we archive validation failure data for compliance audit?
- **OPEN**: What is the escalation process for repeated vendor submission failures?

## Dependencies

### External Systems
- **PIM API (v2.1)**: Required for product data integration
  - Status: Available, documentation provided
  - Contact: PIM team lead
  
- **Vendor Portal**: Source of vendor submission files
  - Status: In development (parallel project)
  - Contact: Portal product owner

### Internal Teams
- **DevOps Team**: S3 bucket provisioning, IAM role setup, Glue job deployment
  - Dependency: Must complete infrastructure setup by May 1, 2026
  
- **Business Team**: Vendor format specifications, validation rules documentation
  - Dependency: Format specs required by March 15, 2026

### Prerequisites
- PIM API access credentials and rate limit documentation
- S3 bucket access for vendor submission staging
- Vendor format specifications and sample data files
```

### Use Case Variations

**Small Feature Objective:**
```bash
python tools/planner_agent.py create "price_validation_enhancement" \
  --description "Add dynamic price range validation based on product category"
```
Use for minor enhancements with limited scope and dependencies.

**Large Pipeline Objective:**
```bash
python tools/planner_agent.py create "multi_vendor_marketplace_integration" \
  --description "Build end-to-end marketplace integration supporting 100+ vendors"
```
Use for major initiatives requiring extensive planning and multiple capability plans.

**Exploration Objective:**
```bash
python tools/planner_agent.py create "vendor_data_quality_research" \
  --description "Research and prototype vendor data quality scoring mechanism"
```
Use for research or prototyping work with high uncertainty and learning goals.

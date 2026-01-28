# 5-Step Development Workflow

This document describes the proper 5-step workflow for development in this repository.

## Workflow Overview

```
Step 1: Define Objective (Planner Agent)
   ↓
Step 2a: Overarching Plan / Pipeline-Level (Pipeline Planner Agent)
   ↓
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓
Step 3: Decompose into Development Elements (Coding Agent)
   ↓
Step 4: Create Codex Tasks (Coding Agent)
   ↓
Step 5: Code Creation (PR Process)
```

## Step 1: Define Objective

**Agent:** Interactive Planner Agent (`tools/interactive_planner_agent.py`)  
**Output:** `docs/roadmaps/<objective_name>.md`  
**Workflow:** Step 1 - Define Objective

### Purpose
Define what must be achieved with explicit boundaries and testable success criteria through **interactive conversation and automated refinement**.

### How the Agent Achieves the Intent

Per `development_approach.md`, the Planning function **supports you in refining the objective**, **ensuring it is actionable**, and **highlighting constraints, unknowns, and risks**. The Interactive Planner Agent automates this through conversational AI:

#### 1. Start Interactive Discussion
```bash
python tools/interactive_planner_agent.py discuss "<objective_name>"
```

The agent conducts a conversation to understand your needs:
```
Agent: "Let's define your objective. What are you trying to achieve?"
You: "I want to automate vendor onboarding"
Agent: "Can you be more specific? What exactly happens in vendor onboarding?"
You: "Vendors send XML files with product catalogs, we need to update PIM"
Agent: "Which PIM system and version? Any format requirements?"
You: "PIM API v2.1, files must match our schema"
Agent: "What's your current process? What problems are you solving?"
```

#### 2. Automated Refinement

**The agent automatically performs refinement through guided questions:**

**A. Refining to be Actionable:**
- Agent asks targeted questions to clarify vague statements
- Agent helps break down general goals into specific requirements
- Agent suggests concrete actions based on your answers
- Example: "automate vendor onboarding" → "Implement XML ingestion pipeline with schema validation and PIM API integration"

**B. Ensuring Context:**
- Agent asks about business context and motivation
- Agent helps define measurable success criteria
- Agent prompts for out-of-scope boundaries
- Agent ensures objective provides direction for subsequent steps

**C. Identifying Constraints, Unknowns, and Risks:**

**Constraints** (agent discovers through conversation):
- "What technical systems must you integrate with?"
- "Any deadlines or budget limitations?"
- "Compliance or regulatory requirements?"
- Agent documents all constraints automatically

**Unknowns** (agent identifies gaps):
- "What information are you missing?"
- "What decisions haven't been made yet?"
- Agent explicitly marks items as TBD or OPEN QUESTION
- Example: "TBD: Average file size (need baseline data)"

**Risks** (agent helps identify):
- "What could go wrong with this approach?"
- "What external dependencies concern you?"
- Agent suggests common risks based on patterns
- Agent captures impact, likelihood, mitigation for each risk

#### 3. Automated Document Generation

The agent generates a complete, refined objective document:
```
✓ Objective statement (refined from conversation)
✓ Specific, measurable goals (extracted from discussion)
✓ Expected outcomes (based on your requirements)
✓ Out-of-scope boundaries (what you said ISN'T included)
✓ Success criteria (functional + quality, testable)
✓ Constraints (technical, business, resources)
✓ Risk assessment (identified risks with mitigation)
✓ Unknowns (explicitly marked TBD/OPEN QUESTION)
✓ Dependencies (external factors identified)
```

#### 4. Iterative Refinement
```bash
python tools/interactive_planner_agent.py refine "<objective_name>"
```

The agent reviews and continues refinement:
```
Agent: "I've reviewed your objective. I notice you mentioned 3 vendors 
        but didn't specify error handling. Should we address that?"
You: "Yes, if validation fails, log errors and notify vendor"
Agent: "Added. I also see no performance requirements. Any SLA needs?"
You: "Process files within 30 minutes"
Agent: "Got it. That's a constraint I'll add. Anything else?"
```

#### 5. Stakeholder Consensus Building
```bash
python tools/interactive_planner_agent.py facilitate "<objective_name>" \
  --stakeholders "tech_lead,architect,product_owner"
```

The agent facilitates multi-party consensus:
```
Agent: "I've analyzed feedback from 3 stakeholders:
       Tech Lead: Concerned about API rate limits (500 calls/hour)
       Architect: Wants async processing for scalability
       Product Owner: Requires 24hr SLA, not 30min
       
       These create conflicts. Let's resolve them:
       - API limit allows ~12K calls/day
       - 24hr SLA gives us flexibility
       - Async processing recommended
       
       Proposed resolution: Async batch processing with 24hr SLA.
       Does this work for everyone?"
```

### Must Include (Auto-Generated by Agent)
- **What must be achieved:** Specific, measurable goals and expected outcomes
- **Out-of-scope boundaries:** Explicitly state what is NOT included
- **Success criteria:** Testable functional and quality criteria
- **Constraints:** Technical, business, time/resource limitations
- **Risk assessment:** Known risks, unknowns, open questions

### Key Point
**The Interactive Planner Agent performs the refinement work WITH you.** Through conversation, it helps you think through implications, identifies gaps you might miss, suggests risks based on patterns, and produces a refined, actionable objective—automating the "assistance in refining" described in development_approach.md.

### Next Step
Once approved by stakeholders → Proceed to **Step 2a**

---

## Step 2a: Overarching Plan (Pipeline-Level)

**Agent:** Interactive Pipeline Planner Agent (`tools/interactive_pipeline_planner_agent.py`)  
**Output:** `docs/roadmaps/<objective_name>_pipeline_plan.md`  
**Workflow:** Step 2a - Overarching Plan (Pipeline-Level)

### Purpose
Create end-to-end pipeline plan showing the complete processing sequence through **interactive architectural discussion**.

### How the Agent Achieves the Intent

Per `development_approach.md`, you must **identify key capabilities**, **define order and dependencies**, and **highlight risks and decision points**. The Interactive Pipeline Planner Agent automates this through architectural conversation:

#### 1. Start Pipeline Design Session
```bash
python tools/interactive_pipeline_planner_agent.py design \
  --objective docs/roadmaps/<objective_name>.md
```

The agent begins architectural discussion:
```
Agent: "I've analyzed your objective: automated vendor onboarding with XML files.
        Let's design the end-to-end pipeline. What are the major processing steps?"
You: "Receive files, validate them, transform data, update PIM"
Agent: "Good start. Let's break that down:
        1. File ingestion - where do files come from?
        2. Schema validation - what schema?
        3. Data transformation - what mapping rules?
        4. PIM integration - which API?
        Does this capture the flow?"
```

#### 2. Automated Capability Identification

**The agent helps identify capabilities through guided analysis:**

**A. Discovering Processing Steps:**
- Agent analyzes objective to suggest initial capabilities
- Agent asks: "What happens first? Then what?"
- Agent prompts: "Any validation or error checking needed?"
- Agent suggests common patterns based on similar pipelines
- Example suggestions:
  ```
  Agent: "For vendor onboarding, I typically see:
         - Ingestion (S3, SFTP, API)
         - Validation (schema, business rules)
         - Transformation (mapping, enrichment)
         - Integration (API calls, database updates)
         - Monitoring (logging, alerts)
         Does this match your needs?"
  ```

**B. Defining Order and Dependencies:**
- Agent asks: "Can any steps run in parallel?"
- Agent identifies: "Step 3 depends on Step 2 output. Correct?"
- Agent maps data flow: "What does each step produce for the next?"
- Agent creates sequence diagram automatically

**C. Decision Point Discovery:**
- Agent asks: "What happens if validation fails?"
- Agent prompts: "Any conditional logic or branching?"
- Agent documents decision trees
- Example:
  ```
  Agent: "If schema validation fails, you have options:
         A) Stop pipeline, notify vendor
         B) Log error, continue with valid records
         C) Queue for manual review
         Which approach?"
  ```

#### 3. Risk and Unknown Identification

**The agent actively identifies risks:**
- Agent suggests common risks: "XML parsing can fail with large files. Size limits?"
- Agent asks: "What external systems could cause failures?"
- Agent prompts: "Any unknowns about data volume or frequency?"
- Agent marks TBDs: "TBD: Retry logic for API failures"

#### 4. Existing Job Analysis
```bash
Agent: "I've scanned your jobs/ directory. Found:
       - jobs/ingestion/s3_reader - could handle Step 1
       - jobs/validation/schema_validator - could handle Step 2
       Do you want to reuse these or create new jobs?"
```

#### 5. Automated Architecture Document Generation

The agent generates complete pipeline plan:
```
✓ Processing sequence (numbered steps, first → last)
✓ Detailed step descriptions (inputs, processing, outputs)
✓ Decision points (conditions and branching logic)
✓ Conceptual artifacts (data passed between steps)
✓ Data flow diagram (automated generation)
✓ Existing job mapping (reuse vs. new development)
✓ Unknowns and open decisions (explicitly marked)
✓ Risk assessment (identified risks per step)
```

#### 6. Architecture Review Facilitation
```bash
python tools/interactive_pipeline_planner_agent.py review \
  --pipeline docs/roadmaps/<objective>_pipeline_plan.md \
  --reviewers "tech_lead,architect"
```

Agent facilitates technical review:
```
Agent: "Tech Lead feedback: 'Consider async processing for scalability'
        Architect feedback: 'Add circuit breaker for PIM API calls'
        
        Should I update the design to include:
        - Async queue between steps 3-4?
        - Circuit breaker pattern for API integration?
        
        This would address both concerns."
```

### Must Include (Auto-Generated by Agent)
- **Processing sequence:** List capabilities/steps in order (first → last)
- **Decision points:** Identify decision logic and fallback paths
- **Conceptual artifacts:** Define artifacts exchanged between steps (names + meaning, NOT S3 paths)
- **Existing job mapping:** State which existing jobs cover which steps
- **Unknowns:** Explicitly mark unknowns and open decisions (no assumptions)

### Key Rule
**DO NOT** define "how" each step works - only define "what" and "sequence"

### Key Point
**The Interactive Pipeline Planner Agent performs architectural planning WITH you.** Through conversation, it helps decompose objectives into capabilities, identifies dependencies and decision points, suggests risks, analyzes existing jobs for reuse, and produces a comprehensive pipeline architecture—automating the "agent assists by creating structured drafts" described in development_approach.md.

### Next Step
Once pipeline plan is approved → Proceed to **Step 2b** for EACH capability

### Key Point
**The Pipeline Planner provides structure; YOU design the architecture.** The capability identification, sequencing, and architectural decisions are MANUAL human activities requiring technical expertise and discussion.

### Next Step
Once pipeline plan is approved → Proceed to **Step 2b** for EACH capability

---

## Step 2b: Capability Plan (Step-Level)

**Agent:** Interactive Capability Planner Agent (`tools/interactive_capability_planner_agent.py`)  
**Output:** `docs/specifications/<capability_name>_capability.yaml`  
**Workflow:** Step 2b - Capability Plan (Step-Level)

### Purpose
Specify ONE capability/step from the pipeline plan in detail through **interactive technical discussion**.

### How the Agent Achieves the Intent

Per `development_approach.md`, the Specification function refines each pipeline step into **purpose, scope, inputs/outputs, and implementation steps**. The Interactive Capability Planner Agent automates this through technical conversation:

#### 1. Start Capability Specification Session
```bash
python tools/interactive_capability_planner_agent.py specify \
  --pipeline docs/roadmaps/<objective>_pipeline_plan.md \
  --step-number 2
```

The agent begins detailed specification:
```
Agent: "You've selected Step 2: Schema Validation from the pipeline.
        Let's define this capability in detail.
        
        What exactly should this capability do?"
You: "Validate vendor XML against our PIM schema"
Agent: "Which schema version? Where is it defined?"
You: "PIM schema v2.1, defined in our schema registry"
Agent: "What happens with invalid data? Fail fast or collect all errors?"
```

#### 2. Automated Purpose and Scope Definition

**The agent helps define what the capability does:**

**A. Purpose Clarification:**
- Agent asks: "Why does this capability exist? What problem does it solve?"
- Agent refines: "So the purpose is: Ensure vendor data quality before transformation"
- Agent documents clearly and concisely

**B. Scope Boundaries:**
- Agent asks: "What does this capability NOT do?"
- Agent prompts: "Does it transform data or only validate?"
- Agent documents explicit boundaries
- Example:
  ```
  Agent: "Clarifying boundaries:
         ✓ DOES: Validate XML structure and content
         ✓ DOES: Generate error reports
         ✗ DOES NOT: Transform or map data
         ✗ DOES NOT: Update PIM system
         Correct?"
  ```

#### 3. Input/Output Specification

**The agent discovers conceptual I/O through conversation:**

**A. Input Discovery:**
- Agent asks: "What data does this capability receive?"
- Agent probes: "What's the expected format and structure?"
- Agent clarifies: "Any data quality assumptions?"
- Agent documents inputs by MEANING, not storage
- Example:
  ```
  Agent: "Inputs identified:
         - Vendor product catalog (XML)
           • Contains: product IDs, descriptions, prices, inventory
           • Source: upstream ingestion step
           • Volume: ~1000-5000 products per file
           • Assumptions: Well-formed XML (checked upstream)
         Correct?"
  ```

**B. Output Discovery:**
- Agent asks: "What does this capability produce?"
- Agent probes: "What happens to valid vs. invalid records?"
- Agent documents both success and failure outputs
- Example:
  ```
  Agent: "Outputs identified:
         - Validated product records (for transformation step)
         - Validation error report (for monitoring/notification)
           • Contains: error type, field, message, record ID
           • Used by: error handling capability
         Correct?"
  ```

#### 4. Business Rules and Logic Specification

**The agent discovers processing requirements:**
- Agent asks: "What validation rules must be enforced?"
- Agent prompts: "Any vendor-specific rules?"
- Agent helps structure rules clearly
- Example:
  ```
  Agent: "Validation rules identified:
         1. Schema compliance (XSD validation)
         2. Required fields: product_id, description, price
         3. Price must be > 0
         4. Product ID must be unique within file
         5. Vendor-specific: Check against vendor contract terms
         
         Any other rules?"
  ```

#### 5. Dependencies and Integration Points

**The agent maps ecosystem connections:**
- Agent asks: "What upstream capabilities provide your inputs?"
- Agent asks: "What downstream capabilities consume your outputs?"
- Agent identifies: "Any external systems or APIs needed?"
- Agent documents dependencies clearly

#### 6. Acceptance Criteria Definition

**The agent helps define testable success criteria:**
- Agent prompts: "How do we know this capability works correctly?"
- Agent suggests: "Should we test with invalid data scenarios?"
- Agent structures criteria as testable statements
- Example:
  ```
  Agent: "Acceptance criteria suggested:
         Functional:
         - Valid records pass validation
         - Invalid records rejected with clear errors
         - Error report contains all validation failures
         
         Quality:
         - Process 5000 records in < 30 seconds
         - 100% of validation rules enforced
         - Zero false positives in validation
         
         Ready to add more?"
  ```

#### 7. Automated YAML Generation

The agent generates complete specification:
```yaml
capability_name: vendor_data_validation
objective: Ensure vendor product data meets PIM quality standards before transformation
scope:
  includes:
    - XML schema validation (XSD)
    - Business rule enforcement
    - Error report generation
  excludes:
    - Data transformation or mapping
    - PIM system updates
    - Vendor notification
inputs:
  - name: vendor_product_catalog
    description: XML file containing vendor product data
    source: xml_ingestion_capability
    structure: Product list with IDs, descriptions, prices, inventory
    assumptions:
      - Well-formed XML
      - File size < 5GB
outputs:
  - name: validated_product_records
    description: Product records that passed all validation
    consumers: [data_transformation_capability]
  - name: validation_error_report
    description: Detailed report of validation failures
    consumers: [error_handling_capability]
business_rules:
  - Schema compliance (PIM XSD v2.1)
  - Required fields: product_id, description, price, inventory
  - Price > 0
  - Product ID unique within file
acceptance_criteria:
  functional:
    - Valid records pass validation
    - Invalid records rejected with errors
    - Error report lists all failures
  quality:
    - Process 5000 records < 30 sec
    - 100% rule enforcement
dependencies:
  upstream: [xml_ingestion_capability]
  downstream: [data_transformation_capability, error_handling_capability]
  external: [pim_schema_registry]
```

#### 8. Technical Review Facilitation
```bash
python tools/interactive_capability_planner_agent.py review \
  --capability docs/specifications/vendor_data_validation.yaml \
  --reviewer tech_lead
```

Agent facilitates spec review:
```
Agent: "Tech Lead feedback: 'Add retry logic for schema registry connection'
        
        Should I add:
        - Dependency note: Schema registry must be available
        - Business rule: Retry up to 3 times with backoff
        - Acceptance criterion: Handles registry unavailability gracefully
        ?"
```

### Must Include (Auto-Generated by Agent)
- **Inputs/outputs:** Define by MEANING, not storage (conceptual, not S3 paths)
- **Business rules and logic:** State rules that must be enforced
- **Acceptance criteria:** Testable functional and quality criteria
- **Boundaries:** Explicitly state what this capability does and does NOT do
- **Dependencies:** Upstream capabilities, downstream consumers, external systems

### Key Rules
- Define inputs/outputs by **meaning**, NOT by S3 location or format details
- Explicitly state boundaries - what this capability does NOT do
- Only proceed after this capability plan is agreed upon

### Key Point
**The Interactive Capability Planner Agent performs technical specification WITH you.** Through conversation, it helps define purpose/scope, discovers inputs/outputs by meaning (not storage), structures business rules, defines testable acceptance criteria, and produces a complete capability specification—automating the "Specification function refines each pipeline step" described in development_approach.md.

### Next Step
Once capability plan is approved → Proceed to **Step 3**

---

## Step 3: Decompose into Development Elements

**Agent:** Interactive Decomposition Agent (`tools/interactive_decomposition_agent.py`)  
**Output:** Development element breakdown  
**Workflow:** Step 3 - Decompose into Development Elements

### Purpose
Break the approved capability into PR-sized development elements through **intelligent code analysis**.

### How the Agent Achieves the Intent

Per `development_approach.md`, this step involves "tasks are implemented, reviewed, iterated on, and integrated." The Interactive Decomposition Agent automates decomposition through repository analysis:

#### 1. Start Decomposition Analysis
```bash
python tools/interactive_decomposition_agent.py decompose \
  --capability docs/specifications/vendor_data_validation.yaml
```

The agent analyzes the capability and repository:
```
Agent: "Analyzing capability: vendor_data_validation
        
        I've scanned your repository structure:
        - jobs/validation/ exists with 3 existing validators
        - Common patterns: PySpark jobs with validation logic
        - Standard structure: glue_script.py + job_manifest.yaml
        
        Suggested decomposition into 3 PRs:
        
        PR 1: Schema Validation Core
        - Create jobs/validation/vendor_schema_validator/glue_script.py
        - Implement XSD validation logic
        - Unit tests
        Estimated size: ~200 lines
        
        PR 2: Business Rules Engine
        - Add business rule validation to glue_script.py
        - Create rule configuration
        - Integration tests
        Estimated size: ~150 lines
        
        PR 3: Error Reporting
        - Add error report generation
        - Create job_manifest.yaml
        - End-to-end tests
        Estimated size: ~100 lines
        
        Does this decomposition make sense?"
```

#### 2. Intelligent Element Sizing

**The agent ensures PR-appropriate sizing:**
- Analyzes complexity of requirements
- Estimates implementation size based on similar code
- Suggests logical groupings
- Ensures each element is independently testable
- Example:
  ```
  Agent: "PR 2 looks large. Should we split it?
         Option A: Keep together (business rules are cohesive)
         Option B: Split by rule type (schema rules vs. business rules)
         
         Based on your codebase patterns, Option A is more maintainable."
  ```

#### 3. Automated Element Specification

**For each element, the agent generates:**

```yaml
element_1:
  name: schema_validation_core
  description: Implement XSD schema validation for vendor product data
  target_paths:
    - jobs/validation/vendor_schema_validator/glue_script.py
    - jobs/validation/vendor_schema_validator/__init__.py
  allowed_changes:
    create:
      - jobs/validation/vendor_schema_validator/glue_script.py
      - jobs/validation/vendor_schema_validator/__init__.py
      - tests/unit/test_schema_validator.py
    modify: []
  acceptance_criteria:
    - XSD validation implemented using lxml library
    - Valid XML passes validation
    - Invalid XML rejected with clear error messages
    - Unit tests cover happy path and error cases
    - Code follows repository Python style guide
  dependencies: []
  estimated_size: 200 lines
  estimated_effort: 4-6 hours

element_2:
  name: business_rules_engine
  description: Add business rule validation (price, required fields, uniqueness)
  target_paths:
    - jobs/validation/vendor_schema_validator/glue_script.py
    - jobs/validation/vendor_schema_validator/rules.py
  allowed_changes:
    create:
      - jobs/validation/vendor_schema_validator/rules.py
      - jobs/validation/vendor_schema_validator/configs/rules.yaml
      - tests/integration/test_business_rules.py
    modify:
      - jobs/validation/vendor_schema_validator/glue_script.py
  acceptance_criteria:
    - Price validation (> 0) implemented
    - Required field checking (product_id, description, price)
    - Product ID uniqueness validation within file
    - Configurable rule definitions
    - Integration tests validate all rules
  dependencies: [element_1]
  estimated_size: 150 lines
  estimated_effort: 3-4 hours
```

#### 4. Dependency Analysis

**The agent discovers implementation order:**
- Analyzes which elements depend on others
- Suggests optimal implementation sequence
- Warns about circular dependencies
- Example:
  ```
  Agent: "Dependency analysis:
         element_1 (schema_validation_core) → no dependencies
         element_2 (business_rules_engine) → depends on element_1
         element_3 (error_reporting) → depends on element_1, element_2
         
         Recommended sequence: 1 → 2 → 3
         
         Can parallelize: None (sequential dependencies)
         Critical path: All elements"
  ```

#### 5. Repository Integration Check

**The agent validates against existing code:**
- Checks for naming conflicts
- Identifies reusable utilities
- Suggests existing patterns to follow
- Example:
  ```
  Agent: "Integration notes:
         - Reuse jobs/validation/common/validator_base.py
         - Follow error format from jobs/validation/schema_validator_v1/
         - Use existing S3 helpers from utils/s3_utils.py
         - Match manifest structure of other validation jobs
         
         Should I update element specs to reference these?"
  ```

#### 6. Iterative Refinement
```bash
python tools/interactive_decomposition_agent.py refine \
  --element element_2
```

Agent helps adjust decomposition:
```
Agent: "Reviewing element_2: business_rules_engine
        
        Concern: This modifies glue_script.py created in element_1.
        Risk: Merge conflicts if element_1 changes during review.
        
        Alternative: Create separate rules module, integrate via config.
        Benefit: Reduces coupling, easier parallel development.
        
        Should I adjust the decomposition?"
```

### Each Element Specifies (Auto-Generated)
- **Target repo paths:** Exact paths to files
- **Allowed changes:** Explicit file list (what CAN be created/modified)
- **Acceptance criteria:** Testable criteria for this specific element
- **Dependencies:** Other elements that must be completed first
- **Size estimates:** Lines of code and effort

### Key Rules
- Each element must fit in ONE pull request
- Define explicit file restrictions
- Acceptance criteria must be verifiable from repo contents
- Minimize dependencies between elements

### Key Point
**The Interactive Decomposition Agent performs intelligent code analysis.** It scans your repository structure, identifies patterns, suggests PR-sized elements, analyzes dependencies, estimates effort, and produces actionable decomposition—automating the task breakdown that enables parallel development.

### Next Step
Once decomposition is approved → Proceed to **Step 4** for EACH element

---

## Step 4: Create Codex Tasks

**Agent:** Interactive Task Generator Agent (`tools/interactive_task_generator_agent.py`)  
**Output:** Complete Codex task with standards enforcement  
**Workflow:** Step 4 - Codex Task Creation

### Purpose
Generate executable Codex task for ONE development element with **automated standards compliance**.

### How the Agent Achieves the Intent

The agent generates actionable Codex tasks by analyzing element specifications and repository standards:

#### 1. Start Task Generation
```bash
python tools/interactive_task_generator_agent.py generate \
  --element element_1
```

The agent analyzes and generates:
```
Agent: "Generating Codex task for element_1: schema_validation_core
        
        Analyzing relevant standards:
        - docs/standards/glue_job_standard.md (for job structure)
        - docs/standards/python_style_guide.md (for code style)
        - docs/standards/testing_standard.md (for test requirements)
        - docs/standards/manifest_standard.md (for job_manifest.yaml)
        
        Generating task..."
```

#### 2. Automated Standards Integration

**The agent automatically includes relevant standards:**
- Scans `docs/standards/` directory
- Identifies applicable standards based on file types
- Includes specific sections from standards
- Generates compliance checklist
- Example:
  ```
  Agent: "Standards included:
         ✓ Glue job structure (glue_script.py requirements)
         ✓ Python PEP 8 compliance
         ✓ Unit test coverage requirements (>80%)
         ✓ Manifest YAML schema validation
         ✓ Documentation requirements
         
         Task will enforce these through quality gates."
  ```

#### 3. Complete Task Generation

The agent generates a comprehensive Codex task:

```markdown
# Codex Task: Implement Schema Validation Core

## Objective
Implement XSD schema validation for vendor product data as specified in capability plan.

## Standards References
This task must comply with:
- `docs/standards/glue_job_standard.md` - Job structure and naming
- `docs/standards/python_style_guide.md` - Code style and formatting
- `docs/standards/testing_standard.md` - Test coverage and quality
- `docs/standards/manifest_standard.md` - Job manifest format

## Target Implementation
**TARGET_SCRIPT:** `jobs/validation/vendor_schema_validator/glue_script.py`

## File Restrictions
**Allowed Changes:**
- CREATE: `jobs/validation/vendor_schema_validator/glue_script.py`
- CREATE: `jobs/validation/vendor_schema_validator/__init__.py`
- CREATE: `jobs/validation/vendor_schema_validator/job_manifest.yaml`
- CREATE: `tests/unit/test_schema_validator.py`
- MODIFY: None

**Prohibited:**
- No modifications to existing jobs
- No changes outside validation/ directory
- No dependency updates without approval

## Requirements from Capability Plan
From `docs/specifications/vendor_data_validation.yaml`:
- Validate against PIM XSD schema v2.1
- Accept XML input (vendor product catalog)
- Produce validated records output
- Generate error report for invalid records
- Handle schema registry connection

## Acceptance Criteria
**Functional:**
- [ ] XSD validation implemented using lxml library
- [ ] Valid XML passes validation
- [ ] Invalid XML rejected with detailed error messages
- [ ] Error report includes: field, error type, message, record ID
- [ ] Handles schema registry unavailability (retry 3x)

**Quality:**
- [ ] Unit test coverage >80%
- [ ] All tests pass
- [ ] Code follows Python style guide (PEP 8)
- [ ] No linting errors
- [ ] Job manifest valid per standard

**Documentation:**
- [ ] Inline code comments for complex logic
- [ ] Docstrings for all functions
- [ ] Job manifest documents inputs/outputs

## Quality Gates
**Must pass before PR approval:**
```bash
# Standards validation
python tools/validate_repo_docs.py --all

# Python linting
pylint jobs/validation/vendor_schema_validator/glue_script.py

# Unit tests
pytest tests/unit/test_schema_validator.py --cov

# Manifest validation
python tools/validate_manifest.py jobs/validation/vendor_schema_validator/job_manifest.yaml
```

## Boundaries (What NOT to do)
- Do NOT implement business rule validation (that's element_2)
- Do NOT implement error reporting infrastructure (that's element_3)
- Do NOT add data transformation logic
- Do NOT modify existing validator code

## Implementation Guidance
**Recommended approach:**
1. Start with minimal XSD validation
2. Add error message formatting
3. Implement retry logic for schema registry
4. Write comprehensive unit tests
5. Create job manifest

**Reusable code:**
- Use `jobs/validation/common/validator_base.py` as template
- Follow error format from `jobs/validation/schema_validator_v1/`
- Use S3 helpers from `utils/s3_utils.py`

## Dependencies
**This element has no dependencies** - implement first.

## Next Steps After Completion
1. Create PR with changes
2. Ensure all quality gates pass
3. Request review from technical lead
4. After merge, proceed to element_2 (business_rules_engine)
```

#### 4. Task Validation

**The agent validates task completeness:**
```bash
python tools/interactive_task_generator_agent.py validate \
  --task element_1_task.md
```

Agent checks:
```
Agent: "Validating task completeness:
        ✓ Standards referenced
        ✓ TARGET_SCRIPT specified
        ✓ File restrictions explicit
        ✓ Quality gates defined
        ✓ Acceptance criteria measurable
        ✓ Boundaries clear
        ✓ Dependencies documented
        
        Task is complete and ready for execution."
```

### Codex Task Includes (Auto-Generated)
- **Standards references:** All relevant specs from `docs/standards/`
- **TARGET_SCRIPT:** Primary file path explicitly stated
- **File restrictions:** Explicit allow-list of files
- **Quality gates:** Automated checks from repo
- **Acceptance criteria:** From decomposition + capability plan
- **Boundaries:** What this element does NOT do
- **Implementation guidance:** Reusable code and patterns

### Key Rules
- Reference standards under `docs/standards/`
- Use TARGET_SCRIPT pattern - state primary file ONCE
- Restrict edits to explicit file set only
- Include quality gates: `validate_repo_docs.py`, syntax checks, etc.
- Do NOT allow modification of working code outside the allowed list

### Key Point
**The Interactive Task Generator Agent creates executable tasks WITH standards enforcement.** It analyzes repository standards, generates compliance checklists, includes quality gates, provides implementation guidance, and produces actionable Codex tasks—automating task definition with built-in quality assurance.

### Next Step
Use Codex task to create PR → Proceed to **Step 5**

---

## Step 5: Code Creation and Review

**Agent:** AI Code Assistant (GitHub Copilot, Codex, or manual)  
**Supporting Agent:** Automated Review Agent (`tools/automated_review_agent.py`)  
**Output:** Pull Request with code changes  
**Workflow:** Step 5 - Code Implementation

### Purpose
Implement the code changes defined in the Codex task with **automated quality checks and review support**.

### How Automated Review Agent Assists

The Automated Review Agent provides continuous feedback during development:

#### 1. Pre-Implementation Checks
```bash
python tools/automated_review_agent.py pre-check \
  --task element_1_task.md
```

Agent verifies readiness:
```
Agent: "Pre-implementation check:
        ✓ Codex task complete
        ✓ Dependencies satisfied (element has no dependencies)
        ✓ Target paths don't conflict with in-progress work
        ✓ Repository up to date
        
        Ready to begin implementation."
```

#### 2. Continuous Quality Monitoring

As code is written, the agent monitors:
```bash
# Run in watch mode during development
python tools/automated_review_agent.py watch \
  --paths jobs/validation/vendor_schema_validator/
```

Agent provides real-time feedback:
```
Agent: "Quality check triggered (file saved):
        Checking glue_script.py:
        ✓ Python syntax valid
        ✓ Imports resolved
        ⚠ Warning: Function validate_xml() lacks docstring
        ✓ Line length within limits
        ⚠ Warning: Test coverage currently 45% (target: 80%)
        
        Continue developing - warnings will be addressed before PR."
```

#### 3. Pre-PR Quality Gate
```bash
python tools/automated_review_agent.py review \
  --element element_1
```

Agent runs comprehensive checks:
```
Agent: "Running quality gates:
        
        Standards Validation:
        ✓ docs/standards/ compliance checked
        ✓ Job structure matches glue_job_standard.md
        ✓ Manifest valid per manifest_standard.md
        
        Code Quality:
        ✓ Python linting passed (pylint score: 9.2/10)
        ✓ No syntax errors
        ✓ PEP 8 compliance
        
        Testing:
        ✓ Unit tests exist
        ✓ Test coverage: 85% (exceeds 80% requirement)
        ✓ All tests pass (12/12)
        
        File Restrictions:
        ✓ Only allowed files modified
        ✓ No changes outside element scope
        
        Documentation:
        ✓ Function docstrings present
        ✓ Inline comments for complex logic
        ✓ Job manifest complete
        
        Acceptance Criteria:
        ✓ 5/5 functional criteria met
        ✓ 3/3 quality criteria met
        ✓ 3/3 documentation criteria met
        
        RESULT: All quality gates PASSED
        Ready to create PR."
```

#### 4. Automated PR Feedback

After PR creation, agent provides review comments:
```bash
# Triggered automatically on PR creation
python tools/automated_review_agent.py pr-review \
  --pr-number 123
```

Agent comments on PR:
```
Agent: "Automated Review Feedback:
        
        ✅ Overall: APPROVED - All quality gates passed
        
        Code Quality: EXCELLENT
        - Clean implementation of XSD validation
        - Good error handling
        - Proper use of lxml library
        
        Suggestions (optional improvements):
        1. Consider caching schema object for performance
        2. Add logging for schema registry retries
        3. Error messages could include XPath to invalid element
        
        Testing: EXCELLENT
        - Comprehensive test coverage (85%)
        - Edge cases covered (empty file, malformed XML, network errors)
        
        Standards Compliance: PERFECT
        - All repository standards met
        - Follows existing patterns
        
        Ready for human review and merge."
```

### Requirements
- Follow the Codex task strictly
- Modify ONLY files in the allowed list
- Pass ALL quality gates before PR submission
- Include tests where applicable

### Quality Gates (Must Pass)
**Automated checks before PR creation:**
- Repository standards validation
- Code linting and syntax
- Test coverage (>80%)
- All tests passing
- File restriction compliance
- Acceptance criteria verification

**See:** `agent_tools_reference.md` for specific validation commands

### PR Review Process
1. Create PR with code changes
2. Automated Review Agent provides initial feedback
3. All automated quality gates must pass
4. Human code review by team
5. Address feedback iteratively
6. Merge to main after approvals

### Key Point
**The Automated Review Agent provides continuous quality feedback.** It monitors code quality during development, runs comprehensive pre-PR checks, ensures standards compliance, verifies acceptance criteria, and provides detailed PR review comments—automating quality assurance while humans focus on design and logic.

### Next Step
After merge → Proceed to **Step 6** (Documentation Update)

---

## Step 6: Documentation Update

**Agent:** Automated Documentation Agent (`tools/automated_documentation_agent.py`)  
**Output:** Updated documentation reflecting code changes  
**Workflow:** Step 6 - Documentation Maintenance

### Purpose
Automatically update documentation to reflect merged code changes.

### How the Agent Achieves the Intent

Per `development_approach.md`, Step 5 includes "update necessary documentation to ensure clarity and completeness." The Automated Documentation Agent handles this:

#### 1. Post-Merge Documentation Analysis
```bash
# Triggered automatically after PR merge
python tools/automated_documentation_agent.py analyze \
  --pr-number 123
```

Agent analyzes impact:
```
Agent: "Analyzing PR #123: schema_validation_core
        
        Code changes detected:
        - New job: jobs/validation/vendor_schema_validator/
        - New capability: vendor data validation
        
        Documentation updates needed:
        1. docs/job_inventory.md - Add new job entry
        2. docs/artifacts_catalog.md - Add validation outputs
        3. docs/script_cards/vendor_schema_validator.md - Create new
        4. README.md - Update capabilities list
        
        Should I generate these updates?"
```

#### 2. Automated Documentation Generation

**The agent generates documentation updates:**

```bash
python tools/automated_documentation_agent.py generate \
  --pr-number 123
```

Agent creates updates:
```
Agent: "Generating documentation updates:
        
        1. Updating docs/job_inventory.md:
           Added entry:
           - jobs/validation/vendor_schema_validator
           - Purpose: Validate vendor XML against PIM schema
           - Inputs: vendor_product_catalog (XML)
           - Outputs: validated_records, validation_errors
        
        2. Updating docs/artifacts_catalog.md:
           Added artifacts:
           - validated_product_records (from schema validation)
           - validation_error_report (for monitoring)
        
        3. Creating docs/script_cards/vendor_schema_validator.md:
           Generated complete script card with:
           - Purpose, inputs, outputs
           - Parameters, configuration
           - Error handling, monitoring
        
        4. Updating README.md:
           Added to capabilities:
           - Vendor data validation (XSD schema enforcement)
        
        Review these updates?"
```

#### 3. Documentation Consistency Checks

**The agent validates documentation quality:**
```bash
python tools/automated_documentation_agent.py validate
```

Agent ensures consistency:
```
Agent: "Validating documentation updates:
        
        Cross-Reference Checks:
        ✓ Job inventory links to script card
        ✓ Artifacts catalog matches job manifest
        ✓ Script card matches actual job code
        ✓ README accurately describes capability
        
        Format Compliance:
        ✓ Script card follows standard template
        ✓ Markdown formatting correct
        ✓ No broken internal links
        
        Completeness:
        ✓ All required sections present
        ✓ Examples provided where needed
        ✓ No TODOs or placeholders
        
        Documentation updates ready for PR."
```

#### 4. Automated Documentation PR

Agent creates documentation PR:
```
Agent: "Creating documentation PR:
        
        PR Title: Update docs for vendor schema validator
        
        Changes:
        - docs/job_inventory.md (1 entry added)
        - docs/artifacts_catalog.md (2 artifacts added)
        - docs/script_cards/vendor_schema_validator.md (new file)
        - README.md (1 capability added)
        
        All documentation changes linked to PR #123.
        
        Requesting review from documentation maintainers."
```

### Documentation Agent Handles
- Job inventory updates
- Artifacts catalog maintenance
- Script card generation
- README capability lists
- Cross-reference validation
- Format compliance checking

### Key Point
**The Automated Documentation Agent maintains documentation automatically.** It analyzes code changes, identifies documentation needs, generates updates following repository standards, validates consistency, and creates documentation PRs—ensuring documentation stays synchronized with code changes without manual effort.

---

## Workflow Enforcement Rules

### Two Planning Layers Required
Before ANY code change:
1. **Step 2a must be completed and approved** (pipeline-level plan)
2. **Step 2b must be completed and approved** (capability-level plan)

### No Assumptions
- All unknowns must be explicitly marked
- Open decisions must be documented
- DO NOT proceed with assumptions - clarify first

### Explicit Boundaries
At every step, explicitly state:
- What IS included
- What is NOT included
- What is deferred to other capabilities/steps

### Evidence-Based
- Map existing jobs to pipeline steps where applicable
- Define artifacts by meaning (what they represent)
- Storage details (S3 paths) come LATER in implementation

---

## Quick Reference

| Step | Agent | Command | Output |
|------|-------|---------|--------|
| 1 | Planner | `planner_agent.py create` | `docs/roadmaps/<objective>.md` |
| 2a | Pipeline Planner | `pipeline_planner_agent.py create` | `docs/roadmaps/<objective>_pipeline_plan.md` |
| 2b | Capability Planner | `capability_planner_agent.py create` | `docs/specifications/<capability>_capability.yaml` |
| 3 | Coding (decompose) | `coding_agent.py decompose` | Console output (suggested elements) |
| 4 | Coding (codex-task) | `coding_agent.py codex-task` | Console output (Codex task) |
| 5 | Manual/Copilot | Standard PR process | Pull Request |

---

## Example Flow

For detailed command syntax and complete example workflow, see:
- `agent_tools_reference.md` - CLI command reference
- `agent_workflow_templates.md` - Step-by-step workflow examples

---

## Benefits of This Workflow

1. **Two planning layers** prevent jumping to implementation too early
2. **Explicit boundaries** prevent scope creep
3. **Testable criteria** enable objective validation
4. **Small elements** reduce PR complexity and review time
5. **Quality gates** ensure standards compliance
6. **No assumptions** - all unknowns explicitly documented

---

## See Also

- `AGENTS_SETUP.md` - Agent installation and setup guide
- `agent_tools_reference.md` - Detailed CLI command reference
- `agent_workflow_templates.md` - Example workflow templates
- `docs/context_packs/agent_system_context.md` - Agent governance and integration
- `docs/standards/` - Repository standards
- `docs/context_packs/system_context.md` - Repository context

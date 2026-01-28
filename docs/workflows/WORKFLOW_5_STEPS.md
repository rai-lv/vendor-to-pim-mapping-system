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

**Agent:** Capability Planner Agent (`tools/capability_planner_agent.py`)  
**Output:** `docs/specifications/<capability_name>_capability.yaml`  
**Workflow:** Step 2b - Capability Plan (Step-Level)

### Purpose
Specify ONE capability/step from the pipeline plan in detail.

### Must Include
- **Inputs/outputs:** Define by MEANING, not storage (conceptual, not S3 paths)
- **Business rules and logic:** State rules that must be enforced
- **Acceptance criteria:** Testable functional and quality criteria
- **Boundaries:** Explicitly state what this capability does and does NOT do
- **Dependencies:** Upstream capabilities, downstream consumers, external systems

### Usage
See `agent_tools_reference.md` for detailed CLI syntax and options.

### Key Rules
- Define inputs/outputs by **meaning**, NOT by S3 location or format details
- Explicitly state boundaries - what this capability does NOT do
- Only proceed after this capability plan is agreed upon

### Next Step
Once capability plan is approved → Proceed to **Step 3**

---

## Step 3: Decompose into Development Elements

**Agent:** Coding Agent (`tools/coding_agent.py decompose`)  
**Output:** Suggested decomposition (console output)  
**Workflow:** Step 3 - Decompose into Development Elements

### Purpose
Break the approved capability into elements small enough for ONE PR each.

### Each Element Must Specify
- **Target repo paths:** Exact paths to files
- **Allowed changes:** Explicit file list (what CAN be created/modified)
- **Acceptance criteria:** Testable criteria for this specific element
- **Dependencies:** Other elements that must be completed first

### Usage
See `agent_tools_reference.md` for detailed CLI syntax and options.

### Key Rules
- Each element must fit in ONE pull request
- Define explicit file restrictions
- Acceptance criteria must be verifiable from repo contents
- Minimize dependencies between elements

### Next Step
Review decomposition → Adjust as needed → Proceed to **Step 4** for each element

---

## Step 4: Create Codex Tasks

**Agent:** Coding Agent (`tools/coding_agent.py codex-task`)  
**Output:** Codex task outline (console output)  
**Workflow:** Step 4 - Codex Task Creation

### Purpose
Generate a Codex task for ONE development element with all requirements.

### Codex Task Must Include
- **Standards references:** List ALL relevant specs from `docs/standards/`
- **TARGET_SCRIPT:** State target file path ONCE explicitly
- **File restrictions:** Explicit allow-list of files that can be changed
- **Quality gates:** Checks that can be run from repo contents
- **Acceptance criteria:** From decomposition + capability plan
- **Boundaries:** What this element does NOT do

### Usage
See `agent_tools_reference.md` for detailed CLI syntax and options.

### Key Rules
- Reference standards under `docs/standards/`
- Use TARGET_SCRIPT pattern - state primary file ONCE
- Restrict edits to explicit file set only
- Include quality gates: `validate_repo_docs.py`, syntax checks, etc.
- Do NOT allow modification of working code outside the allowed list

### Next Step
Use Codex task to create PR → Proceed to **Step 5**

---

## Step 5: Code Creation

**Process:** Standard PR workflow  
**Tool:** GitHub Copilot / Manual development  
**Output:** Pull Request with code changes

### Purpose
Implement the code changes defined in the Codex task.

### Requirements
- Follow the Codex task strictly
- Modify ONLY files in the allowed list
- Pass ALL quality gates before PR submission
- Include tests where applicable

### Quality Gates (Must Pass)
See `agent_tools_reference.md` for specific validation commands and quality gate procedures.

### PR Review Process
1. Automated tests run (Testing Agent)
2. Code review by team
3. All quality gates must pass
4. Merge to main

### Next Step
After merge → Update documentation (Documentation Agent)

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

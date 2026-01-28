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

**Agent:** Planner Agent (`tools/planner_agent.py`)  
**Output:** `docs/roadmaps/<objective_name>.md`  
**Workflow:** Step 1 - Define Objective

### Purpose
Define what must be achieved with explicit boundaries and testable success criteria.

### How to Achieve the Intent (Refinement Process)

Per `development_approach.md`, the Planning function supports you in **refining the objective** and **ensuring it is actionable**. Here's the process:

#### 1. Generate Initial Template
Use the Planner Agent tool to generate a structured template:
```bash
python tools/planner_agent.py create "<objective_name>" \
  --description "<brief description>"
```

#### 2. Manual Refinement Process (Required)

**The tool only generates an empty template. YOU must perform the refinement work:**

**A. Refine the Objective to be Actionable:**
- Read your initial description (e.g., "I want to update products automatically")
- Ask yourself: What SPECIFICALLY needs to happen?
- Break down vague statements into concrete actions
- Example refinement:
  - Before: "Update products automatically"
  - After: "Implement automated vendor onboarding pipeline that ingests XML files, validates against PIM schema, transforms data, and updates products via PIM API v2.1"

**B. Ensure Context for Subsequent Steps:**
- Document WHY this objective exists (business context)
- Define WHAT success looks like (measurable outcomes)
- Specify WHAT is out of scope (boundaries to prevent scope creep)

**C. Identify Constraints, Unknowns, and Risks:**

**Constraints** (conduct analysis and discussions):
- Technical: What existing systems/APIs must you use? (e.g., "Must use PIM API v2.1")
- Business: What are the deadlines, budgets, compliance requirements?
- Resources: What team size, time allocation, infrastructure limits?

**Unknowns** (mark explicitly as TBD):
- What don't you know yet? (e.g., "TBD: Average file size - need baseline data")
- What decisions haven't been made? (e.g., "OPEN QUESTION: Batch vs. real-time processing")

**Risks** (think through potential issues):
- What could go wrong? (e.g., "API rate limits could cause delays")
- What's the impact and likelihood?
- How would you mitigate?

#### 3. Stakeholder Discussion
- Share the refined objective with stakeholders
- Facilitate discussion to reach consensus
- Iterate based on feedback
- Resolve disagreements on scope, constraints, priorities

#### 4. Validation
Validate the refined objective:
```bash
python tools/planner_agent.py validate docs/roadmaps/<objective_name>.md
```
This checks structure, but YOU ensure the CONTENT is actionable.

### Must Include
- **What must be achieved:** Specific, measurable goals and expected outcomes
- **Out-of-scope boundaries:** Explicitly state what is NOT included
- **Success criteria:** Testable functional and quality criteria
- **Constraints:** Technical, business, time/resource limitations
- **Risk assessment:** Known risks, unknowns, open questions

### Key Point
**The Planner Agent provides structure; YOU provide the thinking.** The refinement, analysis, discussion, and consensus-building are MANUAL human activities. The tool validates format, not quality.

### Next Step
Once approved by stakeholders → Proceed to **Step 2a**

---

## Step 2a: Overarching Plan (Pipeline-Level)

**Agent:** Pipeline Planner Agent (`tools/pipeline_planner_agent.py`)  
**Output:** `docs/roadmaps/<objective_name>_pipeline_plan.md`  
**Workflow:** Step 2a - Overarching Plan (Pipeline-Level)

### Purpose
Create end-to-end pipeline plan showing the complete processing sequence.

### How to Achieve the Intent (Planning Process)

Per `development_approach.md`, you must **identify key capabilities**, **define order and dependencies**, and **highlight risks and decision points**. Here's the process:

####1. Generate Pipeline Template
```bash
python tools/pipeline_planner_agent.py create \
  --objective docs/roadmaps/<objective_name>.md
```

#### 2. Manual Planning Process (Required)

**The tool only generates structure. YOU must do the architectural planning:**

**A. Identify Key Capabilities:**
- Review your objective document
- Break down the objective into discrete processing steps
- Think: What are the major chunks of work?
- Example from "vendor onboarding":
  - Step 1: XML Ingestion (read files from source)
  - Step 2: Schema Validation (check against PIM schema)
  - Step 3: Data Transformation (map vendor format to PIM format)
  - Step 4: PIM API Integration (update products)
  - Step 5: Error Handling (log failures, notify vendors)

**B. Define Order and Dependencies:**
- Sequence the steps: What must happen first?
- Identify data flow: What does each step consume/produce?
- Define dependencies: Which steps depend on others?
- Document decision points: Where does logic branch?
  - Example: "If schema validation fails → error handling path (no PIM update)"

**C. Highlight Risks and Decision Points:**
- **Decision Points** (where logic branches):
  - What conditions trigger different paths?
  - What are the alternative flows?
- **Risks** (what could go wrong):
  - Where could the pipeline fail?
  - What external dependencies exist?
- **Unknowns** (what needs investigation):
  - Mark with TBD or OPEN QUESTION
  - Example: "TBD: Retry logic for PIM API failures"

#### 3. Architecture Discussion
- Review with technical lead and architect
- Discuss trade-offs (batch vs. streaming, sync vs. async, etc.)
- Validate against objective constraints
- Adjust based on feedback

#### 4. Existing Job Mapping
- Identify which existing AWS Glue jobs can be reused
- Determine which capabilities need new development
- Document the mapping

### Must Include
- **Processing sequence:** List capabilities/steps in order (first → last)
- **Decision points:** Identify decision logic and fallback paths
- **Conceptual artifacts:** Define artifacts exchanged between steps (names + meaning, NOT S3 paths)
- **Existing job mapping:** State which existing jobs cover which steps
- **Unknowns:** Explicitly mark unknowns and open decisions (no assumptions)

### Key Rule
**DO NOT** define "how" each step works - only define "what" and "sequence"

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

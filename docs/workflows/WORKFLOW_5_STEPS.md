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

### Must Include
- **What must be achieved:** Specific, measurable goals and expected outcomes
- **Out-of-scope boundaries:** Explicitly state what is NOT included
- **Success criteria:** Testable functional and quality criteria
- **Constraints:** Technical, business, time/resource limitations
- **Risk assessment:** Known risks, unknowns, open questions

### Usage
```bash
python tools/planner_agent.py create "vendor_onboarding" \
  --description "Implement vendor onboarding pipeline"
```

### Next Step
Once approved by stakeholders → Proceed to **Step 2a**

---

## Step 2a: Overarching Plan (Pipeline-Level)

**Agent:** Pipeline Planner Agent (`tools/pipeline_planner_agent.py`)  
**Output:** `docs/roadmaps/<objective_name>_pipeline_plan.md`  
**Workflow:** Step 2a - Overarching Plan (Pipeline-Level)

### Purpose
Create end-to-end pipeline plan showing the complete processing sequence.

### Must Include
- **Processing sequence:** List capabilities/steps in order (first → last)
- **Decision points:** Identify decision logic and fallback paths
- **Conceptual artifacts:** Define artifacts exchanged between steps (names + meaning, NOT S3 paths)
- **Existing job mapping:** State which existing jobs cover which steps
- **Unknowns:** Explicitly mark unknowns and open decisions (no assumptions)

### Usage
```bash
python tools/pipeline_planner_agent.py create "vendor_onboarding" \
  --objective-ref "vendor_onboarding.md"
```

### Key Rule
**DO NOT** define "how" each step works - only define "what" and "sequence"

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
```bash
python tools/capability_planner_agent.py create "data_ingestion" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"
```

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
```bash
python tools/coding_agent.py decompose data_ingestion_capability
```

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
```bash
python tools/coding_agent.py codex-task data_ingestion_capability 1
```

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
```bash
# Repository validation
python tools/validate_repo_docs.py --all

# Python syntax (if applicable)
python -m py_compile <target_file>

# Best practices check
python tools/coding_agent.py check
```

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

```bash
# Step 1: Define objective
python tools/planner_agent.py create "vendor_onboarding"

# Edit and approve objective document
vim docs/roadmaps/vendor_onboarding.md

# Step 2a: Create pipeline plan
python tools/pipeline_planner_agent.py create "vendor_onboarding" \
  --objective-ref "vendor_onboarding.md"

# Edit and approve pipeline plan
vim docs/roadmaps/vendor_onboarding_pipeline_plan.md

# Step 2b: Create capability plan for first step
python tools/capability_planner_agent.py create "data_ingestion" \
  --pipeline-ref "vendor_onboarding_pipeline_plan.md"

# Edit and approve capability plan
vim docs/specifications/data_ingestion_capability.yaml

# Step 3: Decompose into elements
python tools/coding_agent.py decompose data_ingestion_capability

# Step 4: Create Codex task for element 1
python tools/coding_agent.py codex-task data_ingestion_capability 1

# Step 5: Create PR using Codex task
# (Use GitHub Copilot or manual development)
```

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

- `AGENTS_SETUP.md` - Agent usage details
- `docs/standards/` - Repository standards
- `docs/context_packs/system_context.md` - Repository context

# Roadmaps

This directory contains planning documents created during **Step 1** and **Step 2a** of the 5-step development workflow.

## Purpose

Roadmaps define business objectives and pipeline-level architecture for development initiatives. They serve as authoritative planning documents that guide all downstream work.

## Document Types

### 1. Objective Definitions (Step 1)

**Created by:** Planner Agent  
**File Pattern:** `<objective_name>.md`  
**Purpose:** Define what must be achieved with explicit boundaries and testable success criteria

**Contents:**
- Objective statement and expected outcomes
- Out-of-scope boundaries
- Success criteria (functional and quality)
- Constraints (technical, business, resource)
- Risk assessment and unknowns
- Dependencies

**Example:** `vendor_onboarding.md`

### 2. Pipeline Plans (Step 2a)

**Created by:** Pipeline Planner Agent  
**File Pattern:** `<objective_name>_pipeline_plan.md`  
**Purpose:** Define end-to-end processing sequence with decision points and conceptual artifacts

**Contents:**
- Processing sequence (ordered list of capabilities)
- Decision points and fallback paths
- Conceptual artifacts (by meaning, not storage)
- Existing job mapping
- Unknowns and open decisions

**Example:** `vendor_onboarding_pipeline_plan.md`

## Creating Planning Documents

### Step 1: Create Objective Definition

```bash
# Via Planner Agent
python tools/planner_agent.py create "objective_name" \
  --description "Brief objective description"

# Output: docs/roadmaps/objective_name.md
```

### Step 2a: Create Pipeline Plan

```bash
# Via Pipeline Planner Agent (requires approved Step 1)
python tools/pipeline_planner_agent.py create "objective_name" \
  --objective-ref "objective_name.md"

# Output: docs/roadmaps/objective_name_pipeline_plan.md
```

## Workflow Integration

Planning documents follow the **5-step development workflow**:

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan / Pipeline-Level (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓ [Creates specifications in docs/specifications/]
```

**See:** `docs/workflows/WORKFLOW_5_STEPS.md` for complete workflow details

## Key Principles

1. **Manual Discussion Required:** All planning documents require stakeholder review and approval
2. **No Assumptions:** Explicitly mark unknowns and open decisions
3. **Evidence-Based:** Reference existing jobs and capabilities where applicable
4. **Sequential Execution:** Complete and approve each step before proceeding
5. **Testable Criteria:** All success criteria must be objectively verifiable

## Directory Contents

Each planning initiative produces:
- One objective definition document (Step 1)
- One or more pipeline plan documents (Step 2a)
- Referenced by capability specifications in `docs/specifications/` (Step 2b)

## Listing Planning Documents

```bash
# List all objectives
python tools/planner_agent.py list

# List all pipeline plans
python tools/pipeline_planner_agent.py list
```

## Validation

Planning documents should be reviewed for:
- Clear, testable success criteria
- Explicit boundaries (what IS and is NOT included)
- Identified unknowns and open decisions
- Alignment with repository standards
- Consensus among stakeholders

## Related Documentation

- **Complete Workflow:** `docs/workflows/WORKFLOW_5_STEPS.md`
- **Agent System:** `docs/context_packs/agent_system_context.md`
- **Agent Setup:** `docs/workflows/AGENTS_SETUP.md`
- **Specifications:** `docs/specifications/README.md` (Step 2b outputs)
- **Repository Context:** `docs/context_packs/system_context.md`

## Best Practices

1. **Start with Step 1:** Always create objective definition before pipeline plan
2. **Get Approval:** Ensure stakeholder consensus before proceeding to next step
3. **Document Unknowns:** Mark unknowns explicitly - do not assume or guess
4. **Map Existing Jobs:** Identify reusable jobs to minimize new development
5. **Focus on "What" not "How":** Pipeline plans define sequence, not implementation details

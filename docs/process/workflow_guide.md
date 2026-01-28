# Workflow Guide: 5-Step Execution

## Purpose statement
This document is the **runbook** for executing the 5-step working approach.
It makes the approach **repeatable** by defining:
- step entry/exit criteria (human-checkable),
- how iteration within a step works,
- where human approvals happen,
- how agents and tools are used without role drift,
- how to handle conflicts and re-homing without creating “double truth”.

## Scope and non-goals
**In scope:** execution procedures and checkpoints.

**Out of scope:** templates/schemas/required fields, tool/CLI manuals, and troubleshooting. Those belong to standards and ops documents.

## Inputs this guide assumes exist
- An approved **Development Approach** (principles + 5-step intent).
- An approved **Target Agent System** (agents vs tools, approval gates, evidence discipline, conflict handling).
- A **Documentation System Catalog** (document types, boundaries, canonical placement).
- A **Glossary** (canonical term meanings).

---

## 0) Choose the correct execution path (Quickstart)

Use this section first. It prevents “random walk” execution.

### Path A — Clarify or improve existing documentation (no meaning change)
Use when:
- wording, readability, navigation, structure improve,
- but intent/requirements/rules do not change.

Run:
1) Identify affected document type and canonical home.
2) Apply edit.
3) Run a consistency scan (see Section 6).
4) Human approves “no meaning change”.

### Path B — Introduce or change meaning (intent, rules, or responsibilities)
Use when:
- a definition changes,
- a role boundary changes,
- approval/evidence expectations change,
- a contract or document type is added/removed.

Run:
1) Determine which step artifact is affected (Objective / Pipeline / Capability / Execution / Validation).
2) Re-run the relevant step(s) below until exit criteria are met.
3) Human approves the changed meaning before implementation depends on it.

### Path C — Re-home content (fix layer placement; meaning unchanged)
Use when:
- content currently lives in the wrong layer (e.g., ops manual inside context),
- but the content is still valid and should not change.

Run:
1) Identify the canonical target document type.
2) Move content verbatim.
3) Replace source with a pointer.
4) Human approves “meaning unchanged”.

### Path D — Resolve contradiction (intent vs rules vs runtime vs evidence)
Use when:
- approved intent conflicts with implemented behavior,
- standards conflict with an artifact,
- evidence contradicts claims.

Run:
1) Stop work.
2) Classify the conflict (see Section 7).
3) Human decides resolution path.
4) Apply resolution and record approval.

---

## 1) Operating loop (how iteration works)

Every step follows the same loop:

1) Draft the step output (human and/or agent-supported).
2) Review against step exit criteria.
3) Iterate until exit criteria pass **or** escalation trigger fires.
4) Human approval gate: approve the step output.
5) Proceed to the next step.

**Rule:** Iteration is allowed within a step. Progressing to the next step is not allowed without approval.

---

## 2) Step 1 — Define the Objective

**Agent support:** Objective Support Agent (see target_agent_system.md).

### Practical goal
Produce an objective that is “implementable enough” to plan a pipeline.

### Entry criteria
- A human-owned problem statement or desired outcome exists.

### What to do
1) Write the objective in one clear paragraph.
2) Add:
   - success criteria (how you will know it’s achieved),
   - scope boundaries (what is explicitly out-of-scope).
3) List unknowns:
   - keep as explicit unknowns, or
   - convert to controlled assumptions only with explicit approval.

### Exit criteria (human-checkable)
- Success criteria exist and are evaluable.
- Scope boundaries exist (in-scope/out-of-scope is unambiguous).
- Unknowns are explicitly listed (not hidden).
- No downstream implementation details are embedded here.

### Approval gate
- Human approves the objective artifact.

### Escalation triggers
- Scope cannot be bounded.
- Success criteria cannot be evaluated.
- Critical unknowns would block pipeline planning but are not acknowledged.

---

## 3) Step 2 — Plan the Pipeline

**Agent support:** Pipeline Support Agent (see target_agent_system.md).

### Practical goal
Translate the objective into an ordered list of capabilities with clear boundaries.

### Entry criteria
- Objective artifact is approved.

### What to do
1) List the capabilities needed to satisfy the success criteria.
2) Order them (only as far as you can justify).
3) Mark decision points / dependencies that must be resolved before Step 4.

### Exit criteria (human-checkable)
- Each capability has a short purpose line and a clear boundary.
- The list is ordered sufficiently to start capability planning.
- Known decision points/dependencies are explicitly surfaced (not implied).
- The pipeline does not expand beyond objective scope.

### Approval gate
- Human approves the pipeline plan.

### Escalation triggers
- Capabilities overlap so heavily that boundaries are unclear.
- Ordering depends on unresolved assumptions not approved or stated.
- Pipeline introduces out-of-scope elements.

---

## 4) Step 3 — Capability Planning (and codable tasks)

**Agent support:** Capability Support Agent (see target_agent_system.md).

### Practical goal
Make one capability implementable without uncontrolled decomposition.

### Entry criteria
- Pipeline plan is approved.
- A single capability is selected.

### What to do
1) Define capability boundaries:
   - what it must do, and what it must not do.
2) Define acceptance criteria (minimal and evaluable).
3) Define inputs and outputs at a level that supports implementation decisions.
4) Decompose into **codable tasks**:
   - tasks must be individuable and bounded,
   - each task has a clear intended outcome,
   - task dependencies are explicit.
5) Surface unknowns/assumptions and stop if unapproved assumptions would be required.

### Exit criteria (human-checkable)
- Capability boundary is unambiguous.
- Acceptance criteria are evaluable.
- Tasks are bounded (no “do everything” task) and cover the capability.
- Unknowns/assumptions are explicitly handled (unknown or approved).
- No standards/schema content is duplicated inside the capability plan.

### Approval gate
- Human approves the capability plan and its codable-task breakdown.

### Escalation triggers
- Acceptance criteria cannot be evaluated.
- Tasks cannot be bounded without introducing new assumptions.
- Capability plan leaks into standards/templates or ops/tool manuals.

---

## 5) Step 4 — Execute codable tasks (implementation)

**Agent support:** Coding Agent (see target_agent_system.md).

### Practical goal
Implement approved tasks and produce reviewable changes aligned to the capability plan.

### Entry criteria
- Capability plan and codable tasks are approved.

### What to do
1) Select execution mode:
   - human implementation with agent support, or
   - agent-assisted implementation under human review.
2) Implement tasks one by one:
   - keep boundaries intact,
   - do not expand scope silently.
3) If an unexpected requirement appears:
   - stop,
   - escalate,
   - revise Step 3 (or earlier) with approval.

### Exit criteria (human-checkable)
- Each codable task’s intended outcome exists in the repo.
- Changes are traceable to the approved tasks.
- No unapproved scope expansion occurred.

### Approval gate
- Human approves the implementation changes (e.g., PR approval/merge evidence).

### Escalation triggers
- Implementation requires changing acceptance criteria.
- Implementation requires new assumptions.
- Implementation conflicts with standards or existing approved intent.

---

## 6) Step 5 — Validate, test, and document

**Agent support:** Validation Support Agent and Documentation Support Agent (see target_agent_system.md).

### Practical goal
Produce evidence that acceptance criteria are met and update documentation to match reality without creating double truth.

### Entry criteria
- Implementation changes exist and are reviewable.

### What to do
1) Validate acceptance criteria using available deterministic evidence.
2) Update documentation that must reflect the change:
   - ensure correct routing (context vs standards vs process vs ops).
3) Perform a **Doc Impact Scan**:
   - glossary terms still consistent,
   - no duplicated authority introduced,
   - references still point to canonical homes.

### Exit criteria (human-checkable)
- Evidence exists (or gaps are explicitly documented and approved).
- Documentation reflects outcomes and does not contradict intent/rules/runtime.
- No “verified/confirmed” claim exists without referenced evidence.

### Approval gate
- Human approves completion based on evidence review.

### Escalation triggers
- Evidence contradicts expected behavior.
- Required evidence is missing and cannot be justified.
- Documentation changes would alter meaning without going back to earlier steps.

---

## 7) Conflict handling (intent vs rules vs runtime vs evidence)

### When to invoke
Invoke this section whenever you detect contradictions.

### Classification
Classify the conflict first:
- **Intent conflict:** approved artifacts disagree with each other.
- **Rules conflict:** standards/gov rules conflict with an artifact.
- **Runtime conflict:** implementation behavior conflicts with approved intent.
- **Evidence conflict:** evidence contradicts claims or expected outcomes.

### Resolution procedure
1) Stop and surface the conflict explicitly.
2) Propose resolution options (at least two when possible).
3) Human selects a resolution path:
   - align runtime to intent,
   - or update intent/rules to match reality (with explicit approval).
4) Record the decision in an auditable form.
5) Apply changes and re-validate.

---

## 8) Re-homing procedure (layer placement fix without meaning change)

Use this to move content into its correct canonical document type.

1) Identify source content and target canonical home.
2) Copy content verbatim to target (no edits).
3) Replace source section with a short pointer to the target.
4) Run Doc Impact Scan (Section 6).
5) Human approves “meaning unchanged”.

---

## 9) “Where specifics live” routing guide

- Principles and workflow intent → Development Approach
- Agent/tool operating rules → Target Agent System + agent profiles
- Document types and boundaries → Documentation System Catalog
- Shared term meanings → Glossary
- Schemas / required fields / enforcement rules → Standards
- Tool usage / CI / troubleshooting → Ops
- Per-job intent and behavior → per-job docs

This workflow guide is intentionally procedural and must not become a standards document or tool manual.

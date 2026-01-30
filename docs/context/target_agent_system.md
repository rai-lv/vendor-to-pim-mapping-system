# Target Agent System

## Purpose

This document defines the **target agent system operating model** that supports the working approach defined in `development_approach.md`.

It describes:

- what “agents” are expected to do (as collaborative roles under human oversight),
- what “tools” are (deterministic instruments used by humans/agents),
- how agents, tools, and humans interact across the 5-step workflow,
- what rules prevent drift, double truth, and silent changes.

This document does **not** define concrete tool names, command syntax, templates, required fields, file locations, or enforcement mechanisms.

---

## Scope and Authority

- This document is **subordinate** to `development_approach.md` and must not redefine the workflow intent, authority model, or approval discipline.
- This document is **superior** to tool manuals and operational runbooks in the sense that those documents must conform to the operating rules defined here.

---

## Definitions

- **Agent:** A collaborative role that can reason, propose options, draft artifacts, implement changes when tasked, and review outputs — always under human oversight and explicit approval gates.
- **Tool:** A deterministic instrument used by humans and agents to scaffold, validate, and produce evidence. Tools do not invent meaning.
- **Approval gate:** A point where progression requires explicit human sign-off.
- **Evidence:** Deterministic outputs that support approval decisions (e.g., validation reports, test results, run receipts, logs).
- **Conflict:** Any mismatch between approved intent and observed reality (tool results, implementation behavior, or artifact content).

---

## Non-Negotiable Operating Rules

### 1) Human approval gates
Progression between workflow stages requires explicit human approval captured in an auditable form.

Agents may produce drafts and implement tasks, but must not advance stage transitions without human approval of the relevant stage output.

### 2) Explicit unknowns and controlled assumptions
Assumptions and unknowns are allowed only if they are:

- explicitly labeled,
- bounded (what is assumed, why, impact),
- approved by a human before implementation depends on them.

### 3) No hidden authority
Agents and tools must never imply outputs are “true” because an agent produced them or a tool reported them. Truth is grounded in:

- human decisions and approvals,
- enforceable standards and governance rules,
- runtime behavior of implemented artifacts,
- deterministic evidence outputs (e.g., validation/test/run results).

### 4) Separation of concerns
Documentation and artifacts must not mix layers:

- **Principles / intent** (what the system is trying to achieve and what success means),
- **Enforceable rules** (schemas, standards, governance constraints),
- **Execution procedures** (how work is carried out and how completion is proven),
- **Operational references** (how to run tools and interpret outputs).

Agents must avoid creating “shadow specifications” in the wrong layer.

### 5) No double truth and explicit conflict resolution
If approved intent conflicts with current artifacts, tool outputs, or observed behavior, the conflict must be surfaced and resolved explicitly; it must not be silently overridden.

### 6) Single source per contract type
To prevent “double truth,” each contract type must have exactly one authoritative home. Other documents may reference it, but must not redefine it.

---

## Core Design Principles

### 1) Human-led, agent-assisted, tool-enforced

- Humans own decisions and approvals.
- Agents accelerate drafting, reasoning, review, and implementation support.
- Tools enforce consistency and provide deterministic checks and evidence.

### 2) Sequential workflow with iterative refinement inside steps

The workflow proceeds through the five steps defined in `development_approach.md`. Iteration is allowed **within** a step until success criteria are satisfied; step transitions require explicit approval.

---

## Agents and Their Responsibilities

Agents are defined as **functions** that may be implemented by one or multiple actual agents. Responsibilities describe what they may do; humans decide.

**Implementation note:** The three planning agent functions below (Objective Support, Pipeline Support, Capability Support) are currently implemented by the Combined Planning Agent (see `.github/agents/combined-planning-agent.md`), which provides all three functions through explicit mode switching. The functional responsibilities defined below remain the canonical specification regardless of implementation approach.

**Note:** The summaries below provide an overview of each agent role. For detailed, canonical role definitions including full responsibilities, non-responsibilities, escalation triggers, and typical outputs, see `docs/agents/agent_role_charter.md`.

### Objective Support Agent

Supports Step 1.

- Helps refine objectives into clear scope boundaries and success criteria.
- Surfaces unknowns, assumptions, and decision points.
- Produces draft objective artifacts for human review.

**Must escalate when:** scope is ambiguous, success criteria are not testable, or assumptions would materially impact later steps.

---

### Pipeline Support Agent

Supports Step 2.

- Proposes decomposition into capabilities and ordering.
- Highlights dependencies and decision points (when relevant/known).
- Produces a draft pipeline plan for human review.

**Must escalate when:** capability boundaries are unclear or ordering depends on unresolved assumptions.

---

### Capability Support Agent

Supports Step 3.

- Drafts implementable capability definitions: inputs/outputs, rules/constraints, acceptance criteria.
- Breaks the capability into individuable codable tasks that can be executed and reviewed in a controlled way (task boundaries, dependencies, and intended outputs per task).
- Produces a structured implementation step outline that maps 1:1 (or many:1) to these tasks, so execution stays bounded and traceable.
- Performs consistency checks against the objective and pipeline, and flags scope creep or missing prerequisites before execution begins.

**Must escalate when:** acceptance criteria are not evaluable, required inputs/outputs are unknown, or task boundaries cannot be defined without introducing new assumptions.

---

### Coding Agent

Supports Step 4.

- Executes the codable tasks defined in Step 3, producing the actual code/configuration/documentation changes required by each task.
- Keeps implementation aligned with the approved capability definition and task boundaries; flags scope creep or missing prerequisites immediately.
- Produces changes in a form suitable for human review and approval, including any evidence outputs required for validation.

**Must escalate when:** implementing a task would require new assumptions, expands scope beyond the defined task boundaries, or changes the agreed rules/acceptance criteria.

---

### Validation Support Agent

Supports Step 5.

- Assembles evidence against acceptance criteria.
- Interprets deterministic tool outputs and summarizes gaps.
- Proposes additional checks where evidence is insufficient.

**May not:** declare success without evidence.
**Must escalate when:** evidence contradicts expectations, or acceptance criteria are incomplete.

---

### Documentation Support Agent

Supports Steps 1–5 (continuous).

- Keeps documentation consistent with approved intent and implemented reality.
- Ensures intent documentation is not conflated with execution details.
- Flags contradictory statements across documents.

**Must escalate when:** resolving inconsistency would change meaning or authority (requires explicit human decision).

---

## Tools and How They Are Used

### What tools are

Tools are deterministic instruments used to:

- scaffold (create structured starting points),
- validate conformance to standards,
- generate evidence outputs.

Tools do not invent requirements, interpret intent, or make approval decisions.

### Tool categories

- **Scaffolding tools:** Generate empty or minimally-filled structures to reduce manual work.
- **Validation tools:** Check conformance and internal consistency against defined standards.
- **Evidence tools:** Produce deterministic outputs used for approval decisions.

### Tool output rules

- Tool outputs are inputs to human and agent review, not decisions.
- If tool outputs conflict with approved intent or observed behavior, the conflict must be surfaced and resolved explicitly.

---

## Approval Gates and Evidence Discipline

### Approval gates (principle-level)

Approval gates are a non-negotiable operating rule (see “Non-Negotiable Operating Rules”). Approval must be based on evidence proportional to the stage and impact.

### Evidence discipline

- Evidence must be deterministic and reviewable.
- Agents may summarize evidence but must not substitute narrative for proof.
- Lack of evidence must be recorded explicitly (e.g., “evidence missing / TBD”) and blocks approval unless a human explicitly approves proceeding under a controlled assumption.
- Agents may use terms like “verified” or “confirmed” only when explicit evidence is referenced (in the repository or in the conversation).

---

## Conflict Handling

A conflict exists when:

- approved intent differs from current artifacts, tool outputs, or observed behavior.

Required handling:

1. **Surface the conflict explicitly.**
2. Identify which “kind of truth” is involved (intent vs rules vs runtime vs evidence).
3. Propose resolution options:

   * align implementation to approved intent, or
   * update intent/rules to match reality with explicit human approval.
4. Record the decision in an auditable form.

Agents and tools must not silently resolve conflicts by rewriting documents or code without approval.

---

## What “good” looks like

The target agent system is achieved when:

- different contributors can follow the workflow and produce consistent outcomes,
- agents speed up drafting and implementation without inventing requirements,
- tools reliably enforce standards and provide evidence without becoming a second source of meaning,
- approvals are explicit, evidence-backed, and resistant to silent drift.

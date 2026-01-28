# System Context

## Purpose statement
This document explains **what this repository/system is**, its **scope**, and **how truth is established** (intent vs rules vs runtime vs evidence).

It is an onboarding and orientation document. It is **not** a workflow guide, a standards document, or an operational manual.

---

## 1) What this repository is

This repository is an **AI-supported development system** for building and maintaining automation components (primarily jobs/scripts and their documentation) in the domain of **vendor → PIM mapping**.

“AI-supported” means:
- humans remain the decision-makers (approval gates),
- agents accelerate drafting/review/implementation under human oversight,
- tools provide deterministic scaffolding/validation/evidence.

---

## 2) Scope boundaries

This repository includes:
- implementation artifacts (e.g., job code and job interfaces),
- documentation that defines intent, rules, execution guidance, and operational references,
- evidence artifacts produced by validation and automation.

Scope boundaries are enforced by the documentation system:
- Context documents define intent and framing (this document).
- Standards define enforceable rules/schemas.
- Process documents describe how to execute the workflow.
- Ops documents describe how to run tooling and interpret outputs.
- Per-job documents capture job-local intent and job-local operational behavior.

If a topic does not clearly belong to one of these layers, it must be routed explicitly (no “shadow specs”).

---

## 3) The working approach this repo is built to support

The repository is built around the **5-step working approach** defined in `development_approach.md`.

System Context does not restate the steps in detail. It provides the navigation logic:
- “What is the approach?” → `development_approach.md`
- “How do agents/tools behave in that approach?” → `target_agent_system.md`
- “Where does each doc type live and what must it contain?” → `documentation_system_catalog.md`
- “How do I execute the steps in practice?” → process-layer workflow guide(s)

---

## 4) How truth is established (and how conflicts are handled)

This system explicitly separates “kinds of truth” so contradictions are resolvable without drift.

### 4.1 Intent truth (what should be true)
Intent truth comes from **approved** planning artifacts produced in the 5-step workflow
(e.g., objective/pipeline/capability definitions and their acceptance criteria).

### 4.2 Rules truth (what is allowed)
Rules truth comes from **standards and governance** documents that define:
- schemas and required fields,
- naming conventions,
- validation semantics,
- decision-record requirements.

Rules truth is enforceable (validator/CI) and must not be duplicated elsewhere.

### 4.3 Runtime truth (what actually runs)
Runtime truth comes from the implemented artifacts (e.g., code and interface manifests).
Runtime truth can diverge from intent truth (bugs, incomplete work, drift) — this must be surfaced, not rationalized.

### 4.4 Evidence truth (what can be proven)
Evidence truth comes from deterministic outputs:
validation reports, test results, run receipts, logs, and other reviewable artifacts.

Claims like “verified/confirmed” are only valid when evidence is explicitly referenced.

### 4.5 Conflict handling rule (no silent resolution)
If artifacts disagree (intent vs rules vs runtime vs evidence), the conflict must be:
1) surfaced explicitly,
2) classified (which truth types are in conflict),
3) resolved by an explicit decision (update implementation, or update intent/rules, with approval),
4) recorded in an auditable form.

No actor (human/agent/tool) may silently “pick a side” without making the conflict explicit.

---

## 5) Documentation architecture (how to navigate)

This repository uses a layered documentation system to prevent “double truth”.

### 5.1 Canonical routing
Each document type has exactly one authoritative “home” location and a defined scope boundary.
System Context only summarizes the routing principle; the full catalog is authoritative.

Reference: `documentation_system_catalog.md`

### 5.2 Practical reading order (recommended)
For onboarding and consistent work:
1) `development_approach.md` (highest-level working approach)
2) `target_agent_system.md` (agent/tool operating model and non-negotiables)
3) `documentation_system_catalog.md` (document ecosystem and boundaries)
4) `glossary.md` (shared definitions)
5) process-layer workflow guide(s) (how-to execution)
6) standards relevant to the task (schemas/rules)
7) per-job docs for the job you are touching (intent + operational behavior)

---

## 6) How to change the system safely (routing by change type)

Use this routing to avoid creating contradictions:

- Want to change **how a job behaves** → change implementation artifacts; then update the job’s operational documentation to match.
- Want to change **what a job is supposed to do** → change intent artifacts; ensure downstream implications are reviewed and approved.
- Want to change **schemas / required fields / naming rules** → change standards (and expect validator/CI updates).
- Found **a contradiction** between intent and runtime → follow conflict handling; record a decision if the resolution changes meaning.

This document does not define templates, schemas, or required fields; it routes you to where those live.

---

## 7) Terminology

Shared terms must be defined **once** in the Glossary and referenced elsewhere.
If a term is used in multiple layers (e.g., “capability”, “artifact contract”, “approval gate”), it must not acquire different meanings per document.

Reference: `glossary.md`

---

## 8) Non-goals of this document

System Context must not contain:
- step-by-step execution procedures,
- normative schemas or embedded authoritative templates,
- tool command syntax, CLI manuals, or troubleshooting.

Those belong in process / standards / ops layers as defined in the documentation catalog.

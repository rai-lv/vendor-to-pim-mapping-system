# Documentation System Catalog

## Purpose

This catalog defines the **target documentation set** required for the development system and clarifies the **role, necessity, and content boundaries** of each document type.

It exists to:

* enforce **internal consistency** across documentation,
* prevent **double truth** by assigning **one authoritative home** per contract type,
* keep clear separation between **principles**, **enforceable standards**, **execution guidance**, **operational references**, and **living catalogs**.

This catalog is **descriptive and governing**: it defines what each document is for and what it must not contain.

---

## Layers and Intent

* **Context layer:** explains intent, shared meaning, and system framing.
* **Governance and standards layer:** normative rules and schemas (validator-enforceable).
* **Agent documentation layer:** defines agent roles and how they are used (without becoming tool manuals).
* **Process layer:** how-to guidance for executing the approach (non-normative).
* **Operational reference layer:** technical manuals for tools and automation (allowed to be detailed).
* **Living catalogs and per-job docs:** instances that document the concrete system (jobs/artifacts/decisions) and per-job intent/operations.

---

## Document Types

### Context layer

#### 1) Development Approach

**Purpose statement:** Defines the highest-level working approach: principles, workflow intent, iteration shape, and human approval discipline.
**Why necessary:** Provides a stable anchor for all downstream documentation and decisions.
**Must contain:** Principles; 5-step intent; approval/assumption philosophy; boundaries.
**Must not contain:** Tool names, templates, schemas, file paths, operational instructions.

#### 2) Target Agent System

**Purpose statement:** Defines the intended operating model for agents and tools, including non-negotiable rules, evidence discipline, and conflict handling.
**Why necessary:** Prevents agent authority creep, silent assumptions, and double truth.
**Must contain:** Agent responsibilities per step; tool concept; approval and evidence rules; conflict resolution rules; single-source principle.
**Must not contain:** CLI manuals, detailed tool specifications, embedded authoritative templates.

#### 3) System Context

**Purpose statement:** Explains what the repository/system is, its scope, and how truth is established (intent vs runtime vs evidence) for contributors and agents.
**Why necessary:** Avoids repeated context restatement and reduces onboarding friction.
**Must contain:** Repo purpose/scope; truth framing; high-level component map; pointers to standards/process docs.
**Must not contain:** Normative schemas, step-by-step workflows, tool command syntax.

#### 4) Glossary

**Purpose statement:** Provides a single canonical definition set for shared system terms.
**Why necessary:** Prevents semantic drift across documents, jobs, and agent outputs.
**Must contain:** One definition per shared term; cross-references where needed.
**Must not contain:** Job-specific rules, templates, or operational procedures.

#### 5) Documentation System Catalog

**Purpose statement:** Defines the documentation ecosystem by stating each document type’s role, necessity, and boundaries.
**Why necessary:** Enforces single-source-per-contract-type and prevents documentation sprawl.
**Must contain:** Document list with purpose/role/scope; layer placement; “must not contain” boundaries.
**Must not contain:** The actual schemas or procedures (those live in standards/process docs).

---

### Governance and standards layer (normative)

#### 6) Naming Standard

**Purpose statement:** Defines naming rules for jobs, artifacts, identifiers, and placeholders to ensure stability and automation.
**Why necessary:** Prevents drift and enables consistent validation and tooling.
**Must contain:** Naming conventions; identifier rules; compatibility expectations.
**Must not contain:** Tool instructions or job-specific business logic.

#### 7) Validation Standard

**Purpose statement:** Defines what “verified” means, what validations are required, and what evidence is acceptable for approvals.
**Why necessary:** Operationalizes evidence discipline and prevents unverifiable claims.
**Must contain:** Validation rules; evidence expectations; pass/fail semantics; blocking conditions.
**Must not contain:** Tool command syntax (belongs in tooling reference).

#### 8) Job Manifest Spec

**Purpose statement:** Defines the normative schema and semantics for machine-readable job interface manifests.
**Why necessary:** Enables consistent invocation and automation across jobs.
**Must contain:** Required/optional fields; semantic meaning; placeholder rules; compatibility/breaking-change rules.
**Must not contain:** Per-job content or examples that become authoritative.

#### 9) Artifact Contract Spec

**Purpose statement:** Defines the normative schema for describing artifact contracts and content expectations.
**Why necessary:** Prevents ad-hoc contract definitions scattered across job docs.
**Must contain:** Artifact entry schema; content-contract fields; empty behavior semantics; producer/consumer representation.
**Must not contain:** Job-specific implementations.

#### 10) Job Inventory Spec

**Purpose statement:** Defines the normative schema for job inventory entries.
**Why necessary:** Enables validation, discovery, and consistent indexing.
**Must contain:** Required fields; reference/link expectations; lifecycle/status semantics (as schema).
**Must not contain:** Tool manuals or per-job narrative descriptions.

#### 11) Business Job Description Spec

**Purpose statement:** Defines the normative structure for describing job purpose, scope boundaries, and business rules.
**Why necessary:** Ensures business intent is captured consistently and auditable.
**Must contain:** Required sections/fields; conventions for assumptions/unknowns; rule representation conventions (non-code).
**Must not contain:** Operational “how to run” details.

#### 12) Script Card Spec

**Purpose statement:** Defines the normative structure for operational job documentation (behavior, invariants, failure modes).
**Why necessary:** Ensures consistent operational clarity without mixing business rationale.
**Must contain:** Runtime behavior sections; failure-mode/observability structure; operational invariants conventions.
**Must not contain:** Business justification or contract rules already defined elsewhere.

#### 13) Codable Task Spec

**Purpose statement:** Defines the normative structure for individuable codable tasks used to control implementation work.
**Why necessary:** Keeps Step 3→4 execution bounded, traceable, and reviewable.
**Must contain:** Task boundaries; intended outputs; acceptance check/evidence expectation; dependencies/blocks; scope constraints.
**Must not contain:** Full code solutions; tool command syntax.

#### 14) Decision Records Standard

**Purpose statement:** Defines when and how explicit governance decisions are recorded.
**Why necessary:** Required for conflict resolution and contract evolution without silent changes.
**Must contain:** Decision template; status lifecycle; required evidence/approval references.
**Must not contain:** General workflow instructions (belongs in process docs).

---

### Agent documentation layer

#### 15) Agent Role Charter

**Purpose statement:** Defines the authoritative set of agent roles and their responsibilities and boundaries.
**Why necessary:** Prevents role drift and ad-hoc agent creation.
**Must contain:** Role list; responsibilities; escalation conditions; interaction with approvals/evidence.
**Must not contain:** Tool command syntax; embedded authoritative templates.

#### 16) Agent Profiles (per role)

**Purpose statement:** Provides operational guidance for invoking each agent role consistently.
**Why necessary:** Reduces variance and improves repeatability of agent-assisted work.
**Must contain:** Expected inputs; typical outputs; stop/escalation rules; evidence expectations; forbidden behaviors.
**Must not contain:** Normative schemas (belong in standards) or full tool manuals.

#### 17) Prompt Packs (non-authoritative)

**Purpose statement:** Provides reusable prompt skeletons and examples to invoke agents consistently.
**Why necessary:** Reduces friction and variance in agent usage.
**Must contain:** Prompt templates/examples clearly labeled as non-normative.
**Must not contain:** Requirements that compete with standards.

#### 18) Agent–Tool Interaction Guide

**Purpose statement:** Describes how agents should use tools conceptually and what evidence outputs should be produced/referenced.
**Why necessary:** Keeps tools as instruments and prevents agent docs becoming tool manuals.
**Must contain:** Tool categories; usage triggers; evidence output expectations; pointers to tooling reference.
**Must not contain:** CLI syntax or detailed troubleshooting.

---

### Process layer (how-to)

#### 19) Workflow Guide: 5-Step Execution

**Purpose statement:** Provides the practical “how-to” for executing the 5-step approach, including checkpoints and handoffs.
**Why necessary:** Makes the approach repeatable without embedding schemas or tool manuals.
**Must contain:** Step procedures; iteration guidance; checkpoints; escalation triggers; references to standards.
**Must not contain:** Normative schemas (belong in standards) or CLI manuals.

#### 20) Contribution and Approval Guide

**Purpose statement:** Defines how work is proposed, reviewed, approved, and recorded.
**Why necessary:** Approval gates are central; this prevents approval ambiguity.
**Must contain:** Approval evidence expectations; review checklist at principle level; decision recording guidance; conflict handling entry points.
**Must not contain:** Tool syntax (belongs in operational reference).

---

### Operational reference layer

#### 21) Tooling Reference

**Purpose statement:** Technical manual for repo tools and agent-support tools, including usage and troubleshooting.
**Why necessary:** Centralizes operational details to prevent contamination of context/standards docs.
**Must contain:** Tool inventory; usage; parameters; outputs; troubleshooting; version notes.
**Must not contain:** Normative rules that belong in standards.

#### 22) CI / Automation Reference

**Purpose statement:** Explains what automation runs, what evidence it produces, and how to interpret failures.
**Why necessary:** CI is part of the working system and must be understandable.
**Must contain:** Automation overview; triggers; produced artifacts; failure interpretation; remediation patterns.
**Must not contain:** Contract schemas (belongs in standards).

---

### Living catalogs and per-job documentation

#### 23) Job Inventory (instance)

**Purpose statement:** Living catalog of all jobs, conforming to Job Inventory Spec.
**Why necessary:** Discoverability and governance at scale.
**Must contain:** Job entries; links/references; status; ownership signals (as data).
**Must not contain:** Schema definitions (belongs in Job Inventory Spec).

#### 24) Artifact Catalog (instance)

**Purpose statement:** Living catalog of artifact contracts, conforming to Artifact Contract Spec.
**Why necessary:** Stable shared contracts and producer/consumer visibility.
**Must contain:** Artifact entries; content expectations; producer/consumer relations.
**Must not contain:** Artifact schema definitions (belongs in Artifact Contract Spec).

#### 25) Per-job Business Description

**Purpose statement:** Job-local business intent: purpose, scope boundaries, and business rules.
**Why necessary:** Makes each job auditable against intent without mixing operational detail.
**Must contain:** Purpose; scope; rules; job-local assumptions/unknowns.
**Must not contain:** Operational run instructions or normative contract rules.

#### 26) Per-job Script Card

**Purpose statement:** Job-local operational behavior: how it runs, invariants, failure modes, observability.
**Why necessary:** Operator and developer clarity without re-deriving from code.
**Must contain:** Behavior summary; failure modes; invariants; observability expectations.
**Must not contain:** Business rationale or normative contract schemas.

#### 27) Decision Log (index)

**Purpose statement:** Index of recorded decision records for navigation and traceability.
**Why necessary:** Maintains continuity and governance transparency.
**Must contain:** List of decisions with status/tags/links.
**Must not contain:** Decision templates (belongs in Decision Records Standard).

#### 28) Repository README

**Purpose statement:** Entry point for contributors to understand the repo and find the documentation system quickly.
**Why necessary:** Basic adoption and navigation.
**Must contain:** What the repo is; where to start; pointers to catalog and workflow/standards.
**Must not contain:** Deep technical manuals or duplicated schemas.

---

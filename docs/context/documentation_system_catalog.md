# Documentation System Catalog

## Purpose

This catalog defines the **target documentation set** required for the development system and clarifies the **role, necessity, content boundaries, and canonical placement** of each document type.

It exists to:

- enforce **internal consistency** across documentation,
- prevent **double truth** by assigning **one authoritative home** per contract type,
- keep separation between **principles**, **enforceable standards**, **execution guidance**, **operational references**, and **living catalogs**,
- provide a single authoritative routing map: **document type → canonical folder location**.

This catalog is **descriptive and governing**: it defines what each document is for, where it lives, and what it must not contain.

---

## Canonical Placement Rules

- Each document type has exactly one **canonical folder** in this repository.
- Documents may reference other documents, but must not duplicate their authoritative rules.
- Operational detail (tool syntax, troubleshooting) must not appear in context or standards documents.
- If canonical placement changes, it is treated as a repository refactor and must be updated here.

---

## Layers and Intent

- **Context layer:** explains intent, shared meaning, and system framing.
- **Governance and standards layer:** normative rules and schemas (validator-enforceable).
- **Agent documentation layer:** defines agent roles and how they are used (without becoming tool manuals).
- **Process layer:** how-to guidance for executing the approach (non-normative).
- **Operational reference layer:** technical manuals for tools and automation.
- **Living catalogs and per-job docs:** instances describing the concrete system and per-job intent/operations.

---

## Document Types

### Context layer (`docs/context/`)

#### 1) Development Approach

**Canonical location:** `docs/context/`
**Purpose statement:** Defines the highest-level working approach: principles, workflow intent, iteration shape, and human approval discipline.
**Why necessary:** Provides a stable anchor for all downstream documentation and decisions.
**Must contain:** Principles; 5-step intent; approval/assumption philosophy; boundaries.
**Must not contain:** Tool names, templates, schemas, operational instructions.

#### 2) Target Agent System

**Canonical location:** `docs/context/`
**Purpose statement:** Defines the operating model for agents and tools, including non-negotiable rules, evidence discipline, and conflict handling.
**Why necessary:** Prevents agent authority creep, silent assumptions, and double truth.
**Must contain:** Agent responsibilities per step; tool concept; approval/evidence rules; conflict resolution; single-source principle.
**Must not contain:** CLI manuals, detailed tool specifications, embedded authoritative templates.

#### 3) System Context

**Canonical location:** `docs/context/`
**Purpose statement:** Explains what the repository/system is, its scope, and how truth is established (intent vs runtime vs evidence).
**Why necessary:** Reduces onboarding friction and avoids repeated context restatement.
**Must contain:** Repo purpose/scope; truth framing; high-level component framing; pointers to standards/process docs.
**Must not contain:** Normative schemas, step-by-step workflows, tool command syntax.

#### 4) Glossary

**Canonical location:** `docs/context/`
**Purpose statement:** Provides a single canonical definition set for shared system terms.
**Why necessary:** Prevents semantic drift across documents, jobs, and agent outputs.
**Must contain:** One definition per shared term; cross-references where needed.
**Must not contain:** Job-specific rules, templates, or operational procedures.

#### 5) Documentation System Catalog

**Canonical location:** `docs/context/`
**Purpose statement:** Defines the documentation ecosystem by stating each document type’s role, necessity, boundaries, and canonical placement.
**Why necessary:** Enforces single-source-per-contract-type and prevents documentation sprawl.
**Must contain:** Document list with purpose/role/scope; canonical folders; “must not contain” boundaries.
**Must not contain:** The actual schemas or procedures (those live in standards/process docs).

---

### Governance and standards layer (`docs/standards/`)

#### 6) Naming Standard

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines naming rules for jobs, artifacts, identifiers, and placeholders to ensure stability and automation.
**Why necessary:** Prevents drift and enables consistent validation and tooling.
**Must contain:** Naming conventions; identifier rules; compatibility expectations.
**Must not contain:** Tool instructions or job-specific business logic.

#### 7) Validation Standard

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines what “verified” means, what validations are required, and what evidence is acceptable for approvals.
**Why necessary:** Operationalizes evidence discipline and prevents unverifiable claims.
**Must contain:** Validation rules; evidence expectations; pass/fail semantics; blocking conditions.
**Must not contain:** Tool command syntax.

#### 8) Documentation Specification

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines how documentation must be structured, formatted, and governed, combining foundational principles (the WHY) with practical rules (the WHAT and HOW).
**Why necessary:** Ensures documentation is reliable, maintainable, discoverable, and aligned with principles that prevent duplication, confusion, and unclear authority.
**Must contain:** Foundational principles; formatting rules; metadata requirements; versioning discipline; quality criteria; anti-patterns; application guidelines; governance procedures.
**Must not contain:** Semantic content rules (those live in documentation_system_catalog.md); tool command syntax; operational procedures.

#### 9) Job Manifest Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema and semantics for machine-readable job interface manifests.
**Why necessary:** Enables consistent invocation and automation across jobs.
**Must contain:** Required/optional fields; semantic meaning; placeholder rules; compatibility/breaking-change rules.
**Must not contain:** Per-job content or embedded authoritative examples.

#### 10) Artifacts Catalog Entry Specification

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for describing artifact contracts and content expectations.
**Why necessary:** Prevents ad-hoc contract definitions scattered across job docs.
**Must contain:** Artifact entry schema; content-contract fields; empty behavior semantics.
**Must not contain:** Job-specific implementations.

#### 11) Job Inventory Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for job inventory entries.
**Why necessary:** Enables validation, discovery, and consistent indexing.
**Must contain:** Required fields; reference/link expectations; lifecycle/status semantics (as schema).
**Must not contain:** Tool manuals or per-job narrative descriptions.

#### 12) Business Job Description Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative structure for describing job purpose, scope boundaries, and business rules.
**Why necessary:** Ensures business intent is captured consistently and auditable.
**Must contain:** Required sections/fields; conventions for assumptions/unknowns.
**Must not contain:** Operational “how to run” details.

#### 13) Script Card Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative structure for operational job documentation (behavior, invariants, failure modes).
**Why necessary:** Ensures consistent operational clarity without mixing business rationale.
**Must contain:** Runtime behavior sections; failure-mode/observability structure.
**Must not contain:** Business justification or contract rules already defined elsewhere.

#### 14) Codable Task Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative structure for individuable codable tasks used to control implementation work.
**Why necessary:** Keeps Step 3→4 execution bounded, traceable, and reviewable.
**Must contain:** Task boundaries; intended outputs; acceptance check/evidence expectation; dependencies/blocks.
**Must not contain:** Full code solutions; tool command syntax.

#### 15) Decision Records Standard

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines when and how explicit governance decisions are recorded.
**Why necessary:** Required for conflict resolution and contract evolution without silent changes.
**Must contain:** Decision template; status lifecycle; required evidence/approval references.
**Must not contain:** General workflow instructions.

---

### Agent documentation layer (`docs/agents/`)

#### 16) Agent Role Charter

**Canonical location:** `docs/agents/`
**Purpose statement:** Defines the authoritative set of agent roles and their responsibilities and boundaries.
**Why necessary:** Prevents role drift and ad-hoc agent creation.
**Must contain:** Role list; responsibilities; escalation conditions; interaction with approvals/evidence.
**Must not contain:** Tool command syntax; embedded authoritative templates.

#### 17) Agent Definitions (canonical)

**Canonical location:** `.github/agents/`
**Purpose statement:** Contains the authoritative agent profile definitions used by the GitHub Copilot agent invocation system.
**Why necessary:** GitHub requires complete agent definitions in `.github/agents/` and cannot reference external files. This is the single source of truth for agent behavior.
**Must contain:** Complete agent instructions including detailed operating rules, expected inputs/outputs, forbidden behaviors, stop/escalation rules, evidence expectations, and prompt examples; frontmatter metadata (name, description).
**Must not contain:** Normative schemas or full tool manuals; business logic or contract definitions.

#### 18) Prompt Packs (non-authoritative)

**Canonical location:** `docs/agents/prompt_packs/`
**Purpose statement:** Provides reusable prompt skeletons and examples to invoke agents consistently.
**Why necessary:** Reduces friction and variance in agent usage.
**Must contain:** Prompt templates/examples clearly labeled as non-normative.
**Must not contain:** Requirements that compete with standards.

#### 19) Agent–Tool Interaction Guide

**Canonical location:** `docs/agents/`
**Purpose statement:** Describes how agents should use tools conceptually and what evidence outputs should be produced/referenced.
**Why necessary:** Keeps tools as instruments and prevents agent docs becoming tool manuals.
**Must contain:** Tool categories; usage triggers; evidence output expectations; pointers to tooling reference.
**Must not contain:** CLI syntax or detailed troubleshooting.

---

### Process layer (`docs/process/`)

#### 20) Workflow Guide: 5-Step Execution

**Canonical location:** `docs/process/`
**Purpose statement:** Provides the practical how-to for executing the 5-step approach, including checkpoints and handoffs.
**Why necessary:** Makes the approach repeatable without embedding schemas or tool manuals.
**Must contain:** Step procedures; iteration guidance; checkpoints; escalation triggers; references to standards.
**Must not contain:** Normative schemas or CLI manuals.

#### 21) Contribution and Approval Guide

**Canonical location:** `docs/process/`
**Purpose statement:** Defines how work is proposed, reviewed, approved, and recorded.
**Why necessary:** Approval gates are central; this prevents approval ambiguity.
**Must contain:** Approval evidence expectations; review expectations; decision recording guidance; conflict entry points.
**Must not contain:** Tool syntax.

---

### Operational reference layer (`docs/ops/`)

#### 22) Tooling Reference

**Canonical location:** `docs/ops/`
**Purpose statement:** Technical manual for repo tools and agent-support tools, including usage and troubleshooting.
**Why necessary:** Centralizes operational details and prevents contamination of context/standards docs.
**Must contain:** Tool inventory; usage; parameters; outputs; troubleshooting; version notes.
**Must not contain:** Normative rules that belong in standards.

#### 23) CI / Automation Reference

**Canonical location:** `docs/ops/`
**Purpose statement:** Explains what automation runs, what evidence it produces, and how to interpret failures.
**Why necessary:** CI is part of the working system and must be understandable.
**Must contain:** Automation overview; triggers; produced artifacts; failure interpretation; remediation patterns.
**Must not contain:** Contract schemas.

---

### Living catalogs and per-job documentation (`docs/catalogs/` and `docs/jobs/`)

#### 24) Job Inventory (instance)

**Canonical location:** `docs/catalogs/`
**Purpose statement:** Living catalog of all jobs, conforming to Job Inventory Spec.
**Why necessary:** Discoverability and governance at scale.
**Must contain:** Job entries; links/references; status signals.
**Must not contain:** Schema definitions.

#### 25) Artifact Catalog (instance)

**Canonical location:** `docs/catalogs/`
**Purpose statement:** Living catalog of artifact contracts, conforming to Artifacts Catalog Entry Specification.
**Why necessary:** Stable shared contracts and producer/consumer visibility.
**Must contain:** Artifact entries; content expectations; producer/consumer relations.
**Must not contain:** Schema definitions.

#### 26) Per-job Business Description

**Canonical location:** `jobs/<job_group>/<job_id>/`
**Purpose statement:** Job-local business intent: purpose, scope boundaries, and business rules.
**Why necessary:** Makes each job auditable against intent without mixing operational detail.
**Must contain:** Purpose; scope; rules; job-local assumptions/unknowns.
**Must not contain:** Operational run instructions or normative contract schemas.

#### 27) Per-job Script Card

**Canonical location:** `jobs/<job_group>/<job_id>/`
**Purpose statement:** Job-local operational behavior: how it runs, invariants, failure modes, observability.
**Why necessary:** Operator and developer clarity without re-deriving from code.
**Must contain:** Behavior summary; failure modes; invariants; observability expectations.
**Must not contain:** Business rationale or normative contract schemas.

#### 28) Decision Log (index)

**Canonical location:** `docs/catalogs/`
**Purpose statement:** Index of recorded decision records for navigation and traceability.
**Why necessary:** Maintains continuity and governance transparency.
**Must contain:** List of decisions with status/tags/links.
**Must not contain:** Decision templates.

#### 29) Repository README

**Canonical location:** repository root
**Purpose statement:** Entry point for contributors to understand the repo and find the documentation system quickly.
**Why necessary:** Basic adoption and navigation.
**Must contain:** What the repo is; where to start; pointers to documentation catalog and workflow/standards.
**Must not contain:** Deep technical manuals or duplicated schemas.

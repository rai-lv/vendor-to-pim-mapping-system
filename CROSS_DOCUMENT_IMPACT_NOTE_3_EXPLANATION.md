# Explanation: Cross-Document Impact Note 3

## The Question

Why should the Documentation System Catalog entry #27 (Per-job Script Card) be updated to match the refined script_card_spec?

## Quick Answer

The catalog entry should be updated because it currently contains an **outdated, simplified description** that doesn't accurately reflect the **significantly expanded and refined** specification. The catalog's role is to provide an authoritative index of document types, and outdated entries undermine this purpose.

---

## Detailed Explanation

### What is the Documentation System Catalog?

From `docs/context/documentation_system_catalog.md`:

> This catalog defines the **target documentation set** required for the development system and clarifies the **role, necessity, content boundaries, and canonical placement** of each document type.
> 
> It exists to:
> - enforce **internal consistency** across documentation,
> - prevent **double truth** by assigning **one authoritative home** per contract type,
> - keep separation between **principles**, **enforceable standards**, **execution guidance**, **operational references**, and **living catalogs**,
> - provide a single authoritative routing map: **document type → canonical folder location**.

**The catalog is the directory/index for the entire documentation system.** When someone asks "what document types exist?" or "where does operational job documentation live?", the catalog is the authoritative answer.

### Current State: Entry #27 (Per-job Script Card)

**Current catalog entry:**

```markdown
#### 27) Per-job Script Card

**Canonical location:** `docs/jobs/<job_id>/`
**Purpose statement:** Job-local operational behavior: how it runs, invariants, failure modes, observability.
**Why necessary:** Operator and developer clarity without re-deriving from code.
**Must contain:** Behavior summary; failure modes; invariants; observability expectations.
**Must not contain:** Business rationale or normative contract schemas.
```

This entry was written **before** the script_card_spec was comprehensively reworked. It's accurate but **incomplete** — it captures the basics but misses the refined scope and boundaries.

### Refined State: Script Card Specification (Current)

**From `docs/standards/script_card_spec.md`:**

**Purpose statement:**
> This standard defines the normative structure for **operational job documentation** ("script cards"), focusing on runtime behavior, invariants, failure modes, and observability. It ensures consistent operational clarity across jobs without mixing business rationale or duplicating contract rules.

**Key refinements in the reworked spec:**

1. **Explicit operational focus:** "operational + interface reference that enables operators and developers to understand and troubleshoot job execution"

2. **10 normative required sections** (not just "behavior summary"):
   - Identity (job_id, glue_job_name, runtime, paths)
   - Purpose (1-3 sentences on outputs/side effects)
   - Trigger and Parameters
   - Interface: Inputs (with artifact_id cross-references)
   - Interface: Outputs (with artifact_id cross-references)
   - Side Effects (deletes_inputs, overwrites_outputs)
   - Runtime Behavior (4-8 bullets)
   - Invariants (externally meaningful properties)
   - Failure Modes and Observability (4 subfields)
   - References (manifest, business description, artifacts, dependencies)

3. **Strong boundary enforcement** (Section 1 & 3):
   - Clear separation from business descriptions (WHY vs HOW)
   - Clear separation from artifacts catalog (reference vs define)
   - Clear separation from ops docs (what signals exist vs how to query)

4. **Resolved design decisions** (Section 9):
   - Run receipt format: per-job variation accepted
   - Validation tooling: presence/absence only, not cardinality
   - Dependencies: derived from artifacts catalog (single source)

5. **Enforcement and validation guidance** (Section 7):
   - What automated tooling validates
   - Human review checkpoints
   - Relationship to validation standard

### The Gap: Why the Catalog Needs Updating

The current catalog entry says:

> **Must contain:** Behavior summary; failure modes; invariants; observability expectations.

But the refined spec now requires **10 specific sections** with defined structure, not just a loose "behavior summary."

The current entry doesn't mention:
- The **identity section** (critical for traceability)
- The **interface sections** (inputs/outputs with artifact_id cross-references)
- The **references section** (linking to manifest, business description, artifacts catalog)
- The **derived fields** concept (upstream/downstream jobs computed from artifacts catalog)
- The **explicit boundary rules** preventing "double truth"

### Impact of Not Updating

If the catalog entry remains outdated:

1. **Navigation confusion:** Someone reading the catalog to understand "what's in a script card?" gets an incomplete picture
2. **Inconsistent authority:** The catalog is supposed to be the index, but it doesn't match the spec
3. **Missed boundaries:** New contributors might not realize script cards have strong separation rules
4. **Drift detection failure:** The catalog exists to detect documentation drift; outdated entries undermine this

### Principle: Catalog as Living Index

From the Documentation System Catalog's own purpose:

> This catalog is **descriptive and governing**: it defines what each document is for, where it lives, and what it must not contain.

The catalog isn't just a historical record — it's a **living index** that should reflect the current state of document types. When a spec is refined (as script_card_spec was), the catalog entry should be updated to match.

---

## Comparison: Current vs Should Be

### Current Entry (Outdated)

```markdown
#### 27) Per-job Script Card

**Canonical location:** `docs/jobs/<job_id>/`
**Purpose statement:** Job-local operational behavior: how it runs, invariants, failure modes, observability.
**Why necessary:** Operator and developer clarity without re-deriving from code.
**Must contain:** Behavior summary; failure modes; invariants; observability expectations.
**Must not contain:** Business rationale or normative contract schemas.
```

### Recommended Updated Entry

```markdown
#### 27) Per-job Script Card

**Canonical location:** `jobs/<job_group>/<job_id>/` or `docs/jobs/<job_id>/`
**Purpose statement:** Job-local operational documentation focusing on runtime behavior, invariants, failure modes, and observability. Provides operational + interface reference for operators and developers.
**Why necessary:** Enables operators and developers to understand and troubleshoot job execution without re-deriving from code or mixing business rationale.
**Must contain:** 10 required sections including identity, purpose, trigger/parameters, inputs/outputs (with artifact_id cross-references), side effects, runtime behavior, invariants, failure modes/observability, and references.
**Must not contain:** Business justification (belongs in business description); artifact contract definitions (belongs in artifacts catalog); CLI commands or troubleshooting (belongs in ops docs).
```

**Key changes:**
1. **Canonical location:** Updated to reflect both possible locations (per Section 5.1 of spec)
2. **Purpose statement:** More complete — includes "operational + interface reference" phrasing
3. **Must contain:** Specific mention of "10 required sections" and key examples (identity, inputs/outputs with artifact_id)
4. **Must not contain:** Expanded to include all three boundary rules (business/artifacts/ops separation)

---

## Rationale for Update

### 1. Catalog Entry Format

The catalog entries follow a specific format:
- **Canonical location:** Where it lives
- **Purpose statement:** What it is and what it does
- **Why necessary:** Justification for existence
- **Must contain:** Required content/structure
- **Must not contain:** Exclusions to prevent boundary violations

The script_card_spec now has **much more detail** on all of these dimensions. The catalog entry should reflect this detail (in summary form).

### 2. Alignment with Documentation Spec Principles

From `docs/standards/documentation_spec.md` Section 1.1:

> **Principle:** Each fact, rule, definition, or contract must have exactly one authoritative source.

The script_card_spec is the **authoritative source** for what script cards contain. The catalog entry should **summarize** that authority accurately, not provide an outdated snapshot.

### 3. Preventing "Shadow Specifications"

If the catalog entry is incomplete or outdated, it becomes a **shadow specification** — someone might read the catalog and think "oh, script cards just need a behavior summary" without realizing there's a full 10-section structure defined in the spec.

This violates the "single source of truth" principle.

### 4. Supporting Discovery and Navigation

New contributors or agents use the catalog to understand "what documentation exists and what's in it." An outdated entry hampers this discovery:

- Agent asks: "What sections must a script card have?"
- Reads catalog: "Behavior summary; failure modes; invariants; observability expectations"
- Reality: 10 specific sections with defined structure

The catalog should enable accurate discovery.

---

## Proposed Action

**Update `docs/context/documentation_system_catalog.md` entry #27** to align with the refined script_card_spec.

The update should:
1. Preserve the catalog entry format (concise, structured)
2. Accurately reflect the current spec's purpose and scope
3. Mention the key structural requirement (10 required sections)
4. Capture all three boundary rules (not just "business rationale")
5. Note both possible canonical locations

**Why this is minimal and necessary:**
- **Minimal:** Only updating entry #27; no other catalog changes
- **Necessary:** Maintains catalog accuracy and prevents shadow specifications
- **Aligned:** Follows the catalog's own stated purpose as a "living index"

---

## Summary

**Cross-document impact note 3 says the catalog entry should be updated because:**

1. The script_card_spec was significantly reworked with expanded structure and refined boundaries
2. The catalog is the authoritative index for document types
3. An outdated catalog entry creates "shadow specifications" and navigation confusion
4. The catalog's purpose is to be a **living, accurate index** — not a historical snapshot
5. Updating maintains the "single source of truth" principle: spec is authoritative, catalog summarizes accurately

**The fix is straightforward:** Update entry #27 to reflect the current spec's purpose, structure, and boundaries in catalog entry format (concise but complete).

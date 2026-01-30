# Cross-Document Impact Note 3: Before/After Comparison

## Summary

Cross-document impact note 3 identified that the Documentation System Catalog entries for script cards were outdated after the comprehensive rework of the script_card_spec. This document shows the before/after changes.

---

## Entry #13: Script Card Spec (Standards Layer)

### BEFORE (Outdated)

```markdown
#### 13) Script Card Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative structure for operational job documentation (behavior, invariants, failure modes).
**Why necessary:** Ensures consistent operational clarity without mixing business rationale.
**Must contain:** Runtime behavior sections; failure-mode/observability structure.
**Must not contain:** Business justification or contract rules already defined elsewhere.
```

### AFTER (Updated)

```markdown
#### 13) Script Card Spec

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative structure for operational job documentation ("script cards"), focusing on runtime behavior, invariants, failure modes, and observability.
**Why necessary:** Ensures consistent operational clarity across jobs without mixing business rationale or duplicating contract rules.
**Must contain:** 10 required sections (identity, purpose, trigger/parameters, inputs/outputs, side effects, runtime behavior, invariants, failure modes/observability, references); boundary rules; validation approach; resolved design decisions.
**Must not contain:** Business justification (belongs in business job description spec); artifact contract rules (belongs in artifacts catalog spec); tool/CLI instructions (belongs in ops layer).
```

### Key Changes

1. **Purpose statement:** Added "script cards" terminology and "observability" emphasis
2. **Why necessary:** More complete description including "duplicating contract rules"
3. **Must contain:** 
   - Specific mention of **10 required sections** (was vague "runtime behavior sections")
   - Listed the actual sections by name
   - Added "boundary rules", "validation approach", "resolved design decisions"
4. **Must not contain:** 
   - Expanded to all **three boundary rules** (was generic "contract rules")
   - Specific destinations for excluded content (was vague "already defined elsewhere")

---

## Entry #27: Per-job Script Card (Instance Layer)

### BEFORE (Outdated)

```markdown
#### 27) Per-job Script Card

**Canonical location:** `docs/jobs/<job_id>/`
**Purpose statement:** Job-local operational behavior: how it runs, invariants, failure modes, observability.
**Why necessary:** Operator and developer clarity without re-deriving from code.
**Must contain:** Behavior summary; failure modes; invariants; observability expectations.
**Must not contain:** Business rationale or normative contract schemas.
```

### AFTER (Updated)

```markdown
#### 27) Per-job Script Card

**Canonical location:** `jobs/<job_group>/<job_id>/` or `docs/jobs/<job_id>/`
**Purpose statement:** Job-local operational documentation focusing on runtime behavior, invariants, failure modes, and observability. Provides operational + interface reference for operators and developers.
**Why necessary:** Enables operators and developers to understand and troubleshoot job execution without re-deriving from code or mixing business rationale.
**Must contain:** 10 required sections including identity, purpose, trigger/parameters, inputs/outputs (with artifact_id cross-references), side effects, runtime behavior, invariants, failure modes/observability, and references.
**Must not contain:** Business justification (belongs in business description); artifact contract definitions (belongs in artifacts catalog); CLI commands or troubleshooting (belongs in ops docs).
```

### Key Changes

1. **Canonical location:** 
   - Updated to reflect **both possible locations** (co-located with job or centralized in docs/)
   - Includes `<job_group>` in path structure
2. **Purpose statement:** 
   - Added "operational + interface reference" phrasing from refined spec
   - More complete description
3. **Why necessary:** 
   - Expanded to include "troubleshoot job execution"
   - Added "mixing business rationale" boundary
4. **Must contain:**
   - Specific mention of **10 required sections** (was vague "behavior summary")
   - Listed key sections including **artifact_id cross-references** (critical refinement)
5. **Must not contain:**
   - Expanded to all **three boundary rules** (was only two)
   - Added "CLI commands or troubleshooting" (ops boundary)
   - Specific destinations for each type of excluded content

---

## Rationale: Why These Updates Matter

### 1. Catalog Accuracy

The Documentation System Catalog states its purpose:

> provide a single authoritative routing map: **document type → canonical folder location**

When catalog entries are outdated, the routing map is inaccurate, undermining the catalog's core purpose.

### 2. Preventing "Shadow Specifications"

The old entry said script cards need a "behavior summary" but the refined spec requires **10 specific sections**. Without the update, the catalog becomes a **shadow specification** — an incomplete version that conflicts with the authoritative spec.

### 3. Supporting Navigation

New contributors or agents consult the catalog to understand "what document types exist and what's in them." Outdated entries provide incorrect guidance.

### 4. Boundary Enforcement

The refined spec has three explicit boundary rules:
- Business justification → business description
- Artifact contracts → artifacts catalog  
- CLI commands → ops docs

The old catalog entry only mentioned two of these. The update ensures all three boundaries are documented in the index.

### 5. Single Source of Truth Principle

From Documentation Spec Section 1.1:

> Each fact, rule, definition, or contract must have exactly one authoritative source.

The script_card_spec is the authoritative source. The catalog **summarizes** that authority. When the spec changes significantly, the summary must be updated to maintain alignment.

---

## What Changed in the Spec (Context for Why Catalog Needed Update)

The script_card_spec was **comprehensively reworked** from 165 lines to 666 lines with:

1. **Expanded structure:** 10 normative required sections (was loosely defined)
2. **Explicit boundaries:** Full section on separation from business descriptions, artifacts catalog, and ops docs
3. **Resolved design decisions:** 3 governance decisions documented
4. **Validation approach:** Clear scope for automated vs human review
5. **Migration guidance:** How to upgrade existing script cards
6. **Consistency check appendix:** Alignment verification with 9 repository standards

The catalog entries reflected the **old, pre-rework state**. The update brings them into alignment with the **refined, comprehensive state**.

---

## Files Changed

1. **`docs/context/documentation_system_catalog.md`**
   - Entry #13 (Script Card Spec): +4 lines
   - Entry #27 (Per-job Script Card): +4 lines

2. **`docs/standards/script_card_spec.md`**
   - Cross-document impact note #3: Changed "Action required" → "Action completed (2026-01-30)"

3. **`CROSS_DOCUMENT_IMPACT_NOTE_3_EXPLANATION.md`** (new)
   - Comprehensive explanation of why the update was necessary
   - 10KB detailed rationale and comparison

---

## Status

✅ **Cross-document impact note 3: RESOLVED**

Both catalog entries (standards layer #13 and instance layer #27) have been updated to accurately reflect the refined script_card_spec. The catalog now provides accurate routing and scope information for script cards.

# Open Items Resolution Summary

## Overview

This document summarizes the resolution of three open items in the Script Card Specification (`docs/standards/script_card_spec.md`).

**Date resolved:** 2026-01-30

## Decisions Made

### 9.1 Run Receipt Format Standardization

**Decision:** Accept per-job variation for now.

**Rationale:**
- No standard run receipt schema currently exists across jobs
- Forcing standardization would block documentation of existing jobs
- Per-job variation allows operational documentation to proceed without waiting for cross-job schema alignment

**Impact on specification:**
- Script cards document whether a run receipt exists and what it contains conceptually (Section 2.9)
- No requirement to conform to a standard schema
- If a standard run receipt spec is introduced later, it may be referenced but is not mandatory

### 9.2 Validation Tooling Scope

**Decision:** Validation tooling should enforce only presence/absence of sections, not field cardinality.

**Rationale:**
- Cardinality requirements (e.g., "4–8 bullets") remain normative for human review
- Automated enforcement of cardinality would be overly rigid for edge cases
- Presence/absence checking provides structural validation without constraining legitimate variation
- Human reviewers can assess whether content meets quality expectations

**Impact on specification:**
- Section 7.1 updated with explicit scope clarification
- Automated tooling validates: section presence, required field presence, cross-reference validity
- Automated tooling does NOT validate: bullet counts, sentence counts, word limits
- Human review remains essential for operational clarity and quality

### 9.3 Cross-Job Dependency Representation

**Decision:** Automatic derivation from single source (artifacts catalog).

**Rationale:**
- Prevents inconsistency between script cards and job inventory
- Artifacts catalog is the authoritative source of producer/consumer relationships
- Manual maintenance in script cards would create "double truth"
- Aligns with "single source per contract type" principle

**Impact on specification:**
- Section 2.10 updated to clarify `upstream_jobs` and `downstream_jobs` are derived fields
- Values are computed automatically from artifacts catalog (producer/consumer relationships)
- Script cards MAY list these for human readability, but they are not authoritative
- Tooling should generate or validate these fields against artifacts catalog
- During manual documentation, use `TBD` if artifacts catalog is incomplete; resolve via catalog updates

## Changes Made to Specification

### Section 2.10 (References)

**Before:**
```
| `upstream_jobs` | Jobs this job depends on | Job IDs (comma-separated) or `TBD` or `NONE` |
| `downstream_jobs` | Jobs that consume this job's outputs | Job IDs (comma-separated) or `TBD` or `NONE` |
```

**After:**
```
| `upstream_jobs` | Jobs this job depends on (derived from artifacts catalog) | Job IDs (comma-separated) or `TBD` or `NONE` |
| `downstream_jobs` | Jobs that consume this job's outputs (derived from artifacts catalog) | Job IDs (comma-separated) or `TBD` or `NONE` |
```

**Added derivation note:**
> The `upstream_jobs` and `downstream_jobs` fields are **derived fields** computed automatically from the artifacts catalog (producer/consumer relationships). Script cards MAY list these for human readability, but the artifacts catalog is the authoritative source. During manual documentation, use `TBD` if the artifacts catalog is incomplete; resolve via catalog updates rather than manual script card maintenance.

### Section 7.1 (Validation Approach)

**Added scope clarification:**
> **Scope of automated validation (per decision 9.2):**
> - Automated tooling enforces **presence/absence** of sections and fields
> - Automated tooling does NOT enforce **field cardinality** (e.g., "4–8 bullets", "1–3 sentences")
> - Cardinality requirements remain normative for human review but are not enforced by tooling

### Section 9 (Title and Content)

**Before:** "9) Open Items / TBD"

**After:** "9) Resolved Design Decisions"

Each subsection now includes:
- The original question
- **Decision (2026-01-30):** with clear statement
- **Rationale:** explaining why the decision was made
- **Implementation:** describing how it affects the specification

### Consistency Check Appendix

**Added new subsection:**
> ### Resolved design decisions
> 
> Three design decisions documented in Section 9 (resolved 2026-01-30):
> 
> 1. **Run receipt format (9.1):** Accept per-job variation. No standard schema enforced.
> 2. **Validation tooling scope (9.2):** Automated validation enforces presence/absence only, not field cardinality.
> 3. **Dependency representation (9.3):** `upstream_jobs` and `downstream_jobs` are derived fields computed from artifacts catalog (single source).
> 
> These decisions align with:
> - Documentation system principles (single source of truth, evidence-based, no double truth)
> - Practical constraints (no standard run receipt schema exists yet)
> - Enforcement philosophy (automated structure checking, human quality review)

### Notes on Finalization

**Before:**
> 3. **Open items:** Sections 9.1–9.3 require human decisions. Should they be resolved before finalizing, or is it acceptable to finalize with TBDs?

**After:**
> 3. **Design decisions:** Section 9 documents resolved decisions for run receipt format, validation tooling scope, and dependency derivation.

## Alignment with Documentation System

All three decisions align with the repository's documentation system principles:

1. **Single source of truth:** Decision 9.3 explicitly prevents "double truth" by making artifacts catalog the single source for dependencies
2. **Evidence-based:** Decision 9.1 acknowledges practical reality (no standard schema exists)
3. **Separation of concerns:** Decision 9.2 maintains appropriate boundary between automated structure checking and human quality review
4. **No double truth:** All decisions prevent redundancy and competing authority

## Next Steps

The Script Card Specification is now complete with all design decisions resolved. Next steps:

1. **Implementation:** Build validation tooling that enforces presence/absence (per 9.2)
2. **Tooling for derivation:** Create or update tooling to derive `upstream_jobs`/`downstream_jobs` from artifacts catalog (per 9.3)
3. **Documentation of existing jobs:** Use this spec to create script cards for existing jobs, accepting per-job run receipt variation (per 9.1)
4. **Human review process:** Establish review process for operational clarity and quality (complementing automated validation)

## Statistics

- **File size:** 666 lines (was 624 lines before this update)
- **Net change:** +57 insertions, -15 deletions (+42 lines)
- **Sections updated:** 4 (Section 2.10, Section 7.1, Section 9, Consistency Check Appendix)
- **New content:** Rationale and implementation guidance for each decision

## Evidence of Completion

All three open items from the problem statement have been resolved:

✅ **9.1** = Accept per-job variation for now  
✅ **9.2** = Validation tooling should enforce only presence/absence of sections  
✅ **9.3** = Automatic derivation from single source (artifacts catalog)

The specification document now reflects these decisions with clear rationale and implementation guidance.

# Deep Analysis: business_job_description_spec.md

**Date:** 2026-01-30  
**Analysis Type:** Internal Correctness, System Fit, Completeness  
**Focus Questions:**
- a) Internal correctness and consistency
- b) Necessity and sufficiency of rules
- c) Compatibility with actual system
- d) Gaps and missing elements
- e) Content placement (belongs here vs elsewhere)

---

## Executive Summary

**Overall Assessment: STRONG with ACTIONABLE IMPROVEMENTS IDENTIFIED**

The specification is internally consistent and well-designed, with **3 critical gaps**, **2 internal inconsistencies**, and **4 content placement issues** identified through analysis against actual usage.

**Status:** Specification is usable in current form but would benefit from targeted improvements.

---

## A) Internal Correctness and Consistency

### A.1 Section Structure Consistency

**Analysis Result: INCONSISTENT - Minor Issue**

**Issue 1: Section 1 "Business purpose and context" - Inconsistent Requirements**

Lines 84-95 state:
```
**Must contain**
* Business purpose (one sentence): <exactly one sentence...>
* 1–3 sentences: business objective and what outcome is produced.
* One explicit boundary statement ("Does not …").

**Optional**
* One sentence: where it sits in the overall process landscape (or `TBD`).
```

**Problem:** The "Business purpose (one sentence)" appears to be a **label** followed by content, but the requirement "1-3 sentences" is ambiguous:
- Does this mean 1-3 sentences AFTER the one-sentence purpose?
- Or does it mean the total section is 1-3 sentences including the purpose?

**Evidence from actual usage:**
Looking at `matching_proposals/bus_description_matching_proposals.md`:
```markdown
## 1) Business purpose in your vendor→PIM mapping pipeline

This job takes the **product-level "forMapping_products" feed** (created by the previous job) and aggregates it into a **vendor-category-centric mapping proposal file**:

* For each **vendor category** (Warengruppe / Gruppenknoten from the vendor tree), it summarizes:
  * how many products are in that vendor category, and
  * into which **PIM categories** those products currently "land"...
```

The actual usage is:
1. Section heading (not matching spec's format)
2. Multi-sentence paragraph (not following "Business purpose (one sentence):" label format)
3. Nested bullets

**Verdict:** The spec's "must contain" format is NOT being followed in practice.

**Recommendation:**
```
**Must contain**
* Section heading: "Business purpose and context" (or similar)
* Opening statement: 1 sentence labeled "Business purpose:" or integrated into first paragraph
* Context: 1-3 additional sentences explaining business objective and outcome
* Boundary statement: One explicit "Does not..." or "Boundary:" statement
```

---

**Issue 2: Template vs Requirements Mismatch**

Section 2 requirements (lines 98-122) specify:
```
**Must contain**
* Plain-language list of required inputs...
* For each required input: one short phrase describing what it represents.
* Behavior when missing...

**Optional**
* Mention where the job *gets* the pointers from...
```

But the template (lines 257-264) shows:
```markdown
## Section 2: Inputs (business view)
Required inputs:
- <Artifact name> (<meaning>)
- <Artifact name> (<meaning>)
Notes: <e.g., "input pointers are taken from run receipt/config">

Optional inputs:
- <Artifact name> (<meaning>) — Behavior if absent: <...>
```

**Problem:** The template introduces "Optional inputs" subsection which is NOT mentioned in the requirements section.

**Evidence from actual usage:**
`matching_proposals/bus_description_matching_proposals.md` shows:
```markdown
## 2) Inputs (business view)

### Runtime parameters
The job requires:
* `INPUT_BUCKET`, `OUTPUT_BUCKET`
* `vendor_name`
...

### Expected input file (discovered flexibly)
It looks under:
* `<prepared_input_key>/canonicalCategoryMapping/`
```

Actual files use **different subsections** (Runtime parameters, Expected input file) than what the template suggests.

**Verdict:** Template does not match requirements OR actual usage. This creates confusion.

**Recommendation:** Either:
1. Update requirements to acknowledge runtime parameters vs data inputs, OR
2. Update template to match actual usage patterns, OR
3. Mandate strict template adherence (but this may be too restrictive)

---

### A.2 Placeholder Notation Consistency

**Analysis Result: CORRECT - Well Defined**

Section 2 note (lines 115-117):
```
**Note on placeholder notation:**
- Use `${parameter_name}` format per `docs/standards/naming_standard.md` Section 4.6
- Examples: `${vendor_name}_products.json`, not `<vendor>_products.json`
```

**Cross-check with naming_standard.md Section 4.6:**
- ✅ Correctly references naming standard
- ✅ Format `${parameter_name}` is correct for manifests
- ✅ Examples match standard

**However, actual usage shows inconsistency:**

In `matching_proposals/bus_description_matching_proposals.md` line 36:
```
* `<prepared_input_key>/canonicalCategoryMapping/`
```

Uses `<prepared_input_key>` instead of `${prepared_input_key}`.

**Root cause analysis:** The naming_standard.md Section 4.6 states:
> "In job manifests": `${NAME}` (canonical format per job_manifest_spec.md)

But business descriptions are NOT manifests—they're human-readable docs. The spec prohibits `<vendor>` notation but the actual business descriptions use angle brackets for readability in some places.

**Verdict:** The rule is TOO STRICT for business descriptions. The notation should be flexible for human readability.

**Recommendation:** Clarify that `${parameter_name}` is PREFERRED but `<parameter_name>` is ACCEPTABLE for human readability in prose, as long as it's consistent within a document.

---

### A.3 Evidence Discipline Consistency

**Analysis Result: CORRECT - Well Integrated**

Section 1 (lines 62-77) defines TBD/ASSUMPTION/Verified discipline.
Section 8 (lines 200-206) requires their use.

**Cross-check:**
- ✅ Aligns with `target_agent_system.md` Section 3.2
- ✅ Aligns with `validation_standard.md` (though validation_standard is minimal)
- ✅ Section 1 rules match Section 8 requirements

**Actual usage check:**
In `matching_proposals/bus_description_matching_proposals.md` line 176:
```markdown
## 8) Two important observations (one fact, one explicitly marked assumption)

### Fact: The "invalid category" exclusion can drop large parts of the vendor tree
...

### Assumption:
This exception rule is likely meant to avoid training on vendor categories...
```

**Verdict:** Evidence discipline IS being followed in actual usage. ✅

---

### A.4 Anti-Pattern Section Consistency

**Analysis Result: CORRECT - Comprehensive**

Section 3 (lines 219-244) lists anti-patterns:
- Shadow specifications ✅
- Tool manuals ✅
- Code-level detail ✅
- Mixing layers ✅

These align with:
- `documentation_spec.md` Section 5.3 (semantic anti-patterns)
- `documentation_system_catalog.md` Entry 12 (business description boundaries)

**Verdict:** Anti-patterns are comprehensive and correctly positioned.

---

## B) Necessity and Sufficiency of Rules

### B.1 Are All Rules Necessary?

**Analysis of each major rule:**

#### Rule: Section 1 must have "Business purpose (one sentence)"
**Necessity: HIGH** - Forces clarity and prevents rambling
**Evidence:** All actual files have a clear opening statement
**Keep:** YES

#### Rule: Section 4 must have "4-10 steps"
**Necessity: MEDIUM** - Arbitrary bounds
**Evidence:** Actual files show:
- matching_proposals: 9 steps (within range)
- category_mapping_to_canonical: 3 parts with sub-steps (doesn't match format)
**Issue:** The "4-10" is too prescriptive. Complex jobs may need more, simple jobs fewer.
**Recommendation:** Change to "4-12 steps or logical parts" for flexibility

#### Rule: Section 6 must have "2-6 bullets"
**Necessity: LOW** - Arbitrary bounds
**Evidence:** Actual files vary:
- matching_proposals: 3 bullets (within range)
- category_mapping_to_canonical: 2 bullets (within range)
**Issue:** Why minimum 2? A job might have only 1 clear non-goal.
**Recommendation:** Change to "1-6 bullets" or "at least 1 bullet"

#### Rule: Section 7 is "optional, use sparingly"
**Necessity: HIGH** - Good boundary enforcement
**Evidence:** Files use it minimally
**Keep:** YES

#### Rule: Section 9 must list "Script identifier/path"
**Necessity: HIGH** - Critical traceability
**Evidence:** Not consistently followed in actual files (they don't have Section 9!)
**Issue:** MISSING from actual business descriptions
**Action Required:** Either enforce OR make optional

---

### B.2 Are Rules Sufficient?

**CRITICAL GAP 1: No guidance on handling dynamic/parameterized behavior**

Section 4 (Processing logic) says "4-10 steps in natural language" but doesn't explain how to handle:
- Conditional logic ("if X exists, do Y, else do Z")
- Parameterized behavior ("behavior depends on vendor_name")
- Multi-phase processing ("Part 1: ..., Part 2: ...")

**Evidence from actual usage:**
`category_mapping_to_canonical/bus_description_category_mapping_to_canonical.md` uses:
```markdown
### PART 1 — Build `vendor_mappings` on products
1) Read the 3 vendor-preprocessed files.
2) Join product-category links...

### PART 2 — Enrich with existing canonical vendor→PIM mappings (if available)
If a latest `Category_Mapping_Reference_<timestamp>.json` exists:
1) Flatten reference...
```

This is a **better pattern** than the spec suggests, but the spec doesn't acknowledge multi-phase processing.

**Recommendation:** Add guidance in Section 4:
```
**For complex jobs with multiple phases:**
- Use subsections (### PART 1, ### PART 2, etc.)
- Each part can have 2-6 steps
- Total combined should remain readable (aim for <15 total steps across all parts)
```

---

**CRITICAL GAP 2: No guidance on documenting error handling at business level**

Section 2 says "Behavior when missing" should be documented for inputs, but:
- What about partial inputs (file exists but empty)?
- What about malformed inputs?
- What about downstream failure propagation?

**Evidence from actual usage:**
`matching_proposals/bus_description_matching_proposals.md` line 42:
```
If no input file is found, it writes an **empty `{}`** output and exits.
```

This is documented, but the spec doesn't mandate this level of error behavior documentation.

**Recommendation:** Add to Section 2:
```
**Must contain**
* Behavior when missing: "job fails" / "job continues with empty output" / "job skips the element"
* Behavior when empty: (if different from missing)
* Behavior when malformed: (if relevant)
```

---

**CRITICAL GAP 3: No guidance on documenting data volume expectations**

Business stakeholders often care about:
- Expected input sizes ("processes ~10K products per vendor")
- Output sizes ("generates 1 JSON object per vendor category, typically 50-200 entries")
- Performance expectations ("completes in 5-10 minutes for typical vendor")

**Evidence:** Actual business descriptions do NOT include this, which may be intentional.

**Recommendation:** Add OPTIONAL subsection guidance:
```
**Section 2 optional addition:**
* Volume expectations: typical input sizes and processing times (if relevant to business understanding)
```

---

**GAP 4: No guidance on documenting data quality rules**

Business descriptions document business rules (Section 5) but don't explicitly call out:
- Data quality checks ("rejects records with missing article_id")
- Validation rules ("skips products with invalid category references")
- Data filtering ("excludes products marked as discontinued")

**Evidence from actual usage:**
`matching_proposals/bus_description_matching_proposals.md` lines 117-124 documents:
```markdown
### Step 3 — Exception rule: exclude "ambiguous vendor categories"
...
* If a product has `vm_count > 1` (i.e., belongs to multiple vendor categories),
  then **all vendor_category_id values that occur in such multi-mapped products are marked "invalid"**.
```

This is a **data quality/filtering rule** that affects business outcomes, and it IS documented.

**Verdict:** Current Section 5 "Business rules and controls" IS sufficient if used properly, but could benefit from examples.

**Recommendation:** Add examples to Section 5:
```
**Must contain**
* Bullet list of rules that materially affect results:
  * selection/prioritization (e.g., "uses first match found")
  * exclusions (e.g., "filters out products without article_id")
  * thresholds (e.g., "requires minimum 3 products per category")
  * validation rules (e.g., "skips malformed records")
  * "truth protection" (e.g., "never overwrites existing canonical mappings")
```

---

## C) Compatibility with Actual System

### C.1 Does the Spec Match Actual Usage?

**Analysis: PARTIAL MATCH with significant deviations**

| Spec Requirement | Actual Usage | Match? |
|------------------|--------------|--------|
| Section numbering required | ✅ Files use numbered sections | ✅ YES |
| "Business purpose (one sentence):" label | ❌ Files use headings without label | ❌ NO |
| Section 2: "Required inputs" / "Optional inputs" | ❌ Files use "Runtime parameters" / "Expected input file" | ❌ NO |
| Section 4: "4-10 steps" | ⚠️ Some use multi-part structure | ⚠️ PARTIAL |
| Section 7: Optional operational notes | ✅ Used minimally | ✅ YES |
| Section 8: Assumptions and TBDs | ✅ Used correctly | ✅ YES |
| Section 9: References | ❌ MISSING from actual files | ❌ NO |

**Verdict:** Spec is NOT fully aligned with actual usage. This suggests either:
1. The spec was written AFTER the business descriptions and tried to formalize them, OR
2. The business descriptions were written BEFORE the spec was finalized, OR
3. The spec is too prescriptive and people are adapting it pragmatically

---

### C.2 Does Section 9 (References) Belong Here?

**Analysis Result: QUESTIONABLE**

Section 9 requirements (lines 209-216):
```
**Must contain**
* Script identifier/path (repo path or filename)
* Names of key artifacts referenced (inputs/outputs)
* Optional: link to run receipt / config artifact names
```

**Problem 1:** This information already exists in:
- `job_manifest.yaml` (has script path as `entrypoint` field)
- `job_inventory.md` (has job_dir, references artifacts)
- Script card (has manifest_path, artifact references)

**Problem 2:** Actual business descriptions DON'T have Section 9.

**Problem 3:** This feels like "metadata" more than "business understanding."

**Business stakeholder test:** Would a business stakeholder need "Script identifier/path" to understand what the job achieves? **NO.**

**Verdict:** Section 9 is a **metadata reference section** that belongs in a different document type, not in a business description.

**Recommendation:** 
- REMOVE Section 9 from business_job_description_spec.md
- This information is already captured in job_manifest.yaml and job_inventory.md
- If cross-referencing is needed, add a single line in Section 1: "For technical details, see `job_manifest.yaml`"

---

### C.3 Does Section 7 (Operational Notes) Create Boundary Confusion?

**Analysis Result: ACCEPTABLE but RISKY**

Section 7 is "optional, use sparingly" for operational facts that "materially affect business understanding."

**The boundary test:**
- "Critical failure behavior that affects business continuity" → **Belongs in business description? MAYBE**
- "Output behavior that affects downstream consumption" → **Belongs in business description? YES**
- "Monitoring/observability artifacts essential to business tracking" → **Belongs in business description? BORDERLINE**

**Evidence from actual usage:**
`category_mapping_to_canonical/bus_description_category_mapping_to_canonical.md` line 139:
```markdown
## 5) Output behavior (important operational detail)
After enrichment, the job writes NDJSON again and **overwrites the same final key**:
```

This is labeled "important operational detail" and placed in **Section 5** (not Section 7).

**Observation:** The actual files are blending operational detail into Section 3 (Outputs) and Section 5 (Business rules), NOT using Section 7.

**Verdict:** Section 7 exists but is NOT being used because the guidance is unclear. People are integrating operational facts contextually.

**Recommendation:** Either:
1. **Remove Section 7** and acknowledge that operational facts can be integrated into Sections 2, 3, or 5 where contextually relevant, OR
2. **Clarify Section 7** with very specific examples of what goes there vs elsewhere

---

## D) Missing Elements

### D.1 Missing: Versioning/Change Tracking Guidance

**Issue:** Business descriptions document business intent. When intent changes (e.g., new business rule added), how should this be tracked?

The spec says (Section 5, lines 297-306):
```
### Breaking changes
Changes to business descriptions are generally **non-breaking**... However, the following require decision records...
```

But it doesn't say:
- Should business descriptions be versioned?
- Should they include "Last reviewed" or "Last updated" dates?
- How to handle retroactive documentation of existing jobs?

**Evidence from actual usage:**
Files don't have explicit version numbers or dates.

**Recommendation:** Add guidance:
```
### Version tracking
Business descriptions use git history for change tracking per `documentation_spec.md` Section 4.
- No explicit version numbers in the document
- Use git blame for line-level history
- Add `Last reviewed: YYYY-MM-DD` in frontmatter only if documenting an existing job retroactively
```

---

### D.2 Missing: Guidance on Initial vs Retroactive Documentation

**Issue:** The spec assumes documentation is created during development, but many actual business descriptions are **retroactive** (documenting existing jobs).

When documenting existing jobs:
- Should you describe what the code DOES (runtime truth)?
- Should you describe what it's SUPPOSED to do (intent truth)?
- What if these diverge?

**Recommendation:** Add to Section 0:
```
### Documentation timing

**For new jobs (during development):**
Business descriptions capture intended behavior and approved business rules before/during implementation.

**For existing jobs (retroactive documentation):**
Business descriptions document observed behavior from code analysis and operational knowledge.
- Mark interpretations with ASSUMPTION:
- Mark uncertain behaviors with TBD
- If behavior contradicts apparent intent, document the contradiction in Section 8
```

---

### D.3 Missing: Concrete Examples Section

**Issue:** The template (Section 4) is abstract. New users would benefit from seeing a complete example.

**Recommendation:** Add Section 6 to the spec:
```
## 6) Complete example

See `jobs/vendor_input_processing/matching_proposals/bus_description_matching_proposals.md` for a complete reference implementation of this specification.

Key patterns demonstrated:
- Multi-sentence opening with clear boundary
- Runtime parameters documented separately from data inputs
- Processing logic with detailed steps
- Explicit fact vs assumption labeling
```

---

## E) Content Placement Issues

### E.1 Section 1: Evidence Discipline Rules

**Current location:** business_job_description_spec.md Section 1 (lines 62-77)

**Content:** Defines TBD/ASSUMPTION/Verified discipline

**Analysis:** These rules are **not specific to business descriptions**. They apply to:
- Job manifests (TBD fields)
- Script cards (TBD fields)
- Artifacts catalog (TBD fields)
- All documentation

**Verdict:** This is DUPLICATING content from `target_agent_system.md` Section 3.2.

**Issue Type:** Shadow specification / double truth

**Recommendation:** 
REPLACE Section 1 with a reference:
```
## 1) Evidence and assumptions discipline

Business descriptions must follow the evidence discipline defined in `docs/context/target_agent_system.md` Section 3.2 and `docs/standards/validation_standard.md`:

**Summary:**
- Use `TBD` for unknown facts
- Label interpretations with `ASSUMPTION:`
- Use "Verified/Confirmed" only with explicit evidence

See Section 8 of this spec for application to business descriptions.
```

This reduces duplication and maintains single source of truth.

---

### E.2 Section 3: Anti-Patterns

**Current location:** business_job_description_spec.md Section 3 (lines 219-244)

**Content:** Lists shadow specs, tool manuals, code detail, mixing layers as anti-patterns

**Analysis:** These anti-patterns are **not specific to business descriptions**. They're general documentation principles defined in `documentation_spec.md` Section 5.3.

**However:** The examples ARE specific to business descriptions ("Do NOT duplicate manifest schemas").

**Verdict:** This is PARTLY duplicative but adds value with specific examples.

**Recommendation:** Keep but clarify:
```
## 3) Anti-patterns and what NOT to include

Per `docs/standards/documentation_spec.md` Section 5.3, business descriptions must avoid these patterns.

**Business description specific guidance:**

**Shadow specifications:**
- Do NOT duplicate manifest schemas (parameters, S3 patterns) — reference `job_manifest.yaml` instead
...
```

---

### E.3 Placeholder Notation Rules

**Current location:** business_job_description_spec.md Section 2 note (lines 115-117)

**Content:** Defines `${parameter_name}` vs `<vendor>` notation

**Analysis:** This is a naming convention rule that belongs in `naming_standard.md`.

**However:** `naming_standard.md` Section 4.6 ONLY covers manifests, not business descriptions.

**Verdict:** This guidance is NEEDED here because naming_standard doesn't cover human-readable docs.

**Recommendation:** 
1. ADD to naming_standard.md Section 4.6:
```
**For human-readable documentation (business descriptions, script cards):**
- PREFERRED: Use `${parameter_name}` for consistency with manifests
- ACCEPTABLE: Use `<parameter_name>` for readability in prose
- Choose one style per document and be consistent
- Avoid: `{parameter_name}` (ambiguous)
```

2. REFERENCE from business_job_description_spec.md Section 2:
```
**Note on placeholder notation:**
- Follow `docs/standards/naming_standard.md` Section 4.6
- Example: `${vendor_name}_products.json`
```

---

### E.4 Section 9: References

**Current location:** business_job_description_spec.md Section 9 (lines 209-216)

**Content:** Requires script path, artifact names, run receipt references

**Verdict:** As analyzed in C.2, this is **metadata** that:
- Already exists in job_manifest.yaml
- Already exists in job_inventory.md
- Is NOT business understanding
- Is NOT followed in actual usage

**Recommendation:** REMOVE Section 9 entirely. Replace with:
```
## Cross-references

For technical details related to this job:
- Interface contract: see `job_manifest.yaml` in same directory
- Operational behavior: see `script_card_<job_id>.md` in same directory
- Artifact schemas: see `docs/catalogs/artifacts_catalog.md`
- Job inventory entry: see `docs/catalogs/job_inventory.md`
```

---

## F) Validation Against Script Card Spec

### F.1 Boundary Clarity Between Business Description and Script Card

**Analysis:** Let me compare requirements side-by-side:

| Concern | Business Description | Script Card |
|---------|---------------------|-------------|
| **Purpose** | WHY job exists, WHAT it does (business view) | Operational reference, runtime behavior |
| **Inputs** | Business artifacts, what they represent | bucket/key/format/required/meaning |
| **Outputs** | Business artifacts, outcome type | bucket/key/format/required/meaning/consumers |
| **Processing** | 4-10 business steps | 4-8 high-level steps (action-phrased) |
| **Rules** | Business rules affecting results | Invariants (externally meaningful) |
| **Failure** | Optional (Section 7) | MUST have failure conditions |
| **Evidence** | Assumptions/TBDs | Not mentioned |

**Overlap identified:**
1. Both require processing steps (business description: "4-10 steps", script card: "4-8 bullets")
2. Both describe inputs/outputs (business description: business view, script card: technical view)
3. Both can mention failure behavior (business description: Section 7, script card: Section 1.9)

**Clarity test:** Given a statement, can I unambiguously determine which document it belongs in?

Example statements:
- "Reads `${vendor}_products.json` from S3" → **Both acceptable** (business: Section 2, script: Section 1.4)
- "Uses Spark's `explode()` function on vendor_mappings array" → **Script card only** (implementation detail)
- "Aggregates products per vendor category" → **Business description preferred** (business transformation)
- "Fails if input file not found" → **Both acceptable** (business: Section 2, script: Section 1.9)

**Verdict:** Boundaries are MOSTLY clear but have **intentional overlap** for key operational facts.

**Recommendation:** Add comparison table to BOTH specs:
```
### Relationship to [Business Description / Script Card]

| Aspect | Business Description | Script Card |
|--------|---------------------|-------------|
| Focus | WHY and WHAT (business) | HOW (operational) |
| Inputs | Business artifacts + meaning | Technical: bucket/key/format |
| Processing | Business transformations | Operational steps |
| Failure | Critical business impacts | All failure conditions |
| Audience | Business stakeholders | Operators and developers |

**Rule:** If it affects business understanding, document in business description.
If it's needed to run/operate the job, document in script card.
Some facts belong in both (minimal duplication is acceptable).
```

---

## G) Summary of Issues

### Critical Issues (MUST FIX)

1. **Section 1 format inconsistency** - "Business purpose (one sentence):" label not followed in practice
2. **Section 9 misplacement** - Metadata that belongs elsewhere or should be removed
3. **Template mismatch** - Template doesn't match requirements or actual usage

### Important Issues (SHOULD FIX)

4. **Section 4 step count** - "4-10 steps" too restrictive, doesn't handle multi-phase jobs
5. **Section 6 bounds** - "2-6 bullets" arbitrary, should be "1-6"
6. **Placeholder notation** - Too strict for human-readable docs, should allow `<param>` for readability
7. **Evidence discipline duplication** - Section 1 duplicates target_agent_system.md

### Enhancement Opportunities (CONSIDER)

8. **Missing multi-phase guidance** - Complex jobs use PART 1/PART 2 structure not in spec
9. **Missing error handling guidance** - Need guidance on documenting empty/malformed inputs
10. **Missing versioning guidance** - How to track changes to business intent
11. **Missing retroactive documentation guidance** - How to document existing jobs
12. **Missing complete example reference** - Point to actual file as reference

---

## H) Recommendations Priority List

### Immediate Actions (Before Next Use)

1. **Fix Section 1 format** - Make "Business purpose (one sentence):" optional label, allow prose
2. **Remove or redesign Section 9** - It's not used and duplicates other docs
3. **Update template** - Match actual usage patterns (runtime params, input files)

### Short-term Improvements

4. **Relax Section 4 bounds** - Change "4-10 steps" to "4-12 steps or logical parts"
5. **Relax Section 6 bounds** - Change "2-6 bullets" to "1-6 bullets"
6. **Clarify placeholder notation** - Allow `<param>` in prose for readability

### Medium-term Enhancements

7. **Add multi-phase guidance** - Acknowledge PART 1/PART 2 pattern
8. **Add error handling guidance** - Document empty/malformed input behavior
9. **Add versioning guidance** - Reference documentation_spec for change tracking
10. **Add example reference** - Point to matching_proposals as complete example

### Long-term Considerations

11. **Consolidate evidence discipline** - Reduce duplication with target_agent_system.md
12. **Add boundary comparison table** - Show business description vs script card clearly

---

## I) Is the Spec Usable Today?

**YES, with caveats:**

✅ **Core structure is sound** - 9 sections, clear boundaries
✅ **Anti-patterns are helpful** - Prevents common mistakes
✅ **Evidence discipline is correct** - TBD/ASSUMPTION properly defined
✅ **Actual usage exists** - 3 real business descriptions following (mostly) this pattern

⚠️ **But users will struggle with:**
- Section 1 format (label vs prose)
- Section 2 structure (runtime params vs data inputs)
- Section 4 multi-phase jobs
- Section 9 (should they include it or not?)
- Placeholder notation strictness

**Recommendation:** The spec is usable TODAY but would benefit from a focused update addressing the 3 critical issues before broader adoption.

---

## J) Final Verdict

### Internal Correctness: B+ (Good with fixable issues)
- Evidence discipline: ✅ Correct
- Anti-patterns: ✅ Comprehensive
- Section structure: ⚠️ Minor inconsistencies
- Template alignment: ❌ Needs fixing

### Necessity/Sufficiency: B (Mostly sufficient)
- Core requirements: ✅ Necessary
- Bounds (4-10, 2-6): ⚠️ Too restrictive
- Error handling: ⚠️ Insufficient guidance
- Multi-phase jobs: ⚠️ Not addressed

### System Fit: B- (Works but deviates from actual usage)
- Actual files exist: ✅
- Follow spec exactly: ❌ (especially Section 1, 2, 9)
- Script card boundary: ✅ Mostly clear
- Integration: ✅ Good

### Completeness: B (Good foundation, some gaps)
- Core sections: ✅ Complete
- Versioning guidance: ❌ Missing
- Retroactive docs: ❌ Missing
- Examples: ❌ Missing
- Multi-phase guidance: ❌ Missing

### Content Placement: B+ (Mostly correct)
- Evidence discipline: ⚠️ Duplicates other docs
- Anti-patterns: ✅ Appropriate with examples
- Section 9: ❌ Misplaced metadata
- Placeholder rules: ⚠️ Should reference naming_standard

**Overall Grade: B (Good, usable, needs targeted improvements)**

---

**End of Analysis**

**Next Steps:** If improvements are desired, prioritize the 3 critical issues, then work through short-term improvements based on actual usage feedback.

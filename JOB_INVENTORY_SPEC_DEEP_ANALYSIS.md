# Job Inventory Spec - Deep Analysis: Internal Correctness, Necessity, and Practical Applicability

**Date:** 2026-01-29  
**Analyzer:** Documentation System Maintainer Agent  
**Scope:** Deep analysis of `docs/standards/job_inventory_spec.md` against actual repository data

---

## Executive Summary

### Critical Findings

**a) Internal Correctness: MULTIPLE ISSUES FOUND** ⚠️
- Several rule inconsistencies and ambiguities detected
- Placeholder normalization rule has gaps
- Dependency derivation has edge case issues
- Field sourcing rules contain contradictions

**b) Necessity and Sufficiency: MOSTLY SUFFICIENT BUT SOME GAPS** ⚠️
- Some rules are overly complex for current needs
- Missing rules for real-world scenarios found in manifests
- Unnecessary restrictions that will block adoption

**c) Practical Applicability: WILL PRODUCE MOSTLY TBD** 🚨
- **Critical:** artifacts_catalog.md is empty → all artifact linking will fail → TBD
- No business descriptions exist → business_purpose will be TBD
- Several manifest fields use TBD → evidence_artifacts will be TBD
- Result: Most inventory fields will be TBD, defeating the purpose

---

## Test Data Summary

**Jobs found:** 4 jobs in `jobs/vendor_input_processing/`
1. `preprocessIncomingBmecat` - 7 outputs, complex manifest
2. `matching_proposals` - 2 outputs, clean manifest
3. `mapping_method_training` - 12 outputs (!), very complex, has run_receipt
4. `category_mapping_to_canonical` - 2 outputs (one duplicated pattern)

**Artifacts catalog:** Nearly empty (no artifact entries with IDs)
**Business descriptions:** None exist (docs/business_job_descriptions/ does not exist)
**Current inventory:** Empty template

---

## A) Internal Correctness Analysis

### Issue 1: Job Discovery Rule - Folder Name Format (INCONSISTENCY)

**Spec lines 38-42:**
```
Canonical `job_id` rule (MUST):
- The canonical `job_id` used in `docs/job_inventory.md` MUST be the folder name `<job_id>` from `jobs/<job_group>/<job_id>/`.
- The canonical `job_id` MUST be snake_case.
- If the folder `<job_id>` is not snake_case, the inventory MUST still use the folder name as-is and MUST add an open verification item
```

**Issue:** `preprocessIncomingBmecat` is **camelCase**, not snake_case.

**Testing with actual data:**
- `preprocessIncomingBmecat` - NOT snake_case (should be `preprocess_incoming_bmecat`)
- `matching_proposals` - snake_case ✓
- `mapping_method_training` - snake_case ✓
- `category_mapping_to_canonical` - snake_case ✓

**Impact:** 1 of 4 jobs will immediately trigger `[TBD-job-id-format]` open verification item.

**Internal correctness verdict:** Rule is CORRECT but documents existing non-compliance.

---

### Issue 2: Manifest job_id vs Folder job_id (CORRECTNESS ISSUE)

**Spec lines 67-71:**
```
Manifest `job_id` consistency check (MUST):
- If the manifest contains a top-level key `job_id` and its value differs from the canonical folder-based `job_id`,
  - the inventory MUST still use the canonical folder-based `job_id`,
  - and an open verification item MUST be added:
    - `[TBD-manifest-id-mismatch] Manifest job_id differs from folder job_id for jobs/<job_group>/<job_id>/.`
```

**Testing with actual data:**
All 4 manifests have `job_id` as the first line:
- `preprocessIncomingBmecat` manifest: `job_id: preprocessIncomingBmecat` (matches folder)
- `matching_proposals` manifest: `job_id: matching_proposals` (matches folder)
- etc.

**Issue:** The check is correct, but...

**Problem:** The spec uses `job_id` as a **required manifest field** throughout Section 1.2-1.3 for sourcing other fields, BUT it's not actually used for anything except the mismatch check. This is confusing.

**Recommendation:** Clarify that manifest `job_id` is informational/validation only. Canonical `job_id` always comes from folder name.

**Internal correctness verdict:** Technically correct but potentially confusing to implementers.

---

### Issue 3: Placeholder Normalization (INCOMPLETE RULE)

**Spec lines 120-123:**
```
Placeholder normalization (deterministic):
- Replace any placeholder segments (e.g. `<vendor>`, `{vendor}`, `${vendor}`, `<timestamp>`, `{run_id}`) with the canonical token `<VAR>`.
- Compare the normalized strings literally (no fuzzy matching).
```

**Testing with actual manifest patterns:**

**From preprocessIncomingBmecat manifest:**
- Input: `${bmecat_input_key}` 
- Outputs: `${bmecat_output_prefix}${vendor_name}_vendor_products.json`

**From mapping_method_training manifest:**
- Input: `canonical_mappings/Category_Mapping_Reference_${timestamp}.json`
- Output: `${prepared_output_prefix}/mappingMethodTraining/run_receipts/run_receipt_${vendor_name}_${run_id}.json`

**Issue 1: Multi-placeholder patterns**
Pattern: `${prefix}${vendor_name}_vendor_products.json`
After normalization: `<VAR><VAR>_vendor_products.json`
This concatenates `<VAR>` tokens without separators.

**Issue 2: Static text between placeholders**
Pattern: `run_receipt_${vendor_name}_${run_id}.json`
After normalization: `run_receipt_<VAR>_<VAR>.json`
This is correct.

**Issue 3: Partial path placeholders**
Pattern: `${bmecat_input_key}` (where bmecat_input_key might be a full path or partial)
After normalization: `<VAR>`
If one manifest has `${bmecat_input_key}` and catalog has `path/to/file.xml`, no match.

**Critical Gap:** The rule doesn't handle:
- Placeholders that represent **path segments vs full paths**
- Placeholders that represent **prefixes that end without separator**

**Example of failure:**
- Manifest: `${OUTPUT_BUCKET}` / `${bmecat_output_prefix}${vendor_name}_vendor_products.json`
- Full pattern: `${bmecat_output_prefix}${vendor_name}_vendor_products.json`
- Normalized: `<VAR><VAR>_vendor_products.json`

If artifact catalog has:
- `s3://bucket/preprocessed/<vendor>_vendor_products.json`
- Normalized: `preprocessed/<VAR>_vendor_products.json`

**NO MATCH** because `<VAR><VAR>` ≠ `preprocessed/<VAR>`.

**Internal correctness verdict:** Rule is INCOMPLETE and will fail on real patterns.

**Fix needed:** Either:
1. Normalize more intelligently (preserve structure between placeholders)
2. Use fuzzy matching based on static text segments
3. Require artifact catalog to use same placeholder pattern as manifests

---

### Issue 4: Scalar TBD Handling (CORRECT BUT IMPACTS RESULTS)

**Spec lines 62-66:**
```
Scalar `TBD` handling (MUST):
- If a manifest key is present but its value is the scalar string `TBD`, treat it as unknown exactly as if the key were missing.
```

**Testing with actual manifests:**

**preprocessIncomingBmecat:**
- `logging_and_receipt.counters_observed: TBD` → will produce TBD
- `run_receipt_bucket: TBD` → but `writes_run_receipt: false`, so this is correct

**mapping_method_training:**
- `logging_and_receipt.counters_observed: TBD` → will produce TBD
- BUT `writes_run_receipt: true` with concrete bucket/key pattern

**Impact:** The rule is correct, but 3 of 4 jobs have `counters_observed: TBD`, so `evidence_artifacts.counters` will be TBD for 75% of jobs.

**Internal correctness verdict:** CORRECT. The issue is with the manifest data quality, not the spec rule.

---

### Issue 5: Dependency Derivation - Multiple Producers (CORRECTNESS ISSUE)

**Spec lines 268-270:**
```
3. If `len(producers(artifact_id)) > 1` (safety rule):
   - NO dependency link bullets MUST be created for this `artifact_id`.
   - Add an open verification item:
     - `[TBD-wiring] Multiple producers for artifact_id=<artifact_id>: <producer_job_id_1>, <producer_job_id_2>, ... . Dependency edges not generated.`
```

**Testing with mapping_method_training manifest:**

This job has outputs with **same bucket patterns as inputs:**
```yaml
inputs:
  - bucket: ${INPUT_BUCKET}
    key_pattern: canonical_mappings/stable_training_sets/StableTrainingSet.json

outputs:
  - bucket: ${INPUT_BUCKET}  # <-- SAME BUCKET as input
    key_pattern: canonical_mappings/stable_training_sets/StableTrainingSet.json
```

**Scenario:** This is an **update-in-place** pattern where a job reads a file, modifies it, and writes it back.

**Problem with spec rule:**
1. After artifact linking, this will have same `artifact_id` in both inputs and outputs
2. Job is both producer AND consumer of the same artifact
3. Is this "multiple producers" or "self-dependency"?

**Ambiguity:** The spec doesn't handle:
- Self-dependencies (job produces what it consumes)
- Update-in-place patterns
- Artifacts that are both read and written by same job

**Internal correctness verdict:** Rule is INCOMPLETE for real-world update-in-place patterns.

---

### Issue 6: Empty List Semantics (CORRECT)

**Spec lines 78-87:**
```
- `parameters`:
  - Use `parameters` (list of names) if present.
  - If `parameters` exists and is an empty list: `NONE`.
  - Else if missing: `TBD` and add `[TBD-params]`.
```

**Testing with actual manifests:**
All 4 jobs have non-empty parameter lists. Cannot test empty case.

**Hypothetical test:**
```yaml
parameters: []
```
Would correctly produce `NONE` in inventory.

**Internal correctness verdict:** CORRECT (but untestable with current data).

---

### Issue 7: Side Effects Format (CORRECT)

**Spec lines 199-200:**
```
- `side_effects`: compact string `deletes_inputs=<v>; overwrites_outputs=<v>` where `<v>` is `true|false|TBD`
```

**Testing with actual manifests:**
All 4 manifests have:
```yaml
side_effects:
  deletes_inputs: false
  overwrites_outputs: true
```

Expected inventory value: `deletes_inputs=false; overwrites_outputs=true`

**Internal correctness verdict:** CORRECT.

---

### Issue 8: Evidence Artifacts Format (AMBIGUITY)

**Spec lines 201-207:**
```
- `evidence_artifacts`: compact string `run_receipt=<v>; counters=<v>`
  - `run_receipt` value `<v>` is `true|false|TBD`
  - `counters` value `<v>` is:
    - comma-separated counter names (no values), OR
    - `NONE`, OR
    - `TBD`
```

**Testing with actual manifests:**

**mapping_method_training (writes_run_receipt=true):**
```yaml
logging_and_receipt:
  writes_run_receipt: true
  counters_observed: TBD
```
Expected: `run_receipt=true; counters=TBD`

**preprocessIncomingBmecat (writes_run_receipt=false):**
```yaml
logging_and_receipt:
  writes_run_receipt: false
  counters_observed: TBD
```
Expected: `run_receipt=false; counters=TBD`

**Question:** If `writes_run_receipt=false`, is `counters=TBD` meaningful?
- Counters typically go in run receipts
- If no receipt, how are counters observed?

**Ambiguity:** The spec treats `run_receipt` and `counters` as independent, but they're typically coupled.

**Internal correctness verdict:** Technically correct but semantically ambiguous.

---

## B) Necessity and Sufficiency Analysis

### B.1: Necessary Rules

**Rules that are clearly necessary:**

1. ✅ **Job discovery rule** (Section 1.1) - Must know what jobs exist
2. ✅ **Manifest field sourcing** (Section 1.2) - Must derive fields from manifests
3. ✅ **Table schema** (Section 3) - Must have consistent structure
4. ✅ **TBD handling** (throughout) - Must track unknowns
5. ✅ **Open verification items** (Section 5) - Must track gaps

**Verdict:** These are essential for the inventory's purpose.

---

### B.2: Overly Complex Rules

**Rules that may be unnecessarily complex:**

1. ⚠️ **Placeholder normalization** (Section 1.3, lines 120-123)
   - Problem: Complex and error-prone (see Issue 3)
   - Alternative: Require artifact catalog to use exact patterns from manifests (simpler)
   - Current approach tries to be smart but has gaps

2. ⚠️ **Business purpose extraction** (Section 1.2, lines 103-111)
   - Problem: Requires exact format `Business purpose (one sentence):`
   - Fragile: Format change breaks automation
   - Alternative: Use entire first paragraph, or require structured metadata

3. ⚠️ **Dependency derivation algorithm** (Section 4)
   - Problem: Complex algorithm (D1) with edge cases
   - Alternative: Allow manual dependency declarations in manifests
   - Current: Tries to infer from artifacts (ambitious but fragile)

**Verdict:** Some rules are more complex than necessary and introduce brittleness.

---

### B.3: Missing Rules

**Scenarios not covered by current rules:**

1. 🚨 **Config files in interface:**
   - Manifests have `config_files[]` section
   - Spec says (line 51): "config_files[] from the manifest are not represented as separate interface columns"
   - Problem: Config files are important for understanding job requirements
   - Missing: No way to track config file dependencies in inventory

2. 🚨 **Self-dependencies / Update-in-place:**
   - mapping_method_training reads and writes same artifact
   - Spec doesn't handle this pattern (see Issue 5)
   - Missing: Rules for jobs that update artifacts

3. 🚨 **Dynamic placeholders:**
   - Manifests use `${timestamp}` (select latest file at runtime)
   - Spec placeholder normalization doesn't distinguish static vs dynamic
   - Missing: How to handle runtime-determined patterns

4. 🚨 **Multiple outputs to same artifact:**
   - category_mapping_to_canonical has 2 output entries with nearly identical patterns:
     - `${prepared_output_prefix}/${vendor_name}_forMapping_products.ndjson`
     - `${prepared_output_prefix}/${vendor_name}_forMapping_products`
   - One with extension, one without
   - Missing: Rule for handling near-duplicate output patterns

5. 🚨 **Required vs optional inputs/outputs:**
   - Manifests have `required: true/false` for inputs/outputs
   - Spec doesn't use this information
   - Missing: Should inventory distinguish required vs optional artifacts?

6. 🚨 **Artifact format field:**
   - Manifests specify `format: json`, `format: ndjson`, `format: xml`
   - Spec doesn't use this
   - Missing: Should inventory show artifact formats?

**Verdict:** Several important real-world scenarios are not covered.

---

### B.4: Unnecessary Restrictions

**Rules that may block adoption:**

1. ⚠️ **Strict snake_case requirement** (lines 38-42)
   - Current reality: 1 job is camelCase
   - Effect: Will trigger open verification item
   - Question: Is snake_case critical, or is consistency critical?
   - Suggestion: Change to "folder name is canonical; snake_case is recommended"

2. ⚠️ **last_reviewed auto-set rule** (lines 218-220)
   - Rule: Automation sets `last_reviewed` only if ALL fields resolve (no TBD)
   - Current reality: artifacts_catalog is empty → all artifact links are TBD
   - Effect: `last_reviewed` will NEVER be set automatically
   - Problem: This defeats the purpose of the field
   - Suggestion: Allow `last_reviewed` to be set even with some TBD fields

3. ⚠️ **Exact table structure** (Section 2)
   - Rule: "MUST be exactly these top-level headings in this order"
   - Effect: No flexibility for evolution
   - Suggestion: Allow additional sections as long as required ones exist

**Verdict:** Some restrictions are too rigid for practical adoption.

---

## C) Practical Applicability Analysis

### C.1: Testing Spec Rules Against Actual Data

Let me simulate what the inventory would look like if generated today:

#### Job 1: preprocessIncomingBmecat

**Sourcing results:**

| Field | Source | Actual Value | Would Be TBD? |
|---|---|---|---|
| job_id | Folder name | preprocessIncomingBmecat | NO |
| job_dir | Folder path | jobs/vendor_input_processing/preprocessIncomingBmecat/ | NO |
| executor | glue_job_name present | aws_glue | NO |
| deployment_name | glue_job_name | ${JOB_NAME} | NO (literal value) |
| runtime | manifest.runtime | python_shell | NO |
| owner | (human maintained) | TBD | YES ⚠️ |
| business_purpose | Business description | TBD | YES ⚠️ (no description exists) |
| parameters | manifest.parameters | JOB_NAME, INPUT_BUCKET, OUTPUT_BUCKET, vendor_name, bmecat_input_key, bmecat_output_prefix | NO |
| inputs | manifest.inputs + catalog | TBD | YES ⚠️ (catalog empty, cannot link) |
| outputs | manifest.outputs + catalog | TBD; TBD; TBD; TBD; TBD; TBD; TBD | YES ⚠️ (7 outputs, all TBD) |
| side_effects | manifest.side_effects | deletes_inputs=false; overwrites_outputs=true | NO |
| evidence_artifacts | manifest.logging_and_receipt | run_receipt=false; counters=TBD | PARTIAL (counters TBD) |
| upstream_job_ids | Derived from artifacts | TBD | YES ⚠️ (cannot derive without artifact links) |
| downstream_job_ids | Derived from artifacts | TBD | YES ⚠️ (cannot derive without artifact links) |
| status | (human maintained) | TBD | YES ⚠️ |
| last_reviewed | Auto-set if complete | TBD | YES ⚠️ (cannot auto-set due to TBDs) |

**Open verification items generated:**
- `[TBD-job-id-format] Folder job_id is not snake_case: jobs/vendor_input_processing/preprocessIncomingBmecat/.`
- `[TBD-owner] Owner not specified for job_id=preprocessIncomingBmecat`
- `[TBD-biz-purpose] Business description missing for job_id=preprocessIncomingBmecat`
- `[TBD-artifact-catalog] No catalog match for input at position 0 in job_id=preprocessIncomingBmecat`
- `[TBD-artifact-catalog] No catalog match for output at position 0 in job_id=preprocessIncomingBmecat`
- `[TBD-artifact-catalog] No catalog match for output at position 1 in job_id=preprocessIncomingBmecat`
- ... (5 more for remaining outputs)
- `[TBD-evidence] Counters schema not defined for job_id=preprocessIncomingBmecat`

**Result: 10+ TBD markers, 12+ open verification items**

---

#### Job 2: matching_proposals

**Key differences:**
- Only 2 outputs (vs 7 for preprocessIncomingBmecat)
- Otherwise similar TBD pattern

**Result: 8+ TBD markers, 6+ open verification items**

---

#### Job 3: mapping_method_training

**Key differences:**
- Has `writes_run_receipt: true` → `run_receipt=true` (good!)
- BUT still `counters_observed: TBD`
- Has **12 outputs** → 12 artifact linking attempts, all fail

**Result: 15+ TBD markers, 16+ open verification items**

---

#### Job 4: category_mapping_to_canonical

**Key differences:**
- 2 outputs with nearly identical patterns (see B.3 Issue 4)
- Will both fail artifact linking

**Result: 8+ TBD markers, 6+ open verification items**

---

### C.2: Summary of What Would Actually Be Generated

**If job_inventory.md were generated today following the spec exactly:**

```markdown
## Jobs
| job_id | job_dir | executor | deployment_name | runtime | owner | business_purpose | parameters | inputs | outputs | side_effects | evidence_artifacts | upstream_job_ids | downstream_job_ids | status | last_reviewed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| preprocessIncomingBmecat | jobs/vendor_input_processing/preprocessIncomingBmecat/ | aws_glue | ${JOB_NAME} | python_shell | TBD | TBD | JOB_NAME, INPUT_BUCKET, ... | TBD | TBD; TBD; TBD; TBD; TBD; TBD; TBD | deletes_inputs=false; overwrites_outputs=true | run_receipt=false; counters=TBD | TBD | TBD | TBD | TBD |
| matching_proposals | jobs/vendor_input_processing/matching_proposals/ | aws_glue | ${JOB_NAME} | pyspark | TBD | TBD | JOB_NAME, INPUT_BUCKET, ... | TBD | TBD; TBD | deletes_inputs=false; overwrites_outputs=true | run_receipt=false; counters=TBD | TBD | TBD | TBD | TBD |
| mapping_method_training | jobs/vendor_input_processing/mapping_method_training/ | aws_glue | ${JOB_NAME} | python_shell | TBD | TBD | JOB_NAME, vendor_name, ... | TBD; TBD; TBD; TBD; TBD; TBD; TBD | TBD; TBD; TBD; TBD; TBD; TBD; TBD; TBD; TBD; TBD; TBD; TBD | deletes_inputs=false; overwrites_outputs=true | run_receipt=true; counters=TBD | TBD | TBD | TBD | TBD |
| category_mapping_to_canonical | jobs/vendor_input_processing/category_mapping_to_canonical/ | aws_glue | ${JOB_NAME} | pyspark | TBD | TBD | JOB_NAME, INPUT_BUCKET, ... | TBD; TBD; TBD; TBD | TBD; TBD | deletes_inputs=false; overwrites_outputs=true | run_receipt=false; counters=TBD | TBD | TBD | TBD | TBD |
```

**Fields with concrete values:** 6-7 per job (job_id, job_dir, executor, deployment_name, runtime, parameters, side_effects)
**Fields with TBD:** 9 per job (owner, business_purpose, inputs, outputs, evidence_artifacts.counters, upstream, downstream, status, last_reviewed)

**Open verification items:** ~40-50 items total

---

### C.3: Why So Many TBDs?

**Root cause analysis:**

1. 🚨 **artifacts_catalog.md is empty**
   - Effect: ALL artifact linking fails
   - Impact: inputs, outputs, upstream_job_ids, downstream_job_ids all TBD
   - This is the PRIMARY blocker

2. ⚠️ **No business descriptions**
   - Effect: business_purpose always TBD
   - Impact: Less critical but reduces value

3. ⚠️ **Manifest TBD fields**
   - Effect: counters_observed is TBD in manifests
   - Impact: evidence_artifacts.counters is TBD

4. ⚠️ **Human-maintained fields not set**
   - Effect: owner, status, last_reviewed are TBD
   - Impact: Reduces governance value

**Conclusion:** The spec will produce mostly TBD results until:
1. artifacts_catalog.md is populated with artifact entries (CRITICAL)
2. Business descriptions are created (IMPORTANT)
3. Manifests have counters defined (NICE-TO-HAVE)
4. Humans set owner/status fields (ONGOING)

---

## D) Recommendations

### D.1: Critical Fixes Required (Blockers)

1. **Fix placeholder normalization rule** (Issue 3)
   - Current rule will fail on real manifest patterns
   - Recommend: Switch to requiring artifact catalog patterns to match manifest patterns exactly
   - Alternative: Implement more sophisticated pattern matching

2. **Define artifact catalog population process**
   - Current: Catalog is empty, blocking all artifact linking
   - Recommend: Create artifact entries for the 20+ artifacts used by the 4 jobs
   - This is PREREQUISITE for inventory to have value

3. **Handle self-dependencies** (Issue 5, B.3 Issue 2)
   - Current: Spec doesn't handle update-in-place patterns
   - Recommend: Add rule for when job has same artifact in inputs and outputs
   - Suggested behavior: Mark as self-dependency, don't create circular edge

---

### D.2: Important Improvements (High Value)

4. **Relax last_reviewed auto-set rule** (B.4 Issue 2)
   - Current: Never sets last_reviewed if any TBD exists
   - Recommend: Set last_reviewed if manifest fields are successfully sourced, even if artifact linking has TBDs
   - Reason: Partial progress is better than no progress

5. **Track config_files** (B.3 Issue 1)
   - Current: config_files[] ignored
   - Recommend: Add column for config_files or note them in a separate section
   - Reason: Config files are important dependencies

6. **Support required vs optional** (B.3 Issue 5)
   - Current: All inputs/outputs treated equally
   - Recommend: Add marker (e.g., asterisk) for required artifacts
   - Example: `artifact_id*; artifact_id; artifact_id*` (asterisk = required)

---

### D.3: Nice-to-Have Enhancements

7. **Add artifact format column**
   - Would show: json, ndjson, xml, parquet
   - Value: Quick understanding of data types

8. **Support near-duplicate patterns** (B.3 Issue 4)
   - category_mapping_to_canonical has `/products.ndjson` and `/products`
   - Recommend: Treat as same artifact if they resolve to same catalog entry

9. **Improve business purpose extraction**
   - Current: Exact format required
   - Recommend: More flexible parsing or use frontmatter

10. **Version examples in spec**
    - Add worked examples showing successful artifact linking
    - Add example showing dependency derivation
    - This would clarify ambiguities

---

## E) Final Verdict

### a) Internal Correctness: ISSUES FOUND

**Rating:** ⚠️ NEEDS FIXES

**Issues:**
- Placeholder normalization is incomplete (will fail on real patterns)
- Self-dependency/update-in-place not handled
- Some semantic ambiguities (evidence_artifacts coupling)

**Severity:** Moderate to High
- Placeholder issue is BLOCKER for artifact linking
- Self-dependency is edge case but real (1 of 4 jobs affected)

---

### b) Necessity and Sufficiency: MOSTLY SUFFICIENT, SOME GAPS

**Rating:** ⚠️ GAPS EXIST

**Unnecessary complexity:**
- Placeholder normalization too clever (should be simpler)
- Some rules too rigid (snake_case, exact table order)

**Missing rules:**
- Config files not tracked
- Self-dependencies not handled
- Required vs optional not distinguished
- Dynamic placeholders not addressed

**Severity:** Moderate
- Core purpose is served but important scenarios not covered
- Some rules create friction without adding value

---

### c) Practical Applicability: WILL PRODUCE MOSTLY TBD

**Rating:** 🚨 CRITICAL GAP

**Current state:**
- artifacts_catalog.md is EMPTY → all artifact linking FAILS
- No business descriptions → business_purpose always TBD
- Result: 9 of 16 fields will be TBD for all jobs

**Impact:**
- Inventory will be of LIMITED VALUE until artifacts_catalog is populated
- The spec is CORRECT but the ECOSYSTEM is not ready

**Severity:** CRITICAL
- Spec cannot demonstrate value without populated artifacts_catalog
- This is not a spec problem but a chicken-and-egg problem

**Path forward:**
1. Populate artifacts_catalog.md FIRST (20-30 artifact entries needed)
2. Create business descriptions SECOND (4 descriptions needed)
3. THEN generate inventory to see actual value

---

## F) Immediate Action Items

**To make the spec practically useful:**

1. **CRITICAL:** Populate `docs/catalogs/artifacts_catalog.md`
   - Add entries for all artifacts used by the 4 jobs
   - Use patterns that match manifest patterns
   - This unlocks artifact linking

2. **HIGH:** Fix placeholder normalization rule
   - Simplify or clarify the matching algorithm
   - Add worked examples

3. **HIGH:** Add rule for self-dependencies
   - Handle update-in-place patterns

4. **MEDIUM:** Create business descriptions
   - 4 descriptions in `docs/business_job_descriptions/`
   - Follow format expected by spec

5. **MEDIUM:** Relax last_reviewed rule
   - Allow partial completion to set date

6. **LOW:** Consider adding config_files tracking
   - Improves completeness

---

## Conclusion

The job_inventory_spec.md is **ambitious and mostly well-designed**, but:
- Has **internal correctness issues** that need fixing (placeholder normalization, self-dependencies)
- Has **gaps** in real-world scenario coverage (config files, required/optional)
- **Cannot demonstrate value** with current repository state (empty artifacts_catalog)

**The spec is NOT BROKEN, but the ecosystem is NOT READY.**

**Recommendation:** 
1. Fix the spec issues (placeholder normalization, self-dependency)
2. Populate artifacts_catalog.md (blocking issue)
3. Then re-test to see actual results

**Estimated effort to make spec useful:**
- Spec fixes: 2-4 hours
- Artifact catalog population: 4-8 hours
- Business descriptions: 1-2 hours
- **Total: 1-2 days of focused work**

---

**END OF ANALYSIS**

## 1) What this job is for (business purpose)

This job is a **self-learning “mapping method training” run**: it learns and maintains **rule-based signals** (mapping methods) that later runs can use to **propose / validate vendor-category → PIM-category mappings**.

Concretely, it:

1. **Builds / updates a StableTrainingSet** from already-trustworthy vendor→PIM assignments (“existing_category_match”, 1→1 cases). 
2. From that training base, it derives **token-based evidence** (unigrams + token pairs) from product texts/codes and turns them into **mapping rules** per PIM category.  
3. It runs those rules against the current vendor data, produces **rule validation + vendor-category mapping status**, and then **updates the canonical Category_Mapping_Reference** (rulebase maintenance).  

---

## 2) Key inputs (what it reads)

### A) Vendor run input produced earlier (Step2 artifacts)

The job expects the vendor run’s Step2 outputs:

* `.../<vendor>_categoryMatchingProposals.json` (full)
* `.../<vendor>_categoryMatchingProposals_oneVendor_to_onePim_match.json` (1→1 subset)

Those keys are carried in the run receipt / config as `step2_full_key` and `step2_1to1_key`. 

### B) Canonical mapping reference + training set

* Latest `Category_Mapping_Reference_<...>.json` (selected as input reference) 
* `StableTrainingSet.json` (read if exists, otherwise created) 

### C) Denylist configuration (token hygiene)

A denylist config is loaded and used to remove “bad / generic / unwanted” tokens from the learned rulebase.  

---

## 3) What it produces (business outputs)

The outputs are **operational artifacts for governance + mapping automation**:

### A) Training base artifacts

* `stable_training_set_delta_<vendor>_<run_id>.json` (what changed / was added this run) 
* Updated `StableTrainingSet.json` (persistent knowledge across runs) 

### B) Evidence + rulebase artifacts

* Stable training evidence for tokens (unigrams) and token-pairs (co-occurrence) per PIM category  
* Generated mapping rules per PIM category (three operator families) 

### C) Run validation / monitoring artifacts

* `rule_validation_status_<vendor>_<run_id>.ndjson` (for each rule: supported / violated / not_applicable + run proof/coverage) 
* `vendor_category_mapping_status_<vendor>_<run_id>.json` which classifies each vendor category as:

  * `unambiguous`
  * `conflicting`
  * `insufficient`
  * `no_rule_hits` 

### D) Updated canonical rulebase

* Writes a **new** `Category_Mapping_Reference_<new_suffix>.json` with updated `mapping_methods` (rules), and records the input/output keys in the run receipt. 

---

## 4) How it works end-to-end (business logic, stepwise)

### Step 1 — Build truth-based training delta (what counts as “learning data”)

It extracts training records only from trusted assignments:

* it uses the 1→1 subset and relies on the assignment source being “existing_category_match” (i.e., previously confirmed mapping), then creates delta records including vendor category metadata and the set of products used as proof.  

### Step 2 — Persist learning: upsert StableTrainingSet

The delta is merged into the long-lived `StableTrainingSet.json`, so learned evidence is not lost between runs. 

### Step 3 — Build evidence from product fields (signal extraction)

For each PIM category in the StableTrainingSet, it builds token evidence from three fields:

* **KEYWORD**
* **DESCRIPTION_SHORT**
* **CLASS_CODES**

It normalizes tokens (including plural normalization) and removes denylisted tokens for KEYWORD/DESCRIPTION_SHORT. 

It also builds **token-pair evidence** (co-occurrence patterns) and prunes pairs below a minimum stored count to keep only meaningful patterns.  

### Step 4 — Generate mapping rules (candidate “mapping methods”)

It generates rule candidates per PIM category across operator types such as:

* `contains_any`
* `contains_all`
* `contains_any_exclude_any` 

(These become “mapping_methods” entries later.)

### Step 5 — Validate rules on the current vendor run

It applies rules to vendor categories/products and produces:

* per-rule validation (supported/violated/not_applicable + proof stats) 
* vendor category mapping status (unambiguous/conflicting/insufficient/no_rule_hits) based on which supported rules fired and whether they pass threshold. 

Threshold evaluation is explicitly used while building per-vendor-category rule results (`pass_threshold`). 

### Step 6 — Update Category_Mapping_Reference (rulebase maintenance)

This is a governance-critical step:

* It constructs the next `mapping_methods` per PIM category from rule validation results, **deduplicates** by method signature, and **sorts** methods deterministically. 
* It **guards** against accidental changes to the canonical **vendor_mappings**: it compares vendor_mappings JSON before/after and aborts the write if anything changed. 
* It writes a new reference file `Category_Mapping_Reference_<suffix>.json`. 

Promotion policy is explicitly recorded as:

* “supported_and_pass_threshold_only”
* violated rules removed
* not_applicable retained (i.e., stays in rulebase) 

---

## 5) Two important business safeguards (why this matters)

1. **Truth protection:** the job will not silently alter your manual/canonical vendor mappings while updating mapping methods—if it detects a change, it aborts. 
2. **Rule quality controls:** denylist removal + threshold gating + explicit supported/violated tracking prevents noisy rules from accumulating in the canonical rulebase.  

---

## Interpretation (explicitly marked)

**Interpretation (not a direct fact statement):** This job is the “learning loop” that continuously improves the rule-based layer used to map vendor categories (and indirectly vendor assortment) to PIM categories by updating `Category_Mapping_Reference` with validated `mapping_methods`. This interpretation is based on the fact that it writes a new reference file containing refreshed `mapping_methods` from rule validation outputs. 

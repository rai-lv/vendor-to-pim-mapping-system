## 1) Business purpose in your vendor→PIM mapping pipeline

This job takes the **vendor-preprocessed datasets** (from the previous job) and produces **one “forMapping_products” product feed** that is already enriched with:

1. each product’s **vendor category mapping context** (vendor category id/name/path/type), and
2. a **preliminary PIM category assignment**:

* first via **existing canonical vendor→PIM mappings** (if present),
* then via **rule-based matching** (mapping methods) against product signals (description / keywords / class codes). 

**Important boundary (fact):** this job assigns **PIM categories**, not a full SKU-level “same-as PIM product” match. It’s a category mapping enrichment step for downstream jobs. 

---

## 2) Inputs (business view)

### Runtime parameters

The job requires:

* `INPUT_BUCKET`, `OUTPUT_BUCKET`
* `vendor_name`
* `preprocessed_input_key` (treated as a **prefix** where the vendor files are located)
* `prepared_output_prefix` (target prefix for results) 

### Required preprocessed vendor files under `preprocessed_input_key/`

It searches the prefix for these vendor-specific files:

* `<vendor>_vendor_products.json`
* `<vendor>_product_category_links.json`
* `<vendor>_vendor_categories.json` 

If any of these three are missing, the job fails. 

### Optional canonical mapping reference (for enrichment + rules)

It tries to find the **latest** file in:

* `s3://<INPUT_BUCKET>/canonical_mappings/Category_Mapping_Reference_<timestamp>.json` 

If none exists, it **does not fail**; it just leaves PIM assignment fields empty and skips rule-based logic. 

---

## 3) What the job produces (business datasets / objects)

### Main output: `<vendor>_forMapping_products` (NDJSON, 1 record per vendor product)

Each product record is basically your vendor product object plus:

#### A) `vendor_mappings` array (category context per product)

Built by joining:

* product↔vendor-category links
  with
* vendor category master data (name/path/type)

and aggregating into:

````json
"vendor_mappings": [
  {
    "vendor_short_name": ...,
    "vendor_category_id": ...,
    "vendor_category_name": ...,
    "vendor_category_path": ...,
    "vendor_category_type": ...
  }
]
``` :contentReference[oaicite:8]{index=8}

#### B) PIM category assignment fields (preliminary)
The job adds/maintains:
- `pim_category_id`
- `pim_category_name`
- `assignment_source`
- `assignment_confidence` :contentReference[oaicite:9]{index=9}

---

## 4) Processing logic (business flow)

### PART 1 — Build `vendor_mappings` on products
1) Read the 3 vendor-preprocessed files. :contentReference[oaicite:10]{index=10}  
2) Join product-category links to vendor categories to enrich category metadata. :contentReference[oaicite:11]{index=11}  
3) Aggregate per product to create `vendor_mappings[]`. :contentReference[oaicite:12]{index=12}  
4) Write NDJSON output to `OUTPUT_BUCKET` and copy it to the final key:  
`<prepared_output_prefix>/<vendor>_forMapping_products` :contentReference[oaicite:13]{index=13}  

**Business meaning:** after this part, every product carries its vendor-category “where does the vendor place this product?” context.

---

### PART 2 — Enrich with existing canonical vendor→PIM mappings (if available)
If a latest `Category_Mapping_Reference_<timestamp>.json` exists:

1) Flatten reference `vendor_mappings[]` into rows `(vendor_short_name, vendor_category_id) → (pim_category_id, pim_category_name)`. :contentReference[oaicite:14]{index=14}  
2) Explode each product’s `vendor_mappings[]` and join to the reference mappings. :contentReference[oaicite:15]{index=15}  
3) Per product, take the **first non-null** PIM category match found. :contentReference[oaicite:16]{index=16}  
4) If a PIM category is assigned here, set:
- `assignment_source = "existing_category_match"`
- `assignment_confidence = "full"` :contentReference[oaicite:17]{index=17}  

If no reference file exists (or it contains no usable vendor mappings), the job keeps the PIM fields empty and continues (rule part may be skipped depending on availability). :contentReference[oaicite:18]{index=18}

**Business meaning:** this is the “use what we already know and trust” step.

---

### PART 3 — Rule-based matching for products that are still unmapped
This part is only executed if the mapping reference exists and contains `mapping_methods`. :contentReference[oaicite:19]{index=19}  

It evaluates unmapped products (i.e., not already `existing_category_match`) against rules derived from the reference file’s `mapping_methods`, grouped by field:

- `DESCRIPTION_SHORT` rules (tokenized text)  
- `KEYWORD` rules (tokenized keyword list)  
- `CLASS_CODES` rules (normalized system + code tokens, e.g. `eclass-5.1:21052103`) :contentReference[oaicite:20]{index=20}  

**Rule evaluation mechanics (business view):**
- Each PIM category can have multiple methods per field. A product “hits” a PIM category if one or more methods match. The job counts how many methods matched per PIM category per signal. :contentReference[oaicite:21]{index=21}  
- It then tries to resolve a final PIM assignment:
  - If the **intersection** of candidate PIM IDs across the non-empty signals is **exactly 1**, it assigns that single PIM category.
    - `assignment_source` indicates which signals contributed (e.g., `code_class_and_keyword_match`). :contentReference[oaicite:22]{index=22}  
    - `assignment_confidence` becomes the **sum of method-hit counts** (stored as a string). :contentReference[oaicite:23]{index=23}  
  - If there is **no unique intersection**, it sets:
    - `pim_category_id` to a `|`-separated list of candidate IDs  
    - `pim_category_name` to a `|`-separated list of names  
    - `assignment_confidence = "mixed"` :contentReference[oaicite:24]{index=24}  

The job also prints statistics about how many products had hits per signal and how many ended up as unique vs mixed outcomes. :contentReference[oaicite:25]{index=25}  

**Business meaning:** this is a “best-effort, explainable rule inference” step for unmapped products, based on your maintained mapping methods.

---

## 5) Output behavior (important operational detail)
After enrichment, the job writes NDJSON again and **overwrites the same final key**:
- `s3://<OUTPUT_BUCKET>/<prepared_output_prefix>/<vendor>_forMapping_products` :contentReference[oaicite:26]{index=26}  

So the output of this job is a **single canonical “forMapping” product feed** for the vendor run, progressively enriched inside this job. :contentReference[oaicite:27]{index=27}

---

## 6) Key business rules / controls embedded in the job
- **Hard fail** if the 3 required vendor input datasets are missing. :contentReference[oaicite:28]{index=28}  
- **Graceful behavior** if no Category_Mapping_Reference exists: keep PIM fields empty; don’t fail. :contentReference[oaicite:29]{index=29}  
- **Existing matches are protected:** products already assigned via `existing_category_match` are excluded from rule evaluation. :contentReference[oaicite:30]{index=30}  
- **German-aware token normalization:** converts umlauts (ä→ae etc.), lowercases, drops short tokens, filters a fixed stopword list, and drops numeric-only tokens in certain fields. :contentReference[oaicite:31]{index=31}  
- **Class code normalization:** e.g., anything starting with “eclass…” is normalized to `eclass-5.1` for token consistency. :contentReference[oaicite:32]{index=32}  

---

## 7) What this job does *not* do (boundary)
- It does not build vendor-category-level mapping proposals; it assigns at **product level** (per article_id). :contentReference[oaicite:33]{index=33}  
- It does not attempt entity resolution “vendor SKU == PIM SKU”; it only prepares/enriches vendor products with **PIM category assignment fields** to support later mapping/training steps. :contentReference[oaicite:34]{index=34}

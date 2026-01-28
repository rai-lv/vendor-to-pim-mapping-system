## 1) Business purpose in your vendor→PIM mapping pipeline

This job takes the **product-level “forMapping_products” feed** (created by the previous job) and aggregates it into a **vendor-category-centric mapping proposal file**:

* For each **vendor category** (Warengruppe / Gruppenknoten from the vendor tree), it summarizes:

  * how many products are in that vendor category, and
  * into which **PIM categories** those products currently “land” (based on the product-level preliminary PIM assignment fields),
  * including **product examples** per PIM match cluster.

So the output is essentially:
**“For vendor category X, here is the distribution of products across PIM categories + evidence.”** 

This is a **category mapping proposal builder**, not a product master matching job. 

---

## 2) Inputs (business view)

### Runtime parameters

The job requires:

* `INPUT_BUCKET`, `OUTPUT_BUCKET`
* `vendor_name`
* `prepared_input_key`
* `prepared_output_prefix` 

### Expected input file (discovered flexibly)

It looks under:

* `<prepared_input_key>/canonicalCategoryMapping/`

and expects a base name:

* `<vendor_name>_forMapping_products`

It supports presence/absence of “.json” and even other extensions by listing S3 keys if needed. 

If no input file is found, it writes an **empty `{}`** output and exits. 

---

## 3) Output files (business view)

It writes two JSON outputs (pretty printed, not NDJSON):

1. **Full proposals**

* `<prepared_output_prefix>/<vendor>_categoryMatchingProposals.json`

2. **Subset: one vendor category → one PIM match**

* `<prepared_output_prefix>/<vendor>_categoryMatchingProposals_oneVendor_to_onePim_match.json` 

Both outputs are JSON dictionaries keyed by `vendor_category_id`. 

---

## 4) What the “full proposals” output contains

For each `vendor_category_id`, the record includes:

### A) Vendor category metadata (`vendor_mappings`)

* vendor_short_name
* vendor_category_id
* vendor_category_name
* vendor_category_path
* vendor_category_type 

### B) `total_products_in_vendor_category`

Count of products assigned to this vendor category (after applying the exception filter described below). 

### C) `pim_matches` list

A list of “clusters”, each representing one PIM category outcome for products in this vendor category, split by method/source:

Each entry includes:

* `pim_category_id` (or `"UNMATCHED"` if missing)
* `pim_category_name` (if present)
* `assignment_source` (e.g., existing match vs rule-match label)
* `assignment_confidence` (either `"full"`, `"mixed"`, or a numeric-like string from upstream job)
* `products_in_pim_category` (count)
* `products`: **list of product evidence objects** with:

  * article_id
  * description_short
  * keywords
  * class_codes (as `{system, code}` list) 

Business meaning: you can review each vendor category and see **which PIM categories appear and why**, with concrete product examples to validate/curate mappings.

---

## 5) Business processing logic (step-by-step)

### Step 1 — Read the product feed

Reads the discovered `forMapping_products` JSON (tries normal read, falls back to `multiLine=true`).
Fails gracefully to `{}` if the file is empty or lacks `vendor_mappings`. 

### Step 2 — Explode product.vendor_mappings[]

Each product can have vendor_mappings as an array; the job explodes it so each row represents:

* one product
* one vendor-category assignment 

### Step 3 — Exception rule: exclude “ambiguous vendor categories”

This is a crucial business rule in this job:

* It counts `vm_count = size(vendor_mappings)` per product.
* If a product has `vm_count > 1` (i.e., belongs to multiple vendor categories),
  then **all vendor_category_id values that occur in such multi-mapped products are marked “invalid”**.
* Then the job removes **all rows** belonging to these invalid vendor categories from further processing. 

**Business meaning (fact from code):**
A vendor category is excluded entirely if there exists at least one product that maps to it **and** also maps to another vendor category. This is an aggressive “purity” filter to keep vendor categories clean for training/review.

### Step 4 — Normalize missing PIM assignment as `"UNMATCHED"`

If `pim_category_id` is missing/empty, set a normalized field:

* `pim_category_id_norm = "UNMATCHED"` 

Also ensures columns exist for downstream aggregation: assignment_source/confidence, pim_category_name, and product detail columns. 

### Step 5 — Aggregate “PIM match clusters” per vendor category

Group by:

* vendor_category_id
* pim_category_id_norm
* assignment_source
* assignment_confidence

For each group, compute:

* products_in_pim_category
* collect_list(products with details) 

Then collect those groups as `pim_matches[]` per vendor_category_id.

### Step 6 — Aggregate vendor category metadata + totals

For each vendor_category_id, take first (non-null) values for name/path/type and count total products. 

### Step 7/8 — Build a dictionary keyed by vendor_category_id

It collects Spark results to the driver and produces the final JSON dict structure described above, including product evidence per cluster. 

### Step 9 — Write the full proposals JSON

Writes pretty JSON to S3. 

---

## 6) What the “oneVendor_to_onePim” subset means (and how it’s chosen)

From the full dictionary, it selects vendor categories where:

* Exactly **one** `pim_matches` entry exists (i.e., the vendor category’s products all landed in exactly one cluster), AND
* `assignment_confidence` of that single entry is not:

  * `"mixed"`
  * `"null"`
  * empty / None 

Those selected vendor categories are written unchanged into the subset file.

**Business meaning:** this subset is intended as a “highly unambiguous” training/automation candidate set (“this vendor category maps cleanly to exactly one PIM category outcome”). (This interpretation is an assumption; the code itself only enforces the conditions above.) 

---

## 7) What this job does *not* do (boundary)

* It does not create or change mapping rules.
* It does not decide the “true” vendor→PIM category mapping; it only summarizes **current preliminary assignments** from the product feed.
* It does not compute textual similarity etc.; it’s an **aggregation and evidence packaging** job. 

---

## 8) Two important observations (one fact, one explicitly marked assumption)

### Fact: The “invalid category” exclusion can drop large parts of the vendor tree

Because a single multi-mapped product can invalidate an entire vendor category, this can suppress many categories if the vendor data commonly assigns products to multiple categories. 

### Assumption:

This exception rule is likely meant to avoid training on vendor categories that are not “pure” (products belong to multiple categories), because such categories create ambiguity/noise for stable vendor→PIM mapping learning.

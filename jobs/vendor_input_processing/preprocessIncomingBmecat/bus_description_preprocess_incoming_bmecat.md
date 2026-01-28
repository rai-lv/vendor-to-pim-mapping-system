## 1) Business purpose in your vendor→PIM mapping pipeline

This job is a **vendor BMECAT preprocessing / structuring step**:

* It takes a **vendor BMECAT XML** and converts it into multiple **normalized, line-based JSON datasets (NDJSON)**.
* The result is a set of “cleanly separable” datasets (products, features, category links, etc.) that later jobs can use to **match vendor assortment to your PIM assortment** (e.g., via identifiers, category mappings, attributes/classifications, etc.). 

**Important fact:** this job **does not perform vendor→PIM matching itself**. It only extracts and structures vendor data into prepared outputs. 

---

## 2) Inputs (business view)

### Runtime parameters (Glue arguments)

The job expects these inputs at runtime:

* `INPUT_BUCKET`, `OUTPUT_BUCKET`
* `vendor_name`
* `bmecat_input_key` (S3 key to the BMECAT XML)
* `bmecat_output_prefix` (S3 prefix for outputs) 

### Vendor-specific extraction configuration

It loads a vendor-specific config JSON from:

* `s3://<INPUT_BUCKET>/configuration-files/incomingVendorBmecatPreprocessing_configs/incomingVendorBmecatPreprocessing_config_<vendor_name>.json` 

**Business meaning:** you can onboard different vendors / BMECAT variants by changing config paths/fields, without rewriting code.

---

## 3) What the job extracts (business datasets)

The job parses the BMECAT XML (including removing XML namespaces so paths match) and produces these datasets:

### A) `vendor_products` (required)

One record per vendor article (product), keyed by `article_id`, plus:

* vendor name
* configurable “simple fields” (e.g., descriptions, manufacturer, etc. — whatever the config maps)
* `keywords` (list; extracted from configured paths)
* `class_codes` (list of `{system, code}`; pulled from ARTICLE_FEATURES and optionally filtered by allowed systems) 

### B) `product_features` (required)

A flattened “attribute/value” style dataset per product:

* joins to product via `article_id`
* extracts feature system/group metadata + individual feature rows (name, value, unit, order etc. per config)
* supports **exploding multiple feature values** (one row per value) if configured
* performs **deduplication** (default dedup key: `article_id`, `fname`, `fvalue` unless config overrides) 

### C) `product_category_links` (required)

A dataset that links products to vendor category nodes (BMECAT “article to catalog group map” type structure), extracted from a configured root path and fields. 

### D) Optional datasets (only if present in config)

* `product_mimes`: media links per product (type/source/purpose/etc.)
* `product_relations`: product-to-product relations (e.g., accessories), incl. attribute-based fields like `@type`
* `product_prices`: extracted price rows (incl. `@price_type`, amount, currency)
* `vendor_categories`: vendor category tree nodes; additionally can compute a **category path** (e.g., `"A > B > C"`) via parent relations, using special config notation like `ancestors.GROUP_NAME` 

---

## 4) Outputs (business view)

It writes each dataset as **NDJSON** (newline-delimited JSON records) into **single S3 objects** in `OUTPUT_BUCKET`, named like:

* `<bmecat_output_prefix>/<vendor>_vendor_products.json`
* `<...>/<vendor>_product_features.json`
* `<...>/<vendor>_product_category_links.json`
* plus optional ones (`_product_mimes.json`, `_product_relations.json`, `_product_prices.json`, `_vendor_categories.json`) 

It also prints a final **job summary** with record counts per dataset and skipped counts. 

---

## 5) Key business rules / controls embedded in the job

These behaviors matter for downstream mapping quality and reliability:

1. **Fail-fast if no products found**

* If the configured ARTICLE root path yields **0 ARTICLE nodes**, the job fails hard. 

2. **Skip products without a usable key**

* If `article_id` cannot be extracted (primary path, then fallback path), the product is **skipped** (and counted as `skipped_articles_no_id`). 

3. **Config-path mismatch visibility**

* If a configured XML path is missing, it logs a **warning once per path**, not per record (reduces log spam while still signaling schema/config drift). 

4. **Supports multiple BMECAT “shapes”**

* The job’s path resolution is intentionally “simple path” based and namespace-agnostic (namespace stripped), enabling vendor-specific variations to be handled via config. 

---

## 6) What this job does *not* do (important boundary)

* It does **not** compare against your PIM assortment.
* It does **not** calculate match candidates, similarity scores, canonical category assignments, dedup across vendor vs PIM, etc.

**Business interpretation:** this is a **standardization / extraction stage** that produces the raw material needed for the actual vendor→PIM mapping jobs that follow. 

# Artifacts Catalog

This file follows docs/standards/artifacts_catalog_spec_v1.1.md.

## preprocess_incoming_bmecat__tbd

- artifact_id: preprocess_incoming_bmecat__tbd
- file_name_pattern: TBD
- s3_location_pattern:
  - s3://${INPUT_BUCKET}/${bmecat_input_key}
- format: xml
- producer_job_id: TBD
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Vendor BMECAT XML input used by the preprocessing job to extract and structure vendor data into normalized datasets.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__incoming_vendor_bmecat_preprocessing_config_vendor_name

- artifact_id: preprocess_incoming_bmecat__incoming_vendor_bmecat_preprocessing_config_vendor_name
- file_name_pattern: incomingVendorBmecatPreprocessing_config_${vendor_name}.json
- s3_location_pattern:
  - s3://${INPUT_BUCKET}/configuration-files/incomingVendorBmecatPreprocessing_configs/incomingVendorBmecatPreprocessing_config_${vendor_name}.json
- format: json
- producer_job_id: TBD
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Vendor-specific preprocessing configuration JSON that controls BMECAT extraction paths and mappings for the job.
- content_contract:
  - top_level_type: TBD
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_products

- artifact_id: preprocess_incoming_bmecat__vendor_products
- file_name_pattern: ${vendor_name}_vendor_products.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_vendor_products.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: Line-delimited dataset of vendor product records extracted from BMECAT, one record per article, keyed by article_id.
- content_contract:
  - top_level_type: scalar
  - primary_keying: keyed by article_id
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__product_features

- artifact_id: preprocess_incoming_bmecat__product_features
- file_name_pattern: ${vendor_name}_product_features.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_features.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Line-delimited dataset of product feature rows extracted from BMECAT, representing attribute/value pairs per product.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__product_category_links

- artifact_id: preprocess_incoming_bmecat__product_category_links
- file_name_pattern: ${vendor_name}_product_category_links.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_category_links.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: Line-delimited dataset linking vendor products to vendor category nodes extracted from BMECAT.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__product_mimes

- artifact_id: preprocess_incoming_bmecat__product_mimes
- file_name_pattern: ${vendor_name}_product_mimes.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_mimes.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Optional line-delimited dataset of product media (mimes) extracted from BMECAT.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__product_relations

- artifact_id: preprocess_incoming_bmecat__product_relations
- file_name_pattern: ${vendor_name}_product_relations.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_relations.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Optional line-delimited dataset of product-to-product relations extracted from BMECAT.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__product_prices

- artifact_id: preprocess_incoming_bmecat__product_prices
- file_name_pattern: ${vendor_name}_product_prices.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_prices.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: Optional line-delimited dataset of product prices extracted from BMECAT.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_categories

- artifact_id: preprocess_incoming_bmecat__vendor_categories
- file_name_pattern: ${vendor_name}_vendor_categories.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_vendor_categories.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: Optional line-delimited dataset of vendor category tree nodes extracted from BMECAT.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: Line-delimited JSON records.
- stability: evolving
- breaking_change_rules: TBD

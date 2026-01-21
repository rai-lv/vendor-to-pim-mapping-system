# Artifacts Catalog
Follows docs/standards/artifacts_catalog_spec_v1.1.md

## preprocess_incoming_bmecat__bmecat_input_key

- artifact_id: preprocess_incoming_bmecat__bmecat_input_key
- file_name_pattern: ${bmecat_input_key}
- s3_location_pattern:
  - s3://${INPUT_BUCKET}/${bmecat_input_key}
- format: xml
- producer_job_id: TBD
- producer_glue_job_name: TBD
- consumers:
  - preprocessIncomingBmecat
- purpose: BMECAT XML input file for preprocessing incoming vendor data.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_vendor_products

- artifact_id: preprocess_incoming_bmecat__vendor_name_vendor_products
- file_name_pattern: ${vendor_name}_vendor_products.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_vendor_products.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: NDJSON listing vendor products extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_product_features

- artifact_id: preprocess_incoming_bmecat__vendor_name_product_features
- file_name_pattern: ${vendor_name}_product_features.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_features.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: NDJSON of product feature records extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_product_category_links

- artifact_id: preprocess_incoming_bmecat__vendor_name_product_category_links
- file_name_pattern: ${vendor_name}_product_category_links.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_category_links.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: NDJSON mapping vendor products to their category links from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_product_mimes

- artifact_id: preprocess_incoming_bmecat__vendor_name_product_mimes
- file_name_pattern: ${vendor_name}_product_mimes.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_mimes.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: NDJSON of product media (mimes) extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_product_relations

- artifact_id: preprocess_incoming_bmecat__vendor_name_product_relations
- file_name_pattern: ${vendor_name}_product_relations.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_relations.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: NDJSON of product relation records extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_product_prices

- artifact_id: preprocess_incoming_bmecat__vendor_name_product_prices
- file_name_pattern: ${vendor_name}_product_prices.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_product_prices.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - TBD
- purpose: NDJSON of product pricing records extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__vendor_name_vendor_categories

- artifact_id: preprocess_incoming_bmecat__vendor_name_vendor_categories
- file_name_pattern: ${vendor_name}_vendor_categories.json
- s3_location_pattern:
  - s3://${OUTPUT_BUCKET}/${bmecat_output_prefix}${vendor_name}_vendor_categories.json
- format: ndjson
- producer_job_id: preprocessIncomingBmecat
- producer_glue_job_name: ${JOB_NAME}
- consumers:
  - category_mapping_to_canonical
- purpose: NDJSON of vendor category records extracted from the BMECAT feed.
- content_contract:
  - top_level_type: scalar
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

## preprocess_incoming_bmecat__incoming_vendor_bmecat_preprocessing_config_vendor_name

- artifact_id: preprocess_incoming_bmecat__incoming_vendor_bmecat_preprocessing_config_vendor_name
- file_name_pattern: incomingVendorBmecatPreprocessing_config_${vendor_name}.json
- s3_location_pattern:
  - s3://${INPUT_BUCKET}/configuration-files/incomingVendorBmecatPreprocessing_configs/incomingVendorBmecatPreprocessing_config_${vendor_name}.json
- format: TBD
- producer_job_id: TBD
- producer_glue_job_name: TBD
- consumers:
  - preprocessIncomingBmecat
- purpose: Configuration file for preprocessing incoming vendor BMECAT data.
- content_contract:
  - top_level_type: TBD
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD

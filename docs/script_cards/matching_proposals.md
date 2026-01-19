# matching_proposals — Script Card

## Identity
- job_id: matching_proposals
- glue_job_name: TBD
- runtime: pyspark
- repo_path: jobs/vendor_input_processing/matching_proposals/glue_script.py
- manifest_path: jobs/vendor_input_processing/matching_proposals/job_manifest.yaml

## Purpose
- Builds category matching proposals by aggregating vendor category mappings and associated PIM category matches from the prepared input dataset, then writes JSON outputs to S3. Produces a full mapping and a filtered oneVendor_to_onePim subset when possible.

## Trigger and Orchestration
- Triggered by: TBD
- Required parameters: JOB_NAME, INPUT_BUCKET, OUTPUT_BUCKET, vendor_name, prepared_input_key, prepared_output_prefix
- Preconditions: TBD

## Inputs
- Input 1:
  - bucket: ${INPUT_BUCKET}
  - key_pattern: TBD
  - format: json
  - required: TBD
  - meaning: JSON product records under the prepared input key, specifically the canonicalCategoryMapping file named <vendor_name>_forMapping_products (with or without a .json extension) as discovered by the script.

## Outputs
- Output 1:
  - bucket: ${OUTPUT_BUCKET}
  - key_pattern: ${prepared_output_prefix}/${vendor_name}_categoryMatchingProposals.json
  - format: json
  - required: TBD
  - meaning: Pretty-printed JSON dictionary keyed by vendor_category_id containing vendor category metadata, total products, and aggregated pim_matches with product details.
  - consumers: TBD
- Output 2:
  - bucket: ${OUTPUT_BUCKET}
  - key_pattern: ${prepared_output_prefix}/${vendor_name}_categoryMatchingProposals_oneVendor_to_onePim_match.json
  - format: json
  - required: TBD
  - meaning: Subset of the main output containing only vendor categories with exactly one pim_match whose assignment_confidence is non-empty and not equal to "mixed" or "null".
  - consumers: TBD

## Side Effects
- deletes_inputs: TBD
- overwrites_outputs: TBD
- other_side_effects: Writes JSON objects to S3 output locations.

## High-level Processing (Factual)
- Resolve Glue arguments and initialize Spark/Glue contexts.
- Discover the input JSON file under prepared_input_key/canonicalCategoryMapping using candidate filenames or S3 listing.
- Read input JSON into a Spark DataFrame (fallback to multiLine JSON) and handle empty/missing vendor_mappings cases by writing an empty output.
- Explode vendor_mappings, identify vendor_category_id entries tied to products with multiple vendor_mappings, and exclude those categories.
- Normalize pim_category_id values and ensure required columns exist for aggregation.
- Aggregate pim_matches by vendor_category_id with counts and product details, then join with vendor metadata.
- Collect results to a dictionary keyed by vendor_category_id and write the main JSON output.
- Derive and write the oneVendor_to_onePim subset based on pim_matches cardinality and assignment_confidence filtering.

## Invariants (As Implemented Today)
- If no input file, no products, missing vendor_mappings, or no valid vendor_category_id remain after filtering, the job writes an empty JSON object to the main output and exits early.
- The oneVendor_to_onePim output only includes records with exactly one pim_match and non-empty assignment_confidence not equal to "mixed" or "null".

## Failure Modes and Observability
- Failure conditions (as coded): getResolvedOptions argument parsing errors; S3 head/list/put errors; Spark read failures beyond the multiLine fallback; unexpected exceptions during processing.
- Logging/metrics (as coded): Glue logger info/warn/error messages and print-based DEBUG statements for argument values, schema, record counts, and key steps.
- Run receipt: TBD
- Operator checks (S3 artifacts to verify): Verify presence of ${prepared_output_prefix}/${vendor_name}_categoryMatchingProposals.json and ${prepared_output_prefix}/${vendor_name}_categoryMatchingProposals_oneVendor_to_onePim_match.json in ${OUTPUT_BUCKET}.

## Related Artifacts and References
- job_manifest: jobs/vendor_input_processing/matching_proposals/job_manifest.yaml
- artifacts_catalog entries: TBD
- upstream jobs: TBD
- downstream jobs: TBD

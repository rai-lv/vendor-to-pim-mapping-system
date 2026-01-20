# Pipeline Inventory

## Scope and evidence
This inventory documents pipeline jobs using job manifests as the source of truth for interfaces, with business purpose summaries from approved business descriptions or script cards when available.

## Jobs
| job_id | job_dir | glue_job_name | runtime | business_purpose | parameters | inputs | outputs | side_effects | upstream_job_ids | downstream_job_ids | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| matching_proposals | jobs/vendor_input_processing/matching_proposals/ | TBD | pyspark | Aggregates the product-level forMapping_products feed into vendor-category mapping proposal JSON outputs for review. | JOB_NAME, INPUT_BUCKET, OUTPUT_BUCKET, vendor_name, prepared_input_key, prepared_output_prefix | TBD | TBD | deletes_inputs=TBD; overwrites_outputs=TBD | TBD | TBD | active |

## Dependency links

## Open verification items
* [TBD-inputs] Identify artifact_ids for matching_proposals inputs in docs/artifacts_catalog.md.
* [TBD-outputs] Identify artifact_ids for matching_proposals outputs in docs/artifacts_catalog.md.
* [TBD-side-effects] Confirm deletes_inputs/overwrites_outputs values for matching_proposals.
* [TBD-wiring] Identify upstream/downstream job_ids for matching_proposals.
* [TBD-artifact-catalog] Create artifact_ids for matching_proposals inputs/outputs in docs/artifacts_catalog.md.

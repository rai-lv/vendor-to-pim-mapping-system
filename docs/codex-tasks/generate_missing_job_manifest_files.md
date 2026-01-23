TITLE:
Generate or refresh job_manifest.yaml for all jobs from glue_script.py (spec + validator compliant)

BRANCH NAME:
docs/job-manifests-sync-from-scripts

GOAL:
For every job folder under jobs/<job_group>/<job_id>/ that contains glue_script.py:
- Ensure jobs/<job_group>/<job_id>/job_manifest.yaml exists
- Ensure each manifest complies with docs/standards/job_manifest_spec.md (v1.0)
- Ensure validator passes: python tools/validate_repo_docs.py --manifests

SCOPE (DO NOT EXPAND):
- Only create/update job manifests.
- Do not edit glue_script.py.
- Do not edit validator or spec documents.
- Do not create any new tooling scripts.

ALLOWED CHANGES (ONLY):
- jobs/*/*/job_manifest.yaml (create or edit)

REFERENCE DOCS (MUST FOLLOW):
- docs/standards/job_manifest_spec.md
- tools/validate_repo_docs.py

NON-NEGOTIABLE RULES:
1) Evidence-based only. Never guess values.
2) Minimize TBD. Use TBD only when the script/deployment evidence in-repo is insufficient.
3) Placeholder style in manifests MUST be ${NAME}. Do not use <name> or {name}.
4) If any field anywhere equals TBD, notes MUST exist and MUST include:
   - a line containing TBD_EXPLANATIONS
   - one explanation line per TBD field path exactly as the validator will detect it (e.g., logging_and_receipt.counters_observed or inputs[2].required).
5) job_id in the manifest MUST exactly match the folder name jobs/<job_group>/<job_id>/.
6) Do not partially guess lists. If list content is unknown, set the whole list key to the scalar string TBD (per spec).

DETERMINISTIC DERIVATION RULES (USE THESE):
A) job_id
- Set job_id to the folder name (<job_id>).

B) entrypoint
- Set entrypoint: glue_script.py (recommended by spec).

C) glue_job_name
- If the script parses/uses the standard Glue arg JOB_NAME (common via getResolvedOptions with "JOB_NAME"):
  set glue_job_name: ${JOB_NAME}
- Otherwise set glue_job_name: TBD and explain in notes (why not derivable from repo evidence).

D) runtime (spec enum)
- If glue_script.py imports/uses Spark/Glue Spark constructs (examples: pyspark, SparkContext, SparkSession, awsglue.context.GlueContext, DynamicFrame):
  set runtime: pyspark
- Else if it is a Glue Python Shell style script (no Spark/GlueContext usage; typical boto3-driven processing):
  set runtime: python_shell
- If truly ambiguous from the script (rare), runtime: TBD with notes explanation.

E) parameters
- Extract parameter names from argument parsing in the script:
  - getResolvedOptions(args, [...]) lists
  - argparse add_argument definitions
  - any explicit sys.argv parsing patterns
- Output parameters as a YAML list of strings (names only), OR parameters: [] if provably none.
- If parameter list cannot be confidently enumerated from the script, set parameters: TBD with notes.

F) inputs / outputs (avoid TBD lists unless truly impossible)
- Enumerate S3 reads/writes performed by the script as inputs/outputs items:
  - boto3 get_object / download_file / list_objects used for reading inputs
  - boto3 put_object / upload_file used for writing outputs
  - Spark read/write paths (s3://bucket/key...) where present
- Convert every S3 path to:
  - bucket: <literal bucket name> OR ${INPUT_BUCKET}/${OUTPUT_BUCKET}/etc if variable-driven
  - key_pattern: stable key or prefix pattern WITHOUT s3://
- Do not hardcode concrete timestamps/vendor values. Use placeholders (${vendor_name}, ${timestamp}, ${run_id}, etc) if the script composes keys from variables/args.
- format:
  - Derive from file extension or writer/reader used:
    .json -> json or ndjson (use ndjson when the script clearly writes newline-delimited records / one JSON per line)
    .csv -> csv
    .xml -> xml
    .zip -> zip
    else -> other
  - If format is not derivable, set that item’s format: TBD and add a notes explanation for the exact path (e.g., inputs[1].format).
- required (true/false/TBD):
  - true if the script fast-fails on missing input (explicit existence checks that raise/exit)
  - false if optional (script branches if missing / try/except / “if exists then …”)
  - TBD only if requiredness cannot be derived; then add notes for the exact path (e.g., outputs[2].required)

G) config_files (optional block)
- If the script reads a stable config from S3 (commonly under configuration-files/...), add a config_files entry.
- If there is a mirrored repo config file under the job folder (jobs/<...>/<...>/configs/...), set repo_path accordingly.
- If repo_path is unknown/not maintained, omit repo_path (it is optional). Do NOT add repo_path: TBD unless the script indicates a repo copy should exist.

H) side_effects
- deletes_inputs:
  - true only if the script calls delete_object/delete_objects on input keys
  - otherwise false (if no deletion code exists)
  - TBD only if deletion behavior cannot be determined from the script
- overwrites_outputs:
  - true if outputs are written to fixed keys/prefixes (boto3 put_object to a stable key overwrites if present; Spark mode overwrite likewise)
  - false if outputs are always written to unique keys per run (e.g., includes ${run_id} or ${timestamp} in file name)
  - TBD only if not derivable from the script; explain in notes

I) logging_and_receipt
- writes_run_receipt:
  - true if the script writes an explicit run receipt/status JSON artifact to S3 (e.g., key includes run_receipt_... or a structured receipt object is persisted)
  - false if no such artifact write exists
  - TBD only if ambiguous; explain
- If writes_run_receipt is true:
  - run_receipt_bucket and run_receipt_key_pattern MUST be populated (not TBD), derived from the script’s S3 write target
- counters_observed:
  - If the script writes a receipt with a stable counters structure, list counter names as strings (prefer dotted paths like counts.step2_full.vendor_category_count when the structure is explicit).
  - If not derivable, set counters_observed: TBD and explain in notes.

WORK PLAN:
1) Discover all job folders:
   - Find directories matching jobs/*/*/ that contain glue_script.py.
2) For each job folder:
   - If job_manifest.yaml is missing: create it from scratch following the minimal template in the spec.
   - If job_manifest.yaml exists: update it to be spec-compliant and validator-compliant, minimizing TBD by extracting more evidence from glue_script.py.
3) Run validation:
   - python tools/validate_repo_docs.py --manifests
   - Fix any failures until SUMMARY shows fail=0.
4) Output the PR with only the allowed file changes.

ACCEPTANCE CRITERIA (MUST ALL PASS):
- Every jobs/*/*/ directory with glue_script.py has jobs/*/*/job_manifest.yaml.
- All manifests include required top-level keys:
  job_id, glue_job_name, runtime, parameters, inputs, outputs, side_effects, logging_and_receipt
- No invalid placeholders:
  - No <...> placeholders
  - No {name} placeholders (only ${NAME})
  - No s3:// in bucket/key_pattern
- If any TBD exists in any manifest:
  - notes exists (list)
  - includes a line containing TBD_EXPLANATIONS
  - includes one line mentioning each exact TBD field path detected by validator
- python tools/validate_repo_docs.py --manifests returns SUMMARY ... fail=0

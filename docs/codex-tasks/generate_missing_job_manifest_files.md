TITLE: Generate missing job_manifest.yaml files from glue_script.py (evidence-based)

BRANCH NAME:
docs/manifests-generate-missing

SCOPE (WHAT THIS PR IS ALLOWED TO CHANGE):
- Create NEW files only: jobs/*/*/job_manifest.yaml  (ONLY where the file is currently missing)
- Do NOT modify any existing job_manifest.yaml
- Do NOT modify any other files or folders

CONTEXT / SPECS (MUST FOLLOW):
- docs/standards/job_manifest_spec.md  (schema, enums, TBD + notes rules, placeholder rules)
- jobs/<job_group>/<job_id>/glue_script.py  (primary evidence source for each manifest)

OBJECTIVE:
For every job folder under jobs/<job_group>/<job_id>/ that contains glue_script.py but does NOT contain job_manifest.yaml, create a compliant job_manifest.yaml based strictly on evidence in that glue_script.py, following docs/standards/job_manifest_spec.md. No guessing. Unknowns must be represented as TBD (using the spec’s rules) with explicit notes.

DETAILED INSTRUCTIONS (DO EXACTLY):

1) Discover target jobs
   - Find all glue scripts: jobs/*/*/glue_script.py
   - For each job folder (jobs/<job_group>/<job_id>/):
     - If jobs/<job_group>/<job_id>/job_manifest.yaml already exists -> SKIP (no changes)
     - Else -> CREATE jobs/<job_group>/<job_id>/job_manifest.yaml

2) For each missing manifest, write YAML using EXACT top-level keys (per spec)
   Required keys:
   - job_id
   - glue_job_name
   - runtime
   - parameters
   - inputs
   - outputs
   - side_effects
   - logging_and_receipt
   Optional/recommended:
   - entrypoint (recommended by spec; use glue_script.py)

   Always include:
   - entrypoint: glue_script.py

3) Field-by-field evidence rules (NO GUESSING)

   3.1 job_id
   - MUST equal the folder name <job_id> exactly.

   3.2 glue_job_name
   - Set to a concrete string ONLY if the deployed Glue job name is explicitly present in-repo evidence inside glue_script.py (rare).
   - Otherwise: glue_job_name: TBD
   - If TBD is used anywhere in the manifest, notes MUST exist and explain it.

   3.3 runtime (enum: pyspark|python_shell|python|nodejs|other|TBD)
   - Set runtime: pyspark ONLY if the script contains clear Spark evidence, e.g.:
     - imports pyspark (e.g., “from pyspark…”), OR
     - uses SparkContext/GlueContext/SparkSession in code
   - Otherwise: runtime: TBD
   - Do NOT infer python_shell vs python; if not provable from code, keep TBD and explain in notes.

   3.4 parameters (list(string) OR scalar "TBD")
   - Extract parameter NAMES ONLY (never values).
   - If script uses awsglue.utils.getResolvedOptions(sys.argv, [...]):
     - parameters MUST be that exact list of strings as found in the code.
   - Else if script uses argparse (add_argument):
     - parameters MUST be the set of argument dest/names that can be proven from the script.
   - If no argument parsing can be proven:
     - parameters: TBD
   - Only use parameters: [] if it is provable that the job takes no parameters (strong evidence required).

   3.5 inputs and outputs (each is: list(items) OR scalar "TBD")
   IMPORTANT SPEC RULE:
   - If list content is unknown, the entire key value MUST be the scalar string "TBD" (no partial lists).

   Only write explicit inputs/outputs lists if BOTH conditions are met:
   (A) all S3 reads/writes can be enumerated from the script without ambiguity, AND
   (B) stable bucket + key_pattern can be expressed without embedding run-specific concrete values.

   If either (A) or (B) fails:
   - inputs: TBD and/or outputs: TBD (as needed)

   When inputs/outputs lists ARE created:
   - Each item MUST have exactly these fields:
     - bucket: <string or TBD>   (no s3://)
     - key_pattern: <string or TBD>  (no s3://)
     - format: one of json|ndjson|csv|xml|zip|other|TBD
     - required: true|false|TBD

   Placeholders:
   - Use ONLY ${NAME} placeholder style in bucket/key_pattern.
   - Convert any <vendor> or {vendor} style seen in prose/comments into ${vendor} or ${VENDOR} (choose placeholder names based on parameter names found in the script when possible).
   - Do NOT embed concrete timestamps, concrete vendor names, or concrete run ids.

   Format:
   - Use format based on provable evidence in code (file extension, parser usage).
   - If not provable: format: TBD

   required flag:
   - If the script clearly fails/raises when missing -> required: true
   - If the script treats missing as optional -> required: false
   - If unclear -> required: TBD

   3.6 config_files (optional)
   - Only include config_files if the script clearly reads a static config artifact (e.g., config JSON/YAML from S3).
   - Each config_files item schema:
     - bucket, key_pattern, format (json|yaml|other|TBD), required (true|false|TBD), optional repo_path
   - If no clear evidence exists, omit config_files entirely (do not add empty list).

   3.7 side_effects
   Must be:
   side_effects:
     deletes_inputs: true|false|TBD
     overwrites_outputs: true|false|TBD

   Evidence rules:
   - deletes_inputs:
     - true ONLY if explicit deletion behavior exists in the script (e.g., S3 delete_object/delete_objects or equivalent).
     - else false (no deletion observed in script).
   - overwrites_outputs:
     - true ONLY if explicit overwrite behavior exists (e.g., Spark write mode overwrite, or explicit delete-then-write to same key).
     - else TBD (do not guess).

   3.8 logging_and_receipt
   Must be:
   logging_and_receipt:
     writes_run_receipt: true|false|TBD
     run_receipt_bucket: <string or TBD>
     run_receipt_key_pattern: <string or TBD>
     counters_observed: <list(string) OR "TBD">

   Evidence rules:
   - If script explicitly writes a run receipt/status artifact to S3:
     - writes_run_receipt: true
     - run_receipt_bucket and run_receipt_key_pattern MUST be concrete (not TBD)
   - If not provable:
     - writes_run_receipt: TBD
     - run_receipt_bucket: TBD
     - run_receipt_key_pattern: TBD
   - counters_observed:
     - list names ONLY if the script explicitly defines/emits counters with stable names (e.g., a dict written in receipt, or clearly named metrics).
     - Otherwise: TBD
     - Only use [] if provably no counters exist (rare).

4) notes handling (MANDATORY when any TBD exists)
   - If any value anywhere in the manifest is TBD, add:
     notes:
       - "TBD_EXPLANATIONS:"
       - "<field_path>: TBD — <why unknown>, <what evidence was checked (file + brief reference)>."

   Field paths must match the manifest structure, e.g.:
   - glue_job_name
   - runtime
   - parameters
   - inputs
   - outputs
   - side_effects.overwrites_outputs
   - logging_and_receipt.writes_run_receipt
   etc.

   One explicit explanation line MUST exist for each TBD field path.

5) Validate locally (must pass)
   - Run:
     python tools/validate_repo_docs.py --manifests
   - Fix any failures until validation passes.

6) Commit
   - Commit message:
     "Add missing job manifests (evidence-based)"

ACCEPTANCE CRITERIA (MUST ALL BE TRUE):
- For every folder matching jobs/*/*/glue_script.py that lacked job_manifest.yaml, a new jobs/*/*/job_manifest.yaml now exists.
- No existing job_manifest.yaml was modified.
- Every new manifest is compliant with docs/standards/job_manifest_spec.md:
  - required top-level keys present
  - job_id matches folder name
  - enums valid
  - placeholder style uses only ${NAME} (no <...> and no {...})
  - if any TBD exists -> notes exists and includes one explanation per TBD field path
- python tools/validate_repo_docs.py --manifests exits successfully (no FAIL lines; exit code 0).

OUT OF SCOPE (MUST NOT DO):
- Do NOT create or modify any repo tooling, workflows, or validator code.
- Do NOT update docs/artifacts_catalog.md or docs/job_inventory.md in this PR.
- Do NOT invent or infer S3 bucket/prefix patterns from business descriptions; manifests must be evidence-based from glue_script.py (and only set stable patterns when provable).

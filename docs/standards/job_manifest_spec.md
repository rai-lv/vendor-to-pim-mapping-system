# Job Manifest Specification (v1.0)

UPD 2026-01-28 14:20
**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema and semantics for machine-readable job interface manifests.
**Why necessary:** Enables consistent invocation and automation across jobs.
**Must contain:** Required/optional fields; semantic meaning; placeholder rules; compatibility/breaking-change rules.
**Must not contain:** Per-job content or embedded authoritative examples.

## 0) Purpose and scope

`jobs/<job_group>/<job_id>/job_manifest.yaml` is the **machine-readable interface contract** for one job.

This spec defines:
- where the manifest lives and how it is named
- the required schema (keys, types, enums)
- deterministic rules for unknowns (`TBD`) and evidence notes
- stability rules so automations can extract data reliably (e.g., for `docs/job_inventory.md`)

Out of scope:
- business meaning and rationale (belongs to `docs/business_job_descriptions/<job_id>.md`)
- code-level implementation details (belongs to `glue_script.py` and script cards)

---

## 1) Definition and alignment within this system

### 1.1 What a job manifest represents

A job manifest is the **source of truth for automation-relevant interface facts** about a job:
- parameters
- S3 inputs (required/optional)
- S3 outputs (required/optional)
- side effects (delete/overwrite)
- run receipt behavior and counters (if present)

Manifests MUST be **evidence-based** (derived from the script and/or declared deployment configuration). No guessing.

### 1.2 Primary consumer alignment

The manifest schema is aligned to `docs/standards/job_inventory_spec.md` in that `job_inventory` automation expects these manifest keys to exist and be stable:
- `glue_job_name`
- `runtime`
- `parameters`
- `inputs[]`
- `outputs[]`
- `side_effects.*`
- `logging_and_receipt.*`

---

## 2) Location and naming convention

### 2.1 Required location per job folder

For each job folder:
- `jobs/<job_group>/<job_id>/glue_script.py`
- `jobs/<job_group>/<job_id>/job_manifest.yaml`

### 2.2 Naming consistency rules

**Rule 1: job_id matches folder name**
- The canonical `job_id` is the folder name: `jobs/<job_group>/<job_id>/`
- The manifest MUST contain `job_id` key whose value matches `<job_id>` exactly
- If `job_id ≠ folder name`, this is a spec violation

**Rule 2: glue_job_name matches job_id**
- The deployed Glue job name MUST equal the `job_id` (and therefore the folder name)
- The manifest MUST contain `glue_job_name` key whose value matches `job_id` exactly
- Example: folder `preprocessIncomingBmecat` → `glue_job_name: preprocessIncomingBmecat`
- If `glue_job_name ≠ job_id`, this is a spec violation

**Verification:**
Verification tools SHOULD check both consistency rules (folder = job_id = glue_job_name).

**Rationale:**
This 1:1:1 mapping ensures:
- No ambiguity about deployed job identity
- Traceability from repo structure to AWS Glue console
- Simplified automation (no separate deployment name lookup needed)

**Deployment note:**
If deployments use environment-specific naming (e.g., `prod-{job_id}`), that is a deployment-time transform. The manifest documents the canonical identity; deployment scripts apply environment prefixes as needed.

---

## 3) Design principles

1. **Deterministic extraction:** automations must not interpret prose or infer behavior.
2. **Stable patterns:** use placeholders for run-specific values; do not hardcode concrete timestamps/vendor identifiers in patterns.
3. **Uniform field names:** all S3 locations use the same pair of fields: `bucket` + `key_pattern`.
4. **Explain unknowns:** if anything is `TBD`, the reason must be documented in `notes`.

---

## 4) Schema overview

Top-level keys and whether they are required:

| Key | Required | Type | Purpose |
|---|---:|---|---|
| `job_id` | yes | string | Identifier for this job (must match folder `<job_id>`) |
| `glue_job_name` | yes | string | Deployed Glue job name (MUST equal `job_id`) |
| `runtime` | yes | enum | Execution runtime type |
| `entrypoint` | recommended | string | Entry file name inside job folder (commonly `glue_script.py`) |
| `parameters` | yes | list(string) or `TBD` | Parameter names only (no values) |
| `inputs` | yes | list(input_item) or `TBD` | Declared required/optional input artifacts |
| `outputs` | yes | list(output_item) or `TBD` | Declared required/optional output artifacts |
| `config_files` | optional | list(config_item) | Static config artifacts used by job |
| `side_effects` | yes | object | Delete/overwrite behaviors |
| `logging_and_receipt` | yes | object | Run receipt behavior and observed counters |
| `notes` | required if any `TBD` exists | list(string) | Evidence notes and `TBD` explanations |

---

## 5) Normative definitions (MUST)

### 5.1 Allowed unknown marker

- `TBD` is the only allowed unknown marker for scalar fields.
- For lists:
  - `[]` means **provably empty**.
  - Missing key means **schema violation** (unless explicitly marked as optional in this spec).
  - If list content is unknown, the entire key value MUST be `TBD` (not a partially guessed list).
- For list-typed keys (`parameters`, `inputs`, `outputs`, `counters_observed`), unknown MUST be represented as the scalar string `TBD` (not `[TBD]`, not omitted).

### 5.2 `runtime` enum

`runtime` MUST be one of:
- `pyspark`
- `python_shell`
- `python`
- `nodejs`
- `other`
- `TBD`

#### 5.2.1 Derivation guidance for new jobs

When creating a new manifest:
- `pyspark`: Use when the job runs PySpark code (typically uses `glueContext`, `spark`, or `SparkSession` and processes data via Spark DataFrames/RDDs).
- `python_shell`: Use when the job is a Glue Python Shell job (job type configured as `pythonshell` in AWS Glue, limited to Python libraries without Spark context).
- `python`: Use for standalone Python scripts that do not run in Glue context (e.g., containerized or Lambda-based).
- `nodejs`: Use for Node.js-based jobs.
- `other`: Use for jobs in other runtimes (e.g., Java, Scala, or shell scripts).
- `TBD`: Use only when evidence is insufficient to classify the runtime. In this case, explain in `notes` what evidence is missing (e.g., "No deployment config found; script uses both Python and Spark patterns without clear context").

### 5.3 `parameters`

`parameters` MUST be:
- a list of strings (parameter names only), OR
- `TBD`

Rules:
- If the job is proven to have no parameters: `parameters: []`
- Parameter values MUST NOT appear in the manifest.

### 5.4 `inputs[]` and `outputs[]`

`inputs` and `outputs` MUST be:
- a list of items in the schemas below, OR
- `TBD`

#### 5.4.0.1 Format semantics and decision rules (MUST)

This repo distinguishes:

- `ndjson`: newline-delimited JSON (one JSON object per line). This is the default JSON layout for Spark/Glue I/O.
- `json`: a single JSON document (one object or one array) stored in one file/key.

Decision rules (MUST):

1) If the job uses Spark/Glue JSON writing via any of the following patterns, `format` MUST be `ndjson`:
   - `DataFrameWriter.json(...)` / `.write.json(...)`
   - `Dataset.toJSON()` followed by `saveAsTextFile(...)`
   - any Spark write that produces partition/part files where each record is a JSON line
   Rationale: Spark writes JSON as JSON Lines / newline-delimited JSON by default. :contentReference[oaicite:1]{index=1}

2) If the job reads JSON via Spark/Glue `read.json(...)` without `multiLine=true`, the expected input `format` MUST be `ndjson`
   Rationale: Spark reads JSON Lines by default; multiline JSON is an explicit opt-in. :contentReference[oaicite:2]{index=2}

3) `format: json` is only allowed if there is evidence that the artifact is a single JSON document written as one unit
   (e.g., `json.dump/json.dumps` to a single file/key, or `multiLine=true` semantics are explicitly used).

4) If the script does not provide enough evidence to classify `json` vs `ndjson`, `format` MUST be `TBD` (do not guess),
   and the `notes` section MUST explain what evidence is missing.

#### 5.4.0.2 Handling other runtimes (Python, Node.js, etc.)

For non-Spark runtimes (e.g., `python`, `nodejs`, `other`), apply similar format classification principles:

**Python (non-Spark) examples:**
- If the job uses Pandas `DataFrame.to_json(..., orient='records', lines=True)`, `format` MUST be `ndjson`.
- If the job uses Pandas `DataFrame.to_json(..., orient='records', lines=False)` or `json.dump/json.dumps`, `format` MUST be `json`.
- If the job uses Pandas `DataFrame.to_csv(...)`, `format` MUST be `csv`.

**Node.js examples:**
- If the job writes using `fs.writeFileSync(path, JSON.stringify(obj))`, `format` MUST be `json`.
- If the job writes line-by-line JSON using streams or libraries like `ndjson`, `format` MUST be `ndjson`.

**General rule:**
- Determine `format` based on the actual library calls and I/O patterns in the code.
- If ambiguous, set `format` to `TBD` and explain in `notes`.

Ordering rule:
- List order MUST be stable and meaningful (do not reorder between updates unless the interface truly changed).
- Automations (e.g., job inventory) preserve this order.

#### 5.4.1 `input_item` schema

Each `inputs[]` item MUST be an object with:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `bucket` | yes | string or `TBD` | Bucket name or placeholder (without `s3://`) |
| `key_pattern` | yes | string or `TBD` | Key or prefix pattern (no `s3://`) |
| `format` | yes | enum | Data format |
| `required` | yes | `true`/`false`/`TBD` | Whether absence causes job failure |

`format` enum for inputs/outputs MUST be one of:
- `json`
- `ndjson`
- `csv`
- `xml`
- `zip`
- `other`
- `TBD`

#### 5.4.2 `output_item` schema

Same as `input_item`:
- `bucket`, `key_pattern`, `format`, `required`

### 5.5 `config_files[]` (optional)

Purpose:
- Declare static configs the job reads (often referenced by scripts and stored in S3).
- This block is optional because some repositories track configs only in S3 without mirroring.

Each `config_files[]` item MUST be an object with:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `bucket` | yes | string or `TBD` | Bucket name or placeholder |
| `key_pattern` | yes | string or `TBD` | Key/pattern to the config artifact |
| `format` | recommended | enum | `json|yaml|other|TBD` |
| `required` | yes | `true`/`false`/`TBD` | Whether job fails without it |
| `repo_path` | optional | string or `TBD` | Path to optional repo-mirrored config (if maintained) |

Allowed `format` enum for `config_files[]`:
- `json`
- `yaml`
- `other`
- `TBD`

#### 5.5.1 Deprecation rule (uniform S3 fields)

To keep parsing uniform:
- New manifests MUST use `bucket` + `key_pattern` everywhere.
- Legacy keys `s3_bucket` / `s3_key_pattern` MUST NOT be used in new manifests.
- **Migration from legacy fields:** If older manifests use `s3_key_pattern` or `s3_bucket`, replace them with `key_pattern` and `bucket` respectively. This ensures consistency across all S3 references and simplifies automation parsing.

#### 5.5.2 Handling repo_path (automation rule)

The `repo_path` field indicates whether a config file is mirrored in the repository.

**Determination rules:**
1. Search repository for file matching the S3 key pattern under:
   - `jobs/<job_id>/config/`
   - `jobs/<job_id>/`
   - `config/` (repo root)
2. **IF file found:** `repo_path: <relative_path_from_repo_root>`
3. **ELIF file not found (confirmed S3-only):** `repo_path: null`
4. **ELSE (cannot determine):** `repo_path: TBD` with explanation in `notes`

**Example (S3-only config):**
```yaml
config_files:
  - bucket: ${INPUT_BUCKET}
    key_pattern: configuration-files/job_config_${vendor_name}.json
    format: json
    required: true
    repo_path: null  # Verified: not in jobs/*/config/ or config/ directories
```

**Note on TBD vs null:**
- Use `null` when you have confirmed the file is NOT in the repository (S3-only)
- Use `TBD` only when you haven't checked yet or cannot determine the location

### 5.6 `side_effects`

`side_effects` MUST be an object with:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `deletes_inputs` | yes | `true`/`false`/`TBD` | Job deletes input objects after processing |
| `overwrites_outputs` | yes | `true`/`false`/`TBD` | Job overwrites existing outputs |

### 5.7 `logging_and_receipt`

`logging_and_receipt` MUST be an object with:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `writes_run_receipt` | yes | `true`/`false`/`TBD` | Whether a run receipt/status artifact is written |
| `run_receipt_bucket` | yes | string or `null` or `TBD` | Bucket/pattern for run receipt (if written) |
| `run_receipt_key_pattern` | yes | string or `null` or `TBD` | Key pattern for run receipt (if written) |
| `counters_observed` | yes | list(string) or `[]` or `TBD` | Names of counters emitted/recorded |

**Rules (for automation and manual authoring):**

**If `writes_run_receipt` is `true`:**
- Both `run_receipt_bucket` and `run_receipt_key_pattern` MUST be concrete strings (not `TBD` or `null`)
- Values MUST be derivable from code (e.g., S3 put_object calls)
- If code writes receipt but pattern cannot be determined, use `TBD` with explanation in `notes`

**If `writes_run_receipt` is `false`:**
- Set `run_receipt_bucket: null`
- Set `run_receipt_key_pattern: null`
- Do NOT use `TBD` - the value is known to be "not applicable", not "unknown"
- No explanation required in `notes` for these null values

**If `writes_run_receipt` is `TBD`:**
- Set `run_receipt_bucket: TBD`
- Set `run_receipt_key_pattern: TBD`
- Explanation in `notes` MUST state why receipt-writing behavior cannot be determined from code

#### 5.7.1 Determining counters_observed

The `counters_observed` field lists names of structured metrics/counters emitted by the job.

**Determination rules:**

**Step 1: Check if run receipt is written**
- IF `writes_run_receipt` is `true` AND receipt structure contains a "counts" dictionary:
  - `counters_observed: [list of keys from counts dict]`
- ELIF receipt exists but has no counts:
  - `counters_observed: []`

**Step 2: Check for CloudWatch metrics**
- IF script contains boto3 `cloudwatch.put_metric_data()` calls:
  - Extract metric names from `MetricName` parameters
  - `counters_observed: [list of metric names]`

**Step 3: Default for no structured counters**
- IF no structured counters found in steps 1-2:
  - `counters_observed: []` (NOT `TBD` - this represents proven absence)

**Use `TBD` ONLY if:**
- Receipt structure is dynamically constructed and cannot be parsed statically
- Metrics are computed from external config files not available during manifest generation
- In these cases, explain in `notes` which dynamic construction prevents static analysis

**Example (no receipt, no counters):**
```yaml
logging_and_receipt:
  writes_run_receipt: false
  run_receipt_bucket: null
  run_receipt_key_pattern: null
  counters_observed: []  # No CloudWatch metrics, no receipt file (verified script analysis)
```

**Example (receipt with counters):**
```yaml
logging_and_receipt:
  writes_run_receipt: true
  run_receipt_bucket: ${OUTPUT_BUCKET}
  run_receipt_key_pattern: ${output_prefix}run_receipts/receipt_${run_id}.json
  counters_observed: 
    - products_processed
    - categories_mapped
    - errors_encountered
```

### 5.8 `notes`

`notes` is REQUIRED if any `TBD` appears anywhere in the manifest.

Minimum requirement if present:
- Provide at least one explicit explanation line for each `TBD` field.
- Explanations MUST state:
  1. **Why** the value is unknown (e.g., "deployment config not found", "script does not demonstrate this behavior")
  2. **What evidence source was checked** (e.g., "inspected glue_script.py lines 50-100", "reviewed AWS Glue console job definition")
  3. **What action is needed** to resolve the TBD (e.g., "need to confirm with team lead", "requires actual deployment config file", "needs testing in staging environment")
- Avoid vague explanations like "unknown" or "needs investigation" without specifics.

Recommended pattern:
- Include a single line marker like `TBD_EXPLANATIONS:` and then list each field explanation.
- Example: `"side_effects.overwrites_outputs: TBD — Script does not show explicit overwrite logic (checked lines 120-150 in glue_script.py). Need to test job in staging to observe actual behavior."`

---

## 6) Placeholder and pattern rules (MUST)

### 6.1 Allowed placeholder style

Canonical placeholder style is `${NAME}`.
Note: Other documents (e.g., business descriptions) may show placeholders as <vendor> or {vendor} for readability. In job_manifest.yaml, the canonical placeholder style MUST be ${NAME}.

#### 6.1.1 Placeholder types and naming

**Type 1: Job parameter placeholders**
- Represent values from the `parameters` list
- Naming: MUST match the parameter name exactly (case-sensitive, character-for-character)
- NO case transformation is applied; placeholder name = parameter name
- Examples: 
  - Parameter `INPUT_BUCKET` → placeholder `${INPUT_BUCKET}`
  - Parameter `vendor_name` → placeholder `${vendor_name}`
  - Parameter `bmecat_input_key` → placeholder `${bmecat_input_key}`

**Type 2: Runtime-generated placeholders**
- Represent values computed at runtime (not in `parameters` list)
- Naming convention: SHOULD use snake_case (lowercase with underscores)
- Examples: `${run_id}`, `${timestamp}`, `${new_suffix}`
- Documentation: MUST be explained in `notes` section (what they represent, how generated)

**General rules:**
- Placeholder names are case-sensitive
- Placeholders MUST NOT contain spaces
- For parameter placeholders: use exact match to parameter name (no case conversion)

### 6.2 Stability requirement

- `bucket` and `key_pattern` MUST be stable patterns.
- Concrete run-specific values (e.g., a specific timestamp string) MUST NOT be embedded directly.
- If a stable pattern cannot be stated, the field must be `TBD` with an explanation in `notes`.

### 6.3 No `s3://` prefixes

- `bucket` MUST NOT include `s3://`.
- `key_pattern` MUST NOT include `s3://`.

### 6.4 Normalized prefix placeholders (MUST)

Problem:
Some Glue scripts accept a prefix parameter that may or may not end with `/`, and then normalize it internally
(e.g., via `ensure_prefix_uri(...)` or equivalent). If a manifest uses `${prefix}${vendor_name}_...` without
making the normalization explicit, any automation that substitutes the raw parameter value can generate wrong keys.

Rule (MUST):
If the script normalizes a prefix-like parameter `X` (example: `preprocessed_input_key`, `bmecat_output_prefix`,
`prepared_output_prefix`, `prepared_input_key`), then the manifest MUST use the normalized placeholder form
`${X_norm}` inside `key_pattern`.

Definition (MUST):
`${X_norm}` means: “the value of parameter `X` after normalization to an S3 *prefix* with exactly one trailing `/`”.
This is a manifest-level convention; `${X_norm}` does not need to appear in `parameters`.


When this rule applies:
- Use `${X_norm}` only when the script contains evidence of prefix normalization logic (e.g., code that ensures trailing `/`).
- If no normalization is evident, use the raw placeholder (e.g., `${Preprocessed_input_key}`) or set to `TBD` if ambiguous.

Examples (MUST):
- Correct:
  - `${Preprocessed_input_key_norm}${Vendor_name}_vendor_products.json`
  - `${Bmecat_output_prefix_norm}${Vendor_name}_vendor_products.json`
- Not allowed (ambiguous when caller passes a prefix without `/`):
  - `${Preprocessed_input_key}${Vendor_name}_vendor_products.json`
  - `${Bmecat_output_prefix}${Vendor_name}_vendor_products.json`

Notes:
- If a job does NOT normalize the prefix in code, then either:
  a) update the code to normalize (preferred), OR
  b) set `key_pattern` to `TBD` and explain missing evidence in `notes` (do not guess).

---

## 7) Sourcing rules (MUST; to keep manifests evidence-based)

For each field, the manifest should reflect the best available evidence:

- `runtime`: derived from the script/job type (e.g., Glue Python Shell vs Spark).
- `parameters`: derived from script argument parsing and/or job configuration.
- `inputs/outputs`: derived from actual S3 reads/writes performed (including config-driven patterns if stable).
- `side_effects`: derived from script behavior (explicit delete/overwrite) and/or job design conventions if explicitly implemented.
- `logging_and_receipt`: derived from actual run receipt writing; counters derived from logged/emitted metrics.

If the script does not provide evidence for a field, set it to `TBD` and explain in `notes`.

This manifest spec applies only to AWS Glue jobs represented by the `jobs/<job_group>/<job_id>/glue_script.py` convention; for this scope, `glue_job_name` is required and non-Glue jobs must not use `job_manifest.yaml` under this convention.

---

## 8) Alignment rules with other documents (informational)

- `docs/job_inventory.md` is compiled from manifests and artifact catalog links; it must not invent interface facts.
- Business descriptions remain the place for intent/context; manifests remain the place for interface facts.

### 8.1 Integration and review process with related documents

To ensure consistency across documentation:

**1. Cross-validation with job inventory:**
- After creating or updating a manifest, verify that the job appears correctly in `docs/job_inventory.md`.
- Check that key fields (`runtime`, `parameters`, `inputs`, `outputs`) are consistently represented.
- If automation has not yet updated the inventory, manually verify the manifest will generate correct inventory entries.

**2. Alignment with business job descriptions:**
- Each manifest should have a corresponding business description at `docs/business_job_descriptions/<job_id>.md`.
- Review the business description to ensure:
  - The manifest's `inputs` and `outputs` match the business flow described.
  - Parameter names referenced in business descriptions align with the manifest's `parameters` list.
  - Any constraints or side effects mentioned in business descriptions are reflected in the manifest.
- If discrepancies exist, update the business description or manifest (or both) to restore consistency.

**3. Verification process:**
- When completing a new manifest, perform a three-way check:
  1. Manifest fields are derived from `glue_script.py` (evidence-based).
  2. Manifest aligns with `docs/job_inventory.md` (automation compatibility).
  3. Manifest aligns with `docs/business_job_descriptions/<job_id>.md` (business intent).
- Document any unresolved conflicts in the manifest's `notes` section.

---

## 9) Compliance checklist (PASS/FAIL)

A manifest is compliant if:

**Structure**
- file exists at `jobs/<job_group>/<job_id>/job_manifest.yaml`
- `job_id` exists and matches folder `<job_id>`
- `glue_job_name` exists and matches `job_id` (and folder name)
- required top-level keys exist: `job_id`, `glue_job_name`, `runtime`, `parameters`, `inputs`, `outputs`, `side_effects`, `logging_and_receipt`

**Types and enums**
- `runtime` is one of the allowed values (or `TBD`)
- `parameters` is a list of strings (or `TBD`)
- `inputs/outputs` are lists of objects with required fields (or `TBD`)
- `required` flags are `true|false|TBD`
- `format` values follow the allowed enums (or `TBD`)

**Optional fields validation**
- if `entrypoint` is present, it must be a valid filename (typically `glue_script.py` or other `.py` files within the job folder)
- if `config_files` is present, each item must have required fields: `bucket`, `key_pattern`, `required`

**Placeholder rules**
- parameter placeholders match parameter names exactly (case-sensitive)
- runtime placeholders use snake_case convention
- placeholders use `${NAME}` format (case-sensitive, no spaces)
- normalized prefix placeholders use `${X_norm}` when script contains normalization logic

**Uniform S3 fields**
- all S3 references use `bucket` + `key_pattern`
- legacy `s3_bucket/s3_key_pattern` are not used in new manifests

**TBD discipline**
- if any `TBD` appears anywhere, `notes` exists and contains explicit explanations for each TBD field
- each TBD explanation must state: why unknown, what evidence was checked, and what action is needed
- use `null` for "not applicable" (e.g., receipt bucket when no receipt written)
- use `[]` for "provably empty" (e.g., counters when none exist)

---

## 10) Minimal template

```yaml
job_id: <folder_job_id>
glue_job_name: <folder_job_id>  # MUST equal job_id
runtime: <pyspark|python_shell|python|nodejs|other|TBD>
entrypoint: glue_script.py

parameters:
  - <PARAM_NAME>
  - <PARAM_NAME>

inputs:
  - bucket: ${INPUT_BUCKET}
    key_pattern: ${Some_input_key}
    format: xml
    required: true

outputs:
  - bucket: ${OUTPUT_BUCKET}
    key_pattern: ${Output_prefix_norm}${Vendor_name}_something.ndjson
    format: ndjson
    required: true

config_files:
  - bucket: ${INPUT_BUCKET}
    key_pattern: configuration-files/..._${Vendor_name}.json
    format: json
    required: true
    repo_path: null  # or path if mirrored in repo

side_effects:
  deletes_inputs: false
  overwrites_outputs: true

logging_and_receipt:
  writes_run_receipt: false
  run_receipt_bucket: null
  run_receipt_key_pattern: null
  counters_observed: []

notes:
  - "Evidence source: Analyzed glue_script.py, checked parameters, I/O patterns, and side effects."
  - "Script does not write run receipt (verified via code analysis). No structured counters emitted."

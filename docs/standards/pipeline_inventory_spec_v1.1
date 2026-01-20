# Pipeline Inventory Specification (v1.1)

## 0) Purpose and scope

`docs/pipeline_inventory.md` is the authoritative **index** of pipeline jobs and their interfaces at the system level.

It must support:

* fast orientation (what jobs exist, what they consume/produce)
* safe AI-supported planning (Codex tasks can reference stable fields)
* incremental extension (new jobs added without rewriting old entries)

The inventory is a **compiled view**. It must not contain invented facts.

---

## 1) Source-of-truth rules (MUST)

For each job row:

1. **Interface fields** (parameters, inputs, outputs, side effects) MUST come from that job’s `job_manifest.yaml`.
2. **Artifact identifiers** for `inputs` and `outputs` MUST come from `docs/artifacts_catalog.md` by linking each manifest input/output to exactly one `artifact_id` (see linking rule below).
3. **Business role text** MAY come from a business description document if present; otherwise `TBD`.
   - If a business description exists, it MUST be taken from `docs/business_descriptions/<job_id>.md` (if present); otherwise `TBD`.
4. **Ordering (“step”)** MUST be either:

   * explicitly stated in the inventory, or
   * `TBD` if dependency order cannot be proven.

**Forbidden:** deriving interface details from Script Cards (they are secondary renderings).

### Artifact linking rule (MUST)
To populate the `inputs` and `outputs` columns:

- For each `inputs[]` item in the job manifest, find exactly one artifact catalog entry whose `s3_location_pattern` matches the manifest `bucket` + `key_pattern` (literal match after variable placeholders are normalized), OR whose `file_name_pattern` matches the terminal filename pattern.
- If exactly one match is found, use that entry’s `artifact_id`.
- If zero or multiple matches are found, write `TBD` in the corresponding position and add an open verification item tagged `[TBD-artifact-catalog]`.

---

## 2) File structure (MUST)

`docs/pipeline_inventory.md` MUST have exactly these top-level headings in this order:

1. `# Pipeline Inventory`
2. `## Scope and evidence`
3. `## Jobs`
4. `## Dependency links`
5. `## Open verification items`

No other top-level headings are allowed.

---

## 3) “Jobs” table schema (MUST)

Under `## Jobs`, there MUST be **one single markdown table** with exactly these columns (same order, same names):

1. `job_id`
2. `job_dir`
3. `glue_job_name`
4. `runtime`
5. `business_purpose`
6. `parameters`
7. `inputs`
8. `outputs`
9. `side_effects`
10. `upstream_job_ids`
11. `downstream_job_ids`
12. `status`

### Column value rules (MUST)

* `job_id`: snake_case, unique across table
* `job_dir`: repo path to the job folder (e.g., `jobs/vendor_input_processing/matching_proposals/`)
* `glue_job_name`: exact value from manifest or `TBD`
* `runtime`: `pyspark | python_shell | TBD`
* `business_purpose`: 1 sentence or `TBD`
* `parameters`: comma-separated parameter names or `TBD`

* `inputs`: semicolon-separated list of `artifact_id` references in the SAME ORDER as `job_manifest.yaml: inputs[]`.
  - Allowed values per position: a concrete `artifact_id` OR `TBD`.
  - If the job has no inputs, use `TBD` (do not use an empty string).
  - Do not paste S3 patterns here.

* `outputs`: semicolon-separated list of `artifact_id` references in the SAME ORDER as `job_manifest.yaml: outputs[]`.
  - Allowed values per position: a concrete `artifact_id` OR `TBD`.
  - If the job has no outputs, use `TBD` (do not use an empty string).
  - Do not paste S3 patterns here.

* `side_effects`: compact string `deletes_inputs=<v>; overwrites_outputs=<v>` where `<v>` is `true|false|TBD`
* `upstream_job_ids`: comma-separated job_ids or `TBD`
* `downstream_job_ids`: comma-separated job_ids or `TBD`
* `status`: one of `active | deprecated | planned | TBD`

**Important:** `inputs` and `outputs` must reference **artifact_ids** from `docs/artifacts_catalog.md` when those exist. If an artifact catalog entry does not exist or cannot be linked unambiguously, use `TBD` for that position (do not paste S3 patterns here).

This makes the inventory stable and “automatically extensible”: new jobs add new artifact_ids rather than rewriting paths everywhere.

---

## 4) Dependency links section (MUST)

Under `## Dependency links`, there MUST be a bullet list, where each bullet is exactly:

`- <upstream_job_id> -> <downstream_job_id> : <artifact_id or TBD>`

Rules:

* Each listed link must correspond to the `upstream_job_ids` / `downstream_job_ids` columns in the Jobs table.
* Use `TBD` if the linking artifact is not yet cataloged.

---

## 5) Open verification items (MUST)

Under `## Open verification items`, include a bullet list of unresolved facts. Each bullet MUST start with one of these tags:

* `[TBD-runtime]`
* `[TBD-params]`
* `[TBD-inputs]`
* `[TBD-outputs]`
* `[TBD-side-effects]`
* `[TBD-wiring]`
* `[TBD-artifact-catalog]`

Example:

* `[TBD-wiring] Confirm Make scenario that triggers job_id=matching_proposals.`

---

## 6) Incremental update rules (MUST)

When adding a new job:

1. Add exactly **one new row** to the Jobs table.
2. Add zero or more new dependency bullets under `## Dependency links`.
3. Add any new verification bullets under `## Open verification items`.
4. Do not rewrite existing rows except to replace `TBD` with confirmed values.
5. If `inputs`/`outputs` positions are `TBD` because artifact_ids are missing or ambiguous, create/fix the required entries in `docs/artifacts_catalog.md` first (or in the same PR), then replace the `TBD` positions.

This enables “automatic extension” without destabilizing history.

---

## 7) Compliance checklist (PASS/FAIL)

The inventory file is compliant if:

* all required headings exist in order
* there is exactly one Jobs table with exact column names
* every job_id is unique and snake_case
* `runtime`, `status` values are from allowed enums
* `side_effects` follows the required `deletes_inputs=...; overwrites_outputs=...` format
* dependency bullets follow the exact `A -> B : artifact` format
* open items bullets start with one of the allowed tags
* `inputs` and `outputs` are semicolon-separated lists aligned to manifest input/output counts (or `TBD` if none)

# Job Inventory Specification (v1.3)

## 0) Purpose and scope

`docs/job_inventory.md` is the authoritative **index** of executable jobs and their **system-level interfaces**.

It must support:
- fast orientation (what jobs exist, what they consume/produce)
- safe AI-supported planning (Codex tasks can reference stable fields)
- incremental extension (new jobs added without rewriting old entries)
- automation-friendly regeneration (deterministic schema; no invented facts)

The inventory is a **compiled view**. It must not contain invented facts.

This specification defines:
- the required structure of `docs/job_inventory.md`
- the required table schema
- deterministic derivation rules from sources of truth
- how unknowns are tracked and displayed


---

## 1) Source-of-truth rules (MUST)

### 1.1 Job discovery rule (MUST)

A job MUST be included in the inventory if and only if:
- a folder under `jobs/<job_group>/<job_id>/` contains `glue_script.py`.

If `job_manifest.yaml` is missing for such a folder, the job row MUST still exist, but all manifest-derived fields MUST be `TBD` and an open verification item `[TBD-manifest]` MUST be added.

### 1.2 Row sourcing rules (MUST)

For each job row:

1. **Interface fields** (parameters, inputs, outputs, side effects, evidence artifacts (run receipt behavior and counters), runtime/executor if present in manifest) MUST come from that job’s `job_manifest.yaml`.
2. **Artifact identifiers** for `inputs` and `outputs` MUST come from `docs/artifacts_catalog.md` by linking each manifest input/output to exactly one `artifact_id` (see artifact linking rule below).
3. **Business purpose text** MAY come from a business description document if present; otherwise `TBD`.
   - If a business description exists, it MUST be taken from `docs/business_job_descriptions/<job_id>.md`.
4. **Dependency claims** (upstream/downstream) MUST only be stated if supported by evidence inside this repo (see “Dependency links” rules). Otherwise `TBD`.

**Forbidden:** deriving interface details from Script Cards (they are secondary renderings).

### 1.3 Manifest field mapping (MUST)

To avoid guessing, the following inventory fields MUST be sourced from these `job_manifest.yaml` keys:

- `deployment_name`:
  - Use `glue_job_name` if present, else `TBD`.
- `runtime`:
  - Use `runtime` if present, else `TBD`.
- `parameters`:
  - Use `parameters` (list of names) if present.
  - If `parameters` exists and is an empty list: `NONE`.
  - Else if missing: `TBD` and add `[TBD-params]`.
- `inputs`:
  - Use `inputs[]` items if present (for artifact linking).
  - If `inputs` exists and has 0 items: `NONE`.
  - Else if missing: `TBD` and add `[TBD-inputs]`.
- `outputs`:
  - Use `outputs[]` items if present (for artifact linking).
  - If `outputs` exists and has 0 items: `NONE`.
  - Else if missing: `TBD` and add `[TBD-outputs]`.
- `side_effects`:
  - Use `side_effects.deletes_inputs` and `side_effects.overwrites_outputs` if present.
  - If missing: `TBD` and add `[TBD-side-effects]`.
- `evidence_artifacts`:
  - `run_receipt` MUST be sourced from `logging_and_receipt.writes_run_receipt` if present; else `TBD` and add `[TBD-evidence]`.
  - `counters` MUST be sourced from `logging_and_receipt.counters_observed` if present:
    - If list is empty: `NONE`.
    - Else: comma-separated names.
  - If `logging_and_receipt` is missing entirely: set both to `TBD` and add `[TBD-evidence]`.

`executor` sourcing:
- If `glue_job_name` exists as a top-level manifest key, set `executor=aws_glue`.
- Otherwise set `executor=TBD` and add `[TBD-executor]`.

### Business purpose extraction rule (deterministic, MAY)

If `docs/business_job_descriptions/<job_id>.md` exists:
- set `business_purpose` to the first sentence of the first paragraph under the heading that starts with `## 1)`.

If the document does not contain such a heading, set `business_purpose=TBD`.

### Artifact linking rule (MUST)

To populate the `inputs` and `outputs` columns:

- For each `inputs[]` / `outputs[]` item in the job manifest, find exactly one artifact catalog entry whose:
  - `s3_location_pattern` matches the manifest `bucket` + `key_pattern` after placeholder normalization, OR
  - `file_name_pattern` matches the terminal filename pattern (if used by the artifact catalog)

Placeholder normalization (deterministic):
- Replace any placeholder segments (e.g. `<vendor>`, `{vendor}`, `${vendor}`, `<timestamp>`, `{run_id}`) with the canonical token `<VAR>`.
- Compare the normalized strings literally (no fuzzy matching).

Match outcome:
- If exactly one match is found, use that entry’s `artifact_id`.
- If zero or multiple matches are found, write `TBD` in the corresponding position and add an open verification item tagged `[TBD-artifact-catalog]`.

No additional heuristics are allowed in v1.3 (to keep automation deterministic).

---

## 2) File structure of `docs/job_inventory.md` (MUST)

`docs/job_inventory.md` MUST have exactly these top-level headings in this order:

1. `# Job Inventory`
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
3. `executor`
4. `deployment_name`
5. `runtime`
6. `owner`
7. `business_purpose`
8. `parameters`
9. `inputs`
10. `outputs`
11. `side_effects`
12. `evidence_artifacts`
13. `upstream_job_ids`
14. `downstream_job_ids`
15. `status`
16. `last_reviewed`

### Column value rules (MUST)

General:
- `TBD` is the only allowed unknown marker.
- `NONE` is the only allowed explicit-empty marker (used only when emptiness is provable from the manifest).
- Table cells MUST NOT contain raw `|` characters. If unavoidable, escape as `\|`.

Field rules:
- `job_id`: snake_case, unique across table
- `job_dir`: repo path to the job folder (e.g., `jobs/vendor_input_processing/matching_proposals/`)
- `executor`: one of `aws_glue | aws_lambda | make | other | TBD`
- `deployment_name`: exact deployment name from manifest if present; else `TBD`
  - For AWS Glue jobs, this is the configured Glue job name.
- `runtime`: one of `pyspark | python_shell | python | nodejs | other | TBD`
- `owner`: short owner identifier (team/role) or `TBD`
- `business_purpose`: 1 sentence or `TBD`
- `parameters`: comma-separated parameter names (no values) or `NONE` or `TBD`
  - `NONE` is allowed only if the manifest shows zero parameters.

Interface lists:
- `inputs`: semicolon-separated list aligned to the manifest `inputs[]` order
  - Each position is either a concrete `artifact_id` or `TBD`
  - If the manifest has zero inputs, use `NONE`
  - Do not paste S3 patterns here
- `outputs`: semicolon-separated list aligned to the manifest `outputs[]` order
  - Each position is either a concrete `artifact_id` or `TBD`
  - If the manifest has zero outputs, use `NONE`
  - Do not paste S3 patterns here

Side effects:
- `side_effects`: compact string `deletes_inputs=<v>; overwrites_outputs=<v>` where `<v>` is `true|false|TBD`

Evidence artifacts:
- `evidence_artifacts`: compact string `run_receipt=<v>; counters=<v>`
  - `run_receipt` value `<v>` is `true|false|TBD`
  - `counters` value `<v>` is:
    - comma-separated counter names (no values), OR
    - `NONE`, OR
    - `TBD`

Dependencies:
- `upstream_job_ids`: comma-separated job_ids or `TBD`
- `downstream_job_ids`: comma-separated job_ids or `TBD`

Lifecycle:
- `status`: one of `active | deprecated | planned | TBD`
- `last_reviewed`: ISO date `YYYY-MM-DD` or `TBD`
  - Meaning: last date the row was validated against its manifest + artifact catalog links.

`last_reviewed` automation rule (MUST):
- When an automation creates or updates a row and can resolve all manifest-derived fields AND can resolve artifact_id links for all inputs/outputs (no `TBD` positions in those lists), it MUST set `last_reviewed` to the automation execution date (local repo convention).
- Otherwise it MUST NOT change `last_reviewed`.

---

## 4) Dependency links section (MUST)

Under `## Dependency links`, there MUST be a bullet list where each bullet is exactly:

`- <upstream_job_id> -> <downstream_job_id> : <artifact_id or TBD>`

Rules:
- Each listed link must correspond to the `upstream_job_ids` / `downstream_job_ids` columns in the Jobs table.
- Use `TBD` if the linking artifact is not yet cataloged.
- If no dependency evidence exists for a job, its upstream/downstream columns remain `TBD` (do not claim `NONE`).

---

## 5) Open verification items (MUST)

Under `## Open verification items`, include a bullet list of unresolved facts.

Each bullet MUST start with one of these tags:

- `[TBD-manifest]`
- `[TBD-runtime]`
- `[TBD-executor]`
- `[TBD-deployment]`
- `[TBD-owner]`
- `[TBD-params]`
- `[TBD-inputs]`
- `[TBD-outputs]`
- `[TBD-side-effects]`
- `[TBD-evidence]`
- `[TBD-wiring]`
- `[TBD-artifact-catalog]`

Example:
- `[TBD-wiring] Confirm Make scenario that triggers job_id=matching_proposals.`

---

## 6) Incremental update rules (MUST)

When adding a new job:
1. Add exactly **one new row** to the Jobs table.
2. Add zero or more new dependency bullets under `## Dependency links`.
3. Add any new verification bullets under `## Open verification items`.
4. Do not rewrite existing rows except to replace `TBD` with confirmed values or to set `last_reviewed`.
5. If `inputs`/`outputs` positions are `TBD` because artifact_ids are missing or ambiguous, create/fix the required entries in `docs/artifacts_catalog.md` first (or in the same PR), then replace the `TBD` positions.

---

## 7) Compliance checklist (PASS/FAIL)

The inventory file is compliant if:
- all required headings exist in order
- there is exactly one Jobs table with exact column names and order
- every job_id is unique and snake_case
- `executor`, `runtime`, `status` values are from allowed enums
- `side_effects` follows the required `deletes_inputs=...; overwrites_outputs=...` format
- `evidence_artifacts` follows the required `run_receipt=...; counters=...` format
- dependency bullets follow the exact `A -> B : artifact` format
- open items bullets start with one of the allowed tags
- `inputs` and `outputs` are semicolon-separated lists aligned to manifest counts, or `NONE` if the manifest count is zero

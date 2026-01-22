# Artifacts Catalog Entry Specification (v1.3.5)

# Artifacts Catalog

## 0) Scope

An **Artifacts Catalog** documents **persistent artifacts** (typically S3 objects) produced/consumed by jobs.
Each **catalog entry** represents **one artifact type** (stable pattern), not a single run instance.

This spec defines a framework that is:
- executable for automation (deterministic create/update rules)
- readable for human review
- auditable via explicit evidence sources

The catalog file is:
- `docs/artifacts_catalog.md`

---

## 1) Catalog file and entry grammar (MUST)

### 1.1 Catalog file structure (MUST)

`docs/artifacts_catalog.md` MUST contain:
- a top-level title: `# Artifacts Catalog`
- then a sequence of entries, each entry starting with `## <artifact_id>`

No other entry delimiter is allowed.

### 1.2 Entry block grammar (MUST)

Each entry MUST follow this structure:

- A heading line: `## <artifact_id>`
- Then a bullet list with keys **in exactly this order**:

1. `artifact_id`
2. `file_name_pattern`
3. `s3_location_pattern`
4. `format`
5. `producer_job_id`
6. `producers` (MUST be present only if shared-artifact exception applies; otherwise MUST be absent)
7. `consumers`
8. `presence_on_success`
9. `purpose`
10. `content_contract`
11. `evidence_sources`

### 1.3 Allowed markers for unknown/empty (MUST)

- `TBD` is the only allowed unknown marker.
- `NONE` is the only allowed explicit-empty marker and MUST be used only when emptiness is provable from evidence.

Scalar `TBD` discipline (MUST):
- For list-typed fields (`consumers`, `producers`, `evidence_sources`, `required_sections`), unknown MUST be expressed as the scalar string `TBD` (not `[TBD]`, not omitted).

---

## 2) Deterministic matching and placeholder normalization (MUST)

### 2.1 Placeholder normalization for matching (MUST)

To make matching deterministic across placeholder styles, automations MUST normalize placeholders before comparison.

Normalization rule:
- Replace any `${...}` token with `<VAR>`.
- Replace any `{...}` token with `<VAR>`.
- Replace any `<...>` token with `<VAR>`.
- No other transformations are allowed (no fuzzy matching).

After normalization, compare strings literally.

### 2.2 Entry matching for create/update (MUST)

Automations that create or update entries MUST follow this matching algorithm to decide whether a candidate artifact
reference corresponds to an existing entry.

Candidate source:
- a job manifest item from `outputs[]`, `inputs[]`, or `config_files[]` (job_manifest.yaml)

Scalar TBD guard (MUST):
- If a candidate block (`outputs`, `inputs`, or `config_files`) is the scalar string `TBD`, stop derivation for that block.
- Do not create new entries from scalar `TBD` blocks.

Step 1 — Construct candidate S3 pattern:
- Construct `s3://${bucket}/${key_pattern}` from the manifest item.
- If `bucket` or `key_pattern` is `TBD`, treat the candidate S3 pattern as `TBD` and continue to Step 3.

Step 2 — Primary match: normalized S3 location match:
- Normalize candidate S3 pattern and each existing entry’s `s3_location_pattern` (see 2.1).
- If exactly one entry matches, reuse that entry.
- If more than one entry matches, automation MUST NOT choose; stop and require human resolution.

Step 3 — Secondary match: terminal filename match:
- Extract terminal segment from the candidate `key_pattern` (after the final `/`).
- Normalize it and compare to existing entries’ `file_name_pattern` (see 2.1).
- If exactly one entry matches, reuse that entry.
- If more than one matches, stop and require human resolution.

Step 4 — No match found:
- Create a new entry and assign `artifact_id` using section 3.1.

---

## 3) Field definitions and sourcing rules (MUST)

### 3.1 `artifact_id` (MUST)

Definition:
- Stable canonical identifier for an artifact type.
- MUST NOT encode run context (timestamps, run ids, concrete vendor values).

If entry exists:
- Existing `artifact_id` MUST be reused; renaming existing ids is forbidden.

If entry does not exist (deterministic derivation rule):
`<producer_anchor>__<artifact_type_snake_case>`

Producer anchor:
- For produced artifacts: `producer_anchor = <producer_job_id>` (folder job_id of the producing job).
- For external (not produced in repo): `producer_anchor = <lexicographically smallest proven consumer job_id>`.
- If no in-repo consumer can be proven: `producer_anchor = external`.

Artifact type token derivation (from manifest `key_pattern`):
1) If `key_pattern` ends with a filename segment containing an extension, use that filename.
2) Else if `key_pattern` is exactly one parameter placeholder (e.g., `${bmecat_input_key}`), use the parameter name without `${}`.
3) Else use the terminal path segment of `key_pattern`.

Normalization:
- Remove common run-context prefixes from the start (at minimum `${vendor_name}_`, `${vendor}_` if present).
- Remove file extension.
- Convert to `snake_case`.

### 3.2 `file_name_pattern` (MUST)

Definition:
- Terminal filename pattern (last segment after final `/`), may contain placeholders.
- MUST NOT be a concrete run instance filename.

Source priority:
1) existing entry (unless change is proven)
2) manifest terminal segment (from `key_pattern`)
3) if `key_pattern` is a single placeholder representing a full key, set `file_name_pattern` to that placeholder token
4) code (last resort; only if a stable filename pattern is explicitly constructed)

If no stable value can be proven: `TBD`.

### 3.3 `s3_location_pattern` (MUST)

Definition:
- Stable S3 location pattern(s) for the artifact type.
- Allowed representation:
  - a single string `s3://...`, OR
  - a bullet list of strings under `s3_location_pattern:`

Automation parsing rule:
- If scalar string is used, treat it as a list of exactly one string for matching and updates.

Source priority:
1) existing entry (unless change is proven)
2) manifest item(s) (`s3://${bucket}/${key_pattern}`)
3) code (last resort; only if stable pattern is explicitly proven)

If no stable pattern can be proven: `TBD`.

### 3.4 `format` (MUST)

Allowed values:
- `json | ndjson | csv | xml | zip | other | TBD`

Source priority:
1) existing entry
2) manifest `format`
3) file extension from `file_name_pattern` (only if unambiguous)
Otherwise `TBD`.

### 3.5 `producer_job_id` (MUST)

Definition:
- Folder `<job_id>` of the in-repo job that produces the artifact type (if produced in repo).
- For shared artifacts (allowlisted), `producer_job_id` is the **canonical owner** (primary accountable producer) of the artifact type.

Source priority:
1) existing entry
2) derive from the producing job’s manifest: the artifact matches an `outputs[]` item using Section 2 matching
Otherwise `TBD`.

### 3.6 Shared artifact exception and `producers` (MUST)

Default rule:
- An artifact type MUST have exactly one producing job (single-writer rule).

Shared-artifact exception:
- Multiple producers are allowed only if `artifact_id` appears in:
  - `docs/registries/shared_artifacts_allowlist.yaml`

If the exception applies:
- `producer_job_id` MUST remain a single job_id (canonical owner / primary accountable producer).
- `producers` MUST be present and MUST list the **additional writer job_ids** (i.e., writers other than `producer_job_id`),
  sorted lexicographically.
- `producers` MUST NOT include the `producer_job_id` value.

If the exception does not apply:
- `producers` MUST be absent.
- If multiple producers are detected, automation MUST stop and require resolution (catalog governance violation).

### 3.7 `consumers` (MUST)

Definition:
- List of in-repo job_ids that consume the artifact type.

Source priority:
1) existing entry
2) derive from other job manifests:
   - a job is a consumer if any item in its `inputs[]` or `config_files[]` matches this entry by Section 2 matching
3) code (last resort; only if stable read pattern is explicitly proven)

If consumers cannot be proven without ambiguity: `TBD`.

Scalar TBD guard:
- If a candidate job manifest has `inputs: TBD` or `config_files: TBD`, do not attempt matching for that block.

### 3.8 `presence_on_success` (MUST)

Allowed values:
- `required | optional | conditional | TBD`

Source priority:
1) existing entry
2) producer manifest output item `required` flag (if available)
   - if `required: true` => `presence_on_success: required`
   - if `required: false` => `presence_on_success: optional`
3) code (only to detect and justify `conditional`)
   - If the code proves the producer job can succeed without writing the artifact under a specific condition
     (e.g., early-exit on empty input, mode switch, feature flag, conditional branch),
     then set `presence_on_success: conditional`.
   - The condition MUST be captured in `content_contract.notes` in plain English (brief, factual, no speculation).
4) otherwise `TBD`

Non-guessing rule (MUST):
- `presence_on_success` MUST NOT be inferred from intent or naming conventions; only manifest or provable code behavior may be used.

### 3.9 `purpose` (MUST)

Definition:
- 1–2 sentence business-level description of what the artifact is and why it exists.
- Must not include implementation mechanics and must not speculate about usage.

Source priority:
1) producer job business description: `docs/business_job_descriptions/<job_id>.md`
2) script card: `docs/script_cards/<job_id>.md` (only if it states business meaning explicitly)
3) minimal factual fallback derived from manifest/code (“what” only)

No-empty rule:
- `purpose` MUST NOT be `TBD`.
- If business intent is not documented, use:
  - `Output written by <producer_job_id>; business purpose not documented yet.`

### 3.10 `content_contract` (MUST)

Definition:
- Minimal parse/validation contract (high level), not a full schema.

Required subfields (in this order):
- `top_level_type`
- `primary_keying`
- `required_sections`
- `empty_behavior`
- `notes`

Allowed values:
- `top_level_type`: `json_object | json_array | ndjson | csv | xml | zip | other | TBD`
- `empty_behavior`: `absent_file_allowed | empty_file_allowed | empty_object_allowed | empty_array_allowed | no_empty_allowed | TBD`
- `primary_keying`: free text or `TBD`
- `required_sections`: list(string), `NONE`, or `TBD`
- `notes`: free text or `TBD`

Operational meaning of `empty_behavior` values (MUST; non-overlapping):
- `absent_file_allowed` — the producer job can succeed without writing the artifact at all (no object exists at the target key/pattern).
- `empty_file_allowed` — the producer writes a zero-byte object to represent “no data”.
- `empty_object_allowed` — the producer writes `{}` to represent “no data”.
- `empty_array_allowed` — the producer writes `[]` to represent “no data”.
- `no_empty_allowed` — on success, a non-empty artifact is expected (representation of “no data” is not allowed).
- `TBD` — cannot be proven from in-repo evidence.

Consistency rule with `presence_on_success` (MUST):
- If `presence_on_success` is set to `conditional` based on provable “success without writing” behavior, then:
  - `content_contract.empty_behavior` MUST be set to `absent_file_allowed`,
  - unless code proves that the success path writes an explicit empty representation instead (then use the relevant `empty_*_allowed`).

Source priority:
1) existing entry
2) business descriptions / ADRs (only if they define structural expectations)
3) manifest/code (only strictly factual structure)
Otherwise `TBD`.

### 3.11 `evidence_sources` (MUST)

Definition:
- List of repo files actually used to populate/confirm fields in the entry.

Allowed sources:
- `jobs/<job_group>/<job_id>/job_manifest.yaml`
- `jobs/<job_group>/<job_id>/glue_script.py`
- `docs/business_job_descriptions/<job_id>.md`
- `docs/script_cards/<job_id>.md`
- `docs/decisions/ADR-*.md`
- `docs/registries/shared_artifacts_allowlist.yaml` (only if shared exception is used)

Population rules:
- MUST include only files actually read/used for the entry.
- MUST be de-duplicated and sorted lexicographically.
- If at least one allowed evidence file was used, `- TBD` MUST NOT be used.
- If no in-repo evidence exists (discouraged), use the scalar string `TBD`.

---

## 4) Compliance checklist (PASS/FAIL)

An entry is compliant if:
- entry heading is `## <artifact_id>` and `artifact_id` key equals the heading id
- keys appear in the exact required order (section 1.2)
- `purpose` is present and not `TBD`
- `format` is one of the allowed values
- `content_contract.empty_behavior` is one of the allowed values
- if the shared-artifact exception applies (artifact_id is allowlisted in `docs/registries/shared_artifacts_allowlist.yaml`), then:
  - `producer_job_id` is a single job_id (canonical owner) and MUST NOT be `shared`
  - `producers` exists and lists additional writer job_ids (sorted lexicographically)
  - `producers` MUST NOT include `producer_job_id`
- if the shared-artifact exception does not apply, then:
  - `producers` is absent
- placeholder normalization and matching rules (section 2) are the only rules used for create/update decisions
- `evidence_sources` lists only allowed sources and reflects what was actually used

The catalog file is compliant if:
- it contains only valid entry blocks as defined in section 1
- no duplicate `artifact_id` entries exist

---

## 5) Example entry skeleton (compliant)

## <artifact_id>

- artifact_id: <artifact_id>
- file_name_pattern: TBD
- s3_location_pattern:
  - TBD
- format: TBD
- producer_job_id: TBD
- consumers: TBD
- presence_on_success: TBD
- purpose: Output written by <producer_job_id>; business purpose not documented yet.
- content_contract:
  - top_level_type: TBD
  - primary_keying: TBD
  - required_sections: TBD
  - empty_behavior: TBD
  - notes: TBD
- evidence_sources: TBD

---

## 6) Optional governance fields (MAY)

These fields MAY be added to an entry to support governance and operational review.  
If present, they MUST appear **only after** `evidence_sources` and **in exactly this order**:
1) `producer_glue_job_name`  
2) `stability`  
3) `breaking_change_rules`

### 6.1 `producer_glue_job_name` (MAY)

Definition:
- Concrete AWS Glue job name used in deployment for the producer.
- This is deployment metadata; it may differ from repo `job_id`.

Allowed values:
- a concrete string (e.g., `preprocess_incoming_bmecat-prod`)
- `TBD`

Source priority:
1) existing entry  
2) producer job manifest `glue_job_name` (if present)  
3) deployment config (only if represented in repo and explicitly referenced in `evidence_sources`)  

Otherwise `TBD`.

### 6.2 `stability` (MAY)

Definition:
- Human governance signal for how stable the artifact contract is expected to be.

Allowed values:
- `stable | evolving | experimental | TBD`

Guidance:
- `stable` — breaking changes strongly discouraged; require explicit governance action.  
- `evolving` — contract may change; consumers should be robust.  
- `experimental` — contract is volatile; consumers should not rely on it.  
- `TBD` — unknown / not set.

Source priority:
1) existing entry  
2) ADR or business description that explicitly states stability expectations  

Otherwise `TBD`.

### 6.3 `breaking_change_rules` (MAY)

Definition:
- Explicit governance rule for how breaking changes are handled for this artifact type.

Allowed values:
- `No breaking changes allowed without ADR and versioned filename`
- `Breaking changes allowed if consumers updated in same PR`
- `TBD`

Source priority:
1) existing entry  
2) ADR or governance doc that explicitly states the rule  

Otherwise `TBD`.

---


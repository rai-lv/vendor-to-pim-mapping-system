# Artifacts Catalog Entry Specification (v1.2)

## 0) Scope

An **Artifacts Catalog** documents **persistent files** produced/consumed by the system (typically S3 objects).
Each **entry** describes **one artifact type** (one filename pattern), not a single run instance.

This specification defines the **minimum necessary fields** to:
- auto-create/update entries from GitHub evidence (manifests + code + business descriptions)
- reference artifacts reliably in further Codex-driven planning/coding tasks

---

## 1) Entry structure (MUST)

Each artifact entry MUST be a standalone markdown block with the following headings and keys **in exactly this order**.

### Definitions and derivations ###

#### 1.0.1 artifact_id definition and derivation (MUST) ####

#### 1.0.1.1 Definition (MUST)
`artifact_id` is the stable canonical identifier for an **artifact type**.

An artifact type represents the same kind of persistent file across runs (same semantic payload + role),
not a specific run instance.

Therefore, `artifact_id` MUST NOT encode run context such as:
- timestamps
- vendor values (e.g., actual vendor names)
- run_id / execution ids

`artifact_id` MUST be usable as a stable reference key across documentation and Codex tasks.

#### 1.0.1.2 Source-of-truth rule (MUST)
If an entry already exists in `docs/artifacts_catalog.md`, its `artifact_id` is the source of truth and MUST be reused.
Codex MUST NOT rename existing `artifact_id`s.

#### 1.0.1.3 Deterministic derivation rule for new entries (MUST)
If no entry exists yet, `artifact_id` MUST be assigned deterministically using only in-repo evidence.

Canonical construction:
`<producer_job_id_snake_case>__<artifact_type_snake_case>`

Where:
- `<producer_job_id_snake_case>` is the job folder name of the producing job (for outputs), normalized to snake_case.
  - If the artifact is not produced by an in-repo job (external input/config), use the **consumer job_id** (the job that uses it).
- `<artifact_type_snake_case>` is derived from the manifest `key_pattern` as follows:

Step A: Determine the base token:
1) If the manifest `key_pattern` ends with a filename segment (contains a terminal segment with an extension), use that filename.
2) Else if `key_pattern` is a single parameter placeholder like `${bmecat_input_key}`, use the parameter name (e.g., `bmecat_input_key`).
3) Else use the terminal path segment of `key_pattern`.

Step B: Normalize the base token to an artifact type name:
- Remove common run-context placeholders/prefixes from the start of the base token, at minimum:
  - `${vendor_name}_`
  - `${vendor}_`
- Remove the file extension (`.json`, `.ndjson`, `.xml`, etc.).
- Convert the result to `snake_case`.

The resulting `artifact_id` MUST be stable across runs and deterministic given the same repo state.

#### 1.0.2 file_name_pattern definition and sourcing (MUST) ####

#### 1.0.2.1 Definition (MUST)
`file_name_pattern` is the **terminal filename pattern** of the artifact type: the last segment of the object key
(after the final `/`).

It is a pattern (may contain placeholders) that represents the artifact type across runs.
It MUST NOT be a concrete run instance filename.

#### 1.0.2.2 Source priority (MUST)
Populate `file_name_pattern` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse its `file_name_pattern` unless a change is proven.
2) **Job manifest** (`jobs/<job_id>/job_manifest.yaml`):
   - If the relevant `key_pattern` ends with a filename segment, set `file_name_pattern` to that terminal segment.
3) **Manifest placeholder fallback**:
   - If the manifest `key_pattern` is a single parameter placeholder representing a full key (e.g., `${bmecat_input_key}`)
     and no filename segment can be extracted, set `file_name_pattern` to that placeholder token (e.g., `${bmecat_input_key}`).
4) **Code (last resort)**:
   - Only if the manifest does not contain a usable terminal segment or placeholder, and the code constructs a stable filename
     pattern explicitly (e.g., via literal string templates). Otherwise do not guess.

If none of the above yields a stable token, set `file_name_pattern: TBD`.

#### 1.0.2.3 Run-context tokens (timestamps/run IDs) (MUST)
If filenames include run-context such as timestamps or run IDs, `file_name_pattern` MUST express them as placeholders,
not concrete values.

Accepted placeholder tokens include (examples):
- `${timestamp}`, `${run_id}`, `${vendor_timestamp}`, `${date}`, `${datetime}`

Rules:
- Manifests MUST represent run-context in `key_pattern` using placeholders (not literal timestamps).
- `file_name_pattern` MUST preserve those placeholders.
- Concrete filenames containing literal timestamps MUST NOT be copied into `file_name_pattern`.

If a manifest provides only a concrete timestamped filename and no placeholder can be proven,
set `file_name_pattern: TBD` and record the reason in `content_contract.notes`.

#### 1.0.3 s3_location_pattern definition and sourcing (MUST) ####

#### 1.0.3.1 Definition (MUST)
`s3_location_pattern` is the canonical **S3 URI pattern** that locates the artifact type in storage.

It MUST represent a stable pattern (may contain placeholders) and MUST NOT be a single run instance path with concrete
run-context values (timestamps, vendor values), unless those are expressed as placeholders.

A single artifact type MAY have multiple S3 location patterns; in that case `s3_location_pattern` MUST be a bullet list.

#### 1.0.3.2 Source priority (MUST)
Populate `s3_location_pattern` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse its `s3_location_pattern` unless a change is proven.
2) **Job manifest** (`jobs/<job_id>/job_manifest.yaml`):
   - For each relevant manifest item (`inputs[]`, `outputs[]`, `config_files[]`), construct:
     `s3://${bucket}/${key_pattern}`
   - If both `bucket` and `key_pattern` are present, `s3_location_pattern` MUST NOT be `TBD`.
3) **Code (last resort)**:
   - Only if the manifest does not provide `bucket` and/or `key_pattern`, and the code proves a stable S3 key pattern
     via explicit string templates. Otherwise do not guess.

If none of the above yields a provable stable S3 pattern, set `s3_location_pattern: TBD`.

#### 1.0.3.3 Scope note (MUST)
This specification is scoped to **file artifacts stored in S3**, because job manifests express storage as `bucket` + `key_pattern`.
Non-S3 artifacts (e.g., database tables, API endpoints, message topics) are out of scope for this catalog and require a separate
catalog/spec if introduced in the system.

#### 1.0.4 format definition and sourcing (MUST) ####

#### 1.0.4.1 Definition (MUST)
`format` specifies the **serialization format of the artifact file as stored** (what a consumer must parse).
It does not describe schema or business meaning.

Allowed values:
`json | ndjson | csv | xml | zip | other | TBD`

Rules:
- If `format = other`, `content_contract.notes` MUST name the actual format in plain text.
- `TBD` is allowed only if the format cannot be proven from in-repo evidence.

#### 1.0.4.2 Source priority (MUST)
Populate `format` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse `format` unless a change is proven.
2) **Job manifest** (`jobs/<job_id>/job_manifest.yaml`): use the `format` value from the relevant `inputs[]`, `outputs[]`, or `config_files[]` item.
3) **File extension inference** (controlled fallback):
   - If the manifest `format` is missing or `TBD`, infer from `file_name_pattern` if it ends with a known extension:
     - `.json` → `json`
     - `.ndjson` → `ndjson`
     - `.csv` → `csv`
     - `.xml` → `xml`
     - `.zip` → `zip`
4) **Code (last resort)**:
   - Only if the manifest and filename pattern do not prove the format, and the code proves the read/write format via explicit logic
     (e.g., line-by-line JSON writing for NDJSON, `json.dumps` for JSON document). Otherwise do not guess.

If none of the above yields a provable value, set `format: TBD`.

#### 1.0.5 producer_job_id definition and sourcing (MUST) ####

#### 1.0.5.1 Definition (MUST)
`producer_job_id` is the **repository job identifier** (job folder name) of the job that produces the artifact type.

A job is considered a producer if it **writes** the artifact as part of normal execution, including:
- create new
- overwrite/replace
- append (content changes)
- update-in-place via write-then-replace

`producer_job_id` is a repo-internal identifier used for documentation linking and automation.
It is not an AWS Glue console job name.

#### 1.0.5.2 Source priority (MUST)
Populate `producer_job_id` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse `producer_job_id` unless a change is proven.
2) **Job manifest** (`jobs/<job_group>/<job_id>/job_manifest.yaml`):
   - If the artifact corresponds to an item in `outputs[]` of that manifest, then `producer_job_id` MUST be `<job_id>`.
3) **Code (last resort)**:
   - Only if no manifest exists or outputs are not declared, and the code proves the job writes the artifact via stable patterns.
   - Otherwise do not guess.

If the artifact is not produced by any in-repo job (e.g., vendor-provided inputs, manually maintained external files),
set `producer_job_id: TBD`.

#### 1.0.5.3 Single-writer rule and shared-artifact exception (MUST)
By default, an artifact type MUST have exactly one producing job in this monorepo (single-writer rule).

If multiple in-repo jobs write the same artifact type, this is a specification violation unless the artifact is explicitly
declared as a shared artifact in:
`docs/registries/shared_artifacts_allowlist.yaml`.

For allowlisted shared artifacts:
- the artifacts catalog entry MUST keep a single `producer_job_id` as the canonical producer (the primary owner), and
- MAY additionally include `additional_writer_job_ids` as an optional field.

If multiple writers are detected and the artifact is not allowlisted, automated updates MUST fail with an instruction to
create/update the shared-artifact allowlist and add an ADR under `docs/decisions/`.

#### 1.0.6 consumers definition and sourcing (MUST) ####

#### 1.0.6.1 Definition (MUST)
`consumers` is the list of repository job identifiers (job folder names) of jobs that **consume** the artifact type.

A job is a consumer if it reads/uses the artifact as part of normal execution via any of the following manifest sections:
- `inputs[]`
- `config_files[]`

`consumers` lists only in-repo jobs (monorepo scope). External systems are out of scope.

#### 1.0.6.2 Source priority (MUST)
Populate `consumers` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse `consumers` unless changes are proven.
2) **Derivation from other job manifests** (`jobs/**/job_manifest.yaml`):
   - A job is a consumer if any item in its `inputs[]` or `config_files[]` matches this artifact type using the matching rules below.
3) **Code (last resort)**:
   - Only if the manifest does not declare the input, and code proves a stable S3 read pattern for this artifact type. Otherwise do not guess.

If consumers cannot be proven without ambiguity, set:
- `consumers: TBD`

#### 1.0.6.3 Matching rules (MUST)
Consumer derivation MUST follow these rules, in order:

Rule A (preferred): **terminal filename match**
- Compare the terminal segment of the candidate job manifest `key_pattern` with this entry’s `file_name_pattern`.
- If they match exactly (including placeholders), the candidate job is a consumer.

Rule B (stronger match for ambiguous filenames): **full S3 pattern match**
- Construct `s3://${bucket}/${key_pattern}` for the candidate manifest item.
- If it matches exactly one of the entry’s `s3_location_pattern` strings, the candidate job is a consumer.

If multiple artifact entries could match the same manifest item using Rule A (ambiguous),
Rule B MUST be attempted. If ambiguity remains, the consumer MUST NOT be added.

#### 1.0.6.4 Allowed use of TBD (MUST)
`consumers` MUST be `TBD` if:
- the artifact is only consumed by systems not represented as jobs in the repo, or
- manifests do not contain matchable patterns (e.g., only opaque key placeholders), or
- matching is ambiguous and cannot be resolved using Rule B.

#### 1.0.7 presence_on_success definition and sourcing (MUST) ####

#### 1.0.7.1 Definition (MUST)
`presence_on_success` defines the expected existence of the artifact type **after a successful run of its producer job**.

Allowed values:
- `required` — the artifact MUST exist after every successful run of the producer job
- `optional` — the artifact MAY or MAY NOT exist after a successful run (missing is not an error)
- `conditional` — the artifact MUST exist only when a provable condition holds; otherwise it may be missing on success
- `TBD` — cannot be proven from in-repo evidence

#### 1.0.7.2 Source priority (MUST)
Populate `presence_on_success` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse `presence_on_success` unless a change is proven.
2) **Producer job manifest** (`jobs/<producer_job_id>/job_manifest.yaml`):
   - If the artifact corresponds to an item in `outputs[]` with `required: true`, set `presence_on_success: required`.
   - If the artifact corresponds to an item in `outputs[]` with `required: false`, set `presence_on_success: optional`.
3) **Code (only to detect conditional)**:
   - If the manifest indicates `required: true/false` but the code proves the job can succeed without writing the artifact
     based on a condition (e.g., early exit on empty input, feature flag, mode switch), set `presence_on_success: conditional`.
   - The condition MUST be summarized in `content_contract.notes` (brief, non-speculative).
4) If `producer_job_id: TBD`, set `presence_on_success: TBD` unless another in-repo producer is proven.

If no value can be proven, set `presence_on_success: TBD`.

#### 1.0.7.3 Non-guessing rule (MUST)
`presence_on_success` MUST NOT be inferred from intent or naming conventions.
Only manifest or provable code behavior may be used.

#### 1.0.8 purpose definition and sourcing (MUST) ####

#### 1.0.8.1 Definition (MUST)
`purpose` is a 1–2 sentence business-level description of:
- what the artifact represents (human meaning), and
- why it exists (business intent / role).

It MUST NOT include implementation details (Spark/Glue mechanics) and MUST NOT speculate.

#### 1.0.8.2 Source priority (MUST)
Populate `purpose` using this priority:

1) **Business job descriptions** (`docs/business_descriptions/<job_id>.*`):
   - If the artifact is produced by a job, extract the purpose of the specific output artifact from the producer job’s business description.
2) **Script cards** (`docs/script_cards/<job_id>.md`):
   - Use only if the script card explicitly states the business meaning of the output artifact.
3) **Manifest/code (fallback; “what” only)**:
   - If no business description or script card provides business intent, derive a minimal strictly factual purpose from manifest/code
     describing what the file is (e.g., “Output written by <job_id> containing aggregated records keyed by vendor_category_id.”).
   - Do not claim downstream usage unless documented in in-repo business descriptions or ADRs.

`evidence_sources` MUST include the actual source files used.

#### 1.0.8.3 No-empty rule (MUST)
`purpose` MUST NOT be `TBD`.
If business intent is not documented, use an explicit unknown-safe fallback sentence such as:
- “Output written by <producer_job_id>; business purpose not documented yet.”

#### 1.0.9 content_contract definition and sourcing (MUST) ####

#### 1.0.9.1 Definition (MUST)
`content_contract` is the minimal parse- and validation contract for the artifact type.
It describes high-level structure and valid empty representation, without defining a field-by-field schema.

It MUST be evidence-based and MUST NOT speculate.

#### 1.0.9.2 Source priority (MUST)
Populate `content_contract` using this priority:

1) **Existing catalog entry**: if the artifact entry already exists, reuse `content_contract` unless a change is proven.
2) **Code (primary for structure)** (`jobs/<job_id>/glue_script.py`):
   - Use only provable facts from explicit object/array/stream construction and write behavior.
3) **Job manifest (supporting evidence)** (`jobs/<job_id>/job_manifest.yaml`):
   - Use for format-related constraints and location context, but do not infer structure unless explicitly stated.
4) **Business descriptions / script cards (supporting evidence)**:
   - May be used only to confirm naming of sections if explicitly stated and consistent with code.
5) If no provable value exists for a sub-field, set that sub-field to `TBD`.

`evidence_sources` MUST include the actual source files used.

#### 1.0.9.3 Sub-field sourcing rules (MUST)

**top_level_type**
- Set to `object` if code writes a single JSON object as the stored artifact (e.g., dumps a dict / writes `{...}`).
- Set to `array` if code writes a single JSON array (e.g., dumps a list / writes `[...]`).
- Set to `scalar` only if code writes a single scalar value (rare).
- For `ndjson` streams, set `top_level_type: TBD` and describe stream semantics in `notes` (see below), unless code proves
  a different top-level container.

**primary_keying**
- Set only if code (or explicit business docs consistent with code) proves top-level keying (e.g., “object keyed by vendor_category_id”).
- Otherwise set `TBD`.

**required_sections**
- List only coarse, stable top-level sections that code explicitly constructs or validates (e.g., top-level keys in a JSON object).
- Do not list inferred fields or deep schema.
- If not provable, use `- TBD`.

**empty_behavior**
Set based on provable producer behavior:
- `empty_object` if the job writes `{}` to represent no data.
- `empty_array` if the job writes `[]` to represent no data.
- `empty_file` if the job writes a zero-byte object.
- `absent_file` if the job can succeed without writing the artifact at all.
- If not provable, set `TBD`.

**notes**
- Use for short factual clarifications (e.g., “NDJSON: one JSON object per line”, compression/zip behavior, known quirks).
- For `ndjson`, notes MUST explicitly state the stream semantics if known from code.

#### 1.0.9.4 Non-guessing rule (MUST)
`content_contract` MUST NOT be inferred from intent, file naming, or assumed conventions.
Only manifest/code/business docs may be used, and only when they provide explicit evidence.

### 1.1 Entry header (MUST)

`## <artifact_id>`

Rules:
* `<artifact_id>` MUST be unique across the catalog.
* `<artifact_id>` MUST be `snake_case`.
* `<artifact_id>` MUST represent an **artifact type**, not a run instance (no timestamps; no vendor-specific values).

### 1.2 Fields (MUST)

Each entry MUST contain all fields below (values may be `TBD` where allowed):

1. **artifact_id:** (repeat the id; must match heading)
2. **file_name_pattern:** (e.g., `${vendor_name}_categoryMatchingProposals.json` or `${bmecat_input_key}` or `TBD`)
3. **s3_location_pattern:** (bucket + key pattern; may be a single string or a bullet list; may be `TBD`)
4. **format:** one of `json | ndjson | csv | xml | zip | other | TBD`
5. **producer_job_id:** (job_id folder name if produced by an in-repo job, else `TBD`)
6. **consumers:** list of job_ids that consume it, or `TBD`
7. **presence_on_success:** one of `required | optional | conditional | TBD`
8. **purpose:** 1–2 sentences (human meaning; must not speculate)
9. **content_contract:**
10. **evidence_sources:** (see below)

#### 1.2.1 evidence_sources (MUST)

`evidence_sources` MUST be a bullet list of repo paths used to populate the entry, using only:
- `jobs/<job_id>/job_manifest.yaml`
- `jobs/<job_id>/glue_script.py`
- `docs/business_descriptions/<job_id>.*`
- `docs/decisions/ADR-*.md`
or `- TBD` if no in-repo evidence exists (discouraged; should be rare).

Purpose: make the entry auditable and prevent silent drift in automated updates.

---

## 1.3 Optional fields (MAY)

The following fields MAY be added, but are NOT required for compliance:

- **producer_glue_job_name:** (exact AWS Glue job name, or `${JOB_NAME}`, or `TBD`)
- **stability:** one of `stable | evolving | experimental | TBD`
- **breaking_change_rules:** one of:
  - `No breaking changes allowed without ADR and versioned filename`
  - `Breaking changes allowed if consumers updated in same PR`
  - `TBD`

These are intentionally optional in v1.2 to keep the catalog automation-focused and minimize unprovable placeholders.

---

## 2) Source priority (MUST)

Populate artifact catalog entries using this priority order:

1) Use `jobs/<job_id>/job_manifest.yaml` first (inputs/outputs/config_files, formats, required flags, bucket/key patterns).
2) Use business descriptions for `purpose` / business meaning when available.
3) Use code only when the manifest/business description does not expose something required by this spec
   (notably: `presence_on_success=conditional`, `empty_behavior`, `required_sections`, `primary_keying`).
4) Use `TBD` only if none of the above provide provable information.

`evidence_sources` MUST list the concrete repo paths actually used.

---

## 3) Allowed use of `TBD` (MUST)

A field MAY be `TBD` only if:
* it cannot be proven from the code/docs currently in the repo, **or**
* it depends on environment wiring not captured in GitHub (e.g., Make scenario details).

Not allowed:
* inventing values to avoid `TBD`
* adding consumers/producers without evidence

---

## 4) Verifiable compliance checklist (PASS/FAIL)

An artifact entry is compliant if and only if:

* It has the exact heading `## <artifact_id>`
* All 10 required fields exist
* `format` uses only allowed values
* `presence_on_success` uses only allowed values
* `content_contract` contains all 5 sub-fields with allowed values
* `evidence_sources` is present and is a bullet list (or `- TBD`)

Optional fields do not affect compliance.

---

## 5) Example entry skeleton (format reference)

```md
## <artifact_id>

- artifact_id: <artifact_id>
- file_name_pattern: TBD
- s3_location_pattern:
  - TBD
- format: TBD
- producer_job_id: TBD
- consumers:
  - TBD
- presence_on_success: TBD
- purpose: TBD
- content_contract:
  - top_level_type: TBD
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- evidence_sources:
  - TBD

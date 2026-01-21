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
9. **content_contract:** (see below)
10. **evidence_sources:** (see below)

#### 1.2.1 evidence_sources (MUST)

`evidence_sources` MUST be a bullet list of repo paths used to populate the entry, using only:
- `jobs/<job_id>/job_manifest.yaml`
- `jobs/<job_id>/glue_script.py`
- `docs/business_descriptions/<job_id>.*`
- `docs/decisions/ADR-*.md`
or `- TBD` if no in-repo evidence exists (discouraged; should be rare).

Purpose: make the entry auditable and prevent silent drift in automated updates.

### 1.3 content_contract (MUST)

`content_contract` MUST contain exactly these sub-fields:

* **top_level_type:** one of `object | array | scalar | TBD`
* **primary_keying:** (e.g., “keyed by vendor_category_id”, or `TBD`)
* **required_sections:** bullet list of required high-level parts of the content, or `- TBD`
* **empty_behavior:** one of `empty_object | empty_array | empty_file | absent_file | TBD`
* **notes:** free text or `TBD` (short)

Rules:
- No field-by-field schema here. This is a “shape + meaning” contract.
- `ndjson` is typically represented as a stream; describe stream semantics in `notes`.

---

## 1.4 Optional fields (MAY)

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

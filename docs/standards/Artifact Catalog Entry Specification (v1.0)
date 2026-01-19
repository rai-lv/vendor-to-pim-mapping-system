# Artifact Catalog Entry Specification (v1.0)

## 0) Scope

An **Artifact Catalog** documents **persistent files** produced/consumed by the pipeline (typically S3 objects).
Each **entry** describes **one artifact type** (one filename pattern), not a single run instance.

## 1) Entry structure (MUST)

Each artifact entry MUST be a standalone markdown block with the following headings and keys **in exactly this order**:

### 1.1 Entry header (MUST)

`## <artifact_id>`

Rules:

* `<artifact_id>` MUST be unique across the catalog.
* `<artifact_id>` MUST be `snake_case`.

### 1.2 Fields (MUST)

Each entry MUST contain all fields below (values may be `TBD` where allowed):

1. **artifact_id:** (repeat the id; must match heading)
2. **file_name_pattern:** (e.g., `${vendor_name}_categoryMatchingProposals.json` or `TBD`)
3. **s3_location_pattern:** (bucket + prefix/key pattern; may be `TBD`)
4. **format:** one of `json | ndjson | csv | xml | zip | other | TBD`
5. **producer_job_id:** (job_id folder name, or `TBD`)
6. **producer_glue_job_name:** (exact AWS Glue job name or `TBD`)
7. **consumers:** list of job_ids or `TBD`
8. **purpose:** 1–2 sentences (human meaning)
9. **content_contract:** (see below)
10. **stability:** one of `stable | evolving | experimental | TBD`
11. **breaking_change_rules:** (see below)

### 1.3 content_contract (MUST)

`content_contract` MUST contain exactly these sub-fields:

* **top_level_type:** one of `object | array | scalar | TBD`
* **primary_keying:** (e.g., “keyed by vendor_category_id”, or `TBD`)
* **required_sections:** bullet list of required high-level parts of the content, or `- TBD`
  (Example: “vendor_categories”, “pim_matches”, etc. Only if provable.)
* **empty_behavior:** one of `empty_object | empty_array | absent_file | TBD`
* **notes:** free text or `TBD` (short)

**Rule:** No field-by-field schema here. This is a “shape + meaning” contract.

### 1.4 breaking_change_rules (MUST)

This MUST be one of:

* `No breaking changes allowed without ADR and versioned filename`, or
* `Breaking changes allowed if consumers updated in same PR`, or
* `TBD`

(You can pick one policy globally, but the entry must state which applies.)

---

## 2) Allowed use of `TBD` (MUST)

A field MAY be `TBD` only if:

* it cannot be proven from the code/docs currently in the repo, **or**
* it depends on environment wiring not captured yet (e.g., exact S3 prefix set by Make).

**Not allowed:** inventing values to avoid `TBD`.

---

## 3) Verifiable compliance checklist (PASS/FAIL)

An artifact entry is compliant if and only if:

* It has the exact heading `## <artifact_id>`
* All 11 required fields exist
* `format` uses only allowed values
* `content_contract` contains all 5 sub-fields with allowed values
* `stability` uses only allowed values
* `breaking_change_rules` is one of the allowed statements or `TBD`

---

## 4) Example entry skeleton (format reference)

```md
## <artifact_id>

- artifact_id: <artifact_id>
- file_name_pattern: TBD
- s3_location_pattern: TBD
- format: TBD
- producer_job_id: TBD
- producer_glue_job_name: TBD
- consumers:
  - TBD
- purpose: TBD
- content_contract:
  - top_level_type: TBD
  - primary_keying: TBD
  - required_sections:
    - TBD
  - empty_behavior: TBD
  - notes: TBD
- stability: TBD
- breaking_change_rules: TBD
```

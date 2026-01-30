# Artifacts Catalog Entry Specification

## Purpose

This standard defines the normative schema for describing artifact contracts and content expectations, preventing ad-hoc contract definitions scattered across job documentation.

## 0) Scope

An **Artifacts Catalog** documents **persistent artifacts** (typically S3 objects) produced/consumed by jobs.
Each **catalog entry** represents **one artifact type** (stable pattern), not a single run instance.

This spec defines a framework that is:
- executable for automation (deterministic create/update rules)
- readable for human review
- auditable via explicit evidence sources

The catalog file is:
- `docs/catalogs/artifacts_catalog.md`

---

## 1) Catalog file and entry grammar (MUST)

### 1.1 Catalog file structure (MUST)

`docs/catalogs/artifacts_catalog.md` MUST contain:
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

**Optional governance fields (Section 6)** MAY appear after `evidence_sources` if present.

### 1.3 Allowed markers for unknown/empty (MUST)

- `TBD` is the only allowed unknown marker.
- `NONE` is the only allowed explicit-empty marker and MUST be used only when emptiness is provable from evidence.

#### 1.3.1 Scalar `TBD` discipline (MUST)

For list-typed fields (`consumers`, `producers`, `evidence_sources`, `required_sections`), unknown MUST be expressed as the scalar string `TBD` (not `[TBD]`, not omitted).

**YAML representation:**
```yaml
# Correct - unknown list field:
consumers: TBD

# Incorrect - do not use:
consumers: [TBD]    # Wrong: not a scalar
consumers:          # Wrong: omitted
  - TBD             # Wrong: list with TBD item
```

#### 1.3.2 `NONE` vs empty list representation (MUST)

For list-typed fields, use the following representation rules:

**When emptiness is provable from evidence:**
```yaml
consumers: NONE     # Correct: scalar string NONE
```

**Empty list representation is NOT allowed:**
```yaml
consumers: []       # Wrong: use NONE instead
```

**Omitted fields are NOT allowed:**
```yaml
# Wrong: field omitted (all required fields must be present)
```

**Semantic meaning:**
- `NONE` (scalar string): Provably empty based on evidence (e.g., no consumers exist)
- Omitted field: Schema violation (all required fields must be present per Section 1.2)
- `[]` (empty list): NOT allowed; use `NONE` instead to maintain consistent scalar representation

---

## 2) Deterministic matching and placeholder normalization (MUST)

### 2.1 Placeholder normalization for matching (MUST)

To make matching deterministic across placeholder styles, automations MUST normalize placeholders before comparison.

#### 2.1.1 Core normalization rule (MUST)

- Replace any `${...}` token with `<VAR>`.
- Replace any `{...}` token with `<VAR>`.
- Replace any `<...>` token with `<VAR>`.
- No other transformations are allowed (no fuzzy matching).

After normalization, compare strings literally.

#### 2.1.2 Edge case handling (MUST)

**Complete placeholder tokens only:**
- Only complete placeholder tokens matching the full pattern are normalized
- Token definition: `${` followed by one or more characters followed by `}`
- Partial matches are NOT normalized

**Adjacent placeholders:**
```
${vendor_name}${date} → <VAR><VAR>
```

**Placeholders within text:**
```
prefix_${vendor}_suffix → prefix_<VAR>_suffix
```

**Nested or malformed placeholders:**
- Nested placeholders (e.g., `${outer_${inner}}`) are NOT expected in artifact patterns
- If encountered during matching, treat the entire string as a single placeholder token
- Malformed placeholders (e.g., unclosed `${vendor`) are NOT normalized; match literally

**Escaped or literal placeholder-like text:**
- Backslash-escaped placeholders (e.g., `\${literal}`) are NOT expected in S3 patterns
- If encountered, treat literally without normalization
- Context: S3 key patterns use actual placeholders, not escaped text

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
- Normalize candidate S3 pattern (see 2.1)
- For each existing entry:
  - If entry has a single `s3_location_pattern`, normalize it and compare to candidate
  - If entry has multiple `s3_location_pattern` values (list), normalize each and compare to candidate
  - Entry matches if candidate matches ANY of the entry's patterns (OR logic)
- If exactly one entry matches, reuse that entry
- If more than one entry matches, automation MUST NOT choose; stop and require human resolution

**Multi-pattern matching rule:**
- An entry with patterns `[A, B, C]` matches candidate `X` if `X` matches `A` OR `B` OR `C`
- "Exactly one entry matches" means exactly one catalog entry has at least one pattern matching the candidate

Step 3 — Secondary match: terminal filename match:
- Extract terminal segment from the candidate `key_pattern` (after the final `/`).
- Normalize it and compare to existing entries’ `file_name_pattern` (see 2.1).
- If exactly one entry matches, reuse that entry.
- If more than one matches, stop and require human resolution.

Step 4 — No match found:
- Create a new entry and assign `artifact_id` using section 3.1.

### 2.3 Entry update rules (MUST)

When a matched entry exists and new evidence differs from the current entry value, follow these update rules:

#### 2.3.1 Auto-updatable fields (additive only)

The following fields MAY be automatically updated by automation when new evidence is discovered:

**Additive list updates:**
- `consumers`: Add new consumer job_ids when evidence shows additional consumers
- `evidence_sources`: Add new evidence source files when used
- `producers`: Add new producer job_ids (only if shared-artifact exception applies per Section 3.6)

**Update rules:**
- MUST add new items when proven by evidence
- MUST NOT remove items without explicit evidence of removal
- MUST maintain lexicographic sort order after updates
- MUST de-duplicate entries

#### 2.3.2 Human-approval fields (breaking changes)

The following fields require human approval before modification (governed by Section 6.5):

**Identity and contract fields:**
- `artifact_id` (renaming forbidden per Section 3.1)
- `producer_job_id` (ownership transfer)
- `file_name_pattern` (may break consumers)
- `s3_location_pattern` (may break discovery)
- `format` (incompatible type changes)
- `presence_on_success` (behavioral contract change)
- `content_contract` (structural contract change)

**Update process:**
- Automation MUST stop and report conflict
- Human reviews conflict and decides on resolution
- Changes require breaking change governance per Section 6.5

#### 2.3.3 Conflict resolution

When evidence conflicts with existing entry values:

**Stop conditions (automation MUST NOT proceed):**
- Evidence contradicts existing field value (e.g., format changed from `json` to `csv`)
- Multiple evidence sources provide conflicting values
- New evidence would trigger breaking change per Section 6.5

**Automation response:**
- Stop update process
- Generate conflict report per Section 2.4
- Require human resolution before proceeding

### 2.4 Conflict resolution process (MUST)

When automation cannot proceed deterministically, follow this process:

#### 2.4.1 Create conflict report

Generate a conflict report containing:
- **Timestamp**: When conflict was detected
- **Candidate artifact**: Details of the artifact causing conflict
- **Conflict type**: One of:
  - Multiple entries match (ambiguous matching)
  - Evidence contradicts existing entry
  - Multiple evidence sources conflict
  - Breaking change detected
- **Matching entries**: List of entry IDs involved (if applicable)
- **Conflicting values**: Current value vs. new evidence value
- **Evidence sources**: Files/sources contributing to conflict
- **Recommendation**: Suggested resolution (if determinable)

#### 2.4.2 Store conflict report

- Create report file: `docs/catalogs/conflicts/YYYY-MM-DD-<artifact_summary>.md`
- Use naming pattern: date prefix, then brief artifact identifier
- Example: `2026-01-30-vendor_products_format_conflict.md`

#### 2.4.3 Notification and resolution

**Notification:**
- Notify catalog maintainer via configured channel (e.g., GitHub issue, PR comment)
- Include link to conflict report file
- Mark automation run as requiring human intervention

**Human resolution options:**
1. Update existing entry to resolve ambiguity (add differentiation, correct values)
2. Create new entry with explicit differentiation
3. Update matching rules in this spec if systematic issue identified
4. Update evidence sources if evidence was incorrect

**Documentation:**
- Document resolution decision in conflict report file
- If systematic issue, consider ADR for rule change
- Update affected catalog entries with resolution

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
- For external (not produced in repo): `producer_anchor = external` (permanent; see below).

**External artifact naming stability rule (MUST):**
- External artifacts (not produced in this repository) always use `producer_anchor = external`
- This anchor is permanent and MUST NOT change even when consumers are added later
- Rationale: Ensures artifact_id stability (satisfies "renaming forbidden" rule above)
- Consumer tracking: Use `consumers` field to document which jobs consume the external artifact
- Exception: If an external artifact later becomes produced in-repo, this is a fundamental change requiring new artifact entry with new artifact_id

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

#### 3.3.1 Multi-pattern usage constraints (MUST)

When an entry has multiple `s3_location_pattern` values, they MUST satisfy these constraints:

**Purpose constraint:**
- Multiple patterns MUST represent alternative locations for the SAME logical artifact
- Valid use cases:
  - Cross-region replication (same artifact in multiple regions)
  - Primary and backup locations
  - Historical migration paths during transition periods
- Invalid use cases (use separate entries instead):
  - Different artifact versions (e.g., `v1` vs `v2`)
  - Different artifact purposes or content
  - Artifacts with different producers

**Consumer guidance:**
- Consumers should treat all patterns as equivalent alternatives
- Primary pattern is typically listed first (by convention)
- Consumers may use any pattern based on their access/proximity needs

**Validation rule:**
- If multiple patterns exist, document in `content_contract.notes` why multiple locations are needed
- If patterns represent fundamentally different artifacts, split into separate catalog entries

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
- If `presence_on_success` is set to `conditional` based on provable "success without writing" behavior, then:
  - `content_contract.empty_behavior` MUST be set to `absent_file_allowed`,
  - unless code proves that the success path writes an explicit empty representation instead (then use the relevant `empty_*_allowed`).

#### 3.10.1 Bidirectional consistency matrix (MUST)

The following combinations of `presence_on_success` and `content_contract.empty_behavior` are valid or invalid:

**Valid combinations:**

`presence_on_success: required` (file must exist on success):
- `empty_behavior: empty_file_allowed` ✅ (zero-byte file written)
- `empty_behavior: empty_object_allowed` ✅ (`{}` written)
- `empty_behavior: empty_array_allowed` ✅ (`[]` written)
- `empty_behavior: no_empty_allowed` ✅ (non-empty content required)

`presence_on_success: optional` (file may or may not exist):
- `empty_behavior: absent_file_allowed` ✅ (file may be missing)
- `empty_behavior: empty_file_allowed` ✅ (or zero-byte if present)
- `empty_behavior: empty_object_allowed` ✅ (or `{}` if present)
- `empty_behavior: empty_array_allowed` ✅ (or `[]` if present)
- `empty_behavior: no_empty_allowed` ✅ (if present, must be non-empty)

`presence_on_success: conditional` (file existence depends on conditions):
- `empty_behavior: absent_file_allowed` ✅ (may be missing based on condition)
- `empty_behavior: empty_file_allowed` ✅ (or zero-byte when written)
- `empty_behavior: empty_object_allowed` ✅ (or `{}` when written)
- `empty_behavior: empty_array_allowed` ✅ (or `[]` when written)

**Invalid combinations:**

`presence_on_success: required` (file must exist on success):
- `empty_behavior: absent_file_allowed` ❌ **INVALID** - contradicts "required" (file missing on success is not allowed)

**Validation rule:**
- Automation MUST reject entries with invalid combinations
- Human review MUST verify consistency when either field is updated
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
4) `deprecated`

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

### 6.4 `deprecated` (MAY)

Definition:
- Marks an artifact type as deprecated or retired from active use.
- Communicates lifecycle state to consumers and automation.

Schema (when present):
```yaml
deprecated:
  status: true
  superseded_by: <new_artifact_id>  # Optional: replacement artifact
  deprecation_date: YYYY-MM-DD      # Optional: when deprecated
  removal_date: YYYY-MM-DD          # Optional: planned removal
  reason: <text>                     # Optional: explanation
```

Allowed values:
- `status`: `true` (artifact is deprecated) or omit field entirely if not deprecated
- `superseded_by`: artifact_id of replacement artifact (if applicable), or omit
- `deprecation_date`: ISO 8601 date when deprecation was announced
- `removal_date`: ISO 8601 date when artifact will be removed/unsupported
- `reason`: Brief explanation of why deprecated and migration guidance

Usage rules (MUST):
- When `deprecated.status: true`, the artifact is marked as deprecated
- Deprecated entries remain in catalog for historical reference
- Consumers should migrate away from deprecated artifacts
- New consumers should not use deprecated artifacts
- If `superseded_by` is provided, it MUST reference a valid artifact_id in the catalog

Example (artifact deprecated with replacement):
```yaml
deprecated:
  status: true
  superseded_by: preprocessIncomingBmecat__vendor_products_v2
  deprecation_date: 2026-01-15
  removal_date: 2026-06-30
  reason: "Migrating to new schema with enhanced validation. See ADR-042 for migration guide."
```

Example (artifact deprecated without replacement):
```yaml
deprecated:
  status: true
  deprecation_date: 2026-01-20
  reason: "Feature discontinued. No replacement planned."
```

Source priority:
1) existing entry
2) ADR documenting deprecation decision
3) explicit team decision with documented rationale

### 6.5 Breaking Changes for Artifact Contracts (normative)

This section defines what constitutes a **breaking change** vs a **non-breaking change** for artifact catalog entries.

**Purpose:** Enable consistent governance decisions and validation automation by providing a canonical definition of artifact contract compatibility.

#### 6.4.1 Breaking changes (MUST require governance approval)

The following changes to an artifact catalog entry are **breaking changes** and MUST follow the governance approval process defined in `docs/standards/decision_records_standard.md`:

**Identity and location changes:**
- Renaming `artifact_id` (breaks references from job manifests, orchestration, and other catalog entries)
- Changing `file_name_pattern` in a way that breaks existing S3 key construction (e.g., changing `output.json` to `result.json`)
- Adding, removing, or changing `s3_location_pattern` entries when it prevents existing consumers from finding the artifact
- Changing `producer_job_id` (reassigning ownership)

**Format and structure changes:**
- Changing `format` to an incompatible type (e.g., `json` → `csv`, `ndjson` → `json`)
- Changing `content_contract.top_level_type` to an incompatible type (e.g., `json_object` → `json_array`)
- Removing items from `content_contract.required_sections` (consumers may depend on these sections)
- Changing `content_contract.primary_keying` in a way that breaks consumer join/lookup logic

**Behavioral changes:**
- Changing `presence_on_success` from `required` to `optional` or `conditional` (breaks consumers expecting the file to always exist)
- Changing `content_contract.empty_behavior` to a more restrictive value:
  - `absent_file_allowed` → `empty_file_allowed` (file must now always be written)
  - `empty_file_allowed` → `no_empty_allowed` (file must now contain data)
  - `empty_object_allowed` → `no_empty_allowed` (object must now contain keys)
  - `empty_array_allowed` → `no_empty_allowed` (array must now contain elements)

**Governance field changes (if used):**
- Changing `stability` from `stable` to `evolving` or `experimental` (signals reduced reliability)

#### 6.4.2 Non-breaking changes (allowed without special approval)

The following changes are **non-breaking** and MAY be made without formal governance approval, though they SHOULD still be reviewed:

**Additive changes:**
- Adding new `s3_location_pattern` entries (additional locations where the artifact can be found)
- Adding items to `content_contract.required_sections` (additional guaranteed sections; does not break existing consumers)
- Changing `presence_on_success` from `optional` or `conditional` to `required` (strengthens the guarantee)

**Relaxing restrictions:**
- Changing `content_contract.empty_behavior` to a less restrictive value:
  - `no_empty_allowed` → any other value (more permissive)
  - `empty_file_allowed` → `absent_file_allowed` (more permissive)

**Metadata and documentation changes:**
- Clarifying `purpose` text without changing the artifact's actual behavior
- Adding or updating `content_contract.notes` (documentation only)
- Adding, removing, or updating `evidence_sources` (traceability metadata)
- Updating `producer_glue_job_name` to reflect deployment changes (metadata only)
- Changing `stability` from `experimental` to `evolving` or `stable` (signals increased reliability)

**Format compatibility changes:**
- Changing `format` to a compatible type if the file structure remains unchanged (e.g., `other` → `json` when format is clarified)

#### 6.4.3 Backward compatibility expectations

When a breaking change is unavoidable, the following practices SHOULD be followed:

**Deprecation period:**
- Minimum: 2 release cycles or 30 days (whichever is longer)
- During deprecation: support both old and new contracts (e.g., dual-write to old and new filenames)
- Emit deprecation warnings in job logs and run receipts

**Versioned filenames:**
- For breaking format/structure changes: introduce a versioned filename (e.g., `output.json` → `output_v2.json`)
- Update producer to write both versions during transition
- Update consumers one by one to read new version
- Remove old version after all consumers migrated

**Migration plan:**
- Document migration steps in an ADR
- Identify all affected consumers (use `consumers` field in catalog entry)
- Coordinate updates with consumer owners
- Validate that no downstream jobs break

**Decision record:**
- Create an ADR documenting:
  - Why the breaking change is necessary
  - Which consumers are affected
  - Migration plan and timeline
  - Backward compatibility approach (if any)

#### 6.4.4 Relationship to `breaking_change_rules` field

The optional `breaking_change_rules` field (Section 6.3) MAY be used to override or augment these default rules for a specific artifact type:

- `No breaking changes allowed without ADR and versioned filename` — Strict governance; all breaking changes require both ADR approval and versioned filenames (no in-place updates)
- `Breaking changes allowed if consumers updated in same PR` — Relaxed governance for tightly-coupled artifacts; breaking changes are allowed if all consumer job manifests are updated in the same pull request

If `breaking_change_rules` is `TBD` or absent, the default rules in this section (6.4) apply.

---

## 7) Consistency Check Appendix

### 7.1 Aligned documents

This specification was drafted and validated against the following repository documentation:

**Context layer:**
- `docs/context/development_approach.md` — Ensured alignment with 5-step workflow, approval gates, and evidence discipline
- `docs/context/target_agent_system.md` — Verified agent/tool role separation and "no hidden authority" principle
- `docs/context/documentation_system_catalog.md` — Confirmed canonical placement in `docs/standards/` and appropriate content boundaries
- `docs/context/glossary.md` — Verified term usage (artifact, evidence, TBD, deterministic, job manifest, etc.)

**Standards layer:**
- `docs/standards/job_manifest_spec.md` — Aligned artifact entry sourcing rules with manifest schema (inputs, outputs, config_files, bucket, key_pattern, format, required flag)
- `docs/standards/naming_standard.md` — Aligned artifact_id derivation rules with job_id and naming conventions
- `docs/standards/validation_standard.md` — Ensured compliance checklist is validator-friendly and deterministic

**Process layer:**
- `docs/process/workflow_guide.md` — Verified that the spec supports validation/evidence requirements (Step 5) and does not conflict with process

**Living catalogs:**
- `docs/catalogs/artifacts_catalog.md` — This spec defines the schema that catalog entries must follow

### 7.2 Assumptions introduced

**Assumption 1: Job manifest as primary evidence source**
- **What**: The spec assumes `job_manifest.yaml` files exist for all jobs and contain `inputs[]`, `outputs[]`, and `config_files[]` sections
- **Why**: Required for deterministic artifact entry derivation (Section 2.2, 3.2, 3.3, 3.5, 3.7)
- **Grounding**: Validated against `docs/standards/job_manifest_spec.md` which defines these as required manifest sections
- **Impact**: Spec is only operationalizable when job manifests exist
- **Status**: ✅ Grounded — no action needed

**Assumption 2: Single-writer default**
- **What**: Section 3.6 assumes the default governance rule is "one producer per artifact type" (single-writer rule)
- **Why**: Simplifies orchestration and reduces coordination complexity
- **Grounding**: Not explicitly stated in development approach or governance docs, but implied by the need for an explicit "shared-artifact exception" mechanism
- **Impact**: If multi-writer artifacts are common, the exception mechanism may be overused
- **Status**: ⚠️ Implicit — consider making explicit in a governance doc or ADR

**Assumption 3: S3 as artifact storage**
- **What**: The spec assumes all artifacts are S3 objects (Section 0: "typically S3 objects", Section 3.3: `s3_location_pattern`)
- **Why**: Matches the AWS Glue / PySpark runtime environment described in glossary
- **Grounding**: Validated against `docs/context/system_context.md` and `docs/standards/job_manifest_spec.md` which use S3 extensively
- **Impact**: Spec would need updates if non-S3 artifacts are introduced (e.g., DynamoDB tables, RDS data)
- **Status**: ✅ Grounded — documented in scope (Section 0)

**Assumption 4: Placeholder normalization prevents all ambiguity**
- **What**: Section 2.1 assumes that normalizing `${...}`, `{...}`, and `<...>` to `<VAR>` makes matching deterministic
- **Why**: Enables consistent matching across different placeholder style conventions
- **Grounding**: Informed by `docs/standards/job_manifest_spec.md` which uses `${...}` style
- **Impact**: May fail if placeholders have semantic differences (e.g., `${date}` vs `${timestamp}`) that should not match
- **Status**: ⚠️ Bounded — normalization is intentionally lossy; edge cases may require human resolution

### 7.3 Cross-document dependencies

This spec depends on:
- `docs/standards/job_manifest_spec.md` — for manifest schema and field semantics
- `docs/standards/naming_standard.md` — for job_id and artifact naming conventions; aligned with for breaking change definitions
- `docs/standards/decision_records_standard.md` — for governance approval process (referenced in Section 6.5)
- `docs/catalogs/artifacts_catalog.md` — as the instance file this spec governs
- `docs/registries/shared_artifacts_allowlist.yaml` — for shared-artifact exception (now created)

Documents that depend on this spec:
- `docs/catalogs/artifacts_catalog.md` — must conform to entry structure defined here
- `docs/registries/shared_artifacts_allowlist.yaml` — follows governance rules defined here
- Automation tools (e.g., catalog generators/updaters) — must follow matching and sourcing rules
- `docs/standards/validation_standard.md` — should include artifact catalog compliance checks

### 7.4 Traceability summary

| Section | Requirement | Grounded in | Status |
|---------|-------------|-------------|--------|
| 0 (Scope) | Artifacts are S3 objects | System context, glossary, job manifest spec | ✅ Verified |
| 1.1 (Catalog file) | Single canonical file `docs/catalogs/artifacts_catalog.md` | Documentation system catalog | ✅ Verified |
| 1.2 (Entry grammar) | Required field order | Job manifest spec field order pattern | ✅ Aligned |
| 2.1 (Placeholder normalization) | Deterministic matching | Job manifest spec placeholder usage | ✅ Aligned |
| 3.1 (artifact_id) | Derivation from job_id | Naming standard | ✅ Verified |
| 3.6 (Shared artifact exception) | Allowlist file location | Documentation system catalog (registries layer); file now created | ✅ Verified |
| 3.8 (presence_on_success) | Required flag alignment | Job manifest spec `required` field | ✅ Verified |
| 3.9 (purpose) | No-empty rule | Development approach (no silent unknowns) | ✅ Aligned |
| 3.10 (content_contract) | Empty behavior semantics | Validation standard (deterministic evidence) | ✅ Aligned |
| 6.3 (breaking_change_rules) | Breaking change definition | Naming standard; Section 6.5 provides normative definitions | ✅ Complete |
| 6.4 (Breaking changes) | Compatibility rules | Naming standard Section 5; decision records standard | ✅ Aligned |

---


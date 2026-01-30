# Job Inventory Entry Specification

## Purpose

This standard defines the normative schema and semantics for **job inventory entries** — machine-readable records that describe the interface and metadata of executable jobs in the system. Job inventory entries enable consistent discovery, validation, automation, and cross-job integration without requiring direct inspection of job implementation artifacts.

## 0) Purpose and scope

### What this standard defines

This specification defines the **canonical structure and interpretation rules** for individual job inventory entries. Each entry represents one job's:
- identity (job ID, deployment name, location),
- execution characteristics (runtime, executor),
- interface contract (parameters, inputs, outputs, side effects),
- lifecycle metadata (owner, status, review date),
- dependency relationships (upstream/downstream jobs).

The normative schema defined here supports:
- **Discovery**: Fast orientation for humans and agents (what jobs exist, what they consume/produce)
- **Validation**: Deterministic verification that entries conform to required structure and semantics
- **Automation**: Reliable extraction of job metadata by tools, orchestration systems, and planning agents
- **Governance**: Tracking of job lifecycle, ownership, and interface stability

### How entries are used

Job inventory entries are compiled into the repository's authoritative job catalog (`docs/catalogs/job_inventory.md`). The catalog is a **living inventory** that aggregates entries following this specification.

Entries are sourced from:
- Job manifests (`jobs/<job_group>/<job_id>/job_manifest.yaml`) for interface facts
- Artifact catalog (`docs/catalogs/artifacts_catalog.md`) for artifact identifiers
- Business descriptions (`docs/business_job_descriptions/<job_id>.md`) for purpose statements
- Repository evidence (folder structure, file presence) for discovery

### Out of scope

This specification does NOT define:
- **Catalog file structure**: The overall structure and section rules for `docs/catalogs/job_inventory.md` (this is an implementation concern)
- **Tool command syntax**: How to run validation or regeneration tools (see `docs/ops/tooling_reference.md`)
- **Per-job business logic**: Business rationale, requirements, or domain rules (see `docs/standards/business_job_description_spec.md`)
- **Implementation details**: Job code structure or runtime behavior (see `docs/standards/script_card_spec.md`)
- **Derivation procedures**: Detailed algorithms for extracting entry values from source artifacts (this is tooling implementation)
---

## 1) Core concepts

### 1.1 What is a job inventory entry?

A **job inventory entry** is a structured record representing one executable job. It captures:
- **Identity**: Unique identifier, folder location, deployment name
- **Interface contract**: What the job accepts (parameters, inputs) and produces (outputs)
- **Behavior characteristics**: Side effects, evidence artifacts, execution runtime
- **Governance metadata**: Owner, lifecycle status, last review date
- **Dependencies**: Relationships with other jobs via shared artifacts

### 1.2 Entry vs catalog distinction

- **Entry** (this spec): The normative schema for a single job's record
- **Catalog** (separate concern): The compiled inventory file containing all entries

This specification defines entries. The catalog structure, section headings, and presentation format are implementation concerns governed by catalog tooling and documentation standards.

### 1.3 Semantic properties

**Machine-readable**: Entries must be parseable and validatable by automation without human interpretation.

**Evidence-based**: Entry values must be sourced from authoritative artifacts (manifests, catalogs, file system evidence). Unknown values are explicitly marked with `TBD`.

**Stable patterns**: Entries describe stable interface contracts, not run-specific instances. Placeholders represent parameterized values; concrete run identifiers must not appear in entry patterns.

**Incremental maintenance**: New jobs can be added by inserting new entries without modifying existing entries (except to update dependency relationships or resolve TBDs).

---

## 2) Normative schema for job inventory entries

### 2.1 Required fields

Every job inventory entry MUST contain the following fields:

| Field | Type | Meaning | Unknown marker |
|-------|------|---------|----------------|
| `job_id` | string (identifier) | Canonical job identifier (snake_case) | N/A (always known) |
| `job_dir` | string (path) | Repository path to job folder | N/A (always known) |
| `executor` | enum | Job execution platform | `TBD` |
| `deployment_name` | string | Deployed job name | `TBD` |
| `runtime` | enum | Execution runtime type | `TBD` |
| `owner` | string | Responsible team/role | `TBD` |
| `business_purpose` | string (sentence) | One-sentence purpose statement | `TBD` |
| `parameters` | list(string) or marker | Parameter names (no values) | `TBD`, `NONE` |
| `inputs` | list(artifact_id) or marker | Input artifact identifiers | `TBD`, `NONE` |
| `outputs` | list(artifact_id) or marker | Output artifact identifiers | `TBD`, `NONE` |
| `side_effects` | structured string | Delete/overwrite behaviors | `TBD` |
| `evidence_artifacts` | structured string | Run receipt and counters | `TBD` |
| `upstream_job_ids` | list(job_id) or marker | Jobs this job depends on | `TBD` |
| `downstream_job_ids` | list(job_id) or marker | Jobs that depend on this job | `TBD` |
| `status` | enum | Job lifecycle status | `TBD` |
| `last_reviewed` | date (ISO 8601) | Last validation date | `TBD` |

### 2.2 Field semantics and value rules

#### 2.2.1 Identity fields

**`job_id` (MUST; always known)**
- Format: snake_case identifier (lowercase with underscores)
- Uniqueness: Must be unique across all entries
- Derivation: Folder name from `jobs/<job_group>/<job_id>/`
- Specification: `docs/standards/naming_standard.md` Section 4.1
- Breaking change: Renaming a job_id requires governance approval and migration plan

**`job_dir` (MUST; always known)**
- Format: Repository-relative path ending with `/`
- Example: `jobs/vendor_input_processing/matching_proposals/`
- Derivation: Path to folder containing `glue_script.py`

**`deployment_name` (MUST)**
- Meaning: Deployed job name in execution platform (e.g., AWS Glue job name)
- Format: String matching platform naming constraints
- Source: `glue_job_name` field from job manifest
- Unknown: `TBD` (if manifest missing or field not present)

#### 2.2.2 Execution characteristics

**`executor` (MUST)**
- Meaning: Platform that executes the job
- Allowed values: `aws_glue`, `aws_lambda`, `make`, `other`, `TBD`
- Derivation: Inferred from manifest `glue_job_name` presence or explicit declaration
- Unknown: `TBD` (if cannot determine from manifest)

**`runtime` (MUST)**
- Meaning: Execution runtime type
- Allowed values: `pyspark`, `python_shell`, `python`, `nodejs`, `other`, `TBD`
- Source: `runtime` field from job manifest
- Unknown: `TBD` (if manifest missing or field not present)
- Specification: `docs/standards/job_manifest_spec.md` Section 5.2

#### 2.2.3 Interface contract fields

**`parameters` (MUST)**
- Meaning: List of parameter names accepted by job (no values)
- Representation:
  - Known parameters: Comma-separated list (e.g., `INPUT_BUCKET, vendor_name`)
  - Provably empty: `NONE`
  - Unknown: `TBD`
- Source: `parameters` list from job manifest
- Order: Preserve manifest order when known

**`inputs` (MUST)**
- Meaning: List of artifact identifiers consumed by job
- Representation:
  - Known artifacts: Semicolon-separated list aligned to manifest order (e.g., `external__bmecat_input; preprocessIncomingBmecat__vendor_products`)
  - Individual unknown positions: `TBD` in specific position
  - Provably empty: `NONE`
  - Entirely unknown: `TBD`
- Source: Artifact identifiers resolved from manifest `inputs[]` via artifact catalog matching
- Linking: Each manifest input item must match exactly one artifact catalog entry by normalized S3 pattern or filename
- Placeholder normalization: See `docs/standards/artifacts_catalog_spec.md` Section 2.1

**`outputs` (MUST)**
- Meaning: List of artifact identifiers produced by job
- Representation: Same rules as `inputs`
- Source: Artifact identifiers resolved from manifest `outputs[]` via artifact catalog matching

**`side_effects` (MUST)**
- Meaning: Job behaviors that modify S3 state beyond declared outputs
- Format: Compact structured string `deletes_inputs=<value>; overwrites_outputs=<value>`
- Allowed values per component: `true`, `false`, `TBD`
- Example: `deletes_inputs=false; overwrites_outputs=true`
- Source: `side_effects` object from job manifest
- Unknown: `deletes_inputs=TBD; overwrites_outputs=TBD` (if manifest missing or incomplete)

**`evidence_artifacts` (MUST)**
- Meaning: Audit artifacts produced by job
- Format: Compact structured string `run_receipt=<value>; counters=<value>`
- Allowed values for `run_receipt`: `true`, `false`, `TBD`
- Allowed values for `counters`: Comma-separated counter names, `NONE`, `TBD`
- Example: `run_receipt=true; counters=products_processed, errors_encountered`
- Source: `logging_and_receipt` object from job manifest

#### 2.2.4 Dependency fields

**`upstream_job_ids` (MUST)**
- Meaning: Jobs that produce artifacts consumed by this job
- Representation:
  - Known dependencies: Comma-separated job IDs (e.g., `preprocessIncomingBmecat, external_data_source`)
  - Unknown: `TBD`
- Derivation: Artifact-level evidence (jobs producing artifacts this job consumes)
- Order: Lexicographic sort for stability

**`downstream_job_ids` (MUST)**
- Meaning: Jobs that consume artifacts produced by this job
- Representation: Same rules as `upstream_job_ids`
- Derivation: Artifact-level evidence (jobs consuming artifacts this job produces)

#### 2.2.5 Governance metadata

**`owner` (MUST)**
- Meaning: Team or role responsible for the job
- Format: Short identifier (e.g., `data_pipeline_team`, `vendor_integration`)
- Maintenance: Human-maintained; automation must preserve existing non-TBD values
- Unknown: `TBD`

**`business_purpose` (MUST)**
- Meaning: One-sentence description of job's business objective
- Format: Single sentence (under 200 characters recommended)
- Source: Extracted from business description document if present
- Unknown: `TBD`

**`status` (MUST)**
- Meaning: Job lifecycle stage
- Allowed values: `active`, `deprecated`, `planned`, `TBD`
- Maintenance: Human-maintained; automation must preserve existing non-TBD values
- Unknown: `TBD`

**`last_reviewed` (MUST)**
- Meaning: Date when entry was last validated against source artifacts
- Format: ISO 8601 date `YYYY-MM-DD`
- Update rule: Set to current date when automation successfully resolves all manifest-derived fields and artifact links
- Unknown: `TBD`

### 2.3 Unknown and empty value semantics

#### 2.3.1 `TBD` (unknown marker)

**Meaning**: Value cannot be determined from available evidence.

**Usage rules**:
- Use for scalar fields when source artifact is missing or field is not present
- Use for list fields when list content is entirely unknown (not partially known)
- Must be accompanied by explanation in verification items (catalog implementation concern)

**Distinction from provably empty**: `TBD` means "unknown"; `NONE`/`[]` means "proven to be empty"

#### 2.3.2 `NONE` (explicit empty marker)

**Meaning**: Evidence confirms the list is provably empty.

**Usage rules**:
- Use for `parameters` when manifest shows `parameters: []`
- Use for `inputs` when manifest shows `inputs: []`
- Use for `outputs` when manifest shows `outputs: []`
- Use within `evidence_artifacts` counters when manifest shows `counters_observed: []`

**Rationale**: Distinguishes "no items exist" from "don't know if items exist"

#### 2.3.3 Scalar `TBD` discipline for list fields

For list-type fields (`parameters`, `inputs`, `outputs`, `upstream_job_ids`, `downstream_job_ids`):
- Unknown MUST be represented as scalar string `TBD` (not `[TBD]` or omitted field)
- Individual unknown positions within a known-length list use `TBD` at that position

Example for `inputs` with 3 positions where middle one is unknown:
```
inputs: artifact_one; TBD; artifact_three
```

---

## 3) Placeholder handling

### 3.1 Placeholder representation in entries

Job inventory entries describe **stable interface patterns**, not concrete run instances. Placeholders represent runtime-substituted values in artifact patterns.

### 3.2 Canonical placeholder format

**In job manifests**: `${NAME}` (canonical format per `docs/standards/job_manifest_spec.md` Section 6.1)

**In inventory entries**: Placeholders are resolved to artifact identifiers through artifact catalog matching. The inventory does not expose placeholder syntax directly; it references stable artifact identifiers.

### 3.3 Normalized placeholder matching

When matching manifest patterns to artifact catalog entries, placeholders are normalized per `docs/standards/artifacts_catalog_spec.md` Section 2.1:
- `${vendor}`, `{vendor}`, `<vendor>` all normalize to `<VAR>`
- Matching is deterministic after normalization
- No fuzzy matching or heuristic interpretation

### 3.4 Cross-reference

For complete placeholder naming rules and semantics:
- Parameter placeholders: `docs/standards/naming_standard.md` Section 4.6
- Manifest placeholder usage: `docs/standards/job_manifest_spec.md` Section 6
- Artifact matching normalization: `docs/standards/artifacts_catalog_spec.md` Section 2.1

---

## 4) Compatibility and breaking changes

### 4.1 Stable contracts

Job inventory entries represent **interface contracts**. The following changes are considered breaking and require governance approval:

**Breaking changes**:
- Renaming `job_id`
- Changing `deployment_name` for a deployed job
- Removing items from `parameters` list
- Removing items from `inputs` or `outputs` lists
- Changing `artifact_id` references (cascades from artifact catalog changes)

**Governance requirements for breaking changes**:
- Decision record documenting rationale, impact, and migration plan
- Deprecation period with backward compatibility support (where feasible)
- Update to all affected entries and downstream dependencies
- Explicit human approval before implementation

### 4.2 Non-breaking changes

The following changes are non-breaking and can be made incrementally:

- Adding new entries (new jobs)
- Adding optional parameters to existing jobs (if appended to list)
- Adding new outputs (if additive and not replacing existing artifacts)
- Resolving `TBD` values to concrete values
- Updating `last_reviewed` date
- Updating `status` from `planned` to `active`

### 4.3 Backward compatibility expectations

**Deprecation period**: Minimum 30 days or one release cycle (whichever is longer) when removing or renaming stable identifiers.

**Dual-write support**: For artifact renames, maintain dual-write (old and new artifact) during transition period.

**Migration guidance**: Breaking changes must include explicit migration steps for affected consumers.

### 4.4 Schema evolution

**Adding new fields**: New optional fields may be added to the schema without breaking existing entries. Automation must handle absent fields gracefully.

**Changing field semantics**: Requires new specification version and governance approval. Cannot be done silently.

**Deprecating fields**: Requires deprecation marker, transition period, and eventual removal with version increment.

---

## 5) Validation expectations

### 5.1 Schema validation (MUST)

Validators MUST verify:

**Structural compliance**:
- All required fields are present
- Field types match normative schema
- Enum values are from allowed sets
- `job_id` is unique across all entries
- `job_id` follows naming standard (snake_case pattern)

**Semantic compliance**:
- `job_dir` path exists in repository (contains `glue_script.py`)
- Artifact identifiers in `inputs`/`outputs` exist in artifact catalog
- Job IDs in `upstream_job_ids`/`downstream_job_ids` reference existing entries
- `side_effects` and `evidence_artifacts` follow compact structured string format
- `last_reviewed` is valid ISO 8601 date or `TBD`

**Consistency compliance**:
- `deployment_name` matches manifest `glue_job_name` (if manifest exists)
- `runtime` matches manifest `runtime` field (if manifest exists)
- Parameter/input/output counts align with manifest declarations

### 5.2 Evidence validation (SHOULD)

Validators SHOULD check:

**Source traceability**:
- Fields marked as sourced from manifest can be traced to actual manifest file
- Artifact identifiers can be matched to artifact catalog entries
- Business purpose can be traced to business description document

**TBD tracking**:
- All `TBD` values have corresponding verification items (catalog implementation)
- `TBD` values are not present when source evidence exists

### 5.3 Validation failure handling

**Critical violations** (MUST block entry acceptance):
- Missing required fields
- Invalid enum values
- Malformed structured strings
- Non-existent artifact references
- Duplicate `job_id`
- `job_id` format violations

**Warnings** (SHOULD flag for review):
- `TBD` values without explanation
- Missing manifest when job folder exists
- Misaligned field values between entry and manifest
- Outdated `last_reviewed` date (>90 days)

---

## 6) Illustrative example (non-normative)

The following example shows a complete job inventory entry. This is for illustration only and is not normative.

```yaml
job_id: preprocessIncomingBmecat
job_dir: jobs/vendor_input_processing/preprocessIncomingBmecat/
executor: aws_glue
deployment_name: preprocessIncomingBmecat
runtime: pyspark
owner: vendor_integration_team
business_purpose: Extract and standardize product data from vendor BMEcat XML files
parameters: INPUT_BUCKET, Vendor_name, Bmecat_input_key, Bmecat_output_prefix
inputs: external__bmecat_input
outputs: preprocessIncomingBmecat__vendor_products; preprocessIncomingBmecat__vendor_categories
side_effects: deletes_inputs=false; overwrites_outputs=true
evidence_artifacts: run_receipt=true; counters=products_processed, categories_extracted
upstream_job_ids: TBD
downstream_job_ids: matching_proposals, category_mapping_to_canonical
status: active
last_reviewed: 2026-01-30
```

**Note**: Actual representation format (table, YAML, JSON) is an implementation detail of the job inventory catalog tool. This schema defines the semantic content, not the presentation format.

---

## 7) Consistency check appendix

### 7.1 Documents aligned with

This specification was developed in alignment with:

1. **`docs/context/glossary.md`**: Used canonical definitions for job_id, artifact_id, TBD, NONE, breaking change, evidence
2. **`docs/context/development_approach.md`**: Aligned with 5-step workflow and evidence discipline
3. **`docs/context/documentation_system_catalog.md`**: Positioned as normative standard (not catalog implementation or per-job content)
4. **`docs/process/workflow_guide.md`**: Supported Step 5 validation and documentation requirements
5. **`docs/standards/naming_standard.md`**: Referenced for job_id format, parameter naming, and breaking change rules
6. **`docs/standards/job_manifest_spec.md`**: Used as authoritative source for manifest field semantics and placeholder rules
7. **`docs/standards/artifacts_catalog_spec.md`**: Referenced for artifact_id format and placeholder normalization
8. **`docs/standards/documentation_spec.md`**: Followed metadata header and formatting requirements

### 7.2 Conflicts detected

**None detected**. The following potential overlaps were reviewed and resolved:

- **With job_manifest_spec.md**: This spec references manifest fields as sources but does not redefine them. Clear boundary: manifest spec defines interface contracts; this spec defines inventory entry schema.
- **With naming_standard.md**: This spec references naming rules but does not duplicate them. Clear boundary: naming standard defines identifier formats; this spec defines where identifiers appear in entries.
- **With artifacts_catalog_spec.md**: This spec uses artifact_id as a reference type but does not define artifact catalog entry structure. Clear boundary: artifact catalog spec defines artifact contracts; this spec defines how jobs reference artifacts.

### 7.3 Boundaries enforced

This specification explicitly avoids:

1. **Catalog file structure**: Does not define section headings, dependency link format, or verification items structure for `docs/catalogs/job_inventory.md` (implementation concern)
2. **Derivation algorithms**: Does not specify step-by-step procedures for extracting entry values from manifests (tooling concern; see `docs/ops/tooling_reference.md`)
3. **Tool command syntax**: Does not include validation commands or regeneration tool usage (see `docs/ops/tooling_reference.md`)
4. **Per-job business logic**: Does not define job-specific requirements or domain rules (see business job descriptions)
5. **Implementation details**: Does not describe job code structure or runtime behavior (see script cards)

### 7.4 Design decisions

This section documents design decisions made during specification development.

**Decision 1: Multi-repository artifact linking**
- **Question**: How to represent artifacts consumed from or produced to external repositories
- **Current scope**: This specification assumes all artifacts are in a single repository's artifact catalog
- **Decision**: Maintain single-repo assumption until multi-repo need is proven (2026-01-30)
- **Rationale**: 
  - No current evidence of multi-repo artifact dependencies in the repository
  - Adding multi-repo support now would introduce unnecessary complexity
  - Schema can be extended later if requirement emerges (via optional `external_source` field or qualified artifact_id format)
- **Future extension path**: If multi-repo linking becomes necessary, add as non-breaking schema extension without modifying existing single-repo entries

**Decision 2: Artifact version tracking in entries**
- **Question**: Whether entries should reference specific artifact versions or schemas
- **Current approach**: Entries reference artifact_id without version information
- **Decision**: Maintain version-agnostic references (2026-01-30)
- **Rationale**:
  - Artifact catalog is responsible for documenting artifact schemas and versions
  - Job inventory entries describe stable interface contracts, not versioned artifacts
  - Separates concerns: inventory tracks "what artifacts", catalog tracks "what's in artifacts"
  - Reduces maintenance burden (entries don't need updates when artifact schemas evolve compatibly)
- **Breaking change handling**: If artifact versions introduce breaking changes, handle via artifact catalog migration procedures (dual-write, deprecation) rather than versioning in inventory entries

### 7.5 Verification notes

**Evidence sources checked**:
- Current `job_inventory_spec.md` (v1.4) reviewed for completeness
- Repository contains 4 jobs under `jobs/vendor_input_processing/` verified by file system scan
- Existing job inventory file at `docs/catalogs/job_inventory.md` reviewed (currently empty template)

**Standards consistency**:
- All field names match glossary definitions
- All references to other specs use correct section numbers (verified 2026-01-30)
- No shadow specifications introduced (standards referenced, not duplicated)

**Completeness check**:
- All 16 required fields defined with semantics
- All enum values specified
- All unknown/empty markers defined
- Placeholder handling delegated to authoritative specs
- Breaking change rules aligned with governance requirements

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-01-30 | Resolved TBD entries: Approved single-repo assumption (Decision 1) and version-agnostic artifact references (Decision 2) per recommended options |
| 2.0 | 2026-01-30 | Complete rework: Focused on normative entry schema; removed catalog file structure details; clarified boundaries; added consistency check appendix; referenced authoritative specs for placeholder/naming rules |
| 1.4 | (prior) | Previous version: Combined entry schema with catalog file structure and derivation procedures |


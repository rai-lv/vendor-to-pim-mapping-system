# Script Card Specification

## Purpose

This standard defines the normative structure for **operational job documentation** ("script cards"), focusing on runtime behavior, invariants, failure modes, and observability. It ensures consistent operational clarity across jobs without mixing business rationale or duplicating contract rules.

## 0) Scope

### What a script card documents

A **script card** documents **one executable job** from an operational perspective:

- What happens when the job runs (runtime behavior at a high level)
- Properties that must always hold (invariants)
- Expected ways the job can fail and how failures surface (failure modes)
- What observability signals exist conceptually (logs, metrics, receipts)

A script card is an **operational + interface reference** that enables operators and developers to understand and troubleshoot job execution.

### What a script card is NOT

A script card is NOT:

- A business justification or rationale document (belongs in business job description)
- A full artifact schema or contract definition (belongs in artifacts catalog spec)
- A tool manual or "how to run" guide (belongs in ops documentation)
- A code walkthrough or implementation detail document
- A global glossary (belongs in `docs/context/glossary.md`)

---

## 1) Relationship to Other Documentation

### Separation from business descriptions

**Business job descriptions** (`bus_description_<job_id>.md`) answer:
- WHY does this job exist? (business purpose)
- WHAT business problem does it solve? (scope and boundaries)
- WHAT business rules govern its behavior? (decision logic from business perspective)

**Script cards** answer:
- HOW does the job behave at runtime? (execution behavior)
- WHAT must always be true? (invariants)
- HOW does it fail? (failure modes and detection)
- WHAT signals does it produce? (observability)

**Boundary rule:** A script card MUST NOT include business justification, scope rationale, or "why it exists" content. If that context is essential, it belongs in the business description with a cross-reference from the script card.

### Separation from artifact contracts

**Artifacts catalog** (`docs/catalogs/artifacts_catalog.md`) and its governing spec (`docs/standards/artifacts_catalog_spec.md`) define:
- Artifact identity (artifact_id, file patterns, S3 locations)
- Artifact content contracts (format, structure, validation rules)
- Producer/consumer relationships

**Script cards** reference artifacts but MUST NOT:
- Define artifact schemas or content contracts (belongs in artifacts catalog)
- Duplicate location patterns or format definitions
- Redefine artifact identities

**Interface rule:** Script cards list inputs and outputs with **meaning** (short human description) and **reference to artifact_id**. Detailed contract information lives in the artifacts catalog.

### Separation from operational runbooks

**Operational reference docs** (`docs/ops/`) define:
- Tool command syntax and parameters
- Deployment procedures
- Troubleshooting guides and runbooks

**Script cards** describe **what observability signals exist** (conceptually) but MUST NOT:
- Include CLI commands to query logs or metrics
- Provide troubleshooting procedures
- Embed deployment instructions

**Observability rule:** Script cards describe what logs/metrics/receipts are expected and what they indicate. How to access them lives in ops documentation.

---

## 2) Required Sections (Normative)

Every script card MUST contain the following sections in order. Each section's requirements are specified below.

### 2.1 Identity (MUST)

**Purpose:** Uniquely identifies the job and its technical metadata.

**Required fields:**

| Field | Description | Allowed values | Example |
|-------|-------------|----------------|---------|
| `job_id` | Repository folder identifier | Must match folder name | `preprocessIncomingBmecat` |
| `glue_job_name` | AWS Glue job name (if applicable) | Exact name or `TBD` | `preprocessIncomingBmecat` |
| `runtime` | Execution runtime | `pyspark`, `python_shell`, `aws_lambda`, `make`, `other`, `TBD` | `pyspark` |
| `repo_path` | Path to entry script | Relative from repo root | `jobs/vendor_input_processing/preprocessIncomingBmecat/glue_script.py` |
| `manifest_path` | Path to job manifest | Relative from repo root | `jobs/vendor_input_processing/preprocessIncomingBmecat/job_manifest.yaml` |

**Format:** Bullet list.

**Pass criterion:** All five fields present and non-empty; `TBD` allowed only where stated.

**Rationale:** These fields enable deterministic job discovery and traceability to source artifacts.

---

### 2.2 Purpose (MUST)

**Purpose:** Brief operational summary of what the job does.

**Requirements:**
- 1–3 sentences describing what the job produces or changes (outputs and/or side effects)
- At least one explicit reference to output(s) or side effect(s)
- Focus on **observable outcomes**, not business intent

**Pass criterion:** 1–3 sentences; contains explicit reference to outputs/side effects.

**Example (compliant):**
> "Preprocesses incoming BMEcat XML files, validates structure, and writes normalized JSON output to S3. Produces one JSON file per input XML. Deletes successfully processed input files."

**Example (non-compliant):**
> "Supports the vendor integration pipeline by handling BMEcat processing." ❌ (too vague, no outputs/side effects mentioned)

---

### 2.3 Trigger and Parameters (MUST)

**Purpose:** Documents how the job is invoked and what parameters it requires.

**Required subfields:**

| Subfield | Description | Allowed values |
|----------|-------------|----------------|
| `Triggered by` | Invocation mechanism | Text description or `TBD` |
| `Required parameters` | Parameter names (comma-separated) | Parameter names or `TBD` |
| `Preconditions` | Required state before execution | Text description or `TBD` |

**Format:** Bullet list with subfields.

**Pass criterion:** All three subfields present; if parameters are known they must be listed as **names only** (no inline descriptions).

**Note:** Parameter semantics are documented in the job manifest. The script card references them by name only.

---

### 2.4 Interface: Inputs (MUST)

**Purpose:** Documents S3 artifacts consumed by the job.

**Required blocks:** At least one input block MUST be present.

**Per-input block fields:**

| Field | Description | Allowed values | Example |
|-------|-------------|----------------|---------|
| `artifact_id` | Reference to artifacts catalog entry | Artifact ID or `TBD` | `external__vendor_bmecat_xml` |
| `bucket` | S3 bucket | Bucket name or placeholder or `TBD` | `vendor-input-raw` |
| `key_pattern` | S3 key pattern | Pattern with placeholders or `TBD` | `vendors/${vendor_name}/bmecat/*.xml` |
| `format` | File format | Format string or `TBD` | `xml` |
| `required` | Whether input is mandatory | `true`, `false`, `TBD` | `true` |
| `meaning` | Short human description | Text | `Vendor product catalog in BMEcat format` |

**Format:** One block per input; fields presented as bullet list or compact table.

**Pass criterion:** Each input block contains all six fields.

**Cross-reference rule:** If `artifact_id` is known, it MUST match an entry in `docs/catalogs/artifacts_catalog.md`. Do NOT redefine artifact contracts here.

---

### 2.5 Interface: Outputs (MUST)

**Purpose:** Documents S3 artifacts produced by the job.

**Required blocks:** At least one output block MUST be present.

**Per-output block fields:**

| Field | Description | Allowed values | Example |
|-------|-------------|----------------|---------|
| `artifact_id` | Reference to artifacts catalog entry | Artifact ID or `TBD` | `preprocessIncomingBmecat__normalized_vendor_products` |
| `bucket` | S3 bucket | Bucket name or placeholder or `TBD` | `vendor-input-processed` |
| `key_pattern` | S3 key pattern | Pattern with placeholders or `TBD` | `preprocessed/${vendor_name}/products.json` |
| `format` | File format | Format string or `TBD` | `json` |
| `required` | Whether output is always written | `true`, `false`, `TBD` | `true` |
| `meaning` | Short human description | Text | `Normalized vendor products in JSON format` |
| `consumers` | Downstream jobs or systems | Job IDs (comma-separated) or `TBD` or `NONE` | `matching_proposals` |

**Format:** One block per output; fields presented as bullet list or compact table.

**Pass criterion:** Each output block contains all seven fields.

**Cross-reference rule:** If `artifact_id` is known, it MUST match an entry in `docs/catalogs/artifacts_catalog.md`. Do NOT redefine artifact contracts here.

---

### 2.6 Side Effects (MUST)

**Purpose:** Documents job behaviors that modify S3 state beyond declared outputs.

**Required subfields:**

| Subfield | Description | Allowed values | Example |
|----------|-------------|----------------|---------|
| `deletes_inputs` | Whether job deletes input objects | `true`, `false`, `TBD` | `true` |
| `overwrites_outputs` | Whether job overwrites existing outputs | `true`, `false`, `TBD` | `true` |
| `other_side_effects` | Other state modifications | Text description or `TBD` | `Updates metadata in DynamoDB table` |

**Format:** Bullet list with subfields.

**Pass criterion:** All three subfields present.

**Semantic note:** Side effects are critical for orchestration and recovery logic. Mark as `TBD` only if truly unknown; investigate code if possible.

---

### 2.7 Runtime Behavior (MUST)

**Purpose:** High-level description of what the job does during execution.

**Requirements:**
- 4–8 bullets describing the job's high-level steps
- Bullets MUST be phrased as **actions** (verb-first)
- Bullets MUST NOT include implementation details (function names, column names, code-level branches) unless essential to understand external behavior

**Pass criterion:** 4–8 bullets; action phrasing; no code-level detail.

**Example (compliant):**
> - Reads BMEcat XML file from S3
> - Validates XML structure against BMEcat schema
> - Extracts product records and normalizes field names
> - Writes normalized JSON output to S3
> - Deletes successfully processed input file
> - Logs summary statistics (product count, validation errors)

**Example (non-compliant):**
> - Calls `parse_bmecat()` function ❌ (implementation detail)
> - Iterates over `product_list` array and checks `if article_id is not None` ❌ (code-level detail)

---

### 2.8 Invariants (MUST)

**Purpose:** Documents properties that must always hold true, regardless of inputs or runtime conditions.

**Requirements:**
- Either:
  - A list of 1+ invariants, OR
  - A single bullet: `- TBD`
- Any stated invariant MUST be **externally meaningful** (observable behavior, not internal algorithm statements)

**Pass criterion:** Section present with either ≥1 invariant or exactly `- TBD`.

**Example (compliant):**
> - Always writes exactly one output file per input file (1:1 mapping)
> - Output file is always valid JSON (parseable as JSON object or array)
> - If input count is zero, output bucket remains unchanged (no empty files written)
> - Job never partially processes an input (atomic: success or rollback)

**Example (non-compliant):**
> - Uses efficient hash map for lookups ❌ (internal implementation, not externally observable)

---

### 2.9 Failure Modes and Observability (MUST)

**Purpose:** Documents how the job fails and what observability signals exist.

**Required subfields:**

| Subfield | Description | Content guidance | Example |
|----------|-------------|------------------|---------|
| `Failure conditions (as coded)` | Explicit failure conditions in code | Text description of exit codes, exceptions, or `TBD` | `Exits with code 1 if XML validation fails; raises ValueError if required field missing` |
| `Logging/metrics (as coded)` | What logs/metrics are emitted | Conceptual description (not CLI commands) or `TBD` | `Logs INFO for each file processed; logs ERROR for validation failures; emits CloudWatch metric for product count` |
| `Run receipt` | Whether structured run receipt is written | `true`, `false`, `TBD`, or brief description | `Writes run_receipt.json to S3 with timestamp, input/output counts, errors` |
| `Operator checks` | What S3 artifacts operators should verify | Text description or `TBD` | `Verify output file exists in processed bucket; check run_receipt.json for errors=0` |

**Format:** Bullet list with subfields.

**Pass criterion:** All four subfields present.

**Observability guideline:** Describe **what signals exist** and **what they indicate**. Do NOT include CLI commands to query logs (belongs in ops docs).

---

### 2.10 References (MUST)

**Purpose:** Links to related documentation and upstream/downstream dependencies.

**Required subfields:**

| Subfield | Description | Example |
|----------|-------------|---------|
| `job_manifest` | Path to job manifest | `jobs/vendor_input_processing/preprocessIncomingBmecat/job_manifest.yaml` |
| `business_description` | Path to business description | `jobs/vendor_input_processing/preprocessIncomingBmecat/bus_description_preprocess_incoming_bmecat.md` |
| `artifacts_catalog_entries` | Artifact IDs referenced | `external__vendor_bmecat_xml, preprocessIncomingBmecat__normalized_vendor_products` or `TBD` |
| `upstream_jobs` | Jobs this job depends on (derived from artifacts catalog) | Job IDs (comma-separated) or `TBD` or `NONE` |
| `downstream_jobs` | Jobs that consume this job's outputs (derived from artifacts catalog) | Job IDs (comma-separated) or `TBD` or `NONE` |

**Format:** Bullet list with subfields.

**Pass criterion:** All five subfields present.

**Cross-reference rule:** All paths and identifiers MUST be valid and resolvable within the repository.

**Derivation note (per decision 9.3):** The `upstream_jobs` and `downstream_jobs` fields are **derived fields** computed automatically from the artifacts catalog (producer/consumer relationships). Script cards MAY list these for human readability, but the artifacts catalog is the authoritative source. During manual documentation, use `TBD` if the artifacts catalog is incomplete; resolve via catalog updates rather than manual script card maintenance.

---

## 3) Explicit Exclusions (MUST NOT)

A script card MUST NOT:

1. **Define global terms** that apply across multiple jobs → Belongs in glossary (`docs/context/glossary.md`)

2. **Provide full JSON schema or field-by-field structure of outputs** → Belongs in artifacts catalog (`docs/catalogs/artifacts_catalog.md`) and its spec

3. **Include business justification or rationale** → Belongs in business job description

4. **Propose future improvements or refactors** → Phase 1 documentation is descriptive, not prescriptive

5. **Include speculative statements** → If unknown, use `TBD`

6. **Embed CLI commands, troubleshooting procedures, or deployment instructions** → Belongs in ops documentation (`docs/ops/`)

7. **Redefine artifact contracts or location patterns** → Belongs in artifacts catalog; script cards reference only

**Rationale:** These exclusions prevent "double truth" and maintain clear separation of concerns across the documentation system.

---

## 4) Optional Sections

### 4.1 Known Limitations (OPTIONAL)

**When to include:** When there are known operational limitations that affect job behavior (e.g., max file size, known edge cases not handled).

**Format:** Bullet list.

**Example:**
> - Does not handle BMEcat files larger than 500MB (memory constraint)
> - Skips products with missing `article_id` field (logs warning but continues)

### 4.2 Dependencies (OPTIONAL)

**When to include:** When the job has external dependencies not captured in inputs/outputs (e.g., DynamoDB tables, external APIs).

**Format:** Bullet list.

**Example:**
> - Requires read access to DynamoDB table `vendor_metadata`
> - Requires network access to validate XML against external BMEcat schema URL

---

## 5) Formatting and Structure Rules

### 5.1 File naming and location

**Canonical location:** `jobs/<job_group>/<job_id>/script_card_<job_id>.md`

**Alternative location (if per-job docs are centralized):** `docs/jobs/<job_id>/script_card_<job_id>.md`

**Naming convention:** `script_card_<job_id>.md` where `<job_id>` matches the job folder name and manifest `job_id` field.

### 5.2 Markdown structure

- Use heading hierarchy correctly (H1 → H2 → H3; do not skip levels)
- H1: `# Script Card: <job_id>`
- H2: Major sections (Identity, Purpose, Interface, etc.)
- H3: Optional subsections within major sections
- Use bullet lists for field lists (not tables, unless compact tables improve readability for inputs/outputs)
- Use code blocks (triple backticks) for examples, not inline code spans

### 5.3 Placeholder representation

When documenting patterns with placeholders (e.g., S3 key patterns):
- Use the format: `${placeholder_name}`
- Examples: `${vendor_name}`, `${execution_date}`
- Reference the naming standard for placeholder conventions: `docs/standards/naming_standard.md`

### 5.4 TBD discipline

- Use `TBD` for unknown values (not `TODO`, `UNKNOWN`, or `???`)
- When using `TBD`, add a note explaining why the value is unknown and what would be needed to resolve it
- Do NOT use `TBD` as a permanent placeholder; it signals work remaining

### 5.5 Cross-references

- Use relative paths from repository root (not absolute URLs for internal documents)
- Format: `docs/context/glossary.md` (not `/docs/context/glossary.md` or full GitHub URLs)
- Verify cross-references are valid and resolvable

---

## 6) Compatibility and Breaking Changes

### 6.1 What constitutes a breaking change to script card structure

The following changes to this specification are **breaking changes** requiring governance approval and migration plan:

- Removing a required section (2.1–2.10)
- Renaming a required field (e.g., `job_id` → `job_identifier`)
- Changing field semantics (e.g., `runtime` allowed values)
- Changing section ordering requirements

### 6.2 Non-breaking changes

The following changes are **non-breaking**:

- Adding optional sections (e.g., new section 4.3)
- Clarifying field descriptions without changing semantics
- Adding examples or guidance
- Fixing typos or improving readability

### 6.3 Versioning approach

This specification follows the repository's versioning discipline:
- Changes are tracked via git history (commits, tags)
- No explicit version numbers in document metadata
- Breaking changes are announced and linked from the documentation system catalog

---

## 7) Enforcement and Validation

### 7.1 Validation approach

Script cards MAY be validated using automated tooling that checks:
- Presence of all required sections (2.1–2.10)
- Presence of all required fields within sections
- Cross-reference validity (paths, artifact_ids, job_ids)
- TBD count and distribution (high TBD count may signal incomplete documentation)

**Scope of automated validation (per decision 9.2):**
- Automated tooling enforces **presence/absence** of sections and fields
- Automated tooling does NOT enforce **field cardinality** (e.g., "4–8 bullets", "1–3 sentences")
- Cardinality requirements remain normative for human review but are not enforced by tooling

### 7.2 Human review checkpoints

Before approving a script card, reviewers SHOULD verify:
- Operational clarity: Can an operator understand how to verify job success/failure?
- No business rationale mixed in (belongs in business description)
- No artifact contract duplication (belongs in artifacts catalog)
- No tool commands embedded (belongs in ops docs)
- Cross-references are valid and necessary

### 7.3 Relationship to validation standard

This spec defines the **structure** of script cards. The **validation standard** (`docs/standards/validation_standard.md`) defines:
- What "verified" means
- What evidence is acceptable
- Pass/fail semantics

Script cards document observability signals; the validation standard governs how those signals are used for approval decisions.

---

## 8) Migration Guidance (For Existing Script Cards)

### 8.1 If upgrading from the previous version

The previous version of this spec (as of 2026-01-30) included similar sections but with less clarity on boundaries and exclusions. When migrating:

1. **Add cross-references:** Ensure `business_description` is listed in References section
2. **Remove business rationale:** Move "why it exists" content to business description
3. **Remove artifact schemas:** Move detailed content contracts to artifacts catalog
4. **Add artifact_id fields:** Reference artifacts catalog entries by artifact_id
5. **Clarify observability:** Separate what signals exist (script card) from how to query them (ops docs)

### 8.2 Handling TBDs during migration

When documenting existing jobs retroactively:
- Use `TBD` for values that cannot be determined from code analysis or operational knowledge
- Prioritize filling in identity, interface, and failure modes (sections critical for operations)
- Document what is known first; iterate to resolve TBDs over time

---

## 9) Resolved Design Decisions

This section documents design decisions made for this specification.

### 9.1 Run receipt format standardization

**Question:** Should script cards reference a standard run receipt schema, or is per-job variation acceptable?

**Decision (2026-01-30):** Accept per-job variation for now.

**Rationale:** 
- No standard run receipt schema currently exists across jobs
- Forcing standardization would block documentation of existing jobs
- Per-job variation allows operational documentation to proceed without waiting for cross-job schema alignment

**Implementation:**
- Script cards document whether a run receipt exists and what it contains conceptually (Section 2.9)
- No requirement to conform to a standard schema
- If a standard run receipt spec is introduced later, it may be referenced but is not mandatory

### 9.2 Validation tooling scope

**Question:** Should validation tooling enforce field cardinality (e.g., "at least 4 runtime behavior bullets"), or only presence/absence of sections?

**Decision (2026-01-30):** Validation tooling should enforce only presence/absence of sections, not field cardinality.

**Rationale:**
- Cardinality requirements (e.g., "4–8 bullets") remain normative for human review
- Automated enforcement of cardinality would be overly rigid for edge cases
- Presence/absence checking provides structural validation without constraining legitimate variation
- Human reviewers can assess whether content meets quality expectations

**Implementation:**
- Automated tooling validates: section presence, required field presence, cross-reference validity
- Automated tooling does NOT validate: bullet counts, sentence counts, word limits
- Human review remains essential for operational clarity and quality (Section 7.2)

### 9.3 Cross-job dependency representation

**Question:** Should `upstream_jobs` and `downstream_jobs` be derived automatically from artifacts catalog, or manually maintained in script cards?

**Decision (2026-01-30):** Automatic derivation from single source (artifacts catalog).

**Rationale:**
- Prevents inconsistency between script cards and job inventory
- Artifacts catalog is the authoritative source of producer/consumer relationships
- Manual maintenance in script cards would create "double truth"
- Aligns with "single source per contract type" principle

**Implementation:**
- `upstream_jobs` and `downstream_jobs` fields in Section 2.10 are **derived fields**
- Values are computed automatically from artifacts catalog (producer/consumer relationships)
- Script cards MAY list these for human readability, but they are not authoritative
- Tooling should generate or validate these fields against artifacts catalog
- During manual documentation, use `TBD` if artifacts catalog is incomplete; resolve via catalog updates

---

## Consistency Check Appendix

### Documents aligned with

This reworked script card specification aligns with:

1. **Development Approach** (`docs/context/development_approach.md`)
   - Supports 5-step execution model (script cards are part of Step 5 documentation)
   - Respects human approval gates and evidence discipline
   - Maintains separation between agents (who draft) and tools (which enforce)

2. **Documentation System Catalog** (`docs/context/documentation_system_catalog.md`)
   - Conforms to definition of "Script Card Spec" (document type #13)
   - Canonical location: `docs/standards/` ✓
   - Purpose: Operational job documentation structure ✓
   - Exclusions: No business rationale, no artifact contracts, no tool commands ✓

3. **Glossary** (`docs/context/glossary.md`)
   - Uses terms consistently: job_id, artifact_id, runtime, TBD, side effects, invariants
   - Does not redefine glossary terms ✓
   - References glossary for shared term meanings ✓

4. **Target Agent System** (`docs/context/target_agent_system.md`)
   - Supports agent-assisted documentation (agents can draft, humans approve)
   - Enforces "single source per contract type" principle
   - Prevents "double truth" by explicit exclusions
   - Maintains layer separation (operational vs business vs contracts)

5. **Workflow Guide** (`docs/process/workflow_guide.md`)
   - Script cards are created/updated in Step 5 (Validate, test, and document)
   - Supports evidence-based claims (observability section enables validation)
   - Respects approval gates (script cards document "what is", not "what should be")

6. **Artifacts Catalog Spec** (`docs/standards/artifacts_catalog_spec.md`)
   - References artifact_id as canonical identifier ✓
   - Does not duplicate artifact contract definitions ✓
   - Maintains clear boundary: script cards reference, artifacts catalog defines

7. **Job Manifest Spec** (`docs/standards/job_manifest_spec.md`)
   - Uses consistent field names: glue_job_name, runtime, parameters, inputs, outputs, side_effects
   - References manifests as source of truth for interface facts
   - Avoids duplicating manifest schema

8. **Naming Standard** (`docs/standards/naming_standard.md`)
   - Uses snake_case for job_id, artifact_id ✓
   - Uses placeholder format `${placeholder_name}` ✓
   - Follows file naming conventions ✓

9. **Documentation Spec** (`docs/standards/documentation_spec.md`)
   - Follows foundational principles: single source of truth, separation of concerns, evidence-based claims, explicit over implicit ✓
   - Respects layer architecture (this is a standards doc, not context or ops) ✓
   - Uses proper heading hierarchy ✓
   - Includes versioning approach aligned with git-based versioning ✓

### Conflicts detected

**None.** This reworked specification is consistent with all reviewed documentation.

### Resolved design decisions

Three design decisions documented in Section 9 (resolved 2026-01-30):

1. **Run receipt format (9.1):** Accept per-job variation. No standard schema enforced.
2. **Validation tooling scope (9.2):** Automated validation enforces presence/absence only, not field cardinality.
3. **Dependency representation (9.3):** `upstream_jobs` and `downstream_jobs` are derived fields computed from artifacts catalog (single source).

These decisions align with:
- Documentation system principles (single source of truth, evidence-based, no double truth)
- Practical constraints (no standard run receipt schema exists yet)
- Enforcement philosophy (automated structure checking, human quality review)

### Assumptions introduced

1. **Assumption:** Script cards are primarily written retroactively (after job implementation) or updated during Step 5 (Validate, test, and document).
   - **Bounded:** Applies to timing of script card creation.
   - **Why:** The spec focuses on describing "what is" (runtime behavior, invariants) rather than "what should be" (intent, requirements).
   - **Impact:** If script cards are needed prospectively (during Step 3 capability planning), additional guidance may be needed for handling unknowns.
   - **Approval status:** Marked as assumption; not yet approved.

2. **Assumption:** Per-job script cards are co-located with job folders (`jobs/<job_group>/<job_id>/`) rather than centralized in `docs/jobs/`.
   - **Bounded:** Applies to file location only.
   - **Why:** Follows pattern observed for business descriptions. Documentation System Catalog lists alternative location as acceptable.
   - **Impact:** Tools and validation must support both locations. Cross-references must use full paths.
   - **Approval status:** Marked as assumption; both locations are acceptable per catalog.

### What was deliberately excluded to avoid double truth

1. **Artifact contract schemas:** These belong in `docs/standards/artifacts_catalog_spec.md` and `docs/catalogs/artifacts_catalog.md`. Script cards reference artifact_id only.

2. **Business rationale and scope boundaries:** These belong in business job descriptions (`bus_description_<job_id>.md`). Script cards focus on operational behavior.

3. **Tool command syntax:** CLI commands, troubleshooting procedures, and runbooks belong in `docs/ops/`. Script cards describe what observability signals exist, not how to query them.

4. **Job manifest schema:** The schema is defined in `docs/standards/job_manifest_spec.md`. Script cards reference manifest fields by name only.

5. **Glossary definitions:** Shared terms are defined once in `docs/context/glossary.md`. Script cards use those terms consistently without redefining them.

6. **Validation rules and evidence expectations:** These belong in `docs/standards/validation_standard.md`. Script cards document observability signals that enable validation, but do not define what "verified" means.

### Cross-document impact notes

1. **Business Job Description Spec** (`docs/standards/business_job_description_spec.md`)
   - Should clarify boundary with script cards (business vs operational)
   - May need to reference script card spec in Section 0 (Scope)
   - **Action required:** Add cross-reference from business description spec to script card spec

2. **Job Inventory Spec** (`docs/standards/job_inventory_spec.md`)
   - Job inventory derives some fields from manifests and artifacts catalog
   - Script cards provide human-readable operational context
   - **Impact:** No changes needed; script cards are complementary

3. **Documentation System Catalog** (`docs/context/documentation_system_catalog.md`)
   - Entry #27 (Per-job Script Card) description should be updated to match this spec
   - **Action required:** Update catalog entry to reference this spec's refined purpose statement

4. **Ops Documentation** (`docs/ops/tooling_reference.md`, `docs/ops/ci_automation_reference.md`)
   - Should reference script cards as source of "what signals exist"
   - Ops docs provide "how to query/interpret" those signals
   - **Impact:** No changes needed; boundary is clear

### Notes on finalization

This specification has been reviewed and decisions made for previously open items (see Section 9). Key review checkpoints:

1. **Boundary clarity:** Are the exclusions (Section 3) clear and enforceable?
2. **Required sections:** Are sections 2.1–2.10 the right balance of completeness vs. simplicity?
3. **Design decisions:** Section 9 documents resolved decisions for run receipt format, validation tooling scope, and dependency derivation.
4. **Migration guidance:** Is Section 8 sufficient for upgrading existing script cards?

**Approval gate:** This spec requires explicit human approval before being used to validate or generate script cards.

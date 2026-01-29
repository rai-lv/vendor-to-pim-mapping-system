# Naming Standard (v2.0)

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines naming rules for jobs, artifacts, identifiers, and placeholders to ensure stability and automation.
**Why necessary:** Prevents drift and enables consistent validation and tooling.
**Must contain:** Naming conventions; identifier rules; compatibility expectations.
**Must not contain:** Tool instructions or job-specific business logic.

**Last Updated:** 2026-01-29
**Version:** 2.0

---

## 1) Purpose Statement

This standard governs the naming conventions for repository elements that are referenced by automation, validation tools, and cross-job integration. It exists to:

- Ensure **naming stability** for machine-readable identifiers (job IDs, artifact IDs, placeholders),
- Enable **deterministic validation** and **automated discovery**,
- Prevent **naming drift** that breaks tooling or causes ambiguity,
- Support **human readability** while maintaining consistency.

### What this standard does NOT cover

- Job-specific business logic or domain rules (belongs in business job descriptions)
- Tool command syntax or operational procedures (belongs in ops layer)
- Data content schema or artifact contracts (belongs in artifact catalog spec)
- Deployment-specific naming transforms (e.g., environment prefixes like `prod-{job_id}`)
- **Temporary or intermediate artifacts** (within a job, not cross-job) that are:
  - Not declared in job manifests (inputs/outputs/config_files)
  - Not consumed by other jobs
  - Ephemeral (deleted before job completion or managed with S3 lifecycle policies)
  - Examples: checkpoint files, intermediate transforms, debug outputs, job-internal cache files

---

## 2) Scope and Applicability

This standard applies to the following object classes:

1. **Job identifiers** (`job_id`): the canonical name for a job, used in folder structure, manifests, and deployment
2. **Job group identifiers** (`job_group`): the organizational grouping within `jobs/` directory
3. **Script filenames**: the entrypoint scripts within job folders
4. **Repository artifact identifiers**: filenames for shared outputs consumed by multiple jobs
5. **Document identifiers**: filenames for standards, process docs, context docs, and per-job documentation
6. **Placeholder names**: template variables used in job manifests and specs (e.g., `${vendor_name}`)
7. **Parameter names**: job invocation parameters declared in manifests

### Exceptions policy

Job-specific naming exceptions are **not allowed** unless explicitly documented in a decision record and referenced in the job's manifest notes. All naming must conform to this standard to enable consistent automation.

---

## 3) General Naming Rules (Global)

These rules apply to all naming across the repository unless explicitly overridden by entity-specific rules in Section 4.

### 3.1 Allowed character set

**MUST:**
- Use only alphanumeric characters (`a-z`, `A-Z`, `0-9`) and underscores (`_`) or hyphens (`-`)
- Start with a letter (not a number or special character)
- NOT use spaces, dots (except file extensions), or special characters (`@`, `#`, `$`, `%`, `&`, `*`, etc.)

**Exceptions:**
- File extensions (`.py`, `.yaml`, `.md`, `.json`) are allowed
- Placeholder delimiters (`${...}`) follow their own rules (see 4.6)

### 3.2 Casing conventions

**Default convention: snake_case**
- Use lowercase letters with underscores as separators
- Applies to: job IDs, job groups, artifact filenames, parameter names (when lowercase), placeholders (when lowercase), document filenames

**Alternate convention: camelCase**
- Start with lowercase, capitalize first letter of subsequent words
- Applies to: legacy job IDs (see Section 4.1 for migration guidance)

**Alternate convention: UPPER_SNAKE_CASE**
- All uppercase with underscores
- Applies to: AWS Glue system parameters (`JOB_NAME`, `INPUT_BUCKET`, `OUTPUT_BUCKET`)

**Rule (MUST):**
- Each entity type has a specified casing convention (see Section 4)
- Do NOT mix casing within a single identifier (e.g., `myJob_ID` is forbidden)

### 3.3 Separators

- For snake_case: use underscore (`_`) only
- For camelCase: no separators; use capitalization to mark word boundaries
- For kebab-case: use hyphen (`-`) only (currently not used; reserved for future)

### 3.4 Length guidance

**Recommendations (SHOULD):**
- Keep identifiers under 64 characters for human readability
- Prefer descriptive names over abbreviations (e.g., `vendor_products` over `vp`)
- Job IDs: typically 15-40 characters

**Hard limits (MUST):**
- All identifiers MUST be under 256 characters (filesystem/S3 constraint)
- Parameter names: under 128 characters (AWS Glue constraint)

### 3.5 Reserved words

**MUST NOT use as standalone identifiers:**
- AWS Glue reserved parameters: `JOB_NAME`, `JOB_RUN_ID`, `TempDir`, `scriptLocation`
- Python reserved keywords: `class`, `def`, `import`, `for`, `if`, `while`, etc.
- Common system terms: `temp`, `tmp`, `cache`, `log`, `test` (when used alone; compound names like `test_results` are acceptable)

### 3.6 Stability expectations

**MUST:**
- Once an identifier is deployed and referenced by automation or other jobs, it MUST NOT be renamed casually
- Renaming requires explicit approval and a breaking change decision record
- Identifiers used in manifests, artifact catalogs, or job inventory are considered **stable contracts**

**Compatibility rule:**
- If an identifier must change, provide a deprecation period with aliasing or migration guidance
- Breaking changes require explicit governance approval (see Section 5)

---

## 4) Naming Conventions by Entity Type

### 4.1 Job IDs

#### Definition
A `job_id` is the canonical identifier for a job. It serves as:
- The folder name under `jobs/<job_group>/`
- The `job_id` field value in `job_manifest.yaml`
- The `glue_job_name` field value in `job_manifest.yaml`
- The deployed AWS Glue job name (base name, without environment prefixes)

#### Format rule (MUST)

**Casing:** snake_case (lowercase with underscores)

**Pattern:** `^[a-z][a-z0-9_]{2,62}$`
- Starts with a lowercase letter
- Contains lowercase letters, digits, and underscores
- Length: 3-63 characters

**Consistency rule (normatively defined in `job_manifest_spec.md` Section 2.2):**
- `job_id` (manifest field) = folder name = `glue_job_name` (manifest field)
- This is a 1:1:1 mapping with no exceptions

#### Examples

**Valid (snake_case - current standard):**
- `matching_proposals`
- `category_mapping_to_canonical`
- `mapping_method_training`
- `preprocess_incoming_bmecat`
- `generate_vendor_report`

**Valid (legacy camelCase - grandfathered):**
- `preprocessIncomingBmecat` (existing job; allowed for backward compatibility)

**Invalid:**
- `PreprocessIncomingBmecat` (PascalCase; should start lowercase)
- `preprocess-incoming-bmecat` (kebab-case; not allowed)
- `preprocessIncomingBMEcat` (mixed casing; inconsistent)
- `p` (too short; under 3 characters)

#### Compatibility expectations

**Current pattern:**
- **snake_case is the standard** for all new jobs (verified against 3 out of 4 existing jobs in `vendor_input_processing`)
- One legacy camelCase job (`preprocessIncomingBmecat`) is grandfathered for backward compatibility

**Stable:**
- Job IDs MUST NOT change after deployment without a breaking change decision
- Renaming a job ID requires updating:
  - Folder name
  - Manifest `job_id` and `glue_job_name` fields
  - All references in artifact catalogs, job inventory, orchestration configs, and downstream dependencies

**Evolving:**
- New jobs MUST use snake_case
- Existing camelCase jobs MAY remain as-is (no forced migration)
- If a camelCase job is renamed for other reasons, it SHOULD be migrated to snake_case

---

### 4.2 Job Groups

#### Definition
A `job_group` is an organizational folder under `jobs/` that groups related jobs by functional area or pipeline stage.

#### Format rule (MUST)

**Casing:** snake_case (lowercase with underscores)

**Pattern:** `^[a-z][a-z0-9_]{2,62}$`
- Starts with a lowercase letter
- Contains lowercase letters, digits, and underscores
- Length: 3-63 characters

#### Examples

**Valid:**
- `vendor_input_processing`
- `process_controls`
- `pim_integration`
- `data_quality_checks`

**Invalid:**
- `VendorInputProcessing` (PascalCase; should be snake_case)
- `vendorInputProcessing` (camelCase; should be snake_case)
- `vendor-input-processing` (kebab-case; not allowed)

#### Compatibility expectations

**Stable:**
- Job group names SHOULD remain stable once established
- Renaming requires updating all job folder paths and references

**Evolving:**
- New job groups may be added
- Jobs may be moved between groups if justified by a refactor decision

---

### 4.3 Script Filenames and Folder Structure

#### Definition
Script filenames are the entrypoint files within job folders, typically Python scripts executed by AWS Glue.

#### Format rule (MUST)

**Primary entrypoint (normatively defined in `job_manifest_spec.md` Section 4.2):**
- Filename: `glue_script.py`
- Location: `jobs/<job_group>/<job_id>/glue_script.py`
- This is the standard entrypoint name; must be declared in manifest `entrypoint` field

**Supporting scripts (if present):**
- Use snake_case: lowercase with underscores
- Pattern: `^[a-z][a-z0-9_]+\.py$`
- Examples: `helpers.py`, `data_transformations.py`, `validation_rules.py`

#### Folder structure identifiers

**Per-job folder pattern:**
- `jobs/<job_group>/<job_id>/`
  - `glue_script.py` (required)
  - `job_manifest.yaml` (required)
  - Supporting scripts (optional)
  - `config/` (optional, for repo-mirrored configs)

**Config subfolder (if used):**
- Name: `config/` (lowercase, no variation)
- Contents: job-local configuration files in JSON, YAML, or other formats

#### Examples

**Valid:**
- `glue_script.py`
- `data_transformations.py`
- `s3_helpers.py`

**Invalid:**
- `GlueScript.py` (PascalCase; should be snake_case)
- `glue-script.py` (kebab-case; not allowed)
- `main.py` (non-standard entrypoint name; use `glue_script.py`)

#### Compatibility expectations

**Stable:**
- `glue_script.py` is the canonical entrypoint name and MUST NOT change
- Supporting script names SHOULD remain stable once referenced by the entrypoint

---

### 4.4 Artifact IDs / Artifact Filenames

#### Definition
Artifact identifiers are filenames for data outputs written to S3 that are consumed by other jobs or systems. These are declared in job manifests under `outputs[]` and registered in the artifacts catalog.

#### Format rule (MUST)

**Casing:** snake_case (lowercase with underscores)

**Pattern:** `^[a-z][a-z0-9_]+\.(json|ndjson|csv|xml|parquet|txt)$`
- Starts with a lowercase letter
- Contains lowercase letters, digits, and underscores (no hyphens)
- Ends with a recognized file extension

**Placeholder integration:**
- Artifact filenames MAY include placeholders (e.g., `${vendor_name}`) for dynamic components
- Placeholders follow rules in Section 4.6
- Static prefix/suffix components use snake_case

**Recommended structure:**
- `<domain>_<entity>_<qualifier>.<extension>`
- Examples: `vendor_products.json`, `category_mappings.csv`, `run_receipt.json`

#### Examples

**Valid:**
- `vendor_products.json`
- `vendor_categories.ndjson`
- `category_mapping_proposals.json`
- `${vendor_name}_vendor_products.json` (with placeholder)
- `product_features_normalized.csv`

**Invalid:**
- `VendorProducts.json` (PascalCase; should be snake_case)
- `vendor-products.json` (kebab-case; not allowed)
- `vendorProducts.json` (camelCase; should be snake_case)
- `products` (no extension)

#### Compatibility expectations

**Stable:**
- Artifact filenames declared in manifests and artifact catalogs are stable contracts
- Changing an artifact filename is a breaking change requiring:
  - Decision record
  - Update to all producers and consumers
  - Migration period with dual-write support (if needed)

**Evolving:**
- New artifact types may be added without affecting existing artifacts
- Additional optional outputs may be added to jobs without breaking changes

---

### 4.5 Documentation Filenames

#### Definition
Documentation filenames identify standards, context docs, process guides, and per-job documentation.

#### Format rule (MUST)

**Casing:** snake_case (lowercase with underscores)

**Extension:** `.md` (Markdown)

**Pattern by document layer:**

**Context layer (`docs/context/`):**
- Pattern: `<concept>_<type>.md`
- Examples: `development_approach.md`, `target_agent_system.md`, `glossary.md`, `system_context.md`

**Standards layer (`docs/standards/`):**
- Pattern: `<domain>_<spec_type>.md` or `<standard_name>.md`
- Examples: `job_manifest_spec.md`, `naming_standard.md`, `validation_standard.md`, `artifact_catalog_spec.md`

**Process layer (`docs/process/`):**
- Pattern: `<process_name>_<guide_type>.md`
- Examples: `workflow_guide.md`, `contribution_approval_guide.md`

**Ops layer (`docs/ops/`):**
- Pattern: `<tool_or_system>_reference.md`
- Examples: `tooling_reference.md`, `ci_automation_reference.md`

**Agent layer (`docs/agents/`):**
- Pattern: `<agent_role>_<type>.md`
- Examples: `agent_role_charter.md`, `agent_tool_interaction_guide.md`

**Catalogs (`docs/catalogs/`):**
- Pattern: `<catalog_name>.md`
- Examples: `job_inventory.md`, `artifacts_catalog.md`, `decision_log.md`

**Per-job docs (`docs/jobs/<job_id>/` or `jobs/<job_group>/<job_id>/`):**
- Business description: `bus_description_<job_id>.md`
- Script card: `script_card_<job_id>.md`
- Examples: `bus_description_preprocessIncomingBmecat.md`, `script_card_matchingProposals.md`

#### Examples

**Valid:**
- `job_manifest_spec.md`
- `workflow_guide.md`
- `agent_role_charter.md`
- `bus_description_preprocessIncomingBmecat.md`

**Invalid:**
- `JobManifestSpec.md` (PascalCase; should be snake_case)
- `workflow-guide.md` (kebab-case; not allowed)
- `workflowGuide.md` (camelCase; should be snake_case)

#### Compatibility expectations

**Stable:**
- Document filenames in the standards and context layers SHOULD remain stable
- Renaming requires updating all cross-references in other documents

**Evolving:**
- New documents may be added following the layer-specific patterns

---

### 4.6 Placeholder Names in Manifests/Specs

#### Definition
Placeholders are template variables used in job manifests to represent runtime-substituted values. They appear in `bucket` and `key_pattern` fields.

**Canonical placeholder format (normatively defined in `job_manifest_spec.md` Section 6.1):**
- `${NAME}` (case-sensitive, no spaces)

#### Format rule (MUST)

**Type 1: Parameter placeholders**
- **Rule:** MUST match the parameter name exactly (character-for-character, case-sensitive)
- **No transformation:** Do NOT apply case conversion
- **Examples:**
  - Parameter `INPUT_BUCKET` → placeholder `${INPUT_BUCKET}`
  - Parameter `vendor_name` → placeholder `${vendor_name}`
  - Parameter `bmecat_input_key` → placeholder `${bmecat_input_key}`

**Type 2: Runtime-generated placeholders**
- **Rule:** SHOULD use snake_case (lowercase with underscores)
- **Examples:** `${run_id}`, `${timestamp}`, `${new_suffix}`
- **Documentation requirement:** MUST be explained in manifest `notes` section

**Type 3: Normalized placeholders (special case, defined in `job_manifest_spec.md` Section 6.4):**
- **Rule:** Use `${X_norm}` suffix to indicate prefix normalization
- **Meaning:** Parameter `X` has been normalized to ensure trailing `/` for S3 prefix operations
- **Examples:** `${bmecat_output_prefix_norm}`, `${prepared_input_key_norm}`
- **When to use:** Only when the script contains explicit normalization logic

#### Placeholder naming rules (MUST)

- Placeholder names are **case-sensitive**
- No spaces allowed inside `${...}`
- No special characters except underscore (`_`)
- Parameter placeholders: exact match to parameter name (including case)
- Runtime placeholders: snake_case convention

#### Examples

**Valid:**
- `${INPUT_BUCKET}` (matches UPPER_SNAKE_CASE parameter)
- `${vendor_name}` (matches snake_case parameter)
- `${bmecat_output_prefix_norm}` (normalized placeholder)
- `${run_id}` (runtime-generated, snake_case)

**Invalid:**
- `${input_bucket}` (if parameter is `INPUT_BUCKET`; case mismatch)
- `${VendorName}` (if parameter is `vendor_name`; case mismatch)
- `${ vendor_name }` (spaces not allowed)
- `{vendor_name}` (wrong delimiter; must be `${...}`)
- `<vendor_name>` (wrong delimiter for manifests; `<...>` is for business docs only)

#### Compatibility expectations

**Stable:**
- Placeholder names are tied to parameter names and MUST remain consistent
- Changing a parameter name requires updating all placeholder references in manifest patterns

**Evolving:**
- New runtime-generated placeholders may be added with documentation in `notes`

---

### 4.7 Parameter Names

#### Definition
Parameter names are job invocation arguments declared in the manifest `parameters` list and passed to the Glue job at runtime.

#### Format rule (MUST)

**Two allowed conventions (determined by AWS Glue system vs. user-defined):**

**Convention 1: UPPER_SNAKE_CASE (for AWS Glue system parameters)**
- Pattern: `^[A-Z][A-Z0-9_]+$`
- Used for: `JOB_NAME`, `INPUT_BUCKET`, `OUTPUT_BUCKET`, `TempDir`, etc.
- Reserved by AWS Glue; do NOT create custom parameters with this casing

**Convention 2: snake_case (for user-defined parameters)**
- Pattern: `^[a-z][a-z0-9_]+$`
- Used for: `vendor_name`, `bmecat_input_key`, `bmecat_output_prefix`, etc.
- Preferred for all custom job parameters

**Prohibited:** camelCase, PascalCase, kebab-case for parameters

#### Examples

**Valid (system parameters):**
- `JOB_NAME`
- `INPUT_BUCKET`
- `OUTPUT_BUCKET`

**Valid (user-defined parameters):**
- `vendor_name`
- `bmecat_input_key`
- `bmecat_output_prefix`
- `run_date`

**Invalid:**
- `vendorName` (camelCase; use snake_case)
- `VendorName` (PascalCase; use snake_case)
- `vendor-name` (kebab-case; not allowed)
- `Vendor_Name` (mixed case; inconsistent)

#### Compatibility expectations

**Stable:**
- Parameter names are part of the job interface contract
- Changing a parameter name is a breaking change requiring:
  - Decision record
  - Update to all callers and orchestration configs
  - Deprecation period with backward-compatible aliasing (if feasible)

---

## 5) Compatibility and Change Rules

### 5.1 Breaking vs. non-breaking naming changes

**Breaking changes (require governance approval):**
- Renaming a job ID (`job_id`, `glue_job_name`)
- Renaming a job group (folder restructure)
- Renaming an artifact filename declared in manifests or artifact catalogs
- Changing a parameter name in a deployed job
- Changing a placeholder name that affects existing patterns
- Renaming a standard or context document referenced by multiple other documents

**Non-breaking changes (allowed without special approval):**
- Adding a new job, artifact, or parameter
- Renaming a supporting script not referenced outside the job folder
- Clarifying documentation without changing identifier names
- Adding new optional outputs or parameters (non-breaking extension)

### 5.2 Backward compatibility expectations

**Deprecation period (SHOULD):**
- When a breaking naming change is unavoidable, provide a deprecation period:
  - Minimum: 2 release cycles or 30 days (whichever is longer)
  - During deprecation: support both old and new names (aliasing)
  - Emit deprecation warnings in logs/docs

**Aliasing (MAY):**
- For parameter renames: accept both old and new names; log warnings
- For artifact renames: dual-write to both old and new filenames during transition
- Document aliasing in manifest `notes` and decision record

**Migration guide (MUST for breaking changes):**
- Decision record MUST include:
  - Old name → new name mapping
  - Impact assessment (which jobs/systems affected)
  - Migration steps for consumers
  - Rollback plan

### 5.3 Governance action for breaking changes

**Required steps (MUST):**
1. Create a decision record documenting:
   - Reason for the change
   - Old vs. new naming
   - Impact analysis (all affected jobs, artifacts, references)
   - Migration plan and timeline
2. Obtain explicit human approval before implementation
3. Update all affected manifests, catalogs, and documentation
4. Test changes in non-production environment
5. Execute migration with monitoring

**Escalation trigger:**
- If a naming change would affect more than 3 jobs or 5 artifact references, escalate for broader review

---

## 6) Validation Expectations

This section defines what validators SHOULD/MUST check for naming compliance. It does NOT include tool command syntax (see `docs/ops/tooling_reference.md` for tool usage).

### 6.1 Required validation checks (MUST)

**Job ID consistency:**
- Folder name = `job_id` (manifest field) = `glue_job_name` (manifest field)
- Job ID matches snake_case pattern `^[a-z][a-z0-9_]{2,62}$` (legacy camelCase jobs `^[a-z][a-zA-Z0-9]{2,62}$` are grandfathered)

**Job group consistency:**
- Job group folder matches snake_case pattern `^[a-z][a-z0-9_]{2,62}$`

**Script filename:**
- Entrypoint is `glue_script.py` and exists in job folder

**Artifact filename format:**
- Artifact filenames in manifest `outputs[]` match snake_case pattern with valid extension
- No spaces, no special characters (except placeholders and extension)

**Parameter naming:**
- System parameters use UPPER_SNAKE_CASE
- User-defined parameters use snake_case
- No camelCase or PascalCase parameters

**Placeholder consistency:**
- Placeholders in manifest patterns use `${NAME}` format
- Parameter placeholders match declared parameter names exactly (case-sensitive)

**Documentation filename format:**
- Documentation files match layer-specific naming patterns
- All doc files use `.md` extension
- Filenames use snake_case

### 6.2 Recommended validation checks (SHOULD)

**Length limits:**
- Job IDs under 64 characters
- Parameter names under 128 characters
- All identifiers under 256 characters

**Reserved words:**
- No standalone use of Python keywords or AWS Glue reserved parameters

**Consistency across references:**
- Job IDs referenced in artifact catalogs match actual job folders
- Placeholder names in artifact catalogs match manifest declarations

### 6.3 Validation failure handling

**Critical violations (MUST block merge/deployment):**
- Job ID inconsistency (folder ≠ manifest fields)
- Invalid character set (spaces, special characters)
- Missing required files (`glue_script.py`, `job_manifest.yaml`)
- Placeholder mismatch (placeholder name ≠ parameter name)

**Warnings (SHOULD flag for review):**
- Length exceeds recommended limits
- Non-descriptive names (single-letter identifiers, overly abbreviated)
- Case convention violations in new files

### 6.4 Validation evidence requirements

**For approval of new jobs:**
- Validation report MUST show all naming checks passed
- Manifest consistency verified (job_id = folder = glue_job_name)

**For renaming (breaking changes):**
- Evidence MUST include:
  - Impact analysis (list of affected references)
  - Test results from non-production environment
  - Confirmation that all references updated

---

## Revision History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 2.0     | 2026-01-29 | Removed Section 7 (TBD resolution history); specification now contains only normative rules. All resolved items already incorporated into appropriate sections. |
| 1.3     | 2026-01-29 | Closed TBD-3: Temp artifacts explicitly excluded from scope; all 4 TBDs now resolved |
| 1.2     | 2026-01-29 | Closed TBD-2: No filename versioning needed, use PR/breaking change process; 1 TBD remains open (TBD-3) |
| 1.1     | 2026-01-29 | Closed TBD-1 and TBD-4 by referencing existing approved standards (artifacts_catalog_spec.md, job_manifest_spec.md); 2 TBDs remain open |
| 1.0     | 2026-01-29 | Initial release: all sections, 4 open TBDs   |

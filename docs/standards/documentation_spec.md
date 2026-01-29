# Documentation Specification

**Canonical location:** `docs/standards/`  
**Purpose statement:** Defines how documentation in this repository must be formatted, versioned, and structured to maintain consistency, prevent double truth, and enforce separation of concerns.  
**Why necessary:** Eliminates inconsistencies in document formatting, versioning, metadata, and content boundaries; provides clear MUST and MUST NOT rules for each document type.  
**Must contain:** Formatting rules; metadata requirements; versioning discipline; content boundary rules per document type; prohibited patterns.  
**Must not contain:** Tool command syntax or operational procedures.

---

## 0) Purpose and Scope

This specification defines **how documents must be formatted and what they may/may not contain**, independent of their semantic purpose (which is defined in the Documentation System Catalog).

### In scope:
- Document structure and formatting rules
- Metadata header requirements and versioning discipline
- Content boundaries (what may NOT appear in each document type)
- Prohibited patterns that violate separation of concerns or create double truth

### Out of scope:
- Semantic purpose and canonical placement (see `documentation_system_catalog.md`)
- Specific schemas and templates (see individual standard specs)
- Tool usage and operational procedures (see `docs/ops/`)

---

## 1) Universal Formatting Rules (MUST)

These rules apply to ALL documents in `docs/` unless explicitly exempted for a specific document type.

### 1.1 Markdown Format

All documentation files MUST:
- Use `.md` extension
- Use valid Markdown syntax
- Use UTF-8 encoding without BOM

### 1.2 File Naming

File names MUST:
- Use snake_case (lowercase with underscores): `job_manifest_spec.md`, `workflow_guide.md`
- Be descriptive and match the document's primary purpose
- NOT include version numbers in the filename (e.g., NOT `spec_v1.0.md`)

### 1.3 Document Structure

Every document MUST:
- Start with a single H1 heading (`# Title`)
- Use heading hierarchy correctly (H1 → H2 → H3, no skipping levels)
- Use consistent indentation (2 spaces for nested lists)

Every document MUST NOT:
- Have multiple H1 headings
- Use hard-coded dates/timestamps in body content (use metadata headers only)
- Include "Draft" or "WIP" markers in committed documents (use git branches for drafts)

### 1.4 Lists and Formatting

Lists MUST:
- Use `-` for unordered lists (not `*` or `+`)
- Use `1.`, `2.`, etc. for ordered lists
- Be indented with 2 spaces per nesting level

Code blocks MUST:
- Specify language for syntax highlighting when applicable: `` ```yaml ``
- Use fenced code blocks (` ``` `) not indentation-based code blocks

### 1.5 Links and References

Cross-document references MUST:
- Use relative paths from repository root: `docs/context/development_approach.md`
- NOT embed absolute URLs for internal documents
- Include path to specific document, not just folder

References to external resources SHOULD:
- Include full URL
- Be verified as accessible before committing

---

## 2) Metadata Header Requirements

All documents MUST include a metadata header block immediately after the H1 title. The format and content depend on document type.

### 2.1 Standards Documents (docs/standards/)

Standards documents define normative rules and schemas. They MUST include ALL of the following metadata fields, in this order:

```markdown
# [Document Title]

**Canonical location:** `docs/standards/`
**Purpose statement:** [One sentence: what this standard defines]
**Why necessary:** [One sentence: why this standard exists]
**Must contain:** [Brief list of required content]
**Must not contain:** [Brief list of prohibited content]
```

**Version and Update Tracking:**

Standards documents MUST include ONE of the following versioning approaches:

**Option A: Semantic Version (for stable, published standards):**
- Use when the standard has reached a stable state and changes require explicit version bumps
- Format: `**Version:** X.Y.Z` where X.Y.Z follows semantic versioning
  - Major version (X): Breaking changes to schema/format/requirements
  - Minor version (Y): Backward-compatible additions
  - Patch version (Z): Clarifications, typo fixes, non-normative changes
- Example: `**Version:** 1.2.0`

**Option B: Update Timestamp (for evolving standards):**
- Use when the standard is still evolving and frequent updates are expected
- Format: `**Last Updated:** YYYY-MM-DD` or `UPD YYYY-MM-DD` or `UPD YYYY-MM-DD HH:MM`
- Example: `UPD 2026-01-28 14:20`

**Rule:** Do NOT use both version number and update timestamp in the same document. Choose one approach based on the standard's maturity.

**Migration rule:** When transitioning from timestamp-based to version-based tracking:
1. Remove the timestamp line
2. Add `**Version:** 1.0.0` to mark the first stable version
3. Document the change in a decision record if the standard is widely used

### 2.2 Context Documents (docs/context/)

Context documents define intent, principles, and system framing. They MUST include:

```markdown
# [Document Title]

## Purpose
[2-3 sentences explaining the document's purpose]
```

Context documents MUST NOT:
- Include version numbers (they evolve with system understanding, not schema changes)
- Include update timestamps in metadata (use git history for change tracking)
- Include "Last Updated" or "UPD" fields

**Rationale:** Context documents describe evolving understanding and intent. Their authority comes from human approval and git history, not version markers. Version numbers imply contract stability that doesn't apply to conceptual framing.

### 2.3 Process Documents (docs/process/)

Process documents describe how-to guidance. They MUST include:

```markdown
# [Document Title]

## Purpose statement
[2-3 sentences: what this guide covers and when to use it]

## Scope and non-goals
**In scope:** [what this guide addresses]
**Out of scope:** [what belongs elsewhere, with pointers]
```

Process documents MUST NOT:
- Include version numbers
- Include update timestamps in metadata
- Duplicate normative rules from standards documents

### 2.4 Operational Reference Documents (docs/ops/)

Operational documents provide technical tool manuals. They SHOULD include:

```markdown
# [Document Title]

**Purpose:** [One sentence: what this reference covers]
**Scope:** [What tools/systems are covered]
```

Operational documents MAY include version numbers if they track specific tool versions, but this is optional.

### 2.5 Living Catalogs (docs/catalogs/)

Living catalogs are compiled views. They MUST include:

```markdown
# [Document Title]

**Canonical location:** `docs/catalogs/`
**Purpose statement:** [What this catalog indexes]
**Why necessary:** [Why this catalog exists]
**Must contain:** [What entries must include]
**Must not contain:** [What should not be here]
```

Catalogs MAY include an update timestamp showing last compilation:
- Format: `UPD YYYY-MM-DD` (date only, no time)
- Placed immediately after the title, before other metadata
- Example: `UPD 2026-01-28`

### 2.6 Agent Documentation (docs/agents/ and .github/agents/)

Agent role definitions MUST include:

```markdown
# [Document Title]

**Purpose:** [What this document defines]
**Scope:** [What aspects of agent behavior are covered]
```

Agent profile definitions (.github/agents/) MUST include frontmatter:

```markdown
---
name: agent-name
description: One sentence describing agent purpose
---
```

### 2.7 Per-Job Documentation (jobs/<job_group>/<job_id>/)

Per-job documentation lives in the job folder structure `jobs/<job_group>/<job_id>/` and includes multiple document types with different purposes:

#### 2.7.1 Job Manifest (REQUIRED)

**File:** `job_manifest.yaml`

**Purpose:** Machine-readable interface contract defining parameters, inputs, outputs, side effects, and observability.

**Specification:** `docs/standards/job_manifest_spec.md`

**Metadata requirements:**
- YAML format
- Must conform to job_manifest_spec schema
- Version/timestamp NOT required (follows deployment versioning)
- Required fields defined in spec (job_id, glue_job_name, runtime, parameters, inputs, outputs, side_effects, logging_and_receipt)

#### 2.7.2 Implementation Code (REQUIRED)

**File:** `glue_script.py` (or other entrypoint as declared in manifest)

**Purpose:** The executable job implementation.

**Format:** Python code (PySpark or Python Shell)

**Metadata requirements:**
- Standard Python file conventions
- Shebang optional
- Docstrings recommended but not enforced by this spec

#### 2.7.3 Business Job Description (REQUIRED)

**File:** `bus_description_<job_id>.md`

**Purpose:** Human-readable business intent, scope, and rules.

**Specification:** `docs/standards/business_job_description_spec.md`

**Metadata requirements:**
- Follow business_job_description_spec structure
- No version numbers or timestamps
- Use git history for change tracking

#### 2.7.4 Script Card (DEFINED, may not exist yet)

**File:** `script_card_<job_id>.md`

**Purpose:** Operational behavior documentation (how it runs, invariants, failure modes).

**Specification:** `docs/standards/script_card_spec.md`

**Metadata requirements:**
- Follow script_card_spec structure
- No version numbers or timestamps
- Use git history for change tracking

**Note:** Script cards are defined in the standard but may not yet exist for all jobs. The specification exists to guide future documentation efforts.

---

## 3) Versioning Discipline (Standards Documents Only)

This section applies ONLY to documents in `docs/standards/`.

### 3.1 When to Increment Versions

**Major version (X.0.0):**
- Change breaks existing tooling or validation
- Required fields are removed or renamed
- Enum values are removed
- Schema structure changes incompatibly

**Minor version (X.Y.0):**
- New optional fields added
- New enum values added
- Backward-compatible clarifications that change interpretation
- New sections added without changing existing requirements

**Patch version (X.Y.Z):**
- Typo fixes
- Grammar/clarity improvements
- Example updates
- Non-normative text changes
- Formatting improvements

### 3.2 Version Number Placement

When using version numbers:
- Place AFTER "Purpose statement" and "Why necessary"
- Use format: `**Version:** X.Y.Z`
- Do NOT use "v" prefix: use `1.0.0` not `v1.0.0`

### 3.3 Timestamp Format (When Used Instead of Versions)

When using timestamps instead of semantic versions:
- Format: `UPD YYYY-MM-DD` or `UPD YYYY-MM-DD HH:MM`
- Place immediately after title, before other metadata
- Time portion (HH:MM) is optional
- Use UTC timezone when including time

### 3.4 Deprecated: Hybrid Approach

**MUST NOT:** Use both version number and timestamp in the same document header.

**Legacy documents with hybrid approach:** Migrate to single approach:
- If standard is stable and widely referenced: keep version number, remove timestamp
- If standard is evolving: keep timestamp, remove version number

---

## 4) Content Boundary Rules by Document Type

### 4.1 Context Documents (docs/context/) MUST NOT Contain:

- Tool command syntax or CLI usage examples
- Step-by-step operational procedures
- Normative schemas, required fields, or validation rules
- Embedded authoritative templates
- Specific tool names as requirements (tools are referenced conceptually)
- Detailed troubleshooting instructions

**What they SHOULD contain:**
- Principles and intent
- Conceptual definitions
- Operating model and roles
- Truth hierarchy and authority structure
- Pointers to where specifics live

### 4.2 Standards Documents (docs/standards/) MUST NOT Contain:

- Tool command examples (reference ops docs instead)
- Workflow procedures (reference process docs instead)
- Embedded context/rationale that restates principles
- Per-job content or instances (those belong in catalogs or per-job docs)
- Conflicting definitions with glossary terms

**What they MUST contain:**
- Normative schemas and required fields
- Validation rules and pass/fail criteria
- Allowed enums and formats
- Breaking change rules
- Compliance checklists

### 4.3 Process Documents (docs/process/) MUST NOT Contain:

- Normative schemas (use standards docs)
- Tool command syntax (use ops docs)
- Redefined terms (use glossary)
- Embedded templates that compete with standards

**What they SHOULD contain:**
- Step-by-step execution guidance
- Entry and exit criteria
- Approval gate procedures
- Escalation triggers
- Iteration patterns
- References to relevant standards

### 4.4 Operational Reference Documents (docs/ops/) MUST NOT Contain:

- Normative schemas or contract definitions
- Business rationale or principles
- Workflow approval gates
- Standard definitions

**What they SHOULD contain:**
- Tool command syntax and parameters
- Troubleshooting procedures
- CI/automation configuration
- Version compatibility notes
- Output interpretation guides

### 4.5 Living Catalogs (docs/catalogs/) MUST NOT Contain:

- Schema definitions (reference standards instead)
- Tool usage instructions
- Workflow procedures
- Business rationale for individual entries

**What they MUST contain:**
- Compiled entries conforming to relevant specs
- References to canonical sources
- Status/lifecycle indicators
- Index/navigation structure

### 4.6 Per-Job Documentation MUST NOT Contain:

**Job Manifests (job_manifest.yaml) MUST NOT contain:**
- Business rationale or "why" explanations (use business description)
- Operational troubleshooting (reference script card or ops docs)
- Global definitions (use glossary)
- Per-job-instance values (use placeholders for runtime values)

**Implementation Code (glue_script.py) MUST NOT contain:**
- This specification does not govern code content (see development standards if they exist)

**Business Descriptions MUST NOT contain:**
- Operational run instructions (use script card)
- Technical interface details already in manifest (reference manifest instead)
- Global definitions applicable across jobs (use glossary)

**Script Cards MUST NOT contain:**
- Global definitions applicable across jobs (use glossary)
- Business justification (use business description)
- Normative contract schemas already defined elsewhere (reference standards)
- Duplicated metadata already in manifests (reference manifest instead)

---

## 5) Prohibited Patterns (MUST NOT)

These patterns violate separation of concerns or create double truth and are PROHIBITED in all documentation:

### 5.1 "Open Items" or "TODO" Sections in Standards

**Prohibited:**
```markdown
## Open Items
- [ ] Decide on validation approach
- [ ] Define error handling
```

**Rationale:** Standards documents are normative contracts. Incomplete standards should not be committed. Use `TBD` fields within the schema with explanations in `notes`, or use git issues/branches for work in progress.

**Allowed alternative:**
- Use `TBD` as a field value with explanation (as defined in each standard spec)
- Use decision records to track unresolved decisions
- Use git issues for tracking future enhancements

### 5.2 Embedded Competing Authority

**Prohibited:** Redefining schemas, templates, or rules that are defined authoritatively elsewhere.

**Example of violation:**
A process guide contains a complete job manifest template with required fields, competing with `job_manifest_spec.md`.

**Correct approach:**
Process guide references the standard: "See `docs/standards/job_manifest_spec.md` for required fields."

### 5.3 Shadow Specifications

**Prohibited:** Embedding normative requirements in documents of the wrong type.

**Examples:**
- Tool command syntax in context documents
- Approval gate procedures in standards documents
- Schema definitions in process guides
- Business rationale in operational references

### 5.4 Undocumented Version Changes

**Prohibited:** Changing version numbers or timestamps without corresponding content changes in a commit.

**Rule:** Version/timestamp changes MUST occur in the same commit as the content changes that necessitate them.

### 5.5 Subjective "Verified" Claims

**Prohibited:** Using "verified", "confirmed", "validated" without explicit evidence reference.

**Example violation:**
```markdown
The job correctly handles all edge cases. (verified)
```

**Correct approach:**
```markdown
The job correctly handles all edge cases (verified via test execution 2026-01-28, see test_results.log).
```

Or use `TBD`:
```markdown
Edge case handling: TBD (requires integration testing in staging environment)
```

### 5.6 Hardcoded Timestamps in Body Text

**Prohibited:** Including update timestamps or "last modified" statements in document body.

**Example violation:**
```markdown
## Schema Definition
(Updated 2026-01-28)
...
```

**Correct approach:** Use metadata header only; rely on git history for detailed change tracking.

---

## 6) Special Cases and Exemptions

### 6.1 README.md (Repository Root)

The repository root `README.md` is EXEMPTED from:
- Metadata header requirements (use free-form structure optimized for first-time visitors)
- Versioning requirements

It MUST still:
- Follow universal formatting rules (section 1)
- Provide clear navigation to the documentation system
- Avoid duplicating authoritative content

### 6.2 Decision Records (docs/decisions/)

Decision records follow `decision_records_standard.md` and are EXEMPTED from:
- Standard metadata headers (use decision-specific headers)

They MUST:
- Include decision status (Proposed, Accepted, Superseded)
- Include decision date
- Include rationale and alternatives considered

### 6.3 Agent Profile Definitions (.github/agents/)

Agent profiles MUST:
- Use frontmatter for metadata (GitHub Copilot requirement)
- Include complete agent instructions in a single file (GitHub limitation)
- Reference but not duplicate standards

They are EXEMPTED from:
- Standard documentation metadata headers
- Canonical location statements (GitHub requires `.github/agents/`)

---

## 7) Compliance and Enforcement

### 7.1 Pre-Commit Validation

Validation tools MAY check:
- Metadata header completeness
- Prohibited patterns (open items sections, hardcoded timestamps)
- Version/timestamp format compliance
- Heading hierarchy
- Cross-reference validity

### 7.2 Human Review Checklist

When reviewing documentation changes, check:
- [ ] Metadata header is complete and correctly formatted for document type
- [ ] Version/timestamp approach is consistent (not hybrid)
- [ ] No prohibited patterns present
- [ ] Content boundaries respected (no shadow specs)
- [ ] Cross-references use correct paths
- [ ] Changes align with versioning discipline

### 7.3 Migration of Existing Documents

Existing documents that violate this specification:
- SHOULD be updated incrementally as they are edited
- MUST be migrated before adding new normative requirements
- Changes SHOULD be minimal (formatting/metadata only) to reduce noise

---

## 8) Relationship to Other Documents

This specification:
- **Builds on** `documentation_system_catalog.md` (which defines document types and purposes)
- **Aligns with** `target_agent_system.md` (separation of concerns, no double truth)
- **Is enforced by** `validation_standard.md` (compliance checking)
- **Guides** all documentation authors and agents in producing consistent documentation

---

## 9) Examples

### 9.1 Correct Standards Document Header (with version)

```markdown
# Example Standard Specification

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for example artifacts.
**Why necessary:** Ensures consistent structure across example artifacts.
**Must contain:** Required fields, validation rules, compliance checklist.
**Must not contain:** Tool command syntax, workflow procedures.
**Version:** 1.2.0
```

### 9.2 Correct Standards Document Header (with timestamp)

```markdown
# Example Standard Specification

UPD 2026-01-28
**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for example artifacts.
**Why necessary:** Ensures consistent structure across example artifacts.
**Must contain:** Required fields, validation rules, compliance checklist.
**Must not contain:** Tool command syntax, workflow procedures.
```

### 9.3 Correct Context Document Header

```markdown
# Example Context Document

## Purpose
This document defines the conceptual framework for the example subsystem.
It explains intent, roles, and operating principles without specifying
normative schemas or tool usage.
```

### 9.4 Incorrect: Hybrid Version/Timestamp (PROHIBITED)

```markdown
# Example Specification (v1.0)

UPD 2026-01-28 14:20
**Version:** 1.0.0
**Canonical location:** `docs/standards/`
...
```

**Problem:** Uses both timestamp and version number.

### 9.5 Incorrect: Open Items Section (PROHIBITED)

```markdown
# Example Specification

...

## Open Items
- Define retry behavior
- Clarify error handling

## Schema
...
```

**Problem:** Committed standard contains incomplete "open items" section.

### 9.6 Per-Job Documentation Structure (CORRECT)

For a job `preprocessIncomingBmecat` in the `vendor_input_processing` group:

```
jobs/vendor_input_processing/preprocessIncomingBmecat/
├── job_manifest.yaml              # Machine-readable interface contract (REQUIRED)
├── glue_script.py                 # Implementation code (REQUIRED)
├── bus_description_preprocessIncomingBmecat.md  # Business intent (REQUIRED)
└── script_card_preprocessIncomingBmecat.md      # Operational behavior (defined in spec, may not exist yet)
```

**Key points:**
- All four document types serve different purposes and are not redundant
- job_manifest.yaml is the source of truth for interface facts
- Business descriptions explain "why" and scope
- Script cards explain "how" and failure modes
- glue_script.py is the actual implementation

---

## 10) Summary: Key Rules

**Universal rules (all documents):**
1. Use consistent Markdown formatting
2. Single H1 title
3. No hardcoded timestamps in body text
4. Valid cross-references

**Metadata rules (by document type):**
- Standards: Full metadata block + version OR timestamp (not both)
- Context: Purpose only, no version markers
- Process: Purpose and scope, no version markers
- Catalogs: Full metadata block + optional update timestamp
- Ops: Minimal metadata, optional tool version
- Per-job manifests: YAML schema, no metadata header
- Per-job business descriptions: Follow business_job_description_spec
- Per-job script cards: Follow script_card_spec (when they exist)

**Content boundaries (prevent double truth):**
- Context: principles, not tools/schemas
- Standards: schemas, not tools/procedures
- Process: procedures, not schemas
- Ops: tools, not contracts/schemas
- Catalogs: indexes, not definitions
- Per-job manifests: interface facts only, not business rationale
- Per-job business descriptions: intent/scope, not technical interface details
- Per-job script cards: operational behavior, not business justification

**Prohibited patterns:**
- Open items sections in standards
- Competing authority (shadow specs)
- Unsubstantiated "verified" claims
- Hybrid version/timestamp markers
- Tool syntax in context/standards
- Schemas in process/ops

---

**Compliance:** This specification takes effect immediately for new documents. Existing documents SHOULD migrate incrementally.

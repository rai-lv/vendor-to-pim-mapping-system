# Documentation Specification

**Canonical location:** `docs/standards/`  
**Purpose statement:** Defines how documentation in this repository must be formatted, structured, and versioned to maintain consistency.  
**Why necessary:** Eliminates inconsistencies in document formatting, structure, versioning, and metadata; ensures uniform presentation across all documentation types.  
**Must contain:** Formatting rules; metadata requirements; versioning discipline; file naming conventions; structural anti-patterns.  
**Must not contain:** Semantic content rules (see documentation_system_catalog.md); tool command syntax; operational procedures.

---

## 0) Purpose and Scope

This specification defines **how documents must be formatted, structured, and versioned** to maintain consistency across the documentation system.

### In scope:
- Document structure and formatting rules (Markdown conventions, headings, lists, code blocks)
- Metadata header requirements and formatting
- Versioning discipline (when to use versions vs timestamps, how to format them)
- Structural anti-patterns (e.g., multiple H1 headings, hardcoded timestamps in body text)
- File naming conventions

### Out of scope:
- **Semantic content rules** (what each document type should/shouldn't contain) - see `documentation_system_catalog.md`
- Canonical placement and document type purposes - see `documentation_system_catalog.md`
- Specific schemas and templates (see individual standard specs)
- Tool usage and operational procedures (see `docs/ops/`)

**Key principle:** This specification addresses FORMAT and STRUCTURE. The documentation_system_catalog.md addresses SEMANTIC CONTENT and PURPOSE.

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

## 4) Semantic Content Rules

**This specification does NOT define semantic content rules.** 

For rules about what content belongs in each document type (what documents MUST contain and MUST NOT contain), see:
- **`docs/context/documentation_system_catalog.md`** - Defines the purpose, scope, and content boundaries for each document type

This specification focuses exclusively on **format, structure, and presentation** requirements.

---

## 5) Prohibited Structural Patterns (MUST NOT)

These patterns violate formatting, structure, or versioning discipline and are PROHIBITED:

### 5.1 "Open Items" or "TODO" Sections in Committed Documents

**Prohibited:**
```markdown
## Open Items
- [ ] Decide on validation approach
- [ ] Define error handling
```

**Rationale:** This is a STRUCTURAL anti-pattern. Committed documents should be complete. Use git branches for work-in-progress, or use `TBD` fields within schemas (as defined in individual specs).

**Allowed alternative:**
- Use `TBD` as a field value with explanation (as defined in each standard spec)
- Use git issues for tracking future enhancements
- Keep work-in-progress on feature branches

### 5.2 Multiple H1 Headings

**Prohibited:** More than one H1 (`#`) heading in a document.

**Rationale:** Document structure requires exactly one H1 title at the top.

### 5.3 Undocumented Version Changes

**Prohibited:** Changing version numbers or timestamps without corresponding content changes in a commit.

**Rule:** Version/timestamp changes MUST occur in the same commit as the content changes that necessitate them.

### 5.4 Hardcoded Timestamps in Body Text

**Prohibited:** Including update timestamps or "last modified" statements in document body.

**Example violation:**
```markdown
## Schema Definition
(Updated 2026-01-28)
...
```

**Correct approach:** Use metadata header only; rely on git history for detailed change tracking.

### 5.5 Hybrid Version/Timestamp Markers

**Prohibited:** Using both version number and timestamp in the same document header.

**Example violation:**
```markdown
UPD 2026-01-28 14:20
**Version:** 1.0.0
```

**Correct approach:** Choose ONE versioning approach (see section 3).

### 5.6 Incorrect Heading Hierarchy

**Prohibited:** Skipping heading levels (e.g., H1 → H3 without H2).

**Correct:** Use sequential heading levels: H1 → H2 → H3 → H4

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

This specification addresses **format and structure**.

**Division of responsibility:**

- **`documentation_system_catalog.md`** (SEMANTIC CONTENT):
  - Defines document types and their purposes
  - Specifies what content belongs in each document type
  - Provides "Must contain" and "Must not contain" rules
  - THIS IS THE AUTHORITATIVE SOURCE FOR CONTENT RULES

- **`documentation_spec.md`** (FORMAT AND STRUCTURE - this document):
  - Defines formatting conventions (Markdown, headings, lists)
  - Specifies metadata header formats
  - Defines versioning discipline
  - Provides structural anti-patterns

- **`target_agent_system.md`**:
  - Defines separation of concerns principles
  - Specifies no double truth rule
  - This spec aligns with those principles

- **`validation_standard.md`**:
  - May enforce rules from both catalog (content) and spec (format)

**Key principle:** Semantic content rules live in ONE place (documentation_system_catalog.md). Format rules live in ONE place (this document). This prevents double truth.

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

**Universal formatting rules (all documents):**
1. Use consistent Markdown formatting (snake_case filenames, UTF-8 encoding)
2. Single H1 title at document start
3. Sequential heading hierarchy (H1 → H2 → H3, no skipping)
4. No hardcoded timestamps in body text (use metadata headers only)
5. Valid cross-references using relative paths
6. Consistent list markers (`-` for unordered, `1.` for ordered)

**Metadata rules (by document type):**
- Standards: Full metadata block + version OR timestamp (not both)
- Context: Purpose section only, no version markers
- Process: Purpose and scope sections, no version markers
- Catalogs: Full metadata block + optional update timestamp
- Ops: Minimal metadata, optional tool version tracking
- Per-job manifests: YAML schema per job_manifest_spec
- Per-job business descriptions: Follow business_job_description_spec structure
- Per-job script cards: Follow script_card_spec structure (when they exist)

**Versioning discipline:**
- Semantic versions (X.Y.Z) for stable standards with breaking change tracking
- Timestamps (UPD YYYY-MM-DD) for evolving standards
- Never mix both in same document
- Version/timestamp changes only in same commit as content changes

**Prohibited structural patterns:**
- Open items/TODO sections in committed documents
- Multiple H1 headings in one document
- Hardcoded timestamps in body text
- Hybrid version/timestamp markers
- Incorrect heading hierarchy (skipping levels)
- Undocumented version changes

**For semantic content rules (what belongs in each document type):**
- See `docs/context/documentation_system_catalog.md`

---

**Compliance:** This specification takes effect immediately for new documents. Existing documents SHOULD migrate incrementally.

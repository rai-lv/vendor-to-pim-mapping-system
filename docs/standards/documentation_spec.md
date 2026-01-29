# Documentation Specification

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines how documentation must be structured, formatted, and governed to maintain consistency, clarity, and single source of truth across the documentation system.
**Why necessary:** Ensures documentation is reliable, maintainable, discoverable, and aligned with foundational principles that prevent duplication and confusion.
**Must contain:** Foundational principles, formatting rules, metadata requirements, versioning discipline, quality criteria, anti-patterns, examples, and governance procedures.
**Must not contain:** Tool command syntax (belongs in docs/ops/), workflow procedures (belongs in docs/process/), or specific document type schemas (belongs in individual specs).

---

## 0) Purpose and Principles

### 0.1 What This Specification Addresses

This specification defines **how documentation must be structured, formatted, and governed** to maintain consistency across the documentation system.

**In scope:**
- Foundational principles that govern all documentation
- Document structure and formatting rules (Markdown conventions, headings, lists, code blocks)
- Metadata header requirements and formatting
- Versioning discipline (when to use versions vs timestamps, how to format them)
- Quality criteria and anti-patterns
- File naming conventions
- Governance and compliance

**Out of scope:**
- **Semantic content rules** (what each document type should/shouldn't contain) - see `documentation_system_catalog.md`
- Canonical placement and document type purposes - see `documentation_system_catalog.md`
- Specific schemas and templates (see individual standard specs)
- Tool usage and operational procedures (see `docs/ops/`)

### 0.2 Core Philosophy

**Documentation exists to enable informed decisions and effective action.**

This specification is grounded in foundational principles that prevent the most common documentation failures: duplication, confusion, staleness, and unclear authority. These principles ensure documentation serves as a reliable, maintainable system of record rather than becoming a burden.

**Key principle:** This specification addresses FORMAT, STRUCTURE, and GOVERNANCE. The documentation_system_catalog.md addresses SEMANTIC CONTENT and PURPOSE.

---

## 1) Foundational Principles

These are the non-negotiable foundation of the documentation system. All other rules derive from these.

**Note:** These principles are documentation-specific. For system-wide principles governing human-agent collaboration and approval gates, see `target_agent_system.md`.

### 1.1 Single Source of Truth (No Double Truth)

**Principle:** Each fact, rule, definition, or contract must have exactly one authoritative source.

**Why:** Duplication creates divergence over time, confusion about which source is correct, and maintenance burden.

**Application:**
- If information exists in document A, document B may REFERENCE it but MUST NOT redefine it
- When the same information appears in multiple places, one must be designated authoritative and others removed or converted to references
- Schemas, templates, and normative rules have one canonical home

**Example violations:**
- ❌ Job manifest schema defined in both `job_manifest_spec.md` and workflow guide
- ❌ Glossary term redefined in multiple documents with different meanings
- ❌ Metadata header format defined in both the spec and in each document using it

**Example compliance:**
- ✅ Job manifest schema defined ONLY in `job_manifest_spec.md`, referenced elsewhere
- ✅ Glossary defines terms once; other docs use those terms consistently
- ✅ Metadata header format defined in spec; individual docs follow it without redefining

### 1.2 Separation of Concerns (Layered Architecture)

**Principle:** Documentation must be organized into distinct layers, each with a specific purpose that does not overlap with others.

**Why:** Mixing purposes creates confusion, makes documents hard to maintain, and obscures the appropriate level of abstraction.

**Layers:**

1. **Context Layer** (docs/context/) - Intent, principles, framing
   - WHAT the system aims to achieve
   - WHY it's structured this way
   - High-level operating model
   - Does NOT contain: tool commands, normative schemas, step-by-step procedures

2. **Standards Layer** (docs/standards/) - Enforceable rules and schemas
   - Normative schemas and required fields
   - Validation rules and compliance criteria
   - Breaking change definitions
   - Does NOT contain: rationale (belongs in context), procedures (belongs in process)

3. **Process Layer** (docs/process/) - Execution guidance
   - Step-by-step how-to guides
   - Entry/exit criteria for stages
   - Approval gate procedures
   - Does NOT contain: normative schemas (belongs in standards), tool syntax (belongs in ops)

4. **Operations Layer** (docs/ops/) - Tool manuals and troubleshooting
   - Command syntax and parameters
   - CI/CD configuration
   - Troubleshooting guides
   - Does NOT contain: business rationale (belongs in context), schemas (belongs in standards)

5. **Catalog Layer** (docs/catalogs/) - Living inventories
   - Compiled views of instances
   - Status and lifecycle tracking
   - Does NOT contain: schema definitions (belongs in standards)

6. **Instance Layer** (jobs/, per-job docs) - Specific implementations
   - Per-job manifests, descriptions, cards
   - Implementation-specific details
   - Does NOT contain: global rules (belongs in standards)

**Anti-pattern:** "Shadow specifications" - normative requirements embedded in the wrong layer (e.g., a process guide that contains required field definitions instead of referencing the standard).

### 1.3 Evidence-Based Claims

**Principle:** Claims about system behavior, validation status, or compliance must be backed by explicit evidence.

**Why:** Prevents unverifiable assertions, ensures accountability, enables independent verification.

**Rules:**
- Words like "verified", "confirmed", "validated" MUST reference specific evidence
- Evidence must be reproducible (others with same inputs and context can verify the claim)
- If evidence doesn't exist, use "TBD" or "unverified" rather than claiming verification

**Example violations:**
- ❌ "The job handles all edge cases correctly (verified)" - no evidence reference
- ❌ "All tests pass" - which tests? when? evidence link?

**Example compliance:**
- ✅ "Edge case handling verified via test suite run 2025-12-15 (see test_results.log)"
- ✅ "Validation status: UNVERIFIED - requires integration testing in staging"
- ✅ "Complies with spec (validated by `validate_manifest.py` on 2025-12-15)"

### 1.4 Explicit Over Implicit

**Principle:** Unknowns, assumptions, decisions, and boundaries must be stated explicitly, not left implicit.

**Why:** Prevents silent assumptions, makes gaps visible, enables informed decisions.

**Rules:**
- Unknown information: Mark as "TBD" or "unknown", don't hide it
- Assumptions: Label explicitly, state what/why/impact, get approval before depending on them
- Scope boundaries: State both what IS and what IS NOT in scope
- Decisions: Document in decision records with rationale and alternatives considered

**Example violations:**
- ❌ Silently assuming a parameter is optional when it's actually unknown
- ❌ Leaving unknowns unmarked and proceeding as if everything is known
- ❌ Making an architecture decision without documenting rationale

**Example compliance:**
- ✅ "Parameter `retry_count`: TBD - requires discussion with ops team"
- ✅ "Assumption: S3 bucket has versioning enabled. Impact: Recovery possible. Approved: 2025-12-15"
- ✅ Decision record documents why approach X was chosen over alternatives Y and Z

---

## 2) Universal Formatting Rules (MUST)

These rules apply to ALL documents in `docs/` unless explicitly exempted for a specific document type.

### 2.1 Markdown Format

All documentation files MUST:
- Use `.md` extension
- Use valid Markdown syntax
- Use UTF-8 encoding without BOM

### 2.2 File Naming

File names MUST:
- Use snake_case (lowercase with underscores): `job_manifest_spec.md`, `workflow_guide.md`
- Be descriptive and match the document's primary purpose
- NOT include version numbers in the filename (e.g., NOT `spec_v1.0.md`)

### 2.3 Document Structure

Every document MUST:
- Start with a single H1 heading (`# Title`)
- Use heading hierarchy correctly (H1 → H2 → H3, no skipping levels)
- Use consistent indentation (2 spaces for nested lists)

Every document MUST NOT:
- Have multiple H1 headings
- Use hard-coded dates/timestamps in body content (use metadata headers only)
- Include "Draft" or "WIP" markers in committed documents (use git branches for drafts)

### 2.4 Lists and Formatting

Lists MUST:
- Use `-` for unordered lists (not `*` or `+`)
- Use `1.`, `2.`, etc. for ordered lists
- Be indented with 2 spaces per nesting level

Code blocks MUST:
- Specify language for syntax highlighting when applicable: `` ```yaml ``
- Use fenced code blocks (` ``` `) not indentation-based code blocks

### 2.5 Links and References

Cross-document references MUST:
- Use relative paths from repository root: `docs/context/development_approach.md`
- NOT embed absolute URLs for internal documents
- Include path to specific document, not just folder

References to external resources SHOULD:
- Include full URL
- Be verified as accessible before committing

---

## 3) Metadata Header Requirements

All documents MUST include a metadata header block immediately after the H1 title. The format and content depend on document type.

### 3.1 Standards Documents (docs/standards/)

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

### 3.2 Context Documents (docs/context/)

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

### 3.3 Process Documents (docs/process/)

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

### 3.4 Operational Reference Documents (docs/ops/)

Operational documents provide technical tool manuals. They SHOULD include:

```markdown
# [Document Title]

**Purpose:** [One sentence: what this reference covers]
**Scope:** [What tools/systems are covered]
```

Operational documents MAY include version numbers if they track specific tool versions, but this is optional.

### 3.5 Living Catalogs (docs/catalogs/)

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

### 3.6 Agent Documentation (docs/agents/ and .github/agents/)

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

### 3.7 Per-Job Documentation (jobs/<job_group>/<job_id>/)

Per-job documentation includes multiple file types. For the purpose and semantic content rules of each type, see `docs/context/documentation_system_catalog.md`.

This section defines ONLY the metadata formatting requirements for each file type:

#### 3.7.1 Job Manifest Files (job_manifest.yaml)

**Metadata formatting:**
- YAML format
- No metadata header block (content is schema-driven per `job_manifest_spec.md`)
- No version/timestamp markers in the file itself

#### 3.7.2 Implementation Code Files (glue_script.py)

**Metadata formatting:**
- Python file format
- Standard Python file conventions apply
- Shebang optional
- Docstrings recommended but not enforced by this specification
- No documentation-style metadata header required

#### 3.7.3 Business Description Files (bus_description_<job_id>.md)

**Metadata formatting:**
- Markdown format
- Follow structure defined in `business_job_description_spec.md`
- No version numbers or timestamps in metadata
- Use git history for change tracking

#### 3.7.4 Script Card Files (script_card_<job_id>.md)

**Metadata formatting:**
- Markdown format
- Follow structure defined in `script_card_spec.md`
- No version numbers or timestamps in metadata
- Use git history for change tracking

**Note:** For file naming conventions, see `naming_standard.md`. For semantic content rules (what each file type must/must not contain), see `documentation_system_catalog.md`.

---

## 4) Versioning Discipline (Standards Documents Only)

This section applies ONLY to documents in `docs/standards/`.

### 4.1 When to Increment Versions

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

### 4.2 Version Number Placement

When using version numbers:
- Place AFTER "Purpose statement" and "Why necessary"
- Use format: `**Version:** X.Y.Z`
- Do NOT use "v" prefix: use `1.0.0` not `v1.0.0`

### 4.3 Timestamp Format (When Used Instead of Versions)

When using timestamps instead of semantic versions:
- Format: `UPD YYYY-MM-DD` or `UPD YYYY-MM-DD HH:MM`
- Place immediately after title, before other metadata
- Time portion (HH:MM) is optional
- Use UTC timezone when including time

### 4.4 Deprecated: Hybrid Approach

**MUST NOT:** Use both version number and timestamp in the same document header.

**Legacy documents with hybrid approach:** Migrate to single approach:
- If standard is stable and widely referenced: keep version number, remove timestamp
- If standard is evolving: keep timestamp, remove version number

---

## 5) Quality Criteria and Anti-Patterns

### 5.1 Quality Criteria

Documentation should be evaluated against these criteria:

#### 5.1.1 Accuracy

**Definition:** Information matches reality (code, behavior, decisions).

**Validation:**
- Can claims be verified against evidence?
- Does documentation reflect current implementation?
- Are there conflicts between docs and code?

#### 5.1.2 Completeness

**Definition:** All necessary information is present, unknowns are marked.

**Validation:**
- Are required sections present?
- Are TBDs explicitly marked?
- Is scope clearly bounded?

#### 5.1.3 Currency

**Definition:** Documentation reflects current state, not stale information.

**Validation:**
- Are timestamps/versions recent?
- Do git commit dates match metadata timestamps (when present)?
- Are obsolete documents marked as such?

#### 5.1.4 Clarity

**Definition:** Documentation is understandable to its intended audience.

**Validation:**
- Can target audience understand without external context?
- Are terms defined (or referenced in glossary)?
- Is structure logical and easy to navigate?

#### 5.1.5 Maintainability

**Definition:** Documentation can be updated efficiently without breaking things.

**Validation:**
- Is there duplication that requires updates in multiple places?
- Are cross-references stable or brittle?
- Is scope clear enough to know what belongs where?

### 5.2 Prohibited Structural Patterns (MUST NOT)

These patterns violate formatting, structure, or versioning discipline and are PROHIBITED:

#### 5.2.1 "Open Items" or "TODO" Sections in Committed Documents

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

#### 5.2.2 Multiple H1 Headings

**Prohibited:** More than one H1 (`#`) heading in a document.

**Rationale:** Document structure requires exactly one H1 title at the top.

#### 5.2.3 Undocumented Version Changes

**Prohibited:** Changing version numbers or timestamps without corresponding content changes in a commit.

**Rule:** Version/timestamp changes MUST occur in the same commit as the content changes that necessitate them.

#### 5.2.4 Hardcoded Timestamps in Body Text

**Prohibited:** Including update timestamps or "last modified" statements in document body.

**Example violation:**
```markdown
## Schema Definition
(Updated 2026-01-28)
...
```

**Correct approach:** Use metadata header only; rely on git history for detailed change tracking.

#### 5.2.5 Hybrid Version/Timestamp Markers

**Prohibited:** Using both version number and timestamp in the same document header.

**Example violation:**
```markdown
UPD 2026-01-28 14:20
**Version:** 1.0.0
```

**Correct approach:** Choose ONE versioning approach (see section 4).

#### 5.2.6 Incorrect Heading Hierarchy

**Prohibited:** Skipping heading levels (e.g., H1 → H3 without H2).

**Correct:** Use sequential heading levels: H1 → H2 → H3 → H4

### 5.3 Semantic Anti-Patterns

Based on real issues encountered:

#### 5.3.1 Circular Documentation

**Problem:** Document A defines format that document A itself uses, creating circular self-reference issues.

**Example:** A metadata specification that references its own metadata format definition within its metadata header, creating infinite regress.

**Solution:** Meta-documents (specs, guides about documentation) define rules for other documents to follow. When a meta-document follows its own rules, this is acceptable as long as it doesn't create circular references in the content itself (e.g., "See section X for metadata format" within the metadata header itself).

#### 5.3.2 Shadow Specifications

**Problem:** Normative requirements embedded in the wrong layer.

**Example:** A workflow guide contains "required fields" section competing with the official spec.

**Solution:** Process docs reference standards; they don't redefine them.

#### 5.3.3 Competing Authority

**Problem:** Same rule defined differently in multiple places.

**Example:** Glossary defines "manifest", but a spec redefines it differently.

**Solution:** Designate one source as authoritative, others reference or defer to it.

#### 5.3.4 Implicit Assumptions

**Problem:** Documentation proceeds as if unknowns are known without marking them.

**Example:** Describing a feature's behavior when it hasn't been implemented yet.

**Solution:** Use "TBD", "unknown", or explicit assumption markers.

#### 5.3.5 Stale References

**Problem:** Cross-references break when things move or change names.

**Example:** Linking to "job_spec.md" which was renamed to "job_manifest_spec.md".

**Solution:** Use canonical paths, update references when refactoring, check for broken links.

---

## 6) Application Guidelines

### 6.1 Creating New Documentation

When creating a new document:

1. **Identify its layer** - Context, Standards, Process, Ops, Catalog, or Instance?
2. **Check for existing coverage** - Does this information already exist elsewhere?
3. **Define its scope** - What MUST it contain? What MUST it NOT contain?
4. **Establish authority** - Is this the authoritative source, or does it reference others?
5. **Add to catalog** - Register in documentation_system_catalog.md
6. **Follow format spec** - Use appropriate metadata headers, file naming, structure

### 6.2 Updating Existing Documentation

When updating a document:

1. **Verify single source** - If changing a rule, is THIS the authoritative source?
2. **Check for duplication** - Will this change need to be repeated elsewhere? If so, remove duplication first.
3. **Assess impact** - Is this a breaking change requiring version bump?
4. **Update references** - If changing canonical paths or key sections, update cross-references.
5. **Provide evidence** - If making claims, link to evidence.
6. **Document decision** - If making a significant change, create decision record.

### 6.3 Resolving Conflicts

When documents conflict:

1. **Identify authority** - Which document is the authoritative source for this topic?
2. **Classify conflict** - Intent vs. implementation? Rules vs. behavior? Doc vs. doc?
3. **Surface explicitly** - Don't silently choose one; document the conflict.
4. **Human decision** - Let human decide which should change (don't let agent assume).
5. **Update consistently** - Change subordinate sources to align with authoritative source.
6. **Record decision** - Document why one source was chosen as authoritative.

### 6.4 Deprecating Documentation

When documentation becomes obsolete:

1. **Mark as deprecated** - Add "DEPRECATED" marker at top.
2. **State reason** - Why is it obsolete? What replaced it?
3. **Provide redirect** - Link to replacement documentation if it exists.
4. **Don't delete immediately** - Keep for historical reference (minimum 30 days or one release cycle).
5. **Remove from catalog** - Update documentation_system_catalog.md.
6. **Archive eventually** - Move to an archive folder or delete after grace period.

### 6.5 Special Cases and Exemptions

#### 6.5.1 README.md (Repository Root)

The repository root `README.md` is EXEMPTED from:
- Metadata header requirements (use free-form structure optimized for first-time visitors)
- Versioning requirements

It MUST still:
- Follow universal formatting rules (section 2)
- Provide clear navigation to the documentation system
- Avoid duplicating authoritative content

#### 6.5.2 Decision Records (docs/decisions/)

Decision records follow `decision_records_standard.md` and are EXEMPTED from:
- Standard metadata headers (use decision-specific headers)

They MUST:
- Include decision status (Proposed, Accepted, Superseded)
- Include decision date
- Include rationale and alternatives considered

#### 6.5.3 Agent Profile Definitions (.github/agents/)

Agent profiles MUST:
- Use frontmatter for metadata (GitHub Copilot requirement)
- Include complete agent instructions in a single file (GitHub limitation)
- Reference but not duplicate standards

They are EXEMPTED from:
- Standard documentation metadata headers
- Canonical location statements (GitHub requires `.github/agents/`)

---

## 7) Compliance and Governance

### 7.1 Pre-Commit Validation

Validation tools MAY check:
- Metadata header completeness
- Prohibited patterns (open items sections, hardcoded timestamps)
- Version/timestamp format compliance
- Heading hierarchy
- Cross-reference validity

### 7.2 Human Review Checklist

When reviewing documentation changes, check that:
- Metadata header is complete and correctly formatted for document type
- Version/timestamp approach is consistent (not hybrid)
- No prohibited patterns present
- Content boundaries respected (no shadow specs)
- Cross-references use correct paths
- Changes align with versioning discipline
- Claims are backed by evidence or marked as TBD
- Unknowns and assumptions are explicit

### 7.3 Compliance Checking

Principles should be enforced through:
- **Automated validation:** Where possible (format checks, broken link detection)
- **Human review:** For semantic compliance (separation of concerns, authority)
- **Documentation review checklist:** Run after significant changes (see section 7.2)
- **Periodic audits:** Review documentation set against principles quarterly

### 7.4 Exceptions

Exceptions to principles may be granted if:
- Explicit rationale documented
- Alternatives considered and rejected with reasons
- Documented in decision record
- Approved by documentation maintainer
- Marked in the exceptional document (e.g., "Exception to principle X: rationale")

### 7.5 Principles Evolution

These principles themselves should evolve based on experience:
- **Proposal process:** Changes to principles require written proposal with rationale
- **Review:** Principles changes reviewed by documentation maintainers
- **Approval:** Requires explicit approval, documented in decision record
- **Communication:** Significant changes communicated to all contributors

### 7.6 Migration of Existing Documents

Existing documents that violate this specification:
- SHOULD be updated incrementally as they are edited
- MUST be migrated before adding new normative requirements
- Changes SHOULD be minimal (formatting/metadata only) to reduce noise

---

## 8) Examples

### 8.1 Correct Standards Document Header (with version)

```markdown
# Example Standard Specification

**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for example artifacts.
**Why necessary:** Ensures consistent structure across example artifacts.
**Must contain:** Required fields, validation rules, compliance checklist.
**Must not contain:** Tool command syntax, workflow procedures.
**Version:** 1.2.0
```

### 8.2 Correct Standards Document Header (with timestamp)

```markdown
# Example Standard Specification

UPD 2026-01-28
**Canonical location:** `docs/standards/`
**Purpose statement:** Defines the normative schema for example artifacts.
**Why necessary:** Ensures consistent structure across example artifacts.
**Must contain:** Required fields, validation rules, compliance checklist.
**Must not contain:** Tool command syntax, workflow procedures.
```

### 8.3 Correct Context Document Header

```markdown
# Example Context Document

## Purpose
This document defines the conceptual framework for the example subsystem.
It explains intent, roles, and operating principles without specifying
normative schemas or tool usage.
```

### 8.4 Incorrect: Hybrid Version/Timestamp (PROHIBITED)

```markdown
# Example Specification (v1.0)

UPD 2026-01-28 14:20
**Version:** 1.0.0
**Canonical location:** `docs/standards/`
...
```

**Problem:** Uses both timestamp and version number.

### 8.5 Incorrect: Open Items Section (PROHIBITED)

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

### 8.6 Per-Job File Structure Example

For a job `preprocessIncomingBmecat` in the `vendor_input_processing` group:

```
jobs/vendor_input_processing/preprocessIncomingBmecat/
├── job_manifest.yaml
├── glue_script.py
├── bus_description_preprocessIncomingBmecat.md
└── script_card_preprocessIncomingBmecat.md
```

**File naming follows conventions:**
- Manifest: `job_manifest.yaml` (fixed name)
- Script: `glue_script.py` (or as declared in manifest)
- Business description: `bus_description_<job_id>.md`
- Script card: `script_card_<job_id>.md`

**Metadata formatting:**
- YAML files: No metadata header
- Python files: Standard Python conventions
- Markdown files: Follow respective spec structure (business_job_description_spec.md or script_card_spec.md)

**For semantic rules (what each file contains), see `documentation_system_catalog.md`.**

---

## 9) Relationship to Other Documents

This specification addresses **format, structure, and governance principles**.

**Division of responsibility:**

- **`documentation_system_catalog.md`** (SEMANTIC CONTENT):
  - Defines document types and their purposes
  - Specifies what content belongs in each document type
  - Provides "Must contain" and "Must not contain" rules
  - THIS IS THE AUTHORITATIVE SOURCE FOR CONTENT RULES

- **`documentation_spec.md`** (FORMAT, STRUCTURE, GOVERNANCE - this document):
  - Defines foundational principles (single source of truth, separation of concerns, evidence-based claims, human authority, explicit over implicit)
  - Defines formatting conventions (Markdown, headings, lists)
  - Specifies metadata header formats
  - Defines versioning discipline
  - Provides structural and semantic anti-patterns
  - Defines quality criteria and governance procedures

- **`target_agent_system.md`**:
  - Defines separation of concerns principles for agent system
  - Specifies no double truth rule
  - This spec implements and extends those principles for documentation

- **`development_approach.md`**:
  - Defines development workflow
  - Applies principles from this spec to development process

- **`validation_standard.md`**:
  - May enforce rules from both catalog (content) and spec (format/principles)

- **`glossary.md`**:
  - Single source of truth for term definitions
  - Implements principle 1.1 (Single Source of Truth)

**Key principle:** Semantic content rules live in ONE place (documentation_system_catalog.md). Format, structure, and governance principles live in ONE place (this document). This prevents double truth.

---

## 10) Summary

### 10.1 Core Philosophy

**Documentation exists to enable informed decisions and effective action.**

Good documentation:
- ✅ Has a single source of truth for each concept
- ✅ Separates intent, rules, procedures, and operations into appropriate layers
- ✅ Makes explicit claims backed by evidence
- ✅ Respects human authority and agent assistance boundaries
- ✅ States unknowns and assumptions explicitly
- ✅ Minimizes duplication through references
- ✅ Maintains clear ownership and authority
- ✅ Tracks changes through versioning
- ✅ Composes modularly
- ✅ Follows consistent patterns

Bad documentation:
- ❌ Duplicates information in multiple places (double truth)
- ❌ Mixes layers (rationale in standards, schemas in process docs)
- ❌ Makes claims without evidence
- ❌ Assumes agent authority supersedes human approval
- ❌ Hides unknowns or makes silent assumptions
- ❌ Requires redundant updates in multiple places
- ❌ Has unclear or competing authority
- ❌ Lacks versioning or change tracking
- ❌ Is monolithic and hard to reference
- ❌ Varies format unpredictably

### 10.2 Key Rules

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

**Prohibited semantic patterns:**
- Circular documentation (document defining format it uses)
- Shadow specifications (normative requirements in wrong layer)
- Competing authority (same rule defined differently in multiple places)
- Implicit assumptions (unknowns treated as known)
- Stale references (broken cross-document links)

**For semantic content rules (what belongs in each document type):**
- See [documentation_system_catalog.md](../context/documentation_system_catalog.md)

---

**Compliance:** This specification takes effect immediately for new documents. Existing documents SHOULD migrate incrementally.

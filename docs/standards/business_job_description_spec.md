# Business Job Description Specification

## Purpose statement

This standard defines the normative structure and required sections for per-job business descriptions, ensuring that job purpose, scope boundaries, and business rules are captured consistently, auditably, and separately from operational implementation detail.

**Canonical location:** `docs/standards/business_job_description_spec.md`

**Related standards:**
- `docs/standards/script_card_spec.md` — operational behavior, invariants, failure modes
- `docs/standards/job_manifest_spec.md` — machine-readable interface contracts
- `docs/standards/naming_standard.md` — artifact and placeholder naming rules
- `docs/standards/artifacts_catalog_spec.md` — artifact content contracts
- `docs/standards/validation_standard.md` — evidence and verification rules
- `docs/standards/decision_records_standard.md` — exception and governance approval

**Supersedes:** None (initial normative version)

**Last major review:** 2026-01-30

---

## 0) Scope and document type alignment

### What a business job description is

A **business description** is a per-job documentation file that captures:
- the job's business purpose and rationale,
- what it does (inputs, outputs, processing logic) from a stakeholder perspective,
- business rules and constraints that affect results,
- explicit scope boundaries (what it does NOT do).

Location: `jobs/<job_group>/<job_id>/bus_description_<job_id>.md`

### What it is NOT

A business description is NOT:
- a machine-readable manifest (that is `job_manifest.yaml`)
- operational/runtime documentation (that is `script_card_<job_id>.md`)
- a data schema or artifact content contract (that is in `docs/catalogs/artifacts_catalog.md`)
- a tool manual or implementation guide

### Relationship to other per-job documents

- **Business description** (this spec): WHY the job exists, WHAT it does (business view), business rules
- **Script card** (`script_card_spec.md`): HOW it runs, operational invariants, failure modes, observability
- **Job manifest** (`job_manifest_spec.md`): machine-readable interface contract (parameters, S3 locations, placeholders)

When writing a business description:
- Reference the manifest for technical interface details (don't duplicate schemas)
- Reference the script card for operational behavior (don't duplicate runtime detail)
- Reference the artifacts catalog for content contracts (don't duplicate schemas)

### Alignment with development approach

Business descriptions document the business intent for a job. The specific workflow step where they are created or updated is not prescribed by this standard - they may be created during capability planning, implementation, or retrospective documentation as appropriate to the project context.

**Reference:** See `docs/context/development_approach.md` for the 5-step workflow and `docs/process/workflow_guide.md` for execution guidance.

### Documentation timing

**For new jobs (during development):**
Business descriptions capture intended behavior and approved business rules before/during implementation.

**For existing jobs (retroactive documentation):**
Business descriptions document observed behavior from code analysis and operational knowledge.
- Mark interpretations with `ASSUMPTION:`
- Mark uncertain behaviors with `TBD`
- If behavior contradicts apparent intent, document the contradiction in Section 8

---

## 1) Evidence and assumptions discipline

Business descriptions must follow the evidence discipline defined in `docs/context/target_agent_system.md` Section 3.2 and `docs/standards/validation_standard.md`.

**Summary for quick reference:**
- Use `TBD` for unknown facts that require investigation or runtime evidence
- Label interpretations with `ASSUMPTION:` and get explicit approval before implementation depends on them
- Use "Verified/Confirmed" only when explicit evidence exists

See Section 8 of this spec for application to business descriptions.

---

## 2) Required sections and structure

Business descriptions MUST use the following section structure. Section numbering is required for navigability and consistency.

### Section 1: Business purpose and context

**Must contain**

- Opening statement: A clear, concise statement of the job's business purpose (typically 1-2 sentences)
  - May use the label "Business purpose:" or integrate naturally into the opening paragraph
  - Should answer: "What business outcome does this job achieve?"
- Context: 1-3 additional sentences explaining business objective and what is produced
- Boundary statement: One explicit statement of what the job does NOT do
  - Use format: "Does not..." or "Boundary:..." or integrate into context

**Optional**

- Process landscape: Where the job sits in the overall workflow (or `TBD` if unknown)

---

### Section 2: Inputs (business view)

**Must contain**

- Plain-language list of required inputs, expressed as **business artifacts**, not storage details.
- For each required input: one short phrase describing what it represents.
- Behavior when inputs are missing or malformed:
  - "job fails" / "job continues with empty output" / "job skips the element"
  - If behavior differs for empty vs missing vs malformed, document each case

**Allowed format**

- Subsections are acceptable for clarity:
  - "Runtime parameters" for job invocation parameters
  - "Required input files" for data inputs
  - "Optional inputs" with behavior if absent
- Bullet list of artifact names + parenthetical meaning, e.g.:
  - `${vendor_name}_categoryMatchingProposals.json` (full proposals)
  - `${vendor_name}_categoryMatchingProposals_oneVendor_to_onePim_match.json` (1→1 subset)

**Note on placeholder notation:**
- PREFERRED: Use `${parameter_name}` format for consistency with manifests
- ACCEPTABLE: Use `<parameter_name>` for readability in prose
- Avoid: `{parameter_name}` (ambiguous)
- Be consistent within the document
- Reference: `docs/standards/naming_standard.md` Section 4.6

**Optional**

- Mention where the job gets the pointers from (e.g., "keys carried in run receipt/config") but without bucket/prefix patterns unless they are essential.

---

### Section 3: Outputs (business view)

**Must contain**

- Bullet list of produced artifacts with 1-line meaning each.
- Explicit mention of outcome type:
  - "NDJSON product feed", "JSON dictionary keyed by vendor_category_id", "status report", etc.
- If relevant: whether output is overwritten vs appended (as a business-operational fact).

---

### Section 4: Processing logic (business flow)

**Must contain**

- 4-12 steps in natural language, or logical parts with substeps
- Steps describe transformations that a stakeholder cares about:
  - "enriches products with ..."
  - "aggregates per vendor category ..."
  - "derives rules from stable training base ..."
  - "validates rules and updates reference ..."

**For complex jobs with multiple phases:**
- Use subsections (### PART 1, ### PART 2, etc.)
- Each part can have 2-6 steps
- Total combined should remain readable (aim for under 15 total steps across all parts)

**Must avoid**

- function names, class names, Spark operations (`explode`, `groupBy`) unless they are needed to understand a business rule.
- Detailed code-level implementation (that belongs in the script card or code comments).
- Tool command syntax or operational procedures.

---

### Section 5: Business rules and controls

**Must contain**

- Bullet list of rules that materially affect results:
  - selection/prioritization (e.g., "uses first match found")
  - exclusions (e.g., "filters out products without article_id")
  - thresholds (e.g., "requires minimum 3 products per category")
  - validation rules (e.g., "skips malformed records")
  - "truth protection" (e.g., "never overwrites existing canonical mappings")
  - "what is considered valid evidence"

---

### Section 6: What the job does not do

**Must contain**

- 1-6 bullets of explicit non-goals to prevent misinterpretation.

---

### Section 7: Operational notes (optional, use sparingly)

This section is optional and should be minimal. Use it ONLY for operational facts that materially affect business understanding and cannot be deferred to the script card.

**What belongs here (if anywhere):**

- Critical failure behavior that affects business continuity: "fails fast if ..."
- Output behavior that affects downstream consumption: "writes empty output and exits if ...", "overwrites the same output key each run"
- Monitoring/observability artifacts essential to business tracking: "creates run receipt / status artifacts for monitoring"

**What does NOT belong here:**

- Runtime configuration details (use script card)
- Detailed error handling and recovery (use script card)
- Performance characteristics (use script card)
- Deployment/infrastructure details (use script card or ops documentation)

**Reference:** For comprehensive operational detail, see the corresponding script card per `docs/standards/script_card_spec.md`.

---

### Section 8: Assumptions and TBDs

**Must contain**

- Anything not evidenced: `TBD`
- Any interpretation: explicitly labeled `ASSUMPTION`

---

## 3) Anti-patterns and what NOT to include

Per `docs/standards/documentation_spec.md` Section 5.3, business descriptions must avoid these patterns.

**Business description specific guidance:**

**Shadow specifications:**
- Do NOT duplicate manifest schemas (parameters, S3 patterns) — reference `job_manifest.yaml` instead
- Do NOT duplicate artifact content contracts — reference `docs/catalogs/artifacts_catalog.md` instead
- Do NOT redefine glossary terms — reference `docs/context/glossary.md` instead

**Tool manuals and operational procedures:**
- Do NOT include AWS Glue configuration steps
- Do NOT include deployment commands or infrastructure setup
- Do NOT include detailed error handling procedures (use script card)

**Code-level implementation detail:**
- Do NOT include function signatures or class hierarchies
- Do NOT include detailed algorithm implementations
- Do NOT include code snippets unless essential to explain a business rule

**Mixing layers:**
- Do NOT combine business rationale with operational troubleshooting
- Do NOT embed normative standards (e.g., naming rules, validation criteria)
- Keep business view separate from technical interface detail

**If in doubt:** Ask "Would a business stakeholder need this to understand what the job achieves?" If not, it belongs elsewhere.

---

## 4) Minimal template

```md
# <Job Name> — Business Description

## Section 1: Business purpose and context
This job [clear statement of business purpose and outcome].

[1-3 sentences providing context about business objective.]

Boundary: Does not [explicit non-goal].

## Section 2: Inputs (business view)
### Runtime parameters
- `PARAMETER_NAME` (meaning)

### Required input files
- `${vendor_name}_input_file.json` (meaning)

Behavior if missing: [job fails / continues with empty output / skips element]

### Optional inputs
- `optional_file.json` (meaning) — Behavior if absent: [...]

## Section 3: Outputs (business view)
- `${vendor_name}_output_file.json` — [meaning and type, e.g., "NDJSON product feed"]
- Output behavior: [overwrites / appends / creates new]

## Section 4: Processing logic (business flow)
1. [Business transformation step 1]
2. [Business transformation step 2]
3. [Business transformation step 3]
4. [Business transformation step 4]

## Section 5: Business rules and controls
- [Selection/prioritization rule]
- [Exclusion rule]
- [Validation rule]
- [Truth protection rule]

## Section 6: What the job does not do
- Does not [explicit non-goal 1]
- Does not [explicit non-goal 2]

## Section 7: Operational notes (optional)
- [Critical operational fact affecting business understanding, if any]

## Section 8: Assumptions and TBDs
- TBD: [unknown fact requiring investigation]
- ASSUMPTION: [interpretation requiring approval]
```

**Complete example:** See `jobs/vendor_input_processing/matching_proposals/bus_description_matching_proposals.md` for a reference implementation.

---

## 5) Cross-references

For technical details related to this job:
- Interface contract: see `job_manifest.yaml` in same directory
- Operational behavior: see `script_card_<job_id>.md` in same directory
- Artifact schemas: see `docs/catalogs/artifacts_catalog.md`
- Job inventory entry: see `docs/catalogs/job_inventory.md`

---

## 6) Governance and change control

### Version tracking

Business descriptions use git history for change tracking per `documentation_spec.md` Section 4.
- No explicit version numbers in the document
- Use git blame for line-level history
- Add `Last reviewed: YYYY-MM-DD` in frontmatter only if documenting an existing job retroactively

### Breaking changes

Changes to business descriptions are generally **non-breaking** (documentation updates do not affect runtime behavior). However, the following require decision records per `docs/standards/decision_records_standard.md`:

- Changing the documented business purpose in a way that contradicts approved capability definitions
- Adding/removing scope boundaries that affect approved acceptance criteria
- Changing business rules that would invalidate existing automation or approvals

### Exceptions and special cases

If a job requires deviation from this standard (e.g., highly specialized section structure):
1. Document the deviation reason in `## Section 8: Assumptions and TBDs`
2. Create a decision record per `docs/standards/decision_records_standard.md`
3. Reference the decision record in the business description
4. The deviation must be explicitly approved by a human

### Compliance validation

Business descriptions SHOULD be validated for:
- Presence of all required sections (Sections 1-6, 8)
- Use of consistent placeholder notation (either `${param}` or `<param>` but not mixed)
- No duplication of manifest/schema content
- No embedded tool manuals or code implementation
- Proper use of TBD/ASSUMPTION labels per Section 1

Validation may be manual (human review) or automated (linting/scanning tools).

---

## 7) Relationship to script card

To clarify boundaries between business descriptions and script cards:

| Aspect | Business Description | Script Card |
|--------|---------------------|-------------|
| Focus | WHY and WHAT (business) | HOW (operational) |
| Inputs | Business artifacts + meaning | Technical: bucket/key/format |
| Processing | Business transformations | Operational steps |
| Failure | Critical business impacts | All failure conditions |
| Audience | Business stakeholders | Operators and developers |

**Rule:** If it affects business understanding, document in business description. If it's needed to run/operate the job, document in script card. Some facts belong in both (minimal duplication is acceptable for critical operational facts).

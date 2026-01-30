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

---

## 1) Evidence and assumptions discipline

Per `docs/context/target_agent_system.md` and `docs/standards/validation_standard.md`:

**TBD (explicit unknown):**
- Use `TBD` for facts that are unknown and cannot be determined without additional investigation or runtime evidence.
- TBDs MUST be resolved before the job is considered production-ready, OR explicitly approved as acceptable unknowns with a decision record.

**ASSUMPTION (controlled assumption):**
- Use `ASSUMPTION:` label for interpretations or inferences that are not directly evidenced.
- Assumptions MUST be explicitly approved by a human before implementation depends on them.

**Verified / Confirmed:**
- Use these terms ONLY when explicit evidence exists (script analysis, manifest content, artifact inspection, or documented decisions).
- Otherwise, state "unknown" or use `TBD`.

---

## 2) Required sections and structure

Business descriptions MUST use the following section structure. Section numbering is required for navigability and consistency.

### Section 1: Business purpose and context

**Must contain**

* Business purpose (one sentence): <exactly one sentence; starts with this fixed label; must be the first non-empty line in this section>
* 1–3 sentences: business objective and what outcome is produced.
* One explicit boundary statement (“Does not …”).

**Optional**

* One sentence: where it sits in the overall process landscape (or `TBD`).

---

### Section 2: Inputs (business view)

**Must contain**

* Plain-language list of required inputs, expressed as **business artifacts**, not storage details.
* For each required input: one short phrase describing what it represents.
* Behavior when missing, only at the level of:

  * “job fails” / “job continues with empty output” / “job skips the element”.

**Allowed format (like the examples)**

* Bullet list of artifact names + parenthetical meaning, e.g.:

  * `${vendor_name}_categoryMatchingProposals.json` (full proposals)
  * `${vendor_name}_categoryMatchingProposals_oneVendor_to_onePim_match.json` (1→1 subset)

**Note on placeholder notation:**
- Use `${parameter_name}` format per `docs/standards/naming_standard.md` Section 4.6
- Examples: `${vendor_name}_products.json`, not `<vendor>_products.json`

**Optional**

* Mention where the job *gets* the pointers from (e.g., “keys carried in run receipt/config”) but without bucket/prefix patterns unless they are essential.

---

### Section 3: Outputs (business view)

**Must contain**

* Bullet list of produced artifacts with 1-line meaning each.
* Explicit mention of outcome type:

  * “NDJSON product feed”, “JSON dictionary keyed by vendor_category_id”, “status report”, etc.
* If relevant: whether output is overwritten vs appended (as a business-operational fact).

---

### Section 4: Processing logic (business flow)

**Must contain**

* 4–10 steps in natural language.
* Steps describe transformations that a stakeholder cares about:

  * “enriches products with …”
  * “aggregates per vendor category …”
  * “derives rules from stable training base …”
  * “validates rules and updates reference …”

**Must avoid**

* function names, class names, Spark operations (`explode`, `groupBy`) unless they are needed to understand a business rule.
* Detailed code-level implementation (that belongs in the script card or code comments).
* Tool command syntax or operational procedures.

---

### Section 5: Business rules and controls

**Must contain**

* Bullet list of rules that materially affect results:

  * selection/prioritization
  * exclusions
  * thresholds
  * “truth protection”
  * “what is considered valid evidence”

---

### Section 6: What the job does not do

**Must contain**

* 2–6 bullets of explicit non-goals to prevent misinterpretation.

---

### Section 7: Operational notes (optional, use sparingly)

This section is optional and should be minimal. Use it ONLY for operational facts that materially affect business understanding and cannot be deferred to the script card.

**What belongs here (if anywhere):**

* Critical failure behavior that affects business continuity: "fails fast if …"
* Output behavior that affects downstream consumption: "writes empty output and exits if …", "overwrites the same output key each run"
* Monitoring/observability artifacts essential to business tracking: "creates run receipt / status artifacts for monitoring"

**What does NOT belong here:**

* Runtime configuration details (use script card)
* Detailed error handling and recovery (use script card)
* Performance characteristics (use script card)
* Deployment/infrastructure details (use script card or ops documentation)

**Reference:** For comprehensive operational detail, see the corresponding script card per `docs/standards/script_card_spec.md`.

---


### Section 8: Assumptions and TBDs

**Must contain**

* Anything not evidenced: `TBD`
* Any interpretation: explicitly labeled `ASSUMPTION`

---

### Section 9: References

**Must contain**

* Script identifier/path (repo path or filename)
* Names of key artifacts referenced (inputs/outputs)
* Optional: link to run receipt / config artifact names (not S3 paths unless unavoidable)

---



---

## 5) Governance and change control

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
- Presence of all required sections (Sections 1-6, 8, 9)
- Use of proper placeholder notation (`${param}` not `<param>`)
- No duplication of manifest/schema content
- No embedded tool manuals or code implementation
- Proper use of TBD/ASSUMPTION labels per Section 1

Validation may be manual (human review) or automated (linting/scanning tools).

## 3) Anti-patterns and what NOT to include

Per `docs/standards/documentation_spec.md` Section 6, business descriptions MUST NOT:

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
Business purpose (one sentence): <...>
<1–3 sentences.>
Boundary: Does not ...

## Section 2: Inputs (business view)
Required inputs:
- <Artifact name> (<meaning>)
- <Artifact name> (<meaning>)
Notes: <e.g., “input pointers are taken from run receipt/config”>

Optional inputs:
- <Artifact name> (<meaning>) — Behavior if absent: <...>

## Section 3: Outputs (business view)
- <Artifact name> — <meaning>
- <Artifact name> — <meaning>

## Section 4: Processing logic (business flow)
1. ...
2. ...
3. ...

## Section 5: Business rules and controls
- ...
- ...

## Section 6: What the job does not do
- ...
- ...

## Section 7: Operational notes (optional)
- ...

## Section 8: Assumptions and TBDs
- TBD: ...
- ASSUMPTION: ...

## Section 9: References
- Script:
- Related artifacts:

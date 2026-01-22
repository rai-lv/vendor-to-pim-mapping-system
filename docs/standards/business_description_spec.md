## Business Description Standard for Jobs (v1.1)

**Purpose:** Framework for writing future business-level job descriptions in a consistent, readable way.

**Rule:** Describe what is done and why. Mention technical details only when they change business meaning (e.g., “fails if missing”, “writes empty result”, “overwrites”).

### 1) Business purpose and context

**Must contain**

* Business purpose (one sentence): <exactly one sentence; starts with this fixed label; must be the first non-empty line in this section>
* 1–3 sentences: business objective and what outcome is produced.
* One explicit boundary statement (“Does not …”).

**Optional**

* One sentence: where it sits in the overall process landscape (or `TBD`).

---

### 2) Inputs (business view)

**Must contain**

* Plain-language list of required inputs, expressed as **business artifacts**, not storage details.
* For each required input: one short phrase describing what it represents.
* Behavior when missing, only at the level of:

  * “job fails” / “job continues with empty output” / “job skips the element”.

**Allowed format (like the examples)**

* Bullet list of artifact names + parenthetical meaning, e.g.:

  * `<vendor>_categoryMatchingProposals.json` (full proposals)
  * `<vendor>_categoryMatchingProposals_oneVendor_to_onePim_match.json` (1→1 subset)

**Optional**

* Mention where the job *gets* the pointers from (e.g., “keys carried in run receipt/config”) but without bucket/prefix patterns unless they are essential.

---

### 3) Outputs (business view)

**Must contain**

* Bullet list of produced artifacts with 1-line meaning each.
* Explicit mention of outcome type:

  * “NDJSON product feed”, “JSON dictionary keyed by vendor_category_id”, “status report”, etc.
* If relevant: whether output is overwritten vs appended (as a business-operational fact).

---

### 4) Processing logic (business flow)

**Must contain**

* 4–10 steps in natural language.
* Steps describe transformations that a stakeholder cares about:

  * “enriches products with …”
  * “aggregates per vendor category …”
  * “derives rules from stable training base …”
  * “validates rules and updates reference …”

**Must avoid**

* function names, class names, Spark operations (`explode`, `groupBy`) unless they are needed to understand a business rule.

---

### 5) Business rules and controls

**Must contain**

* Bullet list of rules that materially affect results:

  * selection/prioritization
  * exclusions
  * thresholds
  * “truth protection”
  * “what is considered valid evidence”

---

### 6) What the job does not do

**Must contain**

* 2–6 bullets of explicit non-goals to prevent misinterpretation.

---

### 7) Operational notes (only if important)

This section is optional and should be short.
Include only if it affects operations materially:

* “fails fast if …”
* “writes empty output and exits if …”
* “overwrites the same output key each run”
* “creates run receipt / status artifacts for monitoring”

---

### 8) Assumptions and TBDs

**Must contain**

* Anything not evidenced: `TBD`
* Any interpretation: explicitly labeled `ASSUMPTION`

---

### 9) References

**Must contain**

* Script identifier/path (repo path or filename)
* Names of key artifacts referenced (inputs/outputs)
* Optional: link to run receipt / config artifact names (not S3 paths unless unavoidable)

---

## Minimal template (business style)

```md
# <Job Name> — Business Definition (v1.1)

## 1) Business purpose and context
Business purpose (one sentence): <...>
<1–3 sentences.>
Boundary: Does not ...

## 2) Inputs (business view)
Required inputs:
- <Artifact name> (<meaning>)
- <Artifact name> (<meaning>)
Notes: <e.g., “input pointers are taken from run receipt/config”>

Optional inputs:
- <Artifact name> (<meaning>) — Behavior if absent: <...>

## 3) Outputs (business view)
- <Artifact name> — <meaning>
- <Artifact name> — <meaning>

## 4) Processing logic (business flow)
1. ...
2. ...
3. ...

## 5) Business rules and controls
- ...
- ...

## 6) What the job does not do
- ...
- ...

## 7) Operational notes (optional)
- ...

## 8) Assumptions and TBDs
- TBD: ...
- ASSUMPTION: ...

## 9) References
- Script:
- Related artifacts:

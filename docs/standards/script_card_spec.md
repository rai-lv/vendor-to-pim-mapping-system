# Script Card Specification (v1.0) — Glue Job

## 0) Scope

A **Script Card** documents **one executable job** (one Glue job / one script entrypoint) as an **operational + interface reference**.

It is **not** a full artifact schema, and it is **not** the global glossary.

---

## 1) Normative requirements

### 1.1 Identity (MUST)

A Script Card MUST state:

1. `job_id` (the repo folder identifier of the job)
2. `glue_job_name` (exact AWS Glue job name, or `TBD` if unknown)
3. `runtime` (one of: `pyspark`, `python_shell`, `TBD`)
4. `repo_path` (path to the entry script in the repo)
5. `manifest_path` (path to `job_manifest.yaml` in the repo)

**Pass criterion:** all five fields present and non-empty; allowed value `TBD` only where stated.

---

### 1.2 Purpose (MUST)

A Script Card MUST contain 1–3 sentences describing:

* what the job produces or changes (outputs and/or side effects), and
* the primary transformation at a high level (e.g., “aggregates”, “maps”, “enriches”, “validates”).

**Pass criterion:** 1–3 sentences; contains at least one explicit reference to output(s) or side effect(s).

---

### 1.3 Trigger and Parameters (MUST)

A Script Card MUST list:

* “Triggered by” (value may be `TBD`)
* “Required parameters” as a comma-separated list of parameter names (or `TBD`)
* “Preconditions” (value may be `TBD`)

**Pass criterion:** all three lines present; if parameters are known they must be listed as names only (no descriptions).

---

### 1.4 Interface: Inputs (MUST)

For each input the job consumes, the Script Card MUST include a block containing exactly:

* bucket (or `TBD`)
* key_pattern (or `TBD`)
* format (or `TBD`)
* required (one of: `true`, `false`, `TBD`)
* meaning (short human description)

**Pass criterion:** at least one input block present; each block contains all five fields.

---

### 1.5 Interface: Outputs (MUST)

For each output the job produces, the Script Card MUST include a block containing exactly:

* bucket (or `TBD`)
* key_pattern (or `TBD`)
* format (or `TBD`)
* required (one of: `true`, `false`, `TBD`)
* meaning (short human description)
* consumers (`TBD` allowed)

**Pass criterion:** at least one output block present; each block contains all six fields.

---

### 1.6 Side Effects (MUST)

A Script Card MUST state:

* deletes_inputs (true/false/TBD)
* overwrites_outputs (true/false/TBD)
* other_side_effects (text or `TBD`)

**Pass criterion:** all three lines present.

---

### 1.7 High-level Processing (MUST)

A Script Card MUST provide **4–8 bullets** describing the job’s high-level steps.

Constraints:

* Bullets MUST be phrased as actions (verb-first).
* Bullets MUST NOT list implementation details (no function names, no column names, no code-level branches), unless essential to understand external behavior.

**Pass criterion:** 4–8 bullets; action phrasing; no code-level detail.

---

### 1.8 Invariants (MUST)

A Script Card MUST contain an “Invariants” section that is either:

* a list of 1+ invariants, OR
* a single bullet `- TBD`

Constraints:

* Any stated invariant MUST be externally meaningful (e.g., “writes two output files”, “output is JSON object”, “empty output possible”), not an internal algorithm statement.

**Pass criterion:** section present with either ≥1 invariant or exactly `- TBD`.

---

### 1.9 Failure Modes and Observability (MUST)

A Script Card MUST include:

* Failure conditions (as coded): text or `TBD`
* Logging/metrics (as coded): text or `TBD`
* Run receipt: text or `TBD`
* Operator checks (S3 artifacts to verify): text or `TBD`

**Pass criterion:** all four lines present.

---

### 1.10 References (MUST)

A Script Card MUST include:

* job_manifest: path
* artifacts_catalog entries: text or `TBD`
* upstream jobs: text or `TBD`
* downstream jobs: text or `TBD`

**Pass criterion:** all four lines present.

---

## 2) Explicit exclusions (MUST NOT)

A Script Card MUST NOT:

1. Define global terms that apply across multiple jobs (belongs in glossary).
2. Provide full JSON schema / field-by-field structure of outputs (belongs in artifact catalog / schemas).
3. Propose future improvements or refactors (Phase 1 documentation is descriptive).
4. Include speculative statements; if unknown, use `TBD`.

---

## 3) Where “pipeline role” and “what’s inside” belong (unambiguous)

* A Script Card MUST include **one sentence** of “why it exists” **only if** this can be stated without introducing cross-job definitions.
  If not known, it MUST remain `TBD` via the “Triggered by/Preconditions” or Purpose phrasing.
* “What’s inside” outputs in detail (top-level structure + key fields) MUST be documented in **Artifact Catalog**; the Script Card MUST only provide **short meaning** plus a reference.

# System Context — Vendor→PIM Mapping Monorepo (Context Pack)

## Purpose of this document
This document is the single, stable reference for:
- what the GitHub repository contains,
- how development is planned and executed with ChatGPT + Codex,
- which artifacts are authoritative for which kinds of truth,
- which working rules are non-negotiable.

Its job is to prevent drift: whenever a future discussion or Codex task conflicts with this document, this document wins unless explicitly updated.

---

## Repository objective
Build and evolve a repeatable pipeline that maps incoming vendor assortments (BMECAT products + vendor categories) into the PIM data model, including:
- vendor category → PIM category mapping (rule-based, self-learning),
- vendor product → PIM category assignment when category mapping is missing/insufficient,
- generation of onboarding/upload artifacts for the PIM process.

Pipeline is implemented via AWS S3 + AWS Glue scripts, orchestrated by Make.com scenarios, with code changes produced via Codex PRs in GitHub and deployed manually to Glue.

---

## Truth sources and “what to trust”
### Code truth
- `jobs/<job_id>/glue_script.py` is the source of truth for runtime behavior.

### Interface truth (automation-relevant)
- `jobs/<job_id>/job_manifest.yaml` is the source of truth for:
  - parameters,
  - S3 inputs (including required/optional),
  - S3 outputs (including required/optional),
  - side effects (deletes/overwrites),
  - run receipt behavior and counters (if present).

Manifests must be evidence-based (derived from the script). No guessing.

### Business intent truth
- `docs/script_cards/<job_id>.md` explains “what the job is” and “why it exists” in business terms.
- Definitions shared across jobs must live in `docs/glossary.md` (not duplicated per script card).

### Standards truth
Rules that control naming, manifest fields, script-card structure, and Codex-task structure live under:
- `docs/standards/`

If a Codex task, a manifest, or a script card conflicts with a standard, the standard wins.

---

## Repository structure (authoritative)
### Root
- `README.md`: short repo overview + pointers to the key docs.
- `CHANGELOG.md`: high-level change log (optional, but recommended).

### Jobs
`jobs/<job_id>/` contains everything directly tied to one Glue job.

Required files per job:
- `glue_script.py` — deployed Glue code.
- `job_manifest.yaml` — machine-readable contract derived from the script.
- (optional) `configs/` — repo mirror of static S3 configs used by the job, if you choose to maintain mirrors.
- (optional) `samples/` — tiny redacted examples for debugging/review.

### Documentation
- `docs/glossary.md` — canonical definitions (matching proposal, StableTrainingSet, Category_Mapping_Reference, etc.)
- `docs/script_cards/<job_id>.md` — job business description (must comply with script-card spec)
- `docs/standards/` — specs that Codex tasks must reference for verification
  - `naming_standard_v1.md`
  - `manifest_spec_v1.md`
  - `script_card_spec_v1.md`
  - `run_receipt_spec_v1.md` (if used)
  - `codex_task_spec_v1.md`
- `docs/context_packs/`
  - `system_context.md` (this file)
  - optional objective-specific context packs if needed
- `docs/codex/`
  - `task_template_v1.md`
  - `pr_review_checklist.md`
  - the current manifest-generation task (e.g., `create-update-job-manifest_v1.3.txt`)

Cross-job overview docs (kept consistent with manifests and script cards):
- `docs/pipeline_inventory.md`
- `docs/artifacts_catalog.md`
- `docs/execution_map.md`

### Decisions
- `docs/decisions/ADR-xxxx-*.md` — architecture decisions and rationale (monorepo choice, config-vs-artifact classification rule, bucket contract, etc.)

---

## Naming rules (high level)
Authoritative detail belongs in `docs/standards/naming_standard_v1.md`. The non-negotiable basics:
- `job_id` = folder name under `jobs/`.
- Glue deployed script file can be named `glue_script.py` in the repo even if Glue uses another name; the `job_manifest.yaml` must define the entrypoint filename actually used in the repo job folder.
- S3 artifact naming patterns must be documented exactly as produced/consumed (including suffixes like `_oneVendor_to_onePim_match.json`).

---

## Working approach: objective → plan → elements → Codex tasks → deploy
This is the expected operating loop.

### Step 1 — Define objective (human)
You define the objective in precise terms:
- what must be achieved,
- what is explicitly out of scope,
- how success is verified (testable criteria).

### Step 2 — Plan (ChatGPT-assisted, evidence-based)
Planning output must be explicit:
- required system changes (jobs impacted, new jobs, new configs, new artifacts),
- dependencies and ordering,
- risks and unknowns called out explicitly.

### Step 3 — Decompose into elements-to-be-developed (ChatGPT-assisted)
Each element is small enough to be implemented as a Codex PR without ambiguity.
Each element must have:
- target repo paths,
- allowed changes (file list),
- acceptance criteria.

### Step 4 — Codex task creation (ChatGPT-assisted)
Codex tasks must:
- reference the relevant standards under `docs/standards/`,
- state the target script/path once (TARGET_SCRIPT pattern),
- restrict edits to an explicit file set,
- include quality gates that can be checked from repo contents.

### Step 5 — Execution via Codex PR (Codex)
Codex creates a PR against the repo.

### Step 6 — PR review (human with checklist)
Use `docs/codex/pr_review_checklist.md`.
No merge if:
- standards are violated,
- manifests omit external reads/writes,
- requiredness is wrong,
- outputs are incomplete,
- job behavior is changed when the task scope forbids it.

### Step 7 — Deploy (human)
You manually update the script version in AWS Glue.

### Step 8 — Update documentation (Codex task or human)
When required, documentation artifacts are generated/updated via Codex tasks that are constrained by specs.

---

## Non-negotiable quality rules
- No claim of verification unless the underlying file content was actually checked.
- No “assumption presented as fact”. Anything not provable from provided code/docs must be labeled TBD or as an explicit assumption (and assumptions require your approval before being used as a basis for further design decisions).
- Use only capabilities confirmed by documentation or observed behavior of the system in question (Glue/Make/NocoDB/etc.).
- When “review documentation” is requested, it means full-page, section-by-section processing (no selective scanning).
- Changes must preserve previously locked/confirmed structures and logic unless explicitly authorized.

---

## How ChatGPT and Codex use repository context (practical constraint)
ChatGPT in the chat does not automatically have access to your private GitHub repo contents.
To avoid drift:
- In chat, provide files by attaching them or pasting relevant excerpts when asking for analysis.
- In Codex tasks (running with repo access), explicitly instruct Codex to read specific repo paths (TARGET_SCRIPT + referenced standards).

---

## When and how this document may be updated
This file may be updated only when you explicitly decide to change:
- repo structure,
- planning/execution workflow,
- artifact roles,
- non-negotiable rules.

Updates must be reflected in `docs/standards/` if they affect specs, and optionally recorded as an ADR if the change is architectural.

# System Context — AI-Supported Data Automation Monorepo (Context Pack) — v1.1

## Purpose of this document
This document is the single, stable reference for:
- what the GitHub repository contains,
- how development is planned and executed with ChatGPT + Codex,
- which artifacts are authoritative for which kinds of truth,
- which working rules are non-negotiable.

Whenever a future discussion, Codex task, or PR conflicts with this document, this document wins unless explicitly updated.

---

## Repository objective (universal)
Maintain a monorepo for data-automation jobs (e.g., AWS Glue scripts, optional Lambda helpers, Make.com orchestration interfaces) with a repeatable AI-supported way of working:

- You define the objective.
- ChatGPT helps plan what is required to reach it.
- The plan is decomposed into small, testable development elements.
- ChatGPT produces Codex tasks to implement those elements via PRs.
- Documentation is created/updated as part of the same workflow (via Codex tasks when applicable).

### Current primary use case (example, not a limitation)
A major use case currently managed in this repo is **vendor→PIM assortment mapping** (BMECAT ingestion, category mapping, rule training, onboarding artifacts). This use case must not constrain the repo structure or process: the system is intended to support additional pipelines as well.

---

## Truth sources and “what to trust”
### Code truth
- `jobs/<job_id>/glue_script.py` is the source of truth for runtime behavior.

### Interface truth (automation-relevant)
- `jobs/<job_id>/job_manifest.yaml` is the source of truth for:
  - parameters,
  - S3 inputs (required/optional),
  - S3 outputs (required/optional),
  - side effects (deletes/overwrites),
  - run receipt behavior and counters (if present).

Manifests must be evidence-based (derived from the script). No guessing.

### Business description truth (current reality vs intended artifact)
There are two different concepts:

1) **Business descriptions (current reality)**
- Job business descriptions may exist as free text documents (for example in `docs/business_descriptions/`).
- These are valid input material for planning and for creating structured docs, but they are not a strict standard artifact unless you enforce a spec for them.

2) **Script cards (intended standardized artifact)**
- A script card is a standardized job description that complies with `docs/standards/script_card_spec_v1.0.md` (or its successor).
- Script cards are stored under `docs/script_cards/<job_id>.md`.
- A script card is “authoritative for business intent” only when it exists and complies with the spec.

Definitions shared across jobs must live in `docs/glossary.md` (not duplicated per job card).

### Standards truth
Rules that control naming, manifest fields, script-card structure, and Codex-task structure live under:
- `docs/standards/`

If a Codex task, a manifest, or a script card conflicts with a standard, the standard wins.

---

## Repository structure (authoritative)
### Root
- `README.md`: short repo overview + pointers to key docs.
- `CHANGELOG.md`: high-level changes (optional).

### Jobs
`jobs/<job_id>/` contains everything directly tied to one job.

Required files per job:
- `glue_script.py` — deployed Glue code.
- `job_manifest.yaml` — machine-readable contract derived from the script.

Optional per job (used only if you decide to maintain them):
- `configs/` — repo mirror of static S3 configs used by the job (only if you enforce this convention).
- `samples/` — tiny redacted examples for debugging/review.

### Documentation
Core docs:
- `docs/glossary.md` — canonical definitions (shared terms).
- `docs/context_packs/system_context.md` — this file.
- `docs/standards/` — specs Codex tasks must reference for verification.

Job intent docs:
- `docs/script_cards/<job_id>.md` — standardized script cards (only when present and spec-compliant).
- `docs/business_descriptions/` — non-standard business descriptions, if you keep them.

Codex task assets:
- `docs/codex-tasks/` — templates, checklists, and task prompt files used to drive PR creation:
  - `task_template_v1.md`
  - `pr_review_checklist.md`
  - task prompts such as `create-update-job-manifest_v1.3.txt` (or newer)

Cross-job overview docs (kept consistent with manifests and script cards where available):
- `docs/pipeline_inventory.md`
- `docs/artifacts_catalog.md`

Optional operational doc (only if you decide it is needed and define a spec for it):
- `docs/execution_map.md` — runbook-style orchestration view. Not mandatory unless explicitly adopted.

### Decisions
- `docs/decisions/ADR-xxxx-*.md` — architecture decisions and rationale (monorepo, bucket contract, config-vs-artifact rules, etc.)

---

## Working approach (planning & execution)
This is the expected operating loop.

### Step 1 — Define objective (human)
Objective must include:
- what must be achieved,
- explicit out-of-scope boundaries,
- success criteria that can be tested.

### Step 2 — Plan (ChatGPT-assisted, evidence-based)
Planning output must be explicit:
- required changes (jobs impacted, new jobs, new artifacts, new configs),
- dependencies and ordering,
- risks and unknowns called out explicitly.

### Step 3 — Decompose into development elements (ChatGPT-assisted)
Each element must be small enough for one Codex PR and must specify:
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
Use `docs/codex-tasks/pr_review_checklist.md`.
No merge if:
- standards are violated,
- manifests omit external reads/writes,
- requiredness is wrong,
- outputs are incomplete,
- job behavior is changed when the task scope forbids it.

### Step 7 — Deploy (human)
You manually update the script version in AWS Glue.

### Step 8 — Documentation update (Codex task or human)
When required, documentation artifacts are created/updated via Codex tasks constrained by specs.

---

## Non-negotiable quality rules
- No claim of verification unless the underlying file content was actually checked.
- No “assumption presented as fact”. Anything not provable from provided code/docs must be labeled TBD or as an explicit assumption (assumptions require your approval before they are used as a basis for further decisions).
- Use only capabilities confirmed by documentation or observed system behavior (Glue/Make/NocoDB/etc.).
- When “review documentation” is requested, it means full-page, section-by-section processing (no selective scanning).
- Changes must preserve previously locked/confirmed structures and logic unless explicitly authorized.

---

## How ChatGPT and Codex use repository context (practical constraint)
ChatGPT in chat does not automatically have access to your private GitHub repo contents.
To avoid drift:
- In chat, provide files by attaching them or pasting relevant excerpts when asking for analysis.
- In Codex tasks (with repo access), instruct Codex to read specific repo paths (TARGET_SCRIPT + referenced standards).

---

## When and how this document may be updated
This file may be updated only when you explicitly decide to change:
- repo structure,
- planning/execution workflow,
- artifact roles,
- non-negotiable rules.

If the update affects a standard, the corresponding file under `docs/standards/` must be updated as well. Record architectural changes as ADRs when appropriate.

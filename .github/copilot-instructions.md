# Copilot Instructions for vendor-to-pim-mapping-system

## Repository Overview

This is an AI-supported data automation monorepo for AWS Glue jobs (and optional Lambda helpers, Make.com orchestration) focused on vendor→PIM assortment mapping. The repository uses ChatGPT + Codex for planning and development.

## Key Documentation Files

**ALWAYS** consult these files before making changes:

- `docs/context_packs/system_context.md` — the single source of truth for repo structure, workflow, and non-negotiable rules
- `docs/standards/` — specifications that control naming, manifest fields, script-card structure, and Codex-task structure
- `docs/glossary.md` — canonical definitions for shared terms

## Repository Structure

```
jobs/<job_group>/<job_id>/
  ├── glue_script.py          # Source of truth for runtime behavior
  ├── job_manifest.yaml       # Source of truth for interface (params, I/O, side effects)
  ├── configs/                # Optional: S3 config mirrors
  └── samples/                # Optional: redacted examples

docs/
  ├── context_packs/system_context.md    # Master context document
  ├── standards/                          # Specifications
  ├── business_job_descriptions/          # Business intent docs
  ├── script_cards/                       # Operational reference docs
  ├── job_inventory.md                    # Job index
  ├── artifacts_catalog.md                # Cross-job artifacts
  └── glossary.md                         # Shared definitions

tools/
  └── validate_repo_docs.py              # Standards validation script
```

## Truth Sources (Authority Hierarchy)

1. **Code Truth**: `jobs/<job_group>/<job_id>/glue_script.py` is authoritative for runtime behavior
2. **Interface Truth**: `jobs/<job_group>/<job_id>/job_manifest.yaml` is authoritative for parameters, S3 inputs/outputs, side effects, and run receipts
3. **Standards Truth**: Files under `docs/standards/` override everything else for naming, structure, and validation rules
4. **Business Description Truth**: `docs/business_job_descriptions/<job_id>.md` is authoritative for business intent (why), business logic, and boundaries
5. **Script Card Truth**: `docs/script_cards/<job_id>.md` is authoritative for operational interface and observable behavior

**Rule**: If a Codex task, manifest, or script card conflicts with a standard, the standard wins.

## Standardized Artifacts (Do Not Confuse)

There are **two different** business-facing documentation types:

1. **Business Job Descriptions** (`docs/business_job_descriptions/<job_id>.md`)
   - Spec: `docs/standards/business_job_description_spec.md`
   - Purpose: Business intent, why the job exists, business rules, boundaries
   - Excludes: Technical storage details unless they affect business meaning

2. **Script Cards** (`docs/script_cards/<job_id>.md`)
   - Spec: `docs/standards/script_card_spec.md`
   - Purpose: Operational interface, parameters, I/O blocks, side effects, failure modes
   - Must NOT: Define global terms, include full output schemas

**Important**: Definitions shared across jobs belong in `docs/glossary.md`, NOT duplicated per job doc.

## Critical Rules When Making Changes

### Job Manifest Rules

- Manifests must use `${NAME}` placeholder style (NOT `<name>` or `{name}`)
- Manifests must be evidence-based (derived from script + deployment config)
- Never guess at manifest content — verify from actual code

### Code Changes

- Preserve existing functionality unless explicitly authorized to change it
- Do not assume capabilities unless confirmed by documentation or observed behavior
- Python code for AWS Glue jobs uses PySpark and boto3

### Documentation Changes

- Never duplicate definitions — use `docs/glossary.md` for shared terms
- Business descriptions and script cards serve different purposes — keep them distinct
- Always comply with the relevant spec under `docs/standards/`

### Standards Validation (CI Gate)

Every PR must pass automated validation:

```bash
python tools/validate_repo_docs.py --all
```

This runs automatically via `.github/workflows/validate_standards.yml`. A PR must not be merged if validation fails.

## Development Workflow

The expected workflow has **two planning layers** before code changes:

1. **Define Objective** — what must be achieved, out-of-scope boundaries, success criteria
2. **Overarching Plan** — pipeline-level capabilities, decision points, artifacts
3. **Capability Plan** — step-level inputs/outputs, rules, acceptance criteria
4. **Decompose** — break into small elements for individual PRs
5. **Codex Task** — reference standards, restrict file changes, include quality gates
6. **Execute PR** — Codex creates PR
7. **PR Review** — use `docs/codex-tasks/pr_review_checklist.md`
8. **Deploy** — manual AWS Glue update
9. **Documentation Update** — via Codex task or human

## Non-Negotiable Quality Rules

- **No claim of verification unless file content was actually checked**
- **No "assumption presented as fact"** — label unknowns as TBD or explicit assumptions
- Use only confirmed capabilities (Glue/Make/NocoDB/etc.)
- Preserve previously locked/confirmed structures unless explicitly authorized
- When asked to "review documentation," process it section-by-section (no selective scanning)

## Technology Stack

- **Runtime**: AWS Glue (PySpark)
- **Language**: Python 3.x
- **Infrastructure**: AWS S3, AWS Glue
- **Orchestration**: Make.com (optional)
- **Planning**: ChatGPT + Codex
- **Validation**: Python-based standards validator (`tools/validate_repo_docs.py`)

## Common Tasks

### Adding a New Job

1. Create `jobs/<job_group>/<job_id>/glue_script.py`
2. Create `jobs/<job_group>/<job_id>/job_manifest.yaml` (use `${PLACEHOLDER}` style)
3. Optionally create business description: `docs/business_job_descriptions/<job_id>.md`
4. Optionally create script card: `docs/script_cards/<job_id>.md`
5. Run validation: `python tools/validate_repo_docs.py --all`

### Updating Documentation

1. Check the relevant spec in `docs/standards/`
2. Update the document per spec requirements
3. Add shared terms to `docs/glossary.md` (never duplicate in individual docs)
4. Run validation: `python tools/validate_repo_docs.py --all`

### Updating a Job Manifest

1. Review the script's actual parameters, inputs, outputs, and side effects
2. Update `job_manifest.yaml` with evidence-based content
3. Ensure placeholder style is `${NAME}` (strict requirement)
4. Run validation: `python tools/validate_repo_docs.py --all`

## Best Practices

1. **Read before writing**: Always read `docs/context_packs/system_context.md` before making structural changes
2. **Follow the standards**: Check `docs/standards/` for the spec relevant to what you're creating/updating
3. **Validate early**: Run `python tools/validate_repo_docs.py --all` as soon as you make changes
4. **Don't duplicate**: Use `docs/glossary.md` for shared definitions
5. **Evidence-based**: Derive manifests and documentation from actual code, not assumptions
6. **Respect boundaries**: Business descriptions and script cards have different scopes — don't mix them
7. **Check truth hierarchy**: When conflicts arise, standards win, then code/manifest, then documentation

## When in Doubt

If you're unsure about:
- **Repository structure**: Refer to `docs/context_packs/system_context.md`
- **Documentation format**: Check the relevant spec in `docs/standards/`
- **Shared terminology**: Check `docs/glossary.md`
- **Workflow/process**: Follow the development workflow in system_context.md
- **Validation rules**: Run `python tools/validate_repo_docs.py --all` and read its output

---

*These instructions help GitHub Copilot understand this repository's specific conventions, standards, and workflows. Always prioritize following the documented standards and truth sources.*

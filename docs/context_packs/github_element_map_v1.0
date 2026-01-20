vendor-to-pim-mapping-system/
  README.md
  CHANGELOG.md

  docs/
    pipeline_inventory.md          # factual index of jobs (what exists)
    artifacts_catalog.md           # factual catalog of produced files (what exists)
    execution_map.md               # factual Make → Glue wiring (if known)
    glossary.md                    # canonical term definitions (as used today)
    naming-standard.md             # current naming conventions (as-is)
    context_packs/
      vendor_to_pim_mapping.md     # 1-page truth: scope + links to docs + guardrails
    script_cards/
      <job1>.md                    # one per job: factual I/O + side effects + invariants
      <job2>.md
      <job3>.md
    codex/
      context_header_template.md   # paste block for every Codex task
      task_template.md             # one task = one PR template
      pr_review_checklist.md       # operator-friendly PR checklist
    decisions/
      ADR-0001-monorepo.md         # the monorepo decision (only this for phase 1)

  jobs/
    <job1>/
      glue_script.py               # the deployed script (as-is)
      job_manifest.yaml            # factual I/O + parameters (as observed)
      configs/                     # only configs used by this job (as-is)
      samples/                     # optional: tiny redacted inputs/outputs (if available)
    <job2>/
      glue_script.py
      job_manifest.yaml
      configs/
      samples/
    <job3>/
      glue_script.py
      job_manifest.yaml
      configs/
      samples/

  .github/
    pull_request_template.md       # forces doc updates + scope discipline

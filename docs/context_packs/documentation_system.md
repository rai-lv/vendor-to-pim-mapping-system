# Documentation System Metadata

**Version:** 1.1  
**Last Updated:** 2026-01-27  
**Purpose:** Centralized metadata catalog of all repository documentation, establishing objectives, roles, and scope for each document. Aligned with locked truth principles in `development_approach.md`.

---

## Overview

This repository contains **32 markdown documentation files** organized into a sophisticated, multi-layered documentation system that supports an **agent-assisted** development workflow with **mandatory human oversight**. The documentation follows a clear authority hierarchy (code → manifests → standards → descriptions → script cards) and uses normative specifications to ensure consistency and compliance.

**Key Governance Principle:** This documentation system reflects the core principle from `development_approach.md` that **agents are collaborators, not autonomous actors**. All agent-generated outputs require human review and approval before becoming authoritative.

### Documentation Organization

The documentation is organized into **5 functional layers**:

1. **Context Layer** (4 files) — Foundation documents establishing repository structure, workflows, and principles
2. **Process Layer** (3 files) — Workflow guides and agent setup instructions
3. **Governance Layer** (7 files) — Normative specifications that control structure and compliance
4. **Planning & Implementation Layer** (2 files) — Guides for creating planning and specification documents
5. **Artifact Layer** (16 files) — Job-specific documentation, catalogs, GitHub integration, and operational guides

---

## Documentation Inventory

### Context Layer (Foundation)

#### 1. System Context (`docs/context_packs/system_context.md`)

**Objective:** Establish the single source of truth for repository organization, structure, authority hierarchy, and development workflows.

**Role:** Master context document that defines the repository's purpose, non-negotiable rules, and comprehensive workflow options (manual, Codex-assisted, and agent-assisted with human oversight).

**Scope:**
- Repository objective and structure (`jobs/`, `docs/`, `tools/` directories)
- Three complementary development workflows
- Truth source hierarchy (code > manifests > standards > business descriptions > script cards)
- Critical rules for manifest format (`${NAME}` placeholder style), code changes, and documentation
- Technology stack (AWS Glue, PySpark, boto3, Make.com, NocoDB)
- Common tasks (adding new jobs, updating documentation, updating manifests)
- Best practices and when-in-doubt guidance

---

#### 2. Agent System Context (`docs/context_packs/agent_system_context.md`)

**Objective:** Provide detailed agent-specific workflows, responsibilities, and governance mechanisms ensuring human oversight.

**Role:** Supporting reference document for `system_context.md` that explains how agents **assist humans** within the repository and support the agent-assisted development workflow (v1.3) with mandatory human approval gates.

**Scope:**
- Agent roles and responsibilities as **assistants** (Planner, Pipeline Planner, Capability Planner, Coding, Testing, Documentation)
- Agent workflows with **human oversight and approval requirements**
- Agent integration with the 5-step development process
- Governance principles: human-agent collaboration, manual checkpoints, approval gates

---

#### 3. Development Approach (`docs/context_packs/development_approach.md`)

**Objective:** Define core development principles and the sequential development process. **This is the locked truth document that establishes foundational governance.**

**Role:** **Foundational governance document** that establishes principles (human-agent collaboration, iterative workflows, governance hierarchy) and explains the "why" and "how" of the repository's development methodology. **All other documents must align with this locked truth.**

**Scope:**
- Core principles (agents as collaborators not autonomous actors, sequential workflows, balance of automation and human oversight)
- Sequential 5-step development process overview (Steps 1-5)
- Agent context emphasizing assistance role
- Mandatory manual oversight and checkpoints
- Governance hierarchy: human inputs > standards > automated outputs
- References to where specifics live (standards, governance, agent charters)

---

#### 4. GitHub Element Map (`docs/context_packs/github_element_map.md`)

**Objective:** Map GitHub repository structure to conceptual documentation elements and governance hierarchy.

**Role:** Integration guide between GitHub organization and documentation system; provides visual representation of repository organization **with governance hierarchy annotations**.

**Scope:**
- Repository folder structure with governance layer annotations
- Mapping of conceptual elements to physical locations
- 5-level governance hierarchy (human inputs > standards > code truth > documentation > automated outputs)
- Human approval artifact locations
- Agent-generated vs. human-defined content distinctions
- Navigation guide for different user types

---

### Process Layer (Workflows)

#### 5. 5-Step Workflow Guide (`docs/workflows/WORKFLOW_5_STEPS.md`)

**Objective:** Provide a complete, authoritative guide to the 5-step development workflow enforced in this repository.

**Role:** Primary process guide for developers detailing each step, required outputs, and progression criteria.

**Scope:**
- 5-step workflow overview with visual flow diagram
- Step 1: Define Objective (Planner Agent)
- Step 2a: Overarching Plan (Pipeline Planner Agent)
- Step 2b: Capability Plan (Capability Planner Agent)
- Step 3: Decompose into Elements (Coding Agent)
- Step 4: Create Codex Tasks (Coding Agent)
- Step 5: Code Creation (PR process)
- Workflow enforcement rules and best practices
- Quick reference table and example flow

---

#### 6. Workflow Diagram (`docs/workflows/WORKFLOW_DIAGRAM.md`)

**Objective:** Provide visual representations of workflow architecture, trigger matrix, quality gates, and agent flow.

**Role:** Visual complement to `WORKFLOW_5_STEPS.md`—provides diagrams and integration details.

**Scope:**
- Development lifecycle diagram (ASCII visualization)
- Agent flow and dependencies
- Trigger matrix (manual vs automated)
- File flow across steps
- Quality gates and enforcement mechanisms
- Agent automation levels (fully automated, semi-automated, manual)
- Directory ownership mapping
- Success metrics
- Integration with existing systems

---

#### 7. Agents Setup Guide (`docs/workflows/AGENTS_SETUP.md`)

**Objective:** Provide comprehensive guide to agent installation, usage, and integration.

**Role:** Operational reference for developers using agent tools in the development workflow.

**Scope:**
- Agent overview (6 agents: Planner, Pipeline Planner, Capability Planner, Coding, Testing, Documentation)
- Quick start guide for 5-step workflow
- Detailed agent-by-agent setup and usage instructions
- CLI command examples for each agent
- Workflow automation (automatic triggers and manual triggers)
- Directory structure requirements
- Development workflow integration
- Best practices and troubleshooting

---

### Governance Layer (Standards & Specifications)

#### 8. Job Manifest Specification (`docs/standards/job_manifest_spec.md`)

**Objective:** Define the normative schema, structure, and rules for all job manifest files.

**Role:** Normative specification that all `job_manifest.yaml` files must comply with; enforced via automated validation.

**Scope:**
- Purpose and scope of job manifests (machine-readable interface contracts)
- Location and naming conventions (`jobs/<job_group>/<job_id>/job_manifest.yaml`)
- Design principles (deterministic extraction, stable patterns, uniform fields)
- Complete schema with required and optional keys
- Normative definitions (TBD markers, runtime enum, parameters, inputs, outputs, config_files, side_effects, logging_and_receipt, notes)
- Format semantics (JSON vs NDJSON decision rules)
- Placeholder and pattern rules (`${NAME}` style required, no `<name>` or `{name}`)
- Sourcing rules (evidence-based, derived from actual code)
- Alignment rules with other documents
- Compliance checklist
- Minimal template

---

#### 9. Script Card Specification (`docs/standards/script_card_spec.md`)

**Objective:** Define normative structure and content requirements for operational reference documentation (script cards).

**Role:** Normative specification for operational documentation per job; complements business job descriptions.

**Scope:**
- Scope definition (documents one executable job)
- Normative requirements: Identity, Purpose, Trigger/Parameters, Inputs, Outputs, Side Effects, High-level Processing, Invariants, Failure Modes, References
- Explicit exclusions (no global term definitions, no full schemas, no speculation)
- Guidance on "pipeline role" and "what's inside" (minimal "why", defer detail to artifacts catalog)
- Pass criteria for each required section
- Strict separation of concerns (operational vs business)

---

#### 10. Business Job Description Specification (`docs/standards/business_job_description_spec.md`)

**Objective:** Define normative structure for business-level job documentation.

**Role:** Normative specification for business intent documentation; focuses on "why" rather than "how."

**Scope:**
- 9 required sections: Business Purpose, Inputs, Outputs, Processing Logic, Business Rules, Exclusions, Operational Notes, Assumptions/TBDs, References
- "Must contain" and "optional" guidance for each section
- Business framing principles (why, not how)
- Exclusion of technical storage details unless they affect business meaning
- Minimal template
- Explicit prohibition of function names and Spark operations

---

#### 11. Job Inventory Specification (`docs/standards/job_inventory_spec.md`)

**Objective:** Define normative structure and derivation rules for `docs/job_inventory.md`.

**Role:** Normative specification for the job catalog structure and automation rules.

**Scope:**
- Purpose (fast orientation, safe AI planning, incremental extension, automation-friendly)
- Source-of-truth rules (job discovery, row sourcing, manifest field mapping, artifact linking)
- File structure (5 required headings)
- Jobs table schema (16 columns with detailed derivation rules)
- Dependency links section
- Open verification items section
- Incremental update rules
- Compliance checklist
- Deterministic derivation from manifests

---

#### 12. Artifacts Catalog Specification (`docs/standards/artifacts_catalog_spec.md`)

**Objective:** Define normative structure and rules for cross-job artifacts documentation.

**Role:** Normative specification for the artifact catalog (`docs/artifacts_catalog.md`).

**Scope:**
- Catalog entry grammar (heading + bullet list with 11 required keys)
- Placeholder normalization for deterministic matching
- Deterministic entry matching algorithm (S3 pattern match, filename match)
- Field definitions and sourcing rules (artifact_id, file_name_pattern, s3_location_pattern, format, producer_job_id, producers, consumers, presence_on_success, purpose, content_contract, evidence_sources)
- Shared artifact exception rules (allowlist mechanism)
- Compliance checklist
- Example entry skeleton
- Optional governance fields (producer_glue_job_name, stability, breaking_change_rules)

---

#### 13. Naming Standard (`docs/standards/naming-standard.md`)

**Objective:** Define naming conventions for repository elements.

**Role:** Normative specification for naming consistency across jobs, artifacts, and documentation.

**Scope:**
- Naming conventions for jobs, manifests, and related elements
- Pattern requirements and restrictions
- Consistency rules

**Note:** This file appears to be sparse or placeholder content and may need further development.

---

#### 14. Validation Standard (`docs/standards/validation_standard.md`)

**Objective:** Define validation requirements, tools, and processes for repository documentation and code.

**Role:** Normative specification for validation tooling, CI/CD integration, and compliance verification.

**Scope:**
- Validation tool location and usage (`tools/validate_repo_docs.py`)
- CI/CD integration (`.github/workflows/validate_standards.yml`)
- Validation scope (manifest, business descriptions, script cards, artifacts catalog, job inventory compliance)
- Pass criteria and requirements for PRs
- Common validation workflows (adding jobs, updating documentation, updating manifests)
- Troubleshooting guidance for validation failures
- References to related standards

**Note:** Created as part of conceptual-layer purity implementation to centralize validation rules that were previously duplicated in `system_context.md`.

---

### Planning & Implementation Layer (Guides)

#### 14. Roadmaps Guide (`docs/roadmaps/README.md`)

**Objective:** Guide for creating objective definitions (Step 1) and pipeline plans (Step 2a).

**Role:** How-to guide for the planning phase documentation in the 5-step workflow.

**Scope:**
- Purpose (define business objectives and pipeline-level architecture)
- Document types: Objective Definitions and Pipeline Plans
- Creating planning documents via CLI or GitHub Actions
- Workflow integration with 5-step process
- Key principles (manual discussion required, no assumptions, evidence-based, sequential execution)
- Listing and validation commands
- Related documentation links
- Best practices (stakeholder approval before implementation)

---

#### 15. Specifications Guide (`docs/specifications/README.md`)

**Objective:** Guide for creating capability specifications (Step 2b).

**Role:** How-to guide for detailed capability specification in the 5-step workflow.

**Scope:**
- Purpose (specify ONE capability/step in detail)
- When to create specifications
- Specification structure (YAML format with objective, constraints, inputs, outputs, processing logic, coding tasks, testing requirements, documentation requirements)
- Creating specifications via CLI or GitHub Actions
- Workflow integration
- Key principles (one capability per specification, define by meaning, explicit boundaries, testable criteria, evidence-based)
- Status values (draft, approved, implemented, deprecated)
- Best practices (specification over implementation)

---

### Artifact Layer (Job Documentation & Catalogs)

#### 16. Business Job Description: Matching Proposals (`docs/business_job_descriptions/matching_proposals.md`)

**Objective:** Document the business purpose and logic of the "matching_proposals" job.

**Role:** Business-facing documentation for category mapping proposal generation; exemplifies business job description standard.

**Scope:**
- Business purpose (aggregates vendor products into category-centric mapping proposals)
- Inputs and runtime parameters
- Output file structure and content
- 9-step business processing logic
- "Full proposals" output structure with vendor metadata, PIM matches, and product evidence
- "oneVendor_to_onePim" subset selection logic
- Key business rule: exclusion of "ambiguous vendor categories"
- Boundary definition (what job does NOT do)
- Observations (factual + explicitly marked assumptions)

---

#### 17. Business Job Description: Category Mapping to Canonical (`docs/business_job_descriptions/category_mapping_to_canonical.md`)

**Objective:** Document business purpose of category mapping to canonical assignments.

**Role:** Business-facing documentation for enrichment with canonical vendor→PIM mappings.

**Scope:**
- Business purpose (enriches products with vendor category context + preliminary PIM assignment via existing mappings + rule-based matching)
- Input parameters and required vendor files
- Optional canonical mapping reference
- Output: "forMapping_products" NDJSON product feed with vendor_mappings and PIM assignment fields
- PART 1-3 processing logic (build vendor mappings, enrich with canonical mappings, rule-based matching)
- Rule evaluation mechanics (intersection logic, assignment source/confidence)
- Output behavior (overwrites same final key)
- Key business rules (hard fail conditions, German-aware normalization, class code normalization)
- Boundary definition (what job does NOT do)

---

#### 18. Business Job Description: Mapping Method Training (`docs/business_job_descriptions/mapping_method_training.md`)

**Objective:** Document business purpose of self-learning mapping method training.

**Role:** Business-facing documentation for rule-based mapping rule creation and maintenance.

**Scope:**
- Business purpose (self-learning pipeline that derives + validates rule-based signals for vendor→PIM mapping)
- Key inputs (Step2 artifacts, canonical mapping reference, denylist config)
- Outputs (training delta, stable training set, rule validation, mapping status, updated reference)
- 6-step business logic (build training delta, persist learning, build evidence, generate rules, validate rules, update reference)
- Truth protection safeguard (won't silently alter vendor mappings)
- Rule quality controls (denylist removal, threshold gating)
- Interpretation (explicitly marked)

---

#### 19. Business Job Description: Preprocess Incoming BMECAT (`docs/business_job_descriptions/preprocess_incoming_bmecat.md`)

**Objective:** Document business purpose of BMECAT XML preprocessing.

**Role:** Business-facing documentation for vendor data standardization.

**Scope:**
- Business purpose (preprocessing step that converts vendor BMECAT XML into normalized NDJSON datasets)
- Inputs (runtime parameters, vendor-specific extraction config)
- Extracted datasets (vendor_products, product_features, product_category_links, optional: mimes/relations/prices/categories)
- Output behavior (NDJSON format, single S3 objects)
- Key business rules (fail-fast on no products, skip products without usable key, config-path mismatch visibility, supports multiple BMECAT shapes)
- Boundary definition (what job does NOT do—no matching performed)
- Interpretation (explicitly marked)

---

#### 20. Script Card: Matching Proposals (`docs/script_cards/matching_proposals.md`)

**Objective:** Provide operational reference for matching_proposals job.

**Role:** Operator-facing documentation of interface and observable behavior.

**Scope:**
- Identity (job_id, glue_job_name, runtime, paths)
- Purpose (generates JSON outputs for matching proposals)
- Trigger and parameters
- Input/output interface blocks
- Side effects
- High-level processing (factual steps)
- Invariants
- Failure modes and observability
- Related artifacts and references

**Note:** This file contains many TBD fields indicating incomplete adoption of the script card standard.

---

#### 21. Codex Task: Generate Missing Job Manifest Files (`docs/codex-tasks/generate_missing_job_manifest_files.md`)

**Objective:** Codex task specification for generating missing job manifests.

**Role:** Template for Codex-assisted development of manifest synchronization; exemplifies Codex task structure.

**Scope:**
- Goal (ensure all jobs with glue_script.py have compliant job_manifest.yaml)
- Scope statement (only job manifests, no script/tool edits)
- Allowed changes (only `jobs/*/*/job_manifest.yaml`)
- Reference docs and non-negotiable rules
- Deterministic derivation rules (A-I for each manifest field)
- Work plan (3 steps: discover, create/update, validate)
- Acceptance criteria (all required keys, proper placeholders, TBD explanations)

---

#### 22. Job Inventory (`docs/job_inventory.md`)

**Objective:** Provide authoritative index of executable jobs and their system-level interfaces.

**Role:** Compiled view of all jobs; automation-friendly for Codex tasks and planning; derived from job manifests per `job_inventory_spec.md`.

**Scope:**
- Scope and evidence section
- Jobs table (16 columns): job_id, job_dir, executor, deployment_name, runtime, owner, business_purpose, parameters, inputs, outputs, side_effects, evidence_artifacts, upstream_job_ids, downstream_job_ids, status, last_reviewed
- Dependency links section
- Open verification items section

**Note:** Currently in skeleton/stub state; framework follows spec but content needs population.

---

#### 23. Artifacts Catalog (`docs/artifacts_catalog.md`)

**Objective:** Catalog persistent artifacts exchanged between jobs.

**Role:** Cross-job artifacts documentation; derived per `artifacts_catalog_spec.md`.

**Scope:**
- Artifact entries with 11 required keys (artifact_id, file_name_pattern, s3_location_pattern, format, producer_job_id, producers, consumers, presence_on_success, purpose, content_contract, evidence_sources)
- Optional governance fields (producer_glue_job_name, stability, breaking_change_rules)

**Note:** Currently in skeleton/stub state; framework defined by spec but content needs population.

---

#### 24. Glossary (`docs/glossary.md`)

**Objective:** Provide canonical definitions for shared terminology.

**Role:** Single source of truth for cross-job term definitions; prevents duplication across job documentation.

**Scope:**
- Shared terms used across multiple jobs
- Canonical definitions to avoid duplication in business descriptions and script cards

**Note:** Currently appears empty/minimal; framework in place for future population.

---

#### 25. Documentation Index (`docs/README.md`)

**Objective:** Provide documentation index and navigation guide.

**Role:** Entry point and reference guide for all documentation; helps users find what they need.

**Scope:**
- Quick links (5-step workflow, agent setup, workflow diagram, core context)
- Documentation structure overview
- Documentation by purpose (Planning, Implementation, Documentation, Understanding)
- Standards summary
- Validation instructions (`python tools/validate_repo_docs.py --all`)
- Key principles (truth hierarchy, documentation guidelines)
- Workflow overview
- Contributing guidelines
- Support resources
- Recent changes (reflects 2026-01-27 documentation reorganization)

---

### GitHub Integration & CI/CD

#### 26. Copilot Instructions (`.github/copilot-instructions.md`)

**Objective:** Provide instructions for GitHub Copilot on repository conventions and standards.

**Role:** Guide to help AI assistants (Copilot) understand repository-specific patterns, authority hierarchy, and non-negotiable rules.

**Scope:**
- Repository overview
- Key documentation files
- Repository structure
- Truth sources (authority hierarchy)
- Standardized artifacts (business descriptions vs script cards)
- Critical rules (manifests, code, documentation, validation)
- Development workflow
- Non-negotiable quality rules
- Technology stack
- Common tasks
- Best practices
- When in doubt references

**Note:** Human-friendly guide for AI assistants; intentionally duplicates some `system_context.md` content for accessibility.

---

#### 27. Workflows Implementation Summary (`.github/workflows/IMPLEMENTATION_SUMMARY.md`)

**Objective:** Provide summary of GitHub Actions workflow enhancements for agent-assisted development with human oversight.

**Role:** Technical summary of workflow implementation decisions and architecture.

**Scope:**
- Problem statement requirements (agent integration, manual steps preservation, PR pipeline updates, automation scope, full repository validation)
- New workflows created (pr_validation, pipeline_planner, capability_planner, WORKFLOWS_README)
- Enhanced existing workflows (planner, coding, testing, documentation)
- Workflow integration with 5-step process
- Quality gates summary
- Manual approval checkpoints
- Automation boundaries
- Benefits and testing approach
- Troubleshooting
- Future enhancements

---

#### 28. GitHub Workflows Diagram (`.github/workflows/WORKFLOW_DIAGRAM.md`)

**Objective:** Provide visual diagrams of GitHub Actions workflow architecture.

**Role:** Visual reference for workflow integration and automation levels; complements `.github/workflows/WORKFLOWS_README.md`.

**Scope:**
- High-level workflow architecture (ASCII diagrams)
- Planning phase diagram (Steps 1-2b)
- Implementation phase diagram (Steps 3-4)
- Validation phase diagram (Step 5)
- Workflow trigger summary
- Quality gate enforcement matrix
- Manual approval checkpoints
- Automation boundaries
- Success criteria

**Note:** Appears to duplicate/mirror content from `docs/workflows/WORKFLOW_DIAGRAM.md`.

---

#### 29. GitHub Workflows Guide (`.github/workflows/WORKFLOWS_README.md`)

**Objective:** Provide comprehensive documentation of all GitHub Actions workflows.

**Role:** Operator guide for using and understanding GitHub Actions workflows in the repository.

**Scope:**
- Overview (automation goals)
- Workflow categories (Planning, Implementation, Validation, Legacy)
- Detailed descriptions of 9 workflows:
  - Planner (Step 1)
  - Pipeline Planner (Step 2a)
  - Capability Planner (Step 2b)
  - Coding (Steps 3 & 4)
  - PR Validation
  - Testing
  - Documentation
  - Standards Validation
  - Designer (legacy)
- Workflow integration with 5-step process
- Manual vs automated steps comparison
- Usage examples
- Quality gates summary
- Workflow maintenance
- Troubleshooting
- Related documentation

---

### Operational & Logging

#### 30. Test Logs Guide (`logs/tests_logs/README.md`)

**Objective:** Guide for understanding and using test logs.

**Role:** Reference for test artifact management and log interpretation.

**Scope:**
- Log format (naming convention: YYYYMMDD_HHMMSS)
- Log contents (metadata, test results, summary)
- Viewing logs (CLI and GitHub Actions methods)
- Retention policies
- Automated testing triggers
- Log cleanup instructions (`find logs/tests_logs -type f -name '*.log' -mtime +30 -delete`)
- Best practices
- Troubleshooting

---

### Repository Root

#### 31. Repository README (`README.md`)

**Objective:** Provide repository overview and quick start guide.

**Role:** Entry point for new users; high-level introduction to repository structure and essential documentation.

**Scope:**
- Repository description (AI-supported data automation monorepo for AWS Glue jobs)
- Quick start guide
- Essential documentation links (5-step workflow, agent setup, system context)
- Repository structure overview (visual tree)
- Technology stack
- Development workflow summary

---

## Documentation Analysis

### Strengths

1. **Clear Separation of Concerns**
   - Business documentation (business job descriptions) vs operational documentation (script cards)
   - Planning documentation vs implementation documentation
   - Normative specifications vs implementation artifacts

2. **Well-Defined Authority Hierarchy**
   - Code > Manifests > Standards > Business Descriptions > Script Cards
   - Standards win in all conflicts
   - Evidence-based approach (derive from code, not assumptions)

3. **Comprehensive Workflow Documentation**
   - 5-step process thoroughly documented
   - Multiple reference documents (process guide, visual diagrams, setup instructions)
   - Agent integration clearly explained

4. **Normative Specifications**
   - Detailed versioned specifications (v1.0-v1.4)
   - Automated validation enforcement via CI
   - Compliance checklists for each standard

5. **Agent-Assisted Development Support**
   - Extensive agent documentation with human oversight emphasis (system context, setup guide, workflow integration)
   - Agent roles and responsibilities clearly defined as assistants, not autonomous actors
   - Mandatory human approval gates documented
   - GitHub Actions workflow integration with human review checkpoints

### Observations & Opportunities

1. **Content Population Needed**
   - `docs/job_inventory.md` — Framework in place but needs population from manifests
   - `docs/artifacts_catalog.md` — Framework in place but needs population from job analysis
   - `docs/glossary.md` — Empty/minimal; should be populated with shared terms
   - These are compilation artifacts that support planning and validation workflows

2. **Incomplete Adoption**
   - `docs/script_cards/matching_proposals.md` — Many TBD fields indicate incomplete adoption of script card standard
   - Should complete population to demonstrate full compliance with spec

3. **Sparse Content**
   - `docs/standards/naming-standard.md` — Appears to be placeholder/sparse; may need development or removal

4. **Documentation Consistency**
   - Most documentation follows specifications well
   - Validation is enforced via `tools/validate_repo_docs.py --all` in CI

---

## Proposed for Removal

After comprehensive analysis, the following observations are noted:

### Potential Redundancy

**`.github/workflows/WORKFLOW_DIAGRAM.md` vs `docs/workflows/WORKFLOW_DIAGRAM.md`**

**Analysis:** Both files appear to contain similar content (visual workflow diagrams, trigger matrices, quality gates). However:
- `.github/workflows/WORKFLOW_DIAGRAM.md` focuses on GitHub Actions workflow architecture and integration
- `docs/workflows/WORKFLOW_DIAGRAM.md` focuses on the broader development workflow and agent flow

**Recommendation:** **Do NOT remove**. While there is overlap, these documents serve different audiences:
- `.github/workflows/WORKFLOW_DIAGRAM.md` is for GitHub Actions operators and CI/CD maintenance
- `docs/workflows/WORKFLOW_DIAGRAM.md` is for developers following the 5-step workflow

The duplication appears intentional to provide context-appropriate documentation in each location.

---

### No Documents Proposed for Removal

After thorough analysis of all 31 markdown files, **no documents are proposed for removal** at this time. Each document serves a clear purpose within the documentation system:

1. **Context documents** provide essential foundation and principles
2. **Workflow documents** guide the development process
3. **Specification documents** define normative requirements
4. **Planning guides** support Steps 1, 2a, and 2b
5. **Job documentation** provides business and operational context
6. **Catalog documents** (even if sparse) provide necessary frameworks
7. **GitHub integration documents** support CI/CD and AI assistance
8. **Operational documents** support testing and logging

While some documents are sparse or incomplete (job_inventory.md, artifacts_catalog.md, glossary.md, naming-standard.md), they represent **necessary frameworks** that should be populated rather than removed.

The documentation system is comprehensive, well-organized, and follows a coherent architecture. The primary opportunities are:
- **Population** of catalog/inventory documents
- **Completion** of TBD fields in script cards
- **Development** of sparse standards (naming-standard.md)

---

## Recommendations

1. **Prioritize Population**
   - `docs/job_inventory.md` — Populate from existing job manifests
   - `docs/artifacts_catalog.md` — Populate from job analysis
   - `docs/glossary.md` — Add shared terms to prevent duplication

2. **Complete Script Cards**
   - `docs/script_cards/matching_proposals.md` — Fill TBD fields to demonstrate full compliance

3. **Develop Sparse Standards**
   - `docs/standards/naming-standard.md` — Either develop content or consolidate into another standard

4. **Maintain Documentation System**
   - Run `python tools/validate_repo_docs.py --all` regularly
   - Update this metadata file when documentation structure changes
   - Ensure new documents are added to this inventory

5. **Continue Standards Enforcement**
   - Maintain CI validation via `.github/workflows/validate_standards.yml`
   - Ensure all new documentation follows appropriate specifications
   - Keep authority hierarchy clear and enforced

---

## Version History

- **v1.1 (2026-01-27):** Aligned with `development_approach.md` locked truth principles; emphasized human oversight, agent assistance role, and governance hierarchy throughout document descriptions.
- **v1.0 (2026-01-27):** Initial metadata consolidation; comprehensive inventory of all 31 markdown files; no documents proposed for removal.

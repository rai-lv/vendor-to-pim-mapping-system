# System Context — AI-Supported Data Automation Monorepo

**Version:** 1.3 (Integrated — Manual, Codex, and Agent-Assisted Workflows)

---

## Purpose

This document is the **single source of truth for repository operational setup** within the governance framework established by [`development_approach.md`](development_approach.md). It defines:
- Repository structure and organization
- Authoritative sources (truth hierarchy for resolving conflicts between artifacts)
- Operational implementation of development workflows (manual, Codex-assisted, and agent-assisted)
- Non-negotiable rules and quality standards
- Technology stack and capabilities
- Common tasks and best practices

**Note**: For overarching workflow philosophy and governance principles, see [`development_approach.md`](development_approach.md). This document operationalizes those principles.

This document supports **three complementary development approaches**:
1. **Manual development** with ChatGPT planning
2. **Codex-assisted development** with structured task definitions
3. **Agent-assisted development** with human oversight and approval gates (v1.3)

For detailed agent roles and workflows, see: [`agent_system_context.md`](agent_system_context.md)

---

## Repository Objective

This is an **AI-supported data automation monorepo** for AWS Glue jobs (and optional Lambda helpers, Make.com orchestration) focused on **vendor→PIM assortment mapping**.

### Primary Goals

Enable efficient, scalable, and high-quality development through:
- **Structured planning** with explicit boundaries and testable criteria
- **Multiple workflow options**: manual, Codex-assisted, or agent-assisted
- **Enforcement of standards** via automated validation
- **Evidence-based documentation** derived from actual code
- **Clear authority hierarchy** preventing conflicting truths

---

## Repository Structure

### Job Structure

```
jobs/<job_group>/<job_id>/
  ├── glue_script.py          # Source of truth for runtime behavior
  ├── job_manifest.yaml       # Source of truth for interface (params, I/O, side effects)
  ├── configs/                # Optional: S3 config mirrors
  └── samples/                # Optional: redacted examples
```

### Documentation Structure

```
docs/
  ├── context_packs/
  │   ├── system_context.md           # THIS FILE — Repository operational setup guide
  │   ├── development_approach.md     # 🔒 LOCKED TRUTH — Foundational governance principles
  │   ├── agent_system_context.md     # Agent-specific workflows and roles (v1.3)
  │   ├── github_element_map.md       # GitHub integration and governance hierarchy mapping
  │   └── documentation_system.md     # Documentation inventory and metadata catalog
  ├── workflows/
  │   ├── WORKFLOW_5_STEPS.md         # Complete 5-step development process
  │   ├── WORKFLOW_DIAGRAM.md         # Visual workflow overview
  │   └── AGENTS_SETUP.md             # Agent installation and usage
  ├── roadmaps/                       # Objectives and pipeline plans (Steps 1 & 2a)
  ├── specifications/                 # Capability-level definitions (Step 2b)
  ├── standards/                      # Specifications (naming, manifests, docs)
  ├── business_job_descriptions/      # Business intent documentation
  ├── script_cards/                   # Operational reference documentation
  ├── codex-tasks/                    # Codex task templates and examples
  ├── job_inventory.md                # Job index
  ├── artifacts_catalog.md            # Cross-job artifacts
  └── glossary.md                     # Shared definitions
```

### Tools Structure

```
tools/
  ├── planner_agent.py                # Step 1: Define objectives (agent workflow)
  ├── pipeline_planner_agent.py       # Step 2a: Pipeline plans (agent workflow)
  ├── capability_planner_agent.py     # Step 2b: Capability specs (agent workflow)
  ├── coding_agent.py                 # Steps 3 & 4: Decompose and Codex tasks
  ├── testing_agent.py                # Testing automation
  ├── documentation_agent.py          # Documentation automation
  └── validate_repo_docs.py           # Standards validation (CI gate)
```

---

## Truth Sources (Authority Hierarchy)

When conflicts arise, this hierarchy determines which source is authoritative:

1. **Code Truth**: `jobs/<job_group>/<job_id>/glue_script.py` is authoritative for **runtime behavior**
2. **Interface Truth**: `jobs/<job_group>/<job_id>/job_manifest.yaml` is authoritative for **parameters, S3 inputs/outputs, side effects, and run receipts**
3. **Standards Truth**: Files under `docs/standards/` **override everything else for documentation formats, naming conventions, and validation rules**; runtime truth remains with code
4. **Business Description Truth**: `docs/business_job_descriptions/<job_id>.md` is authoritative for **business intent** (why), business logic, and boundaries
5. **Script Card Truth**: `docs/script_cards/<job_id>.md` is authoritative for **operational interface** and observable behavior

**Rule**: If a Codex task, manifest, script card, or any other document conflicts with a standard **regarding documentation structure or format**, **the standard wins**. For runtime behavior, code always takes precedence.

---

## Development Workflows

This repository supports **three complementary workflow approaches**. Teams can choose the approach that best fits their needs, or combine them as appropriate.

### Workflow Comparison

| Approach | Planning | Execution | Best For |
|----------|----------|-----------|----------|
| **Manual** | ChatGPT discussions | Manual coding | Small changes, prototypes, exploratory work |
| **Codex-Assisted** | Manual planning + structured Codex tasks | Codex generates code from tasks | Standard features, well-defined changes |
| **Agent-Assisted** | Agent-assisted planning with manual approval | Human-driven execution with agent support | Large pipelines, systematic development |

### 1. Manual Development Workflow (ChatGPT-Assisted)

**Traditional approach with AI planning support:**

1. **Define Objective** — Discuss with ChatGPT: what must be achieved, out-of-scope, success criteria
2. **Plan Approach** — Break down into capabilities/steps
3. **Write Code** — Manual implementation
4. **Document** — Create/update manifests, script cards, business descriptions
5. **Validate** — Follow `docs/standards/validation_standard.md`

**When to use**: Small changes, quick iterations, exploratory development

---

### 2. Codex-Assisted Development Workflow

**Structured task-based development:**

1. **Define Objective** — What must be achieved, out-of-scope boundaries, success criteria
2. **Overarching Plan** — Pipeline-level capabilities, decision points, artifacts
3. **Capability Plan** — Step-level inputs/outputs, rules, acceptance criteria
4. **Decompose** — Break into small elements for individual PRs
5. **Codex Task** — Reference standards, restrict file changes, include quality gates
6. **Execute PR** — Codex creates PR from task definition
7. **PR Review** — Use `docs/codex-tasks/pr_review_checklist.md`
8. **Deploy** — Manual AWS Glue update
9. **Documentation Update** — Via Codex task or manual

**When to use**: Standard features, well-defined requirements, systematic development

**Key Principle**: Two planning layers (Overarching + Capability) before code changes

---

### 3. Agent-Assisted Development Workflow (v1.3)

**Agent-assisted planning and human-driven execution with approval gates:**

```
Step 1: Define Objective (Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2a: Overarching Plan / Pipeline-Level (Pipeline Planner Agent)
   ↓ [Manual discussion and approval required]
Step 2b: Capability Plan / Step-Level (Capability Planner Agent)
   ↓ [Manual discussion and approval required]
Step 3: Decompose into Development Elements (Coding Agent)
   ↓
Step 4: Create Codex Tasks (Coding Agent)
   ↓
Step 5: Code Creation (PR Process)
   ↓
Step 6: Validate → Document → Deploy (Testing/Documentation/Deployment Agents)
```

**Mapping to Development Approach 5-Step Process:**
- **Step 1** (above) = Development Approach **Step 1** (Define the Objective)
- **Steps 2a + 2b** (above) = Development Approach **Steps 2-3** (Plan the Pipeline + Break Down Into Capability Plans)
- **Steps 3-5** (above) = Development Approach **Step 4** (Execute Development Tasks) — operational decomposition
- **Step 6** (above) = Development Approach **Step 5** (Validate, Test, and Document)

**When to use**: Large pipelines, complex features, systematic development requiring consistency

**Agent Tools**:
- **Planner Agent** (`tools/planner_agent.py`) — Assists in creating `docs/roadmaps/<objective>.md` with human approval
- **Pipeline Planner Agent** (`tools/pipeline_planner_agent.py`) — Assists in creating `docs/roadmaps/<objective>_pipeline_plan.md` with human approval
- **Capability Planner Agent** (`tools/capability_planner_agent.py`) — Assists in creating `docs/specifications/<capability>.yaml` with human approval
- **Coding Agent** (`tools/coding_agent.py`) — Assists with decomposition and Codex task generation
- **Testing/Documentation/Deployment Agents** — Assist with quality gates and deployment processes, subject to human review

**Key Features**:
- Agent-assisted planning artifact generation with mandatory human approval
- Manual oversight and approval gates at each planning step
- Human validation checkpoints before progression to next phase
- Explicit unknowns and boundaries
- Evidence-based plans referencing existing code

**For complete agent workflow details, see**: [`docs/context_packs/agent_system_context.md`](agent_system_context.md) and [`docs/workflows/WORKFLOW_5_STEPS.md`](../workflows/WORKFLOW_5_STEPS.md)

---

## Standardized Artifacts (Do Not Confuse)

There are **two different** business-facing documentation types with **distinct purposes**:

### 1. Business Job Descriptions

**Location**: `docs/business_job_descriptions/<job_id>.md`  
**Spec**: `docs/standards/business_job_description_spec.md`

**Purpose**:
- Business intent — **why** the job exists
- Business rules and logic
- Boundaries (what's in/out of scope)

**Excludes**: Technical storage details unless they affect business meaning

### 2. Script Cards

**Location**: `docs/script_cards/<job_id>.md`  
**Spec**: `docs/standards/script_card_spec.md`

**Purpose**:
- Operational interface — how to run the job
- Parameters, inputs, outputs
- Side effects, failure modes

**Must NOT**: Define global terms, include full output schemas

**Important**: Definitions shared across jobs belong in `docs/glossary.md`, **NOT duplicated** per job doc.

---

## Critical Rules When Making Changes

### Job Manifest Rules

- Manifests **must** follow placeholder and format rules defined in `docs/standards/job_manifest_spec.md`
- Manifests **must** be evidence-based (derived from script + deployment config)
- **Never guess** at manifest content — verify from actual code

### Code Changes

- **Preserve existing functionality** unless explicitly authorized to change it
- **Do not assume capabilities** unless confirmed by documentation or observed behavior
- Python code for AWS Glue jobs uses **PySpark and boto3**

### Documentation Changes

- **Never duplicate definitions** — use `docs/glossary.md` for shared terms
- Business descriptions and script cards serve **different purposes** — keep them distinct
- Always comply with the **relevant spec** under `docs/standards/`

### Standards Validation (CI Gate)

Every PR **must pass** automated validation. See `docs/standards/validation_standard.md` for validation requirements, tools, and CI integration details.

---

## Non-Negotiable Quality Rules

These rules apply to **all workflows** (manual, Codex, agent):

1. **No claim of verification unless file content was actually checked**
2. **No "assumption presented as fact"** — label unknowns as TBD or explicit assumptions
3. **Use only confirmed capabilities** (Glue/Make/NocoDB/etc.)
4. **Preserve previously locked/confirmed structures** unless explicitly authorized
5. **When asked to "review documentation," process it section-by-section** (no selective scanning)

---

## Technology Stack

- **Runtime**: AWS Glue (PySpark)
- **Language**: Python 3.x
- **Infrastructure**: AWS S3, AWS Glue
- **Orchestration**: Make.com (optional)
- **Planning**: ChatGPT + Codex + Agent-Assisted System (v1.3)
- **Validation**: Standards validator (see `docs/standards/validation_standard.md`)

---

## Common Tasks

### Adding a New Job

1. Create `jobs/<job_group>/<job_id>/glue_script.py`
2. Create `jobs/<job_group>/<job_id>/job_manifest.yaml` (follow `docs/standards/job_manifest_spec.md`)
3. Optionally create business description: `docs/business_job_descriptions/<job_id>.md`
4. Optionally create script card: `docs/script_cards/<job_id>.md`
5. Run validation per `docs/standards/validation_standard.md`

### Updating Documentation

1. Check the relevant spec in `docs/standards/`
2. Update the document per spec requirements
3. Add shared terms to `docs/glossary.md` (never duplicate in individual docs)
4. Run validation per `docs/standards/validation_standard.md`

### Updating a Job Manifest

1. Review the script's actual parameters, inputs, outputs, and side effects
2. Update `job_manifest.yaml` with evidence-based content
3. Follow requirements in `docs/standards/job_manifest_spec.md`
4. Run validation per `docs/standards/validation_standard.md`

---

## Best Practices

1. **Read before writing**: Always read this document before making structural changes
2. **Follow the standards**: Check `docs/standards/` for the spec relevant to what you're creating/updating
3. **Validate early**: Follow validation requirements in `docs/standards/validation_standard.md` as soon as you make changes
4. **Don't duplicate**: Use `docs/glossary.md` for shared definitions
5. **Evidence-based**: Derive manifests and documentation from actual code, not assumptions
6. **Respect boundaries**: Business descriptions and script cards have different scopes — don't mix them
7. **Check truth hierarchy**: When conflicts arise about documentation format/structure, standards win; for runtime behavior, code wins; see Truth Sources section for complete hierarchy

---

## When in Doubt

If you're unsure about:
- **Repository structure**: Refer to this document
- **Agent workflows**: See `docs/context_packs/agent_system_context.md`
- **5-step workflow details**: See `docs/workflows/WORKFLOW_5_STEPS.md`
- **Documentation format**: Check the relevant spec in `docs/standards/`
- **Shared terminology**: Check `docs/glossary.md`
- **Validation**: See `docs/standards/validation_standard.md`

---

## Related Documentation

- **[Agent System Context](agent_system_context.md)** — Detailed agent roles, responsibilities, and workflows (v1.3)
- **[5-Step Workflow](../workflows/WORKFLOW_5_STEPS.md)** — Complete development process guide
- **[Agent Setup Guide](../workflows/AGENTS_SETUP.md)** — Agent installation and usage
- **[Standards Directory](../standards/)** — Specifications for all documentation types
- **[Glossary](../glossary.md)** — Shared terminology and definitions

---

**Last Updated**: 2026-01-27  
**Version**: 1.3 (Integrated — Manual, Codex, and Agent-Assisted Workflows)

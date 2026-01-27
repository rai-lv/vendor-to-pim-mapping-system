# vendor-to-pim-mapping-system

AI-supported data automation monorepo for AWS Glue jobs focused on vendor→PIM assortment mapping.

## Quick Start

This repository follows a **5-step development workflow** with agent-assisted automation. See the documentation below to get started.

### Essential Documentation

- **[5-Step Workflow](docs/workflows/WORKFLOW_5_STEPS.md)** - Complete development process guide
- **[Agent Setup Guide](docs/workflows/AGENTS_SETUP.md)** - Agent installation and usage
- **[Agent System Context](docs/context_packs/agent_system_context.md)** - Detailed agent roles and workflows
- **[System Context](docs/context_packs/system_context.md)** - Repository structure and standards

## Repository Structure

```
.
├── docs/
│   ├── workflows/                    # Workflow and agent documentation
│   │   ├── WORKFLOW_5_STEPS.md      # 5-step development process
│   │   ├── WORKFLOW_DIAGRAM.md      # Visual workflow overview
│   │   └── AGENTS_SETUP.md          # Agent setup and usage
│   ├── context_packs/               # System context documents
│   │   ├── agent_system_context.md  # Agent roles and workflows
│   │   ├── system_context.md        # Repository standards
│   │   └── github_element_map.md    # GitHub integration guide
│   ├── roadmaps/                    # Planning documents (Steps 1 & 2a)
│   ├── specifications/              # Capability specs (Step 2b)
│   ├── standards/                   # Documentation standards
│   ├── script_cards/               # Operational documentation
│   ├── business_job_descriptions/  # Business intent documentation
│   └── glossary.md                 # Shared terminology
├── jobs/                           # Glue job implementations
│   └── <job_group>/<job_id>/
│       ├── glue_script.py         # Source of truth for runtime behavior
│       └── job_manifest.yaml      # Source of truth for interface
├── tools/                          # Agent automation scripts
│   ├── planner_agent.py           # Step 1: Define objectives
│   ├── pipeline_planner_agent.py  # Step 2a: Pipeline plans
│   ├── capability_planner_agent.py # Step 2b: Capability specs
│   ├── coding_agent.py            # Steps 3 & 4: Decompose and Codex tasks
│   ├── testing_agent.py           # Testing automation
│   ├── documentation_agent.py     # Documentation automation
│   └── validate_repo_docs.py      # Standards validation
└── logs/
    └── tests_logs/                # Test execution logs
```

## Development Workflow

This repository uses a **5-step workflow** with two required planning layers:

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
```

**See:** [WORKFLOW_5_STEPS.md](docs/workflows/WORKFLOW_5_STEPS.md) for complete details.

## Key Principles

1. **Two Planning Layers Required** - Steps 2a and 2b must be completed before code changes
2. **No Assumptions** - Explicitly mark unknowns; do not proceed with assumptions
3. **Explicit Boundaries** - State what IS and is NOT included at every step
4. **Evidence-Based** - Reference existing jobs/capabilities; mark gaps explicitly
5. **Testable Criteria** - All success criteria must be objectively verifiable

## Getting Started

### 1. Create an Objective (Step 1)

```bash
python tools/planner_agent.py create "objective_name" \
  --description "Brief description"
```

### 2. Create Pipeline Plan (Step 2a)

```bash
python tools/pipeline_planner_agent.py create "objective_name" \
  --objective-ref "objective_name.md"
```

### 3. Create Capability Specification (Step 2b)

```bash
python tools/capability_planner_agent.py create "capability_name" \
  --pipeline-ref "objective_name_pipeline_plan.md"
```

### 4. Continue with Steps 3-5

See [WORKFLOW_5_STEPS.md](docs/workflows/WORKFLOW_5_STEPS.md) for complete workflow.

## Standards Validation

All changes must pass validation:

```bash
python tools/validate_repo_docs.py --all
```

This runs automatically in CI via `.github/workflows/validate_standards.yml`.

## Documentation

- **Workflow & Agents:** `docs/workflows/`
- **Context & Standards:** `docs/context_packs/`, `docs/standards/`
- **Planning & Specs:** `docs/roadmaps/`, `docs/specifications/`
- **Job Documentation:** `docs/script_cards/`, `docs/business_job_descriptions/`

## Technology Stack

- **Runtime:** AWS Glue (PySpark)
- **Language:** Python 3.x
- **Infrastructure:** AWS S3, AWS Glue
- **Orchestration:** Make.com (optional)
- **Planning:** ChatGPT + Agent System
- **Validation:** Python-based standards validator
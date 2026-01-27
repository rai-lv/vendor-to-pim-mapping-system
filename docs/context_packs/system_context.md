# System Context — AI-Supported Workflow with Agents — v1.3

## Purpose
This document defines the monorepo’s development workflow using specialized agents. It describes:
- Planning and execution phases with defined responsibilities.
- Repository structure and authoritative sources.
- Rules and standards governing tasks.

---

## Repository Objective
Enable efficient, scalable, and high-quality development via:
- Manual planning validated by **agents** and human discussions.
- Automated execution of well-defined tasks.
- Enforcement of standards and automated documentation.

---

### Agent-Driven Development Workflow

#### Step 1: Define Objective (Planner Agent)
- Collaboratively define objectives through discussions:
  - Success criteria, boundaries, risk assessment.
- Output: `docs/roadmaps/<objective>.md`.

#### Step 2a: Overarching Plan (Pipeline Planner Agent)
- Design pipeline plans:
  - Sequences, dependencies, fallback paths.
- Output: `docs/roadmaps/<objective>_pipeline_plan.md`.

#### Step 2b: Capability Plan (Capability Planner Agent)
- Refine capabilities:
  - Rules, constraints, dependencies, testable criteria.
- Output: `docs/specifications/<capability>.yaml`.

#### Step 3: Decompose Tasks (Coding Agent)
- Break down capabilities into small, actionable tasks:
  - Explicit files/criteria.
- Removes reliance on Codex.

#### Steps 4–6: Validate → Document → Deploy
- Testing/Documentation Agents ensure quality.
- Deployment/Monitoring Agents automate final phases.

---

## Repository Structure
- `docs/roadmaps/`: Objectives and pipeline plans.
- `docs/specifications/`: Capability-level definitions.
- `jobs/`: Code for individual tasks.
- `tools/`: Agent files for automation.

---

## Standards and Rules
- All tasks must pass testing/validation.
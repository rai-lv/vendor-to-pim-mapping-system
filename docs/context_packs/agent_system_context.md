# Agent System Context — AI-supported Development Workflow

## Overview
This document defines and describes the roles, responsibilities, workflows, and outputs of the agents embedded in the development workflow for the `vendor-to-pim-mapping-system` repository. It ensures alignment between the agent-based approach, the broader system context (defined in `system_context.md`), and repository-wide standards.

The agent workflows are structured to enable alignment with the 5-step development process outlined in `WORKFLOW_5_STEPS.md`.

---

## Objectives of the Agent System
The agent system is designed to:
- Streamline the development workflow through automation where feasible.
- Maintain manual oversight during critical planning phases (Steps 1–2b).
- Enforce repository standards via automated quality gates.
- Dynamically maintain documentation artifacts as tasks evolve.
- Provide modular, self-contained scripts for executing specific roles in the workflow.

---

## Agent Roles
### 1. Planner Agent
**Purpose:**
- Generates objective definitions with testable success criteria, boundaries, and discussions.

**Input:** Human-provided objectives. 
**Output:** `docs/roadmaps/<objective>.md`

### 2. Pipeline Planner Agent
**Purpose:**
- Develops overarching pipeline plans:
  - Sequences of tasks.
  - Decision points, dependencies.

**Input:** Objective document (`roadmap/md/<objective>.path`)
**Outputs:** Updated references pipelines.md
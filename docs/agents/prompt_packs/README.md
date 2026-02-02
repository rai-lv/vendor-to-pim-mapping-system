# Agent Prompt Packs

## Purpose
This directory contains **reusable prompt skeletons and task specifications** for invoking agents consistently across the repository.

## Scope
As defined in the Documentation System Catalog:
- **Non-authoritative**: These are examples and templates, not normative requirements
- **Purpose**: Reduce friction and variance in agent usage
- **Relationship to standards**: Prompts support but do not compete with standards

## How to Use Prompt Packs
1. Select the appropriate task specification for your work
2. Provide any additional context specific to your situation
3. Invoke the relevant agent (e.g., documentation-agent, combined-planning-agent)
4. The agent will use the task specification to guide its work

## Available Task Specifications

### `task_contribution_approval_guide.md`
**Purpose:** Instructions for the documentation-agent to draft/rework the Contribution Approval Guide

**When to use:** 
- When creating or substantially reworking the Contribution Approval Guide
- When the existing guide needs to be brought into alignment with current standards

**Target agent:** Documentation-agent or general-purpose documentation agent

**Output:** Complete draft of `docs/process/contribution_approval_guide.md`

## Adding New Prompt Packs
When creating new prompt packs:
1. Follow the pattern established in existing packs
2. Include clear success criteria and boundaries
3. Reference relevant context and standards documents
4. Label examples as non-normative
5. Include escalation rules for unclear situations
6. Avoid duplicating normative content from standards

## Relationship to Other Documentation
- **Agent Role Charter** (`docs/agents/agent_role_charter.md`): Defines canonical agent roles and responsibilities
- **Workflow Guide** (`docs/process/workflow_guide.md`): Defines the 5-step execution process
- **Standards** (`docs/standards/`): Define normative requirements that prompt packs support
- **Agent Definitions** (`.github/agents/`): Contains the actual agent implementations

Prompt packs are **supporting artifacts** that help invoke agents consistently but do not define agent behavior or normative requirements.

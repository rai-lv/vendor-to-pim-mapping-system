# Development Approach

## Purpose
This document defines the development approach for the `vendor-to-pim-mapping-system` repository. It provides a clear, step-by-step process for achieving development objectives, ensuring alignment between the user’s high-level goals and the detailed implementation of scripts, pipelines, and artifacts.

**Scope Note:** This document describes guiding principles and the intended workflow shape. Concrete templates, required fields, file locations, and enforcement mechanisms are defined in adjacent repository standards and governance documents.

This approach focuses on iterative planning, collaboration between users and agents, and a workflow that moves seamlessly from high-level objectives to working, validated deliverables.

---

## Core Principles

### 1. Human-Agent Collaboration
- Agents are collaborators, not autonomous actors. Their role is to:
  - Assist in refining outputs based on human feedback.
  - Automate repetitive or mechanical tasks to enhance human decision-making rather than replace it.
- Collaboration is a **feedback loop** where agents iteratively improve outputs with human guidance.

### 2. Iterative and Sequential Workflows
- The development process is iterative, meaning outputs evolve dynamically across multiple cycles:
  - Each step involves drafts from the agent.
  - Humans provide feedback, refine decisions, and validate results.
- The workflow is sequential in structure and iterative within each step.

### 3. Balance of Automation and Oversight
- Automation enforces standards, consistency, and efficiency for well-defined tasks.
- Human decision-making provides critical judgment for open-ended, high-stakes, or creative decisions.
- This balance ensures that automation complements human intelligence, rather than bypassing or replacing it.

### 4. Manual Oversight and Checkpoints
- Progression between stages is expected to include explicit human sign-off, captured in the repository’s governance artifacts.
- Manual checkpoints ensure key decisions are well documented, including objective refinement, scope changes, breaking changes, and acceptance of assumptions.

### 5. Governance and Truth Hierarchy
- All workflows, agents, and outputs must align with the repository’s documented principles.
- Decision-making is guided by a clear **truth hierarchy**:
  1. **Human-defined inputs** and validated objectives take precedence.
  2. **Standards and criteria** enforced across the repository.
  3. **Automated outputs**, which must remain subordinate to human-defined rules and validations.

### 6. Alignment with Success Criteria
- Every artifact (pipeline, capabilities, code) must comply with user-defined success criteria at each planning stage.
- Validation ensures that outputs meet these criteria before moving forward.

---

## Agent Context

The sequential development process described in this document is **agent-assisted** at each stage. Agents support specific functions within the workflow:

- **Planning Function**: Assists in refining objectives and producing pipeline plans.
- **Specification Function**: Helps break down capabilities into building plans and actionable steps.
- **Implementation Function**: Supports the execution of tasks aligned with building plans.
- **Validation Function**: Ensures outputs meet predefined success criteria and include appropriate validation artifacts.
- **Documentation Function**: Automates documentation tasks while addressing broader repository needs.

Agents operate under human oversight, iterating on drafts, automating well-defined tasks, and providing structured support across the workflow.

**Implementation Details**: Concrete agent tools, workflows, and collaboration models are documented in [`agent_system_context.md`](agent_system_context.md). Agent installation and usage instructions are in [`../workflows/AGENTS_SETUP.md`](../workflows/AGENTS_SETUP.md).

---

## Sequential Development Process

The development system follows a **structured, sequential workflow** divided into five steps. Each step builds on the previous one, ensuring gradual refinement from high-level objectives to implemented and validated solutions. Human efforts are **assisted by agents** at each stage.

---

### **Step 1: Define the Objective**
The **objective** describes what the system aims to achieve. This is a **high-level statement of intent** that provides the context and direction for all subsequent planning and development.

#### What Happens:
- The **user defines the objective**, describing what they want to accomplish. For example:
  > "I have incoming vendor XML documents containing assortment information and want a system that allows me to update the products into my PIM system automatically."
- The Planning function, **assisted by agents**, supports the user in refining this objective:
  - Ensuring it is actionable for the following steps.
  - Highlighting any known constraints, unknowns, or risks.

#### Output:
- A defined **objective document** (`docs/roadmaps/<objective>.md`).

---

### **Step 2: Plan the Pipeline**

The **pipeline plan** breaks the high-level objective into a series of **capabilities** necessary to achieve the goal. Agents assist by creating structured drafts for collaboration.

This step is divided into two sub-steps:
- **Step 2a: Overarching Plan** — High-level pipeline architecture and processing sequence
- **Step 2b: Capability Plans** — Detailed specifications for each capability

#### Step 2a: Overarching Plan (Pipeline-Level)

**What Happens:**
- The Planning function collaborates with the user and agents to create a high-level plan:
  - Identify **key capabilities** or components (e.g., "process incoming XML files", "map assortment data").
  - Define the **order of tasks** and dependencies for each capability.
  - Highlight risks or decision points.

**Output:**
- A pipeline plan (`docs/roadmaps/<objective>_pipeline_plan.md`).

**Approval Gate:** Manual approval required before proceeding to Step 2b.

#### Step 2b: Capability Plans (Step-Level)

**What Happens:**
- The Specification function, working with users and agent drafts, refines each pipeline step into:
  - What the capability does (purpose, scope).
  - Key inputs, outputs, and transformations.
  - Business rules and acceptance criteria.

**Output:**
- Capability specification documents (`docs/specifications/<capability>.yaml`).

**Approval Gate:** Manual approval required for each capability before proceeding to Step 3.

---

### **Step 3: Break Down Into Development Elements**

Agents assist in decomposing capability plans into small, PR-sized development elements.

#### What Happens:
- The Implementation function helps break down each approved capability into:
  - Small development elements (completable in one PR).
  - Explicit file restrictions and acceptance criteria.
  - Dependencies between elements.

#### Output:
- Development elements list (console output or document).

---

### **Step 4: Create Codex Tasks**

Agents generate detailed Codex task specifications with quality gates.

#### What Happens:
- The Implementation function creates task specifications for each development element:
  - Standards compliance requirements.
  - Explicit file restrictions.
  - Quality gates and testing strategy.

#### Output:
- Codex task specifications (`docs/codex-tasks/<task>.md`).

---

### **Step 5: Code Creation and Validation**

Tasks are implemented, reviewed, iterated on, and integrated collaboratively.

#### What Happens:
- Code is created (manually or via Codex) based on task specifications.
- Validation function ensures outputs meet success criteria:
  - Automated testing and syntax validation.
  - Standards compliance checks.
  - Specification-based testing.
- Documentation function updates necessary artifacts:
  - Business job descriptions.
  - Script cards.
  - Glossary terms.

#### Output:
- Completed changes merged into the repository with traceability to the initial capability plan.
- Validated deliverables aligned with success criteria.
- Updated documentation covering changes and outcomes.

---

## Where Specifics Live

This document defines guiding principles, while the following documents define specific requirements and implementation:

**Implementation Documents:**
- **[Agent System Context](agent_system_context.md)**: Detailed agent roles, responsibilities, workflows, and collaboration models
- **[System Context](system_context.md)**: Repository structure, workflow options, truth hierarchy, and common tasks
- **[GitHub Element Map](github_element_map.md)**: Physical structure mapping and governance enforcement mechanisms

**Standards and Specifications:**
- **Repository Standards** (`docs/standards/`): Templates, naming conventions, metadata formats
- **Validation Standard** (`tools/validate_repo_docs.py`): Validation rules and pass criteria
- **Governance Rules**: Change control policies, breaking-change requirements

**Workflow Guides:**
- **[5-Step Workflow](../workflows/WORKFLOW_5_STEPS.md)**: Complete step-by-step development process
- **[Agent Setup Guide](../workflows/AGENTS_SETUP.md)**: Agent installation and usage instructions
- **[Workflow Diagrams](../workflows/WORKFLOW_DIAGRAM.md)**: Visual workflow representations

---

## Related Documentation

- **[System Context](system_context.md)** — Repository structure and workflow implementation
- **[Agent System Context](agent_system_context.md)** — Agent roles and detailed workflows
- **[GitHub Element Map](github_element_map.md)** — Physical structure and governance mapping
- **[Documentation System](documentation_system.md)** — Documentation catalog and metadata

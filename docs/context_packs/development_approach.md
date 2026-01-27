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

Agents operate under human oversight, iterating on drafts, automating well-defined tasks, and providing structured support across the workflow. Role-specific responsibilities are documented in the Agent Role Charter (if present).

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

#### What Happens:
- The Planning function collaborates with the user and agents to create a high-level plan:
  - Identify **key capabilities** or components (e.g., "process incoming XML files", "map assortment data").
  - Define the **order of tasks** and dependencies for each capability.
  - Highlight risks or decision points.

#### Output:
- A pipeline plan (`docs/roadmaps/<objective>_pipeline_plan.md`).

---

### **Step 3: Break Down Into Capability Plans**
Agents assist in creating a **building plan**, which includes success criteria and structured steps.

#### What Happens:
- The Specification function, working with users and agent drafts, refines each pipeline step into:
  - What the capability does (purpose, scope).
  - Key inputs, outputs, and transformations.
  - Steps for implementation, included in a **Development Step Document**.

#### Output:
- A building plan (`docs/specifications/<capability>.yaml`) and structured Development Step Document.

---

### **Step 4: Execute Development Tasks**
#### What Happens:
- Tasks are implemented, reviewed, iterated on, and integrated collaboratively.
- Agents assist by automating repetitive tasks and enforcing consistency.

#### Output:
- Completed changes merged into the repository with traceability to the initial capability plan.

---

### **Step 5: Validate, Test, and Document**
#### What Happens:
- Validate outputs against success criteria.
- Capture validation artifacts.
- Update necessary documentation to ensure clarity and completeness.

#### Output:
- Validated deliverables aligned with success criteria.
- Updated documentation covering changes and outcomes.

---

## Where Specifics Live

This document defines guiding principles, while the following standards define specific requirements:
- **Repository Standards**: Templates, naming conventions, metadata formats.
- **Validation Standard**: Validation rules and pass criteria.
- **Governance Rules**: Change control policies, breaking-change requirements.
- **Agent Role Charter**: Definitions of agent responsibilities and functions.

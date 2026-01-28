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

## Agents and Tools

### Agents

Agents are **collaborative roles** that support humans during planning, implementation, validation, and documentation. Agents may:

* propose drafts and alternatives,
* surface unknowns, risks, and trade-offs,
* improve clarity and completeness,
* implement changes when asked.

Agents are **not autonomous owners** of decisions. Progress between stages requires **explicit human approval**.

### Tools

Tools are **deterministic instruments** used by humans and agents. Tools may:

* generate empty scaffolding/skeletons with required section headings when requested,
* validate structure and conformance to repository standards,
* check presence/consistency of required artifacts and links,
* produce deterministic evidence outputs (e.g., validation reports).

Tools must **not** invent requirements, change intent, or introduce new business logic. Tools provide structure; humans define content and meaning.

### Scope rule

This document defines **principles and workflow shape**. Concrete tool names, command syntax, templates, required fields, and enforcement mechanisms are defined in adjacent standards and workflow documents.

---

## Agent Context

The development system is **human-led** and **agent-assisted**.

* Agents support the workflow by drafting, reviewing, proposing improvements, and implementing changes when directed by humans.
* Tools support the workflow by providing empty scaffolding, enforcing standards, validating structure, and producing deterministic evidence outputs.
* Work is refined iteratively **within** each stage until success criteria are satisfied.
* Stage transitions occur only after explicit human approval, captured in an auditable form.
* Agent outputs (proposals, drafts, reviews) require human validation before becoming authoritative.

---

## Sequential Development Process

The development system follows a **structured, sequential workflow** divided into five steps. Each step builds on the previous one, ensuring gradual refinement from high-level objectives to implemented and validated solutions. Human efforts are **supported by scaffolding and validation tools** at each stage.

---

### **Step 1: Define the Objective**
The **objective** describes what the system aims to achieve. This is a **high-level statement of intent** that provides the context and direction for all subsequent planning and development.

#### What Happens:
- The **user defines the objective**, describing what they want to accomplish. For example:
  > "I have incoming vendor XML documents containing assortment information and want a system that allows me to update the products into my PIM system automatically."
- The Planning function, **supported by templates**, helps structure this objective:
  - Scaffolding tools generate document skeletons with required section headings (goals, boundaries, success criteria, constraints, risks).
  - Users manually fill in the content, performing the actual refinement work.
  - Users ensure objectives are actionable, identify constraints, unknowns, and risks through their own analysis and stakeholder discussions.

#### Output:
- A defined **objective document** (`docs/roadmaps/<objective>.md`).

#### Roles:
- Agents: propose refinements to intent, scope, and success criteria; surface unknowns for human consideration.
- Tools: validate artifact structure (if defined by standards).
---

### **Step 2: Plan the Pipeline**
The **pipeline plan** breaks the high-level objective into a series of **capabilities** necessary to achieve the goal. Scaffolding tools provide structure for collaboration.

#### What Happens:
- The Planning function, supported by scaffolding tools, helps users create a high-level plan:
  - Tools generate document skeletons for pipeline documentation (processing sequence, step descriptions, decision points).
  - Users manually identify **key capabilities** or components (e.g., "process incoming XML files", "map assortment data").
  - Users manually define the **order of tasks** and dependencies for each capability.
  - Users manually highlight risks or decision points through analysis and discussion.

#### Output:
- A pipeline plan (`docs/roadmaps/<objective>_pipeline_plan.md`).

#### Roles:
- Agents: propose decomposition into major parts and ordering; identify decision points for human review.
- Tools: validate structure and completeness checks.
 
---

### **Step 3: Break Down Into Capability Plans**
Scaffolding tools provide structured specification skeletons for capability documentation.

#### What Happens:
- The Specification function, supported by scaffolding tools, helps users refine each pipeline step:
  - Tools generate YAML specification skeletons with required sections.
  - Users manually define what the capability does (purpose, scope).
  - Users manually specify key inputs, outputs, and transformations.
  - Users manually document steps for implementation in a **Development Step Document**.

#### Output:
- A building plan (`docs/specifications/<capability>.yaml`) and structured Development Step Document.

#### Roles:
- Agents: draft implementable capability definitions and acceptance criteria for human approval.
- Tools: validate structure and required fields as defined by standards.
 
---

### **Step 4: Execute Development Tasks**
#### What Happens:
- Tasks are implemented, reviewed, iterated on, and integrated collaboratively.
- Scaffolding tools assist by generating task skeletons and enforcing repository standards through validation.

#### Output:
- Completed changes merged into the repository with traceability to the initial capability plan.

#### Roles:
- Agents: implement changes as directed by humans and/or propose task breakdown for human approval; flag conflicts with approved intent.
- Tools: run deterministic checks and validations; produce evidence.

---

### **Step 5: Validate, Test, and Document**
#### What Happens:
- Validate outputs against success criteria (manual validation by developers/testers).
- Capture validation artifacts.
- Update necessary documentation to ensure clarity and completeness.
- Automated tools validate documentation format and standards compliance.

#### Output:
- Validated deliverables aligned with success criteria.
- Updated documentation covering changes and outcomes.

#### Roles:
- Agents: review evidence against criteria and propose findings; ensure documentation matches reality for human verification.
- Tools: execute validation procedures and emit deterministic reports.

---

## Where Specifics Live

This document defines guiding principles, while the following standards define specific requirements:
- **Repository Standards**: Templates, naming conventions, metadata formats.
- **Validation Standard**: Validation rules and pass criteria.
- **Governance Rules**: Change control policies, breaking-change requirements.
- **Agent Role Charter**: Definitions of agent responsibilities and functions.

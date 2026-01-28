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
The sequential development process described in this document is **template-assisted** at each stage. Automated tools provide structured templates and validation to support human work:
- **Planning Function**: Provides structured templates for objectives and pipeline plans with validation checks.
- **Specification Function**: Generates templates for capability specifications with required sections.
- **Implementation Function**: Creates task templates and enforces repository standards.
- **Validation Function**: Automates standards compliance checking and format validation.
- **Documentation Function**: Generates documentation templates and validates completeness.

Tools operate under human oversight, generating structured templates for well-defined artifacts. Humans perform the actual thinking, refinement, discussion, and decision-making work. Role-specific responsibilities are documented in the Agent Role Charter (if present).

---

## Sequential Development Process

The development system follows a **structured, sequential workflow** divided into five steps. Each step builds on the previous one, ensuring gradual refinement from high-level objectives to implemented and validated solutions. Human efforts are **supported by templates** at each stage.

---

### **Step 1: Define the Objective**
The **objective** describes what the system aims to achieve. This is a **high-level statement of intent** that provides the context and direction for all subsequent planning and development.

#### What Happens:
- The **user defines the objective**, describing what they want to accomplish. For example:
  > "I have incoming vendor XML documents containing assortment information and want a system that allows me to update the products into my PIM system automatically."
- The Planning function, **supported by template tools**, helps structure this objective:
  - Template tools generate structured documents with required sections (goals, boundaries, success criteria, constraints, risks).
  - Users manually fill in the content, performing the actual refinement work.
  - Users ensure objectives are actionable, identify constraints, unknowns, and risks through their own analysis and stakeholder discussions.

#### Output:
- A defined **objective document** (`docs/roadmaps/<objective>.md`).

---

### **Step 2: Plan the Pipeline**
The **pipeline plan** breaks the high-level objective into a series of **capabilities** necessary to achieve the goal. Template tools provide structure for collaboration.

#### What Happens:
- The Planning function, supported by template tools, helps users create a high-level plan:
  - Tools generate structured templates for pipeline documentation (processing sequence, step descriptions, decision points).
  - Users manually identify **key capabilities** or components (e.g., "process incoming XML files", "map assortment data").
  - Users manually define the **order of tasks** and dependencies for each capability.
  - Users manually highlight risks or decision points through analysis and discussion.

#### Output:
- A pipeline plan (`docs/roadmaps/<objective>_pipeline_plan.md`).

---

### **Step 3: Break Down Into Capability Plans**
Template tools provide structured specifications for capability documentation.

#### What Happens:
- The Specification function, supported by template tools, helps users refine each pipeline step:
  - Tools generate YAML specification templates with required sections.
  - Users manually define what the capability does (purpose, scope).
  - Users manually specify key inputs, outputs, and transformations.
  - Users manually document steps for implementation in a **Development Step Document**.

#### Output:
- A building plan (`docs/specifications/<capability>.yaml`) and structured Development Step Document.

---

### **Step 4: Execute Development Tasks**
#### What Happens:
- Tasks are implemented, reviewed, iterated on, and integrated collaboratively.
- Template tools assist by generating task templates and enforcing repository standards through validation.

#### Output:
- Completed changes merged into the repository with traceability to the initial capability plan.

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

---

## Where Specifics Live

This document defines guiding principles, while the following standards define specific requirements:
- **Repository Standards**: Templates, naming conventions, metadata formats.
- **Validation Standard**: Validation rules and pass criteria.
- **Governance Rules**: Change control policies, breaking-change requirements.
- **Agent Role Charter**: Definitions of agent responsibilities and functions.

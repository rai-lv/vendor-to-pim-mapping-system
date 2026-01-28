# Template Tools System Context — Structured Development Workflow

## Overview

This document defines the roles, responsibilities, and governance principles for template tools that support the development workflow. It provides a high-level view of how template generation tools integrate with the 6-step operational model and provide structure for human work.

**Key Principle**: Tools are **template generators and validators, not interactive assistants**. Their role is to generate structured documents, validate completeness, and enforce standards—not to refine ideas, facilitate discussion, or iterate on content. Humans perform all thinking, refinement, and decision-making work.

The tool workflows are structured to support the 5-step development process outlined in `development_approach.md`, with mandatory human work at each stage (refinement, analysis, discussion, decision-making).

**For detailed technical specifications and usage instructions**, see:
- `docs/workflows/agent_tools_reference.md` - Tool CLI commands, parameters, and troubleshooting
- `docs/workflows/agent_workflow_templates.md` - Example templates and step-by-step workflow guides

---

## Objectives of the Tool System

The template tool system is designed to:
- **Provide structure** for development artifacts through standardized templates
- **Generate starting points** with required sections and validation checkpoints
- Maintain mandatory **manual work** during all planning phases (Steps 1–2b) where humans fill in content
- Enforce repository standards via automated format and completeness checking
- Validate documentation structure and required sections
- Provide modular, self-contained tools that **generate templates** for specific workflow steps

---

## Human Work and Governance Principles

This template tool system operates under strict governance principles aligned with `development_approach.md`:

### Core Governance Principles

1. **Human-Performed Work**
   - Tools are **template generators, not collaborators**
   - Tools **generate structure** but humans perform all content work
   - Tools **validate format** but humans make all decisions
   - No "feedback loop" or "iteration" —tools generate once, humans refine manually

2. **Mandatory Manual Work**
   - **Every planning step (Steps 1, 2a, 2b)** requires humans to manually fill in all template content
   - Humans perform refinement, analysis, discussion, and decision-making
   - No automated content generation—only structure provision
   - Manual sign-off captured in planning artifacts (objectives, pipeline plans, capability specs)

3. **Governance Hierarchy**
   - **Human-defined content** is the authoritative source
   - **Repository standards** guide template structure and validation rules
   - **Tool-generated templates** are empty starting points, not proposals
   - Templates provide structure; humans provide all substance

4. **Clear Tool Limitations**
   - Tools generate standardized templates with required sections
   - Tools validate completeness and format compliance
   - Tools do NOT: refine ideas, facilitate discussion, ask questions, iterate on content, or make suggestions
   - All thinking, refinement, and consensus-building performed by humans

### Approval Gates

| Stage | Tool Role | Human Work Required | Documentation |
|-------|-----------|---------------------|---------------|
| **Step 1** | Planner tool generates objective template | ✅ Human fills all content, refines, gets approval | Captured in `docs/roadmaps/<objective>.md` |
| **Step 2a** | Pipeline tool generates architecture template | ✅ Human designs architecture, fills content, gets approval | Captured in `docs/roadmaps/<objective>_pipeline_plan.md` |
| **Step 2b** | Capability tool generates spec template | ✅ Human writes specification, gets approval | Captured in `docs/specifications/<capability>.yaml` |
| **Step 3** | Coding tool generates decomposition template | ✅ Human performs decomposition, gets approval | Reviewed before task creation |
| **Step 4** | Coding tool generates task templates | ✅ Human writes task details, gets approval | Reviewed before PR creation |
| **Step 5** | Manual PR creation | ✅ Human review before merge | PR review process |
| **Step 6** | Validation tools check standards | ✅ Human review of results | PR review process |

---

## Workflow Context: Agent-Assisted Operational Model

The agent-assisted workflow follows a **6-step operational model** as defined in `system_context.md`, which maps to the 5-step Development Approach defined in `development_approach.md`:

### Agent-Assisted 6-Step Operational Flow

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
Step 6: Validate → Document (Testing/Documentation Agents)
```

### Mapping to Development Approach 5-Step Process

This operational 6-step model maps to `development_approach.md` as follows:

- **Step 1** (Define Objective) = **DA Step 1** (Define the Objective)
- **Steps 2a + 2b** (Overarching + Capability Plans) = **DA Steps 2-3** (Plan the Pipeline + Break Down Into Capability Plans)
- **Steps 3-5** (Decompose + Codex + PR) = **DA Step 4** (Execute Development Tasks) — operational decomposition of execution
- **Step 6** (Validate + Document) = **DA Step 5** (Validate, Test, and Document)

**Note**: Development Approach Step 2 is split into operational sub-steps 2a (pipeline-level) and 2b (capability-level) for agent-assisted workflows to enforce proper approval gates at each planning layer.

### Critical Rules

1. **Sequential Execution:** Each step must be completed and approved before proceeding to the next
2. **Manual Discussion Required:** Each planning step output requires human review, discussion, and explicit approval
3. **Explicit Unknowns and Assumptions:** All unknowns must be explicitly marked as TBD; assumptions must be explicitly labeled and require human approval before being used as planning inputs
4. **Evidence-Based:** Plans must reference existing code/jobs where applicable and mark unknowns explicitly

---

## Agent Roles and Responsibilities

### Planning Agents (Steps 1, 2a, 2b)

Planning agents assist in the strategic and architectural planning phases, where human oversight is most critical. All planning agent outputs require explicit human approval before progression.

#### 1. Planner Agent (Step 1: Define Objective)

**Role:** Assist humans in defining business objectives with explicit boundaries, testable success criteria, and risk assessment.

**Responsibilities:**
- **Proposes** structured objective definition templates
- Facilitates manual discussion between stakeholders
- Iterates on drafts based on human feedback
- Supports consensus-building on objectives before design work begins

**Inputs:** Human-provided objective name and description, stakeholder requirements

**Outputs:** Objective definition document at `docs/roadmaps/<objective>.md` containing:
- Objective statement and expected outcomes
- Out-of-scope boundaries
- Testable success criteria (functional and quality)
- Constraints (technical, business, process)
- Risk assessment and unknowns
- Dependencies

**Approval Gate:** Human stakeholders must explicitly approve the objective definition before proceeding to Step 2a.

**See also:** `docs/workflows/agent_tools_reference.md` for CLI usage and `docs/workflows/agent_workflow_templates.md` for example templates.

---

#### 2. Pipeline Planner Agent (Step 2a: Overarching Plan / Pipeline-Level)

**Role:** Assist humans in designing the end-to-end pipeline plan showing processing sequence, decision points, and conceptual artifacts.

**Responsibilities:**
- **Proposes** pipeline architecture aligned with approved objective
- Maps conceptual processing steps to potential AWS Glue jobs
- Identifies decision points and data transformations
- Flags unknowns requiring investigation
- Iterates based on human architectural decisions

**Inputs:** Approved objective definition from Step 1

**Outputs:** Pipeline plan document at `docs/roadmaps/<objective>_pipeline_plan.md` containing:
- Processing sequence (conceptual steps)
- Detailed step descriptions (inputs, processing, outputs)
- Conceptual artifacts produced at each step
- Decision points and branching logic
- Existing job mapping (where applicable)
- Unknowns and open decisions

**Approval Gate:** Technical lead and architect must approve the pipeline design before proceeding to Step 2b.

**See also:** `docs/workflows/agent_tools_reference.md` for CLI usage and `docs/workflows/agent_workflow_templates.md` for example templates.

---

#### 3. Capability Planner Agent (Step 2b: Capability Plan / Step-Level)

**Role:** Assist humans in breaking down pipeline steps into specific technical capability specifications ready for implementation.

**Responsibilities:**
- **Proposes** detailed capability specifications for each pipeline step
- Defines explicit inputs/outputs and processing logic
- Specifies job parameters and configuration needs
- References relevant repository standards
- Explicitly labels any assumptions for human approval
- Iterates based on human technical decisions

**Inputs:** Approved pipeline plan from Step 2a

**Outputs:** Capability specification at `docs/specifications/<capability>.yaml` containing:
- Capability name and objective
- Technical scope and boundaries
- Input/output specifications
- Processing requirements and business logic
- Job parameters and configuration
- Dependencies and prerequisites
- Success criteria and acceptance criteria
- Explicitly labeled assumptions requiring approval

**Approval Gate:** Technical lead must approve capability specification before proceeding to Step 3.

**See also:** `docs/workflows/agent_tools_reference.md` for CLI usage, `docs/workflows/agent_workflow_templates.md` for example templates, and `docs/standards/` for specification format requirements.

---

### Implementation Agents (Steps 3–6)

Implementation agents support the execution, testing, and documentation phases. While these agents have more automation, human review and approval remain mandatory before code changes are merged.

#### 4. Coding Agent (Steps 3–4: Decompose and Create Tasks)

**Role:** Assist humans in decomposing capability specifications into development elements and creating Codex tasks.

**Responsibilities:**
- **Proposes** decomposition of capability into discrete development elements
- Generates Codex task definitions per repository standards
- Ensures each element has clear boundaries and acceptance criteria
- Maps elements to target scripts/paths in the repository
- Flags quality gates that must pass

**Inputs:** Approved capability specification from Step 2b

**Outputs:**
- Development element decomposition (Step 3)
- Codex task definitions at `docs/codex-tasks/<task_id>.md` (Step 4)

**Approval Gate:** Human review required before tasks are assigned to agents for PR creation.

**See also:** `docs/workflows/agent_tools_reference.md` for CLI usage and Codex task format specifications.

---

#### 5. Testing Agent (Step 6: Validation)

**Role:** Assist in validating code changes meet acceptance criteria and quality standards.

**Responsibilities:**
- Proposes test execution plans
- Runs repository validation according to `docs/standards/validation_standard.md`
- Verifies code changes against acceptance criteria
- Reports validation results for human review

**Approval Gate:** Human review of test results required before PR merge.

**See also:** `docs/standards/validation_standard.md` for validation procedures.

---

#### 6. Documentation Agent (Step 6: Documentation)

**Role:** Assist in updating documentation to reflect code changes.

**Responsibilities:**
- **Proposes** documentation updates based on code changes
- Ensures documentation standards compliance
- Identifies documentation gaps
- Iterates based on human review feedback

**Approval Gate:** Human review of documentation changes required before PR merge.

**See also:** `docs/standards/` for documentation format standards.

---

## Integration with System Context

Agent-assisted workflows are **one of three supported approaches** in the repository, as defined in `system_context.md`:

1. **Manual Workflow** - Traditional approach for small changes
2. **Codex-Assisted Workflow** - Developer uses Codex tasks without agent automation
3. **Agent-Assisted Workflow** - Agents support planning and execution (this document)

All three approaches must:
- Map to the same Development Approach (5 steps) defined in `development_approach.md`
- Comply with repository standards defined in `docs/standards/`
- Use validation procedures in `docs/standards/validation_standard.md`
- Each approach may have its own operational step breakdown (e.g., agent-assisted uses 6 steps, manual uses 5 steps, Codex-assisted uses 9 steps as documented in `system_context.md`)

### Document Hierarchy and Conflict Resolution

When conflicts arise between documents, the following hierarchy applies:

1. **development_approach.md** - Foundational governance principles (locked truth, highest authority)
2. **system_context.md** - Repository operational setup (subordinate to development_approach.md)
3. **This document** - Agent-specific implementation details (subordinate to both above)
4. **docs/standards/** - Technical standards for documentation formats and validation
5. **Code and job manifests** - Runtime truth for actual implementation

**Conflict Resolution Rule**: In case of disagreement, defer to the document higher in this hierarchy. For runtime behavior, code always takes precedence over documentation.

### Relationship to Other Documentation

- **development_approach.md** - Foundational governance principles (locked truth)
- **system_context.md** - Repository operational setup and workflow models
- **This document** - Agent-specific roles and integration points
- **docs/workflows/agent_tools_reference.md** - Technical tool specifications
- **docs/workflows/agent_workflow_templates.md** - Example templates and guides
- **docs/standards/** - Authoritative standards for all workflows

---

## Key Principles Summary

### Agents as Collaborators

1. **Agents propose, humans decide** - All critical decisions require human approval
2. **Iterative refinement** - Agents iterate on drafts based on human feedback
3. **Evidence-based** - Agent proposals reference existing code and standards
4. **Explicit unknowns** - Agents flag assumptions and unknowns for human resolution
5. **Standards compliance** - Agents enforce repository standards, subject to human override

### Human Approval Gates

- **Planning phases (Steps 1, 2a, 2b)**: Mandatory explicit approval at each step
- **Implementation phases (Steps 3-5)**: Review and approval before task execution
- **Validation phase (Step 6)**: Review before PR merge

### Quality and Governance

- All agent outputs subject to repository validation per `docs/standards/validation_standard.md`
- Agents subordinate to human-defined objectives and standards
- No autonomous progression between workflow stages
- Full traceability from objective through implementation

---

## Getting Started

### For Planning Activities (Steps 1-2b)

1. **Start with human discussion** - Define what you're trying to achieve
2. **Use Planner Agent** to structure the objective definition
3. **Iterate with stakeholders** - Refine based on feedback
4. **Get explicit approval** before moving to next step
5. **Repeat for Steps 2a and 2b** with appropriate agents

**See:** `docs/workflows/agent_workflow_templates.md` for step-by-step guides and example templates.

### For Implementation Activities (Steps 3-6)

1. **Start with approved capability spec** from Step 2b
2. **Use Coding Agent** to decompose into tasks
3. **Review proposed decomposition** before task creation
4. **Create Codex tasks** and assign to implementation
5. **Review and validate** results before merge

**See:** `docs/workflows/agent_tools_reference.md` for tool usage and troubleshooting.

### For All Activities

- **Follow the 6-step operational model** - No skipping steps
- **Maintain human oversight** - Agents assist, humans decide
- **Document assumptions** - Label and get approval for unknowns
- **Run validation** - Per `docs/standards/validation_standard.md`
- **Respect approval gates** - Wait for explicit human sign-off

---

## See Also

**Context and Governance:**
- `development_approach.md` - Foundational governance principles (locked truth)
- `system_context.md` - Repository operational setup guide
- `docs/standards/` - Authoritative standards for all development work

**Agent Tools and Usage:**
- `docs/workflows/agent_tools_reference.md` - Detailed CLI specifications and troubleshooting
- `docs/workflows/agent_workflow_templates.md` - Example templates and step-by-step guides
- `docs/workflows/WORKFLOW_5_STEPS.md` - Complete workflow documentation

**Standards and Validation:**
- `docs/standards/validation_standard.md` - Validation tool and CI/CD procedures
- `docs/standards/script_card_spec.md` - Script card template standards
- `docs/standards/business_job_description_spec.md` - Business description template standards

---

**Version:** 2.0  
**Last Updated:** 2026-01-27  
**Changes:** Restructured to align with documentation_system.md description - extracted detailed technical content to separate operational documents, retained high-level governance and workflow integration


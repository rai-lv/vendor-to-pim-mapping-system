# Agent task: Draft `Codable Task Spec`

## Purpose
Create a standards-layer document that defines the **normative structure** for individuable codable tasks used to control implementation work during Step 3→4 execution. This standard ensures that tasks remain bounded, traceable, reviewable, and aligned with the repository's evidence and approval discipline.

## Where it lives
Target file: `docs/standards/codable_task_spec.md`

## Context you must consider
You must read and align to the existing documentation set, especially:
- **Context baselines:** 
  - `docs/context/development_approach.md` — 5-step workflow and approval discipline
  - `docs/context/target_agent_system.md` — agent responsibilities, evidence discipline, conflict handling
  - `docs/context/system_context.md` — repository purpose and truth framing
  - `docs/context/documentation_system_catalog.md` — document types, boundaries, canonical placement
  - `docs/context/glossary.md` — canonical term definitions (do not redefine terms)
- **Process guidance:**
  - `docs/process/workflow_guide.md` — Step 3 (capability planning and codable tasks) execution procedures, checkpoints, and escalation triggers
  - `docs/process/contribution_approval_guide.md` — approval evidence expectations and review procedures
- **Related standards:**
  - `docs/standards/documentation_spec.md` — documentation structure and formatting rules
  - `docs/standards/business_job_description_spec.md` — example of a well-structured per-job standard
  - `docs/standards/script_card_spec.md` — example of operational documentation structure
  - `docs/standards/artifacts_catalog_spec.md` — example of catalog entry specification
  - `docs/standards/naming_standard.md` — naming conventions and identifier rules
  - `docs/standards/validation_standard.md` — validation rules and evidence expectations

Do not modify context files.

## Following documents are not finalized and their current content MUST NOT be used as info source or format standard:
- `docs/process/contribution_approval_guide.md`
- `docs/standards/codable_task_spec.md` (the document you are creating)
- `docs/standards/decision_records_standard.md`
- `docs/standards/validation_standard.md`

## What this spec must achieve (success criteria)

The resulting spec must:

1. **Define what a codable task is** — provide a clear definition that distinguishes codable tasks from:
   - high-level capabilities (which may contain multiple tasks),
   - implementation details (actual code/scripts),
   - operational procedures (how-to guides),
   - business requirements (purpose/rationale).

2. **Define the normative structure** for a codable task specification, including:
   - Required sections/fields that every task must contain,
   - The level of detail expected (bounded but not over-specified),
   - How task boundaries are expressed,
   - How dependencies between tasks are declared.

3. **Define content expectations** that ensure tasks are:
   - **Individuable:** each task can be understood and implemented independently (given its stated dependencies),
   - **Bounded:** clear scope with explicit boundaries (what it does and does NOT do),
   - **Traceable:** outcomes can be verified against the task specification,
   - **Reviewable:** another developer can understand the intent and validate the implementation.

4. **Align with Step 3→4 transition** as defined in `workflow_guide.md`:
   - Tasks must support the approval gate between capability planning (Step 3) and implementation (Step 4),
   - Tasks must be decomposed from approved capabilities without introducing unapproved assumptions,
   - Task specifications must provide enough detail to implement without embedding full solutions.

5. **Support evidence and validation discipline:**
   - Define what "task completion" means,
   - Specify what evidence is expected for task acceptance,
   - Clarify how unknowns and assumptions are handled in task specifications.

6. **Prevent anti-patterns:**
   - Tasks that are too vague ("implement everything"),
   - Tasks that embed full code solutions,
   - Tasks that duplicate standards or schemas,
   - Tasks that introduce tool command syntax or operational procedures.

7. **Be clear about boundaries** (what belongs in this spec vs elsewhere):
   - What belongs in the codable task spec itself (task structure and content rules),
   - What belongs in capability plans (overall capability purpose and acceptance criteria),
   - What belongs in implementation artifacts (actual code, tests, documentation),
   - What belongs in operational documentation (how to run, troubleshoot, deploy).

## Boundaries (non-goals)

The spec must NOT:
- Include full task templates that would become a second source of truth (short examples are acceptable if clearly labeled NON-normative),
- Include capability planning procedures (those belong in `workflow_guide.md`),
- Embed tool/CLI instructions or troubleshooting guides (those belong in `docs/ops/`),
- Redefine glossary terms or workflow steps,
- Prescribe specific implementation approaches or technology choices,
- Include job-specific task examples (may reference real examples from the repo, but do not embed them in full).

## What to include (content expectations)

Your draft should include:

### 1. Purpose and scope statement
- What problem this standard solves (why codable tasks need a normative structure)
- What a codable task specification is and what it is NOT
- Relationship to capability plans, implementation artifacts, and operational documentation

### 2. Definition of "codable task"
- Clear definition that distinguishes tasks from capabilities and implementation details
- Key characteristics (individuable, bounded, traceable, reviewable)
- Position in the 5-step workflow (Step 3→4 transition)

### 3. Required structure for task specifications
Define the normative sections/fields that every codable task must contain:
- **Task identity** (how tasks are named/identified, if applicable)
- **Purpose/objective** (what the task aims to achieve — short and clear)
- **Boundaries** (what the task does and explicitly does NOT do)
- **Dependencies** (prerequisite tasks, required inputs, external dependencies)
- **Intended outputs** (what artifacts, changes, or states result from completing this task)
- **Acceptance criteria** (how to verify the task is complete — must be evaluable)
- **Unknowns/assumptions** (if any — must be explicit and bounded)

Specify the expected level of detail for each section and provide minimal guidance on what "good enough" looks like.

### 4. Task granularity and decomposition guidance
- How to determine appropriate task size (not too coarse, not too fine)
- When to split a task vs when to keep it unified
- How to maintain cohesion (tasks should be logically coherent units)
- Guidance on task dependencies and ordering

### 5. Evidence and validation expectations
- What constitutes completion evidence for a task
- How acceptance criteria should be structured to support verification
- Relationship to the validation standard (`validation_standard.md`)
- How to handle tasks where evidence is not immediately deterministic

### 6. Unknowns and assumptions discipline
- How to handle unknowns discovered during task specification
- When assumptions are permitted and how they must be documented
- Escalation conditions (when to stop and seek approval rather than proceeding)
- Reference to the evidence discipline defined in `target_agent_system.md`

### 7. Anti-patterns and prohibited content
Explicitly list what must NOT appear in codable task specifications:
- Full implementation code or detailed algorithms
- Tool command syntax or CLI instructions
- Duplicated schemas, standards, or governance rules
- Operational procedures or troubleshooting guides
- Business justification or high-level capability rationale (belongs in capability plans)

### 8. Relationship to other documentation
Clarify how codable task specifications relate to:
- **Capability plans** (parent decomposition source)
- **Implementation artifacts** (code, tests, scripts produced by executing tasks)
- **Operational documentation** (script cards, runbooks)
- **Standards and governance** (naming, validation, artifacts, job manifests)

### 9. Examples (minimal, non-normative)
Provide 1-2 short, clearly labeled examples that illustrate:
- A well-structured task specification
- Common mistakes or anti-patterns to avoid

Examples should be short (5-10 lines) and clearly marked as **NON-normative illustrations only**.

### 10. Compatibility and evolution
- When changes to this standard constitute breaking changes
- How to handle evolution of task specifications over time
- Versioning considerations (if applicable)

### 11. Open items / TBD section
List anything you could not ground in existing docs:
- Mark each item as TBD with explanation
- Indicate what evidence or approval is needed to resolve
- Propose 1-2 resolution options for human decision

## Output format requirements

- Produce a complete Markdown draft for `docs/standards/codable_task_spec.md`
- Follow the documentation formatting rules from `docs/standards/documentation_spec.md`:
  - Use ATX-style headers (`#`, `##`, `###`)
  - Number major sections for navigation
  - Use RFC 2119 keywords (MUST, SHOULD, MAY) for normative requirements
  - Include a purpose statement at the top
  - Include cross-references to related standards
- Add a short **"Consistency check"** appendix at the end:
  - Which existing documents you aligned with
  - Any potential conflicts you detected (if none, state "None detected")
  - Any assumptions/TBDs you introduced with rationale

## Escalation rule

If you cannot ground a key decision in existing docs, do not invent silently:
- Mark it as **TBD** in the "Open items" section
- Explain the impact of leaving it unresolved
- Propose 1-2 options for human decision
- Clearly label the assumption and its boundaries

Examples of items that might require escalation:
- Specific required fields if not evident from workflow_guide or examples
- Task naming/identification conventions if not covered by naming_standard
- Granularity thresholds (how to determine if a task is too large/small)
- Evidence formats if not covered by validation_standard

# Agent task: Draft `Contribution Approval Guide`

## Purpose
Create a process-layer document that defines **how work is proposed, reviewed, approved, and recorded** in this repository, ensuring that approval gates are clear, approval evidence is captured consistently, and decisions are traceable across all workflow stages.

## Where it lives
Target file: `docs/process/contribution_approval_guide.md`

## Context you must consider
You must read and align to the existing documentation set, especially:
- context baselines (development approach, target agent system, system context, documentation system catalog),
- glossary (do not redefine terms),
- workflow guide (ensure the guide supports the 5-step execution model, approval gates, and evidence discipline),
- other standards (naming, validation, documentation spec, decision records standard) to avoid duplication and ensure consistent cross-references,
- agent role charter (understand agent responsibilities and escalation triggers).

Do not modify context files.

## Following documents are not finalized and their current Content MUST NOT be used as info source or Format Standard:
- `docs/process/contribution_approval_guide.md` (the current version exists but is incomplete)
- `docs/standards/decision_records_standard.md`
- `docs/standards/validation_standard.md`

## What this guide must achieve (success criteria)
The resulting guide must:
1) Define **what constitutes a contribution** and when approval is required (triggering conditions).
2) Define **approval gate requirements** for each workflow step (Steps 1-5) with clear expectations for what must be approved before progression.
3) Define **approval evidence expectations** (what forms of approval are valid, what must be documented, where evidence lives).
4) Define **review expectations** (who reviews, what they check, how feedback is integrated).
5) Define **decision recording guidance** (when decisions must be recorded, how to reference decision records, relationship to the decision records standard).
6) Define **conflict entry points** (how to surface and handle conflicts between approved intent and implementation/evidence).
7) Integrate with the repository's existing governance model (human ownership of decisions, evidence discipline, explicit unknowns and controlled assumptions).
8) Make it clear **what belongs in the approval guide** vs what belongs in other documents (to prevent double truth).
9) Be practical, actionable, and consistent with existing workflow patterns.

## Boundaries (non-goals)
The guide must NOT:
- include normative schemas or required fields (those belong in standards),
- include tool/CLI instructions or troubleshooting (those belong in ops),
- embed large templates that would become a second source of truth,
- redefine glossary terms,
- duplicate workflow step definitions (those are in workflow guide),
- duplicate agent role definitions (those are in agent role charter),
- include philosophical rationale for approval gates (that belongs in context layer).

## What to include (content expectations)
Your draft should include:

### 1. Purpose + scope statement
- What problem this guide solves
- Why contribution approval process is necessary in this repository's working model
- What this guide covers vs what it doesn't
- Relationship to development approach, target agent system, and workflow guide

### 2. What constitutes a contribution (definitions and scope)
Define what types of work require the approval process:
- New work (objectives, pipelines, capabilities, code, documentation)
- Changes to existing work (updates, refactoring, breaking changes)
- Documentation changes (clarifications vs meaning changes)
- Conflict resolutions
- Decision records

Define what does NOT require formal approval (e.g., typo fixes, formatting improvements that don't change meaning).

Reference the glossary for key terms like "contribution," "approval," "evidence," "conflict."

### 3. Approval gate requirements per workflow step
For each of the 5 workflow steps, define:

#### Step 1: Define the Objective
- **What must be approved:** The objective artifact (scope, success criteria, boundaries, explicit unknowns)
- **Who approves:** Human (typically the requestor or designated decision-maker)
- **Approval criteria:** Exit criteria from workflow guide are met
- **Evidence required:** Approved objective document (location, format expectations)
- **Escalation triggers:** Scope ambiguity, non-evaluable success criteria, hidden unknowns

#### Step 2: Plan the Pipeline
- **What must be approved:** The pipeline plan (ordered capabilities, decision points, dependencies)
- **Who approves:** Human (typically the same decision-maker from Step 1)
- **Approval criteria:** Exit criteria from workflow guide are met
- **Evidence required:** Approved pipeline document (location, format expectations)
- **Escalation triggers:** Capability boundary conflicts, scope creep, unresolved dependencies

#### Step 3: Capability Planning
- **What must be approved:** The capability plan (boundaries, acceptance criteria, codable tasks)
- **Who approves:** Human
- **Approval criteria:** Exit criteria from workflow guide are met, tasks are bounded and traceable
- **Evidence required:** Approved capability plan (may be in issues, planning docs, or PR descriptions per workflow guide)
- **Escalation triggers:** Non-evaluable acceptance criteria, unbounded tasks, silent assumptions

#### Step 4: Execute Development Tasks
- **What must be approved:** Implementation changes (code, configuration, documentation)
- **Who approves:** Human (via PR review/approval mechanism)
- **Approval criteria:** Changes align with approved tasks, no unapproved scope expansion
- **Evidence required:** PR approval, merge commit, traceability to approved tasks
- **Escalation triggers:** Scope expansion, conflicts with standards/intent, new assumptions required

#### Step 5: Validate and Document
- **What must be approved:** Validation evidence and documentation updates
- **Who approves:** Human
- **Approval criteria:** Acceptance criteria met with evidence, documentation consistent with reality
- **Evidence required:** Validation report/evidence, updated documentation
- **Escalation triggers:** Evidence contradicts expectations, required evidence missing, documentation meaning changes

### 4. Approval evidence expectations (normative)
Define what constitutes valid approval evidence:

#### Forms of approval
- **PR approval:** GitHub PR approval mechanism (with explicit approver identity and timestamp)
- **Explicit sign-off:** Comment or discussion thread with clear approval statement
- **Issue closure:** For issues that represent objectives or capabilities, closure with completion evidence
- **Merge commit:** For implementation changes, the merge commit serves as approval evidence when combined with PR review
- **Decision record:** For governance-level decisions, reference to an approved decision record (see decision records standard)

#### Evidence documentation requirements
- **Traceability:** Every approval must be linkable/referenceable (PR number, issue number, decision record ID, commit SHA)
- **Approver identity:** Who approved must be clear
- **Approval timestamp:** When approval occurred must be captured
- **Approval scope:** What exactly was approved must be unambiguous (e.g., "Step 3 capability plan for XYZ")

#### Evidence storage and discoverability
- **PR-based work:** Approval evidence lives in PR review/approval records
- **Issue-based work:** Approval evidence lives in issue comments/closure
- **Decision records:** Approval evidence references live in the decision record (see decision records standard)
- **Planning documents:** Approval evidence may be captured in document change history (Git commits) or linked issues/PRs

### 5. Review expectations (normative)
Define what reviews must check and how feedback is handled:

#### Review scope per workflow step
- **Step 1-3 (Planning reviews):** Check alignment with previous steps, scope boundaries, evaluability of criteria, explicit treatment of unknowns/assumptions
- **Step 4 (Implementation reviews):** Check code quality, alignment with approved tasks, test coverage, no scope creep, no security vulnerabilities
- **Step 5 (Validation reviews):** Check evidence completeness, documentation accuracy, no double truth introduced

#### Reviewer responsibilities
- Surface conflicts between approved intent and implementation
- Check for unapproved assumptions or scope expansion
- Verify evidence claims are backed by actual evidence
- Ensure documentation changes maintain layer separation and single source of truth
- Flag escalation triggers per workflow guide

#### Feedback integration
- Reviewers provide feedback as comments/suggestions
- Author addresses feedback iteratively
- Approval withheld until exit criteria met and concerns resolved
- Escalation to human decision-maker if conflicts arise

### 6. Decision recording guidance (integration with decision records standard)
Define when and how to use decision records in the approval process:

#### When a decision record is required
Reference the decision records standard for triggering conditions. In the context of approvals:
- **Breaking changes to stable contracts:** Approval requires a decision record documenting the change, rationale, and approval evidence
- **Changes to foundational principles or governance rules:** Must be captured as a decision record
- **Conflict resolutions (intent vs implementation):** Resolution path must be documented in a decision record
- **Scope changes during execution:** If approved scope changes, document via decision record
- **Document type or canonical placement changes:** Must be captured as a decision record

#### How to reference decision records in approvals
- Decision records serve as approval evidence for governance-level changes
- PRs that implement decisions should reference the decision record ID
- Approval comments should cite decision records when relevant
- Decision records must include their own approval evidence (who approved the decision itself)

#### Relationship to decision records standard
- This guide defines **when and how approvals trigger decision records**
- Decision records standard defines **the structure and lifecycle of decision records themselves**
- Cross-reference the decision records standard; do not duplicate its normative content

### 7. Conflict entry points (integration with workflow guide conflict handling)
Define how to surface conflicts in the approval process:

#### Types of conflicts requiring explicit handling
- **Intent conflict:** Approved artifacts disagree with each other (e.g., objective vs capability plan)
- **Rules conflict:** Implementation conflicts with standards or governance rules
- **Runtime conflict:** Implementation behavior differs from approved intent
- **Evidence conflict:** Evidence contradicts claims or expected outcomes

#### How to surface conflicts
- Stop work and do not proceed with approval
- Document the conflict explicitly (what conflicts, why, evidence)
- Propose resolution options (at least two when possible)
- Escalate to human decision-maker

#### Conflict resolution approval process
- Human selects resolution path (align runtime to intent, or update intent with approval)
- Resolution is documented (via decision record if governance-level, or PR comment if implementation-level)
- Changes are applied and re-validated
- Approval resumes once conflict is resolved

Reference the workflow guide's conflict handling section for detailed procedures; do not duplicate.

### 8. Approval for different contribution types (operational guidance)
Provide practical guidance for common contribution scenarios:

#### Documentation-only changes
- **Clarifications/wording improvements (no meaning change):** Lightweight review, focus on accuracy and readability, no decision record needed
- **Meaning changes (intent/rules/responsibilities):** Full review against relevant standards, decision record if governance-level, human approval required

#### Code/implementation changes
- **Within approved scope:** Standard PR review process, approval via PR approval mechanism
- **Scope expansion:** Escalate, revise relevant planning step, obtain new approval before proceeding

#### Breaking changes
- **Requires:** Decision record, explicit approval with rationale, migration/impact documentation
- **Cross-reference:** Naming standard, artifacts catalog spec for breaking change definitions

#### Conflict resolutions
- **Requires:** Explicit conflict classification, resolution options proposed, human decision, decision record (if governance-level)
- **Cross-reference:** Workflow guide conflict handling section

### 9. Integration with existing governance and standards
Clarify how this guide relates to other governance artifacts:

#### Relationship to target agent system
- Approval gates defined here operationalize the principles in target agent system
- Evidence discipline defined here implements the evidence rules from target agent system
- Agent escalation triggers align with agent role charter

#### Relationship to workflow guide
- Workflow guide defines step execution procedures; this guide defines approval requirements per step
- Workflow guide defines exit criteria; this guide defines how exit criteria are approved
- Workflow guide defines conflict handling procedures; this guide defines conflict approval requirements

#### Relationship to validation standard
- Validation standard defines what evidence is valid; this guide defines how evidence supports approvals
- Validation tools produce evidence; approvals consume and evaluate that evidence

#### Relationship to documentation system catalog
- Catalog defines document types and boundaries; this guide ensures approvals respect those boundaries
- Catalog enforces single source of truth; this guide ensures approvals don't introduce double truth

### 10. Practical examples (non-normative)
Provide 2-3 short, clearly labeled NON-normative examples that illustrate:
- A typical Step 3 -> Step 4 approval (capability plan approved, implementation proceeds, PR approved and merged)
- A breaking change approval (decision record created, reviewed, approved, implementation follows)
- A conflict resolution approval (conflict surfaced, options proposed, human decides, resolution documented)

Keep examples minimal and focused on the approval flow, not the content.

### 11. Open items / TBD section
List anything you could not ground in existing docs, including:
- Any assumptions you had to make
- Areas where existing documentation is unclear or contradictory
- Questions that require human decision
- For each item, explain the impact and propose 1-2 resolution options

## Output format requirements
- Produce a complete Markdown draft for `docs/process/contribution_approval_guide.md`.
- Use clear section headings following the structure above (but feel free to reorganize for better flow).
- Use clear, actionable language appropriate for a process guide (not overly formal, but precise).
- Use normative keywords (MUST/SHOULD/MAY) sparingly and only where enforceability is critical.
- Add a short "Consistency check" appendix at the end:
  - which existing documents you aligned with,
  - any potential conflicts you detected,
  - any assumptions/TBDs you introduced.

## Escalation rule
If you cannot ground a key requirement (e.g., approval evidence forms, review scope, conflict handling integration) in existing docs, do not invent silently:
- mark it as TBD,
- explain impact,
- propose 1-2 options for human decision.

## Integration with best practices
You must also consider industry best practices for contribution and approval processes, such as:
- GitHub Pull Request review best practices
- Code review standards (readability, security, testability)
- Change control and approval workflows in software development
- Separation of duties and approval authority patterns
- Audit trail and traceability requirements

Balance these best practices with the specific needs and constraints of this repository's governance model. The goal is to create a guide that is:
- **Familiar** to engineers who have used standard PR review and approval processes
- **Aligned** with this repository's principles (human approval gates, evidence discipline, single source of truth, explicit conflict resolution)
- **Practical** and not overly bureaucratic
- **Enforceable** through existing GitHub mechanisms (PR reviews, issue tracking, decision records)

## How to approach this task
1. First, read all the context documents listed above to understand the repository's governance model and approval philosophy.
2. Review the workflow guide to understand the 5-step process and how approvals fit into each step.
3. Review the agent role charter to understand agent responsibilities and escalation triggers (these inform review expectations).
4. Review the decision records standard to understand when decision records are required and how they integrate with approvals.
5. Draft the guide section by section, grounding each requirement in either:
   - Explicit statements from context/standards/process documents, or
   - Industry best practices (labeled as such), or
   - Reasonable inferences from the governance model (labeled as assumptions).
6. As you draft, maintain a running list of open items/TBDs where you lack grounding.
7. Write the consistency check appendix last, reviewing your draft against all referenced documents.
8. If you encounter contradictions or ambiguities, escalate them in the TBD section rather than making arbitrary choices.

## Success indicators
You will know this task is complete when:
- The guide provides clear, actionable approval requirements for each workflow step
- Approval evidence expectations are explicit and enforceable
- Review expectations are clear and aligned with agent responsibilities
- Decision recording integration is explicit and non-duplicative
- Conflict entry points are clear and integrated with workflow guide procedures
- The guide respects layer separation and does not duplicate standards/schemas/tool manuals
- The guide is grounded in existing documentation with explicit references
- Any assumptions or TBDs are clearly marked and explained
- The consistency check confirms alignment with the documentation system

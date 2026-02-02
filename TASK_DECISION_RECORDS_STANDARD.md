# Agent task: Draft `Decision Records Standard`

## Purpose
Create a standards-layer document that defines the **normative way** this repository records explicit governance decisions, so that conflict resolution and contract evolution can be handled without silent changes and with full traceability.

## Where it lives
Target file: `docs/standards/decision_records_standard.md`

## Context you must consider
You must read and align to the existing documentation set, especially:
- context baselines (development approach, target agent system, system context, documentation system catalog),
- glossary (do not redefine terms),
- workflow guide (ensure the standard supports the 5-step execution model, approval gates, and evidence discipline),
- other standards (naming, validation, documentation spec, artifacts catalog spec, job manifest spec) to avoid duplication and ensure consistent cross-references.

Do not modify context files.

## Following documents are not finalised and their current Content MUST NOT be used as info source or Format Standard:
- `docs/process/contribution_approval_guide.md`
- `docs/standards/decision_records_standard.md` (the current version exists but is incomplete)
- `docs/standards/validation_standard.md`

## What this spec must achieve (success criteria)
The resulting spec must:
1) Define **when** a decision record is required (triggering conditions).
2) Define **what constitutes a decision record** (required sections/fields) in a normative way.
3) Define a **status lifecycle** for decision records (proposed, approved, superseded, etc.) with clear state transition rules.
4) Define **evidence and approval reference expectations** (what must be linked/referenced for a decision to be valid).
5) Integrate with the repository's existing governance model (approval gates, human ownership of decisions, explicit conflict resolution).
6) Make it clear **what belongs in a decision record** vs what belongs in other documents (to prevent double truth).
7) Be readable, enforceable, and practical (use MUST/SHOULD/MAY, but avoid unnecessary complexity).

## Boundaries (non-goals)
The spec must NOT:
- include general workflow instructions (those belong in workflow guide),
- include tool/CLI instructions or troubleshooting,
- embed large templates that would become a second source of truth (provide minimal structural examples only),
- redefine glossary terms,
- duplicate approval/evidence rules already defined in target agent system or validation standard,
- include operational guidance on how to file decisions (that belongs in process layer).

## What to include (content expectations)
Your draft should include:

### 1. Purpose + scope statement
- What problem this standard solves
- Why decision records are necessary in this repository's working model
- What this standard covers vs what it doesn't

### 2. When decision records are required (triggering conditions)
Define the normative conditions that **require** a decision record, such as:
- Breaking changes to stable contracts (naming, artifact IDs, schemas, APIs)
- Changes to foundational principles or governance rules
- Resolution of conflicts between approved intent and implemented reality
- Introduction or removal of document types or canonical placements
- Changes to approval gates or evidence expectations
- Explicit scope changes during execution
- Other governance-level decisions that affect multiple jobs or the system as a whole

Make it clear what does NOT require a decision record (routine implementation, clarifications that don't change meaning, etc.).

### 3. Decision record structure (normative)
Define the **minimum required sections/fields** that every decision record must contain:
- **Decision ID / Title**: How decisions are uniquely identified
- **Status**: Current state in the lifecycle (see section 4)
- **Context**: What situation triggered this decision
- **Decision**: What was decided (the actual choice made)
- **Rationale**: Why this decision was made (reasoning, trade-offs considered)
- **Consequences**: What changes as a result (impacts, migrations needed)
- **Approval reference**: Link to or description of human approval (who approved, when, how)
- **Evidence sources**: Links to supporting evidence (validation results, test outcomes, investigation findings)
- **Supersedes / Superseded by**: References to related decisions (if applicable)

Define any optional sections that MAY be included.

### 4. Status lifecycle (normative)
Define the allowed status values and transition rules:
- **Proposed**: Decision is drafted but not yet approved
- **Approved**: Decision has received human approval and is in effect
- **Superseded**: Decision has been replaced by a newer decision
- **Rejected**: Decision was proposed but explicitly rejected
- Any other states needed (e.g., "Under Review", "Implemented", etc.)

Define the rules for status transitions (what approvals or conditions are required).

### 5. Evidence and approval requirements (normative)
Define what constitutes valid evidence and approval references:
- What forms of approval are acceptable (PR approval, explicit sign-off, meeting notes, etc.)
- What level of evidence detail is required (links to validation reports, test results, investigation outputs)
- How to handle decisions made before this standard existed (grandfathering rules)

### 6. Storage and discovery (normative)
Define:
- **Canonical location**: Where decision records are stored (individual files, single log file, etc.)
- **Naming conventions**: How decision record files should be named (if using individual files)
- **Index maintenance**: Reference to the decision log catalog (`docs/catalogs/decision_log.md`) and what it must contain
- **Cross-referencing rules**: How other documents should reference decisions

### 7. Relationship to other governance artifacts
Clarify how decision records relate to:
- Approval gates defined in target agent system
- Validation evidence defined in validation standard
- Breaking change rules defined in naming standard and artifact catalog spec
- Contribution and approval processes (when finalized)

### 8. Minimal examples (non-normative)
Provide 1-2 short, clearly labeled NON-normative examples that illustrate:
- A simple decision record (e.g., approving a naming convention change)
- A decision record that supersedes another decision

Keep examples minimal and focused on structure, not content.

### 9. Open items / TBD section
List anything you could not ground in existing docs, including:
- Any assumptions you had to make
- Areas where existing documentation is unclear or contradictory
- Questions that require human decision
- For each item, explain the impact and propose 1-2 resolution options

## Output format requirements
- Produce a complete Markdown draft for `docs/standards/decision_records_standard.md`.
- Use clear section headings following the structure above.
- Use normative keywords (MUST/SHOULD/MAY) consistently and correctly.
- Add a short "Consistency check" appendix at the end:
  - which existing documents you aligned with,
  - any potential conflicts you detected,
  - any assumptions/TBDs you introduced.

## Escalation rule
If you cannot ground a key decision (e.g., status lifecycle states, required fields, approval requirements) in existing docs, do not invent silently:
- mark it as TBD,
- explain impact,
- propose 1-2 options for human decision.

## Integration with best practices
You must also consider industry best practices for decision records, such as:
- Architecture Decision Records (ADR) patterns commonly used in software development
- The MADR (Markdown Any Decision Records) format
- Lightweight decision record approaches that emphasize clarity and discoverability

Balance these best practices with the specific needs and constraints of this repository's governance model. The goal is to create a standard that is:
- **Familiar** to engineers who have used ADRs or similar approaches
- **Aligned** with this repository's principles (human approval gates, evidence discipline, single source of truth)
- **Practical** and not overly bureaucratic

## How to approach this task
1. First, read all the context documents listed above to understand the repository's governance model.
2. Identify patterns and requirements in existing standards (especially naming standard, artifacts catalog spec, documentation spec) that should be mirrored in the decision records standard.
3. Draft the standard section by section, grounding each requirement in either:
   - Explicit statements from context/standards documents, or
   - Industry best practices (labeled as such), or
   - Reasonable inferences from the governance model (labeled as assumptions).
4. As you draft, maintain a running list of open items/TBDs where you lack grounding.
5. Write the consistency check appendix last, reviewing your draft against all referenced documents.
6. If you encounter contradictions or ambiguities, escalate them in the TBD section rather than making arbitrary choices.

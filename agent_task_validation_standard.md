# Agent task: Draft `Validation Standard`

## Purpose
Create a standards-layer document that defines the **normative rules** for what "verified" means, what validations are required, and what evidence is acceptable for approvals, so that evidence discipline and approval gates can be operationalized without unverifiable claims.

## Where it lives
Target file: `docs/standards/validation_standard.md`

## Context you must consider
You must read and align to the existing documentation set, especially:
- context baselines (development approach, target agent system, system context, documentation system catalog),
- glossary (do not redefine terms),
- workflow guide (ensure the standard supports the 5-step execution model, approval gates, and evidence discipline),
- other standards (naming, documentation spec, decision records, artifacts catalog spec, job manifest spec) to avoid duplication and ensure consistent cross-references.

Do not modify context files.

## Following documents are not finalised and their current Content MUST NOT be used as info source or Format Standard:
- `docs/process/contribution_approval_guide.md`
- `docs/standards/decision_records_standard.md` (use structure/format as reference but not content expectations)
- `docs/standards/validation_standard.md` (the current version exists but must be treated as incomplete and potentially incorrect)

## What this spec must achieve (success criteria)
The resulting spec must:
1) Define **what "verified" means** in this repository's context with clear, testable semantics.
2) Define **when validation is required** (triggering conditions tied to the 5-step workflow).
3) Define **what constitutes acceptable evidence** for different types of claims (code changes, documentation changes, breaking changes, approvals).
4) Define **validation categories** and the validation rules that apply to each (structure validation, conformance validation, consistency validation, runtime validation).
5) Define **pass/fail semantics** and what happens when validation fails (blocking conditions, remediation expectations).
6) Define **evidence expectations** for approval gates at each workflow step.
7) Integrate with the repository's existing governance model (approval gates, human ownership of decisions, explicit conflict resolution, evidence discipline).
8) Make it clear **what types of validation exist** and where they are applied (tooling vs manual review, deterministic vs judgment-based).
9) Be readable, enforceable, and practical (use MUST/SHOULD/MAY, but avoid unnecessary complexity).

## Boundaries (non-goals)
The spec must NOT:
- include tool command syntax or CLI instructions (those belong in ops layer),
- include general workflow instructions (those belong in workflow guide),
- embed troubleshooting procedures or operational runbooks,
- redefine glossary terms,
- duplicate approval/evidence rules from target agent system (reference them instead),
- duplicate tool-specific validation logic (reference the tools that implement validation),
- include per-job validation specifics (those belong in per-job documentation).

## What to include (content expectations)
Your draft should include:

### 1. Purpose + scope statement
- What problem this standard solves
- Why validation and evidence discipline are necessary in this repository's working model
- What this standard covers vs what it doesn't
- How this standard relates to approval gates and evidence discipline defined in target agent system

### 2. Foundational principles (grounded in existing docs)
Reference and operationalize the principles from:
- Target agent system: evidence discipline, no hidden authority, explicit unknowns
- Documentation spec: evidence-based claims, explicit over implicit
- Development approach: validation against success criteria

Define what these principles mean for validation in practice.

### 3. What "verified" means (normative definition)
Define the conditions under which a claim can be labeled as "verified":
- What evidence is required
- What forms of evidence are acceptable
- When verification is sufficient vs when additional validation is needed
- The relationship between verification and approval

This should align with the glossary definition and target agent system rules about evidence.

### 4. When validation is required (triggering conditions)
Define the normative conditions that **require** validation, tied to:
- The 5-step workflow (which steps require validation, what kind)
- Approval gates (what validation must precede each approval)
- Change types (code changes, documentation changes, breaking changes, governance changes)
- Evidence production (when deterministic evidence must be generated)

Make it clear what does NOT require formal validation (e.g., trivial wording changes, draft exploration).

### 5. Validation categories and rules (normative)
Define the categories of validation that exist in this repository:

#### 5.1 Structure validation
- **What it validates:** Conformance to required file structures, naming conventions, metadata headers
- **When applied:** On all documentation and manifest files
- **Pass criteria:** Files follow naming standard, contain required sections, metadata is valid
- **Typical tools:** File system checks, manifest validators, structure checkers
- **Evidence output:** Validation reports showing pass/fail per file

#### 5.2 Conformance validation
- **What it validates:** Compliance with normative schemas and specifications
- **When applied:** On manifests, artifacts catalog entries, job descriptions, script cards
- **Pass criteria:** All required fields present, values match expected types/formats, cross-references are valid
- **Typical tools:** Schema validators, spec compliance checkers
- **Evidence output:** Conformance reports with specific failures listed

#### 5.3 Consistency validation
- **What it validates:** Internal consistency across related documents (e.g., job manifest references match artifacts catalog)
- **When applied:** After changes to related documents, before approval gates
- **Pass criteria:** No contradictions, all references resolve, cross-document constraints satisfied
- **Typical tools:** Cross-reference checkers, consistency scanners
- **Evidence output:** Consistency reports identifying contradictions or broken references

#### 5.4 Runtime validation
- **What it validates:** That implemented code/scripts behave as specified in their contracts
- **When applied:** After code changes, before Step 5 approval
- **Pass criteria:** Tests pass, outputs match expected formats, invariants hold, error handling works
- **Typical tools:** Unit tests, integration tests, output validators, behavior checks
- **Evidence output:** Test results, run logs, behavior verification reports

#### 5.5 Manual review validation
- **What it validates:** Judgment-based quality checks that cannot be fully automated
- **When applied:** At approval gates, for breaking changes, for governance decisions
- **Pass criteria:** Human reviewer confirms alignment with intent, quality standards, and principles
- **Typical tools:** PR reviews, decision record reviews, architectural reviews
- **Evidence output:** Approval records, review comments, sign-offs

For each category, define:
- What it checks
- When it's required
- What constitutes a pass
- What evidence it produces
- Whether it's deterministic (tool-based) or judgment-based (human review)

### 6. Evidence expectations by workflow step (normative)
Define what validation evidence is required at each step of the 5-step workflow:

**Step 1 (Define Objective):**
- What validation/evidence is needed before objective approval
- What constitutes "sufficient clarity" for an objective

**Step 2 (Plan Pipeline):**
- What validation/evidence is needed before pipeline approval
- How to verify pipeline completeness and feasibility

**Step 3 (Break Down Into Capability Plans):**
- What validation/evidence is needed before capability plan approval
- How to verify capability definitions are implementable

**Step 4 (Execute Development Tasks):**
- What validation is required during implementation
- What evidence must be produced before task completion
- When runtime validation is required

**Step 5 (Validate, Test, and Document):**
- What comprehensive validation is required
- What evidence must be assembled for final approval
- How to verify alignment with success criteria

### 7. Pass/fail semantics and blocking conditions (normative)
Define:
- **Pass criteria:** What constitutes validation success (all checks pass, evidence is complete, no contradictions)
- **Fail criteria:** What constitutes validation failure (missing evidence, validation errors, contradictions found)
- **Blocking conditions:** When validation failure must block progression:
  - Structural validation failures block file acceptance
  - Conformance validation failures block step approval
  - Consistency validation failures block merging
  - Runtime validation failures block deployment
  - Manual review rejection blocks approval
- **Non-blocking conditions:** When validation failures are informational but don't block (warnings, recommendations, best practice suggestions)
- **Remediation expectations:** What must happen when validation fails (fix and re-validate, escalate for decision, document exception)

### 8. Evidence formats and storage (normative)
Define:
- **Acceptable evidence formats:** Validation reports (JSON, text), test results (JUnit XML, TAP), logs, screenshots, approval records
- **Evidence requirements:** Evidence must be deterministic, reproducible, and reviewable
- **Evidence storage:** Where validation evidence lives (CI artifacts, PR comments, commit messages, decision records)
- **Evidence lifecycle:** How long evidence must be retained, when it can be discarded
- **Evidence references:** How to reference evidence from decision records, approvals, and documentation

### 9. Relationship to other governance artifacts
Clarify how validation relates to:
- Approval gates defined in target agent system (validation provides evidence for approvals)
- Evidence discipline defined in target agent system (validation operationalizes evidence expectations)
- Decision records standard (validation failures may trigger decision record creation)
- Breaking change rules defined in naming standard and artifact catalog spec (breaking changes require additional validation)
- Workflow guide (validation checkpoints in the 5-step execution)

### 10. Validation tools and references (non-normative)
Provide a brief overview (non-normative) of:
- What validation tools exist in this repository
- Where to find detailed tool documentation (reference ops layer)
- How tools relate to the validation categories defined above

**Do not include** tool command syntax, troubleshooting, or operational procedures. Reference `docs/ops/tooling_reference.md` and `docs/ops/ci_automation_reference.md` instead.

### 11. Minimal examples (non-normative)
Provide 1-2 short, clearly labeled NON-normative examples that illustrate:
- What validation evidence looks like for a simple code change
- What validation evidence looks like for a breaking change requiring decision record

Keep examples minimal and focused on the validation and evidence aspect, not the change content.

### 12. Open items / TBD section
List anything you could not ground in existing docs, including:
- Any assumptions you had to make
- Areas where existing documentation is unclear or contradictory
- Questions that require human decision
- For each item, explain the impact and propose 1-2 resolution options

## Output format requirements
- Produce a complete Markdown draft for `docs/standards/validation_standard.md`.
- Use clear section headings following the structure above.
- Use normative keywords (MUST/SHOULD/MAY) consistently and correctly (RFC 2119 style).
- Add a short "Consistency check" appendix at the end:
  - which existing documents you aligned with,
  - any potential conflicts you detected,
  - any assumptions/TBDs you introduced.

## Escalation rule
If you cannot ground a key decision (e.g., validation categories, evidence requirements, pass/fail semantics) in existing docs, do not invent silently:
- mark it as TBD,
- explain impact,
- propose 1-2 options for human decision.

## Integration with best practices
You must also consider industry best practices for validation and evidence discipline, such as:
- Test-driven development (TDD) validation patterns
- Continuous integration (CI) validation approaches
- Documentation validation and linting standards
- Schema validation best practices (JSON Schema, YAML validators)
- Evidence-based software engineering principles
- Automated quality gates in modern DevOps pipelines

Balance these best practices with the specific needs and constraints of this repository's governance model. The goal is to create a standard that is:
- **Familiar** to engineers who have used CI/CD pipelines and validation frameworks
- **Aligned** with this repository's principles (human approval gates, evidence discipline, single source of truth)
- **Practical** and not overly bureaucratic
- **Enforceable** through both automated tooling and human review

## How to approach this task
1. First, read all the context documents listed above to understand the repository's governance model and evidence discipline.
2. Identify patterns and requirements in existing standards (especially documentation spec, target agent system, decision records standard) that relate to validation and evidence.
3. Draft the standard section by section, grounding each requirement in either:
   - Explicit statements from context/standards documents, or
   - Industry best practices (labeled as such), or
   - Reasonable inferences from the governance model (labeled as assumptions).
4. As you draft, maintain a running list of open items/TBDs where you lack grounding.
5. Write the consistency check appendix last, reviewing your draft against all referenced documents.
6. If you encounter contradictions or ambiguities, escalate them in the TBD section rather than making arbitrary choices.
7. Remember: this is a STANDARDS document. It should define normative rules, not operational procedures. Keep tool syntax and troubleshooting in the ops layer.

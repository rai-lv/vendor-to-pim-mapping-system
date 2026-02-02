# Contribution and Approval Guide

## Purpose Statement

This guide defines **how work is proposed, reviewed, approved, and recorded** in the vendor-to-pim-mapping-system repository, ensuring that approval gates are clear, approval evidence is captured consistently, and decisions are traceable across all workflow stages.

### Why this guide exists

The repository's governance model requires **explicit human approval gates** at key workflow stages (ref: `target_agent_system.md`). This guide operationalizes those approval requirements by defining:

- What types of work require approval
- What must be approved at each workflow step
- What forms of approval are valid
- How approval evidence is documented and discovered
- How review and feedback integrate with the approval process
- When and how conflicts are surfaced and resolved

### Relationship to other documents

This guide:

- **Supports** the 5-step workflow defined in `development_approach.md` and `workflow_guide.md` by defining approval requirements per step
- **Implements** the approval gate and evidence discipline principles from `target_agent_system.md`
- **Integrates with** the decision records standard (`decision_records_standard.md`) for governance-level approvals
- **Aligns with** the agent role charter (`agent_role_charter.md`) for review expectations and escalation triggers
- **Complements** the validation standard (when finalized) for evidence-based approvals

### Scope and boundaries

**In scope:**
- Approval triggering conditions and gate requirements
- Approval evidence forms and documentation
- Review processes and feedback integration
- Decision recording for governance approvals
- Conflict surfacing and resolution entry points

**Out of scope (lives elsewhere):**
- Normative schemas and required fields (standards documents)
- Tool/CLI instructions and troubleshooting (ops layer)
- Step execution procedures (workflow guide)
- Agent role definitions (agent role charter)
- Philosophical rationale for approval gates (target agent system)

---

## 1. What Constitutes a Contribution

### 1.1 Contributions requiring approval

The following types of work require formal approval through the processes defined in this guide:

#### New work
- **Objectives** (Step 1): New problem statements or desired outcomes
- **Pipeline plans** (Step 2): Decomposition of objectives into capabilities
- **Capability definitions** (Step 3): Detailed specifications with codable task breakdowns
- **Code/configuration/documentation** (Step 4): Implementation of approved tasks
- **Validation evidence and documentation** (Step 5): Proof of acceptance criteria and updated docs

#### Changes to existing work
- **Updates to approved artifacts** that change meaning, scope, or acceptance criteria
- **Refactoring** that affects cross-job contracts or automation
- **Breaking changes** to stable identifiers, artifact contracts, or schemas
- **Documentation meaning changes** that alter intent, rules, or responsibilities

#### Governance artifacts
- **Decision records** documenting significant decisions (see Section 6)
- **Standards changes** that affect enforceable rules or validation requirements
- **Context document changes** that alter principles or workflow intent

#### Conflict resolutions
- **Intent conflicts** where approved artifacts disagree with each other
- **Rules conflicts** where standards conflict with artifacts
- **Runtime conflicts** where implementation behavior differs from approved intent
- **Evidence conflicts** where evidence contradicts claims or expectations

### 1.2 Work NOT requiring formal approval

The following work types do NOT require the formal approval process:

- **Typo fixes** and **formatting improvements** that don't change meaning
- **Clarifications** that improve wording/readability without altering intent or rules (Path A in workflow guide)
- **Bug fixes** that restore originally approved behavior without changing contracts
  - **Qualifies for exemption:** Fix aligns implementation with manifest/documentation that was previously approved (restores intent)
  - **Does NOT qualify for exemption:** Fix changes manifest/documentation to match current implementation (updates intent—requires approval)
  - **When in doubt:** If fixing the bug requires deciding "what should the correct behavior be?" rather than "what was the approved behavior?", seek approval
- **Internal refactoring** within a job that doesn't affect its manifest or cross-job contracts
- **Temporary/intermediate artifacts** within a job that aren't consumed by other jobs

**Boundary test:** Ask "Does this change affect stable contracts, governance rules, approved scope, or require re-approval of previously approved intent?" If no, formal approval is not required.

### 1.3 Key terms (cross-referenced to glossary)

For canonical definitions, see `docs/context/glossary.md`:

- **Approval gate** — A point where progression requires explicit human sign-off
- **Evidence** — Deterministic outputs that support approval decisions
- **Conflict** — Any mismatch between approved intent and observed reality
- **Breaking change** — A change that requires migration, deprecation period, or coordination
- **Contribution** — (this guide defines contribution scope)
- **Decision record** — A structured document recording significant decisions

---

## 2. Approval Gate Requirements Per Workflow Step

This section defines approval requirements for each of the 5 workflow steps. For step execution procedures, see `workflow_guide.md`.

### 2.0 Definition: Material Change

A "material change" is a change that affects scope boundaries, success criteria, acceptance criteria, or approval conditions. Material changes require re-approval.

**Material changes include:**
- Adding, removing, or modifying scope boundaries or out-of-scope statements
- Adding, removing, or modifying success criteria or acceptance criteria
- Changing capability boundaries or task boundaries
- Adding or removing unknowns/assumptions
- Changing traceability (pointing to different parent artifact)
- Modifying approval conditions or gate requirements

**Non-material changes include:**
- Wording improvements that don't change meaning
- Formatting or structural reorganization
- Adding clarifications that make existing criteria more explicit
- Correcting typos or grammatical errors
- Adding examples that illustrate existing criteria

**When in doubt:** Treat as material and seek re-approval. It's better to over-communicate than to bypass approval gates.

### 2.1 Step 1: Define the Objective

**What must be approved:**
- The objective artifact containing:
  - Clear problem statement or desired outcome
  - Evaluable success criteria
  - Scope boundaries (in-scope / out-of-scope)
  - Explicit unknowns or controlled assumptions

**Who approves:**
- Human decision-maker (typically the requestor or designated owner)

**Approval criteria:**
- Exit criteria from `workflow_guide.md` Section 2 are met:
  - Success criteria exist and are evaluable
  - Scope boundaries are unambiguous
  - Unknowns are explicitly listed (not hidden)
  - No downstream implementation details embedded

**Evidence required:**
- Approved objective document (GitHub issue, planning document, or PR description)
- Approval evidence: issue comment, PR approval, or explicit sign-off

**Approval storage/discoverability:**
- For issue-based objectives: approval via issue comment or label
- For planning documents: approval via PR review when committed
- For inline objectives: approval in parent PR/issue

**Escalation triggers (from workflow guide and agent role charter):**
- Scope cannot be bounded
- Success criteria cannot be evaluated
- Critical unknowns block pipeline planning but are not acknowledged

**Iteration:**
- Iteration within Step 1 is allowed and does not require re-approval
- Re-approval required only if changes are material (per Section 2.0 definition)

---

### 2.2 Step 2: Plan the Pipeline

**What must be approved:**
- The pipeline plan containing:
  - Ordered list of capabilities
  - Capability boundaries (short purpose per capability)
  - Known dependencies and decision points
  - Alignment with approved objective

**Who approves:**
- Human decision-maker (typically the same owner from Step 1)

**Approval criteria:**
- Exit criteria from `workflow_guide.md` Section 3 are met:
  - Each capability has clear boundary
  - List is ordered sufficiently to start capability planning
  - Known decision points/dependencies are explicit
  - Pipeline does not expand beyond objective scope

**Evidence required:**
- Approved pipeline document (issue, planning doc, or PR description)
- Traceability to approved objective
- Approval evidence: issue comment, PR approval, or explicit sign-off

**Approval storage/discoverability:**
- Same storage options as Step 1
- MUST reference the approved objective it derives from

**Escalation triggers:**
- Capabilities overlap so heavily that boundaries are unclear
- Ordering depends on unresolved, unapproved assumptions
- Pipeline introduces out-of-scope elements

**Iteration:**
- Iteration within Step 2 is allowed
- Re-approval required if changes are material (per Section 2.0 definition)

---

### 2.3 Step 3: Capability Planning

**What must be approved:**
- The capability plan containing:
  - Capability boundary statement (what it does and does NOT do)
  - Acceptance criteria (minimal and evaluable)
  - Inputs, outputs, rules, constraints
  - Codable task breakdown (individuable, bounded, traceable)
  - Explicit unknowns/assumptions

**Who approves:**
- Human decision-maker

**Approval criteria:**
- Exit criteria from `workflow_guide.md` Section 4 are met:
  - Capability boundary is unambiguous
  - Acceptance criteria are evaluable
  - Tasks are bounded and cover the capability
  - Unknowns/assumptions are explicitly handled
  - No standards/schema content duplicated inside capability plan

**Evidence required:**
- Approved capability plan document following structure from `codable_task_spec.md`
- Traceability to approved pipeline plan
- Approval evidence: issue comment, PR approval, or explicit sign-off

**Approval storage/discoverability (from workflow guide Section 4):**
- **GitHub Issues** — For issue-tracked work, capability plans in issue descriptions
- **Planning documents** — Markdown files in `docs/planning/` or project-specific location
- **PR descriptions** — For single-PR capabilities

**Required traceability:**
- Capability plans MUST reference approved pipeline plan
- Codable tasks MUST reference parent capability

**Escalation triggers:**
- Acceptance criteria cannot be evaluated
- Tasks cannot be bounded without introducing new assumptions
- Capability plan leaks into standards/templates or ops/tool manuals

**Iteration:**
- Iteration within Step 3 is allowed
- Re-approval required if changes are material (per Section 2.0 definition)

---

### 2.4 Step 4: Execute Development Tasks

**What must be approved:**
- Implementation changes (code, configuration, documentation) that:
  - Implement approved codable tasks
  - Stay within approved task boundaries
  - Produce intended outcomes from capability plan
  - Do not expand scope without escalation

**Who approves:**
- Human reviewer (via PR review/approval mechanism)

**Approval criteria:**
- Exit criteria from `workflow_guide.md` Section 5 are met:
  - Each codable task's intended outcome exists in the repo
  - Changes are traceable to approved tasks
  - No unapproved scope expansion occurred

**Evidence required:**
- PR approval via GitHub's PR approval mechanism
- Merge commit as implementation approval evidence
- Traceability to approved tasks (PR references capability/task identifiers)

**Approval storage/discoverability:**
- PR approval records (GitHub API accessible)
- Merge commits with references to approved capability/tasks
- Code review comments as feedback trail

**Escalation triggers:**
- Implementation requires changing acceptance criteria
- Implementation requires new assumptions
- Implementation conflicts with standards or existing approved intent
- Scope expansion beyond defined task boundaries

**Iteration:**
- Implementation review is iterative
- Approval withheld until concerns resolved and exit criteria met

---

### 2.5 Step 5: Validate and Document

**What must be approved:**
- Validation evidence demonstrating acceptance criteria are met
- Documentation updates reflecting implemented reality
- Consistency with approved intent and implemented behavior

**Who approves:**
- Human decision-maker (reviewing evidence and documentation)

**Approval criteria:**
- Exit criteria from `workflow_guide.md` Section 6 are met:
  - Evidence exists or gaps are explicitly documented and approved
  - Documentation reflects outcomes without contradicting intent/rules/runtime
  - No "verified/confirmed" claims without referenced evidence

**Evidence required:**
- Validation evidence (test results, validation reports, run receipts, logs)
- Updated documentation with correct layer placement
- Doc Impact Scan confirmation (no double truth, correct routing)

**Approval storage/discoverability:**
- Validation evidence stored in job artifacts, test outputs, or validation reports
- Documentation updates approved via PR approval mechanism
- Evidence references in validation summaries or acceptance criteria mapping

**Escalation triggers:**
- Evidence contradicts expected behavior
- Required evidence is missing and cannot be justified
- Documentation changes would alter meaning without going back to earlier steps

**Iteration:**
- Validation and documentation review is iterative
- Re-validation required if significant changes made after initial review

---

### 2.6 Approval Authority and Independence

This section defines who can approve work and establishes requirements to ensure approval integrity.

**Single-person team exception:**
When there is only one team member, that person has absolute authority to approve all work, including their own contributions. Self-approval is permitted and necessary for the system to function. The independence requirements below apply only when there are multiple team members.

**Self-approval rules (multi-person teams):**
When there are two or more team members:
- Contributors should not approve their own work when independent reviewers are available
- All approvals should involve independent peer review when feasible
- Self-approval may be necessary in exceptional cases (emergency fixes, sole domain expert) but should be documented with rationale

**Independence definition (multi-person teams):**
An independent reviewer is someone who:
- Did not author the work being approved
- Is not directly supervised by or supervising the author
- Has no direct conflict of interest in the specific work being approved

**Approval authority by workflow step:**

- **Steps 1-3 (Planning):** Any qualified team member can approve. "Qualified" means familiar with the domain and governance process. For single-person team: sole member approves.
- **Step 4 (Implementation):** Code owners or designated reviewers for affected areas. When formal code owners are not defined, any qualified team member. For single-person team: sole member approves.
- **Step 5 (Validation):** Same authority as Step 4, with focus on evidence review rather than implementation details. For single-person team: sole member approves.
- **Governance decisions (Decision records):** Team maintainers or designated decision-makers as defined by team processes. For single-person team: sole member approves.

**When designated approver is unavailable (multi-person teams):**
- **Planned absence:** Designate backup approver before absence begins
- **Unplanned absence:** Escalate to team lead, maintainers, or next available qualified reviewer
- **Maximum wait time:** 5 business days before auto-escalation to team maintainers

**Authority conflicts:**
If approval authority is unclear for a specific contribution, escalate to team maintainers for clarification. For single-person team: sole member decides. Document the clarification for future reference.

**Scaling note:** As the team grows from one to multiple members, the independence requirements and self-approval restrictions automatically apply. No decision record required for this transition—it's an organic scaling of the approval model. However, when first adding team members, document the team's approach to code review and approval authority.

---

## 3. Approval Evidence Expectations

This section defines what constitutes valid approval evidence and how it must be documented.

### 3.1 Forms of approval evidence

The following forms constitute valid approval evidence:

#### PR approval (implementation changes)
- **Mechanism:** GitHub PR approval via the "Approve" review action
- **Approver identity:** GitHub username of approver
- **Timestamp:** GitHub-recorded approval timestamp
- **Approval scope:** The specific changes in the PR at the time of approval
- **Usage:** Standard mechanism for Step 4 (implementation) approvals

#### Explicit sign-off (planning stages)
- **Mechanism:** Comment or discussion thread with clear approval statement
- **Examples:**
  - "Approved for Step 2 progression" in issue comment
  - "Objective looks good, proceed to pipeline planning" in PR comment
  - "Capability plan approved, proceed to implementation"
- **Required elements:** Clear approval statement, approver identity (comment author)
- **Usage:** Steps 1-3 (planning) approvals when not using PR mechanism

#### Issue closure with completion evidence
- **Mechanism:** Closing an issue that represents an objective or capability
- **Required:** Closure must include completion evidence or reference to merged implementation
- **Approver identity:** Issue closer (typically same as approver)
- **Usage:** When objectives or capabilities are tracked as issues

#### Decision record approval
- **Mechanism:** Approved decision record (status: Approved) per `decision_records_standard.md`
- **Required elements:** Decision record with Status section showing "Approved", approver identity, approval date
- **Usage:** Governance-level decisions (breaking changes, principle changes, conflict resolutions)
- **Cross-reference:** See Section 5 (Decision Recording Guidance)

### 3.1A Execution confirmation (not approval evidence)

The following artifacts confirm that approved work was executed, but are not approval evidence themselves:

#### Merge commit
- **Mechanism:** Merge commit SHA in Git history
- **Purpose:** Confirms that approved changes were merged into the repository
- **Required context:** Must reference PR number or approval evidence (e.g., "Merge PR #124")
- **Usage:** Proves execution of work that was already approved via PR approval or decision record
- **Important distinction:** Merge commit is **execution confirmation**, not approval evidence. The approval must exist before merge (via PR approval mechanism or other approval forms above). Merge commit demonstrates that approved work was completed and integrated.

### 3.2 Evidence documentation requirements

All approval evidence MUST meet the following requirements:

#### Traceability
- Every approval must be linkable/referenceable via:
  - PR number (e.g., `#123`)
  - Issue number (e.g., `#456`)
  - Decision record ID (e.g., `DR-0001`)
  - Commit SHA (for merge commits)
  - Comment URL (for explicit sign-offs)

#### Approver identity
- Who approved must be clear and auditable
- GitHub username for PR approvals and comments
- Name/Role for decision records (ref: `decision_records_standard.md` Section 3.1.2)

#### Approval timestamp
- When approval occurred must be captured
- GitHub automatically timestamps PR approvals and comments
- Decision records include explicit date field

#### Approval scope
- What exactly was approved must be unambiguous
- Examples:
  - "Step 3 capability plan for vendor product matching"
  - "PR #123: Implementation of codable tasks 3.1-3.5"
  - "DR-0042: Breaking change to artifact naming convention"

### 3.3 Evidence storage and discoverability

#### PR-based work
- **Storage:** GitHub PR records (approvals, reviews, comments)
- **Discovery:** PR number referenced in commits, issues, or documentation
- **Retention:** Permanent (GitHub retention policies)

#### Issue-based work
- **Storage:** GitHub issue comments, labels, closure evidence
- **Discovery:** Issue number referenced in related artifacts
- **Retention:** Permanent

#### Decision records
- **Storage:** Decision record files in `docs/decisions/` per `decision_records_standard.md`
- **Discovery:** Decision log (`docs/catalogs/decision_log.md`) provides index
- **Retention:** Permanent; superseded decisions remain for historical reference

#### Planning documents
- **Storage:** Git commit history for documents in `docs/planning/` or job-specific locations
- **Discovery:** Document references in issues, PRs, or capability plans
- **Retention:** Permanent via Git history

#### Evidence artifacts (validation)
- **Storage:** Job output artifacts, test results, validation reports
- **Discovery:** Referenced in validation summaries, PR descriptions, or acceptance criteria mapping
- **Retention:** Per artifact lifecycle policies

### 3.4 Evidence discipline (from target agent system)

These rules apply to all approval evidence:

- Evidence must be **deterministic and reviewable**
- Agents may summarize evidence but **must not substitute narrative for proof**
- Lack of evidence must be **recorded explicitly** (e.g., "evidence missing / TBD") and blocks approval unless human explicitly approves proceeding under controlled assumption
- Agents may use "verified" or "confirmed" **only when explicit evidence is referenced**

### 3.5 Approval Withdrawal and Revocation

Approval can be withdrawn before work is merged if circumstances change or errors are discovered.

#### Who can revoke approval

- **Original approver** can withdraw their own approval at any time before merge
- **Any reviewer** who discovers critical issues can request approval revocation
- **Team maintainers** can revoke approval for governance or security reasons

#### Process for revoking approval

**Step 1: Document reason**
- Add comment to PR/Issue stating reason for revocation
- Reference specific concern (e.g., "Security vulnerability discovered in lines 45-60", "Conflicts with newly-approved DR-0042")
- Tag the PR author and any other approvers

**Step 2: Notify stakeholders**
- Notify PR author and other approvers
- If multiple approvals exist, specify which approval(s) are revoked
- Provide clear guidance on what must be addressed

**Step 3: Resolution required**
- Author addresses concern or discusses with revoker
- Changes may require re-review by multiple reviewers depending on scope
- Once adequately addressed, new approval sought (same process as original approval)

#### Auto-revocation conditions

Approval is automatically considered invalid (and should be formally revoked) if:

- **Material changes after approval:** Approved artifact is materially changed after approval was given (per Section 2.0 definition). GitHub's "Dismiss stale reviews" setting can help enforce this.
- **Dependency approval revoked:** If PR B depends on approved PR A, and PR A's approval is revoked, PR B's approval should also be reviewed and may need revocation.
- **Decision record rejected:** If a decision record approval was required for the work, and the decision record is subsequently rejected, the dependent work's approval is invalid.
- **Conflict discovered:** If a runtime, intent, rules, or evidence conflict is discovered after approval that affects the approved work (per Section 6).

#### Re-approval after revocation

After approval is revoked and concerns are addressed:
- Author updates the work and notifies reviewers
- Re-approval follows the same process as initial approval (same evidence requirements, same authority rules from Section 2.6)
- Revocation and resolution should be documented in the approval trail (PR comments or issue updates)

---

## 4. Review Expectations

This section defines what reviews must check and how feedback is integrated into the approval process.

### 4.1 Review scope per workflow step

#### Steps 1-3 (Planning reviews)

**What reviewers check:**
- **Alignment** with previous steps (objective → pipeline → capability)
- **Scope boundaries** are clear and respected
- **Evaluability** of success criteria and acceptance criteria
- **Explicit treatment** of unknowns/assumptions (not hidden or silently introduced)
- **Exit criteria** from workflow guide are met
- **No scope creep** beyond approved boundaries
- **Traceability** to parent artifacts

**Relevant agent responsibilities (from agent role charter):**
- Objective Support Agent: Flag scope ambiguity, non-testable criteria, hidden unknowns
- Pipeline Support Agent: Flag unclear capability boundaries, unresolved assumption dependencies
- Capability Support Agent: Flag non-evaluable acceptance criteria, unbounded tasks, silent assumptions

#### Step 4 (Implementation reviews)

**What reviewers check:**
- **Code quality** (readability, maintainability, consistency with repository patterns)
- **Alignment** with approved tasks (no scope expansion)
- **Test coverage** (when applicable and feasible)
- **No security vulnerabilities** (ref: security tools when available)
- **No scope creep** (implementation stays within task boundaries)
- **Standards conformance** (naming, documentation, manifest structure)
- **Traceability** (changes reference approved tasks/capabilities)

**Relevant agent responsibilities (from agent role charter):**
- Coding Agent: Flag scope creep, missing prerequisites, conflicts with approved intent

#### Step 5 (Validation and documentation reviews)

**What reviewers check:**
- **Evidence completeness** (all acceptance criteria addressed)
- **Documentation accuracy** (reflects implemented reality)
- **No double truth** introduced (documentation doesn't duplicate standards or create competing authority)
- **Correct layer separation** (context vs standards vs process vs ops)
- **Evidence discipline** (no unverified claims; deterministic evidence referenced)

**Relevant agent responsibilities (from agent role charter):**
- Validation Support Agent: Flag contradictions between evidence and expectations, missing evidence
- Documentation Support Agent: Flag contradictory statements, wrong-layer content, double truth

### 4.2 Reviewer responsibilities

Reviewers (human or agent-assisted) have the following responsibilities:

#### Surface conflicts
- Identify and explicitly surface conflicts between:
  - Approved intent and implementation
  - Standards and artifacts
  - Expected behavior and evidence
  - Documentation claims and runtime reality

#### Check for unapproved assumptions
- Flag any assumptions introduced during implementation that were not in approved capability plan
- Require escalation and re-approval before proceeding

#### Verify evidence claims
- Ensure any "verified" or "confirmed" statements reference explicit evidence
- Flag narrative claims that lack supporting evidence
- Accept explicit "TBD" or "unknown" statements (evidence discipline principle)

#### Ensure documentation layer separation
- Check that documentation changes respect canonical placement (per `documentation_system_catalog.md`)
- Flag content in wrong layer (e.g., tool syntax in context docs, standards embedded in process docs)
- Propose re-homing when needed

#### Flag escalation triggers
- Identify situations requiring escalation per workflow guide and agent role charter:
  - Acceptance criteria changes needed
  - New assumptions required
  - Standards conflicts
  - Scope expansion
  - Evidence contradictions

### 4.3 Feedback integration

The following process applies to integrating review feedback:

#### Feedback delivery
- Reviewers provide feedback as:
  - PR review comments (for code/implementation)
  - Issue comments (for planning artifacts)
  - Inline suggestions (when using GitHub suggestion feature)

#### Author response
- Author addresses feedback iteratively
- Changes made in response documented (reply to comments or commit messages)
- If disagreement, explicit discussion required (not silent override)

#### Approval withheld until concerns resolved
- Approval is NOT given until:
  - Exit criteria are met
  - Review concerns are addressed
  - Evidence or rationale provided for any disagreements

#### Escalation to decision-maker
- If conflicts arise that cannot be resolved through discussion:
  - Escalate to human decision-maker (not silent resolution)
  - Document the conflict and resolution options
  - Human selects resolution path (ref: workflow guide Section 7)

### 4.4 Review best practices (industry alignment)

These practices align with standard PR review and code review processes:

- **Constructive feedback** — Focus on improvement, not criticism
- **Specific and actionable** — Point to exact lines/sections, suggest alternatives
- **Balanced perspective** — Acknowledge good aspects alongside concerns
- **Focus on high-signal issues** — Prioritize bugs, security, logic errors, and contract violations over style preferences
- **Timely reviews** — Review promptly to avoid blocking work
- **Iterative refinement** — Expect multiple rounds of feedback and revision

---

## 5. Decision Recording Guidance

This section defines when and how to use decision records in the approval process. For complete decision record structure and requirements, see `decision_records_standard.md`.

### 5.1 When a decision record is required

Decision records are required when governance-level decisions must be documented and approved.

**Authoritative source:** See `decision_records_standard.md` Section 2.1 for the complete list of triggering conditions and detailed examples.

**Common scenarios in approval workflows:**

- **Breaking changes:** Renaming identifiers, changing artifact contracts, modifying manifest schemas (requires decision record BEFORE implementation approval)
- **Governance changes:** Modifying approval gates, changing workflow structure, altering principles or operating rules
- **Conflict resolutions:** When resolving conflicts that change governance rules or principles (implementation-level conflicts don't require decision records—see Section 6)
- **Scope expansions:** When approved scope must change during execution (affects approved objective, pipeline, or capability)
- **Standards exceptions:** When specific case requires exception to established standard or principle
- **Architecture decisions:** Significant design decisions affecting multiple components or system-wide behavior

**Integration with approval process:**
When a triggering condition occurs during the approval workflow:
1. Pause the current approval process
2. Create and approve decision record per Section 5.4 below
3. Resume original approval process with decision record reference

**Cross-reference discipline:**
This guide defines WHEN decision records integrate with approvals and HOW they serve as approval evidence. `decision_records_standard.md` remains the authoritative source for decision record structure, lifecycle, triggering conditions, and storage requirements.

### 5.2 How to reference decision records in approvals

#### Decision records serve as approval evidence
- An approved decision record (status: Approved) is a form of approval evidence
- PRs implementing decisions SHOULD reference the decision record ID
- Example: "This PR implements DR-0042 (artifact naming convention change)"

#### Approval comments should cite decision records
- When approving work that implements a decision, reference the decision record
- Example: "Approved per DR-0042. Migration plan looks good."

#### Decision records must include their own approval evidence
- Decision record Status section must document:
  - Who approved the decision
  - When it was approved
  - Reference to approval evidence (PR approval, explicit sign-off)
- Ref: `decision_records_standard.md` Section 3.1.2

### 5.3 Relationship to decision records standard

**Division of responsibilities:**

This guide defines:
- **WHEN** approvals trigger decision records (ref: Section 5.1 above)
- **HOW** decision records integrate with the approval process (ref: Section 5.2 above)

Decision records standard defines:
- **STRUCTURE** of decision records (required sections, format)
- **LIFECYCLE** (status transitions, superseding, deprecation)
- **STORAGE** (file naming, decision log maintenance)

**Cross-reference principle:**
- This guide MUST NOT duplicate the normative structure from decision records standard
- When decision record structure changes, this guide remains stable
- Decision records standard is the authoritative source for decision record format

### 5.4 Approval process for decision records

Creating and approving a decision record IS the governance approval process for changes requiring decision records:

**Step 1: Draft decision record**
- Author (human or agent-assisted) creates decision record file
- Follow structure from `decision_records_standard.md`
- Status: Proposed

**Step 2: Review decision record**
- Reviewers check:
  - Context is clear and complete
  - Alternatives were considered
  - Rationale is sound
  - Consequences are explicit (positive and negative)
- Iterate until concerns addressed

**Step 3: Approve decision record**
- Human decision-maker approves (typically via PR approval)
- Update Status section:
  - Status: Approved
  - Date: approval date
  - Approved by: approver identity
- Merge decision record into repository

**Step 4: Implement decision**
- Implementation work references the approved decision record
- Implementation approval follows standard process (PR approval)
- Implementation MUST align with approved decision

---

## 6. Conflict Entry Points

This section defines how to surface conflicts in the approval process and integrate with workflow guide conflict handling. For detailed conflict resolution procedures, see `workflow_guide.md` Section 7.

### 6.1 Types of conflicts requiring explicit handling

The following conflict types MUST be surfaced and cannot proceed to approval:

#### Intent conflict
- **Definition:** Approved artifacts disagree with each other
- **Examples:**
  - Objective states "support BMEcat format only" but pipeline includes "parse CSV files"
  - Capability plan acceptance criteria conflict with objective success criteria
  - Codable task boundaries conflict with capability boundaries

#### Rules conflict
- **Definition:** Implementation conflicts with standards or governance rules
- **Examples:**
  - Code uses camelCase job IDs when standard requires snake_case
  - Documentation embeds normative schemas in wrong layer
  - Job manifest violates required field constraints from `job_manifest_spec.md`

#### Runtime conflict
- **Definition:** Implementation behavior differs from approved intent
- **Examples:**
  - Job manifest declares output as required, but script makes it optional
  - Implementation produces different artifacts than approved capability plan specified
  - Code behavior contradicts business description documentation

#### Evidence conflict
- **Definition:** Evidence contradicts claims or expected outcomes
- **Examples:**
  - Documentation claims feature is "verified" but no evidence exists
  - Test results show failures but acceptance criteria marked as met
  - Validation report contradicts implementation claims

#### Decision conflict
- **Definition:** Two or more approved decision records contradict each other
- **Examples:**
  - DR-0001 requires snake_case universally, but DR-0025 allows camelCase exceptions
- **Resolution:** Create new decision record that supersedes one or both conflicting decisions (ref: `decision_records_standard.md` Section 2.1.3)

### 6.2 How to surface conflicts

When reviewing work, systematically check for conflicts before approval:

#### Conflict detection checklist

Use this checklist to systematically detect conflicts during review:

**For Steps 1-3 (Planning reviews):**
- [ ] **Alignment check:** Does this artifact align with its parent artifact? (objective → pipeline → capability)
- [ ] **Consistency check:** Do success/acceptance criteria contradict each other within or across artifacts?
- [ ] **Scope check:** Do scope boundaries align across all related artifacts?
- [ ] **Decision check:** Review decision log for relevant decisions that might conflict with this work
- [ ] **Standards check:** Does this planning artifact comply with repository standards?

**For Step 4 (Implementation reviews):**
- [ ] **Capability alignment:** Does implementation match the approved capability plan and task definitions?
- [ ] **Contract consistency:** Do manifest declarations match code behavior? (e.g., required fields, output contracts)
- [ ] **Standards compliance:** Does code follow naming conventions, documentation standards, and structure requirements?
- [ ] **Traceability:** Can changes be traced back to approved tasks or capabilities?
- [ ] **Cross-reference check:** If implementation references other jobs/artifacts, are those references correct and current?

**For Step 5 (Validation reviews):**
- [ ] **Evidence validity:** Does evidence actually support the claims being made?
- [ ] **Documentation accuracy:** Does documentation reflect implemented reality (not aspirational behavior)?
- [ ] **Double truth check:** Does documentation duplicate content that should only exist in standards or other authoritative locations?
- [ ] **Layer separation:** Is content in the correct document type/layer?

**If any checklist item fails or raises concern:** Surface the conflict using the process below.

#### Conflict surfacing procedure

When a conflict is detected (via checklist or observation), the following procedure applies:

**Step 1: Stop work and do not proceed with approval**
- Halt progression immediately
- Do NOT attempt to silently resolve the conflict
- Do NOT approve conflicting artifacts

**Step 2: Document the conflict explicitly**
- State what conflicts (be specific)
- Explain why it's a conflict (what principle/rule/expectation is violated)
- Reference evidence (point to specific artifacts, lines, behavior)

**Step 3: Classify the conflict**
- Identify conflict type: intent / rules / runtime / evidence / decision
- Determine severity: blocking (cannot proceed) vs non-blocking (can address later)

**Step 4: Propose resolution options**
- Present at least two options when possible
- Examples:
  - Option A: Align implementation to approved intent
  - Option B: Update intent with explicit approval (via decision record if governance-level)
  - Option C: Document exception with rationale

**Step 5: Escalate to human decision-maker**
- Human selects resolution path
- Document the decision (comment for implementation-level, decision record for governance-level)

### 6.3 Conflict resolution approval process

Once a resolution path is selected:

#### For implementation-level conflicts (no governance change)
- Apply changes to align conflicting elements
- Document resolution in PR comment or issue
- Re-validate that conflict is resolved
- Resume approval process

#### For governance-level conflicts (principles/rules change)
- Create decision record documenting:
  - The conflict (Context section)
  - Resolution chosen (Decision section)
  - Rationale and alternatives (Rationale section)
  - Impact (Consequences section)
- Approve decision record per Section 5.4
- Apply changes according to approved decision
- Re-validate and resume approval

### 6.4 Integration with workflow guide

**Reference point:**
- This guide defines **conflict entry points in the approval process**
- Workflow guide (`workflow_guide.md` Section 7) defines **detailed conflict resolution procedures**

**Division of responsibility:**
- **This guide:** When to stop approval, how to surface conflicts, approval requirements for resolutions
- **Workflow guide:** Classification taxonomy, step-by-step resolution procedures, re-homing procedures

**Cross-reference rule:**
- This guide MUST NOT duplicate workflow guide conflict handling procedures
- When workflow guide procedures change, this guide remains stable

### 6.5 Concurrent Approvals and Merge Coordination

When multiple PRs are in flight that depend on the same approved artifacts or affect the same code/documents, coordination is required to prevent conflicts and ensure approval validity.

#### Upstream changes require downstream re-review

**Rule:** If PR A merges before PR B, and both reference the same capability or affect the same artifacts, PR B requires re-review after PR A merges.

**Process:**
1. PR B author rebases or merges latest main branch (incorporating PR A changes)
2. PR B author notifies original reviewer: "Rebased after PR #[A]; conflicts resolved; ready for re-review"
3. Reviewer confirms:
   - PR B still aligns with approved capability plan
   - No conflicts introduced with merged PR A
   - Changes remain within approved scope
4. If conflicts detected, surface and resolve per Section 6

**Automated enforcement:**
- GitHub's "Require branches to be up to date before merging" setting helps enforce this
- Planned: Automated checks to detect concurrent changes (Section 10.4)

#### Conflicting approved changes

**Prevention:** When reviewing PR B, reviewer should check for conflicts with recently-merged or in-flight PRs affecting the same artifacts.

**Resolution if conflict detected after both approved:**
- First-merged PR takes precedence (its approval remains valid)
- Second PR's approval is considered stale/invalid
- Author of second PR must:
  1. Resolve conflict with first PR
  2. Seek re-approval (same process as initial approval)
  3. Document resolution in PR comments

#### Merge sequence coordination

**Best practice:** When multiple PRs affect the same artifacts and have interdependencies:
- Coordinate merge sequence with other PR authors
- Consider merging in the same sequence approvals were given
- Document dependencies in PR descriptions

**When sequence matters:** PRs modifying the same job manifest, artifact contracts, or cross-job interfaces should be merged sequentially with explicit coordination.

**Enforcement:** Manual coordination currently; automated dependency detection planned (Section 10.4).

---

## 7. Approval for Different Contribution Types

This section provides practical guidance for common contribution scenarios.

### 7.1 Documentation-only changes

#### Clarifications/wording improvements (no meaning change)

**Approval process:**
- **Option 1: Standard approval** — PR review and approval
- **Option 2: Lightweight approval** — If change meets lightweight criteria (ref: Section 10.2), single approver with 24-hour target review window

**Lightweight approval qualification:**
- Documentation-only change (no code/manifest changes)
- No meaning change (wording/readability improvement only)
- No cross-references broken or changed
- Traceable in PR description

**Approval requirements:**
- Reviewer confirms "no meaning change"
- PR approval via GitHub mechanism (evidence maintained)

**Decision record required:** No

**Validation requirements:**
- No specialized validation needed
- Spot-check cross-references still valid
- Run Doc Impact Scan if terminology changes

**Review focus:**
- Improved clarity
- No contradictions introduced
- Cross-references remain valid

#### Meaning changes (intent/rules/responsibilities)

**Approval process:**
- Full review against relevant standards
- Determine if governance-level (requires decision record) or local clarification
- If governance-level: decision record required per Section 5
- If local: standard PR approval with explicit "meaning change approved" comment

**Decision record required:** Yes, if governance-level (changes to principles, standards, agent roles, approval rules)

**Validation requirements:**
- Doc Impact Scan to check for double truth
- Verify affected documents remain consistent
- Check glossary for term definition conflicts

**Review focus:**
- Alignment with approved principles
- No unintended side effects on other documents
- Explicit approval of meaning change

### 7.2 Code/implementation changes

#### Within approved scope

**Approval process:**
- Standard PR review process
- Reviewer confirms alignment with approved tasks
- PR approval via GitHub approval mechanism

**Decision record required:** No

**Validation requirements:**
- Tests pass (when test infrastructure exists)
- Changes traceable to approved tasks
- No scope expansion detected

**Review focus:**
- Code quality and standards conformance
- Alignment with capability plan and tasks
- No security vulnerabilities introduced

#### Scope expansion (beyond approved tasks)

**Approval process:**
- STOP: escalate before proceeding
- Revise relevant planning step (Step 3 typically)
- Obtain new approval for expanded scope
- THEN proceed with implementation

**Decision record required:** Yes, if scope change affects approved objective or introduces breaking changes

**Validation requirements:**
- Re-validation of updated capability plan
- Approval of scope change
- Updated traceability

**Review focus:**
- Justify scope expansion
- Impact on other capabilities or jobs
- Risk assessment for expanded scope

### 7.3 Breaking changes

**Definition (from naming_standard.md Section 5 and artifacts_catalog_spec.md Section 6.5):**
- Changes that require migration, deprecation period, or coordination
- Affect stable contracts or automation
- Examples: renaming identifiers, changing artifact contracts, modifying manifest schemas

**Approval process:**
1. Create decision record documenting the breaking change (ref: Section 5.1)
2. Decision record MUST include:
   - Rationale for breaking change
   - Migration plan
   - Deprecation timeline (if applicable)
   - Impact assessment (affected jobs, consumers)
3. Approve decision record (ref: Section 5.4)
4. Implement breaking change referencing approved decision record
5. Execute migration plan
6. Validate migration complete

**Decision record required:** Yes (MUST)

**Validation requirements:**
- Migration evidence (consumers updated, references migrated)
- Backward compatibility tested during transition
- Deprecation warnings validated

**Review focus:**
- Breaking change justified
- Migration plan complete and realistic
- Impact on downstream consumers acceptable
- Deprecation timeline reasonable

**Cross-reference:**
- Naming standard (`naming_standard.md` Section 5) for identifier breaking changes
- Artifacts catalog spec (`artifacts_catalog_spec.md` Section 6.5) for artifact contract breaking changes
- Decision records standard for breaking change approval process

### 7.4 Conflict resolutions

**Approval process:**
1. Surface conflict explicitly (ref: Section 6.2)
2. Classify conflict type (intent/rules/runtime/evidence/decision)
3. Propose resolution options
4. Human decision-maker selects resolution
5. If governance-level: create decision record documenting resolution
6. If implementation-level: document in PR comment or issue
7. Apply resolution changes
8. Re-validate conflict resolved
9. Resume approval process

**Decision record required:** Yes, if governance-level conflict (rules/principles change)

**Validation requirements:**
- Conflict actually resolved (not just papered over)
- No new conflicts introduced
- Resolution aligns with selected option

**Review focus:**
- Conflict correctly classified
- Resolution options thorough
- Decision documented and traceable
- Downstream impacts considered

**Cross-reference:**
- Workflow guide Section 7 for detailed conflict resolution procedures
- Decision records standard Section 2.1.3 for conflict resolution decision records

---

## 8. Integration with Existing Governance and Standards

This section clarifies how this guide relates to other governance artifacts.

### 8.1 Relationship to target agent system

**Target agent system defines:**
- Non-negotiable operating rules (human approval gates, evidence discipline, no hidden authority)
- Agents vs tools separation
- Conflict handling principles
- Single source of truth principle

**This guide implements:**
- Approval gates defined in target agent system as concrete approval requirements per workflow step
- Evidence discipline from target agent system as specific evidence documentation requirements
- Conflict handling principles as conflict entry points and resolution approval procedures

**Alignment:**
- Agent escalation triggers in agent role charter → escalation triggers in approval gates (Section 2)
- Evidence discipline rules → evidence expectations (Section 3)
- Approval gate principles → approval requirements per step (Section 2)

### 8.2 Relationship to workflow guide

**Workflow guide defines:**
- Step execution procedures (what to do in each step)
- Exit criteria (what must be true before advancing)
- Conflict handling procedures (step-by-step resolution)

**This guide defines:**
- Approval requirements per step (what must be approved to advance)
- How exit criteria are approved (evidence and process)
- Conflict approval requirements (when resolution needs approval)

**Division of responsibility:**
- Workflow guide: HOW to execute steps
- This guide: HOW to approve step outputs and progression

**Mutual support:**
- Workflow guide exit criteria → this guide approval criteria
- Workflow guide escalation triggers → this guide escalation-triggered approval requirements
- Workflow guide conflict handling → this guide conflict resolution approval

### 8.3 Relationship to validation standard

**Note:** Validation standard (`validation_standard.md`) is not yet finalized. This section describes the intended relationship based on the documentation system catalog.

**Validation standard will define:**
- What evidence is valid for different artifact types
- Validation rules and pass/fail semantics
- What "verified" means technically

**This guide defines:**
- How evidence supports approvals
- What approval evidence forms are acceptable
- When validation evidence is required for approval

**Integration:**
- Validation tools produce evidence → approvals consume and evaluate evidence
- Validation standard defines evidence quality → this guide defines evidence documentation
- Validation pass/fail → this guide defines approval based on validation results

### 8.4 Relationship to documentation system catalog

**Documentation system catalog defines:**
- Document types and their purposes
- Canonical placement rules
- Content boundaries per document type
- Single source of truth enforcement

**This guide ensures approvals respect:**
- Document type boundaries (no double truth through approval process)
- Canonical placement (documentation changes approved in correct locations)
- Content separation (no standards embedded in process docs through approval)

**Alignment:**
- Catalog enforces single source of truth → this guide ensures approvals don't introduce double truth
- Catalog defines document boundaries → this guide review expectations check boundary respect
- Catalog defines canonical homes → this guide documentation approvals verify correct placement

### 8.5 Relationship to agent role charter

**Agent role charter defines:**
- Agent responsibilities and non-responsibilities
- Agent escalation triggers
- Agent-specific review expectations

**This guide uses:**
- Agent responsibilities → review expectations per workflow step (Section 4.1)
- Agent escalation triggers → approval gate escalation triggers (Section 2)
- Agent boundaries → reviewer responsibilities (Section 4.2)

**Integration:**
- Agent escalation = approval process pause → human decision required
- Agent review outputs → input to approval decisions
- Agent evidence summaries → approval evidence documentation

---

## 9. Practical Examples (Non-Normative)

The following examples illustrate the approval flow for common scenarios. These are non-normative and intended for guidance only.

### 9.1 Example: Step 3 → Step 4 Approval (Capability to Implementation)

**Scenario:** Implementing a capability for "Generate vendor product matching proposals"

**Step 3 (Capability Planning):**
1. Author drafts capability plan with:
   - Capability boundary: "Generate proposals; does NOT execute matching"
   - Acceptance criteria: "Produces proposals.json with valid schema"
   - Codable tasks: Task 3.1 (load vendor data), Task 3.2 (apply matching rules), Task 3.3 (write proposals)
2. Reviewer checks:
   - Boundary is clear
   - Acceptance criteria are evaluable
   - Tasks are bounded
3. Human approves via issue comment: "Capability plan approved, proceed to implementation"
4. **Approval evidence:** Issue #123 comment with approval timestamp and approver username

**Step 4 (Execute Development Tasks):**
1. Author implements Tasks 3.1-3.3 in PR #124
2. PR description references: "Implements capability from Issue #123, tasks 3.1-3.3"
3. Reviewer checks:
   - Code aligns with approved tasks
   - No scope expansion beyond capability boundary
   - Code quality acceptable
4. Reviewer approves PR via GitHub approval mechanism
5. PR merged
6. **Approval evidence:** PR #124 approval + merge commit SHA

**Traceability:** Merge commit message → PR #124 → Issue #123 → approved capability plan

---

### 9.2 Example: Breaking Change Approval (Artifact Renaming)

**Scenario:** Renaming artifact from `vendor_products.json` to `raw_vendor_products.json` to clarify semantics

**Step 1: Recognize breaking change**
- Author identifies this as a breaking change (affects cross-job references)
- Per Section 5.1 and `decision_records_standard.md`, decision record required

**Step 2: Draft decision record**
- Author creates `DR-0055-rename-vendor-products-artifact.md`
- Context: explains current ambiguity and why rename is needed
- Decision: "Rename `vendor_products.json` to `raw_vendor_products.json`; maintain dual-write for 60 days"
- Rationale: improves semantic clarity, aligns with artifact naming patterns
- Consequences: 3 consuming jobs must update; migration plan provided
- Status: Proposed

**Step 3: Review decision record**
- Reviewers check:
  - Migration plan is complete
  - Impact assessment covers all consumers
  - Deprecation timeline is reasonable
- Feedback integrated iteratively

**Step 4: Approve decision record**
- Human approves via PR comment: "DR-0055 approved"
- Decision record Status updated: Status: Approved, Date: 2026-02-02, Approved by: [Name]
- Decision record merged into repository

**Step 5: Implement breaking change**
- Author creates PR #125: "Implement DR-0055: Rename vendor_products artifact"
- PR implements:
  - Producer job writes both old and new filenames (dual-write)
  - Artifact catalog updated
  - Job manifest updated
- Reviewer confirms alignment with DR-0055
- PR approved and merged

**Step 6: Execute migration**
- Consumer jobs updated (3 PRs)
- After 60 days, dual-write removed

**Approval evidence:**
- DR-0055 (approved decision record)
- PR #125 approval (implementation)
- Consumer update PRs (migration completion)

---

### 9.3 Example: Conflict Resolution Approval (Runtime vs Intent)

**Scenario:** Job manifest declares output as required, but script makes it optional (runtime conflict)

**Step 1: Conflict detected**
- Reviewer notices: manifest says `required: true`, script has `if config.write_output:`
- Conflict surfaced: "Runtime conflict: manifest vs script disagree on output requirement"

**Step 2: Classify and document**
- Conflict type: Runtime conflict
- Documentation: PR comment describing the discrepancy
- Evidence: Manifest line 42, script lines 156-158

**Step 3: Propose resolution options**
- Option A: Update script to always write output (align runtime to intent)
- Option B: Update manifest to `required: false` (align intent to runtime, with rationale)
- Option C: Add configuration parameter to control behavior (expand capability)

**Step 4: Human decision**
- Human selects Option B: "Output should be optional; original intent was incorrect"
- Decision is implementation-level (no governance change)
- No decision record needed (local fix)

**Step 5: Document and apply resolution**
- PR comment: "Conflict resolved via Option B: manifest updated to `required: false`"
- Author updates manifest in same PR
- Reviewer re-reviews updated manifest

**Step 6: Re-validate and approve**
- Reviewer confirms conflict resolved
- PR approved and merged

**Approval evidence:**
- PR comment documenting conflict and resolution
- PR approval after conflict resolution

---

## 10. Open Items / TBD

This section lists items that require human decision or clarification from other documentation.

### 10.1 Validation standard integration (RESOLVED)

**Status:** Validation standard is not yet finalized

**Decision:** Option A selected — Leave as TBD until validation standard is finalized, then update this guide to integrate concrete validation requirements

**Rationale:**
- Minimal impact on approval process usability in current state
- Avoids creating temporary validation requirements that would need to be replaced
- Maintains clean separation: validation standard defines evidence validity; this guide defines approval process

**Impact:**
- Section 3.4 (evidence discipline) references validation standard but cannot provide concrete integration details until standard is finalized
- Section 8.3 (relationship to validation standard) describes intended relationship based on catalog description
- When validation standard is finalized: update Sections 3.4 and 8.3 with concrete integration details

**Action required:** Update this guide when validation standard is approved (tracked as future work)

---

### 10.2 Lightweight approval for low-risk changes (RESOLVED)

**Decision:** Option B selected — Define lightweight approval criteria and accelerated process

**Rationale:**
- Reduces overhead for low-risk changes while maintaining governance discipline
- Accelerates common contribution types (documentation clarifications, test improvements, internal refactoring)
- Maintains traceability and approval evidence even for lightweight process

**Lightweight approval criteria:**

Changes qualify for lightweight approval when ALL of the following are true:

1. **Low risk:** Change does not affect:
   - Cross-job contracts or automation
   - Stable identifiers (job_id, artifact_id, parameter names)
   - Governance rules or principles
   - Approval gate requirements or evidence expectations

2. **Narrow scope:** Change is limited to:
   - Single job internal implementation (no manifest changes)
   - Documentation clarifications without meaning changes
   - Test additions/improvements without changing production code
   - Formatting/style improvements

3. **No breaking changes:** Change requires no migration, deprecation, or consumer coordination

4. **Traceable:** Change is still documented in PR with clear description and references

**Lightweight approval process:**

1. **Single approver:** Requires one human approval (vs. potentially multiple for standard process)
2. **Shorter review window:** Target 24-hour review turnaround (vs. open-ended for standard process)
3. **Focused review:** Reviewer confirms lightweight criteria met and spot-checks quality
4. **Same evidence requirements:** PR approval still required; traceability maintained

**Examples qualifying for lightweight approval:**
- Documentation wording improvements (no meaning change)
- Internal job function refactoring (no manifest/contract changes)
- Test coverage additions (no production code changes)
- Code style/formatting fixes (no behavior changes)
- Comment improvements or addition

**Examples NOT qualifying (require standard approval):**
- Manifest changes (even minor)
- Cross-job interface changes
- Breaking changes (any scale)
- Documentation meaning changes
- Scope expansion during implementation

**Implementation note:** Lightweight approval is a process optimization, not a governance relaxation. All approval evidence requirements remain in effect.

**Action required:** Update Section 7.1 (documentation-only changes) to reference lightweight approval option (completed below)

---

### 10.3 Approval authority matrix (RESOLVED)

**Decision:** Option A selected — Keep approval authority implicit; rely on team processes and PR ownership

**Rationale:**
- Approval authority is contextually clear for current team size
- Explicit matrix would add overhead without providing value at current scale
- Team processes and PR ownership patterns naturally establish approver context
- Flexibility preserved for evolving team structure

**Current approach:**
- "Human decision-maker" remains the documented approver in this guide
- Actual approver identity determined by:
  - PR ownership and assignment
  - Team processes (e.g., code owners, area expertise)
  - Change type context (governance changes naturally escalate to maintainers)
  - GitHub's built-in approval mechanisms and notifications

**Impact:** No changes to approval process; authority remains implicit and contextually determined

**Future consideration:** If team grows significantly or approval bottlenecks emerge, revisit explicit authority matrix via decision record

---

### 10.4 Automated approval gate checks (RESOLVED - Future Work)

**Decision:** Option B selected — Implement automated checks as CI/GitHub Actions (future enhancement)

**Rationale:**
- Automation reduces human error and ensures consistent enforcement
- Scales better as repository and team grow
- Provides fast feedback to contributors (fail fast principle)
- Complements human review rather than replacing it

**Implementation approach (future work):**

**Phase 1: Basic traceability checks**
- PR description must reference approved capability/task for Step 4 implementations
- Breaking change PRs must reference decision record ID
- Warn if PR lacks traceability references

**Phase 2: Approval evidence validation**
- Check that capability plan approval exists before Step 4 PR merge
- Validate decision record status is "Approved" when referenced
- Check for approval evidence (PR approval, sign-off comment) before merge

**Phase 3: Content validation**
- Detect potential breaking changes (manifest schema changes, identifier renames)
- Flag missing decision records for governance-level changes
- Validate documentation changes respect layer boundaries

**Implementation tools:**
- GitHub Actions workflows (`.github/workflows/approval-checks.yml`)
- Custom scripts in `tools/approval-checks/` (if needed)
- GitHub API for approval and reference validation

**Current state:** Approval gates are manually enforced through review process (sufficient for current scale)

**Action required:** Create GitHub issue to track automated approval gate implementation (future work, not blocking for this guide)

---

## 11. Consistency Check Appendix

### 11.1 Documents aligned with

This guide was drafted with explicit alignment to the following repository documents:

**Context layer:**
- `docs/context/development_approach.md` — 5-step workflow, principles, human-agent collaboration
- `docs/context/target_agent_system.md` — Approval gates, evidence discipline, conflict handling, single source of truth
- `docs/context/documentation_system_catalog.md` — Document types, boundaries, canonical placement
- `docs/context/glossary.md` — Canonical term definitions (cross-referenced throughout)

**Process layer:**
- `docs/process/workflow_guide.md` — Step procedures, exit criteria, conflict handling procedures, escalation triggers

**Standards layer:**
- `docs/standards/decision_records_standard.md` — When/how decisions are recorded, decision record structure
- `docs/standards/naming_standard.md` — Breaking change definitions
- `docs/standards/codable_task_spec.md` — Task structure referenced in Step 3 approval requirements
- `docs/standards/job_manifest_spec.md` — Referenced in breaking change examples
- `docs/standards/artifacts_catalog_spec.md` — Breaking change definitions for artifacts

**Agent documentation layer:**
- `docs/agents/agent_role_charter.md` — Agent responsibilities, escalation triggers, review expectations

**Note:** `docs/standards/validation_standard.md` is not yet finalized and was not used as an info source per problem statement instructions.

### 11.2 Potential conflicts detected

**None detected.** The following areas were checked:

- **Approval gate requirements:** Aligned with target agent system non-negotiables and workflow guide exit criteria
- **Evidence discipline:** Consistent with target agent system rules and agent role charter evidence expectations
- **Decision recording:** Integrated with decision records standard without duplication
- **Conflict handling:** References workflow guide procedures without duplication
- **Document boundaries:** Respects documentation system catalog placement rules

### 11.3 Open items resolved

Section 10 open items were resolved with the following decisions:

**10.1 Validation standard integration:**
- **Decision:** Option A (wait for validation standard)
- **Status:** Resolved as future work; guide will be updated when validation standard is finalized
- **Impact:** No immediate changes needed; Sections 3.4 and 8.3 describe intended integration

**10.2 Lightweight approval for low-risk changes:**
- **Decision:** Option B (define lightweight approval criteria)
- **Status:** Resolved; lightweight approval criteria and process added to Section 10.2
- **Impact:** Section 7.1 updated to reference lightweight approval option for documentation clarifications

**10.3 Approval authority matrix:**
- **Decision:** Option A (keep approval authority implicit)
- **Status:** Resolved; no changes to approval process
- **Impact:** "Human decision-maker" remains the documented approver; authority determined by team processes and PR ownership

**10.4 Automated approval gate checks:**
- **Decision:** Option B (implement automated checks as future enhancement)
- **Status:** Resolved as future work; implementation approach documented in Section 10.4
- **Impact:** Manual approval enforcement continues; automation tracked as future enhancement

### 11.4 Assumptions introduced

This section documents assumptions and design choices made in this guide, including those introduced during the 2026-02-02 revision to address identified gaps.

1. **Material change definition (Section 2.0):** This guide defines "material change" objectively to make re-approval triggers enforceable. The definition balances specificity with flexibility by providing concrete examples while allowing "when in doubt" rule.

2. **Self-approval prohibition (Section 2.6):** This guide explicitly prohibits self-approval to maintain governance integrity. The independence definition provides clear criteria while avoiding over-specification of approval authority.

3. **Approval authority model (Section 2.6):** This guide keeps approval authority partially implicit (ref: Section 10.3 rationale) while adding guardrails: independence requirements, unavailability escalation, and authority conflict resolution. This balances flexibility with governance discipline.

4. **Merge commit classification (Section 3.1A):** This guide classifies merge commits as "execution confirmation" rather than "approval evidence" to eliminate circular logic. This distinction clarifies that approval must precede merge.

5. **Approval revocation process (Section 3.5):** This guide establishes revocation process including auto-revocation conditions. Assumes human judgment required for revocation decisions (not automated) except for clearly defined auto-revocation triggers.

6. **Concurrent approval coordination (Section 6.5):** This guide establishes coordination rules for concurrent PRs. Assumes manual coordination is sufficient initially; automated detection is future enhancement (Section 10.4).

7. **Conflict detection checklist (Section 6.2):** This guide provides systematic checklist for conflict detection. Assumes reviewers will use checklist proactively rather than relying on automated conflict detection.

8. **Bug fix exemption clarification (Section 1.2):** This guide distinguishes "restoring approved behavior" vs "updating approved intent" to eliminate contradiction. Assumes contributors can make this distinction with "when in doubt" guidance.

9. **Lightweight approval criteria (Section 10.2):** This guide defines specific lightweight approval criteria for low-risk changes. These criteria balance speed with governance discipline and maintain full traceability.

10. **Validation standard integration (Section 10.1):** This guide describes intended relationship with validation standard based on documentation system catalog description. When validation standard is finalized, Sections 3.4 and 8.3 will be updated with concrete integration.

11. **Evidence retention assumption:** This guide assumes GitHub's standard retention policies for PR/issue records without specifying explicit retention requirements beyond "permanent via GitHub."

12. **Review best practices (Section 4.4):** This guide incorporates industry-standard PR review practices and aligns them with repository-specific governance.

13. **Automated approval checks (Section 10.4):** Detailed implementation approach for future automated checks is documented but not yet implemented. Manual enforcement continues until automation is developed.

### 11.4 Cross-document integration notes

**Strong integration points:**
- Target agent system → This guide (approval gates, evidence discipline)
- Workflow guide → This guide (exit criteria = approval criteria, conflict procedures)
- Decision records standard → This guide (when decisions required, how they serve as approval evidence)
- Agent role charter → This guide (escalation triggers, review responsibilities)

**Boundary respect:**
- This guide does NOT duplicate workflow step procedures (those remain in workflow guide)
- This guide does NOT duplicate decision record structure (that remains in decision records standard)
- This guide does NOT define agent roles (those remain in agent role charter)
- This guide does NOT embed schemas or templates (those remain in standards)

**Cross-reference discipline:**
- All glossary terms cross-referenced (not redefined)
- All external procedures referenced (not duplicated)
- All integration points explicitly noted with document citations

### 11.5 Maintenance notes

**When to update this guide:**
- Workflow guide exit criteria change → update approval criteria accordingly
- Target agent system approval rules change → update approval gate requirements
- Decision records standard structure changes → verify references remain correct (should not require changes due to cross-reference approach)
- Validation standard finalized → update Section 3.4 and 8.3 with concrete integration
- New document types added to catalog → verify no approval process impact

**Stability expectations:**
- Core approval gate requirements (Section 2) are stable and tied to 5-step workflow
- Evidence forms (Section 3.1) are stable and based on GitHub mechanisms
- Review expectations (Section 4) are stable and based on agent responsibilities
- Decision recording integration (Section 5) is stable and cross-references decision records standard

**Version coordination:**
- This guide version should align with target agent system and workflow guide
- Breaking changes to approval process require decision record per this guide's own rules

---

## Summary

The Contribution and Approval Guide defines how work is proposed, reviewed, approved, and recorded in the vendor-to-pim-mapping-system repository. It operationalizes the approval gate and evidence discipline principles from the target agent system by providing concrete approval requirements for each workflow step, clear evidence documentation expectations, and integrated conflict handling procedures.

Key takeaways:
- **Approval gates at every step:** Steps 1-5 each have explicit approval requirements, criteria, and evidence expectations
- **Multiple evidence forms:** PR approvals, explicit sign-offs, issue closures, merge commits, and decision records all serve as valid approval evidence
- **Review is integral:** Review expectations aligned with agent responsibilities and workflow exit criteria
- **Conflicts must be surfaced:** Explicit conflict handling prevents silent resolution and maintains governance discipline
- **Decision records for governance:** Breaking changes, principle changes, and conflict resolutions require decision records
- **Practical and enforceable:** Approval process uses existing GitHub mechanisms and aligns with industry best practices

This guide supports the repository's governance model while remaining practical, actionable, and integrated with the broader documentation system.

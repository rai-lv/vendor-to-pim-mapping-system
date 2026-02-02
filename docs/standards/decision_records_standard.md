# Decision Records Standard

## Purpose

This standard defines when and how explicit governance decisions are recorded, which is required for conflict resolution and contract evolution without silent changes.

It enables:
- **Transparent governance** by documenting significant decisions with rationale and alternatives considered
- **Conflict resolution** by providing an auditable trail of decisions that resolved conflicts between intent, rules, runtime, or evidence
- **Contract evolution** by documenting breaking changes, scope changes, and principle exceptions with explicit approval
- **Traceability** by linking decisions to human approvals and supporting evidence
- **Prevention of silent drift** by requiring explicit decision records for changes that affect system contracts or principles

This standard addresses **when decisions must be recorded**, **what structure decision records must follow**, **what approval and evidence requirements apply**, and **how decisions are stored and indexed**.

**What this standard does NOT cover:**
- General workflow instructions (belongs in `docs/process/workflow_guide.md`)
- How to file or propose decisions (belongs in process layer when finalized)
- Tool command syntax or operational procedures (belongs in `docs/ops/`)
- Content of specific decisions (those live in individual decision records)

---

## 1) Foundational Principles

Decision records in this repository are governed by the following non-negotiable principles from the target agent system:

### 1.1 Human Approval Gates
Decision records document human decisions. Agents may draft decision records, but only humans approve decisions that affect system contracts, principles, or governance rules (ref: `target_agent_system.md`).

### 1.2 Evidence-Based Claims
Decision records must reference explicit evidence where applicable. Claims about validation, compliance, or implementation status must be backed by referenced evidence or marked as unverified (ref: `documentation_spec.md` Section 1.3, `target_agent_system.md`).

### 1.3 Explicit Over Implicit
Unknowns, assumptions, and trade-offs must be stated explicitly. Decision records exist to make governance choices visible and auditable, not to hide them (ref: `documentation_spec.md` Section 1.4).

### 1.4 Single Source of Truth
Each decision is recorded once in its decision record. Other documents may reference the decision but MUST NOT redefine its rationale or approval status (ref: `documentation_spec.md` Section 1.1).

### 1.5 Conflict Handling Discipline
When conflicts exist (approved intent vs. implemented reality, standards vs. artifacts, etc.), they must be surfaced explicitly and resolved via documented decision, not silently overridden (ref: `target_agent_system.md`, `workflow_guide.md` Section 7).

---

## 2) When Decision Records are Required

### 2.1 Required Triggering Conditions (MUST)

A decision record MUST be created when any of the following conditions are met:

**Note:** For breaking changes and governance-level changes, creating and approving a decision record per this standard IS the governance approval process. References in other standards to "governance approval" or "explicit approval" mean creating an approved decision record as defined here.

**Exception for standard adoption:** The initial adoption of this standard itself (and any pre-existing governance documents) is approved via the standard PR approval process. Once this standard is approved and merged, subsequent governance changes follow the decision record process defined here.

#### 2.1.1 Breaking Changes to Stable Contracts
**Trigger:** Any change that breaks existing automation, cross-job references, or established contracts.

**Examples:**
- Renaming a `job_id`, `artifact_id`, or other stable identifier (ref: `naming_standard.md` Section 5)
- Changing artifact filename patterns, bucket locations, or format contracts (ref: `artifacts_catalog_spec.md` Section 6.5)
- Modifying job manifest schema or required fields (ref: `job_manifest_spec.md`)
- Changing parameter names, types, or semantics in a deployed job

**Why required:** Breaking changes affect downstream consumers and require coordination, migration plans, and explicit approval.

#### 2.1.2 Changes to Foundational Principles or Governance Rules
**Trigger:** Any modification to principles, operating rules, or workflow intent defined in context documents.

**Examples:**
- Changing approval gate requirements or evidence expectations (ref: `target_agent_system.md`)
- Modifying the 5-step workflow structure or entry/exit criteria (ref: `development_approach.md`, `workflow_guide.md`)
- Altering separation of concerns or single-source-of-truth principles (ref: `documentation_spec.md`)
- Changing agent role responsibilities or escalation triggers (ref: `agent_role_charter.md`)

**Why required:** Principles govern all downstream work; changing them affects how the system operates and requires explicit approval with rationale.

#### 2.1.3 Resolution of Conflicts Between Approved Intent and Implemented Reality
**Trigger:** When a conflict is detected and must be resolved via an explicit decision (ref: `workflow_guide.md` Section 7).

**Conflict types:**
- **Intent conflict:** Approved artifacts disagree with each other
- **Rules conflict:** Standards or governance rules conflict with an artifact
- **Runtime conflict:** Implementation behavior conflicts with approved intent
- **Evidence conflict:** Evidence contradicts claims or expected outcomes
- **Decision conflict:** Two or more approved decision records contain contradictory requirements

**Examples:**
- Job manifest declares an output as required, but script makes it optional (intent vs. runtime conflict)
- Standard requires snake_case, but deployed job uses camelCase (rules vs. runtime conflict)
- Documentation claims a feature is "verified", but no evidence exists (evidence conflict)
- DR-0001 requires snake_case universally, but DR-0025 allows camelCase for legacy jobs (decision conflict)

**Why required:** Conflicts must not be silently resolved. The decision record documents which source of truth was chosen and why.

**Resolving decision-to-decision conflicts:**
When two approved decision records contradict each other:
1. Create a new decision record that explicitly addresses the conflict
2. The new decision MUST supersede one or both conflicting decisions, or clarify precedence rules
3. Update the superseded decisions' status and cross-references (per Section 3.1.9)
4. Update decision_log.md to reflect the resolution

Example resolution: "DR-0050 supersedes DR-0025 (exception removal) while DR-0001 (snake_case requirement) remains active and now applies universally."

#### 2.1.4 Introduction or Removal of Document Types or Canonical Placements
**Trigger:** Changes to the documentation system catalog structure (ref: `documentation_system_catalog.md`).

**Examples:**
- Adding a new document type to the catalog with its own purpose and boundaries
- Moving a document type's canonical location (e.g., from `docs/process/` to `docs/standards/`)
- Removing a document type that is no longer needed
- Redefining what content belongs in which document type

**Why required:** Documentation structure changes affect where contributors place content and how documents reference each other. These are governance-level decisions.

#### 2.1.5 Changes to Approval Gates or Evidence Expectations
**Trigger:** Modifications to what constitutes valid approval or acceptable evidence.

**Examples:**
- Changing what forms of approval are acceptable (e.g., requiring PR approval vs. issue sign-off)
- Modifying validation requirements or pass/fail criteria (ref: `validation_standard.md` when finalized)
- Altering evidence detail requirements for specific decision types
- Introducing new approval gates or removing existing ones

**Why required:** Approval and evidence discipline are core to the governance model. Changes must be explicit and auditable.

#### 2.1.6 Explicit Scope Changes During Execution
**Trigger:** When approved scope (objective, pipeline, or capability) must change during execution.

**Examples:**
- Objective scope expands beyond original boundaries (requires re-approval of Step 1)
- Capability definition adds new acceptance criteria not in original approval
- Implementation requires additional assumptions not in the approved capability plan

**Why required:** Scope changes affect what was approved. The decision record documents the scope change, rationale, and re-approval.

#### 2.1.7 Exceptions to Standards or Principles
**Trigger:** When a specific case requires an exception to an established standard or principle.

**Examples:**
- Job requires non-standard naming due to external system constraints (ref: `naming_standard.md` exceptions policy)
- Document requires exception to standard metadata format (ref: `documentation_spec.md` Section 7.4)
- Validation cannot be performed due to infrastructure limitations

**Why required:** Exceptions must be documented with rationale and approval to prevent "exception creep" and maintain governance discipline.

#### 2.1.8 Significant Architecture or Design Decisions
**Trigger:** Decisions that affect multiple jobs, system-wide behavior, or future development direction.

**Examples:**
- Choosing between alternative implementation approaches for shared functionality
- Deciding on technology stack or tool choices that affect multiple components
- Establishing conventions for common patterns (e.g., error handling, logging format)
- Defining cross-job integration patterns or data flow conventions

**Why required:** Architecture decisions have lasting impact and should be documented with alternatives considered and rationale.

### 2.2 Not Required (Routine Work)

Decision records are NOT required for:
- **Routine implementation** of approved tasks within bounded scope
- **Clarifications** that don't change meaning (wording improvements, readability fixes)
- **Bug fixes** that restore intended behavior without changing contracts
- **Documentation updates** that reflect existing reality without introducing new rules
- **Internal job changes** that don't affect cross-job contracts or automation
- **Temporary or intermediate artifacts** within a job that aren't consumed by other jobs

**Boundary test:** Ask "Does this change affect stable contracts, governance rules, or require re-approval of previously approved scope?" If no, a decision record is not required.

---

## 3) Decision Record Structure

### 3.1 Required Sections (MUST)

Every decision record MUST contain the following sections in this order:

#### 3.1.1 Decision ID and Title

**Format:**
```markdown
# DR-NNNN: [Short descriptive title]
```

**Rules:**
- **Decision ID:** Format `DR-NNNN` where `NNNN` is a zero-padded 4-digit number (e.g., `DR-0001`, `DR-0042`)
- **Title:** Short, descriptive title (under 80 characters) that summarizes the decision
- **Uniqueness:** Decision IDs MUST be unique and sequential
- **Stability:** Once assigned, a Decision ID MUST NOT be reused even if the decision is superseded

**Example:**
```markdown
# DR-0001: Adopt snake_case for job identifiers
```

#### 3.1.2 Status

**Format:**
```markdown
## Status

**Current Status:** [STATUS_VALUE]
**Date:** [YYYY-MM-DD]
**Approved by:** [Name/Role or reference to approval evidence]
```

**Rules:**
- **Status value:** MUST be one of the values defined in Section 4 (Status Lifecycle)
- **Date:** Date of most recent status change (ISO 8601 format: YYYY-MM-DD)
- **Approved by:** Human approver identity or reference to approval evidence (PR number, issue comment, etc.)
- **Status changes:** When status changes, update all three fields and optionally add a status history subsection

#### 3.1.3 Context

**Format:**
```markdown
## Context

[2-5 paragraphs describing the situation that triggered this decision]
```

**Required content:**
- What situation or problem triggered the need for this decision
- What alternatives or options were being considered
- What constraints or requirements existed
- What evidence or information was available when the decision was made

**Rules:**
- MUST be written so that a reader unfamiliar with the specific situation can understand why the decision was needed
- SHOULD reference relevant documents, issues, PRs, or other artifacts that provide additional context
- MUST NOT embed the actual decision choice here (that belongs in Section 3.1.4)

#### 3.1.4 Decision

**Format:**
```markdown
## Decision

[Clear statement of what was decided]
```

**Required content:**
- The actual choice that was made (what will be done or not done)
- What changed as a result (if a reversal or modification of previous practice)
- What is now considered the authoritative rule or approach

**Rules:**
- MUST be stated clearly enough that someone can implement it without re-deriving the decision
- SHOULD use normative keywords (MUST/SHOULD/MAY) when defining rules
- MUST be unambiguous (no "we should probably" or "it might be good to")

**Example:**
```markdown
## Decision

All job identifiers MUST use snake_case format (lowercase with underscores). Existing jobs using camelCase MUST be migrated within 90 days using the deprecation process defined in `naming_standard.md` Section 5.
```

#### 3.1.5 Rationale

**Format:**
```markdown
## Rationale

[Explanation of why this decision was made]
```

**Required content:**
- Why this choice was made over alternatives
- What trade-offs were considered
- What principles or goals this decision supports
- What risks or downsides were accepted

**Rules:**
- MUST explain the reasoning, not just restate the decision
- SHOULD reference relevant principles from context documents (development approach, target agent system, etc.)
- SHOULD acknowledge trade-offs and explain why the chosen approach was deemed best

#### 3.1.6 Consequences

**Format:**
```markdown
## Consequences

[What changes as a result of this decision]
```

**Required content:**
- **Positive consequences:** What benefits or improvements result from this decision
- **Negative consequences:** What costs, limitations, or trade-offs result (be explicit)
- **Migration needs:** What existing artifacts or processes must change to comply
- **Affected components:** What jobs, documents, or processes are impacted

**Rules:**
- MUST include both positive and negative consequences (honest assessment)
- MUST identify migration needs if the decision affects existing artifacts
- SHOULD quantify impact where possible (e.g., "affects 12 existing jobs", "requires 3 document updates")

#### 3.1.7 Approval Reference

**Format:**
```markdown
## Approval Reference

**Approval method:** [How approval was obtained]
**Approval evidence:** [Link or reference to approval]
**Approved by:** [Name/Role]
**Approval date:** [YYYY-MM-DD]
```

**Required content:**
- How approval was obtained (PR approval, explicit sign-off in issue, meeting notes, etc.)
- Link to or description of approval evidence
- Who approved (human name/role)
- When approval was given

**Rules:**
- MUST provide enough detail that someone can verify the approval occurred
- SHOULD link directly to GitHub PR, issue comment, or other reviewable evidence
- MAY reference multiple approvals if decision required multiple sign-offs

**Example:**
```markdown
## Approval Reference

**Approval method:** PR approval
**Approval evidence:** PR #42 approved and merged by repository maintainer
**Approved by:** Jane Smith (Repository Maintainer)
**Approval date:** 2026-01-15
```

#### 3.1.8 Evidence Sources

**Format:**
```markdown
## Evidence Sources

[Links to or descriptions of evidence that informed this decision]
```

**Required content:**
- References to validation results, test outcomes, investigation findings that informed the decision
- Links to documents, PRs, issues, or other artifacts that provided evidence
- If no evidence was available, state "No direct evidence available" and explain why the decision was made without it

**Rules:**
- MUST provide references where evidence exists
- MUST explicitly state when decisions are made without evidence (e.g., based on principles, expert judgment, or analogous situations)
- SHOULD use specific references (PR numbers, file paths, validation report links) rather than vague descriptions

**Example:**
```markdown
## Evidence Sources

- Investigation of existing job IDs: 8 of 12 jobs use snake_case, 4 use camelCase (analysis: issue #123)
- Validation tool compatibility: snake_case simplifies regex matching (testing: PR #119)
- Industry best practices: Python/YAML ecosystems prefer snake_case (external reference: PEP 8)
```

#### 3.1.9 Supersedes / Superseded By

**Format:**
```markdown
## Supersedes / Superseded By

**Supersedes:** [List of decision IDs this decision replaces, or "None"]
**Superseded by:** [Decision ID that replaces this decision, or "None" if still active]
```

**Required content:**
- List of decision record IDs that this decision explicitly replaces (if any)
- Reference to the decision record that replaced this one (if superseded)
- "None" if no supersession relationship exists

**Rules:**
- MUST be present in every decision record (use "None" if not applicable)
- When a decision is superseded, the Status MUST change to "Superseded" and this section MUST reference the superseding decision
- When creating a decision that supersedes others, MUST update the superseded decisions' status and cross-references

**Handling partial supersession:**
- If a decision is **fully replaced** by a single newer decision: Use "Superseded" status with single "Superseded by" reference
- If a decision is **partially superseded** by multiple decisions (different aspects replaced separately): Keep status as "Approved" and list all superseding decisions in "Superseded by" field (comma-separated). Add a note in the Status section clarifying which aspects remain active and which are superseded.
- Example: "Superseded by: DR-0015 (length guidance only), DR-0020 (casing rules only); snake_case requirement remains active"
- **Rationale:** Partially superseded decisions remain normative for their non-superseded aspects, so "Approved" status is correct. Use "Deprecated" only when the entire decision is no longer recommended but still in effect during a transition period.

### 3.2 Optional Sections (MAY)

Decision records MAY include the following additional sections if helpful:

#### 3.2.1 Alternatives Considered
Detailed analysis of alternative approaches that were evaluated but not chosen. Useful for complex decisions where trade-off analysis is valuable.

#### 3.2.2 Related Decisions
References to other decision records that are related but not superseded/superseding. Useful for tracking decision dependencies or evolution of thinking in an area.

#### 3.2.3 Implementation Notes
Practical guidance for implementing the decision. Should NOT duplicate standards or process documentation; use this for decision-specific implementation guidance only.

#### 3.2.4 Review History
Log of when the decision was reviewed or revisited. Useful for long-lived decisions that are periodically re-evaluated.

### 3.3 Amendments and Corrections to Approved Decisions

After a decision record is approved, certain types of corrections and clarifications are permitted without creating a superseding decision:

#### 3.3.1 Permitted Direct Amendments (MAY)

The following changes MAY be made directly to an approved decision record without superseding it:

**Typographical corrections:**
- Fix spelling errors, grammar issues, or formatting problems
- Correct names, dates, or references that are factually incorrect
- MUST note the correction in the commit message
- Example: "Fix typo: 'Jame Smith' → 'Jane Smith'"

**Evidence additions:**
- Add missing references to evidence that existed at the time of approval
- Add clarifying links to supporting documentation
- MUST NOT change the decision or rationale; only supplement existing evidence

**Clarification notes:**
- Add clarifying text to the Context or Rationale sections if the original wording was ambiguous
- Add to optional Review History section (3.2.4) to note when clarification was added
- MUST NOT change the meaning of the decision

#### 3.3.2 Changes Requiring Supersession (MUST)

The following changes MUST be made via a superseding decision record:

**Substantive changes:**
- Changing the decision itself (what was decided)
- Modifying acceptance criteria, migration timelines, or affected components
- Reversing or materially altering the rationale
- Correcting factual errors that affect the decision's validity (e.g., "affects 4 jobs" → actually affects 12 jobs, requiring different approach)

**Status changes:**
- Marking a decision as Superseded or Deprecated (via superseding decision)
- Withdrawing or rejecting an approved decision (cannot be done; create superseding decision instead)

#### 3.3.3 Amendment Documentation

When making permitted direct amendments:
- Include clear commit message describing the amendment
- If the amendment is significant (beyond typo fixes), consider adding a note to the optional Review History section (3.2.4)
- Preserve git history so the amendment is auditable

**Example Review History entry for clarification:**
```markdown
## Review History

**2026-03-15:** Clarification added to Rationale section regarding exception handling. Original decision unchanged. (Commit: abc123)
```

---

## 4) Status Lifecycle

### 4.1 Allowed Status Values (MUST)

Decision records MUST use exactly one of the following status values:

#### 4.1.1 Proposed
**Definition:** Decision is drafted but not yet approved.

**When used:**
- Initial creation of decision record
- Decision is under review and discussion
- Evidence is being gathered to support the decision

**Transition rules:**
- Can transition to: **Approved**, **Rejected**, **Withdrawn**
- Requires: Draft decision record with all required sections present

#### 4.1.2 Approved
**Definition:** Decision has received human approval and is in effect.

**When used:**
- Human approver has explicitly approved the decision
- Decision is now the authoritative rule or approach
- Implementation may proceed based on this decision

**Transition rules:**
- Can transition to: **Superseded**, **Deprecated**
- Requires: Explicit approval evidence (PR approval, sign-off, etc.) documented in Approval Reference section

#### 4.1.3 Superseded
**Definition:** Decision has been replaced by a newer decision.

**When used:**
- A newer decision record explicitly replaces this decision
- The old approach is no longer valid or recommended
- Cross-reference to superseding decision exists

**Transition rules:**
- Can transition from: **Approved** (directly) or **Deprecated** (after deprecation period)
- Requires: Reference to superseding decision in "Superseded By" section
- The superseding decision MUST list this decision in its "Supersedes" section
- Note: Most decisions transition directly from Approved to Superseded. The Deprecated state is used when a transition period is needed.

#### 4.1.4 Rejected
**Definition:** Decision was proposed but explicitly rejected by human reviewer.

**When used:**
- Proposed decision was reviewed and determined not to be the right approach
- Documents that this approach was explicitly considered and rejected (prevents re-proposing)
- Rationale for rejection should be documented

**Transition rules:**
- Can only transition from: **Proposed**
- Requires: Explanation in Rationale section of why the decision was rejected
- Cannot transition to other states (rejected decisions are archived, not revived)

#### 4.1.5 Withdrawn
**Definition:** Proposed decision was withdrawn before approval/rejection (e.g., no longer relevant, replaced by different proposal).

**When used:**
- Proposer withdraws the decision before review completion
- Decision became irrelevant due to external changes
- Decision was replaced by a substantially different proposal

**Transition rules:**
- Can only transition from: **Proposed**
- Requires: Brief explanation of why withdrawn
- Cannot transition to other states (withdrawn decisions are archived)

#### 4.1.6 Deprecated
**Definition:** Approved decision is being phased out but not yet fully superseded.

**When used:**
- Decision is still technically in effect but no longer recommended
- Transition period exists before full supersession
- New work should not follow this decision; existing work may continue

**Transition rules:**
- Can only transition from: **Approved**
- Can transition to: **Superseded**
- Requires: Explanation of deprecation timeline and migration path

### 4.2 Status Transition Diagram

```
Proposed ──────┐
  │            │
  ├─→ Approved ├─→ Deprecated ──→ Superseded
  │            │
  ├─→ Rejected │
  │            │
  └─→ Withdrawn
```

### 4.3 Status Validation Rules (MUST)

- **Uniqueness:** A decision record MUST have exactly one status at any given time
- **Immutability of terminal states:** **Rejected** and **Withdrawn** are terminal states; decisions cannot transition from these states
- **Supersession requires reference:** A decision marked **Superseded** MUST reference the superseding decision ID
- **Approval requires evidence:** A decision cannot transition to **Approved** without documented approval evidence

---

## 5) Evidence and Approval Requirements

### 5.1 Approval Requirements (MUST)

#### 5.1.1 Who Can Approve
Decisions MUST be approved by humans with appropriate authority:

- **Breaking changes to contracts:** Repository maintainer or technical lead
- **Principle or workflow changes:** Repository owner or governance lead
- **Exception to standards:** Standard owner or repository maintainer
- **Architecture decisions:** Technical lead or team consensus

**Rule:** Decision records MUST identify the approver by name/role, not just "team" or "someone".

**Multiple approvers:**

Multiple approvals are RECOMMENDED when:
- Decision affects multiple teams or functional areas (cross-functional decision)
- Breaking change affects more than 3 jobs or components (high-impact change)
- Principle or workflow changes (governance-level decisions)
- High-risk architectural decisions with significant long-term implications

Multiple approvals are OPTIONAL but may be valuable for:
- Exception requests (standard owner + affected party)
- Controversial or debated decisions (broader consensus)
- Decisions with unclear ownership boundaries

When multiple approvals are obtained, the Approval Reference section (3.1.7) MUST document all approvers and their roles.

#### 5.1.2 Forms of Acceptable Approval

The following forms of approval are acceptable and MUST be documented in the Approval Reference section:

1. **PR approval and merge:** Decision record is submitted via PR, reviewed, approved, and merged by authorized person
2. **Explicit issue sign-off:** Approver posts explicit "+1" or "Approved" comment in GitHub issue with reasoning
3. **Documented meeting decision:** Meeting notes capture decision with attendees and explicit approval
4. **Direct commit by maintainer:** Repository maintainer commits decision record directly (with explanatory commit message)

**Not acceptable:**
- Implicit approval ("no one objected")
- Retroactive approval without evidence
- Agent or tool approval (humans must approve)

#### 5.1.3 Evidence Detail Requirements

Decision records MUST reference evidence proportional to the decision's impact:

**High-impact decisions** (breaking changes, principle changes, architecture decisions):
- MUST provide detailed evidence: validation results, test outcomes, analysis documentation
- SHOULD include quantitative data where relevant (e.g., "affects 12 jobs", "reduces latency by 40%")
- MUST document alternatives considered with evidence-based comparison

**Medium-impact decisions** (exceptions, scope changes, conflict resolutions):
- SHOULD provide supporting evidence where available
- MUST document reasoning even if direct evidence is limited
- SHOULD reference related documents, issues, or investigations

**Low-impact decisions** (clarifications, routine exceptions):
- MAY have minimal evidence if the decision is straightforward
- MUST still document rationale and approval

### 5.2 Grandfathering Rules for Historical Decisions

**Policy:** Historical decisions made before this standard existed are documented **as-needed** when they become relevant to current work.

**Approach:**
- Decision records for pre-standard decisions are created **only when** one of the following conditions is met:
  1. A new decision would supersede or conflict with the historical decision
  2. A current change requires referencing the historical decision's rationale or approval
  3. The historical decision is being questioned or re-evaluated
  4. Documentation of the historical decision would prevent confusion or repeated discussion

**When creating retroactive decision records:**
- Use status **"Approved (retroactive)"** to indicate the decision was made before this standard
- Document known context, rationale, and approval to the best available knowledge
- Explicitly state in the Context section that this is retroactive documentation
- Reference available evidence (commit messages, PR discussions, meeting notes, etc.)
- Mark missing information as "Unknown - decision predates formal documentation" rather than inventing details

**Rationale:**
- Minimizes documentation burden while preserving critical governance history
- Focuses effort on decisions that remain relevant to current work
- Avoids creating unnecessary documentation for obsolete or superseded historical decisions
- Allows organic discovery of which historical decisions matter through actual use

---

## 6) Storage and Discovery

### 6.1 Canonical Location (MUST)

#### 6.1.1 Decision Record Storage
Decision records MUST be stored as individual Markdown files in:
```
docs/decisions/
```

**Rationale:** Individual files enable:
- Clear git history per decision
- Parallel development of multiple decisions
- Easy cross-referencing from other documents
- Simple addition/modification without merge conflicts

#### 6.1.2 File Naming Convention
Decision record files MUST be named:
```
DR-NNNN-short-slug.md
```

**Rules:**
- `NNNN` is the zero-padded 4-digit decision number (must match Decision ID in file)
- `short-slug` is a kebab-case slug derived from the title (lowercase, hyphens, under 50 characters)
- File extension MUST be `.md`

**Examples:**
```
DR-0001-adopt-snake-case-naming.md
DR-0042-migrate-artifacts-catalog-schema.md
```

**Rationale:** File names sort chronologically and are human-readable while maintaining stable references.

### 6.2 Decision Log Index (MUST)

#### 6.2.1 Index Location and Purpose
An index of all decision records MUST be maintained at:
```
docs/catalogs/decision_log.md
```

**Purpose:** Provides navigable index of decisions with status, date, and brief description.

**Reference:** `documentation_system_catalog.md` Section 28 defines the canonical purpose and boundaries of the decision log.

#### 6.2.2 Required Index Content
The decision log MUST contain:

```markdown
# Decision Log

## Purpose
[Standard purpose statement per documentation_system_catalog.md]

## Active Decisions
| Decision ID | Title | Status | Approved Date | Tags |
|-------------|-------|--------|---------------|------|
| DR-0001 | Adopt snake_case naming | Approved | 2026-01-15 | naming, standards |
| ... | ... | ... | ... | ... |

## Superseded Decisions
[List of superseded decisions with references to superseding decisions]

## Rejected/Withdrawn Decisions
[List of rejected/withdrawn decisions for historical reference]
```

**Rules:**
- Index MUST be kept up-to-date when decisions are created or status changes
- Active decisions MUST be listed in reverse chronological order (newest first)
- Tags SHOULD be used to enable filtering by topic area (see Section 6.2.4 for recommended tags)
- Cross-references to decision files MUST use relative paths

**Formatting conventions:**
- **Decision ID column**: Use plain text (e.g., `DR-0001`) or markdown link (e.g., `[DR-0001](../decisions/DR-0001-adopt-snake-case-naming.md)`)
- **Title column**: Keep concise (under 60 characters); truncate with "..." if needed for readability
- **Tags column**: Use comma-separated format (e.g., `naming, standards`); leave empty or use `-` for decisions without tags
- **Long content**: If table becomes unwieldy, consider splitting by year or status in separate sub-tables

#### 6.2.3 Index Maintenance
- Adding a new decision: Add entry to appropriate status section in decision log
- Status change: Move entry between sections and update status/date columns
- Automation: Index maintenance MAY be automated but MUST be verified by humans

#### 6.2.4 Recommended Decision Tags

**Policy:** Tags are **recommended but not required**. Decision records SHOULD use tags from the suggested categories below to enable filtering, but custom tags MAY be added when existing tags are insufficient.

**Recommended tag categories:**

**Scope tags** (what area the decision affects):
- `naming` - Naming conventions, identifiers, file names
- `artifacts` - Artifact contracts, catalog entries, data formats
- `workflow` - Development workflow, process steps, execution procedures
- `governance` - Governance rules, approval gates, authority models
- `standards` - Standard specifications, schemas, required fields
- `architecture` - System architecture, design patterns, technology choices
- `documentation` - Documentation structure, catalog, placement rules

**Impact tags** (nature of the decision):
- `breaking-change` - Breaks existing contracts or requires migration
- `exception` - Exception to an established standard or principle
- `conflict-resolution` - Resolves conflict between intent/rules/runtime/evidence

**Usage guidelines:**
- Use 1-3 tags per decision (avoid over-tagging)
- Prefer existing tags over creating new ones
- When creating custom tags, use lowercase with hyphens (kebab-case)
- Document new tag meanings in decision log if they become commonly used

**Rationale:**
- Suggested tags provide consistency without rigid enforcement
- Allows organic evolution of tag vocabulary based on actual needs
- Scope tags enable filtering by functional area
- Impact tags highlight decisions requiring special attention

### 6.3 Cross-Referencing Rules (MUST)

#### 6.3.1 Referencing Decisions from Other Documents
When other documents reference a decision record:

**Format:**
```markdown
[Brief context] (ref: DR-0001)
```
or
```markdown
See decision record DR-0001 for rationale and approval details.
```

**Rules:**
- MUST use the Decision ID (e.g., `DR-0001`), not the file name
- SHOULD provide brief context about what the decision covers
- MAY link directly to the decision file: `[DR-0001](docs/decisions/DR-0001-adopt-snake-case-naming.md)`
- MUST NOT duplicate the decision's rationale or approval details (single source of truth)

#### 6.3.2 Referencing from Decision Records
Decision records should reference relevant documents:

**Format:**
```markdown
This decision implements the breaking change process defined in `naming_standard.md` Section 5.
```

**Rules:**
- Use relative paths from repository root for document references
- Reference specific sections when applicable
- MUST NOT embed normative rules from other documents (reference only)

---

## 7) Relationship to Other Governance Artifacts

### 7.1 Approval Gates (Target Agent System)
Decision records implement the approval gate discipline defined in `target_agent_system.md`:
- Decisions document explicit human approval (not agent-generated)
- Approval reference section provides auditable evidence of sign-off
- Status lifecycle enforces that decisions cannot be "approved" without evidence

### 7.2 Evidence Discipline (Target Agent System, Validation Standard)
Decision records follow evidence discipline:
- Evidence sources section documents what evidence informed the decision
- Claims about validation or compliance must reference specific evidence
- Lack of evidence is explicitly stated rather than hidden

**Integration point:** When `validation_standard.md` is finalized, decision records should reference validation requirements for decisions that affect validation rules.

### 7.3 Breaking Change Rules (Naming Standard, Artifacts Catalog Spec)
Decision records are required for breaking changes:
- `naming_standard.md` Section 5 defines what constitutes a breaking change to naming conventions
- `artifacts_catalog_spec.md` Section 6.5 defines breaking changes to artifact contracts
- Decision records document the breaking change, migration plan, and approval

**Cross-reference rule:** Breaking change standards SHOULD reference this decision records standard for the documentation requirement.

### 7.4 Conflict Resolution (Workflow Guide)
Decision records implement the conflict resolution procedure:
- `workflow_guide.md` Section 7 defines conflict handling procedure
- Decision records document resolution choices when conflicts are detected
- Context section describes the conflict; Decision section states the resolution

### 7.5 Documentation Governance (Documentation Spec)
Decision records follow documentation principles:
- Single source of truth: Decision is recorded once in its decision record
- Evidence-based claims: Evidence sources section provides references
- Explicit over implicit: Status, approval, and rationale are all explicit
- Separation of concerns: Decision records document governance decisions, not implementation details

**Exception:** Decision records have special metadata requirements (Decision ID, Status section) that differ from standard document headers defined in `documentation_spec.md` Section 3 (ref: `documentation_spec.md` Section 6.5.2).

---

## 8) Examples

### 8.1 Example: Simple Decision Record

**Note:** This is a NON-NORMATIVE example illustrating structure, not content.

```markdown
# DR-0001: Adopt snake_case for job identifiers

## Status

**Current Status:** Approved
**Date:** 2026-01-15
**Approved by:** Jane Smith (Repository Maintainer)

## Context

The repository contains jobs with inconsistent naming: some use snake_case (e.g., `preprocess_incoming_bmecat`) while others use camelCase (e.g., `extractVendorCategories`). This inconsistency complicates automation, validation rules, and creates confusion for contributors.

The naming standard is being developed and needs a normative convention for job identifiers.

## Decision

All job identifiers MUST use snake_case format (lowercase with underscores). 

Existing jobs using camelCase MUST be migrated within 90 days using the deprecation process defined in `naming_standard.md` Section 5.

## Rationale

- **Consistency:** Single convention simplifies automation and validation
- **Ecosystem alignment:** Python and YAML ecosystems prefer snake_case (PEP 8)
- **Readability:** snake_case is more readable than camelCase for multi-word identifiers
- **Tooling:** Regex patterns and validation rules are simpler with consistent casing

Trade-off: Migration requires updating 4 existing jobs, but long-term consistency benefit outweighs short-term migration cost.

## Consequences

**Positive:**
- Consistent naming across all jobs
- Simplified validation and automation rules
- Clearer onboarding for new contributors

**Negative:**
- Requires migrating 4 existing jobs (affects downstream references)
- Short-term disruption during migration period

**Migration needs:**
- Update 4 job folders and manifests
- Update references in artifacts catalog
- Update CI/automation configurations

**Affected components:**
- Jobs: extractVendorCategories, processProductData, validateMappings, generateReport (4 jobs)
- Documents: job_inventory.md, artifacts_catalog.md
- Automation: validation scripts, CI pipeline

## Approval Reference

**Approval method:** PR approval
**Approval evidence:** PR #42 approved and merged
**Approved by:** Jane Smith (Repository Maintainer)
**Approval date:** 2026-01-15

## Evidence Sources

- Analysis of existing job IDs: 8 of 12 jobs use snake_case, 4 use camelCase (documented in issue #123)
- Validation tool testing: snake_case simplifies regex matching (testing: PR #119)
- Industry standards: PEP 8 (Python style guide), YAML best practices
- Team discussion: Consensus in planning meeting 2026-01-10

## Supersedes / Superseded By

**Supersedes:** None (first decision in this area)
**Superseded by:** None (currently active)
```

### 8.2 Example: Decision That Supersedes Another

**Note:** This is a NON-NORMATIVE example illustrating supersession relationship.

```markdown
# DR-0015: Extend job ID length limit to 64 characters

## Status

**Current Status:** Approved
**Date:** 2026-02-20
**Approved by:** Alex Chen (Technical Lead)

## Context

The original naming standard (DR-0001) recommended keeping job IDs under 40 characters. However, as the system grew, several complex jobs require more descriptive names that exceed this limit.

Recent jobs have been artificially abbreviated to fit the 40-character recommendation, reducing readability (e.g., `proc_incom_bme_cat_v2` instead of `process_incoming_bmecat_categories_v2`).

## Decision

The job ID length recommendation is extended from 40 to 64 characters. Job IDs MUST still be under 256 characters (filesystem limit) but SHOULD be under 64 characters for readability.

Existing jobs under 40 characters do NOT need to be renamed. New jobs may use up to 64 characters when descriptive names require it.

## Rationale

- **Readability:** Longer names can be more descriptive and self-documenting
- **Reduced abbreviation:** Eliminates need for cryptic abbreviations
- **Minimal disruption:** Existing jobs are unaffected; only new jobs benefit
- **Bounded:** 64 characters is still well under filesystem limits and reasonable for UI display

Trade-off: Slightly longer names in some contexts, but improved clarity outweighs this minor inconvenience.

## Consequences

**Positive:**
- More descriptive, readable job names
- Reduced need for abbreviations
- Better self-documentation

**Negative:**
- Slightly longer names in logs and UI (minor)

**Migration needs:**
- None (existing jobs are unaffected)
- Update naming standard documentation to reflect new guidance

**Affected components:**
- Documents: naming_standard.md (update Section 3.4)
- New jobs only (existing jobs unchanged)

## Approval Reference

**Approval method:** Issue sign-off
**Approval evidence:** Issue #234, comment by Alex Chen approving the change
**Approved by:** Alex Chen (Technical Lead)
**Approval date:** 2026-02-20

## Evidence Sources

- Analysis of job name lengths: 3 recent jobs required artificial abbreviation (issue #234)
- Readability testing: Team members preferred longer descriptive names over abbreviated versions
- Filesystem limits: No technical constraint below 256 characters

## Supersedes / Superseded By

**Supersedes:** DR-0001 (partially - updates length guidance only; snake_case rule remains)
**Superseded by:** None (currently active)
```

**Note:** DR-0001's status would be updated to:
```markdown
**Superseded by:** DR-0015 (partially - length guidance updated; snake_case rule still active)
```

---

## 9) Resolved Decisions on Standard Implementation

This section documents decisions made about how to implement this standard itself.

### 9.1 Grandfathering Rules for Historical Decisions

**Decision:** Adopted **as-needed documentation** approach (Option 3).

**Rationale:** Minimizes documentation burden while preserving critical governance history. Historical decisions are documented only when they become relevant to current work.

**Implementation:** See Section 5.2 for complete policy and guidelines.

**Date resolved:** 2026-02-02

---

### 9.2 Decision Review and Expiration Policy

**Decision:** **No review policy** (Option 1) - decisions remain active until explicitly superseded.

**Rationale:** 
- Simpler to implement and maintain (reactive approach)
- Avoids bureaucratic overhead of scheduled reviews
- Natural supersession process when decisions become outdated
- Teams can always initiate reviews when concerns arise
- Aligns with reactive conflict resolution model (Section 2.1.3)

**Implementation:**
- Decisions do not expire automatically
- Decisions remain in "Approved" status until explicitly superseded or deprecated
- If a decision becomes questionable, any team member can propose a superseding decision
- Optional "Review History" section (Section 3.2.4) allows tracking when decisions are revisited

**Date resolved:** 2026-02-02

---

### 9.3 Automation and Tooling Support

**Decision:** Automation is **recommended for documentation workflows** but not required.

**Intended automation level:**
- **When adding new documentation elements** (context docs, standards, process guides):
  - Agents/tools SHOULD draft decision records when the change meets triggering conditions in Section 2.1
  - Example: Adding a new document type to the catalog triggers Section 2.1.4 → agent drafts decision record
  
- **When creating PRs that introduce governance changes**:
  - PR workflow SHOULD prompt for decision record creation if changes meet triggering conditions
  - Decision records can be included in the same PR as the changes they document
  - Example: PR modifying approval gate rules → includes draft decision record explaining change

- **Decision log index maintenance**:
  - MAY be automated (parse decision files, generate index)
  - MUST be verified by humans before committing

- **Scaffolding and validation**:
  - Decision record templates MAY be generated (next Decision ID, pre-filled structure)
  - Cross-reference validation MAY be automated (check referenced decisions exist)
  - Status transition validation MAY be automated (enforce lifecycle rules)
  - Decision ID uniqueness validation SHOULD be automated (check no duplicate IDs exist)

**Implementation guidance:**
- Specific automation implementation details (commands, scripts, procedures) belong in `docs/ops/tooling_reference.md` (not in this standard)
- Manual processes (e.g., how to determine next Decision ID) belong in `docs/ops/tooling_reference.md`
- Automation is supportive, not mandatory - manual creation is always acceptable
- Focus automation on reducing friction, not enforcing compliance

**Rationale:**
- Integrating decision record drafting into documentation/PR workflows reduces forgetting
- Automation assists but doesn't replace human judgment on when decisions are needed
- Keeps this standard focused on "what" not "how" (separation of concerns)

**Date resolved:** 2026-02-02

---

### 9.4 Decision Categories and Tags

**Decision:** Adopted **suggested tags** approach (Option 2).

**Rationale:**
- Balances consistency with flexibility
- Provides recommended tags for common categories without rigid enforcement
- Allows organic evolution of tag vocabulary
- Avoids over-engineering at start while providing useful structure

**Implementation:** See Section 6.2.4 for recommended tag categories and usage guidelines.

**Recommended tag categories:**
- **Scope tags:** naming, artifacts, workflow, governance, standards, architecture, documentation
- **Impact tags:** breaking-change, exception, conflict-resolution

**Date resolved:** 2026-02-02

---

## 10) Consistency Check Appendix

### 10.1 Documents Aligned With

This standard was aligned with the following documents:

**Context layer:**
- ✅ `development_approach.md` - Referenced 5-step workflow, approval gates, iterative refinement
- ✅ `target_agent_system.md` - Aligned with approval gates, evidence discipline, conflict handling, no double truth
- ✅ `documentation_system_catalog.md` - Followed document type definitions, canonical placement rules, layer boundaries
- ✅ `glossary.md` - Used canonical term definitions for decision record, conflict, breaking change, approval gate, evidence

**Standards layer:**
- ✅ `documentation_spec.md` - Followed formatting rules (Markdown, metadata headers, single source of truth principles)
- ✅ `naming_standard.md` - Referenced breaking change rules, aligned with file naming conventions (snake_case, kebab-case)
- ✅ `artifacts_catalog_spec.md` - Referenced breaking change rules for artifact contracts
- ✅ `job_manifest_spec.md` - Studied structure and pattern for normative specifications (schema, MUST/SHOULD/MAY keywords)

**Process layer:**
- ✅ `workflow_guide.md` - Aligned with conflict resolution procedure (Section 7), evidence expectations (Section 6)

**Agent layer:**
- ✅ `agent_role_charter.md` - Aligned with agent responsibilities, escalation triggers, human approval gates

**Catalog layer:**
- ✅ `decision_log.md` - Referenced as canonical index location for decision records

**Industry best practices:**
- ✅ Architecture Decision Records (ADR) pattern - Adapted status lifecycle (Proposed/Accepted/Deprecated/Superseded)
- ✅ MADR (Markdown Any Decision Records) - Adopted lightweight Markdown format, context/decision/consequences structure
- ✅ GitHub ADR practices - Used individual files per decision for git history, kebab-case file naming

### 10.2 Potential Conflicts Detected

**No conflicts detected.** This standard builds on existing governance documents without contradicting them.

**Integration points verified:**
- Decision records implement (not replace) conflict resolution procedures in `workflow_guide.md`
- Breaking change rules in `naming_standard.md` and `artifacts_catalog_spec.md` trigger decision record requirement
- Evidence discipline in `target_agent_system.md` is implemented in decision record structure
- Approval gate rules in `target_agent_system.md` are enforced by decision record approval requirements

### 10.3 Assumptions and Resolved Decisions

**Assumptions made (bounded):**
1. **Individual files per decision:** Assumed based on industry best practices (ADR pattern) and git history benefits; explicitly documented in Section 6.1.1
2. **Decision ID format (DR-NNNN):** Assumed based on common ADR numbering schemes; explicitly documented in Section 3.1.1
3. **Four-digit zero-padded numbering:** Allows 10,000 decisions before format change; reasonable for this repository's expected scale
4. **Kebab-case file slugs:** Aligned with industry practice; complements decision ID in file names
5. **Status lifecycle states:** Based on ADR practices (Proposed/Accepted/Superseded) plus repository-specific needs (Rejected, Withdrawn, Deprecated)

**Impact of assumptions:** Low risk. Assumptions follow industry best practices and can be adjusted if needed through decision records.

**Implementation decisions resolved (Section 9):**
1. ✅ **Grandfathering rules:** As-needed documentation approach adopted (Section 9.1, implemented in Section 5.2)
2. ✅ **Review/expiration policy:** No review policy - decisions active until superseded (Section 9.2)
3. ✅ **Automation support:** Recommended for documentation/PR workflows; details in ops layer (Section 9.3)
4. ✅ **Tag standardization:** Suggested tags with recommended categories (Section 9.4, implemented in Section 6.2.4)

**Improvements made (2026-02-02):**
1. ✅ **Circular dependency resolved:** Added exception for standard adoption itself (Section 2.1 note)
2. ✅ **Partial supersession clarified:** Use Approved status with notes, not Deprecated (Section 3.1.9)
3. ✅ **Amendment process added:** New Section 3.3 covering post-approval corrections
4. ✅ **Status transitions clarified:** Section 4.1.3 now explicit about direct and via-Deprecated paths
5. ✅ **Operational details separated:** Section 9.3 now references ops layer for implementation specifics
6. ✅ **Multi-approver guidance added:** Section 5.1.1 now specifies when multiple approvals recommended
7. ✅ **Decision conflicts addressed:** Section 2.1.3 now covers decision-to-decision conflicts

**Next steps:**
- Human review and approval of this standard
- Create `docs/decisions/` directory
- Update `docs/catalogs/decision_log.md` with initial structure per Section 6.2.2
- Optionally create retroactive decision records for historical decisions as they become relevant (per Section 5.2)

### 10.4 Validation Against Requirements

**Original requirements from problem statement:**

1. ✅ **Define when a decision record is required** - Section 2 (triggering conditions with 8 specific scenarios)
2. ✅ **Define what constitutes a decision record** - Section 3 (9 required sections with formats and rules)
3. ✅ **Define status lifecycle** - Section 4 (6 status values with transition rules and diagram)
4. ✅ **Define evidence and approval reference expectations** - Section 5 (approval requirements, acceptable forms, evidence detail)
5. ✅ **Integrate with repository governance model** - Section 7 (relationships to approval gates, evidence discipline, breaking changes, conflicts)
6. ✅ **Clear boundaries** - Purpose and scope sections clarify what belongs in decision records vs. other documents
7. ✅ **Readable and enforceable** - Uses MUST/SHOULD/MAY consistently, provides examples, includes validation rules

**Non-goals verified:**
- ✅ Does not include general workflow instructions (references workflow_guide.md instead)
- ✅ Does not include tool/CLI instructions (notes automation belongs in ops layer)
- ✅ Does not embed large templates (provides minimal structural examples in Section 8)
- ✅ Does not redefine glossary terms (references existing definitions)
- ✅ Does not duplicate approval/evidence rules (references target_agent_system.md)
- ✅ Does not include operational guidance (notes process layer responsibility when finalized)

**Document quality:**
- Follows `documentation_spec.md` formatting requirements (Markdown, snake_case file naming, metadata header)
- Uses normative keywords (MUST/SHOULD/MAY) correctly and consistently
- Provides clear section headings and logical structure
- Includes both normative rules and non-normative examples
- All implementation decisions resolved (grandfathering, review policy, automation, tags)

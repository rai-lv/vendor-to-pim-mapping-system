# Validation Standard

## Purpose

This standard defines the normative rules for what "verified" means, what validations are required, and what evidence is acceptable for approvals, operationalizing evidence discipline and approval gates to ensure all claims are verifiable and all progression is evidence-backed.

---

## 0) Scope

### What This Standard Covers

This standard defines:

1. **What "verified" means** in this repository's context with clear, testable semantics
2. **When validation is required** (triggering conditions tied to the 5-step workflow)
3. **What constitutes acceptable evidence** for different types of claims
4. **Validation categories** and the validation rules that apply to each
5. **Pass/fail semantics** and what happens when validation fails
6. **Evidence expectations** for approval gates at each workflow step
7. **Integration** with the repository's governance model

### What This Standard Does NOT Cover

This standard does NOT include:

- **Tool command syntax or CLI instructions** (see `docs/ops/tooling_reference.md`)
- **General workflow instructions** (see `docs/process/workflow_guide.md`)
- **Troubleshooting procedures or operational runbooks** (see `docs/ops/` layer)
- **Glossary term definitions** (see `docs/context/glossary.md`)
- **Approval process mechanics** (see `docs/process/contribution_approval_guide.md`)
- **Tool-specific validation logic implementation details** (reference tools that implement validation)
- **Per-job validation specifics** (those belong in per-job documentation)

### Relationship to Other Documents

This standard:

- **Operationalizes** evidence discipline principles defined in `docs/context/target_agent_system.md`
- **Supports** the 5-step workflow defined in `docs/context/development_approach.md` and `docs/process/workflow_guide.md`
- **Enables** approval gates defined in `docs/context/target_agent_system.md`
- **References** glossary terms from `docs/context/glossary.md` (does not redefine them)
- **Complements** other standards that define schemas and structures to be validated

---

## 1) Foundational Principles

These principles are grounded in existing repository documentation and govern all validation and evidence practices.

### 1.1 Evidence Discipline (from Target Agent System)

**Principle:** All claims about system behavior, validation status, or compliance MUST be backed by explicit, deterministic evidence.

**Source:** `docs/context/target_agent_system.md` Section "Approval Gates and Evidence Discipline"

**Application to validation:**
- Validation results MUST be deterministic (same inputs → same outputs)
- Validation reports MUST be reviewable by any team member
- "Verified" or "confirmed" claims MUST reference specific evidence
- Lack of evidence MUST be recorded explicitly as "unverified", "unknown", or "TBD"

### 1.2 No Hidden Authority (from Target Agent System)

**Principle:** Agents and tools must never imply outputs are "true" because an agent produced them or a tool reported them. Truth is grounded in human decisions, enforceable standards, runtime behavior, and deterministic evidence.

**Source:** `docs/context/target_agent_system.md` Section "Non-Negotiable Operating Rules"

**Application to validation:**
- Validation tool outputs are inputs to decisions, not decisions themselves
- Humans interpret validation results and approve progression
- Tools enforce defined rules; they do not invent requirements
- Validation failures trigger human review, not automatic rejection

### 1.3 Explicit Over Implicit (from Documentation Spec)

**Principle:** Unknowns, assumptions, decisions, and boundaries must be stated explicitly, not left implicit.

**Source:** `docs/standards/documentation_spec.md` Section 1.4

**Application to validation:**
- If evidence doesn't exist, use "TBD" or "unverified" rather than claiming verification
- If validation cannot be performed, mark it explicitly
- If acceptance criteria cannot be evaluated, escalate rather than assume success
- If validation passes with caveats, document the caveats

### 1.4 Validation Against Success Criteria (from Development Approach)

**Principle:** Every artifact must comply with user-defined success criteria at each planning stage. Validation ensures outputs meet these criteria before moving forward.

**Source:** `docs/context/development_approach.md` Section "Core Principles"

**Application to validation:**
- Validation checks alignment with acceptance criteria
- Success criteria MUST be evaluable (testable)
- Validation evidence demonstrates acceptance criteria are met
- Validation failures indicate misalignment with success criteria

---

## 2) What "Verified" Means (Normative Definition)

### 2.1 Definition

A claim can be labeled as **"verified"** if and only if:

1. **Evidence exists** that directly demonstrates the claim
2. **Evidence is deterministic** (reproducible given same inputs and context)
3. **Evidence is referenced explicitly** (in the repository or in the conversation)
4. **Evidence is reviewable** by any team member with appropriate access

**Source:** Aligns with glossary definition of "Verified / Confirmed" and evidence discipline rules in `docs/context/target_agent_system.md`.

### 2.2 Acceptable Forms of Evidence

Evidence MAY take the following forms:

1. **Validation reports:** Output from validation tools (JSON, text, structured formats)
2. **Test results:** Unit test results, integration test results (JUnit XML, TAP, text reports)
3. **Build outputs:** Successful compilation, linting results, static analysis reports
4. **Runtime logs:** Execution logs showing expected behavior
5. **Run receipts:** Structured execution records (JSON metadata files)
6. **Screenshots/recordings:** Visual evidence of UI behavior or system state
7. **Approval records:** Explicit human approvals in PRs, decision records, or issues
8. **Git commits:** Proof that changes were merged (execution confirmation)
9. **CI/CD artifacts:** Automated validation results from CI workflows

### 2.3 Insufficient Evidence

The following are NOT sufficient evidence on their own:

- **Narrative claims** without referenced outputs ("I checked and it works")
- **Agent assertions** without tool outputs or human approval
- **Implied success** (absence of failure ≠ proof of success)
- **Stale evidence** (evidence from a different version or state)
- **Partial evidence** when comprehensive evidence is required

### 2.4 When Verification is Sufficient vs. Additional Validation Needed

**Verification is sufficient when:**
- Evidence directly demonstrates the claim
- Evidence covers all relevant aspects
- Evidence is recent and matches current state

**Additional validation is needed when:**
- Evidence is partial or incomplete
- Evidence is stale (system has changed since verification)
- Multiple types of validation are required (structure + conformance + runtime)
- Breaking changes require comprehensive validation
- Approval gates require multiple evidence types

### 2.5 Evidence Citation Format

When referencing tool outputs in evidence summaries, approval requests, or validation reports, use the following standard formats to ensure consistency and traceability:

**For validation tools:**
```
Validated using [tool name] [version if known].
Result: [pass/fail summary]
Violations found: [count and brief description]
Evidence: [location of full report or key output lines]
```

**For evidence tools (tests, runtime verification):**
```
Verified using [tool name/test suite name].
Result: [outcome summary]
Acceptance criterion: [specific criterion being verified]
Evidence: [location of logs/reports/screenshots with line numbers or timestamps]
```

**For scaffolding tools:**
```
Draft generated using [tool name] [version if known].
Tool extracted: [list of auto-generated content]
Manual additions: [list of human/agent enhancements]
Status: [ready for review / requires further refinement]
```

**Version citation guidance:**
- For Python tools: Include version from `--version` flag or `__version__` attribute
- For CI/CD tools: Include workflow run ID or build number
- If version unavailable: Note "version unspecified" and include tool location/commit hash if possible
- Version specification helps ensure evidence reproducibility

---

### 2.5 Relationship Between Verification and Approval

**Verification provides evidence for approval but is not approval itself.**

- **Verification** = evidence that acceptance criteria are met
- **Approval** = human decision to proceed based on evidence review
- **Execution confirmation** = proof that approved work was executed (e.g., merge commit)

**Source:** Distinction defined in `docs/context/glossary.md` under "Evidence" and "Execution confirmation".

---

## 3) When Validation is Required (Triggering Conditions)

### 3.1 Validation Requirements by Workflow Step

Validation is REQUIRED at the following points in the 5-step workflow:

#### Step 1 (Define Objective)
- **What requires validation:** Objective exit criteria
- **Validation type:** Manual review
- **Required evidence:** Human approval that success criteria are evaluable and scope is bounded

#### Step 2 (Plan Pipeline)
- **What requires validation:** Pipeline plan exit criteria
- **Validation type:** Manual review + structure validation
- **Required evidence:** Human approval that capabilities are bounded and ordered sufficiently

#### Step 3 (Break Down Into Capability Plans)
- **What requires validation:** Capability definition and codable task breakdown
- **Validation type:** Conformance validation (against codable task spec) + manual review
- **Required evidence:** 
  - Tasks follow structure defined in `docs/standards/codable_task_spec.md`
  - Acceptance criteria are evaluable
  - Human approval of capability plan

#### Step 4 (Execute Development Tasks)
- **What requires validation:** Implementation changes
- **Validation type:** Structure validation + conformance validation + runtime validation (if code changes)
- **Required evidence:**
  - Documentation conforms to specs (if docs changed)
  - Manifests conform to schemas (if manifests changed)
  - Code builds successfully (if code changed)
  - Tests pass (if code changed)
  - Changes are traceable to approved tasks

#### Step 5 (Validate, Test, and Document)
- **What requires validation:** Comprehensive validation of all acceptance criteria
- **Validation type:** All applicable validation types
- **Required evidence:**
  - All Step 4 validations passed
  - Acceptance criteria evidence assembled
  - Documentation updated and consistent
  - No contradictions between intent/rules/runtime

### 3.2 Validation Requirements by Change Type

Different change types trigger different validation requirements:

#### Code Changes (Implementation)
MUST validate:
- **Structure:** Code builds successfully
- **Conformance:** Code follows project conventions (if enforced by linters)
- **Runtime:** Tests pass, behavior matches specification
- **Evidence:** Build logs, test results, run receipts

#### Documentation Changes
MUST validate:
- **Structure:** Files follow naming conventions, metadata headers present
- **Conformance:** Content follows relevant specification (business description spec, script card spec, etc.)
- **Consistency:** Cross-references valid, no contradictions with other docs
- **Evidence:** Validation tool reports, manual review approval

#### Manifest/Schema Changes
MUST validate:
- **Structure:** YAML/JSON is parseable
- **Conformance:** Schema validation passes (job manifest spec, artifacts catalog spec, etc.)
- **Consistency:** Cross-references resolve (artifact IDs exist, job IDs exist)
- **Evidence:** Schema validator reports, cross-reference checker reports

#### Breaking Changes
MUST validate:
- **All applicable validation types** for the change
- **Migration plan exists** (if required)
- **Decision record created** (per naming standard and breaking change rules)
- **Deprecation period documented** (if required)
- **Evidence:** Decision record, migration documentation, approval

#### Governance Changes (Standards, Policies)
MUST validate:
- **Consistency:** No conflicts with other governance documents
- **Manual review:** Human approval required
- **Decision record:** Change documented with rationale
- **Evidence:** Decision record, review approval

### 3.3 Validation NOT Required

Validation is NOT required for:

1. **Draft exploration** on feature branches (not merged)
2. **Trivial wording changes** that do not alter meaning (subject to reviewer judgment)
3. **Private work-in-progress** (personal branches, local changes)
4. **Comments and clarifications** that add information without changing contracts

**Note:** "Trivial" is subject to human judgment. When in doubt, run validation.

---

## 4) Validation Categories and Rules

This section defines five categories of validation used in this repository.

### 4.1 Structure Validation

#### What it validates
Conformance to required file structures, naming conventions, and metadata headers.

#### When applied
- On all documentation files in `docs/`
- On all manifest files (job manifests, decision records)
- Before committing new files
- During CI validation

#### Pass criteria
- File names follow `docs/standards/naming_standard.md`
- Files contain required sections per their document type
- Metadata headers are complete and correctly formatted per `docs/standards/documentation_spec.md`
- Directory structure follows canonical placement per `docs/context/documentation_system_catalog.md`

#### Typical tools
- File system checks (file naming, directory structure)
- Manifest validators (YAML parsing, required fields present)
- Structure checkers (section headings, metadata headers)
- Linters (Markdown linters, YAML linters)

#### Evidence output
- Validation reports showing pass/fail per file
- Specific failures listed with file path and issue description
- References to relevant specification sections

#### Blocking severity
**Structure validation failures SHOULD block file acceptance.**
- Files with invalid structure create downstream issues
- Exception: Minor formatting issues MAY be warnings if content is correct

### 4.2 Conformance Validation

#### What it validates
Compliance with normative schemas and specifications.

#### When applied
- On job manifests (against `docs/standards/job_manifest_spec.md`)
- On artifacts catalog entries (against `docs/standards/artifacts_catalog_spec.md`)
- On business descriptions (against `docs/standards/business_job_description_spec.md`)
- On script cards (against `docs/standards/script_card_spec.md`)
- On codable task specifications (against `docs/standards/codable_task_spec.md`)
- On decision records (against `docs/standards/decision_records_standard.md`)
- During CI validation

#### Pass criteria
- All required fields are present
- Field values match expected types and formats
- Enums use allowed values only
- Cross-references point to existing entities (job IDs, artifact IDs)
- Content follows specification rules (e.g., TBD vs NONE usage, placeholder normalization)

#### Typical tools
- Schema validators (JSON Schema, YAML validators)
- Spec compliance checkers (custom validators per specification)
- Cross-reference validators (check artifact IDs exist, job IDs exist)

#### Evidence output
- Conformance reports with specific failures listed
- Field-level validation errors (missing fields, invalid values, type mismatches)
- Cross-reference resolution failures

#### Blocking severity
**Conformance validation failures MUST block step approval.**
- Non-conforming artifacts cannot be processed by automation
- Cross-reference failures indicate broken dependencies

### 4.3 Consistency Validation

#### What it validates
Internal consistency across related documents (no contradictions, all references resolve, cross-document constraints satisfied).

#### When applied
- After changes to related documents
- Before approval gates
- During Step 5 (Validate, Test, and Document)
- As part of Doc Impact Scan (per `docs/process/workflow_guide.md` Section 6)

#### Pass criteria
- No contradictions between documents
- All cross-references resolve to existing documents/sections
- Glossary terms used consistently across documents
- No competing authority (single source of truth maintained)
- No "double truth" (same contract not defined in multiple places)

#### Typical tools
- Cross-reference checkers (validate links, ensure targets exist)
- Consistency scanners (detect contradictions, duplicate definitions)
- Glossary term checkers (ensure terms used per glossary)
- Manual review (human judgment for semantic consistency)

#### Evidence output
- Consistency reports identifying contradictions
- Broken reference lists (with source and target)
- Competing authority warnings (duplicate definitions)
- Glossary term misuse warnings

#### Blocking severity
**Consistency validation failures SHOULD block merging.**
- Contradictions must be resolved before merging
- Broken references should be fixed or documented as TBD
- Competing authority must be resolved (designate canonical source)
- Exception: Minor inconsistencies MAY be warnings if they don't affect meaning

### 4.4 Runtime Validation

#### What it validates
That implemented code/scripts behave as specified in their contracts.

#### When applied
- After code changes
- Before Step 5 approval
- As part of CI validation for code changes
- When implementing codable tasks

#### Pass criteria
- Unit tests pass
- Integration tests pass (if applicable)
- Outputs match expected formats
- Invariants hold (conditions that must always be true)
- Error handling works as specified
- Performance meets requirements (if specified)

#### Typical tools
- Unit test frameworks (pytest, unittest, JUnit)
- Integration test suites
- Output validators (format checkers, schema validators for outputs)
- Behavior checks (functional tests)
- Static analysis tools (for code quality, security)

#### Evidence output
- Test results (test count, pass/fail, coverage)
- Run logs showing expected behavior
- Output validation reports (format conformance)
- Performance metrics (if applicable)
- Error handling test results

#### Blocking severity
**Runtime validation failures MUST block Step 5 approval.**
- Failed tests indicate implementation does not meet specification
- Invalid outputs indicate contract violations
- Broken invariants indicate logic errors

### 4.5 Manual Review Validation

#### What it validates
Judgment-based quality checks that cannot be fully automated.

#### When applied
- At all approval gates
- For breaking changes
- For governance decisions (standards changes, policy changes)
- When automated validation is insufficient
- At Step 5 final approval

#### Pass criteria
- Human reviewer confirms alignment with intent
- Quality standards met (readability, maintainability, clarity)
- Principles adhered to (evidence discipline, single source of truth, explicit over implicit)
- No obvious issues or concerns
- Acceptance criteria satisfied (human judgment)

#### Typical tools
- PR review process
- Decision record reviews
- Architectural reviews
- Documentation reviews
- Code reviews

#### Evidence output
- Approval records (PR approvals, review comments)
- Review comments (feedback, questions, concerns)
- Sign-offs (explicit approval statements)
- Decision records (for governance decisions)

#### Blocking severity
**Manual review rejection MUST block approval.**
- Human reviewers have authority to block progression
- Rejection requires documented reason
- Re-review required after addressing concerns

---

## 4.6 Escalation Criteria for Validation Failures

This section defines when validation failures should be escalated to human decision rather than automatically fixed by agents.

### Ambiguous Validation Failures

A validation failure is considered **ambiguous** and MUST be escalated when:

1. **Violation message contradicts approved standards:**
   - Validation tool reports a violation that conflicts with a documented standard or specification
   - Multiple interpretations of the requirement exist
   - Example: Tool says field is required, but spec marks it optional

2. **Fix requires interpreting requirements:**
   - Resolution cannot be achieved through mechanical reformatting
   - Agent must make judgment about intent or meaning
   - Example: "Choose between INPUT_BUCKET or VENDOR_DATA_BUCKET based on context"

3. **Multiple valid interpretations exist:**
   - Specification allows multiple correct values
   - Agent cannot determine correct choice without additional context
   - Example: Enum allows both "pending" and "in_progress" with unclear distinction

4. **Validation rule conflicts with workflow guidance:**
   - Validation tool enforces a rule that contradicts approved capability plan or objective
   - Following validation rule would change approved intent
   - Example: Validation requires field but approved plan explicitly excludes it

### Clear Validation Failures (Can Be Fixed)

Validation failures that SHOULD be fixed automatically (no escalation needed):

1. **Formatting issues:**
   - Incorrect indentation, spacing, or line breaks
   - Missing quotation marks or brackets
   - Trailing whitespace or empty lines

2. **Mechanical completeness:**
   - Missing required field that has obvious default value
   - Field present but empty when non-empty required
   - Placeholder using wrong syntax (e.g., `{placeholder}` should be `{{placeholder}}`)

3. **Cross-reference resolution:**
   - Reference to entity that exists but with typo in ID
   - Reference format incorrect but target is clear
   - Example: "job_id: vendor input" should be "job_id: vendor_input"

### Escalation Process

When escalating validation failures:

1. **Provide full context:** Include validation output, affected artifact, and approved intent
2. **Explain the ambiguity:** State why automatic fix is not appropriate
3. **Propose options:** If multiple resolutions exist, list them with trade-offs
4. **Reference standards:** Point to conflicting requirements or specifications
5. **Await human decision:** Do not proceed with implementation until guidance received

---

## 5) Evidence Expectations by Workflow Step

This section defines what validation evidence is required at each step of the 5-step workflow.

### 5.1 Step 1: Define Objective

**Required evidence before objective approval:**

1. **Success criteria exist and are evaluable**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms criteria are testable
   - Acceptable: PR approval, review comment confirming evaluability

2. **Scope boundaries exist and are unambiguous**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms in-scope/out-of-scope is clear
   - Acceptable: PR approval, review comment confirming clarity

3. **Unknowns are explicitly listed**
   - Evidence type: Structure validation + manual review
   - Evidence format: Unknowns section present with TBD markers
   - Acceptable: Document contains unknowns section (even if empty), manual confirmation

**Sufficient clarity criteria:**
- Success criteria can be translated into acceptance criteria
- Scope boundaries prevent scope creep
- Unknowns do not block pipeline planning

### 5.2 Step 2: Plan Pipeline

**Required evidence before pipeline approval:**

1. **Each capability has clear boundaries**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms each capability is bounded
   - Acceptable: PR approval, review comment

2. **Pipeline is ordered sufficiently to start capability planning**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms ordering is clear
   - Acceptable: PR approval, review comment

3. **No scope expansion beyond objective**
   - Evidence type: Consistency validation + manual review
   - Evidence format: Pipeline aligns with objective scope
   - Acceptable: Manual confirmation, consistency check pass

**Pipeline completeness criteria:**
- Capabilities cover success criteria
- Dependencies and decision points surfaced
- No ambiguous capability boundaries

### 5.3 Step 3: Break Down Into Capability Plans

**Required evidence before capability plan approval:**

1. **Capability definition conforms to codable task spec**
   - Evidence type: Conformance validation
   - Evidence format: Structure check passes for codable task elements
   - Acceptable: Validation report showing conformance
   - Reference: `docs/standards/codable_task_spec.md`

2. **Acceptance criteria are evaluable**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms criteria can be tested
   - Acceptable: PR approval, review comment

3. **Tasks are bounded and cover the capability**
   - Evidence type: Manual review
   - Evidence format: Human reviewer confirms no "do everything" tasks
   - Acceptable: PR approval, review comment

4. **No unapproved assumptions**
   - Evidence type: Manual review
   - Evidence format: All assumptions explicitly labeled and approved
   - Acceptable: Assumption documentation + approval record

**Implementation feasibility criteria:**
- Tasks have clear intended outputs
- Dependencies are explicit
- No circular dependencies
- Acceptance criteria can guide implementation

### 5.4 Step 4: Execute Development Tasks

**Required evidence during implementation:**

1. **Code changes (if applicable):**
   - Evidence type: Runtime validation
   - Evidence format: Build succeeds, tests pass
   - Acceptable: CI build logs, test results
   - Blocking: Test failures MUST be resolved

2. **Documentation changes (if applicable):**
   - Evidence type: Structure validation + conformance validation
   - Evidence format: Validation tool reports
   - Acceptable: `validate_repo_docs.py` output showing pass
   - Blocking: Validation failures MUST be resolved

3. **Manifest changes (if applicable):**
   - Evidence type: Conformance validation
   - Evidence format: Schema validation passes
   - Acceptable: Validation tool reports, manual verification
   - Blocking: Schema failures MUST be resolved

4. **Changes traceable to approved tasks:**
   - Evidence type: Manual review
   - Evidence format: PR description references tasks
   - Acceptable: Commit messages, PR description linking to tasks

**Task completion criteria:**
- Intended outputs exist in repository
- No unapproved scope expansion
- Changes align with task boundaries

### 5.5 Step 5: Validate, Test, and Document

**Required comprehensive validation evidence:**

1. **All Step 4 validations passed**
   - Evidence type: All applicable types
   - Evidence format: Validation reports, test results
   - Acceptable: CI passing, local validation passing

2. **Acceptance criteria evidence assembled**
   - Evidence type: Varies by acceptance criteria
   - Evidence format: Test results, validation reports, run receipts, manual verification
   - Acceptable: Evidence list in PR description or validation document

3. **Documentation updated and consistent**
   - Evidence type: Consistency validation
   - Evidence format: Doc Impact Scan performed
   - Acceptable: Consistency check pass, manual review approval

4. **No contradictions between intent/rules/runtime**
   - Evidence type: Consistency validation + manual review
   - Evidence format: Cross-document consistency check
   - Acceptable: No conflicts found, or conflicts resolved with decision record

**Alignment with success criteria:**
- Each success criterion has corresponding evidence
- Evidence demonstrates criterion is met
- Gaps are explicitly documented (TBD or unverified)

---

## 6) Pass/Fail Semantics and Blocking Conditions

### 6.1 Pass Criteria

Validation **passes** when:

1. All required checks execute successfully
2. Evidence is complete (or gaps are explicitly documented)
3. No contradictions detected
4. All errors are resolved (warnings acceptable with review)

### 6.2 Fail Criteria

Validation **fails** when:

1. Required checks do not execute or return errors
2. Evidence is missing and not documented as TBD
3. Contradictions detected and not resolved
4. Errors present that violate specifications or standards

### 6.3 Blocking Conditions

Validation failures MUST block progression in the following cases:

#### Structure Validation Failures
- **Block:** File acceptance
- **Rationale:** Invalid structure prevents downstream processing
- **Remediation:** Fix structure per specification, re-validate

#### Conformance Validation Failures
- **Block:** Step approval
- **Rationale:** Non-conforming artifacts break automation
- **Remediation:** Fix conformance issues per specification, re-validate

#### Consistency Validation Failures
- **Block:** Merging
- **Rationale:** Contradictions create confusion and "double truth"
- **Remediation:** Resolve contradictions, update documents, re-validate

#### Runtime Validation Failures
- **Block:** Step 5 approval, deployment
- **Rationale:** Failed tests indicate implementation does not meet specification
- **Remediation:** Fix implementation, re-run tests, re-validate

#### Manual Review Rejection
- **Block:** Approval
- **Rationale:** Human reviewers have authority over progression
- **Remediation:** Address reviewer concerns, request re-review

### 6.4 Non-Blocking Conditions

Validation results MAY be informational (warnings) and not block progression when:

1. **Minor formatting issues** that do not affect meaning (subject to reviewer judgment)
2. **Best practice suggestions** that are not normative requirements
3. **Recommendations** for improvement that are not mandatory
4. **Informational notices** about system state

**Rule:** Warnings SHOULD be addressed but MAY be waived with reviewer approval.

### 6.5 Remediation Expectations

When validation fails, the following remediation is expected:

#### Fix and Re-Validate (Standard Path)
1. Identify root cause of failure
2. Fix the issue per relevant specification
3. Re-run validation
4. Confirm pass before proceeding

#### Escalate for Decision (Governance Path)
When validation failure indicates:
- A specification is incorrect or unclear
- A requirement conflicts with another requirement
- A breaking change is needed to fix the issue

Then:
1. Stop work
2. Create issue or decision record documenting the conflict
3. Propose resolution options
4. Obtain human decision
5. Apply approved resolution
6. Re-validate

#### Document Exception (Rare Path)
When validation failure is legitimate but cannot be fixed (e.g., legacy system constraint):
1. Document why validation cannot pass
2. Document risk and impact
3. Obtain explicit approval with documented rationale
4. Record exception in decision record
5. Proceed with approval

**Rule:** Exceptions MUST be rare and MUST have explicit approval.

---

## 7) Evidence Formats and Storage

### 7.1 Acceptable Evidence Formats

Evidence MUST be in one of the following formats:

#### Structured Formats (Preferred)
- **JSON:** Validation reports, run receipts, test results
- **YAML:** Configuration, manifests
- **XML:** Test results (JUnit XML)
- **TAP:** Test results (Test Anything Protocol)

#### Text Formats (Acceptable)
- **Plain text:** Logs, validation output
- **Markdown:** Documentation, decision records
- **Diff:** Code changes, documentation changes

#### Binary Formats (When Necessary)
- **Screenshots (PNG, JPEG):** UI validation
- **Recordings (video):** Behavior demonstration
- **Archives (ZIP, TAR):** Artifact bundles

### 7.2 Evidence Requirements

All evidence MUST satisfy:

1. **Deterministic:** Same inputs produce same outputs
2. **Reproducible:** Others can verify given same inputs and context
3. **Reviewable:** Human-readable or machine-parseable
4. **Referenced explicitly:** Linked from approval records, PRs, or decision records

Evidence SHOULD satisfy:
- **Timestamped:** Include when evidence was produced
- **Attributed:** Include who/what produced the evidence
- **Versioned:** Include version of code/docs being validated

### 7.3 Evidence Storage

Evidence MUST be stored in one of the following locations:

#### CI Artifacts (Preferred for Automated Evidence)
- Location: GitHub Actions artifacts, CI build outputs
- Retention: Per CI platform policy (typically 90 days minimum)
- Access: Via CI platform UI or API

#### PR Comments (For Review Evidence)
- Location: GitHub PR comments
- Retention: Permanent (as long as PR exists)
- Access: Via GitHub PR UI

#### Git Repository (For Persistent Evidence)
- Location: Committed files in repository
- Retention: Permanent (git history)
- Access: Via git
- Examples: Decision records, approval documents

#### External Storage (When Required)
- Location: S3 buckets, artifact repositories
- Retention: Per retention policy
- Access: Via appropriate credentials
- Usage: Large artifacts, long-term retention

### 7.4 Evidence Lifecycle

Evidence retention:

- **Short-term evidence** (build logs, test results): Retained for CI platform default (typically 90 days)
- **Long-term evidence** (decision records, approval records): Retained permanently in git
- **Temporary evidence** (draft validation runs): Retained until work is merged or abandoned

Evidence MAY be discarded when:
- Work is abandoned (feature branch deleted)
- Retention period expires (for short-term evidence)
- Evidence is superseded by newer evidence for the same thing

Evidence MUST NOT be discarded when:
- Evidence supports an active approval
- Evidence documents a breaking change
- Evidence is referenced from a decision record
- Evidence is referenced from governance documents

### 7.5 Evidence References

When referencing evidence:

**MUST include:**
- Description of what the evidence demonstrates
- Location of evidence (file path, URL, CI run ID)

**SHOULD include:**
- Timestamp when evidence was produced
- Version of system being validated
- Who produced the evidence (human or tool)

**Example references:**

```markdown
Conformance validated via `validate_repo_docs.py` run on 2026-02-02 (see CI run #1234)

Test results show all 47 unit tests passing (see test_results.xml in CI artifacts)

Manual review approval by @reviewer on 2026-02-02 (PR #456, comment #789)

Breaking change documented in decision record DR-0042
```

---

## 8) Relationship to Other Governance Artifacts

### 8.1 Approval Gates (Target Agent System)

Validation **provides evidence for** approval gates defined in `docs/context/target_agent_system.md`.

**Relationship:**
- Approval gates require evidence (this standard defines what evidence is required)
- Validation produces evidence (validation reports, test results)
- Human approval interprets evidence (tools inform, humans decide)

**Reference:** `docs/context/target_agent_system.md` Section "Approval Gates and Evidence Discipline"

### 8.2 Evidence Discipline (Target Agent System)

Validation **operationalizes** evidence discipline defined in `docs/context/target_agent_system.md`.

**Relationship:**
- Evidence discipline defines principles (evidence must be deterministic, reviewable)
- Validation standard defines rules (what evidence is required, what formats are acceptable)
- Validation tools enforce rules (automated validation checks)

**Reference:** `docs/context/target_agent_system.md` Section "Evidence Discipline"

### 8.3 Decision Records (Decision Records Standard)

Validation failures MAY trigger decision record creation when:
- Validation failure indicates a specification is incorrect
- Validation failure indicates conflicting requirements
- Validation failure requires a breaking change to resolve
- Validation exception is needed (rare)

**Relationship:**
- Decision records document governance decisions
- Validation failures may surface the need for governance decisions
- Decision records may define validation exceptions

**Reference:** `docs/standards/decision_records_standard.md`

### 8.4 Breaking Changes (Naming Standard, Artifact Catalog Spec)

Breaking changes REQUIRE additional validation:
- Decision record created (per breaking change rules)
- Migration plan validated (if required)
- Deprecation period documented (if required)
- All affected documentation updated
- Comprehensive validation performed (all applicable types)

**Relationship:**
- Breaking change rules define when changes are breaking
- Validation standard defines what evidence is required for breaking changes
- Validation tools check breaking change compliance

**References:**
- `docs/standards/naming_standard.md` Section 5 (Breaking Changes)
- `docs/standards/artifacts_catalog_spec.md` Section 6.5 (Breaking Changes)

### 8.5 Workflow Guide (5-Step Execution)

Validation checkpoints in the 5-step workflow:
- Step 1: Manual review (objective approval)
- Step 2: Manual review (pipeline approval)
- Step 3: Conformance + manual review (capability plan approval)
- Step 4: Structure + conformance + runtime (implementation validation)
- Step 5: All applicable types (comprehensive validation)

**Relationship:**
- Workflow guide defines execution procedures
- Validation standard defines what evidence is required at each step
- Workflow guide references validation standard for evidence expectations

**Reference:** `docs/process/workflow_guide.md` Section 6 (Validate, Test, and Document)

---

## 9) Validation Tools and References (Non-Normative)

**Note:** This section is non-normative. For detailed tool documentation, see `docs/ops/tooling_reference.md` and `docs/ops/ci_automation_reference.md`.

### 9.1 Validation Tool Overview

The following validation tools exist in this repository:

#### Repository Documentation Validator
- **Location:** `tools/validate_repo_docs.py`
- **Purpose:** Validates documentation and manifest files against specifications
- **Validation types:** Structure validation, conformance validation
- **Usage:** See `docs/ops/tooling_reference.md`

#### CI Validation Workflow
- **Location:** `.github/workflows/validate_standards.yml`
- **Purpose:** Automated validation on PRs
- **Validation types:** Structure validation, conformance validation
- **Usage:** See `docs/ops/ci_automation_reference.md`

### 9.2 How Tools Relate to Validation Categories

| Validation Category | Tools |
|---------------------|-------|
| Structure Validation | `validate_repo_docs.py`, Markdown linters, YAML linters |
| Conformance Validation | `validate_repo_docs.py`, schema validators, manifest validators |
| Consistency Validation | Cross-reference checkers, manual review |
| Runtime Validation | Test frameworks (pytest, unittest), CI builds |
| Manual Review Validation | PR review process, human reviewers |

### 9.3 Tool Documentation Location

**For tool command syntax, parameters, and troubleshooting:**
- See `docs/ops/tooling_reference.md`
- See `docs/ops/ci_automation_reference.md`

**This standard does NOT duplicate tool documentation.**

---

## 10) Examples (Non-Normative)

**Note:** These examples are non-normative illustrations. They demonstrate validation and evidence concepts but are not requirements.

### 10.1 Example: Validation Evidence for Simple Code Change

**Scenario:** Developer implements a new helper function in `glue_script.py`.

**Validation evidence required:**

1. **Runtime validation:**
   - Evidence: Unit tests pass (8/8 tests passing)
   - Location: CI run #1234, test results in artifacts
   - Format: JUnit XML

2. **Structure validation:**
   - Evidence: Build succeeds
   - Location: CI build logs
   - Format: Text logs

3. **Manual review:**
   - Evidence: PR approval by code reviewer
   - Location: PR #456, approval by @reviewer
   - Format: GitHub approval record

**Approval decision:**
- Human reviewer reviews evidence
- Confirms tests cover new function
- Approves and merges PR

### 10.2 Example: Validation Evidence for Breaking Change

**Scenario:** Developer renames a job ID from `oldJobId` to `new_job_id` (breaking change per naming standard).

**Validation evidence required:**

1. **Decision record:**
   - Evidence: Decision record DR-0042 created
   - Location: `docs/decisions/DR-0042-rename-old-job-id.md`
   - Format: Markdown (per decision records standard)
   - Content: Rationale, migration plan, deprecation period

2. **Conformance validation:**
   - Evidence: Job manifest conforms to new naming standard
   - Location: CI validation report
   - Format: JSON validation report

3. **Consistency validation:**
   - Evidence: All references updated (artifacts catalog, job inventory, documentation)
   - Location: Manual review, cross-reference check
   - Format: Review comments, consistency check report

4. **Migration validation:**
   - Evidence: Migration steps documented and tested
   - Location: Decision record, migration guide
   - Format: Markdown documentation

5. **Manual review:**
   - Evidence: PR approval by maintainer with governance authority
   - Location: PR #789, approval by @maintainer
   - Format: GitHub approval record

**Approval decision:**
- Human reviewer reviews decision record
- Confirms migration plan is complete
- Confirms all references updated
- Approves and merges PR

---

## 11) Open Items / TBD

This section lists items that could not be fully grounded in existing documentation, along with assumptions, uncertainties, and questions requiring human decision.

### Resolved Items

The following items have been resolved per governance decision:

**11.1 - Validation Tool Requirements (RESOLVED - Option 1):**
- **Decision:** Accept current level of detail. Tools implement validation categories as defined.
- **Rationale:** Validation categories are well-defined; specific tool implementations can vary. Tool details belong in ops layer, not standards layer.

**11.2 - Performance Validation Standards (RESOLVED - Option 2):**
- **Decision:** Performance validation is optional unless specified in acceptance criteria.
- **Rationale:** Performance standards can be added later if needed. Acceptance criteria govern validation requirements on a per-case basis.

**11.3 - Security Validation Requirements (RESOLVED - Option 2):**
- **Decision:** Security checks are part of runtime validation with tool-specific requirements.
- **Rationale:** Security validation is part of runtime validation; specific tools and checks can be defined in ops layer as needed.

**11.4 - Validation Frequency for Long-Running Work (RESOLVED - Option 2):**
- **Decision:** Validation frequency is left to developer judgment with PR validation as gate.
- **Rationale:** CI validation at PR time is sufficient gate; additional validation during development is encouraged but not required. Continuous validation during development is developer choice.

### Agreed Assumptions

The following assumptions are agreed and finalized:

**11.5 - Test Coverage Requirements (AGREED):**
- **Assumption:** This standard does not define minimum test coverage requirements (e.g., "80% line coverage").
- **Rationale:** Coverage requirements are project-specific and may vary by component. Tests are required; coverage is a quality metric that can be defined separately if needed.
- **Impact:** Low. If coverage requirements are needed, they can be defined in separate testing standards document or per-job requirements.

---

## 12) Consistency Check Appendix

This appendix documents alignment with existing documentation and identifies any potential conflicts or assumptions.

### 12.1 Documents Aligned With

This standard is aligned with:

1. **`docs/context/development_approach.md`**
   - Validation against success criteria (Section "Core Principles")
   - 5-step workflow (Section "Sequential Development Process")

2. **`docs/context/target_agent_system.md`**
   - Evidence discipline (Section "Approval Gates and Evidence Discipline")
   - No hidden authority (Section "Non-Negotiable Operating Rules")
   - Approval gates (Section "Non-Negotiable Operating Rules")

3. **`docs/context/glossary.md`**
   - Definitions of "verified", "evidence", "validation"
   - No terms redefined

4. **`docs/standards/documentation_spec.md`**
   - Evidence-based claims (Section 1.3)
   - Explicit over implicit (Section 1.4)

5. **`docs/process/workflow_guide.md`**
   - Validation checkpoints in 5-step workflow
   - Doc Impact Scan (Section 6)

6. **`docs/standards/naming_standard.md`**
   - Breaking change rules (Section 5)

7. **`docs/standards/artifacts_catalog_spec.md`**
   - Breaking change rules (Section 6.5)

8. **`docs/standards/codable_task_spec.md`**
   - Task structure requirements (used in Step 3 validation)

9. **`docs/ops/tooling_reference.md`**
   - Tool locations and purposes (referenced, not duplicated)

10. **`docs/ops/ci_automation_reference.md`**
    - CI validation overview (referenced, not duplicated)

### 12.2 Potential Conflicts Detected

**None detected.**

This standard:
- Does not redefine any glossary terms
- Does not duplicate schemas from other standards
- Does not contain tool command syntax (properly references ops layer)
- Does not contain workflow procedures (properly references workflow guide)
- Maintains proper layer separation (standards layer, not context or ops)

### 12.3 Resolved Decisions and Agreed Assumptions

See Section 11 (Open Items / TBD) for detailed status.

**Resolved decisions (Section 11 "Resolved Items"):**
1. Validation tools implement validation categories as defined (governance decision - option 1)
2. Performance validation is optional unless specified in acceptance criteria (governance decision - option 2)
3. Security validation is part of runtime validation with tool-specific requirements (governance decision - option 2)
4. Validation frequency for long-running work left to developer judgment with PR validation as gate (governance decision - option 2)

**Agreed assumptions (Section 11 "Agreed Assumptions"):**
5. Test coverage requirements not defined in this standard (project-specific, can be added later if needed)

**Impact:** Low. All decisions and assumptions are bounded and have minimal impact on validation effectiveness.

**Status:** All open items from initial draft have been resolved or agreed. This standard is complete.

### 12.4 Cross-Document Impact

Changes to the following documents MAY require updates to this standard:

- **`docs/context/target_agent_system.md`** - If evidence discipline rules change
- **`docs/context/development_approach.md`** - If workflow steps change
- **`docs/process/workflow_guide.md`** - If approval gate procedures change
- **`docs/standards/*_spec.md`** - If new specifications are added requiring validation

This standard DOES NOT create new requirements for those documents.

### 12.5 Migration Notes

**Existing `docs/standards/validation_standard.md`:**
- Current file is incomplete and focused on tool usage
- This new version is comprehensive and standards-focused
- Tool usage content properly moved to ops layer (referenced, not duplicated)
- No breaking changes to validation tool behavior
- No breaking changes to validation requirements (codifies existing practices)

**Backward compatibility:**
- All existing validation practices remain valid
- Existing validation tools continue to work
- Additional validation categories provide structure, do not change tools

---

**End of Validation Standard**

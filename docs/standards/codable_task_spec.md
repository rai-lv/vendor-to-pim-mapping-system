# Codable Task Specification

## Purpose statement

This standard defines the normative structure for individuable codable tasks used to control implementation work during Step 3→4 execution. It ensures that tasks remain bounded, traceable, reviewable, and aligned with the repository's evidence and approval discipline.

**Canonical location:** `docs/standards/codable_task_spec.md`

**Related standards:**
- `docs/context/development_approach.md` — 5-step workflow and approval discipline
- `docs/context/target_agent_system.md` — agent responsibilities, evidence discipline, conflict handling
- `docs/process/workflow_guide.md` — Step 3 (capability planning) and Step 4 (implementation) procedures
- `docs/standards/documentation_spec.md` — documentation structure and formatting rules
- `docs/standards/validation_standard.md` — validation rules and evidence expectations
- `docs/standards/naming_standard.md` — naming conventions and identifier rules

**Last major review:** 2026-01-30

---

## 0) Scope and purpose

### What problem this standard solves

In the Step 3→4 transition (from capability planning to implementation), work must be decomposed into units that are:
- small enough to be understood and implemented independently,
- large enough to be coherent and meaningful,
- bounded enough to prevent scope creep and silent assumptions,
- detailed enough to implement without embedding full solutions.

Without a normative structure, codable tasks risk becoming either too vague ("implement everything") or overly prescriptive (embedding full code solutions), undermining the approval gate between planning and implementation.

This standard defines what a codable task specification is, what it must contain, and how it supports the evidence and approval discipline required for controlled execution.

### What a codable task specification is

A **codable task specification** is a structured description of a bounded unit of implementation work that:
- can be understood and implemented independently (given its stated dependencies),
- has clear boundaries (what it does and does NOT do),
- produces verifiable outcomes that can be evaluated against acceptance criteria,
- maintains traceability from capability plan to implementation artifact.

Codable task specifications are created during **Step 3 (Capability Planning)** as part of the capability decomposition process and executed during **Step 4 (Execute Development Tasks)**.

### What a codable task specification is NOT

A codable task specification is NOT:
- A high-level capability definition (capabilities contain multiple tasks)
- A full implementation or code solution (those are produced by executing tasks)
- An operational procedure or "how-to" guide (those belong in ops documentation)
- A business requirement or rationale document (those belong in capability plans or business descriptions)
- A normative schema or standard (those belong in standards documents)
- A tool command reference or CLI manual (those belong in ops documentation)

### Position in the 5-step workflow

Codable tasks are positioned at the **Step 3→4 boundary**:

1. **Step 3 (Capability Planning):** Capabilities are decomposed into codable tasks with clear boundaries, dependencies, and acceptance criteria. Tasks are approved before implementation begins.

2. **Step 4 (Execute Development Tasks):** Each approved task is implemented, producing changes that are traceable to the task specification. Implementation must not expand scope beyond approved task boundaries.

**Approval gate:** Human approval of the codable task breakdown is required before proceeding to Step 4 implementation.

**Reference:** See `docs/process/workflow_guide.md` Sections 4 (Step 3) and 5 (Step 4) for execution procedures.

---

## 1) Definition of "codable task"

### Core definition

A **codable task** is a bounded unit of implementation work derived from an approved capability definition, characterized by:

- **Individuability:** The task can be understood and implemented independently, given its stated dependencies and inputs.
- **Boundedness:** The task has explicit boundaries that define what it does and what it explicitly does NOT do.
- **Traceability:** The task's outcomes can be verified against stated acceptance criteria using deterministic evidence.
- **Reviewability:** Another developer can understand the intent and validate that the implementation satisfies the task specification.

### Key characteristics

#### 1.1 Individuable

A task is individuable when:
- It can be assigned to a single implementer without requiring coordination during implementation (coordination may be needed for integration).
- Its purpose, boundaries, dependencies, and acceptance criteria are sufficient to guide implementation.
- It does not depend on undocumented assumptions or implicit knowledge.

#### 1.2 Bounded

A task is bounded when:
- It has an explicit purpose statement describing what it achieves.
- It has an explicit boundary statement describing what it does NOT do.
- Its scope cannot expand silently during implementation without triggering escalation.

#### 1.3 Traceable

A task is traceable when:
- It references the capability it is part of.
- Its intended outputs are explicitly stated.
- Its acceptance criteria can be evaluated using deterministic evidence.
- Changes produced by implementing the task can be linked back to the task specification.

#### 1.4 Reviewable

A task is reviewable when:
- Its specification is documented in a form that can be read and understood by someone other than the original author.
- Its acceptance criteria provide clear pass/fail conditions.
- Its implementation can be validated against the specification without requiring the implementer to explain undocumented decisions.

### Distinction from related concepts

| Concept | How it differs from a codable task |
|---------|-----------------------------------|
| **Capability** | A capability is a higher-level building block that describes what the system must do to achieve an objective. A capability typically contains multiple codable tasks. |
| **Implementation artifact** | Implementation artifacts (code, tests, documentation) are the outputs produced by executing a codable task. The task specification describes what should be produced; the artifacts are the actual result. |
| **Operational procedure** | Operational procedures describe how to run, troubleshoot, or maintain implemented systems. Codable tasks describe what to implement, not how to operate the result. |
| **Business requirement** | Business requirements describe business purpose, rationale, and high-level needs. Codable tasks describe bounded implementation work derived from those requirements. |

---

## 2) Required structure for task specifications

Every codable task specification MUST contain the following sections. The level of detail should be "sufficient to implement" without being "a full solution."

### 2.1 Task identity (MUST)

**Purpose:** Uniquely identifies the task for tracking and traceability.

**Required fields:**

| Field | Description | Format |
|-------|-------------|--------|
| **Task identifier** | Unique name or ID for this task within the capability | Short descriptive phrase or ID (e.g., "Task 1: Validate input schema", "implement_xml_parser") |
| **Parent capability** | Reference to the capability this task is part of | Capability name or identifier with document reference if available |

**Example:**
```
Task identifier: Task 1: Implement XML validation
Parent capability: "Process incoming BMEcat files" (see capability_plan_001.md)
```

**Note:** Task naming conventions follow `docs/standards/naming_standard.md` where applicable. If no specific naming convention is defined for task identifiers in the naming standard, use clear descriptive phrases that indicate the work to be done.

### 2.2 Task purpose (MUST)

**Purpose:** States what the task aims to achieve in 1-3 sentences.

**Requirements:**
- Clear statement of the intended outcome
- Focus on what will exist or change after task completion
- No business justification or rationale (that belongs in the capability plan)

**Format:** 1-3 sentences.

**Example (compliant):**
> "Implement XML schema validation for incoming BMEcat files. The validation function will check structure and required fields, raising exceptions for invalid input. Validation results will be logged for observability."

**Example (non-compliant):**
> "Support the vendor integration strategy by adding validation." ❌ (too vague, business justification mixed in)

### 2.3 Task boundaries (MUST)

**Purpose:** Explicitly states what the task does and does NOT do.

**Requirements:**
- At least one explicit "does NOT" statement or equivalent boundary marker
- Boundaries must be specific enough to prevent scope creep
- May reference adjacent tasks to clarify boundaries

**Format:** Bullet list or prose with clear boundary markers.

**Example:**
```
**In scope:**
- Validate XML structure against BMEcat schema
- Check presence of required fields (article_id, description, price)
- Raise exceptions for validation failures

**Out of scope (does NOT):**
- Parse or transform XML content (handled by Task 2)
- Write validation results to S3 (handled by Task 4)
- Implement retry logic (handled by orchestration layer)
```

### 2.4 Dependencies (MUST)

**Purpose:** States what must exist or be completed before this task can be executed.

**Required subfields:**

| Subfield | Description | Format |
|----------|-------------|--------|
| **Prerequisite tasks** | Tasks that must be completed first | List of task identifiers or `NONE` |
| **Required inputs** | Inputs that must exist before implementation | List of inputs or `NONE` |
| **External dependencies** | Dependencies on systems, libraries, or decisions outside this capability | List or `NONE` |

**Example:**
```
**Prerequisite tasks:** NONE (first task in capability)

**Required inputs:**
- BMEcat XML schema definition (schema file location TBD, escalate if not available)
- Example valid/invalid BMEcat files for testing

**External dependencies:**
- Python `lxml` library available in Glue runtime (verify version compatibility)
```

**Note:** If a dependency is unknown or uncertain, use `TBD` and mark as escalation trigger. Proceeding with unapproved assumptions about dependencies is not permitted.

### 2.5 Intended outputs (MUST)

**Purpose:** Describes what artifacts, changes, or states result from completing this task.

**Requirements:**
- List concrete outputs (files, functions, tests, documentation)
- Specify form/location where deterministic (e.g., "function in `validation.py`")
- Use `TBD` for unknowns that do not block understanding the task scope

**Format:** Bullet list.

**Example:**
```
**Intended outputs:**
- New function `validate_bmecat_xml(xml_string) -> ValidationResult` in `jobs/vendor_input_processing/preprocessIncomingBmecat/validation.py`
- Unit tests for validation function in `tests/unit/test_validation.py`
- Error messages added to `exceptions.py` for validation failure cases
- Validation behavior documented in script card Section 2.4
```

### 2.6 Acceptance criteria (MUST)

**Purpose:** Defines how to verify the task is complete.

**Requirements:**
- Criteria must be evaluable (checkable by someone other than the implementer)
- Each criterion should have a clear pass/fail condition
- Criteria must not require subjective judgment where objective evidence is possible
- At least 2-3 criteria per task (if task has only 1 criterion, consider if task is too small)

**Format:** Numbered or bulleted list of criteria.

**Example:**
```
**Acceptance criteria:**
1. `validate_bmecat_xml()` function exists and can be imported from `validation.py`
2. Function correctly identifies valid BMEcat XML (test with 3+ valid examples)
3. Function correctly rejects invalid BMEcat XML (test with 3+ invalid examples covering: missing required fields, malformed XML, schema violations)
4. Unit tests pass with 100% coverage of validation logic
5. ValidationResult object contains structured error details (field name, error type, message)
6. Script card Section 2.4 documents validation behavior and failure modes
```

**Evidence expectations:** See Section 4 for how acceptance criteria relate to validation and evidence.

### 2.7 Unknowns and assumptions (MUST if present, MAY be NONE)

**Purpose:** Explicitly surfaces uncertainties and controlled assumptions.

**Requirements:**
- Use `NONE` if no unknowns or assumptions exist
- If unknowns exist, list them explicitly with impact statement
- If assumptions are required, state what is assumed, why, and impact
- All assumptions MUST be approved before implementation proceeds

**Format:** Bullet list or statement of `NONE`.

**Example:**
```
**Unknowns:**
- BMEcat schema version: input files may use v1.2 or v2005. Impact: validation logic must handle version detection or fail explicitly. Resolution: Escalate to capability owner.

**Assumptions:**
- XML encoding is UTF-8 (approved: capability review 2026-01-25). Impact: Non-UTF-8 files will fail validation. Mitigation: Document encoding requirement in validation error messages.
```

**Escalation rule:** If implementing a task requires introducing new assumptions not approved during Step 3, implementation must stop and escalate per `docs/process/workflow_guide.md` Section 5.

---

## 3) Task granularity and decomposition guidance

### 3.1 Appropriate task size

A well-sized task is:
- **Large enough** to be a coherent unit of work (not a single line change)
- **Small enough** to be completed in a single focused session (hours to 1-2 days, not weeks)
- **Bounded enough** that scope cannot expand silently

#### Too coarse (anti-pattern):
> "Task 1: Implement all BMEcat processing logic"

**Problem:** No clear boundaries, too many unknowns, cannot be reviewed as a unit.

#### Too fine (anti-pattern):
> "Task 1: Import lxml library"  
> "Task 2: Define ValidationResult class"  
> "Task 3: Write first unit test"

**Problem:** Excessive decomposition creates coordination overhead without adding clarity.

#### Appropriate (example):
> "Task 1: Implement XML validation function"  
> "Task 2: Parse XML and extract product data"  
> "Task 3: Transform product data to normalized format"  
> "Task 4: Write output to S3"

**Rationale:** Each task is a logical unit that can be implemented, tested, and reviewed independently, with clear boundaries between tasks.

### 3.2 When to split a task

Split a task when:
- It has multiple distinct outputs that could be implemented separately
- It crosses architectural boundaries (e.g., validation + transformation + storage)
- Dependencies are such that one part could be implemented/tested while another is blocked
- Acceptance criteria cannot be cleanly grouped (more than 5-7 criteria may indicate multiple logical tasks)

### 3.3 When to keep tasks unified

Keep a task unified when:
- Splitting would create artificial boundaries that make implementation harder
- The outputs are tightly coupled and must be implemented together
- Testing/validation requires the unified implementation
- Splitting would require complex coordination that adds no value

### 3.4 Maintaining task cohesion

Tasks should be **logically coherent**: all work in a task should contribute to the same focused outcome.

**Coherent (good):**
> "Task: Implement error handling and logging for XML validation"

**Incoherent (bad):**
> "Task: Implement XML validation and write job manifest documentation"

**Reason:** Error handling/logging are directly related to validation (coherent). Documentation is a separate concern that belongs in a different task or Step 5 activity.

### 3.5 Handling task dependencies and ordering

**Dependency types:**
- **Sequential:** Task B requires outputs from Task A (must be explicitly stated)
- **Parallel:** Tasks can be executed concurrently (no prerequisite relationship)
- **Optional ordering:** Tasks could be done in either order but one is recommended

**Representation:**
- Sequential dependencies MUST be stated in the "Dependencies" section of the dependent task
- Parallel tasks MUST NOT have circular dependencies
- Optional ordering MAY be noted in task purpose or boundaries for guidance

**Example:**
```
Task 1: Define data model classes (no prerequisites)
Task 2: Implement validation (no prerequisites, can run parallel to Task 1)
Task 3: Implement transformation (depends on Task 1 for data models)
Task 4: Implement output writer (depends on Task 3 for transformed data)
```

---

## 4) Evidence and validation expectations

### 4.1 Task completion evidence

**Principle:** A task is complete only when acceptance criteria are met and evidence supports that claim.

**Evidence types:**
- **Code artifacts:** Committed code matching intended outputs
- **Test results:** Passing tests that validate acceptance criteria
- **Documentation updates:** Updated script cards, business descriptions, or other docs as specified in intended outputs
- **Run receipts / logs:** For tasks that involve operational changes
- **Review approval:** Human confirmation that acceptance criteria are satisfied

**Reference:** See `docs/standards/validation_standard.md` for detailed evidence rules and validation procedures.

### 4.2 Structuring acceptance criteria for verification

Acceptance criteria SHOULD be structured so that:
- Each criterion maps to a verifiable evidence type
- Pass/fail is deterministic (not subjective)
- Evidence can be produced independently (someone other than implementer can verify)

**Example:**

| Acceptance Criterion | Evidence Type | Verification Method |
|---------------------|---------------|---------------------|
| Function exists and is importable | Code artifact | Import test passes |
| Correctly validates valid XML | Test results | Unit tests with valid examples pass |
| Correctly rejects invalid XML | Test results | Unit tests with invalid examples pass |
| 100% code coverage for validation logic | Test results | Coverage report shows 100% |
| Behavior documented in script card | Documentation update | Script card Section 2.4 exists and contains validation behavior |

### 4.3 Handling tasks with non-deterministic evidence

Some tasks may not have immediately deterministic evidence (e.g., "research approach for X", "design API contract").

**Handling:**
- Acceptance criteria should still be evaluable (e.g., "API design document exists and covers endpoints, request/response formats, error codes")
- Evidence is the artifact produced (e.g., design document)
- Human review confirms completeness against criteria

**Escalation:** If acceptance criteria cannot be made evaluable, escalate during Step 3 for human decision on how to structure the task.

### 4.4 Relationship to validation standard

This specification defines task-level acceptance criteria. The validation standard (`docs/standards/validation_standard.md`) defines:
- What "verified/confirmed" means
- How to interpret validation tool outputs
- When evidence is sufficient for approval

**Boundary:** Codable task specs define WHAT evidence is expected for a specific task. Validation standard defines HOW evidence is evaluated and WHEN it's sufficient.

---

## 5) Unknowns and assumptions discipline

### 5.1 Handling unknowns discovered during task specification

**When unknowns are discovered:**
1. **List them explicitly** in the task's "Unknowns and assumptions" section
2. **Assess impact:** Does the unknown block understanding the task scope?
3. **Decide resolution path:**
   - If impact is low and task can proceed: Mark as `TBD` with impact statement, proceed
   - If impact is medium: Mark as `TBD`, flag for resolution before Step 4 begins
   - If impact is high: Escalate immediately, do not approve task until resolved

**Example - low impact:**
> "Unknown: Exact S3 bucket prefix for outputs (TBD, to be provided by ops). Impact: Low, implementation can use placeholder, will be resolved before deployment."

**Example - high impact:**
> "Unknown: Which XML schema version to validate against. Impact: High, affects validation logic design and error handling. Escalate to capability owner before implementation begins."

### 5.2 When assumptions are permitted

Assumptions are allowed in codable task specifications ONLY when:
- The assumption is explicitly labeled
- The assumption is bounded (what is assumed, why, impact clearly stated)
- The assumption is approved by a human before task implementation begins
- The assumption does not conflict with approved intent from earlier steps

**Example - controlled assumption:**
```
**Assumption:** Input XML files are well-formed (no malformed XML syntax).
**Rationale:** Upstream system guarantees well-formed XML via pre-validation.
**Impact:** Parser will raise exceptions for malformed XML without graceful handling.
**Approved:** Capability review 2026-01-25.
**Mitigation:** Document assumption in script card; add monitoring for XML parse failures.
```

### 5.3 Escalation conditions

**MUST escalate (stop and surface) when:**
- Implementing the task would require new assumptions not approved during Step 3
- Unknowns discovered during implementation change the task boundaries or acceptance criteria
- Evidence contradicts assumptions made during task specification
- Task scope would need to expand to handle discovered requirements

**MUST NOT:**
- Proceed with unapproved assumptions
- Silently expand scope to handle discovered requirements
- Rationalize away contradictions between specification and implementation

**Reference:** See `docs/context/target_agent_system.md` Section 3 (Non-Negotiable Operating Rules) for assumption and escalation discipline.

---

## 6) Anti-patterns and prohibited content

The following patterns are explicitly prohibited in codable task specifications:

### 6.1 Full implementation code or detailed algorithms

**Prohibited:**
```
Task: Implement XML parser

Acceptance criteria:
1. Use lxml.etree.parse() with error handling
2. Extract elements with xpath expressions: //PRODUCT/ARTICLE_ID
3. Create Product objects: Product(article_id=..., name=...)
4. Return list of Products
```

**Problem:** This is a full implementation, not a task specification. It constrains implementation decisions that should be made during Step 4.

**Correct approach:**
```
Task: Implement XML parser

Purpose: Parse BMEcat XML and extract product data into structured objects.

Acceptance criteria:
1. Parser function accepts XML string and returns list of Product objects
2. Product objects contain: article_id, name, description, price (fields from capability plan)
3. Parser handles XML parsing errors gracefully (raises appropriate exceptions)
4. Unit tests validate parsing of valid and invalid XML
```

### 6.2 Tool command syntax or CLI instructions

**Prohibited:**
```
Task: Deploy validation function

Dependencies:
- Run `aws s3 cp validation.py s3://bucket/prefix/`
- Execute `make deploy-glue-job JOB_NAME=preprocess`
```

**Problem:** Tool syntax belongs in ops documentation, not task specifications. Task specs describe WHAT to produce, not HOW to deploy it.

**Correct approach:**
```
Task: Integrate validation function into preprocessIncomingBmecat job

Intended outputs:
- validation.py integrated into job's glue_script.py
- Job manifest updated to reflect validation dependency
- Deployment verified in staging environment

Dependencies:
- Validation function implemented (Task 1)
- Staging environment available for deployment testing
```

### 6.3 Duplicated schemas, standards, or governance rules

**Prohibited:**
```
Task: Create job manifest

Acceptance criteria:
1. Manifest contains fields: job_id, runtime, inputs, outputs, parameters
2. job_id follows format: lowercase snake_case
3. runtime must be one of: pyspark, python_shell, python
...
```

**Problem:** This duplicates the job manifest spec. Task should reference the spec, not redefine it.

**Correct approach:**
```
Task: Create job manifest for preprocessIncomingBmecat

Purpose: Create machine-readable manifest per job_manifest_spec.md

Acceptance criteria:
1. Manifest file exists at jobs/vendor_input_processing/preprocessIncomingBmecat/job_manifest.yaml
2. Manifest conforms to schema in docs/standards/job_manifest_spec.md (validated by manifest validator tool)
3. Manifest declares inputs, outputs, parameters per capability plan
4. Manifest passes validation checks with zero errors
```

### 6.4 Operational procedures or troubleshooting guides

**Prohibited:**
```
Task: Add logging

Intended outputs:
- Logs written to CloudWatch
- To view logs: aws logs tail /aws-glue/jobs/output --follow
- If logs are missing, check IAM permissions on Glue role
```

**Problem:** Operational procedures and troubleshooting belong in ops documentation, not task specifications.

**Correct approach:**
```
Task: Implement structured logging for validation

Intended outputs:
- Logger configured to output structured JSON logs
- Log entries include: timestamp, level, job_id, validation_result, error_details (if failure)
- Logging behavior documented in script card Section 2.10 (Observability)

Acceptance criteria:
1. Validation success/failure logged at INFO level
2. Log entries contain all required fields (timestamp, level, job_id, validation_result)
3. Script card documents log format and observability expectations
```

### 6.5 Business justification or high-level capability rationale

**Prohibited:**
```
Task: Implement vendor integration logic

Purpose: Support our strategic goal of automating vendor data ingestion to reduce manual effort and improve time-to-market for new products.
```

**Problem:** Business rationale belongs in the capability plan or business description, not in task specifications.

**Correct approach:**
```
Task: Implement vendor integration logic

Purpose: Parse incoming vendor XML files and extract product data per capability plan Section 3.
```

### 6.6 Vague or unbounded tasks

**Prohibited:**
- "Task: Implement all processing logic"
- "Task: Handle edge cases"
- "Task: Add tests"
- "Task: Update documentation"

**Problem:** No clear boundaries, acceptance criteria cannot be evaluated, scope can expand silently.

**Correct approach:**
- "Task: Implement XML validation with schema checking and required field validation"
- "Task: Add unit tests for validation function covering valid/invalid XML cases"
- "Task: Update script card Section 2.4 to document validation behavior and failure modes"

---

## 7) Relationship to other documentation

Codable task specifications exist within a larger documentation ecosystem. Understanding these relationships prevents duplication and ensures proper boundaries.

### 7.1 Relationship to capability plans

**Capability plans** define:
- High-level capability purpose and boundaries
- Inputs and outputs at capability level
- Overall acceptance criteria for the capability
- The set of codable tasks that implement the capability

**Codable task specifications** define:
- Bounded units of work within the capability
- Task-specific boundaries, dependencies, acceptance criteria
- Intended outputs per task

**Boundary:** Capability plans describe WHAT the capability achieves. Task specifications describe HOW the capability is decomposed into implementable units.

**Traceability:** Each task MUST reference its parent capability. Capability plans SHOULD list the tasks that implement them.

### 7.2 Relationship to implementation artifacts

**Implementation artifacts** include:
- Code (functions, classes, modules)
- Tests (unit, integration, end-to-end)
- Configuration files
- Documentation updates

**Codable task specifications** define:
- What artifacts should be produced
- What acceptance criteria the artifacts must satisfy

**Boundary:** Task specifications describe WHAT to produce. Implementation artifacts ARE what gets produced.

**Traceability:** Implementation artifacts SHOULD be traceable to the tasks that specified them (e.g., via commit messages, PR descriptions, or explicit task references).

### 7.3 Relationship to operational documentation

**Operational documentation** (script cards, ops manuals) describes:
- How to run implemented jobs
- What observability signals exist
- How to troubleshoot failures

**Codable task specifications** MAY include:
- Tasks to create or update operational documentation
- Acceptance criteria that operational documentation exists

**Boundary:** Task specifications describe WHAT documentation to create. Operational documentation contains the actual HOW-TO content.

**Example:**
```
Task: Document validation behavior

Intended outputs:
- Script card Section 2.4 (Validation) updated with validation logic description
- Script card Section 2.9 (Failure modes) updated with validation failure conditions

Acceptance criteria:
1. Script card Section 2.4 exists and describes validation logic
2. Section 2.9 lists validation failure modes and error messages
```

### 7.4 Relationship to standards and governance

**Standards documents** define:
- Naming conventions
- Required schemas and fields
- Validation rules
- Breaking change policies

**Codable task specifications** MUST:
- Reference standards, not redefine them
- Ensure intended outputs comply with standards
- Include validation against standards in acceptance criteria

**Example:**
```
Task: Create artifact catalog entry

Purpose: Document the vendor_products_json artifact per artifacts_catalog_spec.md

Acceptance criteria:
1. Entry exists in docs/catalogs/artifacts_catalog.md
2. Entry conforms to schema in docs/standards/artifacts_catalog_spec.md Section 3
3. Entry passes validation by artifact catalog validator tool
```

### 7.5 Relationship to validation and evidence

**Validation standard** (`docs/standards/validation_standard.md`) defines:
- What "verified/confirmed" means
- How to evaluate evidence
- When evidence is sufficient for approval

**Codable task specifications** define:
- Task-specific acceptance criteria
- Expected evidence types for each criterion

**Boundary:** Task specs describe WHAT evidence is expected for this specific task. Validation standard describes HOW to evaluate evidence in general.

**Reference:** See Section 4 of this spec for evidence expectations at task level.

---

## 8) Examples (non-normative, illustrative only)

The following examples illustrate well-structured and poorly-structured task specifications. These are **NON-NORMATIVE** — they are for illustration only and do not constitute authoritative templates.

### Example 1: Well-structured task

```
Task identifier: Task 2: Parse XML and extract product data
Parent capability: "Process incoming BMEcat files" (capability_plan_bmecat_001.md)

Purpose:
Parse validated BMEcat XML files and extract product data into structured Product objects.

Boundaries:
**In scope:**
- Parse XML structure and navigate to product elements
- Extract required fields: article_id, name, description, price
- Create Product objects with extracted data
- Handle XML parsing errors

**Out of scope (does NOT):**
- Validate XML schema (handled by Task 1)
- Transform or normalize product data (handled by Task 3)
- Write output to S3 (handled by Task 4)

Dependencies:
**Prerequisite tasks:** Task 1 (XML validation) must be complete
**Required inputs:** Validated XML string (output from Task 1)
**External dependencies:** NONE

Intended outputs:
- Parser function `parse_bmecat_xml(xml_string) -> List[Product]` in `parser.py`
- Product dataclass definition in `models.py`
- Unit tests in `tests/unit/test_parser.py`

Acceptance criteria:
1. parse_bmecat_xml() function exists and returns List[Product]
2. Product objects contain required fields (article_id, name, description, price)
3. Function handles valid XML correctly (tested with 3+ examples)
4. Function raises appropriate exceptions for parsing errors
5. Unit tests achieve 100% coverage of parser logic
6. Parser behavior documented in script card Section 2.5

Unknowns and assumptions:
**Assumptions:**
- BMEcat XML follows standard structure (approved: capability review 2026-01-25)
- All product elements contain required fields (missing fields handled by validation in Task 1)
```

### Example 2: Common mistakes (anti-patterns)

#### Mistake 1: Too vague
```
Task: Implement processing logic

Purpose: Process vendor data

Acceptance criteria:
1. Logic works correctly
2. Tests pass
```
**Problem:** No boundaries, unclear outputs, subjective acceptance criteria.

#### Mistake 2: Full implementation embedded
```
Task: Implement parser

Purpose: Parse XML using lxml.etree.parse(), extract elements with xpath //PRODUCT, 
create Product objects with Product(id=elem.find('ARTICLE_ID').text, ...)

Acceptance criteria: Code matches the above implementation
```
**Problem:** This is an implementation, not a specification. Constrains implementation decisions.

#### Mistake 3: Duplicates standards
```
Task: Create manifest

Acceptance criteria:
1. Manifest has fields: job_id (lowercase snake_case), runtime (pyspark|python_shell|python), 
   inputs (list of dicts with bucket/key/format), outputs (list of dicts), parameters (list of dicts)...
```
**Problem:** Duplicates job_manifest_spec.md instead of referencing it.

---

## 9) Compatibility and evolution

### 9.1 When changes to this standard constitute breaking changes

Changes to this standard are considered breaking when:
- Required sections are added, removed, or renamed
- Required fields within sections are changed
- Validation rules for task specifications become more strict

**Non-breaking changes:**
- Adding optional sections or guidance
- Clarifying examples or wording
- Adding new anti-pattern examples

### 9.2 Handling evolution of task specifications

**For new capabilities:**
- Use the current version of this standard for all new task specifications
- Task specifications should be versioned or timestamped per `docs/standards/documentation_spec.md`

**For existing capabilities:**
- Task specifications created before standard updates are not required to retroactively conform
- If tasks are re-planned or significantly revised, use current standard version
- Include a note referencing the standard version used (e.g., "Conforms to codable_task_spec v1.0 dated 2026-01-30")

### 9.3 Versioning considerations

**Recommended approach:**
- Include "Last reviewed: YYYY-MM-DD" in capability plans that contain task breakdowns
- Reference this standard explicitly when creating task specifications
- If this standard undergoes major revision, update the "Last major review" date in the header

**Governance:**
- Changes to required sections or fields require explicit approval and decision record
- Changes must be reviewed for impact on in-progress capabilities
- Breaking changes require communication to all contributors

**Reference:** See `docs/standards/decision_records_standard.md` for governance decision recording.

---

## 10) Open items / TBD

This section lists items that could not be fully grounded in existing documentation and require human decision or additional evidence.

### 10.1 Task naming/identification conventions

**Status:** TBD

**Issue:** This spec requires task identifiers but does not prescribe a specific naming convention.

**Current state:**
- `docs/standards/naming_standard.md` defines naming for job_id, artifact_id, parameters, placeholders
- No specific convention exists for task identifiers within capability plans

**Options:**
1. **Option A:** Add task naming convention to naming_standard.md (e.g., "Task identifiers SHOULD use format: 'Task N: <verb> <object>'")
2. **Option B:** Leave flexible, require only that task identifiers be "clear descriptive phrases"
3. **Option C:** Recommend numbered format (Task 1, Task 2, ...) within each capability

**Recommendation:** Option B (flexible) is sufficient for now. Add to naming_standard.md only if task identifiers need to be machine-parsed.

**Impact if unresolved:** Low. Task identifiers are primarily for human readability and tracking. Flexibility is acceptable.

### 10.2 Task specification storage location

**Status:** TBD

**Issue:** This spec does not prescribe where task specifications are stored.

**Current state:**
- Capability plans are created during Step 3 but no canonical location is specified
- Task specifications are part of capability plans but storage location undefined

**Options:**
1. **Option A:** Store capability plans with task breakdowns in `docs/planning/` or similar
2. **Option B:** Store inline in Step 3 working documents (e.g., GitHub issues, planning docs)
3. **Option C:** Define in workflow_guide.md as part of Step 3 procedures

**Recommendation:** Defer to workflow_guide.md. This spec defines task structure, not where tasks are stored.

**Impact if unresolved:** Low. Storage location is a workflow concern, not a standards concern.

### 10.3 Granularity thresholds (how to determine if a task is too large/small)

**Status:** Partially resolved

**Issue:** Section 3 provides guidance on task size but does not define hard thresholds.

**Current state:**
- Guidance exists: "hours to 1-2 days, not weeks"
- No quantitative thresholds for lines of code, number of outputs, etc.

**Options:**
1. **Option A:** Add quantitative thresholds (e.g., "typically 1-5 intended outputs", "3-7 acceptance criteria")
2. **Option B:** Leave as qualitative guidance with examples
3. **Option C:** Provide thresholds per execution mode (human vs agent-assisted implementation)

**Recommendation:** Option B (qualitative) is appropriate. Task size depends heavily on context and trying to quantify it may create rigid rules that don't fit all cases.

**Impact if unresolved:** Low. Qualitative guidance with examples is sufficient. Over-prescription could be counterproductive.

---

## 11) Consistency check appendix

### Documents aligned with

This specification was developed in alignment with the following existing documents:

- ✅ `docs/context/development_approach.md` — 5-step workflow, approval gates, human-led / agent-assisted model
- ✅ `docs/context/target_agent_system.md` — evidence discipline, assumption handling, escalation rules, conflict resolution
- ✅ `docs/context/system_context.md` — truth hierarchy (intent vs runtime vs evidence)
- ✅ `docs/context/documentation_system_catalog.md` — standards layer purpose and boundaries
- ✅ `docs/context/glossary.md` — canonical term definitions (codable task, capability, acceptance criteria, evidence, assumption, escalation)
- ✅ `docs/process/workflow_guide.md` — Step 3 (capability planning) and Step 4 (implementation) procedures, checkpoints, escalation triggers
- ✅ `docs/standards/documentation_spec.md` — documentation structure, formatting, RFC 2119 keywords, section numbering
- ✅ `docs/standards/business_job_description_spec.md` — example of per-job standard structure and scope boundaries
- ✅ `docs/standards/script_card_spec.md` — example of operational documentation structure and required sections
- ✅ `docs/standards/artifacts_catalog_spec.md` — example of catalog entry specification and schema definition
- ✅ `docs/standards/naming_standard.md` — naming conventions (referenced for task identifiers, with flexibility where not prescribed)

### Potential conflicts detected

**None detected.**

All cross-references are consistent with existing documentation. No contradictions found between this spec and approved context/standards/process documents.

### Assumptions introduced

1. **Task identifier naming:** This spec requires task identifiers but does not prescribe a specific format. Assumes flexibility is acceptable unless machine-parsing is required. (See Section 10.1)

2. **Task specification storage:** This spec defines task structure but not where tasks are stored. Assumes workflow_guide.md or future updates will define storage location. (See Section 10.2)

3. **Granularity thresholds:** This spec provides qualitative guidance on task size. Assumes quantitative thresholds are not necessary. (See Section 10.3)

### Cross-document impact notes

**Low impact:**
- `docs/context/glossary.md` — May benefit from adding "codable task specification" as a distinct entry (currently only "codable task" is defined)
- `docs/process/workflow_guide.md` — May benefit from explicit reference to this spec in Section 4 (Step 3 procedures)

**No changes required to:**
- Context documents (no meaning changes)
- Other standards (no conflicting definitions)
- Process documents (alignment confirmed)

---

**End of specification**

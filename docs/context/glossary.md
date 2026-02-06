# Glossary

## Purpose
This glossary defines the canonical meaning of key terms used across the development system.
It exists to prevent drift, “double truth”, and silent re-interpretation of core concepts across documents, agents, and tools.

## Usage rule
When a term is used in any repository document or agent output, it MUST match the definition here.
If a definition needs to change, the change must be explicit and approved (not silently introduced).

---

## A

### Acceptance criteria
The minimum, testable conditions that must be met for a capability to be considered successfully implemented.
Acceptance criteria are evaluated using evidence and are a key input to validation.

### Agent
A collaborative role that can reason, propose options, draft artifacts, implement changes when tasked, and review outputs — always under human oversight and explicit approval gates.

### Agent profile
A definition file in `.github/agents/` that specifies agent instructions, tools, and behavior.
Agent profiles use YAML frontmatter for metadata (GitHub Copilot requirement) and contain complete agent instructions in a single file.
Specification: `docs/standards/documentation_spec.md` Section 3.6.

### Agent Layer
Documentation layer defining agent roles, responsibilities, and interaction guidance.
Canonical locations: `docs/agents/` and `.github/agents/`.
Must not contain tool manuals or embedded authoritative templates.
Related: Layer (documentation layer), Agent profile.

### AI-supported
A development approach where humans remain the decision-makers (approval gates), agents accelerate drafting/review/implementation under human oversight, and tools provide deterministic scaffolding/validation/evidence.
This describes the fundamental operating model of the vendor-to-PIM mapping system.
Reference: `docs/context/system_context.md`.

### Anti-pattern
A prohibited pattern in documentation or code that violates foundational principles or quality criteria.
Examples include shadow specifications, double truth, circular documentation, and implicit assumptions.
Anti-patterns are documented in standards to prevent recurring problems.

### Approval gate
A point where progression requires explicit human sign-off.
Approval gates apply to step transitions (not to iterative refinement within a step).

### Approval revocation
The withdrawal of previously-given approval before work is merged, triggered by discovery of critical issues, material changes after approval, or dependency approval revocation.
Requires documented reason and re-approval after concerns addressed.
Process defined in `docs/process/contribution_approval_guide.md` Section 3.5.

### Assumption (controlled)
An assumption is permitted only if it is:
- explicitly labeled,
- bounded (what is assumed, why, impact),
- approved by a human before implementation depends on it.

### artifact_id
Stable canonical identifier for an artifact type (not a single run instance).
Format: `<producer_anchor>__<artifact_type_snake_case>` where producer_anchor is either the producing job_id or "external" for artifacts not produced in this repository.
Once assigned, artifact_ids MUST NOT be renamed to maintain stable references.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.1.

### Artifact type
A stable pattern describing a category of artifacts, distinguished from specific run instances.
Example: artifact type = "vendor_products.json for vendor X", instance = "vendor_products.json written on 2026-01-30 at 14:23:45".
Catalog entries document artifact types, not individual instances.

### Artifacts Catalog
Living catalog documenting all persistent artifact types in the system, including their identifiers, producers, consumers, content contracts, and storage locations.
Canonical location: `docs/catalogs/artifacts_catalog.md`.
Specification: `docs/standards/artifacts_catalog_spec.md`.
Note: Used in both singular ("Artifact Catalog") and plural ("Artifacts Catalog") forms in documentation; both refer to the same catalog.
Related: Artifact type, artifact_id, Catalog entry.

### Auto-revocation
Automatic invalidation of approval when specific conditions occur: material changes after approval, dependency approval revoked, required decision record rejected, or conflict discovered affecting approved work.
Distinguished from manual approval revocation which requires explicit action.
Defined in `docs/process/contribution_approval_guide.md` Section 3.5.

---

## B

### BMEcat
An XML-based standard for product catalog data exchange, commonly used by vendors in B2B contexts.
In this system, BMEcat files are ingested as input to the vendor_input_processing pipeline.
Reference: `jobs/vendor_input_processing/preprocessIncomingBmecat/`.

### Bootstrap order
The required sequence for deriving job inventory entries from source artifacts to resolve cross-references correctly.
The 6-step order: (1) Discover jobs, (2) Extract manifest data, (3) Populate artifacts catalog, (4) Resolve artifact identifiers, (5) Derive dependencies, (6) Resolve remaining TBDs.
When starting from an empty artifacts catalog, entries are initially populated with `TBD` markers for artifact-dependent fields, then updated after catalog population.
Specification: `docs/standards/job_inventory_spec.md` Section 2.4.

### Breaking change
A change that requires migration, deprecation period, or coordination because it affects stable contracts or automation.
Examples include renaming job IDs, changing artifact filenames, or modifying parameter names.
Breaking changes require governance approval, decision records, and explicit migration plans.
Specification: `docs/standards/naming_standard.md` Section 5.

Domain-specific breaking change rules are defined for:
- Artifact contracts: `docs/standards/artifacts_catalog_spec.md` Section 6.5
- Naming conventions: `docs/standards/naming_standard.md` Section 5

### Business artifacts
Data products expressed from a stakeholder or end-user perspective rather than technical storage implementation.
In business descriptions, inputs and outputs are described as business artifacts (what they represent) rather than technical specifications (bucket/key patterns).
Examples: "vendor product catalog", "category mapping proposals", "validation report" (vs. "s3://bucket/path/file.json").
Related: Artifact type, Business description.

### Boundary statement
An explicit declaration of what a job, capability, or objective does NOT do.
Boundary statements prevent scope creep and clarify intent by stating explicit non-goals.
Format: "Does not..." or "Boundary:..." followed by specific exclusions.
Required in business descriptions (Section 1) and recommended for capability definitions.
Specification: `docs/standards/business_job_description_spec.md` Section 1.

### Boundedness
A key characteristic of codable tasks: the task has explicit boundaries that define what it does and what it explicitly does NOT do.
A bounded task has an explicit purpose statement, an explicit boundary statement (what it does NOT do), and scope that cannot expand silently during implementation without triggering escalation.
Specification: `docs/standards/codable_task_spec.md` Section 1.2.

### Business description
A per-job documentation file (`bus_description_<job_id>.md`) that captures business requirements, context, and rationale for a job.
Location: `jobs/<job_group>/<job_id>/` or `docs/jobs/<job_id>/`
Specification: `docs/standards/business_job_description_spec.md`

### Business rules and controls
Rules embedded in job logic that materially affect business outcomes, including:
- selection/prioritization logic (e.g., "uses first match found")
- exclusion criteria (e.g., "filters out products without article_id")
- validation thresholds (e.g., "requires minimum 3 products per category")
- truth protection rules (e.g., "never overwrites existing canonical mappings")
Documented in Section 5 of business descriptions to ensure business stakeholders understand decision logic.
Specification: `docs/standards/business_job_description_spec.md` Section 5.

### Business stakeholder
A person with responsibility for or interest in business outcomes, requirements, or decisions.
Business stakeholders provide requirements, approve objectives, and evaluate whether jobs achieve intended business goals.
Business descriptions target business stakeholders as primary audience (vs. technical operators).
Test: "Would a business stakeholder need this to understand what the job achieves?"

---

## C

### Capability
A building block within a pipeline: a discrete unit of system behavior required to achieve the objective.
Capabilities are planned (pipeline), then specified (capability definition), then implemented through codable tasks.

### Capability definition
A structured description of what a capability must do, typically including:
- inputs and outputs,
- rules/constraints,
- acceptance criteria,
- a bounded breakdown into codable tasks (or an equivalent controlled implementation outline).

### Catalog entry
A structured block in `docs/catalogs/artifacts_catalog.md` that documents one artifact type: its identity, location patterns, format, producer, consumers, content contract, and governance metadata.
Entries follow the schema defined in `docs/standards/artifacts_catalog_spec.md`.

### Codable task
A bounded unit of implementation work derived from an approved capability definition, characterized by four key properties: individuability (can be understood and implemented independently), boundedness (explicit scope with clear "does NOT do" statements), traceability (outcomes verifiable against acceptance criteria), and reviewability (another developer can validate implementation against specification).
Codable tasks are the primary work unit in Step 4 (Execute Development Tasks) and are specified using the structure defined in `docs/standards/codable_task_spec.md`.

### Codable task specification
A structured description documenting a bounded unit of implementation work. Contains seven required elements: task identity (unique identifier and parent capability reference), task purpose (1-3 sentence outcome description), task boundaries (explicit in-scope and out-of-scope statements), dependencies (prerequisite tasks, required inputs, external dependencies), intended outputs (artifacts/changes produced), acceptance criteria (evaluable pass/fail conditions), and unknowns/assumptions (explicit handling of uncertainties).
Created during Step 3 (Capability Planning) and executed during Step 4 (Execute Development Tasks).
Specification: `docs/standards/codable_task_spec.md`.

### Compliance
Adherence to standards, governance rules, and documentation specifications.
Compliance is enforced through automated validation (where possible), human review, and periodic audits.
Compliance checking ensures documentation and artifacts conform to approved formats, principles, and quality criteria.
Specification: `docs/standards/documentation_spec.md` Section 7.

### Concurrent approvals
Multiple PRs in flight that reference the same approved artifacts or affect the same code/documents.
Requires coordination: upstream merges require downstream re-review; first-merged PR takes precedence on conflicts.
Coordination rules defined in `docs/process/contribution_approval_guide.md` Section 6.5.

### Configuration files
Static configuration artifacts used by jobs to control their behavior (e.g., extraction rules, field mappings, vendor-specific settings).
Distinguished from data inputs: configuration files control HOW a job processes data, while inputs are the data TO process.
Configuration files are relatively static (change infrequently) compared to data inputs (which change per execution).
Declared in job manifests under `config_files[]` with bucket, key_pattern, format, and required status.
Documented in script cards Section 2.3A when present.
Specification: `docs/standards/job_manifest_spec.md` Section 5.5.

### Conflict
Any mismatch between approved intent and observed reality (tool results, implementation behavior, or artifact content).
Conflicts must be surfaced explicitly and resolved via an explicit decision (not silently).

### Content contract
A minimal parse and validation contract for an artifact, describing its structural expectations without being a full schema.
Includes: top_level_type, primary_keying, required_sections, empty_behavior, and notes.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.10.

### Context Layer
Documentation layer containing intent, shared meaning, and system framing documents.
Canonical location: `docs/context/`.
Must not contain operational instructions, tool syntax, or normative schemas.
Documents include: development_approach.md, target_agent_system.md, system_context.md, glossary.md, documentation_system_catalog.md.
Related: Layer (documentation layer).

### Cross-reference
A link from one document to another, typically using relative paths from the repository root.
Cross-references enable navigation and must be kept up-to-date when documents are moved or renamed.
Format: `docs/context/development_approach.md` (not absolute URLs for internal documents).

---

## D

### Double truth
A failure mode where the same “contract” or meaning is defined in more than one place (e.g., a standard is duplicated inside a workflow doc),
creating competing sources of authority and eventual inconsistency.

### Decision ID
A unique identifier for a decision record using the format `DR-NNNN` where `NNNN` is a zero-padded 4-digit sequential number (e.g., `DR-0001`, `DR-0042`).
Decision IDs are stable and MUST NOT be reused even if the decision is superseded.
Each decision record file is named using its Decision ID: `DR-NNNN-short-slug.md`.
Specification: `docs/standards/decision_records_standard.md` Section 3.1.1 and Section 6.1.2.

### Decision log
The canonical index of all decision records, maintained at `docs/catalogs/decision_log.md`.
The decision log provides navigable access to decisions with status, date, and tags, organized by status (Active, Superseded, Rejected/Withdrawn).
Purpose: Maintains continuity and governance transparency through decision record traceability.
Specification: `docs/standards/decision_records_standard.md` Section 6.2.

### Decision record
A structured document that records significant decisions, their rationale, alternatives considered, and approval status.
Decision records follow the format defined in `docs/standards/decision_records_standard.md`.
They are essential for breaking changes, exceptions to principles, and governance decisions.

### Decision status
The lifecycle state of a decision record, indicating its current validity and applicability.
Valid status values: **Proposed** (drafted, under review), **Approved** (in effect), **Superseded** (replaced by newer decision), **Deprecated** (being phased out), **Rejected** (proposed but not accepted), **Withdrawn** (proposal withdrawn before review).
Status transitions follow defined rules: Proposed can become Approved/Rejected/Withdrawn; Approved can become Superseded/Deprecated; terminal states are Rejected and Withdrawn.
Specification: `docs/standards/decision_records_standard.md` Section 4.

### Development Step Document
A container document that holds the list of codable task specifications for a capability, serving as a control instrument for implementation tracking and execution.
The Development Step Document is created during Step 3 (Capability Planning) and contains the complete breakdown of codable tasks with their boundaries, dependencies, and acceptance criteria.
Storage location options: GitHub Issues (for issue-tracked work), capability specification documents in `docs/specifications/`, or PR descriptions (for single-PR capabilities).
See `docs/process/workflow_guide.md` Section 4 and `docs/standards/codable_task_spec.md`.

### Deployment name
The name of a job as deployed in its execution platform (e.g., AWS Glue job name).
For AWS Glue jobs, this is stored in the manifest `glue_job_name` field and typically matches the `job_id`.
Deployment-specific prefixes (e.g., `prod-{job_id}`) are applied at deployment time and are not part of the canonical deployment name.
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.1.

### Documentation timing
The phase at which documentation is created: during development (prospective, intent-driven) or after implementation (retroactive, observation-driven).
- **For new jobs:** Business descriptions capture intended behavior and approved business rules before/during implementation.
- **For existing jobs (retroactive):** Business descriptions document observed behavior from code analysis and operational knowledge.
Retroactive documentation must mark interpretations with `ASSUMPTION:` and uncertain behaviors with `TBD`.
Specification: `docs/standards/business_job_description_spec.md` Section 0.4.

### Doc Impact Scan
A systematic consistency check procedure run after documentation changes to verify: (1) term consistency across documents, (2) catalog alignment with actual document set, (3) layer boundary preservation, (4) cross-reference authority validity, (5) documentation completeness.
Required before approval gates involving documentation changes.
Evidence format: Doc Impact Scan report or consistency check pass.
Related: Validation / validation evidence, Double truth, Cross-reference.

### Deprecated
Marked as obsolete but retained temporarily for historical reference and migration support.
Deprecated documents include a deprecation marker, reason, redirect to replacement (if any), and planned removal date.
Minimum retention: 30 days or one release cycle.

### Deterministic
A property of tools and evidence outputs: given the same inputs, a deterministic tool or process produces the same outputs consistently.
Deterministic evidence can be independently verified and does not rely on subjective interpretation.

### Downstream job IDs
Jobs that consume artifacts produced by this job (dependencies in the forward direction).
Derived from artifact-level evidence by finding all jobs that list this job's output artifacts in their inputs.
Represented as comma-separated list in lexicographic sort order.
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.4.

### Drift
Uncontrolled divergence between:
- approved intent (what should be true),
and
- implemented/runtime behavior or documents (what is true).
Drift includes silent changes, shadow specs, and unapproved re-interpretation of terms/rules.

### Dual-write
Migration technique where data is written to both old and new locations during a transition period, enabling gradual consumer migration and rollback capability.
Used for breaking changes to artifact locations or formats.

### Dual-role artifact
An artifact that serves as both input and output for the same job (read at job start, updated and written at job end).
Common pattern for jobs that update shared reference data in place (e.g., canonical mappings).
In job inventory entries, dual-role artifacts are listed in both `inputs` and `outputs` fields.
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.3.

### Documentation system catalog
A registry that defines all document types, their purposes, semantic boundaries, and canonical locations.
The catalog prevents overlap, ensures separation of concerns, and serves as the authoritative reference for where content belongs.
Location: `docs/context/documentation_system_catalog.md`

---

## E

### Empty behavior
Defines how an artifact represents "no data" state.
Allowed values:
- `absent_file_allowed` — file may not exist
- `empty_file_allowed` — zero-byte file written
- `empty_object_allowed` — `{}` written
- `empty_array_allowed` — `[]` written
- `no_empty_allowed` — non-empty content required
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.10.

### Evidence
Deterministic outputs that support approval decisions (e.g., validation reports, test results, run receipts, logs).
Evidence must be reproducible and referenced explicitly when making "verified" or "confirmed" claims.
Ref: `docs/context/target_agent_system.md` and `docs/standards/documentation_spec.md` Section 1.3.

### Execution confirmation
Artifacts that prove approved work was executed and integrated (e.g., merge commits) but are not approval evidence themselves.
The approval must exist before execution.
Distinguished from approval evidence which authorizes work to proceed.
Defined in `docs/process/contribution_approval_guide.md` Section 3.1A.

### Evidence artifacts
Audit artifacts produced by a job for tracking and validation purposes.
Includes run receipts (structured JSON records of execution metadata) and counters (metrics emitted during job execution).
Represented in job inventory entries as compact structured string: `run_receipt=<true|false|TBD>; counters=<names|NONE|TBD>`
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.3.

### Evidence discipline
Rules for how evidence is used:
- Evidence must be deterministic and reviewable.
- Agents may summarize evidence but must not substitute narrative for proof.
- “Verified” / “confirmed” may be used only when the evidence is explicitly referenced.

### Evidence tools
A category of tools that produce deterministic, reviewable outputs to support approval decisions and verify acceptance criteria.
Evidence tools include test runners, runtime execution logs, and CI automation test workflows.
Required for claims of "verified" or "confirmed" status.
Note: Manual observation and screenshots are part of manual review validation (not evidence tools), as they rely on human judgment rather than deterministic tool outputs.
Ref: `docs/agents/agent_tool_interaction_guide.md` Section "Evidence Tools" and `docs/standards/validation_standard.md`.

### Escalation
A required stop-and-surface behavior:
when an agent cannot proceed without introducing new assumptions, expanding scope, or changing agreed rules/criteria,
the agent must escalate for human decision.

### Executor
The platform that executes a job (e.g., AWS Glue, AWS Lambda, Make).
Allowed values: `aws_glue`, `aws_lambda`, `make`, `other`, `TBD`.
Derived from manifest fields: `glue_job_name` → `aws_glue`, `lambda_function_name` → `aws_lambda`, `makefile_target` → `make`.
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.2.

---

## F

### Failure mode
An expected way a job can fail and how the failure surfaces.
Includes: failure conditions (exit codes, exceptions), error detection mechanisms, and recovery/rollback behavior.
Documented in script cards Section 2.9 to enable troubleshooting and orchestration.
Example: "Exits with code 1 if XML validation fails; raises ValueError if required field missing"
Related: Observability.

### Function (agent function)
A responsibility or role that an agent may fulfill in the workflow.
Agent functions are defined independently of specific agent implementations, allowing one or multiple actual agents to fulfill a given function.

### Frontmatter
YAML metadata block at the start of a file, enclosed by `---` delimiters.
Used in agent profile definitions (`.github/agents/`) to specify agent name, description, and other metadata.
Required by GitHub Copilot for agent configuration.

### File name pattern
Terminal filename pattern (last segment after final `/`), which may contain placeholders.
Represents a stable pattern, not a concrete run-instance filename.
Examples: `vendor_products.json`, `${vendor_name}_products.json`.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.2.

### 5-step workflow
The development approach consisting of five sequential stages: (1) Define Objective, (2) Plan Pipeline, (3) Define Capabilities, (4) Execute Tasks, (5) Validate and Document.
Step transitions require approval gates; iteration within steps is permitted.
Also referred to as "five-step approach", "five-step workflow", or "5-step approach".
Related: Process (workflow step), Approval gate, Iteration within a step, Step 1, Step 2, Step 3, Step 4, Step 5.

---

## G

### Glue script
The primary Python entrypoint file for an AWS Glue job, conventionally named `glue_script.py`.
Location: `jobs/<job_group>/<job_id>/glue_script.py`
Contains job logic, data transformations, and integration with AWS Glue APIs.

### Governance
Rules and approval processes that ensure changes to stable contracts, standards, and documentation follow controlled procedures.
Governance includes decision records, breaking change approvals, compliance checking, and exception handling.
Specification: `docs/standards/documentation_spec.md` Section 7.

---

## H

### Heading hierarchy
The structural organization of document headings (H1 → H2 → H3 → H4) without skipping levels.
Proper heading hierarchy ensures documents are navigable and semantically structured.
Required by `docs/standards/documentation_spec.md` Section 2.3.

---

## I

### Individuability
A key characteristic of codable tasks: the task can be understood and implemented independently, given its stated dependencies and inputs.
An individuable task can be assigned to a single implementer without requiring coordination during implementation (coordination may be needed for integration), and does not depend on undocumented assumptions or implicit knowledge.
Specification: `docs/standards/codable_task_spec.md` Section 1.1.

### Independent reviewer
A reviewer who did not author the work being approved, is not directly supervised by or supervising the author, and has no direct conflict of interest in the specific work.
Required for approval in multi-person teams to maintain review independence.
Not required for single-person teams where self-approval is permitted.
Defined in `docs/process/contribution_approval_guide.md` Section 2.6.

### In-scope / Out-of-scope
A boundary statement defining what the objective/capability includes and explicitly excludes.
Used to prevent scope creep and ambiguity in planning and implementation.

### Intent truth
The “should be true” layer:
approved objectives, pipeline plans, and capability definitions that define intended behavior and constraints.


### Invariant
A property of job behavior that must always hold true, regardless of inputs or runtime conditions.
Invariants describe observable, externally meaningful guarantees (not internal implementation details).
Examples: "Always writes exactly one output file per input file", "Output file is always valid JSON"
Documented in script cards Section 2.8 to establish behavior contracts.
Related: Runtime behavior, Failure mode.

### Iteration within a step
Refinement loops that occur before a step output is approved.
Iteration is allowed and expected; it does not advance the system state unless an approval gate is passed.

---

## J

### Job inventory
A living catalog that aggregates job inventory entries for all executable jobs in the repository.
Location: `docs/catalogs/job_inventory.md`
Purpose: Provides fast orientation for humans and agents about what jobs exist, what they consume/produce, and how they relate to each other.
Specification: `docs/standards/job_inventory_spec.md`

### Job inventory entry
A machine-readable structured record representing one executable job, capturing its identity (job_id, deployment_name, job_dir), execution characteristics (executor, runtime), interface contract (parameters, inputs, outputs, side_effects), lifecycle metadata (owner, status, last_reviewed), and dependency relationships (upstream_job_ids, downstream_job_ids).
Each entry enables consistent discovery, validation, automation, and cross-job integration.
Specification: `docs/standards/job_inventory_spec.md`

### Job manifest
A machine-readable YAML file (`job_manifest.yaml`) that serves as the source of truth for a job's interface contract: parameters, inputs, outputs, side effects, and run receipt behavior.
Location: `jobs/<job_group>/<job_id>/job_manifest.yaml`
Specification: `docs/standards/job_manifest_spec.md`
The manifest is evidence-based (derived from script analysis) and supports automation-friendly job discovery and orchestration.

---

## L

### Layer (documentation layer)
A classification used to prevent mixing purposes and authority.
Documentation is organized into distinct layers, each with a specific purpose that does not overlap with others.
Canonical layers:
- Context layer (`docs/context/`): intent, shared meaning, system framing
- Governance and standards layer (`docs/standards/`): normative rules, schemas, validation requirements
- Agent documentation layer (`docs/agents/`): agent roles and interaction guidance
- Process layer (`docs/process/`): how-to guidance for executing the workflow
- Operational reference layer (`docs/ops/`): technical manuals for tools and automation
- Living catalogs and per-job docs (`docs/catalogs/`, `jobs/`): instances describing concrete system and per-job intent/operations
Specification: `docs/context/documentation_system_catalog.md` Section "Layers and Intent".

### Lightweight approval
Accelerated approval process for low-risk changes meeting specific criteria: low risk (no contract/identifier/governance changes), narrow scope (single job internal, doc clarifications, tests), no breaking changes, and traceable.
Requires single approver with 24-hour target review window.
Distinguished from standard approval which may require multiple reviewers.
Defined in `docs/process/contribution_approval_guide.md` Section 10.2.

---

## M

### Manifest generator (tool)
A scaffolding tool that performs static analysis on `glue_script.py` to extract job interface facts and produce a draft `job_manifest.yaml`.
Tool category: Scaffolding (per target agent system).
Used by humans and agents to reduce manual manifest authoring.
Location: `tools/manifest-generator/` (if implemented).

### Material change
A change that affects scope boundaries, success criteria, acceptance criteria, or approval conditions, requiring re-approval.
Material changes include: adding/removing/modifying boundaries or criteria, changing capability/task boundaries, adding/removing unknowns/assumptions, changing traceability.
Distinguished from non-material changes (wording, formatting, clarifications, typos) which do not require re-approval.
Defined in `docs/process/contribution_approval_guide.md` Section 2.0.

### Markdown
A lightweight markup language using plain text formatting syntax.
All documentation files in this repository use Markdown (`.md` extension) with UTF-8 encoding.
Format rules: `docs/standards/documentation_spec.md` Section 2.

### Metadata header
A structured block immediately after the H1 title that provides document context and purpose.
Format and required fields vary by document type (standards, context, process, ops, catalogs, agents, per-job).
Specification: `docs/standards/documentation_spec.md` Section 3.

### Migration
The process of moving from an old format, structure, or naming convention to a new one.
Migration requires decision records, backward compatibility plans, deprecation periods, and explicit approval.
Common scenarios: renaming identifiers, restructuring documentation, updating schemas.

---

## N

### NDJSON (newline-delimited JSON)
Also known as JSON Lines.
A format where each line is a complete, valid JSON object, with lines separated by newline characters.
Used as the default JSON output format for Spark/Glue DataFrame writes.
Distinguished from `json` (single JSON document) in job manifests per format semantic rules.

### No hidden authority
A rule that agents and tools must not imply outputs are “true” because an agent produced them or a tool reported them.
Truth is grounded in:
- human decisions and approvals,
- enforceable standards/governance,
- runtime behavior of implemented artifacts,
- deterministic evidence outputs.


### Normalized placeholder
A manifest placeholder convention (e.g., `${X_norm}`) indicating that parameter `X` has been normalized by the script to ensure a trailing slash for S3 prefix operations.
Example: `${prepared_output_prefix_norm}` means the `prepared_output_prefix` parameter value with exactly one trailing `/`.
Definition: Section 6.4 of `docs/standards/job_manifest_spec.md`.

---

## O

### Objective
A high-level statement of intent describing what the system aims to achieve.
An objective sets:
- success criteria,
- scope boundaries,
- and (when known) unknowns/assumptions that require later resolution.

### Operational notes
An optional, minimal section in business descriptions (Section 7) for operational facts that materially affect business understanding and cannot be deferred to the script card.
Includes: critical failure behavior affecting business continuity, output behavior affecting downstream consumption, monitoring artifacts essential to business tracking.
Should be used sparingly to maintain separation between business view (business description) and operational detail (script card).
Specification: `docs/standards/business_job_description_spec.md` Section 7.

### Ops Layer
Documentation layer containing technical manuals for tools and automation.
Canonical location: `docs/ops/`.
Contains tool usage, parameters, troubleshooting, and operational procedures.
Must not contain normative rules that belong in standards.
Also referred to as "Operational Layer" or "Operational reference layer".
Related: Layer (documentation layer).

### Observability
The signals and artifacts that enable monitoring, troubleshooting, and verification of job execution.
Includes: logs (INFO/ERROR/DEBUG levels), metrics (CloudWatch, custom counters), run receipts (structured execution summaries), and operator verification artifacts.
Documented in script cards Section 2.9 (what signals exist and what they indicate; how to access them is in ops docs).
Related: Failure mode, Run receipt.


---

## P

### Pipeline
An ordered set of capabilities required to achieve an objective, including dependencies/decision points where relevant.

### Processing logic (business flow)
The sequence of business-level transformations described in a business description (Section 4).
Expressed in natural language describing what stakeholders care about (e.g., "enriches products with...", "aggregates per vendor category...") rather than code-level implementation.
Typically 4-12 steps; complex jobs may use multi-phase structure (PART 1, PART 2, etc.).
Distinct from operational steps in script cards which describe technical execution.
Specification: `docs/standards/business_job_description_spec.md` Section 4.

### Process Layer
Documentation layer containing how-to guidance for executing the 5-step workflow.
Canonical location: `docs/process/`.
Provides practical procedures, checkpoints, and escalation triggers.
Must reference but not redefine schemas or tool syntax.
Related: Layer (documentation layer).

### Placeholder (manifest)
A template variable in a job manifest's `bucket` or `key_pattern` field, represented as `${NAME}`.
Placeholders are substituted at job invocation time with actual parameter values or runtime-generated values.
Types: parameter placeholders (match parameter names exactly) and runtime-generated placeholders (computed by the job).

### Placeholder normalization
A technique for deterministic artifact matching across different placeholder styles.
Normalizes `${...}`, `{...}`, and `<...>` to `<VAR>` before comparison to enable consistent matching.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 2.1.

### Presence on success
Defines whether an artifact file must exist when a job succeeds.
Allowed values:
- `required` — file must exist on success
- `optional` — file may or may not exist
- `conditional` — existence depends on job conditions
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.8.

### Preconditions
Required state or artifacts that must exist before a job can execute successfully.
Examples: "Input files from upstream job X must exist", "DynamoDB table Y must contain entry for parameter Z"
Documented in script cards Section 2.3 to clarify job dependencies and execution requirements.
Use `NONE` if no preconditions exist; use `TBD` only if truly unknown.


### Producer anchor
The prefix component in artifact_id derivation: either the producing job_id (for in-repo artifacts) or "external" (for artifacts not produced in this repository).
Producer anchor for external artifacts is permanent and MUST NOT change even when consumers are added later.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.1.

### PySpark
The Python API for Apache Spark, enabling large-scale data processing using Spark's distributed computing engine.
In this system, PySpark jobs run on AWS Glue with access to `SparkContext`, `GlueContext`, and Spark DataFrames.
Runtime type in job manifests: `pyspark`.

### Python Shell (AWS Glue)
A lightweight Glue job type that runs standard Python code without Spark overhead.
Used for tasks that process smaller datasets or orchestrate S3 operations using boto3.
Runtime type in job manifests: `python_shell`.
Distinguished from `pyspark` by absence of SparkContext/GlueContext Spark features.

### Quality criteria
Standards for evaluating documentation quality: accuracy, completeness, currency, clarity, and maintainability.
Quality criteria guide documentation reviews and identify areas for improvement.
Specification: `docs/standards/documentation_spec.md` Section 5.1.

### Process (workflow step)
A named stage in the development approach (e.g., Define Objective → Plan Pipeline → Define Capabilities → Execute Tasks → Validate/Document).
Step transitions require approval gates; iteration within a step is permitted.
Note: "Stage" and "step" are used interchangeably in this system.

---

## R

### Rules truth
The “must conform to” layer:
standards, governance constraints, and enforceable schemas that define how artifacts must be structured and validated.


### Run receipt
A structured JSON artifact written by a job to S3 that records execution metadata: run ID, timestamp, input/output locations, record counts, validation status, and notes.
Run receipts serve as audit trails and enable downstream jobs to verify upstream completion.
Declared in job manifests under `logging_and_receipt.writes_run_receipt`.

### Relative path
A file path specified relative to the repository root, used for cross-document references.
Format: `docs/context/development_approach.md` (not absolute URLs for internal documents).
Ensures links remain valid when repository is cloned or moved.

### Retroactive documentation
Documentation created after a job or system is already implemented, based on code analysis and operational observation rather than prospective design.
Retroactive documentation must mark interpretations with `ASSUMPTION:` and uncertain behaviors with `TBD`.
Contrasts with prospective documentation created during development that captures intended behavior.
See also: Documentation timing.
Specification: `docs/standards/business_job_description_spec.md` Section 0.4.

### Reviewability
A key characteristic of codable tasks: another developer can understand the intent and validate that the implementation satisfies the task specification.
A reviewable task has specification documented in a readable form, acceptance criteria with clear pass/fail conditions, and implementation validatable against the specification without requiring the implementer to explain undocumented decisions.
Specification: `docs/standards/codable_task_spec.md` Section 1.4.

### Runtime truth
The "what actually runs" layer:
the effective behavior defined by code, deployed artifacts, and runtime configuration.

### Runtime behavior
High-level description of what a job does during execution, expressed as action-oriented steps.
Focuses on observable behavior (reads, transforms, writes, logs) not internal implementation details.
Typically 4-8 bullets in script cards Section 2.7.
Example: "Reads XML from S3", "Validates structure", "Writes JSON output"
Related: Invariant, Processing logic (business flow).


---

## S

### Scope boundary
A statement that makes the objective/capability bounded and unambiguous, including explicit exclusions.

### Self-approval
The act of a contributor approving their own work.
Permitted for single-person teams (sole member has absolute authority) but restricted in multi-person teams to maintain review independence.
Distinguished from independent peer review where a separate reviewer approves the work.
Defined in `docs/process/contribution_approval_guide.md` Section 2.6.

### S3 location pattern
Stable S3 location pattern(s) for an artifact type, in the format `s3://${bucket}/${key_pattern}`.
May be a single pattern or multiple patterns (for cross-region replication, backups, or migration paths).
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.3.

### Script card
A per-job operational documentation file (`script_card_<job_id>.md`) that describes runtime behavior, invariants, failure modes, and observability signals for one executable job.
Focus: HOW the job behaves at runtime, WHAT must always be true, HOW it fails, and WHAT signals it produces.
Location: `jobs/<job_group>/<job_id>/`
Specification: `docs/standards/script_card_spec.md`
Related: Business description (WHY/WHAT from business perspective).

### Scaffolding tools
A category of tools that generate empty or minimally-filled structures to reduce manual effort and ensure consistency with repository standards.
Scaffolding tools produce drafts that require agent review and enhancement, often with TBD or placeholder values.
Examples: manifest-generator (generates draft job_manifest.yaml).
Ref: `docs/agents/agent_tool_interaction_guide.md` Section "Scaffolding Tools".

### Separation of concerns
A rule that documentation and artifacts must not mix layers:
- principles/intent,
- enforceable rules,
- execution procedures,
- operational references.
This prevents shadow specs and double truth.

### Shared artifact
An artifact that is produced by multiple jobs or consumed by multiple jobs.
Handling rules:
- Single primary producer: use producer `job_id` as artifact_id anchor
- Multiple producers: register as shared artifact exception per `artifacts_catalog_spec.md` Section 3.6
- External artifacts: use `external__*` prefix
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.3.

### Supersede / Superseded / Supersession
The relationship where a newer decision record explicitly replaces an older decision record.
**Supersede (verb):** To replace a decision with a newer one. The new decision MUST reference which decisions it supersedes.
**Superseded (status/adjective):** A decision that has been replaced. Status transitions to "Superseded" with reference to the superseding decision.
**Supersession (noun):** The act or relationship of replacement. Can be full (entire decision replaced) or partial (some aspects replaced while others remain active).
When a decision is superseded, both the old and new decision records MUST be updated with cross-references to maintain bidirectional traceability.
Specification: `docs/standards/decision_records_standard.md` Sections 3.1.9, 4.1.3, and 4.1.6.

### Shadow specification
An anti-pattern where normative requirements are embedded in the wrong documentation layer.
Example: A process guide containing required field definitions instead of referencing the authoritative standard.
Shadow specs create competing authority and violate the "single source of truth" principle.

### Shared artifact exception
An allowlisted case where multiple producer jobs write to the same artifact type, overriding the default single-writer rule.
Requires explicit registration in `docs/registries/shared_artifacts_allowlist.yaml`.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.6.

### Stale
Outdated information that no longer reflects current implementation, decisions, or behavior.
Stale documentation reduces accuracy and misleads users.
Currency is validated through git commit dates and comparison with runtime behavior.

### Standards Layer
Documentation layer containing normative rules, schemas, and validation requirements.
Canonical location: `docs/standards/`.
Specifications are authoritative and validator-enforceable.
Must not contain per-job implementations or tool manuals.
Related: Layer (documentation layer).

### Side effect (job)
A job behavior that modifies S3 state beyond its declared outputs.
Types:
- `deletes_inputs`: Job deletes input objects after successful processing
- `overwrites_outputs`: Job overwrites existing output objects (vs. fail-on-exists)
Declared in job manifests under `side_effects` to inform orchestration and recovery logic.

### Single source per contract type
A governance rule:
each contract type (e.g., “format rules”, “workflow gates”, “tool usage”, “templates”) must have exactly one authoritative home.
Other documents may reference it but must not redefine it.


### Single-writer rule
Default governance principle: an artifact type MUST have exactly one producing job to simplify orchestration and reduce coordination complexity.
Multi-writer artifacts are allowed only via the shared artifact exception.
Specification: `docs/standards/artifacts_catalog_spec.md` Section 3.6.

### Step 1 (Define Objective)
First stage of the 5-step workflow where high-level intent, success criteria, and scope boundaries are defined and approved.
Output: Approved objective artifact.
Approval required for transition to Step 2.
Related: 5-step workflow, Objective, Approval gate.

### Step 2 (Plan Pipeline)
Second stage of the 5-step workflow where required capabilities are identified, ordered, and approved.
Output: Approved pipeline plan.
Approval required for transition to Step 3.
Related: 5-step workflow, Pipeline, Capability.

### Step 3 (Define Capabilities)
Third stage of the 5-step workflow where individual capabilities are specified with acceptance criteria, codable tasks defined, and approved before implementation.
Output: Approved capability definitions with codable task specifications.
Approval required for transition to Step 4.
Related: 5-step workflow, Capability definition, Codable task, Development Step Document.

### Step 4 (Execute Tasks)
Fourth stage of the 5-step workflow where codable tasks are implemented, tested, and integrated.
Output: Working implementation.
Approval required for transition to Step 5.
Related: 5-step workflow, Codable task.

### Step 5 (Validate and Document)
Fifth stage of the 5-step workflow where integrated work is validated against objective success criteria and documented.
Output: Validation evidence and completed documentation.
Related: 5-step workflow, Validation / validation evidence, Success criteria.

### Step Transition
Movement from one workflow step to the next in the 5-step approach.
Step transitions require explicit approval; distinguished from iteration within a step which does not require re-approval.
Related: Approval gate, Iteration within a step, Process (workflow step).

### Success criteria
Concrete conditions that define when an objective is achieved.
Success criteria inform capability planning and validation evidence.

---

## T

### TBD (explicit unknown)
A deliberately marked unknown that blocks implicit assumptions.
TBDs must be either resolved later or explicitly approved as controlled assumptions before implementation depends on them.

**In job manifests:** Use `TBD` ONLY for values that are truly unknowable from static code analysis (e.g., dynamic runtime behavior, external config dependencies).
- Use `null` for "not applicable" (e.g., receipt bucket when no receipt is written)
- Use `[]` for "provably empty" (e.g., counters when none exist)
- Reserve `TBD` for "cannot determine without runtime/deployment data"

**In artifacts catalog:** Unknown list fields MUST use scalar string `TBD` (not `[TBD]` or omitted).
Specification: `docs/standards/artifacts_catalog_spec.md` Section 1.3.1.

### Task identifier
A unique name or ID for a codable task within a capability, used for tracking and traceability.
Format: Short descriptive phrase or ID (e.g., "Task 1: Validate input schema", "implement_xml_parser").
Naming follows clear descriptive conventions; formal naming rules are intentionally flexible to adapt to context.
Required element in codable task specifications alongside parent capability reference.
Specification: `docs/standards/codable_task_spec.md` Section 2.1.

### Tool
A deterministic instrument used by humans and agents to scaffold, validate, and produce evidence.
Tools do not invent meaning, interpret intent, or make approval decisions.

---

## U

### Upstream job IDs
Jobs that produce artifacts consumed by this job (dependencies in the backward direction).
Derived from artifact-level evidence by finding all jobs that produce artifacts listed in this job's inputs.
Represented as comma-separated list in lexicographic sort order.
Specification: `docs/standards/job_inventory_spec.md` Section 2.2.4.

---

## V

### Verified / Confirmed
A claim can be labeled as "verified" or "confirmed" only when explicit evidence is referenced (in the repository or in the conversation) that:
1. Directly demonstrates the claim
2. Is deterministic (reproducible given same inputs and context)  
3. Is referenced explicitly
4. Is reviewable by any team member with appropriate access

Otherwise, the correct status is "unverified", "unknown", or "TBD".
Verification provides evidence for approval but is not approval itself.
Normative definition: `docs/standards/validation_standard.md` Section 2.1.


### Validation / validation evidence
Validation is the process of checking acceptance criteria and conformance to standards using five distinct categories: structure, conformance, consistency, runtime, and manual review.
Validation evidence is the deterministic output used to support approval decisions.
Detailed validation rules and categories are defined in `docs/standards/validation_standard.md`.

### Validation categories
The five categories of validation used in this repository, each with specific purposes and pass criteria:
1. **Structure Validation** - Checks file structures, naming conventions, and metadata headers
2. **Conformance Validation** - Validates compliance with normative schemas and specifications
3. **Consistency Validation** - Ensures internal consistency across related documents (no contradictions, all references resolve)
4. **Runtime Validation** - Verifies that implemented code/scripts behave as specified in their contracts
5. **Manual Review Validation** - Judgment-based quality checks that cannot be fully automated
Each category has defined blocking severity (MUST or SHOULD block progression when failing).
Specification: `docs/standards/validation_standard.md` Section 4.

### Validation tools
A category of tools that check conformance to repository standards and flag violations deterministically.
Validation tools are used iteratively during work (after each logical unit), before human approval, and before pushing changes.
Examples: validate_repo_docs.py (validates manifests, artifacts catalog, job inventory).
Ref: `docs/agents/agent_tool_interaction_guide.md` Section "Validation Tools".

### Versioning (documentation)
The approach to tracking changes in documentation over time.
This repository uses git history for all change tracking (commits, tags, branches) instead of explicit version numbers in document metadata.
Rationale: Eliminates duplication, provides comprehensive audit trail, and reduces maintenance overhead.
Specification: `docs/standards/documentation_spec.md` Section 4.

---


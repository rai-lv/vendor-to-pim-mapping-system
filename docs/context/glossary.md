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

### Approval gate
A point where progression requires explicit human sign-off.
Approval gates apply to step transitions (not to iterative refinement within a step).

### Assumption (controlled)
An assumption is permitted only if it is:
- explicitly labeled,
- bounded (what is assumed, why, impact),
- approved by a human before implementation depends on it.

---

## B

### BMEcat
An XML-based standard for product catalog data exchange, commonly used by vendors in B2B contexts.
In this system, BMEcat files are ingested as input to the vendor_input_processing pipeline.
Reference: `jobs/vendor_input_processing/preprocessIncomingBmecat/`.

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

### Codable task
A bounded unit of implementation work derived from a capability definition.
A codable task is defined so that it can be executed and reviewed in a controlled way (clear boundaries, dependencies, and intended outputs).
Codable tasks are the primary work unit in Step 4 (Execute Development Tasks).

### Conflict
Any mismatch between approved intent and observed reality (tool results, implementation behavior, or artifact content).
Conflicts must be surfaced explicitly and resolved via an explicit decision (not silently).

---

## D

### Double truth
A failure mode where the same “contract” or meaning is defined in more than one place (e.g., a standard is duplicated inside a workflow doc),
creating competing sources of authority and eventual inconsistency.

### Deterministic
A property of tools and evidence outputs: given the same inputs, a deterministic tool or process produces the same outputs consistently.
Deterministic evidence can be independently verified and does not rely on subjective interpretation.

### Drift
Uncontrolled divergence between:
- approved intent (what should be true),
and
- implemented/runtime behavior or documents (what is true).
Drift includes silent changes, shadow specs, and unapproved re-interpretation of terms/rules.

---

## E

### Evidence
Deterministic outputs that support approval decisions (e.g., validation reports, test results, run receipts, logs).

### Evidence discipline
Rules for how evidence is used:
- Evidence must be deterministic and reviewable.
- Agents may summarize evidence but must not substitute narrative for proof.
- “Verified” / “confirmed” may be used only when the evidence is explicitly referenced.

### Escalation
A required stop-and-surface behavior:
when an agent cannot proceed without introducing new assumptions, expanding scope, or changing agreed rules/criteria,
the agent must escalate for human decision.

---

## F

### Function (agent function)
A responsibility or role that an agent may fulfill in the workflow.
Agent functions are defined independently of specific agent implementations, allowing one or multiple actual agents to fulfill a given function.

---

## I

### In-scope / Out-of-scope
A boundary statement defining what the objective/capability includes and explicitly excludes.
Used to prevent scope creep and ambiguity in planning and implementation.

### Intent truth
The “should be true” layer:
approved objectives, pipeline plans, and capability definitions that define intended behavior and constraints.

### Iteration within a step
Refinement loops that occur before a step output is approved.
Iteration is allowed and expected; it does not advance the system state unless an approval gate is passed.

---

## J

### Job manifest
A machine-readable YAML file (`job_manifest.yaml`) that serves as the source of truth for a job's interface contract: parameters, inputs, outputs, side effects, and run receipt behavior.
Location: `jobs/<job_group>/<job_id>/job_manifest.yaml`
Specification: `docs/standards/job_manifest_spec.md`
The manifest is evidence-based (derived from script analysis) and supports automation-friendly job discovery and orchestration.

---

## L

### Layer (documentation layer)
A classification used to prevent mixing purposes and authority.
Canonical layers:
- Context: intent, principles, operating model
- Standards: enforceable rules/formats/schemas
- Process: how work is executed and how completion is proven
- Ops: how tools are run and how outputs are interpreted
- Per-job: job-specific truth (what this job does, contracts, validation evidence)

---

## M

### Manifest generator (tool)
A scaffolding tool that performs static analysis on `glue_script.py` to extract job interface facts and produce a draft `job_manifest.yaml`.
Tool category: Scaffolding (per target agent system).
Used by humans and agents to reduce manual manifest authoring.
Location: `tools/manifest-generator/` (if implemented).

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

---

## P

### Pipeline
An ordered set of capabilities required to achieve an objective, including dependencies/decision points where relevant.


### Placeholder (manifest)
A template variable in a job manifest's `bucket` or `key_pattern` field, represented as `${NAME}`.
Placeholders are substituted at job invocation time with actual parameter values or runtime-generated values.
Types: parameter placeholders (match parameter names exactly) and runtime-generated placeholders (computed by the job).

### PySpark
The Python API for Apache Spark, enabling large-scale data processing using Spark's distributed computing engine.
In this system, PySpark jobs run on AWS Glue with access to `SparkContext`, `GlueContext`, and Spark DataFrames.
Runtime type in job manifests: `pyspark`.

### Python Shell (AWS Glue)
A lightweight Glue job type that runs standard Python code without Spark overhead.
Used for tasks that process smaller datasets or orchestrate S3 operations using boto3.
Runtime type in job manifests: `python_shell`.
Distinguished from `pyspark` by absence of SparkContext/GlueContext Spark features.

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

### Runtime truth
The “what actually runs” layer:
the effective behavior defined by code, deployed artifacts, and runtime configuration.

---

## S

### Scope boundary
A statement that makes the objective/capability bounded and unambiguous, including explicit exclusions.

### Separation of concerns
A rule that documentation and artifacts must not mix layers:
- principles/intent,
- enforceable rules,
- execution procedures,
- operational references.
This prevents shadow specs and double truth.


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

### Tool
A deterministic instrument used by humans and agents to scaffold, validate, and produce evidence.
Tools do not invent meaning, interpret intent, or make approval decisions.

---

## V

### Verified / Confirmed
Words that may be used only when explicit evidence is referenced (in the repository or in the conversation).
Otherwise, the correct status is “unverified”, “unknown”, or “TBD”.

### Validation / validation evidence
Validation is the process of checking acceptance criteria and conformance to standards.
Validation evidence is the deterministic output used to support approval decisions.

---


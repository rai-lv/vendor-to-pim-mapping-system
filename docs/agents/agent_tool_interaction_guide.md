# Agent–Tool Interaction Guide

## Purpose

This guide describes how agents should use tools conceptually and what evidence outputs should be produced and referenced during the 5-step workflow.

It clarifies:

- **Tool categories** (scaffolding, validation, evidence) and their distinct purposes,
- **Usage triggers** that indicate when an agent should invoke a tool,
- **Evidence output expectations** for each tool category,
- **The boundary between agents (collaborative roles) and tools (deterministic instruments)**.

This document does **not** contain CLI syntax, installation procedures, or troubleshooting steps. For operational tool details, see `docs/ops/tooling_reference.md` and `docs/ops/ci_automation_reference.md`.

---

## Scope and Authority

This guide is **subordinate** to:
- `docs/context/target_agent_system.md` (defines the agents-vs-tools operating model),
- `docs/agents/agent_role_charter.md` (defines agent role responsibilities).

This guide is **superior** to:
- `docs/ops/tooling_reference.md` (must align with the usage principles defined here).

This guide **references** but does not redefine:
- `docs/context/glossary.md` (shared term definitions),
- `docs/standards/validation_standard.md` (what "verified" means and evidence requirements).

---

## Core Principle: Agents Use Tools, Tools Don't Replace Agents

**Agents** are collaborative roles that reason, propose, draft, implement, and review.

**Tools** are deterministic instruments that:
- generate structured starting points (scaffolding),
- check conformance to defined standards (validation),
- produce reviewable outputs for approval decisions (evidence).

**Key boundary:**
- Tools do not invent requirements, interpret intent, or make approval decisions.
- Agents do not blindly trust tool outputs as "truth"—agents review tool outputs and integrate them into human-facing recommendations and evidence summaries.

---

## Tool Categories

### 1) Scaffolding Tools

**Purpose:** Generate empty or minimally-filled structures to reduce manual effort and ensure consistency with repository standards.

**When agents should use them:**
- When creating a new artifact (e.g., job manifest, business description, script card, codable task).
- When a standard template or structure is defined and a tool exists to generate it.
- To reduce manual transcription errors and accelerate drafting.

**Agent responsibilities when using scaffolding tools:**
- **Review tool output:** Scaffolding tools produce drafts, not final answers. Agents must review and enhance generated content.
- **Resolve placeholders:** Tools may output `TBD`, `null`, or placeholder values. Agents must identify these and either resolve them (if information is available) or flag them for human review.
  - **Information is available when:**
    1. Value is explicitly stated in approved objective/pipeline/capability plan
    2. Value can be directly extracted from existing artifacts without interpretation
    3. Value is specified in referenced standards/specifications
  - **If none of these apply, escalate:** Resolving the placeholder requires a new assumption and must be flagged for human decision
- **Check alignment:** Ensure generated scaffolding aligns with approved intent (objectives, pipeline, capability definitions).
- **Evidence citation:** When referencing scaffolding tool output, cite the tool name and version (if known) and note what was auto-generated vs manually refined.

**Evidence expectations:**
- Agents should **not** claim "this artifact is complete" based solely on tool generation.
- Agents **should** note: "Draft generated using [tool name]; reviewed and enhanced with [specific additions/corrections]."

**Example tools:**
- `manifest-generator` (generates draft `job_manifest.yaml` from `glue_script.py`)

**Example agent usage:**
```
Coding Agent (Step 4): "I used the manifest-generator tool to create a draft job_manifest.yaml 
from the glue_script.py. The tool extracted parameters, I/O operations, and runtime type. 
I reviewed the output and resolved 3 TBD bucket references by cross-checking the script's 
S3 operations. The manifest is now ready for human review."
```

---

### 2) Validation Tools

**Purpose:** Check conformance to repository standards and flag violations deterministically.

**When agents should use them:**
- After completing a logical unit of work (artifact creation or significant modification)
- Before requesting human approval of draft artifacts (Step 1–3)
- After implementing changes, before advancing to Step 5 (Step 4)
- During Step 5 validation to confirm structural and conformance requirements
- Whenever an agent modifies documentation, manifests, or governed artifacts
- Before pushing changes to remote repository (as final check)

**Validation timing sequence:**
1. **During work:** Run validation after completing each logical work unit (e.g., after generating/modifying an artifact)
2. **Before human review:** Ensure artifacts pass validation before requesting approval
3. **Before pushing:** Run final validation check before committing and pushing to remote

This sequence ensures artifacts are validated iteratively during work, not just at final submission.

**Agent responsibilities when using validation tools:**
- **Run validation before approval requests:** Do not ask humans to review artifacts that fail basic validation.
- **Interpret validation output:** Summarize violations in human-readable terms. Do not simply paste raw tool output without context.
- **Fix violations when possible:** If validation identifies missing required fields or formatting issues, fix them before escalation (unless the fix would require new assumptions or change approved intent).
- **Escalate ambiguous violations:** If a validation failure is unclear or conflicts with approved intent, escalate to human decision rather than silently "fixing" it.
- **Evidence citation:** When claiming "this artifact passes validation," cite the tool used and include a summary of checks performed.

**Evidence expectations:**
- Agents **must** reference validation tool output when claiming conformance (e.g., "validated using [tool name], 0 violations found").
- Agents **must not** use "verified" or "confirmed" for conformance without running a validation tool (or citing manual review with explicit evidence).

**Example tools:**
- `validate_repo_docs.py` (validates job manifests, artifacts catalog, job inventory against specs)
- CI automation workflows (syntax validation, standards compliance checks)

**Example agent usage:**
```
Capability Support Agent (Step 3): "I ran validate_repo_docs.py on the draft job_manifest.yaml. 
The tool identified 2 violations: missing 'runtime' field and invalid placeholder syntax. 
I corrected both issues and re-ran validation. The manifest now passes all structural checks 
(0 violations). Evidence: validation report attached."
```

---

### 3) Evidence Tools

**Purpose:** Produce deterministic, reviewable outputs that support approval decisions and verify acceptance criteria.

**When agents should use them:**
- During Step 5 (Validate, Test, and Document) to assemble evidence against acceptance criteria.
- When acceptance criteria require runtime verification (e.g., "job runs successfully," "output file is generated").
- When agents need to demonstrate behavior rather than assert it narratively.

**Agent responsibilities when using evidence tools:**
- **Run evidence tools before claiming success:** Do not declare acceptance criteria satisfied without referenced evidence.
- **Summarize evidence outputs:** Interpret test results, logs, and run receipts in the context of acceptance criteria. Map each criterion to supporting evidence.
- **Identify evidence gaps:** If acceptance criteria cannot be fully covered by available evidence tools, flag the gap explicitly.
- **Escalate contradictions:** If evidence contradicts expectations (e.g., test fails when success was expected), surface the conflict immediately.
- **Evidence citation:** When claiming "acceptance criterion X is met," cite the specific evidence output (e.g., "test log line 42: 'All records processed successfully'").
- **Handle conflicting evidence:** If multiple evidence tools produce conflicting results:
  1. **Report all evidence:** Never suppress or omit conflicting evidence
  2. **Assume failure:** If any evidence tool indicates failure, the overall status is failure
  3. **Investigate discrepancies:** Check for environmental differences, test coverage gaps, or tool configuration issues
  4. **Escalate with full context:** Provide all evidence outputs and investigation notes to human reviewer
  5. **Never claim "verified" with conflicting evidence:** Use "partial verification" or "evidence conflict detected" instead

**Evidence expectations:**
- Agents **must** produce or reference deterministic evidence when using "verified" or "confirmed" (ref: `docs/standards/validation_standard.md`).
- Agents **must not** substitute narrative summaries for actual evidence outputs (e.g., "it looks like it worked" is insufficient).
- Evidence outputs must be reviewable by humans (logs, screenshots, test reports, validation reports).

**Example tools:**
- Test runners (pytest, unittest, integration tests)
- Runtime execution logs and run receipts
- CI automation test workflows
- Manual observation and screenshots (when automated evidence is not available)

**Example agent usage:**
```
Validation Support Agent (Step 5): "I ran the integration test suite to verify acceptance criterion #3: 
'Job processes vendor XML and outputs normalized JSON.' Test result: 12/12 tests passed. 
Evidence: test_vendor_input_processing.log lines 150-162 show successful XML parsing and JSON output 
validation. The output file matches the expected schema defined in the artifacts catalog."
```

---

## Usage Triggers: When to Use Each Tool Type

| Workflow Step | Scaffolding Tools | Validation Tools | Evidence Tools |
|---------------|-------------------|------------------|----------------|
| **Step 1: Define Objective** | Use if objective template exists | Validate objective document structure | Not typically needed (Step 1 is intent-setting) |
| **Step 2: Plan Pipeline** | Use if pipeline template exists | Validate pipeline document structure | Not typically needed (Step 2 is planning) |
| **Step 3: Capability Plans** | Use if codable task template exists | Validate capability definition and task structure | Use if acceptance criteria require evidence collection planning |
| **Step 4: Execute Tasks** | **Use heavily** for artifact generation | **Use after each artifact change** to ensure conformance | Use if runtime verification is part of implementation |
| **Step 5: Validate** | Not typically needed | **Use for all conformance checks** | **Use heavily** to verify acceptance criteria |

---

## Tool Selection When Multiple Options Exist

When multiple tools can provide the same evidence category:

1. **Prefer local validation tools for iterative work:**
   - Run `validate_repo_docs.py` locally during development
   - Use local tools after each logical work unit for fast feedback
   - CI validation serves as final confirmation after all local validation passes

2. **Layer validation tools by scope:**
   - Use targeted tools for specific artifacts (e.g., validate single manifest)
   - Use comprehensive tools for full system checks (e.g., validate all docs)

3. **Reference the most granular evidence available:**
   - Cite specific tool output lines when available
   - Fall back to broader CI results when targeted evidence isn't available

---

## Tool Execution Order

When multiple tool types are needed for a task, follow this sequence to ensure efficient and correct results:

**Standard execution sequence:**
1. **Scaffolding** (if generating new artifacts): Use scaffolding tools to create initial structure
2. **Manual review and enhancement**: Review tool output, resolve placeholders (per criteria above)
3. **Validation** (structure + conformance): Run validation tools to check artifact correctness
4. **Fix violations** (if any): Correct issues identified by validation
5. **Re-validate** (if fixes were made): Confirm fixes resolved all violations
6. **Evidence collection** (if runtime verification needed): Run tests, generate logs, collect evidence
7. **Final validation** (if evidence collection modified artifacts): Ensure generated evidence artifacts also pass validation

**Rationale:**
- Validate before evidence collection to avoid wasting resources testing invalid artifacts
- Re-validate after fixes to confirm resolution
- Validate evidence artifacts to ensure they meet documentation standards

**Example scenario (Step 4 - Creating new job manifest):**
```
1. Run manifest-generator tool → generates draft job_manifest.yaml
2. Review output, resolve TBD values using approved capability plan
3. Run validate_repo_docs.py --manifests → identifies missing 'runtime' field
4. Add missing field based on script analysis
5. Re-run validate_repo_docs.py --manifests → 0 violations
6. (If acceptance criteria require runtime test) Run integration test
7. Validate test output artifacts (if any were generated)
```

---

## Evidence Output Expectations by Validation Category

The `docs/standards/validation_standard.md` defines five validation categories. Agents should understand which tool types produce evidence for each category:

### Structure Validation
**Tools:** Validation tools (e.g., `validate_repo_docs.py`, linters, schema validators)  
**Evidence format:** Validation reports showing pass/fail for required fields, metadata headers, naming conventions  
**Agent action:** Run validation tools before approval; cite tool output in evidence summaries

### Conformance Validation
**Tools:** Validation tools (e.g., schema validators, standard compliance checkers)  
**Evidence format:** Validation reports showing alignment with normative schemas and specifications  
**Agent action:** Run validation tools before approval; fix violations when possible; escalate conflicts

### Consistency Validation
**Tools:** Validation tools (cross-reference checkers, link validators) and manual review  
**Evidence format:** Reports showing cross-document consistency (e.g., "all references resolve")  
**Agent action:** Run cross-reference validation; manually verify logical consistency; flag contradictions

### Runtime Validation
**Tools:** Evidence tools (test runners, runtime execution, log analysis)  
**Evidence format:** Test results, execution logs, run receipts, screenshots, recordings  
**Agent action:** Run tests and capture execution evidence; map evidence to acceptance criteria; escalate failures

### Manual Review Validation
**Tools:** None (human judgment)  
**Evidence format:** Manual review notes, approval records, decision records  
**Agent action:** Request human review; summarize findings for human decision; do not substitute agent judgment for human approval

---

## Evidence Citation Format

When referencing tool outputs in evidence summaries or approval requests, follow the standard citation formats defined in `docs/standards/validation_standard.md` Section 2.5.

The validation standard defines citation templates for:
- Validation tools (structure, conformance checks)
- Evidence tools (tests, runtime verification)
- Scaffolding tools (draft generation)

Using standard citation formats ensures consistency and traceability across all agent outputs and supports evidence discipline requirements.

---

## Anti-Patterns: What Agents Must Not Do

### ❌ Blindly trust scaffolding tool outputs as complete
**Why:** Scaffolding tools produce drafts, often with `TBD` or placeholders. Agents must review and enhance.

### ❌ Skip validation before requesting approval
**Why:** Validation tools catch conformance issues early. Requesting human review of invalid artifacts wastes time.

### ❌ Use "verified" or "confirmed" without citing evidence
**Why:** Evidence discipline requires explicit, reviewable evidence. Narrative claims without evidence violate the validation standard.

### ❌ Reinterpret or "fix" validation failures without escalation
**Why:** If validation conflicts with approved intent, the conflict must be surfaced and resolved explicitly, not silently overridden.

### ❌ Substitute tool outputs for human approval
**Why:** Tools provide evidence; humans make approval decisions. Agents must not treat tool success as automatic approval.

### ❌ Embed tool command syntax in agent outputs
**Why:** Tool manuals belong in `docs/ops/`. Agent outputs should reference tool results conceptually and point to operational docs for CLI details.

---

## When Required Tools Don't Exist

If a needed tool doesn't exist:

1. **Escalate to human review:** Explain the tool gap and request guidance
2. **Document the gap:** Note in task documentation that manual evidence is required
3. **Use manual evidence with extra care:** Provide detailed descriptions, screenshots, or step-by-step verification notes
4. **Never claim "verified" without evidence:** Use "manually reviewed" or "human-inspected" instead of "verified" when automated tools aren't available

---

## Relationship to Other Documents

### This guide complements:
- `docs/agents/agent_role_charter.md` (defines agent responsibilities; this guide explains how to use tools within those responsibilities)
- `docs/context/target_agent_system.md` (defines agents vs tools conceptually; this guide operationalizes that separation)
- `docs/standards/validation_standard.md` (defines what "verified" means; this guide explains how agents produce verification evidence using tools)

### This guide defers to:
- `docs/ops/tooling_reference.md` (for CLI syntax, installation, parameters, troubleshooting)
- `docs/ops/ci_automation_reference.md` (for CI tool behavior, triggers, and output interpretation)

### This guide references:
- `docs/context/glossary.md` (for shared term definitions like "verified," "evidence," "validation categories")

### This guide assumes familiarity with:
- `docs/process/workflow_guide.md` (provides step-by-step execution procedures that this guide supports with tool usage patterns)

---

## Summary

Agents are collaborative roles that accelerate human work by drafting, implementing, and reviewing outputs. Tools are deterministic instruments that agents use to generate scaffolding, validate conformance, and produce evidence.

**Key principles:**
1. **Agents use tools, but tools do not replace agent judgment or human approval.**
2. **Scaffolding tools produce drafts; agents must review and enhance.**
3. **Validation tools must be run before approval requests; agents fix violations when possible and escalate conflicts.**
4. **Evidence tools provide the deterministic outputs required for "verified" and "confirmed" claims.**
5. **Agents cite tool outputs explicitly in evidence summaries, mapping evidence to acceptance criteria.**

For operational tool details (command syntax, parameters, troubleshooting), see `docs/ops/tooling_reference.md`.

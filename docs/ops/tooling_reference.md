# Tooling Reference

**Canonical location:** `docs/ops/`
**Purpose statement:** Technical manual for repo tools and agent-support tools, including usage and troubleshooting.
**Why necessary:** Centralizes operational details and prevents contamination of context/standards docs.
**Must contain:** Tool inventory; usage; parameters; outputs; troubleshooting; version notes.
**Must not contain:** Normative rules that belong in standards.

---

## Tool Inventory

This section catalogs available tools in the repository, their purpose, and location.

### Scaffolding Tools

#### Manifest Generator

**Location:** `tools/manifest-generator/`
**Category:** Scaffolding tool (per `docs/context/target_agent_system.md`)
**Purpose:** Performs static analysis on `glue_script.py` files to extract job interface facts and produce draft `job_manifest.yaml` files.
**Usage patterns:** See `docs/agents/agent_tool_interaction_guide.md` for guidance on when and how agents should use this tool.

**When to use:**
- Creating a new job manifest from an existing or new `glue_script.py`
- Validating consistency between script and manifest
- Detecting drift between code and documented interface

**Usage:**

```bash
# Generate new manifest (output to same directory as script)
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/yourJob/glue_script.py

# Generate with custom output location
python tools/manifest-generator/generate.py \
  --script path/to/glue_script.py \
  --output path/to/manifest.yaml

# Verbose mode (show extraction details)
python tools/manifest-generator/generate.py \
  --script path/to/glue_script.py \
  --verbose

# Override job_id (defaults to folder name)
python tools/manifest-generator/generate.py \
  --script path/to/glue_script.py \
  --job-id custom_job_id
```

**Parameters:**
- `--script PATH` (required): Path to `glue_script.py` to analyze
- `--output PATH` (optional): Output path for generated manifest (default: same directory as script)
- `--update PATH` (optional): Path to existing manifest to update (preserves manual edits)
- `--job-id NAME` (optional): Override job_id (default: parent folder name)
- `--verbose` (optional): Print detailed extraction analysis

**What it extracts:**
- Job ID (from folder name)
- Runtime type (pyspark/python_shell/python from imports)
- Parameters (from `getResolvedOptions()`)
- Input/output S3 operations (boto3 + Spark + helper functions)
- Side effects (deletes, overwrites)
- Run receipt writing
- Config file references
- Evidence notes with script line numbers

**Output:**
- Draft `job_manifest.yaml` conforming to `docs/standards/job_manifest_spec.md`
- Uses `null` for "not applicable" (e.g., receipt bucket when no receipt written)
- Uses `[]` for "provably empty" (e.g., no parameters)
- Uses `TBD` only for truly unknowable values
- Includes `notes` section with evidence citations

**Accuracy:**
- Parameters: ~95% (direct extraction from getResolvedOptions)
- Runtime: ~100% (import analysis)
- I/O Operations: ~80-90% (AST + regex hybrid)
- Overall: Provides ~80% complete draft requiring human review

**Limitations (by design):**
- Some buckets may be `TBD` when not directly traceable
- Complex string operations may need manual review
- Normalized placeholders (`_norm` suffix) not auto-detected
- Conditional I/O may not be fully captured
- **Outputs are drafts for review, not final answers**

**Review checklist after generation:**
- Resolve any `TBD` values
- Verify bucket references (INPUT_BUCKET, OUTPUT_BUCKET)
- Validate key patterns use correct placeholders
- Check format types (xml, json, ndjson, csv)
- Add normalized placeholder suffix (`_norm`) where needed
- Verify config file `repo_path` (null if S3-only)
- Enhance evidence notes with business context

**Documentation:**
- README: `tools/manifest-generator/README.md`
- Quick start: `tools/manifest-generator/QUICKSTART.md`
- Examples: `tools/manifest-generator/examples/`

**Version:** v1 (initial release)

**Requirements:**
- Python 3.8+
- Standard library only (no external dependencies)

**Troubleshooting:**

*Issue:* Tool not detecting S3 operations
*Solution:* Check if script uses helper functions or complex patterns. Tool works best with direct boto3/Spark calls. See examples for supported patterns.

*Issue:* Parameters list is empty
*Solution:* Verify script has `getResolvedOptions()` call. Tool looks for this specific pattern.

*Issue:* Too many TBD values
*Solution:* This is expected! Tool provides draft for human review. TBD means "needs manual verification."

*Issue:* Runtime detection incorrect
*Solution:* Verify imports in script. Tool detects based on: pyspark/SparkContext → pyspark; awsglue.utils without Spark → python_shell; no Glue imports → python.

---

## Validation Tools

### Repository Documentation Validator

**Location:** `tools/validation-suite/validate_repo_docs.py`
**Category:** Validation tool (per `docs/context/target_agent_system.md`)
**Purpose:** Validates repository documentation and artifacts against defined standards and specifications.
**Usage patterns:** See `docs/agents/agent_tool_interaction_guide.md` for guidance on when and how agents should use this tool.

**When to use:**
- Before requesting human approval of draft artifacts
- After modifying job manifests, artifacts catalog, or job inventory
- During Step 5 validation to confirm structural and conformance requirements
- As part of iterative development for fast feedback

**Usage:**

```bash
# Validate all documentation
python tools/validation-suite/validate_repo_docs.py --all

# Validate specific artifact types
python tools/validation-suite/validate_repo_docs.py --manifests
python tools/validation-suite/validate_repo_docs.py --artifacts-catalog
python tools/validation-suite/validate_repo_docs.py --job-inventory

# Security scanning
python tools/validation-suite/validate_repo_docs.py --security

# Show validation coverage report
python tools/validation-suite/validate_repo_docs.py --coverage
```

**Parameters:**
- `--all`: Run all available validations
- `--manifests`: Validate job manifest files against job_manifest_spec.md
- `--artifacts-catalog`: Validate artifacts catalog against artifacts_catalog_spec.md
- `--job-inventory`: Validate job inventory against job_inventory_spec.md
- `--security`: Scan for common security issues (secrets, credentials, SQL injection patterns)
- `--coverage`: Display validation coverage report showing what is/isn't validated

**What it validates:**
- Job manifests: Required fields, placeholder syntax, naming conventions, structural correctness
- Artifacts catalog: Entry schema, content expectations, producer/consumer relationships
- Job inventory: Entry fields, reference links, status semantics
- Security: Credential patterns, hardcoded secrets, SQL injection risks

**Output:**
- Exit code 0: All validations passed
- Exit code 1: Validation failures detected
- Detailed violation reports with file locations and line numbers
- Human-readable summaries of validation results

**Requirements:**
- Python 3.8+
- PyYAML (for manifest parsing)
- Standard library only otherwise

**Version:** Current (check tool for version info)

---

### Documentation Impact Scanner

**Location:** `tools/doc-impact-scanner/`
**Category:** Validation tool (per `docs/context/target_agent_system.md`)
**Purpose:** Identifies all documents potentially affected by a term or concept change. Supports Documentation Support Agent's "Doc Impact Scan" workflows.
**Usage patterns:** See `docs/agents/agent_tool_interaction_guide.md` for guidance on when and how agents should use this tool.

**When to use:**
- After changing terminology, definitions, or concepts in documentation
- During Step 5 validation to check for documentation consistency
- When performing "Doc Impact Scan" per `docs/process/workflow_guide.md` Section 6
- To identify potential "double truth" or contradictions after documentation changes

**Usage:**

```bash
# Basic search for a term
python tools/doc-impact-scanner/scan_doc_impact.py --term <term>

# Quick summary view
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --summary-only

# Search with document context
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --document <path>

# Case-sensitive search
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --case-sensitive

# Adjust context lines
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --context 5
```

**Parameters:**
- `--term TERM` (required): The term or concept to search for
- `--document PATH` (optional): Path to the document that was changed (for context tracking)
- `--context N` (optional): Number of context lines to show before/after each match (default: 2)
- `--case-sensitive` (optional): Perform case-sensitive search (default: case-insensitive)
- `--no-context` (optional): Don't show context lines, just the matching line
- `--summary-only` (optional): Show only summary statistics, not detailed occurrences

**What it does:**
- Searches all markdown files in `docs/` and `.github/agents/`
- Uses whole-word matching (e.g., "agent" won't match "management")
- Extracts context lines before/after each match
- Groups results by file with line numbers
- Provides summary statistics (total occurrences, affected documents)

**Output:**
- Exit code 0: No matches found
- Exit code 1: Matches found (informational, not an error)
- Exit code 2: Error (e.g., docs directory not found)
- Summary view: List of files with occurrence counts
- Detailed view: File paths, line numbers, and context snippets

**Example output:**

```
================================================================================
Documentation Impact Scan Results
================================================================================
Term: 'validation'
Total occurrences: 556
Affected documents: 24
================================================================================

Affected Documents:
--------------------------------------------------------------------------------
  docs/agents/agent_role_charter.md                            (12 occurrences)
  docs/standards/validation_standard.md                        (197 occurrences)
  ...
```

**Typical workflow:**
1. Make documentation change that affects terminology
2. Run scanner: `python tools/doc-impact-scanner/scan_doc_impact.py --term "changed-term" --document path/to/changed.md`
3. Review list of affected documents
4. Update related documentation to maintain consistency
5. Verify no contradictions or "double truth" were introduced

**Documentation:**
- README: `tools/doc-impact-scanner/README.md`
- Per DOCUMENTATION_SYSTEM_ANALYSIS.md Section 2.2.1

**Requirements:**
- Python 3.8+
- Standard library only (no external dependencies)

**Version:** v1 (initial release)

**Troubleshooting:**

*Issue:* Too many matches, hard to review
*Solution:* Use `--summary-only` flag to see just file counts, then run detailed scan on specific high-count files.

*Issue:* Missing expected occurrences
*Solution:* Check if term has different capitalization. By default, search is case-insensitive. Use `--case-sensitive` if needed.

*Issue:* Want to see more/less context
*Solution:* Adjust with `--context N` parameter (default is 2 lines before/after).

---

## Evidence Tools

*[To be documented as evidence tools are created]*

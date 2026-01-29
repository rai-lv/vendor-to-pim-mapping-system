# Manifest Generator Tool

## Purpose

The manifest generator is a **scaffolding tool** that performs static analysis on `glue_script.py` files to extract job interface facts and produce draft `job_manifest.yaml` files.

**Tool Category:** Scaffolding (per `docs/context/target_agent_system.md`)

## What It Does

- Extracts job parameters from `getResolvedOptions()` calls
- Detects runtime type from imports (pyspark vs python_shell)
- Identifies S3 inputs/outputs from boto3 and Spark operations
- Detects side effects (deletes, overwrites)
- Identifies run receipt writing and counters
- Generates evidence notes with script line numbers

## What It Does NOT Do

- Invent values not derivable from code
- Interpret business intent
- Make approval decisions
- Modify existing manifests without explicit --update flag

## Usage

### Generate New Manifest

```bash
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/newJob/glue_script.py \
  --output jobs/vendor_input_processing/newJob/job_manifest.yaml
```

### Update Existing Manifest

```bash
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/existingJob/glue_script.py \
  --update jobs/vendor_input_processing/existingJob/job_manifest.yaml
```

### Options

- `--script PATH`: Path to glue_script.py to analyze (required)
- `--output PATH`: Path where to write new manifest (optional, defaults to same dir as script)
- `--update PATH`: Path to existing manifest to update (preserves manual edits)
- `--job-id NAME`: Override job_id (defaults to parent folder name)
- `--verbose`: Print detailed analysis

## Output

The tool generates a draft manifest conforming to `docs/standards/job_manifest_spec.md`:

- Uses `null` for "not applicable" (e.g., receipt bucket when no receipt written)
- Uses `[]` for "provably empty" (e.g., no parameters)
- Uses `TBD` only for truly unknowable values
- Includes `notes` section with evidence citations (script line numbers)

## Workflow Integration

**Typical usage by Coding Agent:**
1. Agent writes new `glue_script.py` per capability definition
2. Agent invokes: `python tools/manifest-generator/generate.py --script glue_script.py`
3. Tool outputs draft manifest (may have TBDs)
4. Agent reviews output, resolves TBDs where possible, adds business context
5. Human reviews final manifest as part of deliverable approval

## Requirements

- Python 3.8+
- No external dependencies (uses stdlib only: `ast`, `re`, `argparse`, `yaml`)

## Conformance

This tool implements extraction rules from `docs/standards/job_manifest_spec.md` Section 9 (if present) or equivalent deterministic decision trees for automated manifest generation.

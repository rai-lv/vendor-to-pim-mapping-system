# Manifest Generator - Quick Start Guide

## Installation

No installation needed! The tool uses Python standard library only.

**Requirements:**
- Python 3.8+
- Standard library modules: `ast`, `re`, `argparse`, `pathlib`, `yaml`

## Basic Usage

### Generate a New Manifest

```bash
cd /path/to/repo
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/yourJob/glue_script.py
```

This will create `job_manifest.yaml` in the same directory as the script.

### Specify Output Location

```bash
python tools/manifest-generator/generate.py \
  --script path/to/glue_script.py \
  --output path/to/custom_manifest.yaml
```

### Verbose Mode (See Extraction Details)

```bash
python tools/manifest-generator/generate.py \
  --script path/to/glue_script.py \
  --verbose
```

This shows what the tool is detecting in real-time.

## Workflow

### For New Jobs (Coding Agent Usage)

1. **Write glue_script.py** based on capability definition
2. **Run generator:**
   ```bash
   python tools/manifest-generator/generate.py --script glue_script.py
   ```
3. **Review output:**
   - Check extracted parameters
   - Verify input/output patterns
   - Resolve any TBD values
4. **Enhance manifest:**
   - Add business context to notes
   - Fix bucket references (if TBD)
   - Verify format types
5. **Commit both** glue_script.py and job_manifest.yaml

### For Existing Jobs (Validation/Update)

1. **Generate fresh manifest:**
   ```bash
   python tools/manifest-generator/generate.py \
     --script jobs/existing/glue_script.py \
     --output /tmp/generated.yaml
   ```
2. **Compare** with existing manifest
3. **Identify drift** between code and manifest
4. **Update** existing manifest to match current code

## Understanding the Output

### What the Tool Does Well

✅ Extracts parameters from `getResolvedOptions()`
✅ Detects runtime (pyspark vs python_shell)
✅ Finds helper function calls (read_*_from_s3, write_*_to_s3)
✅ Extracts f-string key patterns
✅ Generates evidence notes with line numbers
✅ Applies simple rules (glue_job_name = folder name)

### What Needs Review

⚠️ **Bucket references** - May be TBD if not directly traceable
⚠️ **Config file patterns** - Variable references need resolution
⚠️ **Format types** - Verify json vs ndjson distinction
⚠️ **Normalized placeholders** - Add _norm suffix manually where needed
⚠️ **Conditional I/O** - Complex logic may not be fully captured

### Example Review Checklist

After generation, review the manifest for:
- [ ] All TBD values resolved
- [ ] Bucket references correct (INPUT_BUCKET, OUTPUT_BUCKET)
- [ ] Key patterns use correct placeholders (${param_name})
- [ ] Format types accurate (xml, json, ndjson, csv)
- [ ] Normalized placeholders have _norm suffix where needed
- [ ] Config file repo_path set (null if S3-only)
- [ ] Evidence notes enhanced with business context

## Examples

See `tools/manifest-generator/examples/` for:
- Generated manifests from real jobs
- Comparison with manual manifests
- Pattern recognition examples

## Getting Help

**Issue:** Tool not detecting S3 operations
**Solution:** Check if script uses helper functions or complex patterns. Tool works best with direct boto3/Spark calls.

**Issue:** Parameters list is empty
**Solution:** Verify script has `getResolvedOptions()` call. Tool looks for this specific pattern.

**Issue:** Too many TBD values
**Solution:** This is expected! Tool provides draft for human review. TBD means "needs manual verification."

## Alignment with Repository Principles

This tool is a **scaffolding tool** per `docs/context/target_agent_system.md`:
- Deterministic (same script → same output)
- Evidence-based (cites line numbers)
- Non-interpretive (extracts facts, doesn't invent)
- Review-required (outputs are drafts, not decisions)

The tool accelerates manifest creation but does NOT replace human judgment.

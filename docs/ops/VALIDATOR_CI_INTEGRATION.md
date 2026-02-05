# Validator Integration in CI/CD

## Overview

Documentation validators are integrated into CI/CD workflows to ensure all PRs meet repository standards before merge.

## Current Integration

### Workflows That Run Validators

1. **`pr_validation.yml`** - Comprehensive PR quality gates
   - Trigger: PR opened/synchronized/reopened against main
   - Job: `standards_compliance`
   - Scope: All validation types (except consistency checks)

### Validators Enabled in CI

The following validators run on every PR:

✅ **Job Manifests** (`--manifests`)
- Validates job_manifest.yaml files
- Checks required fields, job_id matching, placeholder syntax
- Ensures TBD explanations are provided

✅ **Artifacts Catalog** (`--artifacts-catalog`)
- Validates docs/catalogs/artifacts_catalog.md
- Checks entry structure and required fields
- Validates purpose is not TBD

✅ **Job Inventory** (`--job-inventory`)
- Validates docs/catalogs/job_inventory.md
- Checks required headings and table structure

✅ **Security Checks** (`--security`)
- Scans Python and YAML files for security issues
- Detects hardcoded credentials, API keys, SQL injection patterns

✅ **Context Layer Documents** (`--context-docs`)
- Validates development_approach.md, target_agent_system.md, system_context.md
- Validates glossary.md with duplicate term detection

✅ **Process Layer Documents** (`--process-docs`)
- Validates workflow_guide.md 5-step structure
- Validates contribution_approval_guide.md

✅ **Agent Layer Documents** (`--agent-docs`)
- Validates agent_role_charter.md
- Validates .github/agents/*.md YAML frontmatter

✅ **Per-Job Documents** (`--job-docs`)
- Validates business descriptions (bus_description_*.md)
- Validates script cards (script_card_*.md)

✅ **Decision Records** (`--decision-records`)
- Validates decision record structure
- Checks decision_log.md index consistency

✅ **Codable Task Specifications** (`--codable-tasks`)
- Validates task specifications per codable_task_spec.md
- Ready for when task files are created

✅ **Naming Standard** (`--naming`)
- Validates job IDs, job groups, script filenames
- Validates artifact filenames, documentation filenames
- Validates placeholder syntax, parameter names
- Checks reserved words, length constraints
- Per docs/standards/naming_standard.md

### Validators NOT Currently Blocking PRs

⚠️ **Cross-Document Consistency** (`--consistency`)
- **Status**: Runs as informational only (does not block PRs)
- **Reason**: Currently finds 26 issues (mostly legitimate broken cross-layer references)
- **Action**: Path resolution improvements and broken reference fixes needed
- **Future**: Will be enabled as blocking check once issues are addressed

## Running Validators Locally

Before submitting a PR, run validators locally:

```bash
# Run all validators (including consistency and naming checks)
python tools/validation-suite/validate_repo_docs.py --all

# Run only blocking validators (same as CI, without consistency)
python tools/validation-suite/validate_repo_docs.py \
  --manifests \
  --artifacts-catalog \
  --job-inventory \
  --security \
  --context-docs \
  --process-docs \
  --agent-docs \
  --job-docs \
  --decision-records \
  --codable-tasks \
  --naming

# Run specific validator
python tools/validation-suite/validate_repo_docs.py --context-docs

# Run naming standard validator
python tools/validation-suite/validate_repo_docs.py --naming

# Check coverage
python tools/validation-suite/validate_repo_docs.py --coverage
```

## Interpreting CI Failures

### Exit Codes

- **Exit 0**: All validations passed ✅
- **Exit 2**: Validation failures detected ❌

### Common Failure Patterns

**1. Job Manifest Issues**
```
FAIL manifest jobs/.../job_manifest.yaml missing_required_keys
```
**Fix**: Add missing required fields to job_manifest.yaml

**2. Security Issues**
```
FAIL security jobs/.../script.py generic_api_key Potential API Key at line X
```
**Fix**: Remove hardcoded credentials, use environment variables

**3. Documentation Structure**
```
FAIL context_docs docs/context/glossary.md duplicate_term
```
**Fix**: Remove duplicate term definitions

**4. Broken References (Informational)**
```
FAIL consistency docs/path/file.md broken_reference Broken reference to 'other.md'
```
**Note**: Currently informational only, will not block PR

**5. Naming Standard Violations**
```
FAIL naming jobs/.../job_manifest.yaml artifact_casing Artifact 'MyFile.json' contains uppercase letters
```
**Fix**: Rename artifacts to use snake_case (e.g., `my_file.json`)

## Validator Coverage

Current coverage: **100% (12/12 validation types implemented)**

See `python tools/validation-suite/validate_repo_docs.py --coverage` for detailed report.

### All Validators

1. ✅ Job Manifests
2. ✅ Artifacts Catalog
3. ✅ Job Inventory
4. ✅ Security Checks
5. ✅ Context Layer Documents
6. ✅ Process Layer Documents
7. ✅ Agent Layer Documents
8. ✅ Per-Job Documents
9. ✅ Decision Records
10. ✅ Codable Task Specifications
11. ✅ Cross-Document Consistency (informational)
12. ✅ Naming Standard (NEW)

## Future Enhancements

### Planned

1. **Enable consistency checks as blocking** - After fixing pre-existing broken references
2. **Add performance benchmarks** - Ensure validators run quickly (<2 minutes)
3. **Incremental validation** - Only validate changed files when possible

### Under Consideration

1. **Severity levels** - Warning vs. error distinction
2. **Custom ignore patterns** - Allow specific files to skip certain checks
3. **Automated fixes** - Auto-fix some violations (e.g., placeholder syntax)

## Related Documentation

- **Validation Standards**: `docs/standards/validation_standard.md`
- **CI Reference**: `docs/ops/ci_automation_reference.md`
- **Workflow Architecture**: `docs/ops/ci_workflow_architecture.md`

## Questions?

For issues with validators or CI integration:
1. Check validator output locally first
2. Review this guide and validation_standard.md
3. Consult with the documentation maintainer or Tech Lead

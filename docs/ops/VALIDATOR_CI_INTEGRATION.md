# Validator Integration in CI/CD

## Overview

Documentation validators are integrated into CI/CD workflows to ensure all PRs meet repository standards before merge.

## Current Integration

### Workflows That Run Validators

1. **`validate_standards.yml`** - Basic validation on every PR
   - Trigger: Every pull request
   - Scope: All validation types (except consistency checks)

2. **`pr_validation.yml`** - Comprehensive PR quality gates
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

### Validators NOT Currently Blocking PRs

⚠️ **Cross-Document Consistency** (`--consistency`)
- **Status**: Runs as informational only (does not block PRs)
- **Reason**: Currently finds 56 pre-existing issues (broken document references)
- **Action**: These will be fixed in a follow-up cleanup task
- **Future**: Will be enabled as blocking check once references are fixed

## Running Validators Locally

Before submitting a PR, run validators locally:

```bash
# Run all validators (including consistency checks)
python tools/validate_repo_docs.py --all

# Run only blocking validators (same as CI)
python tools/validate_repo_docs.py \
  --manifests \
  --artifacts-catalog \
  --job-inventory \
  --security \
  --context-docs \
  --process-docs \
  --agent-docs \
  --job-docs \
  --decision-records \
  --codable-tasks

# Run specific validator
python tools/validate_repo_docs.py --context-docs

# Check coverage
python tools/validate_repo_docs.py --coverage
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

## Validator Coverage

Current coverage: **100% (11/11 validation types implemented)**

See `python tools/validate_repo_docs.py --coverage` for detailed report.

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
- **Workflow Diagram**: `.github/workflows/WORKFLOW_DIAGRAM.md`

## Questions?

For issues with validators or CI integration:
1. Check validator output locally first
2. Review this guide and validation_standard.md
3. Consult with the documentation maintainer or Tech Lead

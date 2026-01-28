# Validation Standard

**Version:** 1.0  
**Last Updated:** 2026-01-27  
**Purpose:** Define validation requirements, tools, and processes for repository documentation and code

---

## Overview

This document defines the validation requirements and tooling for ensuring repository documentation and code compliance with established standards.

---

## Validation Tool

### Tool Location

**Validation Script:** `tools/validate_repo_docs.py`

### Running Validation

To validate all repository documentation:

```bash
python tools/validate_repo_docs.py --all
```

### Validation Scope

The validation tool checks:
- Job manifest compliance with `job_manifest_spec.md`
- Business job description compliance with `business_job_description_spec.md`
- Script card compliance with `script_card_spec.md`
- Artifacts catalog compliance with `artifacts_catalog_spec.md`
- Job inventory compliance with `job_inventory_spec.md`
- Documentation structure and format consistency

---

## CI/CD Integration

### Automated Validation

**CI Workflow:** `.github/workflows/validate_standards.yml`

This workflow runs automatically on:
- Pull request creation
- Pull request updates
- Pushes to main branches

### Pass Criteria

A PR **must not be merged** if validation fails. All validation checks must pass before merging.

---

## Validation Requirements

### For All PRs

Every PR must:
1. Run `python tools/validate_repo_docs.py --all` locally before committing
2. Pass automated CI validation checks
3. Address all validation failures before requesting review

### For New Documentation

When creating new documentation:
1. Identify the relevant specification in `docs/standards/`
2. Follow the specification requirements
3. Run validation to verify compliance
4. Iterate until all checks pass

### For Documentation Updates

When updating existing documentation:
1. Check the relevant spec in `docs/standards/`
2. Update the document per spec requirements
3. Run validation to verify continued compliance
4. Address any new validation failures

---

## Common Validation Workflows

### Adding a New Job

After creating job files:
```bash
# Validate the new job's documentation
python tools/validate_repo_docs.py --all
```

### Updating a Job Manifest

After modifying a manifest:
```bash
# Verify manifest compliance
python tools/validate_repo_docs.py --all
```

### Creating/Updating Documentation

After documentation changes:
```bash
# Validate documentation structure and format
python tools/validate_repo_docs.py --all
```

---

## Troubleshooting Validation Failures

### Reading Validation Output

The validation tool provides:
- **Summary:** Pass/fail count for each validation type
- **Details:** Specific failures with file paths and line numbers
- **Guidance:** References to relevant specification sections

### Resolving Failures

1. Read the validation error message
2. Reference the cited specification in `docs/standards/`
3. Correct the issue per the specification
4. Re-run validation
5. Repeat until all checks pass

---

## References

- **Tool Implementation:** `tools/validate_repo_docs.py`
- **CI Workflow:** `.github/workflows/validate_standards.yml`
- **Related Standards:** All specification files in `docs/standards/`

---

**Note:** This is a living document. As validation requirements evolve, this standard will be updated to reflect current practices.

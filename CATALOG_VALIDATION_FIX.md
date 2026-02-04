# Fix: Catalog Validation Paths

**Date**: 2026-02-04  
**Issue**: Validators for artifacts_catalog.md and job_inventory.md were not working

---

## Problem Identified

The user asked: **"What about additions to job_inventory and artifacts_catalog? Should these not be validated?"**

This question revealed a critical issue: The validators existed but were BROKEN due to incorrect file paths.

---

## Root Cause

**Path Mismatch:**
- **Validators looking for**: `docs/artifacts_catalog.md` and `docs/job_inventory.md`
- **Actual file location**: `docs/catalogs/artifacts_catalog.md` and `docs/catalogs/job_inventory.md`

**Impact:**
- Validators always reported "missing_file" error
- Validation was SKIPPED for these files
- Changes to catalogs were NOT being validated in CI
- New entries were NOT being checked for correctness

---

## Solution Implemented

### 1. Fixed Validator Paths (tools/validate_repo_docs.py)

**Before:**
```python
catalog_path = REPO_ROOT / "docs" / "artifacts_catalog.md"
inventory_path = REPO_ROOT / "docs" / "job_inventory.md"
```

**After:**
```python
catalog_path = REPO_ROOT / "docs" / "catalogs" / "artifacts_catalog.md"
inventory_path = REPO_ROOT / "docs" / "catalogs" / "job_inventory.md"
```

### 2. Updated Error Messages

Error messages now reflect correct paths:
- `docs/catalogs/artifacts_catalog.md` (not `docs/artifacts_catalog.md`)
- `docs/catalogs/job_inventory.md` (not `docs/job_inventory.md`)

### 3. Fixed Non-Conforming File

**artifacts_catalog.md title issue:**
- **Before**: `# Artifacts Catalog (instance)`
- **After**: `# Artifacts Catalog`
- **Reason**: Spec requires exact title per artifacts_catalog_spec.md

---

## Validation Results

### Before Fix
```
FAIL artifacts_catalog ... missing_file docs/artifacts_catalog.md does not exist.
FAIL job_inventory ... missing_file docs/job_inventory.md does not exist.
SUMMARY pass=0 fail=2
```

### After Fix
```
SUMMARY pass=2 fail=0
```

Both validators now **PASS** and properly validate the files! ✅

---

## What Gets Validated Now

### Artifacts Catalog Validation ✅

When changes are made to `docs/catalogs/artifacts_catalog.md`, the validator checks:

1. **File Structure**
   - Top-level title: `# Artifacts Catalog`
   - Entry format: `## <artifact_id>`

2. **Required Fields** (in exact order):
   - artifact_id
   - file_name_pattern
   - s3_location_pattern
   - format
   - producer_job_id
   - producers/consumers
   - presence_on_success
   - purpose
   - content_contract
   - evidence_sources

3. **Optional Governance Fields** (in exact order):
   - producer_glue_job_name
   - stability
   - breaking_change_rules

4. **Content Rules**:
   - Purpose cannot be "TBD"
   - Entries with "producers" field must be in shared artifacts allowlist
   - Field order must match spec exactly

### Job Inventory Validation ✅

When changes are made to `docs/catalogs/job_inventory.md`, the validator checks:

1. **Required Headings** (in exact order):
   - `# Job Inventory`
   - `## Scope and evidence`
   - `## Jobs`
   - `## Dependency links`
   - `## Open verification items`

2. **Jobs Table Structure**:
   - Must have all required columns
   - Columns must be in correct order

---

## CI Integration Status

Both validators are already included in CI workflows:
- ✅ `.github/workflows/pr_validation.yml`
- ✅ `.github/workflows/validate_standards.yml`

**CI commands include:**
```bash
python tools/validate_repo_docs.py \
  --manifests \
  --artifacts-catalog \    # NOW WORKS ✅
  --job-inventory \        # NOW WORKS ✅
  --security \
  ...
```

---

## Impact Summary

### Before This Fix
- ❌ Catalog validators were broken (wrong paths)
- ❌ New entries to catalogs were NOT validated
- ❌ Changes to catalogs could violate specs
- ❌ CI ran validators but they always failed with "missing_file"

### After This Fix
- ✅ Catalog validators work correctly
- ✅ New entries to catalogs ARE validated
- ✅ Changes must conform to specs
- ✅ CI properly validates catalog changes on every PR

---

## Answer to Original Question

**Q: "What about additions to job_inventory and artifacts_catalog? Should these not be validated?"**

**A: YES, they absolutely should be and NOW ARE validated!**

The validators existed in the codebase but were broken. This fix ensures:
- Every addition to artifacts_catalog.md is validated for structure and content
- Every change to job_inventory.md is validated for proper format
- Both catalogs must conform to their respective specs
- CI blocks PRs if catalog changes violate standards

---

## Files Changed

1. `tools/validate_repo_docs.py` - Fixed 4 path references
2. `docs/catalogs/artifacts_catalog.md` - Fixed title to match spec

---

## Validation Coverage Impact

**Full Validation Suite:**
- Before: 45 passes, 8 fails
- After: **47 passes, 6 fails**
- Improvement: +2 passes (artifacts_catalog and job_inventory)

The 6 remaining failures are pre-existing issues documented separately.

---

**Status**: ✅ FIXED AND VERIFIED

# CI Workflow Architecture

## Overview

This document describes the **current** GitHub Actions workflows that automate validation and quality gates in this repository.

**Status**: As of 2026-02-05, **2 primary workflows** are active for PR validation, plus 1 legacy stub.

**Location**: All workflows must be in `.github/workflows/` (GitHub Actions requirement)

---

## Active Workflows

### 1. pr_validation.yml - PR Validation and Quality Gates

**Purpose**: Comprehensive multi-job validation on every pull request

**Trigger**: Automatic on pull requests to main branch

**Jobs**:

1. **Syntax Validation** (CRITICAL - Blocks merge ❌)
   - Python syntax check (`py_compile`)
   - YAML syntax check (`yaml.safe_load`)
   
2. **Standards Compliance** (CRITICAL - Blocks merge ❌)
   - Repository standards validation (10 validator types)
   - Manifest placeholder validation (`${NAME}` syntax)
   
3. **Planning Artifacts Validation** (WARNING - Does not block ⚠️)
   - Objective document structure
   - Pipeline plan structure
   - Capability specification structure
   
4. **Quality Gates** (WARNING - Does not block ⚠️)
   - TODO comment detection
   - Best practices check
   
5. **Testing Validation** (WARNING - Does not block ⚠️)
   - Automated test execution
   - Test result upload
   
6. **Documentation Validation** (WARNING - Does not block ⚠️)
   - Documentation completeness check
   - Code-to-docs synchronization reminder
   
7. **Validation Summary**
   - Aggregates all results
   - Fails if critical gates fail

**Critical Path**: Jobs 1 & 2 must pass for PR to be mergeable

---

### 2. testing_workflow.yml - Testing Agent Workflow

**Purpose**: Execute automated tests and infer test requirements

**Triggers**:
- Manual (workflow_dispatch) - User-initiated testing
- Automatic (pull_request) - When code or specs change

**Actions**:
- `run_tests`: Execute test suite for specifications
- `infer_tests`: Generate test requirements from specifications
- `list_logs`: List available test logs

**Blocking**: No ⚠️ - Used for validation feedback, not enforcement

---

### 3. validate_standards.yml - Legacy Stub (Backwards Compatibility)

**Purpose**: Satisfy legacy GitHub branch protection check requirements

**Status**: **STUB ONLY** - Immediately passes with informational message

**Why It Exists**:
- GitHub branch protection may reference old "validate_standards" check
- Deleting the workflow file causes "Expected — Waiting for status" to show as pending
- This stub satisfies the check while directing users to the actual validation

**Actual Standards Validation**: Performed by `pr_validation.yml` → Standards Compliance job

**Blocking**: No ⚠️ - Always passes (real validation in pr_validation.yml)

---

## Validation Coverage

### What Gets Validated

**Documentation Validators (10 types)**:
1. Job Manifests (`job_manifest.yaml`)
2. Artifacts Catalog
3. Job Inventory
4. Security Checks (credentials, SQL injection)
5. Context Layer Documents
6. Process Layer Documents
7. Agent Layer Documents
8. Per-Job Documents
9. Decision Records
10. Codable Task Specifications

**Note**: Cross-document consistency checker (11th validator) runs informational only

**Code Quality**:
- Python syntax
- YAML syntax
- Placeholder style
- TODO comments

---

## Quality Gate Enforcement

```
┌────────────────────────┬─────────────────┬──────────────┬──────────────┐
│ Validation Type        │ Workflow        │ Severity     │ Blocks Merge │
├────────────────────────┼─────────────────┼──────────────┼──────────────┤
│ Python Syntax          │ pr_validation   │ CRITICAL     │ YES ❌       │
│ YAML Syntax            │ pr_validation   │ CRITICAL     │ YES ❌       │
│ Standards Compliance   │ pr_validation   │ CRITICAL     │ YES ❌       │
│ Manifest Placeholders  │ pr_validation   │ CRITICAL     │ YES ❌       │
│ Planning Structure     │ pr_validation   │ WARNING      │ NO ⚠️        │
│ TODO Comments          │ pr_validation   │ WARNING      │ NO ⚠️        │
│ Best Practices         │ pr_validation   │ WARNING      │ NO ⚠️        │
│ Testing                │ pr_validation   │ WARNING      │ NO ⚠️        │
│                        │ testing_wf      │              │              │
│ Documentation          │ pr_validation   │ WARNING      │ NO ⚠️        │
└────────────────────────┴─────────────────┴──────────────┴──────────────┘
```

---

## Workflow Interaction

```
                          Pull Request Created
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
           ┌──────────────┐           ┌──────────────┐
           │ pr_validation│           │testing_wf    │
           │  (7 jobs)    │           │ (1 job)      │
           └──────────────┘           └──────────────┘
                     │                         │
                     └─────────────┬───────────┘
                                   │
                           ┌───────┴────────┐
                           │                │
                           ▼                ▼
                     PASS ✅           FAIL ❌
                  (Can merge)     (Cannot merge)
```

---

## Future Planned Workflows

The following workflows are documented in planning materials but **not yet implemented**:

- `planner_workflow.yml` - Step 1: Define Objective
- `pipeline_planner_workflow.yml` - Step 2a: Pipeline Plan
- `capability_planner_workflow.yml` - Step 2b: Capability Specification
- `coding_workflow.yml` - Steps 3-4: Task decomposition
- `designer_workflow.yml` - Design artifacts
- `documentation_workflow.yml` - Documentation generation

**Note**: These represent a future vision for the CI/CD pipeline automation.

---

## Related Documentation

- **Validator Integration**: `docs/ops/VALIDATOR_CI_INTEGRATION.md`
- **CI Reference**: `docs/ops/ci_automation_reference.md`
- **Validation Standards**: `docs/standards/validation_standard.md`
- **Workflow Guide**: `docs/process/workflow_guide.md`

---

## Maintenance Notes

**Last Updated**: 2026-02-05

**Current State**: 
- 2 active validation workflows (`pr_validation.yml`, `testing_workflow.yml`)
- 1 legacy stub workflow (`validate_standards.yml` - backwards compatibility only)
- 10 of 11 documentation validators enabled as blocking checks
- Critical path: Syntax + Standards compliance must pass
- **Note**: `validate_standards.yml` is a stub that immediately passes; actual validation in `pr_validation.yml`

**Upcoming**:
- Repository admin should remove `validate_standards` from branch protection rules (if configured)
- Enable cross-document consistency checker once broken references are fixed
- Consider implementing planning phase workflows as repository matures

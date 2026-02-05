# CI Workflow Architecture

## Overview

This document describes the **current** GitHub Actions workflows that automate validation and quality gates in this repository.

**Status**: As of 2026-02-05, only **1 workflow** is active for PR validation.

**Location**: All workflows must be in `.github/workflows/` (GitHub Actions requirement)

---

## Active Workflows

### pr_validation.yml - PR Validation and Quality Gates

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
   
5. **Validation Summary**
   - Aggregates all results
   - Fails if critical gates fail

**Critical Path**: Jobs 1 & 2 must pass for PR to be mergeable

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
- 2 active workflows providing comprehensive PR validation
- 10 of 11 documentation validators enabled as blocking checks
- Critical path: Syntax + Standards compliance must pass
- Removed redundant `validate_standards.yml` (duplicate of `pr_validation.yml` standards_compliance job)

**Upcoming**:
- Enable cross-document consistency checker once broken references are fixed
- Consider implementing planning phase workflows as repository matures

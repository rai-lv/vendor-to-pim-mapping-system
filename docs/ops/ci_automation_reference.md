# CI / Automation Reference

**Purpose:** Explain what automation runs, what evidence it produces, and how to interpret failures.

**Scope note:** This file only contains the operational CI/validation guidance that previously lived in System Context. Any normative validation rules remain in `docs/standards/validation_standard.md`.

---

## Automation Overview

This repository uses GitHub Actions for continuous integration with the primary workflow:

**PR Validation and Quality Gates** (`.github/workflows/pr_validation.yml`)
- Primary CI workflow that enforces standards and quality gates
- Runs comprehensive validation on all pull requests
- Multi-job pipeline with dependency management

---

## Triggers

### PR Validation Workflow

**Trigger conditions:**
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
    branches:
      - main
```

**Jobs and their conditional triggers:**
- `syntax_validation`: Always runs on PR events
- `standards_compliance`: Runs after syntax validation
- `planning_validation`: Conditional - only if changes in `docs/roadmaps/` or `docs/specifications/`
- `quality_gates`: Conditional - only if changes in `jobs/` or `tools/`
- `validation_summary`: Always runs after all jobs complete (uses `if: always()`)

---

## Produced Artifacts

### PR Validation Workflow

1. **Console Outputs**
   - Syntax validation results (Python and YAML files)
   - Standards compliance reports
   - Placeholder style validation results
   - Quality gate warnings (TODO comments)

---

## Failure Interpretation

### Common Failure Modes

#### 1. Syntax Validation Failures

**Python syntax errors:**
```
❌ Syntax error in jobs/example/script.py
```
**Cause:** Invalid Python syntax (syntax errors, indentation issues)
**Location:** Check the specific file mentioned in error output

**YAML syntax errors:**
```
❌ Syntax error in jobs/example/manifest.yaml
```
**Cause:** Invalid YAML structure (indentation, quotes, special characters)
**Location:** Check the specific file mentioned in error output

#### 2. Standards Compliance Failures

**Repository standards validation:**
- Failures from `validate_repo_docs.py` indicate violations of documentation standards
- Error messages specify which validator failed and what file/content violated the standard
- Common issues: missing required sections, incorrect file placement, schema violations

**Placeholder style violations:**
```
❌ Found incorrect placeholder style <name>. Use ${NAME} instead.
❌ Found incorrect placeholder style {name}. Use ${NAME} instead.
```
**Cause:** Using deprecated placeholder syntax in manifest files

**Consistency check warnings:**
- Cross-document consistency checks run as informational only (`continue-on-error: true`)
- May report pre-existing issues not related to your changes

#### 3. Planning Validation Failures

**Objective definition issues:**
```
❌ Missing 'Objective Statement' section in docs/roadmaps/example.md
```
**Required sections:** Objective Statement, Expected Outcomes, Out-of-Scope, Success Criteria

**Pipeline plan issues:**
```
❌ Missing 'Processing Sequence' section in docs/roadmaps/example_pipeline_plan.md
```
**Required sections:** Processing Sequence, Conceptual Artifacts (or Artifacts)

**Capability specification issues:**
```
❌ Missing required fields in docs/specifications/example_capability.yaml: ['inputs']
```
**Required fields:** objective, inputs, outputs, acceptance_criteria

#### 4. Quality Gate Failures

**TODO comments detected:**
```
⚠️ Found 5 TODO comments:
jobs/example/script.py:42: TODO: implement error handling
```
**Note:** These produce warnings but don't fail the build

**Best practices violations:**
- Coding agent checks coding standards
- May produce warnings without failing the build

#### 5. Quality Gate Failures

**TODO comments detected:**
```
⚠️ Found 5 TODO comments:
jobs/example/script.py:42: TODO: implement error handling
```
**Note:** These produce warnings but don't fail the build

---

## Remediation Patterns

### Pattern 1: Syntax Error Remediation

**For Python syntax errors:**
1. Locate the file and line number from error output
2. Run local syntax check: `python -m py_compile <file>`
3. Fix syntax issues (common: missing colons, parentheses, indentation)
4. Test locally before pushing

**For YAML syntax errors:**
1. Locate the file from error output
2. Validate locally: `python -c "import yaml; yaml.safe_load(open('<file>'))"`
3. Common issues: incorrect indentation, unquoted special characters, missing spaces after colons
4. Use YAML linter or validator for complex files

### Pattern 2: Standards Compliance Remediation

**For placeholder style violations:**
1. Search for incorrect patterns: `grep -r "<[a-zA-Z_]" jobs/ --include="*.yaml"`
2. Replace with correct style:
   - `<name>` → `${NAME}`
   - `{name}` → `${NAME}`
3. Ensure capitalization follows naming standard

**For repository standards failures:**
1. Review error message for specific validator and violation
2. Consult `docs/standards/validation_standard.md` for requirements
3. Run validator locally: `python tools/validation-suite/validate_repo_docs.py --<validator>`
4. Fix violations and re-run until passing

### Pattern 3: Planning Artifact Remediation

**For missing sections:**
1. Identify document type (objective, pipeline plan, capability spec)
2. Add required sections as specified in error message
3. Consult template or existing documents for section structure
4. Verify all required sections present before pushing

**For capability spec field issues:**
1. Open YAML file in editor
2. Add missing required fields: objective, inputs, outputs, acceptance_criteria
3. Validate YAML structure locally
4. Ensure conformance to capability specification schema

### Pattern 4: Quality Gate Remediation

**For TODO comments:**
1. Review TODO comments listed in output
2. Options:
   - Resolve TODO and implement required functionality
   - Create issue for future work and remove TODO
   - If intentional, convert to tracked issue reference
3. Goal: Zero TODOs before merge (policy dependent)

### General Remediation Strategy

1. **Identify failure type** from job name and error message
2. **Review detailed logs** in GitHub Actions workflow output
3. **Reproduce locally** using commands from workflow steps
4. **Fix issues** following specific remediation pattern
5. **Verify fix locally** before pushing
6. **Push changes** and monitor re-run of CI workflow

---

## Standards Validation (CI Gate)

Every PR **must pass** automated validation. See `docs/standards/validation_standard.md` for validation requirements, tools, and CI integration details.

Critical validations (must pass for merge):
- Syntax validation
- Standards compliance

Other validations provide warnings and guidance but may not block merge depending on conditions.

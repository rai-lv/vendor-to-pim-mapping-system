# GitHub Actions Workflow Integration Diagram

## High-Level Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      PLANNING PHASE (Manual Approval Required)          │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 1: Define Objective                                          │ │
│  │ Workflow: planner_workflow.yml                                    │ │
│  │ Trigger: Manual (workflow_dispatch)                               │ │
│  │                                                                    │ │
│  │ Actions:                                                           │ │
│  │  1. Create objective document template                            │ │
│  │  2. Validate document structure                                   │ │
│  │  3. Commit to repository                                          │ │
│  │                                                                    │ │
│  │ Output: docs/roadmaps/<objective>.md                              │ │
│  │                                                                    │ │
│  │ ✋ MANUAL CHECKPOINT:                                              │ │
│  │    - Review document with stakeholders                            │ │
│  │    - Fill in all TODO sections                                    │ │
│  │    - Obtain explicit approval                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                   ↓                                     │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 2a: Pipeline Plan                                            │ │
│  │ Workflow: pipeline_planner_workflow.yml                           │ │
│  │ Trigger: Manual (workflow_dispatch)                               │ │
│  │                                                                    │ │
│  │ Prerequisites Validated:                                           │ │
│  │  ✓ Step 1 objective document exists                               │ │
│  │  ✓ Step 1 document has required sections                          │ │
│  │                                                                    │ │
│  │ Actions:                                                           │ │
│  │  1. Validate Step 1 prerequisites                                 │ │
│  │  2. Create pipeline plan template                                 │ │
│  │  3. Validate pipeline plan structure                              │ │
│  │  4. Commit to repository                                          │ │
│  │                                                                    │ │
│  │ Output: docs/roadmaps/<objective>_pipeline_plan.md                │ │
│  │                                                                    │ │
│  │ ✋ MANUAL CHECKPOINT:                                              │ │
│  │    - Define processing sequence                                   │ │
│  │    - Define decision points and conceptual artifacts              │ │
│  │    - Review with Tech Lead and Architect                          │ │
│  │    - Obtain explicit approval                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                   ↓                                     │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 2b: Capability Specification                                 │ │
│  │ Workflow: capability_planner_workflow.yml                         │ │
│  │ Trigger: Manual (workflow_dispatch) - Repeat for each capability  │ │
│  │                                                                    │ │
│  │ Prerequisites Validated:                                           │ │
│  │  ✓ Step 2a pipeline plan exists                                   │ │
│  │  ✓ Step 2a plan has required sections                             │ │
│  │                                                                    │ │
│  │ Actions:                                                           │ │
│  │  1. Validate Step 2a prerequisites                                │ │
│  │  2. Create capability specification template                      │ │
│  │  3. Validate specification structure                              │ │
│  │  4. Commit to repository                                          │ │
│  │                                                                    │ │
│  │ Output: docs/specifications/<capability>_capability.yaml          │ │
│  │                                                                    │ │
│  │ ✋ MANUAL CHECKPOINT:                                              │ │
│  │    - Define inputs/outputs, business rules, criteria              │ │
│  │    - Review with Tech Lead and QA Lead                            │ │
│  │    - Obtain explicit approval                                     │ │
│  │    - Repeat for all capabilities in pipeline                      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      IMPLEMENTATION PHASE (Automated Support)           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 3: Decompose into Development Elements                       │ │
│  │ Workflow: coding_workflow.yml (action: list_tasks)                │ │
│  │ Trigger: Manual (workflow_dispatch)                               │ │
│  │                                                                    │ │
│  │ Prerequisites Validated:                                           │ │
│  │  ✓ Step 2b capability specification exists                        │ │
│  │                                                                    │ │
│  │ Actions:                                                           │ │
│  │  1. Validate Step 2b prerequisites                                │ │
│  │  2. List development tasks for capability                         │ │
│  │  3. Display suggested decomposition                               │ │
│  │                                                                    │ │
│  │ Output: Console output with task breakdown                        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                   ↓                                     │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 4: Create Codex Tasks                                        │ │
│  │ Workflow: coding_workflow.yml (action: generate_codex_task)       │ │
│  │ Trigger: Manual (workflow_dispatch)                               │ │
│  │                                                                    │ │
│  │ Prerequisites Validated:                                           │ │
│  │  ✓ Step 3 decomposition complete                                  │ │
│  │                                                                    │ │
│  │ Actions:                                                           │ │
│  │  1. Validate prerequisites                                        │ │
│  │  2. Generate Codex task specification                             │ │
│  │  3. Display task with standards and quality gates                 │ │
│  │                                                                    │ │
│  │ Output: Console output with Codex task specification              │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      VALIDATION PHASE (Automated Quality Gates)         │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ STEP 5: Code Creation and PR Validation                           │ │
│  │ Trigger: Automatic on pull_request                                │ │
│  │                                                                    │ │
│  │ ┌─────────────────────────────────────────────────────────────┐   │ │
│  │ │ pr_validation.yml (Comprehensive Validation)                │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 1: Syntax Validation (CRITICAL)                         │   │ │
│  │ │  • Python syntax check (py_compile)                         │   │ │
│  │ │  • YAML syntax check (yaml.safe_load)                       │   │ │
│  │ │  ❌ Blocks merge if fails                                   │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 2: Standards Compliance (CRITICAL)                      │   │ │
│  │ │  • validate_repo_docs.py --all                              │   │ │
│  │ │  • Manifest placeholder validation (${NAME})                │   │ │
│  │ │  ❌ Blocks merge if fails                                   │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 3: Planning Artifacts Validation                        │   │ │
│  │ │  • Objective document structure                             │   │ │
│  │ │  • Pipeline plan structure                                  │   │ │
│  │ │  • Capability specification structure                       │   │ │
│  │ │  ⚠️  Warnings only                                          │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 4: Quality Gates                                        │   │ │
│  │ │  • TODO comment detection                                   │   │ │
│  │ │  • Best practices check                                     │   │ │
│  │ │  ⚠️  Warnings only                                          │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 5: Testing Validation                                   │   │ │
│  │ │  • testing_agent.py run                                     │   │ │
│  │ │  • Upload test results                                      │   │ │
│  │ │  ⚠️  Warnings only                                          │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 6: Documentation Validation                             │   │ │
│  │ │  • documentation_agent.py validate                          │   │ │
│  │ │  • Check for doc updates                                    │   │ │
│  │ │  ⚠️  Warnings only                                          │   │ │
│  │ │                                                             │   │ │
│  │ │ Job 7: Validation Summary                                   │   │ │
│  │ │  • Summarize all results                                    │   │ │
│  │ │  • Display pass/fail status                                 │   │ │
│  │ │  ❌ Fails if critical gates fail                            │   │ │
│  │ └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                    │ │
│  │ ┌─────────────────────────────────────────────────────────────┐   │ │
│  │ │ testing_workflow.yml (Automated Testing)                    │   │ │
│  │ │  • Runs on PR and push to main                              │   │ │
│  │ │  • Executes test suite                                      │   │ │
│  │ │  • Uploads test logs                                        │   │ │
│  │ └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                    │ │
│  │ ┌─────────────────────────────────────────────────────────────┐   │ │
│  │ │ documentation_workflow.yml (Documentation Checks)           │   │ │
│  │ │  • On PR: Shows documentation reminder                      │   │ │
│  │ │  • On push: Validates documentation                         │   │ │
│  │ └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                    │ │
│  │ ┌─────────────────────────────────────────────────────────────┐   │ │
│  │ │ validate_standards.yml (Standards Validation)               │   │ │
│  │ │  • Runs on all PRs                                          │   │ │
│  │ │  • Validates repository standards                           │   │ │
│  │ │  ❌ Blocks merge if fails                                   │   │ │
│  │ └─────────────────────────────────────────────────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Workflow Trigger Summary

```
┌─────────────────────────┬─────────────────────┬──────────────────────────┐
│ Workflow                │ Trigger Type        │ When                     │
├─────────────────────────┼─────────────────────┼──────────────────────────┤
│ planner_workflow.yml    │ Manual              │ User runs from Actions   │
│ pipeline_planner_...yml │ Manual              │ User runs from Actions   │
│ capability_planner...yml│ Manual              │ User runs from Actions   │
│ coding_workflow.yml     │ Manual + Auto       │ User runs + spec changes │
│ pr_validation.yml       │ Automatic           │ Every PR                 │
│ testing_workflow.yml    │ Manual + Auto       │ User runs + PR + push    │
│ documentation_...yml    │ Manual + Auto       │ User runs + PR + push    │
│ validate_standards.yml  │ Automatic           │ Every PR                 │
│ designer_workflow.yml   │ Manual + Auto       │ User runs + roadmap push │
└─────────────────────────┴─────────────────────┴──────────────────────────┘
```

## Quality Gate Enforcement

```
┌────────────────────────┬─────────────┬──────────────┬──────────────┐
│ Quality Gate           │ Workflow    │ Severity     │ Blocks Merge │
├────────────────────────┼─────────────┼──────────────┼──────────────┤
│ Python Syntax          │ pr_valid... │ CRITICAL     │ YES ❌       │
│ YAML Syntax            │ pr_valid... │ CRITICAL     │ YES ❌       │
│ Standards Compliance   │ pr_valid... │ CRITICAL     │ YES ❌       │
│                        │ validate... │              │              │
│ Manifest Placeholders  │ pr_valid... │ CRITICAL     │ YES ❌       │
│ Planning Structure     │ pr_valid... │ WARNING      │ NO ⚠️        │
│ TODO Comments          │ pr_valid... │ WARNING      │ NO ⚠️        │
│ Best Practices         │ pr_valid... │ WARNING      │ NO ⚠️        │
│ Testing                │ pr_valid... │ WARNING      │ NO ⚠️        │
│                        │ testing...  │              │              │
│ Documentation          │ pr_valid... │ WARNING      │ NO ⚠️        │
│                        │ document... │              │              │
└────────────────────────┴─────────────┴──────────────┴──────────────┘
```

## Manual Approval Checkpoints

```
┌─────────┬──────────────────────┬────────────────────────────────────┐
│ Step    │ Workflow             │ Manual Approval Required           │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 1  │ planner_workflow     │ ✋ Review objective with           │
│         │                      │    stakeholders (Product, Tech,    │
│         │                      │    Business)                       │
│         │                      │ ✋ Fill in all TODO sections        │
│         │                      │ ✋ Obtain explicit approval         │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 2a │ pipeline_planner     │ ✋ Define processing sequence       │
│         │                      │ ✋ Review with Tech Lead, Architect │
│         │                      │ ✋ Obtain explicit approval         │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 2b │ capability_planner   │ ✋ Define inputs, outputs, rules    │
│         │                      │ ✋ Review with Tech Lead, QA        │
│         │                      │ ✋ Obtain explicit approval         │
│         │                      │ ✋ Repeat for each capability       │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 3  │ coding_workflow      │ Review decomposition suggestion    │
│         │                      │ (No formal approval required)      │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 4  │ coding_workflow      │ Review Codex task specification    │
│         │                      │ (No formal approval required)      │
├─────────┼──────────────────────┼────────────────────────────────────┤
│ Step 5  │ pr_validation +      │ ✋ Code review                      │
│         │ other workflows      │ ✋ Review validation results        │
│         │                      │ ✋ Merge decision                   │
└─────────┴──────────────────────┴────────────────────────────────────┘
```

## Automation Boundaries

```
┌─────────────────────────────────┬─────────────────────────────────────┐
│ AUTOMATED (Workflows Handle)    │ MANUAL (Humans Decide)              │
├─────────────────────────────────┼─────────────────────────────────────┤
│ • Template generation           │ • Objective content                 │
│ • Structure validation          │ • Pipeline architecture             │
│ • Syntax checking               │ • Capability specifications         │
│ • Standards compliance          │ • Business rules                    │
│ • Testing execution             │ • Acceptance criteria               │
│ • Documentation validation      │ • Approval decisions                │
│ • Quality gate enforcement      │ • Code review                       │
│ • Prerequisite validation       │ • Merge decisions                   │
│ • Error detection               │ • Strategic planning                │
│ • Log generation                │ • Stakeholder consensus             │
└─────────────────────────────────┴─────────────────────────────────────┘
```

## Success Criteria

```
✅ Planning Phase (Steps 1-2b)
   ✓ Workflows create templates
   ✓ Workflows validate structure
   ✓ Workflows enforce prerequisites
   ✓ Manual approval checkpoints preserved
   ✓ Cannot skip planning steps

✅ Implementation Phase (Steps 3-4)
   ✓ Workflows validate prerequisites
   ✓ Workflows provide guidance
   ✓ Workflows suggest decomposition
   ✓ Workflows generate task specs

✅ Validation Phase (Step 5)
   ✓ Comprehensive PR validation
   ✓ Critical gates block merge
   ✓ Warning gates inform decisions
   ✓ All validations run automatically
   ✓ Clear pass/fail summary

✅ Documentation
   ✓ Comprehensive workflow guide
   ✓ Implementation summary
   ✓ Clear usage examples
   ✓ Troubleshooting assistance
```

---

**Last Updated:** 2026-01-27
**Version:** 1.0

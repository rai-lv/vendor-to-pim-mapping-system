# Fix Summary: Manual Observation Classification

**Date:** 2026-02-04  
**Issue:** Manual observation incorrectly classified as evidence tool  
**Status:** ✅ RESOLVED  

---

## Problem Identified

Manual observation was listed as an "evidence tool" creating a direct conflict with evidence discipline:

1. **Definition conflict:**
   - Evidence tools defined as producing "deterministic, reviewable outputs"
   - Manual observation is inherently non-deterministic (human judgment)

2. **Risk:**
   - Could justify "verified" claims without deterministic evidence
   - Violated evidence discipline rules requiring reproducible outputs

3. **Existing correct classification:**
   - Manual Review Validation already exists as separate category
   - Uses "None (human judgment)" as tools
   - Produces "Manual review notes, approval records, decision records"

---

## Changes Made

### 1. glossary.md - Evidence Tools Definition

**Before:**
```markdown
Evidence tools include test runners, runtime execution logs, CI automation 
test workflows, and manual observation methods.
```

**After:**
```markdown
Evidence tools include test runners, runtime execution logs, and CI automation 
test workflows.
Required for claims of "verified" or "confirmed" status.
Note: Manual observation and screenshots are part of manual review validation 
(not evidence tools), as they rely on human judgment rather than deterministic 
tool outputs.
```

### 2. agent_tool_interaction_guide.md - Evidence Tools Examples

**Before:**
```markdown
**Example tools:**
- Test runners (pytest, unittest, integration tests)
- Runtime execution logs and run receipts
- CI automation test workflows
- Manual observation and screenshots (when automated evidence is not available)
```

**After:**
```markdown
**Example tools:**
- Test runners (pytest, unittest, integration tests)
- Runtime execution logs and run receipts
- CI automation test workflows

**Note on manual observation:** Manual observation and screenshots are part of 
**Manual Review Validation** (not evidence tools), as they rely on human 
judgment rather than deterministic tool outputs. See the "Manual Review 
Validation" section for guidance on manual evidence.
```

### 3. agent_tool_interaction_guide.md - Runtime Validation Evidence Format

**Before:**
```markdown
**Evidence format:** Test results, execution logs, run receipts, screenshots, recordings
```

**After:**
```markdown
**Evidence format:** Test results, execution logs, run receipts, automated 
screenshots/recordings (from test tools)
```

**Rationale:** Clarifies that screenshots in runtime validation come from automated 
test tools (deterministic), not manual observation (non-deterministic).

---

## Verification

### Consistency Check ✅

1. **Evidence tools definition:** Now lists only deterministic tools
2. **Manual observation:** Correctly categorized under Manual Review Validation
3. **Evidence discipline:** Preserved - only deterministic outputs support "verified" claims
4. **Existing guidance:** Section "When Required Tools Don't Exist" already correctly states:
   - Use "manually reviewed" or "human-inspected" instead of "verified"
   - When automated tools aren't available

### Cross-Document Alignment ✅

- ✅ glossary.md: Evidence tools = deterministic only
- ✅ agent_tool_interaction_guide.md: Manual observation → Manual Review Validation
- ✅ validation_standard.md: Manual Review Validation already separate (no changes needed)
- ✅ No conflicts with evidence discipline rules

---

## Impact

**Before the fix:**
- ❌ Ambiguous classification allowed non-deterministic "evidence tools"
- ❌ Could justify "verified" without reproducible outputs
- ❌ Violated core evidence discipline principle

**After the fix:**
- ✅ Clear separation: Evidence tools = deterministic, Manual review = human judgment
- ✅ "Verified" claims require deterministic evidence (no exceptions)
- ✅ Manual observation properly categorized and cannot bypass evidence requirements

---

## Document Types Affected

1. **glossary.md** (context layer) - Term definition corrected
2. **agent_tool_interaction_guide.md** (agent layer) - Behavioral guidance clarified

**Change classification:** Wording/clarity improvement (correcting categorization, no meaning change to evidence discipline)

---

**END OF SUMMARY**

# Script Card Spec Rework Summary

## What Changed

The `docs/standards/script_card_spec.md` has been completely reworked to provide:

1. **Clearer operational focus** - Emphasis on runtime behavior, invariants, failure modes, and observability
2. **Stronger boundaries** - Explicit separation from business descriptions, artifact contracts, and ops documentation
3. **Better structure** - 10 normative required sections with clear pass criteria
4. **Prevention of "double truth"** - Explicit exclusions prevent duplication across documentation types

## Key Improvements

### 1. Expanded Scope Clarity (Section 0-1)
- Defines what script cards ARE (operational + interface reference)
- Defines what script cards are NOT (business rationale, schemas, tool commands)
- Three explicit boundary rules:
  - Boundary rule: No business justification (belongs in business descriptions)
  - Interface rule: Reference artifacts, don't define them (belongs in artifacts catalog)
  - Observability rule: Describe signals conceptually, not CLI commands (belongs in ops)

### 2. Enhanced Required Sections (Section 2)
**Previous version:** 10 sections with basic requirements

**New version:** 10 sections with detailed requirements, including:
- **2.1 Identity:** Added `runtime` field, clearer field descriptions
- **2.2 Purpose:** Emphasis on observable outcomes vs business intent
- **2.4 Inputs / 2.5 Outputs:** Added `artifact_id` field for cross-referencing artifacts catalog
- **2.7 Runtime Behavior:** Explicit anti-pattern examples (no code-level detail)
- **2.8 Invariants:** Clearer "externally meaningful" requirement
- **2.9 Failure Modes and Observability:** Split into 4 subfields for better structure
- **2.10 References:** Added `business_description` cross-reference

### 3. New Sections

#### Section 3: Explicit Exclusions (MUST NOT)
Seven explicit things script cards must NOT contain to prevent double truth:
1. Global term definitions → glossary
2. Full artifact schemas → artifacts catalog
3. Business justification → business descriptions
4. Future improvements → not Phase 1 documentation
5. Speculative statements → use TBD
6. CLI commands/troubleshooting → ops docs
7. Artifact contract redefinitions → artifacts catalog

#### Section 5: Formatting and Structure Rules
- File naming conventions
- Markdown structure requirements
- Placeholder representation (${placeholder_name})
- TBD discipline
- Cross-reference formatting

#### Section 6: Compatibility and Breaking Changes
- Defines what constitutes breaking changes to spec structure
- Non-breaking changes identified
- Versioning approach (git-based)

#### Section 7: Enforcement and Validation
- Validation approach for automated tooling
- Human review checkpoints
- Relationship to validation standard

#### Section 8: Migration Guidance
- How to upgrade from previous version
- Handling TBDs during retroactive documentation

#### Section 9: Open Items / TBD
Three explicit questions requiring human decisions:
1. Run receipt format standardization
2. Validation tooling scope (cardinality enforcement)
3. Cross-job dependency representation (manual vs automatic)

#### Consistency Check Appendix
Comprehensive alignment verification:
- **9 documents aligned with:** Development Approach, Documentation System Catalog, Glossary, Target Agent System, Workflow Guide, Artifacts Catalog Spec, Job Manifest Spec, Naming Standard, Documentation Spec
- **Zero conflicts detected**
- **2 assumptions introduced** (both bounded and explicitly labeled)
- **6 exclusions documented** (preventing double truth)
- **4 cross-document impact notes** (recommended follow-up actions)

## Statistics

- **Line count:** 624 lines (was 165 lines)
- **Net change:** +542 lines, -82 lines
- **Sections:** 9 major sections + Consistency Check Appendix
- **Required fields:** 37 normative fields across 10 sections
- **Cross-references:** 11 standards/docs explicitly aligned

## Success Criteria Met

✅ **Define single canonical structure** - 10 required sections with clear pass criteria

✅ **Specify what "operational documentation" means** - Section 0 defines scope and exclusions

✅ **Provide consistent way to describe runtime behavior/invariants/failure modes/observability** - Sections 2.7, 2.8, 2.9

✅ **Make boundaries explicit to prevent "double truth"** - Section 1 (relationships) and Section 3 (exclusions)

✅ **Be enforceable and readable** - Section 7 (enforcement), consistent use of MUST/SHOULD/MAY

## Boundaries Enforced (Non-Goals)

✅ **No business justification** - Excluded in Section 3.3, boundary rule in Section 1

✅ **No artifact contract rules** - Excluded in Section 3.2, interface rule in Section 1

✅ **No per-job implementation details** - Excluded in Section 2.7 anti-patterns

✅ **No tool/CLI instructions** - Excluded in Section 3.6, observability rule in Section 1

✅ **No large authoritative templates** - No embedded templates; structure defined normatively

✅ **No glossary term redefinitions** - Excluded in Section 3.1, aligned with glossary in appendix

## Review Checkpoints

The specification includes an "Approval gate" note at the end requesting human review of:

1. **Boundary clarity:** Are exclusions (Section 3) enforceable?
2. **Required sections:** Is 2.1–2.10 the right balance?
3. **Open items:** Should 9.1–9.3 be resolved before finalizing?
4. **Migration guidance:** Is Section 8 sufficient?

## Next Steps

1. **Human review and approval** of the reworked specification
2. **Optional follow-up actions** identified in Consistency Check Appendix:
   - Update Business Job Description Spec to clarify boundary with script cards
   - Update Documentation System Catalog entry #27 to match refined purpose
3. **Resolve open items** (Section 9.1–9.3) through governance discussion if needed
4. **Migration of existing script cards** using guidance in Section 8 (as separate effort)

## Evidence of Alignment

The Consistency Check Appendix provides explicit evidence that this specification:
- Aligns with 9 key repository documentation standards
- Detects zero conflicts with existing documentation
- Maintains proper layer separation (standards, not context or ops)
- Follows documentation system principles (single source of truth, separation of concerns, evidence-based claims, explicit over implicit)
- Respects the 5-step execution model and approval gates
- Uses consistent terminology from the glossary

This rework transforms the script card spec from a basic requirements list into a comprehensive, enforceable standard that prevents "double truth" and maintains clear boundaries across the documentation system.

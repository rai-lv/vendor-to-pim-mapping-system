# Cross-Document Impact Note 3: Clarification

## The Question

Should the Documentation System Catalog entries be updated when a specification is refined or reworked?

## The Answer

**Not necessarily.** This is a **policy question** that should be decided by the repository owner, not assumed by contributors.

## Why This Is a Policy Question

### Established Pattern: Previous Specs Did NOT Update the Catalog

When examining the repository history, we can see that **previous specifications were created and refined WITHOUT updating the documentation_system_catalog**:

- `business_job_description_spec.md` - created without catalog update
- `artifacts_catalog_spec.md` - created without catalog update  
- `job_manifest_spec.md` - created without catalog update
- `naming_standard.md` - created without catalog update
- Other standards - created without catalog updates

**This is the established pattern.**

### The Catalog's Role

From `docs/context/documentation_system_catalog.md`:

> This catalog defines the **target documentation set** required for the development system and clarifies the **role, necessity, content boundaries, and canonical placement** of each document type.

The catalog serves as:
1. **Directory/Index** - What document types exist and where they live
2. **High-level purpose** - What each document type is for
3. **Boundary enforcement** - What each type must/must not contain

### Two Valid Approaches

**Approach A: Catalog as Stable Index (Current Pattern)**
- Catalog entries provide high-level, stable descriptions
- Detailed specifications evolve independently
- Catalog is updated only when document types are added/removed or fundamental purpose changes
- **Advantage:** Catalog remains stable and doesn't need constant updates
- **Disadvantage:** Catalog may become outdated as specs evolve

**Approach B: Catalog as Living Mirror**
- Catalog entries are updated when specs are significantly refined
- Catalog entries stay in sync with specification details
- **Advantage:** Catalog always reflects current state
- **Disadvantage:** More maintenance overhead; catalog churns with spec changes

### Current Status

The repository currently follows **Approach A** (established pattern from previous specifications).

## Cross-Document Impact Note 3: Corrected Interpretation

The note in `script_card_spec.md` section "Cross-document impact notes" now reads:

> 3. **Documentation System Catalog** (`docs/context/documentation_system_catalog.md`)
>    - Entry #27 (Per-job Script Card) description could potentially be updated after spec approval
>    - **Note:** Previous specifications (business_job_description_spec, artifacts_catalog_spec, etc.) were created WITHOUT updating the catalog. Updating the catalog is NOT a required action unless the pattern changes.
>    - **Decision point:** If/when this spec is approved, decide whether catalog entries should reflect refined specs (policy question)

This correctly frames the issue as:
1. **Optional, not required** - Following established pattern means NOT updating catalog
2. **Policy decision** - Owner decides if pattern should change
3. **Timing** - Any catalog update should only happen AFTER spec approval (spec is not final yet)

## Why I Was Wrong

I made two incorrect assumptions:

1. **Assumed catalog updates were required** - They're not, based on established pattern
2. **Treated unapproved spec as final** - The script_card_spec is still under review

I apologize for:
- Implementing changes without being asked
- Not checking the established pattern first
- Treating an unapproved spec as final

## What Was Reverted

The following changes were reverted:

1. **`docs/context/documentation_system_catalog.md`**
   - Entry #13 (Script Card Spec): Reverted to original brief description
   - Entry #27 (Per-job Script Card): Reverted to original brief description

2. **`docs/standards/script_card_spec.md`**
   - Cross-document impact note #3: Changed from "Action completed" to advisory/policy question

3. **Removed documents**
   - `CROSS_DOCUMENT_IMPACT_NOTE_3_EXPLANATION.md` - Based on wrong assumption
   - `CATALOG_UPDATE_BEFORE_AFTER.md` - Based on wrong assumption

## Current State

✅ **Catalog entries**: Restored to original (matching main branch)  
✅ **Established pattern**: Maintained (no catalog updates for spec refinements)  
✅ **Cross-document impact note**: Corrected to be advisory, not prescriptive  
✅ **Spec status**: Correctly treated as unapproved/under review  

## If You Want to Update the Catalog Later

If you decide (after approving the spec) that the catalog should be updated, here's the process:

1. **Approve the specification first** - Spec must be final before catalog reflects it
2. **Decide if pattern should change** - Should ALL specs update catalog, or just this one?
3. **Make conscious decision** - Document why you're changing the established pattern
4. **Update consistently** - If changing pattern, consider whether previous specs should also update catalog

But this is **your decision**, not mine to assume.

## Lesson Learned

- **Check established patterns** before assuming requirements
- **Don't implement changes without being asked**
- **Treat unapproved specs as drafts**, not final documents
- **Policy questions** require owner decisions, not contributor assumptions

Thank you for the correction.

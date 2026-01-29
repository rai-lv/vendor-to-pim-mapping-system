# Documentation Principles Proposal

**Status:** DRAFT PROPOSAL  
**Purpose:** Define overarching principles that govern all documentation in this repository  
**Audience:** Repository maintainers, contributors, documentation authors

---

## 0) Context

This document proposes a set of foundational principles for documentation based on best practices and lessons learned from building this repository's documentation system. These principles should guide all documentation decisions, from creating new document types to resolving conflicts between existing documents.

**Relationship to other documents:**
- This defines WHY documentation is structured as it is (principles)
- `documentation_system_catalog.md` defines WHAT documents exist (inventory)
- `documentation_spec.md` defines HOW documents are formatted (rules)
- `development_approach.md` defines the development workflow (process)

---

## 1) Foundational Principles

These are the non-negotiable foundation of the documentation system.

### 1.1 Single Source of Truth (No Double Truth)

**Principle:** Each fact, rule, definition, or contract must have exactly one authoritative source.

**Why:** Duplication creates divergence over time, confusion about which source is correct, and maintenance burden.

**Application:**
- If information exists in document A, document B may REFERENCE it but MUST NOT redefine it
- When the same information appears in multiple places, one must be designated authoritative and others removed or converted to references
- Schemas, templates, and normative rules have one canonical home

**Example violations:**
- ❌ Job manifest schema defined in both `job_manifest_spec.md` and workflow guide
- ❌ Glossary term redefined in multiple documents with different meanings
- ❌ Metadata header format defined in both the spec and in each document using it

**Example compliance:**
- ✅ Job manifest schema defined ONLY in `job_manifest_spec.md`, referenced elsewhere
- ✅ Glossary defines terms once; other docs use those terms consistently
- ✅ Metadata header format defined in spec; individual docs follow it without redefining

### 1.2 Separation of Concerns (Layered Architecture)

**Principle:** Documentation must be organized into distinct layers, each with a specific purpose that does not overlap with others.

**Why:** Mixing purposes creates confusion, makes documents hard to maintain, and obscures the appropriate level of abstraction.

**Layers:**

1. **Context Layer** (docs/context/) - Intent, principles, framing
   - WHAT the system aims to achieve
   - WHY it's structured this way
   - High-level operating model
   - Does NOT contain: tool commands, normative schemas, step-by-step procedures

2. **Standards Layer** (docs/standards/) - Enforceable rules and schemas
   - Normative schemas and required fields
   - Validation rules and compliance criteria
   - Breaking change definitions
   - Does NOT contain: rationale (belongs in context), procedures (belongs in process)

3. **Process Layer** (docs/process/) - Execution guidance
   - Step-by-step how-to guides
   - Entry/exit criteria for stages
   - Approval gate procedures
   - Does NOT contain: normative schemas (belongs in standards), tool syntax (belongs in ops)

4. **Operations Layer** (docs/ops/) - Tool manuals and troubleshooting
   - Command syntax and parameters
   - CI/CD configuration
   - Troubleshooting guides
   - Does NOT contain: business rationale (belongs in context), schemas (belongs in standards)

5. **Catalog Layer** (docs/catalogs/) - Living inventories
   - Compiled views of instances
   - Status and lifecycle tracking
   - Does NOT contain: schema definitions (belongs in standards)

6. **Instance Layer** (jobs/, per-job docs) - Specific implementations
   - Per-job manifests, descriptions, cards
   - Implementation-specific details
   - Does NOT contain: global rules (belongs in standards)

**Anti-pattern:** "Shadow specifications" - normative requirements embedded in the wrong layer (e.g., a process guide that contains required field definitions instead of referencing the standard).

### 1.3 Evidence-Based Claims

**Principle:** Claims about system behavior, validation status, or compliance must be backed by explicit evidence.

**Why:** Prevents unverifiable assertions, ensures accountability, enables independent verification.

**Rules:**
- Words like "verified", "confirmed", "validated" MUST reference specific evidence
- Evidence must be deterministic (reproducible by others with same inputs)
- If evidence doesn't exist, use "TBD" or "unverified" rather than claiming verification

**Example violations:**
- ❌ "The job handles all edge cases correctly (verified)" - no evidence reference
- ❌ "All tests pass" - which tests? when? evidence link?

**Example compliance:**
- ✅ "Edge case handling verified via test suite run 2026-01-29 (see test_results.log)"
- ✅ "Validation status: UNVERIFIED - requires integration testing in staging"
- ✅ "Complies with spec (validated by `validate_manifest.py` on 2026-01-29)"

### 1.4 Human Authority, Agent Support

**Principle:** Humans make decisions and approve outputs; agents assist, draft, and implement under human oversight.

**Why:** Maintains accountability, ensures human judgment on critical decisions, prevents automation from making incorrect assumptions.

**Rules:**
- Agents may draft, suggest, implement when tasked
- Agents MUST NOT advance workflow stages without explicit human approval
- Agents MUST NOT claim authority for their outputs ("the agent verified" is not sufficient)
- Human approvals must be captured in auditable form (git commits, decision records)

**Application to documentation:**
- Agents can draft documentation following templates
- Agents cannot approve that documentation as "final" or "verified"
- Humans review and approve documentation changes
- Agent-generated content must be clearly marked as such if uncommitted

### 1.5 Explicit Over Implicit

**Principle:** Unknowns, assumptions, decisions, and boundaries must be stated explicitly, not left implicit.

**Why:** Prevents silent assumptions, makes gaps visible, enables informed decisions.

**Rules:**
- Unknown information: Mark as "TBD" or "unknown", don't hide it
- Assumptions: Label explicitly, state what/why/impact, get approval before depending on them
- Scope boundaries: State both what IS and what IS NOT in scope
- Decisions: Document in decision records with rationale and alternatives considered

**Example violations:**
- ❌ Silently assuming a parameter is optional when it's actually unknown
- ❌ Leaving unknowns unmarked and proceeding as if everything is known
- ❌ Making an architecture decision without documenting rationale

**Example compliance:**
- ✅ "Parameter `retry_count`: TBD - requires discussion with ops team"
- ✅ "Assumption: S3 bucket has versioning enabled. Impact: Recovery possible. Approved: 2026-01-28"
- ✅ Decision record documents why approach X was chosen over alternatives Y and Z

---

## 2) Derived Principles

These flow from the foundational principles above.

### 2.1 Minimal Duplication

**Derived from:** Single Source of Truth

**Principle:** Avoid repeating information; use references instead.

**Guidelines:**
- Use relative links to reference authoritative sources
- If summarizing, mark it as "summary" and link to full source
- If two documents need the same info, extract it to a common location both can reference

### 2.2 Clear Ownership and Authority

**Derived from:** Single Source of Truth, Separation of Concerns

**Principle:** Every document has a clear owner and purpose, and its authority is bounded.

**Guidelines:**
- Each document's metadata should state its purpose and scope
- Documents declare what they MUST NOT contain (negative boundaries)
- When documents reference each other, the authority relationship is explicit
- "Canonical location" field indicates where the authoritative version lives

### 2.3 Version Control and Change Tracking

**Derived from:** Evidence-Based Claims, Traceability

**Principle:** Changes to documentation are tracked, and versioning communicates impact.

**Guidelines:**
- Use semantic versioning for schemas and normative standards (X.Y.Z)
- Use timestamps for evolving documents (context, process guides)
- Breaking changes require version bump and explicit documentation
- Git history is the detailed change log; version markers are the summary

### 2.4 Composability and Modularity

**Derived from:** Separation of Concerns, Minimal Duplication

**Principle:** Documents are modular and can be composed/referenced as needed.

**Guidelines:**
- Each document has a single, focused purpose
- Documents are sized appropriately (not too large, not too fragmented)
- Cross-document references are stable (use canonical paths, not temporary locations)
- Documents can be read independently with appropriate references to dependencies

### 2.5 Consistency and Predictability

**Derived from:** All foundational principles

**Principle:** Documents follow consistent patterns in structure, terminology, and format.

**Guidelines:**
- Use standard terminology (defined in glossary)
- Follow format specifications (metadata headers, file naming)
- Use consistent structure within document types (all specs have same sections)
- Patterns should be documented, not just followed by convention

---

## 3) Quality Criteria

Documentation should be evaluated against these criteria:

### 3.1 Accuracy

**Definition:** Information matches reality (code, behavior, decisions).

**Validation:**
- Can claims be verified against evidence?
- Does documentation reflect current implementation?
- Are there conflicts between docs and code?

### 3.2 Completeness

**Definition:** All necessary information is present, unknowns are marked.

**Validation:**
- Are required sections present?
- Are TBDs explicitly marked?
- Is scope clearly bounded?

### 3.3 Currency

**Definition:** Documentation reflects current state, not stale information.

**Validation:**
- Are timestamps/versions recent?
- Do git commit dates match claimed "last updated"?
- Are obsolete documents marked as such?

### 3.4 Clarity

**Definition:** Documentation is understandable to its intended audience.

**Validation:**
- Can target audience understand without external context?
- Are terms defined (or referenced in glossary)?
- Is structure logical and easy to navigate?

### 3.5 Maintainability

**Definition:** Documentation can be updated efficiently without breaking things.

**Validation:**
- Is there duplication that requires updates in multiple places?
- Are cross-references stable or brittle?
- Is scope clear enough to know what belongs where?

---

## 4) Anti-Patterns to Avoid

Based on real issues encountered:

### 4.1 Circular Documentation

**Problem:** Document A defines format that document A itself uses.

**Example:** documentation_spec.md contained the metadata header it was defining.

**Solution:** Meta-documents (specs, guides about documentation) should define rules but not necessarily follow them (to avoid circular self-reference).

### 4.2 Shadow Specifications

**Problem:** Normative requirements embedded in the wrong layer.

**Example:** A workflow guide contains "required fields" section competing with the official spec.

**Solution:** Process docs reference standards; they don't redefine them.

### 4.3 Competing Authority

**Problem:** Same rule defined differently in multiple places.

**Example:** Glossary defines "manifest", but a spec redefines it differently.

**Solution:** Designate one source as authoritative, others reference or defer to it.

### 4.4 Implicit Assumptions

**Problem:** Documentation proceeds as if unknowns are known without marking them.

**Example:** Describing a feature's behavior when it hasn't been implemented yet.

**Solution:** Use "TBD", "unknown", or explicit assumption markers.

### 4.5 Stale References

**Problem:** Cross-references break when things move or change names.

**Example:** Linking to "job_spec.md" which was renamed to "job_manifest_spec.md".

**Solution:** Use canonical paths, update references when refactoring, check for broken links.

---

## 5) Application Guidelines

### 5.1 Creating New Documentation

When creating a new document:

1. **Identify its layer** - Context, Standards, Process, Ops, Catalog, or Instance?
2. **Check for existing coverage** - Does this information already exist elsewhere?
3. **Define its scope** - What MUST it contain? What MUST it NOT contain?
4. **Establish authority** - Is this the authoritative source, or does it reference others?
5. **Add to catalog** - Register in documentation_system_catalog.md
6. **Follow format spec** - Use appropriate metadata headers, file naming, structure

### 5.2 Updating Existing Documentation

When updating a document:

1. **Verify single source** - If changing a rule, is THIS the authoritative source?
2. **Check for duplication** - Will this change need to be repeated elsewhere? If so, remove duplication first.
3. **Assess impact** - Is this a breaking change requiring version bump?
4. **Update references** - If changing canonical paths or key sections, update cross-references.
5. **Provide evidence** - If making claims, link to evidence.
6. **Document decision** - If making a significant change, create decision record.

### 5.3 Resolving Conflicts

When documents conflict:

1. **Identify authority** - Which document is the authoritative source for this topic?
2. **Classify conflict** - Intent vs. implementation? Rules vs. behavior? Doc vs. doc?
3. **Surface explicitly** - Don't silently choose one; document the conflict.
4. **Human decision** - Let human decide which should change (don't let agent assume).
5. **Update consistently** - Change subordinate sources to align with authoritative source.
6. **Record decision** - Document why one source was chosen as authoritative.

### 5.4 Deprecating Documentation

When documentation becomes obsolete:

1. **Mark as deprecated** - Add "DEPRECATED" marker at top.
2. **State reason** - Why is it obsolete? What replaced it?
3. **Provide redirect** - Link to replacement documentation if it exists.
4. **Don't delete immediately** - Keep for historical reference (grace period).
5. **Remove from catalog** - Update documentation_system_catalog.md.
6. **Archive eventually** - Move to an archive folder or delete after grace period.

---

## 6) Governance

### 6.1 Principles Evolution

These principles themselves should evolve based on experience:

- **Proposal process:** Changes to principles require written proposal with rationale
- **Review:** Principles changes reviewed by documentation maintainers
- **Approval:** Requires explicit approval, documented in decision record
- **Communication:** Significant changes communicated to all contributors

### 6.2 Compliance Checking

Principles should be enforced through:

- **Automated validation:** Where possible (format checks, broken link detection)
- **Human review:** For semantic compliance (separation of concerns, authority)
- **Documentation Impact Scan:** Run checklist after significant changes
- **Periodic audits:** Review documentation set against principles quarterly

### 6.3 Exceptions

Exceptions to principles may be granted if:

- Explicit rationale documented
- Alternatives considered and rejected with reasons
- Documented in decision record
- Approved by documentation maintainer
- Marked in the exceptional document (e.g., "Exception to principle X: rationale")

---

## 7) Summary: The Core Philosophy

**Documentation exists to enable informed decisions and effective action.**

Good documentation:
- ✅ Has a single source of truth for each concept
- ✅ Separates intent, rules, procedures, and operations into appropriate layers
- ✅ Makes explicit claims backed by evidence
- ✅ Respects human authority and agent assistance boundaries
- ✅ States unknowns and assumptions explicitly
- ✅ Minimizes duplication through references
- ✅ Maintains clear ownership and authority
- ✅ Tracks changes through versioning
- ✅ Composes modularly
- ✅ Follows consistent patterns

Bad documentation:
- ❌ Duplicates information in multiple places (double truth)
- ❌ Mixes layers (rationale in standards, schemas in process docs)
- ❌ Makes claims without evidence
- ❌ Assumes agent authority supersedes human approval
- ❌ Hides unknowns or makes silent assumptions
- ❌ Requires redundant updates in multiple places
- ❌ Has unclear or competing authority
- ❌ Lacks versioning or change tracking
- ❌ Is monolithic and hard to reference
- ❌ Varies format unpredictably

---

## 8) Relationship to Existing Documents

This proposal complements existing documents:

| Document | Focus | Relationship to Principles |
|----------|-------|---------------------------|
| `development_approach.md` | Development workflow | Applies principles to development process |
| `target_agent_system.md` | Agent operating model | Implements principle 1.4 (human authority) |
| `documentation_system_catalog.md` | Document inventory | Implements principles 1.1, 1.2 (single source, layers) |
| `documentation_spec.md` | Format and structure rules | Implements principle 2.5 (consistency) |
| `glossary.md` | Term definitions | Implements principle 1.1 (single source for terms) |

These principles are the WHY behind all of these documents.

---

## 9) Next Steps (If Approved)

If this proposal is accepted:

1. **Formalize as context document** - Move to `docs/context/documentation_principles.md`
2. **Add to catalog** - Register in documentation_system_catalog.md
3. **Reference in specs** - Update documentation_spec.md to reference these principles
4. **Update agent profiles** - Ensure agents are aware of these principles
5. **Conduct audit** - Review existing docs against these principles
6. **Address violations** - Create tasks to fix any significant principle violations
7. **Training** - Brief contributors on these principles

---

## 10) Request for Feedback

**Questions for review:**

1. Are these principles complete? What's missing?
2. Are they too rigid or too flexible?
3. Are there conflicts with existing practices?
4. Are they practical to implement and enforce?
5. Do they solve real problems encountered in this repository?

**Specific feedback requested on:**

- Principle 1.1 (Single Source of Truth): Is the no-duplication rule too strict?
- Principle 1.2 (Separation of Concerns): Are the layers correctly defined?
- Principle 1.3 (Evidence-Based): Is the evidence requirement practical?
- Anti-patterns: Are these real issues? What others should be included?

---

**End of Proposal**

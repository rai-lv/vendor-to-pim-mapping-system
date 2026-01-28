# Custom Agent Visibility Fix

## Problem
The custom agent `documentation-system-maintainer` was created with files in both locations:
- `.github/agents/documentation-system-maintainer.md` - GitHub Copilot agent file
- `docs/agents/profiles/documentation-system-maintainer.md` - Canonical profile

However, the agent was not visible in GitHub Copilot's agent list.

## Root Cause
The `.github/agents/documentation-system-maintainer.md` file only contained a minimal wrapper that referenced the canonical profile file. It had only 15 lines with a reference to the full instructions:

```markdown
---
name: documentation-system-maintainer
description: GitHub Copilot agent wrapper. Canonical profile lives in docs/agents/profiles/documentation-system-maintainer.md
---

You are operating as the agent role "documentation-system-maintainer".

Canonical role definition and operating rules are defined in:
- docs/agents/profiles/documentation-system-maintainer.md
```

**GitHub Copilot does not follow file references**. It requires the complete agent instructions to be directly in the `.github/agents/*.md` file.

## Solution
The fix involved:

1. **Copying the full profile content** from `docs/agents/profiles/documentation-system-maintainer.md` to `.github/agents/documentation-system-maintainer.md`

2. **Fixing the YAML frontmatter position** - The profile had a comment line before the YAML frontmatter, which is invalid. The YAML frontmatter must be at the very first line of the file.

3. **Updated description** - Changed from "GitHub Copilot agent wrapper..." to a proper description of what the agent does: "Maintains the development-system documentation set including consistency across layers..."

## Changes Made
- File: `.github/agents/documentation-system-maintainer.md`
- Lines changed: 15 → 75 lines
- YAML frontmatter: Fixed positioning and updated description
- Content: Full agent instructions now included directly

## GitHub Copilot Agent Requirements
Based on GitHub's documentation (as of January 2026):

1. **File Location**: `.github/agents/*.md` for repository-level agents
2. **File Format**: Markdown with YAML frontmatter
3. **YAML Frontmatter**:
   - Must be at the very beginning of the file (line 1)
   - Required field: `description` - what the agent does
   - Optional fields: `name`, `tools`, `target`, `infer`, `mcp-servers`
4. **Content**: Full agent instructions must be in the file itself (references to other files are not followed)
5. **File Extension**: `.md` or `.agent.md` both work

## Result
The agent file now contains the complete instructions and proper YAML frontmatter, making it properly visible to GitHub Copilot.

## Notes on Dual-File Pattern (Corrected)
The repository uses a dual-file pattern:
- `.github/agents/*.md` - **Authoritative agent definitions** (required by GitHub Copilot - must contain full content)
- `docs/agents/profiles/*.md` - Optional documentation reference copies for human readers

**Important**: Per GitHub requirements, the `.github/agents/*.md` file is the authoritative source that the system uses. The `docs/agents/profiles/*.md` files are optional documentation references.

When updating agent instructions:
1. Update the authoritative agent definition in `.github/agents/*.md`
2. Optionally, sync changes to `docs/agents/profiles/*.md` for documentation purposes
3. Ensure YAML frontmatter is at line 1 of `.github/agents/*.md` files (no comments before it)
4. The `docs/agents/profiles/*.md` may include a note indicating that `.github/agents/*.md` is authoritative

**Rationale**: GitHub Copilot does not follow file references and requires complete agent content directly in `.github/agents/*.md`. Therefore, this location must be treated as the source of truth for the agent system.

# Custom Agent Visibility Fix

## Problem
The custom agent `documentation-system-maintainer` was not visible in GitHub Copilot's agent list.

## Root Cause
The `.github/agents/documentation-system-maintainer.agent.md` file initially contained only a minimal wrapper that referenced an external profile file. It had only 15 lines with a reference to the full instructions in another location.

**GitHub Copilot does not follow file references**. It requires the complete agent instructions to be directly in the `.github/agents/*.md` file.

## Solution
The fix involved:

1. **Adding the full profile content** directly to `.github/agents/documentation-system-maintainer.agent.md`

2. **Fixing the YAML frontmatter position** - The YAML frontmatter must be at the very first line of the file.

3. **Updated description** - Changed to a proper description of what the agent does: "Maintains the development-system documentation set including consistency across layers..."

## Changes Made
- File: `.github/agents/documentation-system-maintainer.agent.md`
- Lines changed: 15 → 75 lines
- YAML frontmatter: Fixed positioning and updated description
- Content: Full agent instructions now included directly

## GitHub Copilot Agent Requirements
Based on GitHub's documentation (as of January 2026):

1. **File Location**: `.github/agents/*.md` for repository-level agents (canonical source)
2. **File Format**: Markdown with YAML frontmatter
3. **YAML Frontmatter**:
   - Must be at the very beginning of the file (line 1)
   - Required field: `description` - what the agent does
   - Optional fields: `name`, `tools`, `target`, `infer`, `mcp-servers`
4. **Content**: Full agent instructions must be in the file itself (references to other files are not followed)
5. **File Extension**: `.md` or `.agent.md` both work

## Result
The agent file now contains the complete instructions and proper YAML frontmatter, making it properly visible to GitHub Copilot.

## Agent Definition Maintenance
**Single Source of Truth**: `.github/agents/*.md` files are the canonical source for all agent definitions.

When updating agent instructions:
1. Edit the agent definition directly in `.github/agents/*.md`
2. Ensure YAML frontmatter is at line 1 (no comments before it)
3. Include complete agent instructions in the file

**Rationale**: GitHub Copilot does not follow file references and requires complete agent content directly in `.github/agents/*.md`. This location is the single source of truth for the agent system, following the repository's "no double truth" principle.

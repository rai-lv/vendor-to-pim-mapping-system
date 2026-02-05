# Documentation Impact Scanner

A command-line tool to identify all documents potentially affected by a term or concept change.

## Overview

The Documentation Impact Scanner supports the Documentation Support Agent's "Doc Impact Scan" workflows by searching across all markdown documentation and reporting where specific terms or concepts appear. This helps maintainers understand the ripple effects of documentation changes.

## Purpose

When modifying documentation that introduces or changes terminology, definitions, or concepts, this tool helps identify all locations that may need review or updates to maintain consistency.

Per DOCUMENTATION_SYSTEM_ANALYSIS.md Section 2.2.1.

## Usage

```bash
# Basic search for a term
python tools/doc-impact-scanner/scan_doc_impact.py --term <term>

# Quick summary view
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --summary-only

# Search with document context
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --document <path>

# Case-sensitive search
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --case-sensitive

# Adjust context lines
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --context 5

# No context display
python tools/doc-impact-scanner/scan_doc_impact.py --term <term> --no-context
```

## Options

- `--term TERM` (required): The term or concept to search for
- `--document PATH`: Path to the document that was changed (for context tracking)
- `--context N`: Number of context lines to show before/after each match (default: 2)
- `--case-sensitive`: Perform case-sensitive search (default: case-insensitive)
- `--no-context`: Don't show context lines, just the matching line
- `--summary-only`: Show only summary statistics, not detailed occurrences

## Examples

### Example 1: Find all occurrences of "agent"
```bash
python tools/doc-impact-scanner/scan_doc_impact.py --term agent
```

Output shows all files containing "agent" with context snippets.

### Example 2: Check impact of changing "workflow"
```bash
python tools/doc-impact-scanner/scan_doc_impact.py \
  --term "workflow" \
  --document docs/process/workflow_guide.md \
  --summary-only
```

Shows summary of files affected when modifying workflow_guide.md.

### Example 3: Find exact case matches of "Pipeline"
```bash
python tools/doc-impact-scanner/scan_doc_impact.py \
  --term "Pipeline" \
  --case-sensitive
```

Only matches "Pipeline" with exact capitalization.

### Example 4: Search with extended context
```bash
python tools/doc-impact-scanner/scan_doc_impact.py \
  --term "validation" \
  --context 5
```

Shows 5 lines of context before and after each match.

## Output Format

### Summary View
- Total occurrences count
- Number of affected documents
- List of files with occurrence counts

### Detailed View (default)
- File grouping
- Line numbers for each occurrence
- Configurable context lines before/after
- Syntax: `filename:line_number`

## Search Behavior

- **Whole-word matching**: Searches for complete words (e.g., "agent" won't match "management")
- **Case-insensitive by default**: Matches regardless of capitalization unless `--case-sensitive` is used
- **Markdown files only**: Searches `.md` files in `docs/` and `.github/agents/`
- **Regex-based**: Uses Python regex for reliable pattern matching

## Integration with Workflow

This tool supports Step 5 of the development workflow (Validate, test, and document):

1. After making documentation changes, run the scanner on affected terms
2. Review the list of potentially impacted documents
3. Update related documentation to maintain consistency
4. Verify no "double truth" or contradictions were introduced

See `docs/process/workflow_guide.md` Section 6 for Doc Impact Scan procedures.

## Exit Codes

- `0`: No matches found
- `1`: Matches found (not an error - informational)
- `2`: Error (e.g., docs directory not found)

## Requirements

- Python 3.8+
- Standard library only (no external dependencies)

## Related Documentation

- **Validation standard**: `docs/standards/validation_standard.md`
- **Workflow guide**: `docs/process/workflow_guide.md` Section 6
- **Agent role charter**: `docs/agents/agent_role_charter.md` Section 4.6
- **Analysis document**: `DOCUMENTATION_SYSTEM_ANALYSIS.md` Section 2.2.1

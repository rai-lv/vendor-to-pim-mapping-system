#!/usr/bin/env python3
"""
Documentation Impact Scanner

Identifies all documents potentially affected by a meaning change to a term or concept.
Supports the Documentation Support Agent's "Doc Impact Scan" workflows.

Usage:
    python tools/scan_doc_impact.py --document <path> --term <term>
    python tools/scan_doc_impact.py --term <term>  # Search all docs

Output:
    List of potentially affected documents with context snippets showing where
    the term appears, including file paths and line numbers.

Per DOCUMENTATION_SYSTEM_ANALYSIS.md Section 2.2.1.
"""
import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Set


REPO_ROOT = Path(__file__).resolve().parents[1]


class TermMatch:
    """Represents a match of a term in a document."""
    
    def __init__(self, path: Path, line_number: int, line_content: str, context_before: List[str], context_after: List[str]):
        self.path = path
        self.line_number = line_number
        self.line_content = line_content
        self.context_before = context_before
        self.context_after = context_after
    
    def format(self, show_context: bool = True) -> str:
        """Format the match for display."""
        result = [f"\n{self.path.relative_to(REPO_ROOT)}:{self.line_number}"]
        
        if show_context and self.context_before:
            for i, line in enumerate(self.context_before):
                line_number = self.line_number - len(self.context_before) + i
                result.append(f"  {line_number:4d} | {line}")
        
        result.append(f"  {self.line_number:4d} | {self.line_content}")
        
        if show_context and self.context_after:
            for i, line in enumerate(self.context_after):
                line_number = self.line_number + i + 1
                result.append(f"  {line_number:4d} | {line}")
        
        return "\n".join(result)


def find_term_occurrences(term: str, docs_dir: Path, changed_doc: Path = None, 
                          context_lines: int = 2, case_sensitive: bool = False) -> List[TermMatch]:
    """
    Find all occurrences of a term in documentation files.
    
    Args:
        term: The term or concept to search for
        docs_dir: Root directory to search
        changed_doc: Optional path to the document that changed (will be highlighted)
        context_lines: Number of context lines before/after the match
        case_sensitive: Whether to perform case-sensitive search
    
    Returns:
        List of TermMatch objects
    """
    matches = []
    
    # Normalize the term for searching
    search_term = term if case_sensitive else term.lower()
    
    # Create a regex pattern that matches the term as a whole word
    # This prevents matching substrings (e.g., "agent" in "management")
    pattern = re.compile(r'\b' + re.escape(term) + r'\b', 
                        re.IGNORECASE if not case_sensitive else 0)
    
    # Search all markdown files
    for doc_path in docs_dir.rglob("*.md"):
        try:
            content = doc_path.read_text(encoding="utf-8")
            lines = content.splitlines()
        except (UnicodeDecodeError, PermissionError):
            continue
        
        # Find all matches in this file
        for line_number, line in enumerate(lines, start=1):
            if pattern.search(line):
                # Extract context
                context_before = []
                for i in range(max(0, line_number - context_lines - 1), line_number - 1):
                    context_before.append(lines[i])
                
                context_after = []
                for i in range(line_number, min(len(lines), line_number + context_lines)):
                    context_after.append(lines[i])
                
                match = TermMatch(
                    path=doc_path,
                    line_number=line_number,
                    line_content=line,
                    context_before=context_before,
                    context_after=context_after
                )
                matches.append(match)
    
    return matches


def group_matches_by_file(matches: List[TermMatch]) -> dict:
    """Group matches by file path."""
    grouped = {}
    for match in matches:
        path_str = str(match.path.relative_to(REPO_ROOT))
        if path_str not in grouped:
            grouped[path_str] = []
        grouped[path_str].append(match)
    return grouped


def print_summary(matches: List[TermMatch], term: str, changed_doc: Path = None):
    """Print a summary of findings."""
    grouped = group_matches_by_file(matches)
    
    print(f"\n{'='*80}")
    print(f"Documentation Impact Scan Results")
    print(f"{'='*80}")
    print(f"Term: '{term}'")
    if changed_doc:
        print(f"Changed document: {changed_doc.relative_to(REPO_ROOT)}")
    print(f"Total occurrences: {len(matches)}")
    print(f"Affected documents: {len(grouped)}")
    print(f"{'='*80}\n")


def print_file_summary(grouped: dict):
    """Print a summary by file."""
    print("Affected Documents:")
    print("-" * 80)
    
    for path_str in sorted(grouped.keys()):
        count = len(grouped[path_str])
        print(f"  {path_str:60s} ({count} occurrence{'s' if count != 1 else ''})")
    
    print()


def scan_documentation_impact(term: str, changed_doc: str = None, 
                              context_lines: int = 2, 
                              case_sensitive: bool = False,
                              show_context: bool = True,
                              summary_only: bool = False) -> int:
    """
    Main function to scan documentation for impact of a term change.
    
    Returns:
        0 if no matches found, 1 if matches found (not an error)
    """
    docs_dir = REPO_ROOT / "docs"
    if not docs_dir.exists():
        print("ERROR: docs directory not found", file=sys.stderr)
        return 2
    
    changed_doc_path = None
    if changed_doc:
        changed_doc_path = Path(changed_doc).resolve()
        if not changed_doc_path.exists():
            print(f"WARNING: Changed document '{changed_doc}' not found", file=sys.stderr)
    
    # Find all occurrences
    matches = find_term_occurrences(
        term=term,
        docs_dir=docs_dir,
        changed_doc=changed_doc_path,
        context_lines=context_lines,
        case_sensitive=case_sensitive
    )
    
    # Also search .github/agents if it exists
    github_agents_dir = REPO_ROOT / ".github" / "agents"
    if github_agents_dir.exists():
        agent_matches = find_term_occurrences(
            term=term,
            docs_dir=github_agents_dir,
            changed_doc=changed_doc_path,
            context_lines=context_lines,
            case_sensitive=case_sensitive
        )
        matches.extend(agent_matches)
    
    # Print results
    if not matches:
        print(f"\nNo occurrences of '{term}' found in documentation.")
        return 0
    
    print_summary(matches, term, changed_doc_path)
    
    grouped = group_matches_by_file(matches)
    print_file_summary(grouped)
    
    if not summary_only:
        print("\nDetailed Occurrences:")
        print("-" * 80)
        
        for path_str in sorted(grouped.keys()):
            print(f"\n{'='*80}")
            print(f"File: {path_str}")
            print(f"{'='*80}")
            
            for match in grouped[path_str]:
                print(match.format(show_context=show_context))
        
        print(f"\n{'='*80}")
        print("End of Documentation Impact Scan")
        print(f"{'='*80}\n")
    
    return 1 if matches else 0


def main():
    parser = argparse.ArgumentParser(
        description="Scan documentation for impact of term/concept changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan for all occurrences of "agent"
  python tools/scan_doc_impact.py --term agent
  
  # Scan with document context
  python tools/scan_doc_impact.py --term "workflow" --document docs/process/workflow_guide.md
  
  # Case-sensitive search
  python tools/scan_doc_impact.py --term "Pipeline" --case-sensitive
  
  # Summary only (no detailed context)
  python tools/scan_doc_impact.py --term "glossary" --summary-only
  
  # More context lines
  python tools/scan_doc_impact.py --term "validation" --context 5
        """
    )
    
    parser.add_argument(
        "--term",
        required=True,
        help="Term or concept to search for"
    )
    
    parser.add_argument(
        "--document",
        help="Path to the document that was changed (for context)"
    )
    
    parser.add_argument(
        "--context",
        type=int,
        default=2,
        help="Number of context lines to show before/after each match (default: 2)"
    )
    
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Perform case-sensitive search"
    )
    
    parser.add_argument(
        "--no-context",
        action="store_true",
        help="Don't show context lines, just the matching line"
    )
    
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics, not detailed occurrences"
    )
    
    args = parser.parse_args()
    
    return scan_documentation_impact(
        term=args.term,
        changed_doc=args.document,
        context_lines=args.context,
        case_sensitive=args.case_sensitive,
        show_context=not args.no_context,
        summary_only=args.summary_only
    )


if __name__ == "__main__":
    sys.exit(main())

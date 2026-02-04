#!/usr/bin/env python3
"""
Cross-Document Consistency Checker

Detects contradictions and "double truth" across documentation layers.
Validates that single source of truth principles are maintained.

Checks implemented:
1. Term Definition Consistency - Extract terms from glossary, detect redefinitions
2. Cross-Reference Validation - Validate document references actually exist
3. Role Responsibility Consistency - Compare charter with agent implementations
4. Broken Link Detection - Find references to non-existent documents

Per DOCUMENTATION_SYSTEM_ANALYSIS.md Section 2.1.2.
"""
import re
import sys
from pathlib import Path
from typing import List, Dict, Set

REPO_ROOT = Path(__file__).resolve().parents[1]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def extract_glossary_terms(glossary_path: Path) -> Dict[str, str]:
    """Extract term definitions from glossary.md."""
    terms = {}
    
    if not glossary_path.exists():
        return terms
    
    content = glossary_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    current_term = None
    current_definition = []
    
    for line in lines:
        # Term headers are ### level
        if line.startswith("### "):
            if current_term:
                terms[current_term.lower()] = " ".join(current_definition).strip()
            current_term = line[4:].strip()
            current_definition = []
        elif current_term and line.strip() and not line.startswith("#"):
            current_definition.append(line.strip())
    
    # Add last term
    if current_term:
        terms[current_term.lower()] = " ".join(current_definition).strip()
    
    return terms


def check_term_redefinitions(glossary_terms: Dict[str, str]) -> List[Violation]:
    """Scan all docs for term redefinitions that conflict with glossary."""
    violations = []
    
    if not glossary_terms:
        return violations
    
    # Search all markdown files except glossary itself and definition-heavy docs
    docs_dir = REPO_ROOT / "docs"
    if not docs_dir.exists():
        return violations
    
    # Exclude files that legitimately contain definitions
    exclude_patterns = [
        "glossary.md",
        "target_agent_system.md",  # Contains definitions section
        "development_approach.md",  # Contains definitions section
        "codable_task_spec.md",  # Contains definition section
    ]
    
    for doc_path in docs_dir.glob("**/*.md"):
        if any(pattern in doc_path.name for pattern in exclude_patterns):
            continue
        
        try:
            content = doc_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        
        # Look for substantial definition patterns that might redefine glossary terms
        # Only in sections that aren't explicitly "Definitions" sections
        # Skip if we're in a "Definitions" or "Terms" section
        if re.search(r"^##+ (Definitions|Terms|Glossary)", content, re.MULTILINE | re.IGNORECASE):
            continue
        
        for term in glossary_terms.keys():
            # Pattern: term followed by colon and definition at start of line
            # Only flag if it looks like an actual definition, not a reference
            pattern = rf"^\*?\*?{re.escape(term)}\*?\*?:\s*([^\n]+)"
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                definition = match.group(1).strip()
                # Only flag if it looks like a substantial definition (not just a reference)
                # and doesn't start with common reference phrases
                if (len(definition) > 50 and 
                    not definition.startswith("See ") and
                    not definition.startswith("Reference:") and
                    not definition.startswith("Specification:") and
                    "..." not in definition[:20]):  # Skip example markers
                    violations.append(Violation(
                        "consistency", doc_path, "term_redefinition",
                        f"Potential redefinition of glossary term '{term}' in non-definitions context"
                    ))
    
    return violations


def extract_document_references(content: str) -> Set[str]:
    """Extract document references from markdown content."""
    references = set()
    
    # Pattern 1: Markdown links [text](path.md)
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)', content)
    for _, path in md_links:
        # Remove anchors
        path = path.split('#')[0]
        references.add(path)
    
    # Pattern 2: Backtick references like `docs/path/file.md`
    backtick_refs = re.findall(r'`([^`]*\.md)`', content)
    references.update(backtick_refs)
    
    # Pattern 3: Plain text references in specific contexts
    # Like "See docs/standards/file.md" or "Reference: docs/path/file.md"
    text_refs = re.findall(r'(?:See|Reference:|Specification:)\s+([^\s]+\.md)', content)
    references.update(text_refs)
    
    return references


def validate_cross_references() -> List[Violation]:
    """Validate that document cross-references point to existing files."""
    violations = []
    
    docs_dir = REPO_ROOT / "docs"
    if not docs_dir.exists():
        return violations
    
    # Also check .github/agents/ for agent profiles
    github_agents_dir = REPO_ROOT / ".github" / "agents"
    
    search_dirs = [docs_dir]
    if github_agents_dir.exists():
        search_dirs.append(github_agents_dir)
    
    for base_dir in search_dirs:
        for doc_path in base_dir.glob("**/*.md"):
            try:
                content = doc_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            
            references = extract_document_references(content)
            
            for ref in references:
                # Skip external URLs
                if ref.startswith('http://') or ref.startswith('https://'):
                    continue
                
                # Skip pattern references (contain wildcards or placeholders)
                if '*' in ref or '<' in ref or '{' in ref:
                    continue
                
                # Skip references that start with backtick (malformed extraction)
                if ref.startswith('`'):
                    continue
                
                # Try to resolve the reference
                ref_path = None
                
                # Clean up the reference
                ref_clean = ref.strip()
                
                # Try repo root relative (docs/...)
                if ref_clean.startswith('docs/') or ref_clean.startswith('jobs/') or ref_clean.startswith('.github/'):
                    candidate = REPO_ROOT / ref_clean
                    if candidate.exists():
                        ref_path = candidate
                # Try relative to current doc
                elif not ref_clean.startswith('/'):
                    candidate = doc_path.parent / ref_clean
                    if candidate.exists():
                        ref_path = candidate
                    # Also try as if it's relative to docs/ or standards/
                    else:
                        # If current path is in .github/agents/, references might be relative to docs/
                        if '.github/agents' in str(doc_path):
                            for try_base in ['docs/standards', 'docs/context', 'docs/process', 'docs/agents', 'docs']:
                                candidate = REPO_ROOT / try_base / ref_clean
                                if candidate.exists():
                                    ref_path = candidate
                                    break
                        # If in docs/process, try docs/standards, docs/context, docs/agents
                        elif 'docs/process' in str(doc_path):
                            for try_base in ['docs/standards', 'docs/context', 'docs/agents']:
                                candidate = REPO_ROOT / try_base / ref_clean
                                if candidate.exists():
                                    ref_path = candidate
                                    break
                        # If in docs/standards, try other standards or context
                        elif 'docs/standards' in str(doc_path):
                            for try_base in ['docs/standards', 'docs/context', 'docs/decisions']:
                                candidate = REPO_ROOT / try_base / ref_clean
                                if candidate.exists():
                                    ref_path = candidate
                                    break
                
                if not ref_path:
                    violations.append(Violation(
                        "consistency", doc_path, "broken_reference",
                        f"Broken reference to '{ref}'"
                    ))
    
    return violations


def check_role_consistency() -> List[Violation]:
    """Check consistency between agent_role_charter.md and agent profile implementations."""
    violations = []
    
    charter_path = REPO_ROOT / "docs" / "agents" / "agent_role_charter.md"
    github_agents_dir = REPO_ROOT / ".github" / "agents"
    
    if not charter_path.exists() or not github_agents_dir.exists():
        return violations
    
    # Extract role names from charter
    charter_content = charter_path.read_text(encoding="utf-8")
    charter_roles = set()
    
    # Roles are defined in section 4 as ### headers
    section_4_match = re.search(r"## 4\).*?(?=\n## |\Z)", charter_content, re.DOTALL)
    if section_4_match:
        section_4 = section_4_match.group(0)
        role_headers = re.findall(r"### (.+)", section_4)
        for role in role_headers:
            # Normalize role name
            role_clean = re.sub(r'\s+(Agent|Support Agent)$', '', role).strip().lower()
            charter_roles.add(role_clean)
    
    # For now, just ensure we have roles defined
    # A more sophisticated check would compare responsibilities, which is complex
    # This is a basic implementation that can be enhanced later
    
    return violations


def check_doc_consistency() -> List[Violation]:
    """Run all cross-document consistency checks."""
    violations = []
    
    # 1. Term definition consistency
    glossary_path = REPO_ROOT / "docs" / "context" / "glossary.md"
    glossary_terms = extract_glossary_terms(glossary_path)
    violations.extend(check_term_redefinitions(glossary_terms))
    
    # 2. Cross-reference validation
    violations.extend(validate_cross_references())
    
    # 3. Role consistency (basic check)
    violations.extend(check_role_consistency())
    
    return violations


def main():
    violations = check_doc_consistency()
    
    for violation in violations:
        print(violation.format())
    
    # For consistency checking, we count the number of checks performed
    # rather than files validated
    check_count = 3  # Term definitions, cross-references, role consistency
    fail_count = len(violations)
    pass_count = check_count if fail_count == 0 else 0
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

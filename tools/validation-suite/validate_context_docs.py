#!/usr/bin/env python3
"""
Context Layer Documentation Validator

Validates the structure and consistency of context layer documents in docs/context/:
- development_approach.md
- target_agent_system.md
- system_context.md
- glossary.md

These documents establish foundational principles, truth hierarchy, and terminology.
"""
import re
import sys
from pathlib import Path
from typing import List, Dict, Set

REPO_ROOT = Path(__file__).resolve().parents[2]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def validate_development_approach(path: Path) -> List[Violation]:
    """Validate development_approach.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "context_docs", path, "missing_file",
            "development_approach.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Required sections
    required_sections = [
        "# Development Approach",
        "## Purpose",
        "## Core Principles",
        "## Definitions",
        "## Agents and Tools",
        "## Sequential Development Process",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "context_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    # Check for Core Principles subsections (1-6)
    core_principles_found = False
    for i, line in enumerate(lines):
        if line.strip() == "## Core Principles":
            core_principles_found = True
            # Look for numbered subsections
            subsections_found = 0
            for j in range(i+1, min(i+100, len(lines))):
                if lines[j].startswith("###"):
                    subsections_found += 1
                elif lines[j].startswith("##"):
                    break
            if subsections_found < 6:
                violations.append(Violation(
                    "context_docs", path, "insufficient_principles",
                    f"Core Principles should have at least 6 subsections, found {subsections_found}"
                ))
            break
    
    # Check for 5 steps in Sequential Development Process
    steps_pattern = re.compile(r"### .*Step \d:")
    steps_found = len(steps_pattern.findall(content))
    if steps_found < 5:
        violations.append(Violation(
            "context_docs", path, "insufficient_steps",
            f"Sequential Development Process should have 5 steps, found {steps_found}"
        ))
    
    return violations


def validate_target_agent_system(path: Path) -> List[Violation]:
    """Validate target_agent_system.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "context_docs", path, "missing_file",
            "target_agent_system.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections
    required_sections = [
        "# Target Agent System",
        "## Purpose",
        "## Scope and Authority",
        "## Definitions",
        "## Non-Negotiable Operating Rules",
        "## Agents and Their Responsibilities",
        "## Tools and How They Are Used",
        "## Approval Gates and Evidence Discipline",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "context_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    return violations


def validate_system_context(path: Path) -> List[Violation]:
    """Validate system_context.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "context_docs", path, "missing_file",
            "system_context.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections
    required_sections = [
        "# System Context",
        "## Purpose",
        "## 1) What this repository is",
        "## 2) Scope boundaries",
        "## 3) The working approach this repo is built to support",
        "## 4) How truth is established",
        "## 5) Documentation architecture",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "context_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    return violations


def validate_glossary(path: Path) -> List[Violation]:
    """Validate glossary.md structure and check for duplicate term definitions."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "context_docs", path, "missing_file",
            "glossary.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Required sections
    required_sections = [
        "# Glossary",
        "## Purpose",
        "## Usage rule",
    ]
    
    for section in required_sections:
        if section not in content:
            violations.append(Violation(
                "context_docs", path, "missing_section",
                f"Missing required section: {section}"
            ))
    
    # Extract all term definitions (### headers)
    terms: Dict[str, List[int]] = {}
    for i, line in enumerate(lines, 1):
        if line.startswith("### "):
            term = line[4:].strip()
            if term not in terms:
                terms[term] = []
            terms[term].append(i)
    
    # Check for duplicate term definitions
    for term, line_numbers in terms.items():
        if len(line_numbers) > 1:
            violations.append(Violation(
                "context_docs", path, "duplicate_term",
                f"Term '{term}' is defined multiple times at lines: {', '.join(map(str, line_numbers))}"
            ))
    
    # Check that terms are organized under letter sections (## A, ## B, etc.)
    letter_sections = [line for line in lines if re.match(r"^## [A-Z]$", line)]
    if len(letter_sections) == 0:
        violations.append(Violation(
            "context_docs", path, "missing_letter_sections",
            "Glossary should organize terms under letter sections (## A, ## B, etc.)"
        ))
    
    return violations


def validate_context_layer() -> List[Violation]:
    """Validate all context layer documents."""
    violations = []
    
    context_dir = REPO_ROOT / "docs" / "context"
    
    # Validate each document
    violations.extend(validate_development_approach(context_dir / "development_approach.md"))
    violations.extend(validate_target_agent_system(context_dir / "target_agent_system.md"))
    violations.extend(validate_system_context(context_dir / "system_context.md"))
    violations.extend(validate_glossary(context_dir / "glossary.md"))
    
    return violations


def main():
    violations = validate_context_layer()
    
    for violation in violations:
        print(violation.format())
    
    # Count files that were successfully validated (exist and have no violations)
    context_dir = REPO_ROOT / "docs" / "context"
    context_files = [
        context_dir / "development_approach.md",
        context_dir / "target_agent_system.md",
        context_dir / "system_context.md",
        context_dir / "glossary.md",
    ]
    
    files_with_violations = set(v.path for v in violations)
    pass_count = sum(1 for f in context_files if f.exists() and f not in files_with_violations)
    fail_count = len(violations)
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

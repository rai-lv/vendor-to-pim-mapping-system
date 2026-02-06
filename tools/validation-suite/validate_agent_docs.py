#!/usr/bin/env python3
"""
Agent Layer Documentation Validator

Validates the structure and consistency of agent layer documents:
- docs/agents/agent_role_charter.md
- .github/agents/*.md (agent profile files with YAML frontmatter)

These documents define agent roles, responsibilities, and operating rules.
"""
import re
import sys
from pathlib import Path
from typing import List, Set, Dict

import yaml

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.config import TOOL_PATHS, REPO_ROOT


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def validate_agent_role_charter(path: Path) -> List[Violation]:
    """Validate agent_role_charter.md structure."""
    violations = []
    
    if not path.exists():
        violations.append(Violation(
            "agent_docs", path, "missing_file",
            "agent_role_charter.md does not exist"
        ))
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Required sections (flexible matching)
    required_section_patterns = [
        (r"# Agent Role Charter", "title"),
        (r"## 1\) Purpose Statement", "section 1"),
        (r"## 2\) Authority", "section 2"),
        (r"## 3\) Agents vs Tools", "section 3"),
        (r"## 4\) Canonical Agent Roles", "section 4"),
        (r"## 5\) Document Boundaries", "section 5"),
        (r"## 6\) How This Charter Is Used", "section 6"),
        (r"## 7\) Relationship to Other Documents", "section 7"),
    ]
    
    for pattern, section_name in required_section_patterns:
        if not re.search(pattern, content):
            violations.append(Violation(
                "agent_docs", path, "missing_section",
                f"Missing required {section_name}"
            ))
    
    # Check for canonical agent roles (at least 6)
    role_pattern = re.compile(r"### .+ (Agent|Support Agent)")
    roles_found = len(role_pattern.findall(content))
    if roles_found < 6:
        violations.append(Violation(
            "agent_docs", path, "insufficient_roles",
            f"Section 4 should define at least 6 agent roles, found {roles_found}"
        ))
    
    return violations


def validate_agent_profile(path: Path) -> List[Violation]:
    """Validate individual agent profile file (.github/agents/*.md)."""
    violations = []
    
    if not path.exists():
        return violations
    
    content = path.read_text(encoding="utf-8")
    
    # Check for YAML frontmatter
    if not content.startswith("---"):
        violations.append(Violation(
            "agent_docs", path, "missing_frontmatter",
            "Agent profile must start with YAML frontmatter (---)"
        ))
        return violations
    
    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        violations.append(Violation(
            "agent_docs", path, "invalid_frontmatter",
            "Agent profile frontmatter is not properly closed with ---"
        ))
        return violations
    
    frontmatter_text = parts[1]
    body = parts[2]
    
    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        violations.append(Violation(
            "agent_docs", path, "invalid_yaml",
            f"Invalid YAML in frontmatter: {e}"
        ))
        return violations
    
    # Check required frontmatter fields
    if not isinstance(frontmatter, dict):
        violations.append(Violation(
            "agent_docs", path, "invalid_frontmatter_structure",
            "Frontmatter must be a YAML mapping/object"
        ))
        return violations
    
    required_fields = ["name", "description"]
    for field in required_fields:
        if field not in frontmatter:
            violations.append(Violation(
                "agent_docs", path, "missing_frontmatter_field",
                f"Frontmatter missing required field: {field}"
            ))
    
    # Check filename matches frontmatter name (if name is present)
    if "name" in frontmatter:
        expected_filename = f"{frontmatter['name']}.md"
        # Also check for .agent.md suffix
        expected_filename_alt = f"{frontmatter['name']}.agent.md"
        if path.name != expected_filename and path.name != expected_filename_alt:
            violations.append(Violation(
                "agent_docs", path, "filename_mismatch",
                f"Filename '{path.name}' does not match frontmatter name '{frontmatter['name']}' (expected '{expected_filename}' or '{expected_filename_alt}')"
            ))
    
    return violations


def check_role_overlap(charter_path: Path, agent_profile_dir: Path) -> List[Violation]:
    """Check for role overlap or conflicts between agent_role_charter.md and agent profiles."""
    violations = []
    
    if not charter_path.exists():
        return violations
    
    # Extract roles from charter
    charter_content = charter_path.read_text(encoding="utf-8")
    charter_roles = set()
    
    # Find section 4 (Canonical Agent Roles)
    section_4_start = charter_content.find("## 4) Canonical Agent Roles")
    if section_4_start != -1:
        section_4_end = charter_content.find("\n## 5)", section_4_start)
        if section_4_end == -1:
            section_4_content = charter_content[section_4_start:]
        else:
            section_4_content = charter_content[section_4_start:section_4_end]
        
        # Extract role names from ### headers
        role_pattern = re.compile(r"### (.+)")
        for match in role_pattern.finditer(section_4_content):
            role_name = match.group(1).strip()
            charter_roles.add(role_name.lower())
    
    # Extract agent names from profiles
    profile_names = set()
    if agent_profile_dir.exists():
        for profile_path in agent_profile_dir.glob("*.md"):
            content = profile_path.read_text(encoding="utf-8")
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1])
                        if isinstance(frontmatter, dict) and "name" in frontmatter:
                            profile_names.add(frontmatter["name"].lower())
                    except (yaml.YAMLError, KeyError):
                        pass
    
    # Note: We don't enforce strict overlap checking as agent profiles may have
    # different granularity than charter roles. This is a placeholder for future
    # more sophisticated overlap detection.
    
    return violations


def validate_agent_layer() -> List[Violation]:
    """Validate all agent layer documents."""
    violations = []
    
    agents_dir = TOOL_PATHS.docs_agents
    github_agents_dir = TOOL_PATHS.github_agents
    
    # Validate agent_role_charter.md
    charter_path = agents_dir / "agent_role_charter.md"
    violations.extend(validate_agent_role_charter(charter_path))
    
    # Validate all agent profiles in .github/agents/
    if github_agents_dir.exists():
        for profile_path in github_agents_dir.glob("*.md"):
            violations.extend(validate_agent_profile(profile_path))
    
    # Check for role overlap/conflicts
    violations.extend(check_role_overlap(charter_path, github_agents_dir))
    
    return violations


def main():
    violations = validate_agent_layer()
    
    for violation in violations:
        print(violation.format())
    
    # Count files that were successfully validated (exist and have no violations)
    agents_dir = TOOL_PATHS.docs_agents
    github_agents_dir = TOOL_PATHS.github_agents
    
    agent_files = [agents_dir / "agent_role_charter.md"]
    if github_agents_dir.exists():
        agent_files.extend(github_agents_dir.glob("*.md"))
    
    files_with_violations = set(v.path for v in violations)
    pass_count = sum(1 for f in agent_files if f.exists() and f not in files_with_violations)
    fail_count = len(violations)
    
    print(f"SUMMARY pass={pass_count} fail={fail_count}")
    
    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())

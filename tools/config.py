#!/usr/bin/env python3
"""
Tool Configuration Module

Centralized configuration for tool paths and settings.
Provides consistent path references across all tools in the repository.

This replaces hardcoded path strings with configurable constants.
"""
from pathlib import Path


class ToolPaths:
    """Centralized path configuration for all tools."""
    
    def __init__(self, repo_root: Path = None):
        """
        Initialize tool paths configuration.
        
        Args:
            repo_root: Optional override for repository root. 
                      If None, auto-detects from __file__ location.
        """
        if repo_root is None:
            # Auto-detect: tools/config.py -> repo_root is 1 parent up
            self._repo_root = Path(__file__).resolve().parent.parent
        else:
            self._repo_root = Path(repo_root).resolve()
    
    @property
    def repo_root(self) -> Path:
        """Repository root directory."""
        return self._repo_root
    
    # Documentation directories
    @property
    def docs_root(self) -> Path:
        """Root documentation directory (docs/)."""
        return self._repo_root / "docs"
    
    @property
    def docs_context(self) -> Path:
        """Context layer documentation (docs/context/)."""
        return self.docs_root / "context"
    
    @property
    def docs_process(self) -> Path:
        """Process layer documentation (docs/process/)."""
        return self.docs_root / "process"
    
    @property
    def docs_agents(self) -> Path:
        """Agent layer documentation (docs/agents/)."""
        return self.docs_root / "agents"
    
    @property
    def docs_decisions(self) -> Path:
        """Decision records (docs/decisions/)."""
        return self.docs_root / "decisions"
    
    @property
    def docs_catalogs(self) -> Path:
        """Catalog documents (docs/catalogs/)."""
        return self.docs_root / "catalogs"
    
    @property
    def docs_standards(self) -> Path:
        """Standard specifications (docs/standards/)."""
        return self.docs_root / "standards"
    
    @property
    def docs_tasks(self) -> Path:
        """Task specifications (docs/tasks/)."""
        return self.docs_root / "tasks"
    
    @property
    def docs_registries(self) -> Path:
        """Registry files (docs/registries/)."""
        return self.docs_root / "registries"
    
    # Specific catalog files
    @property
    def artifacts_catalog(self) -> Path:
        """Artifacts catalog file (docs/catalogs/artifacts_catalog.md)."""
        return self.docs_catalogs / "artifacts_catalog.md"
    
    @property
    def job_inventory(self) -> Path:
        """Job inventory file (docs/catalogs/job_inventory.md)."""
        return self.docs_catalogs / "job_inventory.md"
    
    @property
    def decision_log(self) -> Path:
        """Decision log index (docs/catalogs/decision_log.md)."""
        return self.docs_catalogs / "decision_log.md"
    
    # Specific standard files
    @property
    def glossary(self) -> Path:
        """Glossary file (docs/context/glossary.md)."""
        return self.docs_context / "glossary.md"
    
    @property
    def agent_role_charter(self) -> Path:
        """Agent role charter (docs/agents/agent_role_charter.md)."""
        return self.docs_agents / "agent_role_charter.md"
    
    # Registry files
    @property
    def shared_artifacts_allowlist(self) -> Path:
        """Shared artifacts allowlist (docs/registries/shared_artifacts_allowlist.yaml)."""
        return self.docs_registries / "shared_artifacts_allowlist.yaml"
    
    # Job-related paths
    @property
    def jobs_root(self) -> Path:
        """Root jobs directory (jobs/)."""
        return self._repo_root / "jobs"
    
    def job_manifests_pattern(self) -> str:
        """Pattern for finding job manifest files."""
        return "jobs/*/*/job_manifest.yaml"
    
    # GitHub paths
    @property
    def github_root(self) -> Path:
        """GitHub configuration directory (.github/)."""
        return self._repo_root / ".github"
    
    @property
    def github_agents(self) -> Path:
        """GitHub agent profiles (.github/agents/)."""
        return self.github_root / "agents"
    
    # Tool paths
    @property
    def tools_root(self) -> Path:
        """Tools directory (tools/)."""
        return self._repo_root / "tools"
    
    @property
    def validation_suite(self) -> Path:
        """Validation suite directory (tools/validation-suite/)."""
        return self.tools_root / "validation-suite"
    
    # Log paths
    @property
    def logs_root(self) -> Path:
        """Logs directory (logs/)."""
        return self._repo_root / "logs"
    
    # Root-level files
    @property
    def readme(self) -> Path:
        """Repository README.md."""
        return self._repo_root / "README.md"


# Default global instance for convenience
# Tools can import this directly: from tools.config import TOOL_PATHS
TOOL_PATHS = ToolPaths()


# Backward compatibility: export REPO_ROOT for minimal changes
REPO_ROOT = TOOL_PATHS.repo_root

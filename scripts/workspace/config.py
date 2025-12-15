#!/usr/bin/env python3
"""
Configuration management module
Handles loading and managing repository configurations
"""

import copy
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore


class ConfigManager:
    """Manages repository configuration loading and processing"""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def load_repository_config(self) -> Dict[str, Any]:
        """Load existing repository configuration or return defaults"""
        config_file = self.repo_path / ".omd" / "repository.yaml"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) if yaml else {}
                    return config or {}
            except (OSError, IOError, yaml.YAMLError) as e:
                print(f"  ⚠️  Error loading repository.yaml: {e}")

        # Return default repository configuration
        return {
            "name": self.repo_path.name,
            "description": "",
            "ci_platform": "github",
            "types": ["lib"],
            "languages": [],
            "tags": [],
        }

    def load_language_overrides(self) -> Dict[str, Any]:
        """Load language-specific configuration overrides"""
        overrides_file = self.repo_path / ".omd" / "overrides.yaml"
        if overrides_file.exists():
            try:
                with open(overrides_file, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) if yaml else {}
            except (OSError, IOError, yaml.YAMLError) as e:
                print(f"  ⚠️  Error loading overrides.yaml: {e}")
        return {}

    def save_repository_config(self, config: Dict[str, Any]) -> bool:
        """Save repository configuration to file"""
        config_file = self.repo_path / ".omd" / "repository.yaml"
        config_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                if yaml:
                    yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
                else:
                    # Fallback if yaml not available
                    print("  ⚠️  PyYAML not installed - cannot save configuration")
                    return False
            return True
        except (OSError, IOError, yaml.YAMLError) as e:
            print(f"  ⚠️  Error saving repository.yaml: {e}")
            return False

    def apply_user_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply user-defined configuration overrides"""
        overrides = self.load_language_overrides()
        if not overrides:
            return config

        result = copy.deepcopy(config)

        # Apply repository-level overrides
        if "repository" in overrides:
            self._apply_repository_overrides(result, overrides["repository"])

        # Apply language-specific overrides
        if "languages" in overrides and "languages" in result:
            result["languages"] = self._apply_language_overrides(
                result["languages"], overrides["languages"]
            )

        return result

    def _apply_repository_overrides(
        self, config: Dict[str, Any], repo_overrides: Dict[str, Any]
    ):
        """Apply repository-level configuration overrides"""
        for key, value in repo_overrides.items():
            if key in ["platform", "ci_platform", "deployment_platform", "types", "languages", "tags"]:
                if value is not None:
                    config[key] = value
            elif key == "name" and value:
                config["name"] = value
            elif key == "description" and value is not None:
                config["description"] = value

    def _apply_language_overrides(
        self, languages: List[str], lang_overrides: Dict[str, Any]
    ) -> List[str]:
        """Apply language-specific overrides to language list"""
        result = languages.copy()

        # Add languages specified in overrides
        for lang in lang_overrides.keys():
            if lang not in result:
                result.append(lang)

        return result


class RepositoryConfig:
    """Repository configuration data container"""

    def __init__(self, repo_path: Path, tools_dir: Path):
        self.repo_path = repo_path
        self.tools_dir = tools_dir
        self.config_manager = ConfigManager(repo_path)

        # Load initial configuration
        raw_config = self.config_manager.load_repository_config()
        self.config = self.config_manager.apply_user_overrides(raw_config)

        # Extract configuration values
        self.name = self.config.get("name", repo_path.name)
        self.description = self.config.get("description", "")
        self.ci_platform = self.config.get("ci_platform", self.config.get("platform", "github"))
        self.deployment_platform = self.config.get("deployment_platform")
        self.types = self.config.get("types", ["lib"])
        self.languages = self.config.get("languages", [])
        self.tags = self.config.get("tags", [])

    def get_platform_specific_config(self) -> Dict[str, Any]:
        """Get platform-specific configuration options"""
        platform_configs = {
            "github": {
                "default_branch": "main",
                "issue_templates": True,
                "pr_templates": True,
                "workflows": True,
            },
            "gitlab": {
                "default_branch": "main",
                "merge_request_templates": True,
                "pipelines": True,
            },
            "azure": {
                "default_branch": "main",
                "work_item_templates": True,
                "pipelines": True,
            },
            "bitbucket": {
                "default_branch": "main",
                "pull_request_templates": True,
                "pipelines": True,
            },
        }
        return platform_configs.get(self.ci_platform, platform_configs["github"])

    def get_type_specific_config(self) -> Dict[str, Any]:
        """Get configuration based on repository types"""
        type_configs = {
            "app": {"dockerfile": True, "compose": True, "ci_cd": True},
            "lib": {"packaging": True, "documentation": True, "testing": True},
            "cli": {"installation": True, "help_system": True, "config_files": True},
            "service": {"health_checks": True, "monitoring": True, "scaling": True},
            "infra": {"terraform": True, "compliance": True, "security": True},
            "docs": {"static_site": True, "search": True, "navigation": True},
            "template": {"examples": True, "variables": True, "documentation": True},
        }

        merged_config = {}
        for repo_type in self.types:
            if repo_type in type_configs:
                merged_config.update(type_configs[repo_type])

        return merged_config

    def to_dict(self) -> dict[str, Any]:
        """Convert repository configuration to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "ci_platform": self.ci_platform,
            "deployment_platform": self.deployment_platform,
            "types": self.types,
            "languages": self.languages,
            "tags": self.tags,
        }

    def save(self) -> bool:
        """Save current configuration to file"""
        return self.config_manager.save_repository_config(self.to_dict())

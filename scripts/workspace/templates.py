#!/usr/bin/env python3
"""
Jinja2 template functions module
Contains all template utility functions and formatters
"""

import copy
import json
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class TemplateContext:
    """Manages template context and custom functions"""

    def __init__(self, tools_dir: Path, jinja_env):
        self.tools_dir = tools_dir
        self.templates_dir = tools_dir / "templates"
        self.jinja_env = jinja_env
        self._current_platform = "github"
        self._current_types = ["lib"]
        self._current_repo_path: Optional[Path] = None

    def set_current_context(self, platform: str, types: list, repo_path: Path):
        """Set current template context"""
        self._current_platform = platform
        self._current_types = types
        self._current_repo_path = repo_path

    def create_load_yaml_func(self):
        """Create load_yaml function for templates"""

        def load_yaml_func(path):
            config_file = self.templates_dir / path
            if not config_file.exists():
                print(f"  ⚠️  Template config file not found: {path}")
                return {}
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except (yaml.YAMLError, IOError, OSError) as e:
                print(f"  ⚠️  Error loading template config {path}: {e}")
                return {}

        return load_yaml_func

    def create_load_enhanced_config_func(self):
        """Create load_enhanced_language_config function for templates"""

        def load_enhanced_language_config(language):
            """Load detailed language configuration from languages/ templates"""
            template_path = f"languages/{language}.yaml.j2"
            try:
                template = self.jinja_env.get_template(template_path)
                # Render with current metadata context
                rendered_content = template.render(
                    language=language,
                    languages=[language],  # For template compatibility
                    platform=self._current_platform,
                    types=self._current_types,
                )
                return yaml.safe_load(rendered_content)
            except (yaml.YAMLError, IOError, OSError):
                return None

        return load_enhanced_language_config

    def create_load_workspace_config_func(self):
        """Create load_workspace_config function for templates"""

        def load_workspace_config():
            """Load workspace configuration for current repository"""
            if self._current_repo_path:
                return self.load_workspace_config(self._current_repo_path)
            return {"workspace": {}, "copilot": {}}

        return load_workspace_config

    def load_workspace_config(self, repo_path: Path) -> Dict[str, Any]:
        """Load existing workspace configuration or return defaults"""
        workspace_file = repo_path / ".omd" / "workspace.yaml"
        if workspace_file.exists():
            try:
                with open(workspace_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}
                    return config
            except (yaml.YAMLError, IOError, OSError) as e:
                print(f"  ⚠️  Error loading workspace.yaml: {e}")

        # Return default configuration if file doesn't exist or has errors
        return {
            "workspace": {
                "additional_folders": [],
                "settings": {},
                "recommended_extensions": [],
                "unwanted_extensions": [],
                "tasks": [],
                "launch_configurations": [],
            },
            "copilot": {"instructions": [], "rules": [], "apply_to": "**"},
        }

    def create_apply_overrides_func(self):
        """Create apply_language_overrides function for templates"""

        def apply_language_overrides(settings, language, overrides):
            """Apply language-specific overrides to settings"""
            if not overrides or language not in overrides:
                return settings

            result = copy.deepcopy(settings)
            lang_override = overrides[language]

            if "settings" in lang_override:
                self._apply_settings_overrides(result, lang_override["settings"])

            return result

        return apply_language_overrides

    def _apply_settings_overrides(self, result, settings_overrides):
        """Apply settings overrides to the result dictionary"""
        for key, value in settings_overrides.items():
            if value is None:
                self._remove_setting(result, key)
            elif self._should_deep_merge(result, key, value):
                self._deep_merge_setting(result, key, value)
            else:
                self._update_setting(result, key, value)

    def _remove_setting(self, result, key):
        """Remove a setting from the result"""
        result.pop(key, None)

    def _should_deep_merge(self, result, key, value):
        """Check if settings should be deep merged"""
        return (
            key in result and isinstance(result[key], dict) and isinstance(value, dict)
        )

    def _deep_merge_setting(self, result, key, value):
        """Deep merge nested setting objects"""
        for nested_key, nested_val in value.items():
            if nested_val is None:
                result[key].pop(nested_key, None)
            else:
                result[key][nested_key] = nested_val

    def _update_setting(self, result, key, value):
        """Update or add a setting"""
        result[key] = value

    @staticmethod
    def format_yaml_json(obj, indent_level=0):
        """Format JSON objects and arrays with YAML-style readability and trailing commas"""
        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, str):
            return json.dumps(obj)
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, list):
            return TemplateContext._format_json_list(obj, indent_level)
        elif isinstance(obj, dict):
            return TemplateContext._format_json_dict(obj, indent_level)
        else:
            return json.dumps(obj)

    @staticmethod
    def _format_json_list(obj, indent_level):
        """Format JSON list with proper indentation"""
        if not obj:
            return "[]"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for item in obj:
            formatted_item = TemplateContext.format_yaml_json(item, indent_level + 1)
            items.append(f"{item_indent}{formatted_item},")
        return "[\n" + "\n".join(items) + "\n" + base_indent + "]"

    @staticmethod
    def _format_json_dict(obj, indent_level):
        """Format JSON dictionary with proper indentation"""
        if not obj:
            return "{}"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for key, value in obj.items():
            formatted_value = TemplateContext.format_yaml_json(value, indent_level + 1)
            items.append(f"{item_indent}{json.dumps(key)}: {formatted_value},")
        return "{\n" + "\n".join(items) + "\n" + base_indent + "}"

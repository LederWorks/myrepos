#!/usr/bin/env python3
"""
Cross-platform myrepos tooling system
Supports Windows, macOS, and Linux with explicit metadata configuration
"""

import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from .config import RepositoryConfig
from .detection import RepositoryDetector

# Constants
REPOSITORY_METADATA_FILE = "repository.yaml"


class WorkspaceGenerator:
    """Generates VS Code workspace and configuration files"""

    def __init__(self, tools_dir: Path):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = self.tools_dir / "templates"

        # Initialize template context attributes
        self._current_platform: Optional[str] = None
        self._current_types: Optional[List[str]] = None
        self._current_repo_path: Optional[Path] = None

        # Setup Jinja2 environment with custom functions
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom functions
        self._register_jinja_functions()

    def _register_jinja_functions(self) -> None:
        """Register custom functions for Jinja2 templates"""
        self.jinja_env.globals["load_yaml"] = self._create_load_yaml_func()
        self.jinja_env.globals["load_enhanced_language_config"] = (
            self._create_load_enhanced_config_func()
        )
        self.jinja_env.globals["load_workspace_config"] = (
            self._create_load_workspace_config_func()
        )
        self.jinja_env.globals["apply_language_overrides"] = (
            self._create_apply_overrides_func()
        )
        self.jinja_env.globals["format_yaml_json"] = self._format_yaml_json

    def _create_load_yaml_func(self):
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

    def _create_load_enhanced_config_func(self):
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
                    platform=getattr(self, "_current_platform", "github"),
                    types=getattr(self, "_current_types", ["lib"]),
                )
                return yaml.safe_load(rendered_content)
            except TemplateNotFound:
                return None
            except (yaml.YAMLError, ValueError) as e:
                print(f"  ⚠️  Error loading enhanced config for {language}: {e}")
                return None

        return load_enhanced_language_config

    def _create_load_workspace_config_func(self):
        """Create load_workspace_config function for templates"""

        def load_workspace_config():
            """Load workspace configuration for current repository"""
            if hasattr(self, "_current_repo_path"):
                return self._load_workspace_config(self._current_repo_path)
            return {"workspace": {}, "copilot": {}}

        return load_workspace_config

    def _load_workspace_config(self, repo_path: Path) -> Dict[str, Any]:
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

    def _create_apply_overrides_func(self):
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

    def _format_yaml_json(self, obj, indent_level=0):
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
            return self._format_json_list(obj, indent_level)
        elif isinstance(obj, dict):
            return self._format_json_dict(obj, indent_level)
        else:
            return json.dumps(obj)

    def _format_json_list(self, obj, indent_level):
        """Format JSON list with proper indentation"""
        if not obj:
            return "[]"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for item in obj:
            formatted_item = self._format_yaml_json(item, indent_level + 1)
            items.append(f"{item_indent}{formatted_item},")
        return "[\n" + "\n".join(items) + "\n" + base_indent + "]"

    def _format_json_dict(self, obj, indent_level):
        """Format JSON dictionary with proper indentation"""
        if not obj:
            return "{}"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for key, value in obj.items():
            formatted_value = self._format_yaml_json(value, indent_level + 1)
            items.append(f"{item_indent}{json.dumps(key)}: {formatted_value},")
        return "{\n" + "\n".join(items) + "\n" + base_indent + "}"

    def setup_repository(self, repo_path: Path) -> None:
        """Setup VS Code workspace and configuration for a repository"""
        try:
            config = RepositoryConfig(repo_path, self.tools_dir)

            # Store current metadata and repo path for templates
            self._current_platform = config.platform
            self._current_types = config.types
            self._current_repo_path = repo_path

            print(f"🔍 Processing repository: {config.name}")
            print("📊 Detected content:")
            print(f"        platform: {config.platform}")
            print(f"        languages: {','.join(config.languages)}")
            print(f"        types: {','.join(config.types)}")

            self._create_workspace_file(config)
            self._create_vscode_config(config)
            self._create_omd_files(config)
            self._update_gitignore(config)
            self.generate_copilot_instructions()

            print(f"✅ Setup completed for {config.name}")

        except FileNotFoundError:
            print("🔍 No metadata found, auto-detecting repository configuration...")
            self._auto_detect_and_setup(repo_path)

        except (ValueError, yaml.YAMLError) as e:
            print(f"❌ Metadata error: {e}")

    def _auto_detect_and_setup(self, repo_path: Path) -> None:
        """Auto-detect repository configuration and set up workspace"""
        repo_path = Path(repo_path)

        # Use repository detector for auto-detection
        detector = RepositoryDetector()
        languages = detector.detect_languages(repo_path)
        platform = detector.detect_platform(repo_path)
        repo_types = detector.detect_repository_types(repo_path)

        # Create detected configuration
        detected_config = {
            "name": repo_path.name,
            "description": f"Auto-detected repository: {repo_path.name}",
            "platform": platform,
            "types": repo_types,
            "languages": languages,
            "tags": [],
        }

        print("📊 Auto-detected content:")
        print(f"        platform: {detected_config['platform']}")
        print(f"        languages: {','.join(detected_config['languages'])}")
        print(f"        types: {','.join(detected_config['types'])}")

        # Save detected configuration first
        self._save_detected_metadata(repo_path, detected_config)

        # Now create proper config object using the saved metadata
        config = RepositoryConfig(repo_path, self.tools_dir)

        # Store current context for templates
        self._current_platform = config.platform
        self._current_types = config.types
        self._current_repo_path = repo_path

        # Generate workspace files
        self._create_workspace_file(config)
        self._create_vscode_config(config)
        self._create_omd_files(config)
        self._update_gitignore(config)

        print(f"✅ Auto-setup completed for {config.name}")
        print("💡 Configuration saved to .omd/repository.yaml - edit as needed")

    def _detect_languages(self, repo_path: Path) -> List[str]:
        """Auto-detect languages from file extensions"""
        language_patterns = {
            "terraform": [".tf", ".tfvars", ".hcl", ".tftpl"],
            "python": [".py", ".pyx", ".pyi"],
            "go": [".go", "go.mod", "go.sum"],
            "markdown": [".md", ".markdown", ".mdx"],
            "yaml": [".yml", ".yaml"],
            "json": [".json", ".jsonc"],
            "shell": [".sh", ".bash", ".zsh"],
            "powershell": [".ps1", ".psm1", ".psd1"],
            "sql": [".sql"],
            "j2": [".j2", ".jinja", ".jinja2"],
        }

        detected_languages = set()

        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and not self._is_ignored_path(file_path, repo_path):
                language = self._detect_language_for_file(file_path, language_patterns)
                if language:
                    detected_languages.add(language)

        return sorted(detected_languages) if detected_languages else ["markdown"]

    def _detect_language_for_file(
        self, file_path: Path, language_patterns: Dict[str, List[str]]
    ) -> Optional[str]:
        """Detect language for a specific file"""
        file_ext = file_path.suffix.lower()
        file_name = file_path.name.lower()

        for language, patterns in language_patterns.items():
            for pattern in patterns:
                if file_ext == pattern or file_name == pattern:
                    return language

        return None

    def _detect_platform(self, repo_path: Path) -> str:
        """Auto-detect CI/CD platform"""
        platform_indicators = {
            "github": [".github/", ".github/workflows/"],
            "azuredevops": ["azure-pipelines.yml", ".azure/", "azure-pipelines.yaml"],
        }

        for platform, indicators in platform_indicators.items():
            for indicator in indicators:
                check_path = repo_path / indicator
                if check_path.exists():
                    return platform

        return "github"  # Default fallback

    def _detect_repository_types(self, repo_path: Path) -> List[str]:
        """Auto-detect repository types based on content"""
        detected_types: set[str] = set()

        self._detect_infra_type(repo_path, detected_types)
        self._detect_python_lib_type(repo_path, detected_types)
        self._detect_nodejs_type(repo_path, detected_types)
        self._detect_docker_app_type(repo_path, detected_types)
        self._detect_docs_type(repo_path, detected_types)
        self._detect_template_type(repo_path, detected_types)

        return sorted(detected_types) if detected_types else ["lib"]

    def _detect_infra_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for infrastructure repository patterns"""
        if (repo_path / "main.tf").exists() or (repo_path / "terraform").exists():
            detected_types.add("infra")

        # Check for .tftpl files which indicate terraform templates
        if self._has_files_with_extensions(repo_path, [".tftpl"]):
            detected_types.add("infra")
            detected_types.add("template")

    def _detect_python_lib_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Python library patterns"""
        if (repo_path / "setup.py").exists() or (repo_path / "pyproject.toml").exists():
            detected_types.add("lib")

    def _detect_nodejs_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Node.js project patterns"""
        package_json = repo_path / "package.json"
        if not package_json.exists():
            return

        try:
            with open(package_json, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
                if "next" in pkg_data.get("dependencies", {}):
                    detected_types.add("site")
                elif "scripts" in pkg_data and "build" in pkg_data["scripts"]:
                    detected_types.add("app")
                else:
                    detected_types.add("lib")
        except (json.JSONDecodeError, IOError):
            detected_types.add("lib")

    def _detect_docker_app_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Docker application patterns"""
        if (repo_path / "Dockerfile").exists():
            detected_types.add("app")

    def _detect_docs_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for documentation repository patterns"""
        doc_files = ["README.md", "docs/", "documentation/"]
        if any((repo_path / f).exists() for f in doc_files):
            if not detected_types:
                detected_types.add("docs")

    def _detect_template_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for template repository patterns"""
        # Check for Jinja2 template files
        if self._has_files_with_extensions(repo_path, [".j2", ".jinja", ".jinja2"]):
            detected_types.add("template")

        # Check for common template indicators
        template_indicators = [
            "cookiecutter.json",
            ".cookiecutter.json",
            "template.yaml",
        ]
        if any((repo_path / f).exists() for f in template_indicators):
            detected_types.add("template")

    def _has_files_with_extensions(
        self, repo_path: Path, extensions: List[str]
    ) -> bool:
        """Check if repository contains files with specified extensions"""
        for file_path in repo_path.rglob("*"):
            if (
                file_path.is_file()
                and not self._is_ignored_path(file_path, repo_path)
                and any(file_path.name.endswith(ext) for ext in extensions)
            ):
                return True
        return False

    def _is_ignored_path(self, file_path: Path, repo_root: Path) -> bool:
        """Check if path should be ignored during detection"""
        ignored_patterns = {
            ".git",
            ".vscode",
            ".omd",
            "node_modules",
            ".terraform",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "venv",
            ".venv",
            "env",
            ".env",
            "dist",
            "build",
        }

        try:
            path_parts = file_path.relative_to(repo_root).parts
            return any(
                part.startswith(".")
                and part in ignored_patterns
                or part in ignored_patterns
                for part in path_parts
            )
        except ValueError:
            # Path is not relative to repo_root
            return True

    def _save_detected_metadata(
        self, repo_path: Path, metadata: Dict[str, Any]
    ) -> None:
        """Save auto-detected metadata to .omd/repository.yaml"""
        omd_dir = repo_path / ".omd"
        omd_dir.mkdir(exist_ok=True)

        metadata_file = omd_dir / REPOSITORY_METADATA_FILE

        # Remove computed fields before saving
        clean_metadata = {
            k: v for k, v in metadata.items() if k not in ["repo_name", "repo_path"]
        }

        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write("# Auto-detected repository configuration\n")
            f.write("# Edit as needed and re-run setup\n\n")
            yaml.dump(clean_metadata, f, default_flow_style=False, sort_keys=True)

    def _create_workspace_file(self, config: RepositoryConfig) -> None:
        """Create VS Code workspace file using template"""
        workspace_file = config.repo_path / f"{config.name}.code-workspace"

        try:
            # Use template to generate workspace file with additional folders
            template_name = f"{config.name}.code-workspace.j2"
            template = self.jinja_env.get_template(template_name)
            content = template.render(
                metadata=config.to_dict(),
                repo_name=config.name,
                languages=config.languages,
                platform=config.platform,
                types=config.types,
            )
            with open(workspace_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Generated {workspace_file.name}")
        except TemplateNotFound:
            # Fallback to generic template
            try:
                template = self.jinja_env.get_template("generic.code-workspace.j2")
                content = template.render(
                    metadata=config.to_dict(),
                    repo_name=config.name,
                    languages=config.languages,
                    platform=config.platform,
                    types=config.types,
                )
                with open(workspace_file, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✓ Generated {workspace_file.name}")
            except TemplateNotFound:
                # Last resort: hardcoded fallback
                workspace_data = {"folders": [{"path": "."}]}
                with open(workspace_file, "w", encoding="utf-8") as f:
                    json.dump(workspace_data, f, indent=2)
                print(f"  ✓ Generated {workspace_file.name} (fallback)")

    def _create_vscode_config(self, config: RepositoryConfig) -> None:
        """Create VS Code configuration files using templates"""
        vscode_dir = config.repo_path / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        # Settings using template
        settings_file = vscode_dir / "settings.json"
        try:
            template = self.jinja_env.get_template(".vscode/settings.json.j2")
            settings_content = template.render(
                metadata=config.to_dict(),
                repo_name=config.name,
                languages=config.languages,
                platform=config.platform,
                types=config.types,
            )
            with open(settings_file, "w", encoding="utf-8") as f:
                f.write(settings_content)

            # Check which enhanced templates were used
            enhanced_langs = self._analyze_enhanced_template_usage(config.languages)
            usage_info = self._format_enhanced_template_usage(enhanced_langs)
            print(f"  ✓ Generated .vscode/settings.json ({usage_info})")
        except TemplateNotFound:
            print("  ⚠️  Template .vscode/settings.json.j2 not found, using fallback")
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
            print("  ✓ Generated .vscode/settings.json (fallback)")
        except (yaml.YAMLError, ValueError, TypeError) as e:
            print(f"  ⚠️  Error generating settings.json from template: {e}")
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
            print("  ✓ Generated .vscode/settings.json (fallback)")

        # Extensions using template
        extensions_file = vscode_dir / "extensions.json"
        try:
            template = self.jinja_env.get_template(".vscode/extensions.json.j2")
            extensions_content = template.render(
                metadata=config.to_dict(),
                repo_name=config.name,
                languages=config.languages,
                platform=config.platform,
                types=config.types,
            )
            with open(extensions_file, "w", encoding="utf-8") as f:
                f.write(extensions_content)

            # Check which enhanced templates were used
            enhanced_langs = self._analyze_enhanced_template_usage(config.languages)
            usage_info = self._format_enhanced_template_usage(enhanced_langs)
            print(f"  ✓ Generated .vscode/extensions.json ({usage_info})")
        except TemplateNotFound:
            print("  ⚠️  Template .vscode/extensions.json.j2 not found, using fallback")
            extensions_data: Dict[str, List[str]] = {"recommendations": []}
            with open(extensions_file, "w", encoding="utf-8") as f:
                json.dump(extensions_data, f, indent=2)
            print("  ✓ Generated .vscode/extensions.json (fallback)")
        except (yaml.YAMLError, ValueError, TypeError) as e:
            print(f"  ⚠️  Error generating extensions.json from template: {e}")
            extensions_data = {"recommendations": []}
            with open(extensions_file, "w", encoding="utf-8") as f:
                json.dump(extensions_data, f, indent=2)
            print("  ✓ Generated .vscode/extensions.json (fallback)")

        # Launch configuration using template (optional)
        launch_file = vscode_dir / "launch.json"
        try:
            template = self.jinja_env.get_template(".vscode/launch.json.j2")
            launch_content = template.render(
                metadata=config.to_dict(),
                repo_name=config.name,
                languages=config.languages,
                platform=config.platform,
                types=config.types,
            )
            with open(launch_file, "w", encoding="utf-8") as f:
                f.write(launch_content)

            # Check which languages have launch configurations
            launch_langs = self._analyze_launch_language_usage(config.languages)
            usage_info = self._format_enhanced_template_usage(launch_langs)
            print(f"  ✓ Generated .vscode/launch.json ({usage_info})")
        except TemplateNotFound:
            # launch.json is optional, so we don't create a fallback
            pass
        except (yaml.YAMLError, ValueError, TypeError) as e:
            print(f"  ⚠️  Error generating launch.json from template: {e}")

        # Tasks configuration using enhanced language templates
        self._create_tasks_config(config, vscode_dir)

    def _analyze_enhanced_template_usage(self, languages: List[str]) -> List[str]:
        """Get list of languages with enhanced templates"""
        enhanced_langs = []

        for language in languages:
            enhanced_config = self._create_load_enhanced_config_func()(language)
            if enhanced_config and "languages" in enhanced_config:
                enhanced_langs.append(language)

        return enhanced_langs

    def _analyze_launch_language_usage(self, languages: List[str]) -> List[str]:
        """Get list of languages with launch configurations in enhanced templates"""
        launch_langs = []

        for language in languages:
            enhanced_config = self._create_load_enhanced_config_func()(language)
            has_launch_config = (
                enhanced_config
                and "languages" in enhanced_config
                and enhanced_config["languages"]
                .get(language, {})
                .get("launch_configurations")
            )

            if has_launch_config:
                launch_langs.append(language)

        return launch_langs

    def _get_task_contributing_languages(self, languages: List[str]) -> List[str]:
        """Get list of languages that contribute tasks"""
        task_sources = []
        for language in languages:
            enhanced_config = self._create_load_enhanced_config_func()(language)
            if enhanced_config and "languages" in enhanced_config:
                lang_config = enhanced_config["languages"].get(language, {})
                if lang_config.get("tasks"):
                    task_sources.append(language)
        return task_sources

    def _format_enhanced_template_usage(self, enhanced_langs: List[str]) -> str:
        """Format enhanced template usage information for logging"""
        if enhanced_langs:
            enhanced_str = ", ".join(enhanced_langs)
            return f"enhanced: {enhanced_str}"
        else:
            return "no enhanced templates"

    def _create_tasks_config(self, config: RepositoryConfig, vscode_dir: Path) -> None:
        """Generate tasks.json from enhanced language configurations"""
        all_tasks = []

        # Collect tasks from each language's enhanced configuration
        # Collect tasks from each language's enhanced configuration
        for language in config.languages:
            enhanced_config = self._create_load_enhanced_config_func()(language)
            if enhanced_config and "languages" in enhanced_config:
                lang_config = enhanced_config["languages"].get(language, {})
                tasks = lang_config.get("tasks", [])
                all_tasks.extend(tasks)

        # Create tasks configuration
        tasks_config = {"version": "2.0.0", "tasks": all_tasks}

        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks_config, f, indent=2)

        # Show which languages contributed tasks
        task_sources = self._get_task_contributing_languages(config.languages)
        if task_sources:
            sources_str = ", ".join(task_sources)
            print(f"  ✓ Generated .vscode/tasks.json (enhanced: {sources_str})")
        else:
            print("  ✓ Generated .vscode/tasks.json (enhanced templates)")

    def _create_omd_files(self, config: RepositoryConfig) -> None:
        """Create .omd configuration files using templates"""
        omd_dir = config.repo_path / ".omd"
        omd_dir.mkdir(exist_ok=True)

        # Generate languages.yaml from template for validation compatibility
        try:
            template = self.jinja_env.get_template(".omd/languages.yaml.j2")
            content = template.render(
                metadata=config.to_dict(),
                repo_name=config.name,
                languages=config.languages,
                platform=config.platform,
                types=config.types,
            )
            languages_file = omd_dir / "languages.yaml"
            with open(languages_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("  ✓ Generated .omd/languages.yaml (validation compatibility)")
        except TemplateNotFound:
            print("  ⚠️  Template .omd/languages.yaml.j2 not found")
        except (yaml.YAMLError, ValueError, TypeError) as e:
            print(f"  ⚠️  Error generating languages.yaml: {e}")

        # Generate workspace.yaml from template ONLY if it doesn't exist
        workspace_file = omd_dir / "workspace.yaml"
        if not workspace_file.exists():
            try:
                template = self.jinja_env.get_template(".omd/workspace.yaml.j2")
                content = template.render(
                    languages=config.languages,
                    types=config.types,
                    repo_name=config.name,
                    platform=config.platform,
                    metadata=config.to_dict(),
                )
                with open(workspace_file, "w", encoding="utf-8") as f:
                    f.write(content)
                print("  ✓ Generated .omd/workspace.yaml (workspace configuration)")
            except TemplateNotFound:
                print("  ⚠️  Template .omd/workspace.yaml.j2 not found")
            except (yaml.YAMLError, ValueError, TypeError) as e:
                print(f"  ⚠️  Error generating workspace.yaml: {e}")
        else:
            print("  ✓ Preserved existing .omd/workspace.yaml (user configuration)")

        # Generate platform.yaml from template for platform configuration
        try:
            template = self.jinja_env.get_template(".omd/platform.yaml.j2")
            content = template.render(
                platform=config.platform,
                languages=config.languages,
                types=config.types,
                metadata=config.to_dict(),
                repo_name=config.name,
            )
            platform_file = omd_dir / "platform.yaml"
            with open(platform_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("  ✓ Generated .omd/platform.yaml (platform configuration)")
        except TemplateNotFound:
            print("  ⚠️  Template .omd/platform.yaml.j2 not found")
        except (yaml.YAMLError, ValueError, TypeError) as e:
            print(f"  ⚠️  Error generating platform.yaml: {e}")

    def _update_gitignore(self, config: RepositoryConfig) -> None:
        """Update .gitignore file"""
        gitignore_file = config.repo_path / ".gitignore"

        if not gitignore_file.exists():
            # Generate comprehensive .gitignore from template
            try:
                template = self.jinja_env.get_template(".gitignore.j2")
                content = template.render(
                    languages=config.languages,
                    platform=config.platform,
                    types=config.types,
                    metadata=config.to_dict(),
                    repo_name=config.name,
                )

                with open(gitignore_file, "w", encoding="utf-8") as f:
                    f.write(content)

                print("  ✓ Generated .gitignore")
            except (yaml.YAMLError, ValueError, TypeError, IOError, OSError) as e:
                print(f"  ⚠ Failed to generate .gitignore from template: {e}")
                # Fallback to simple version
                with open(gitignore_file, "w", encoding="utf-8") as f:
                    f.write("*.code-workspace\n")
                print("  ✓ Created simple .gitignore")
        else:
            # Read existing .gitignore and add workspace pattern if missing
            try:
                with open(gitignore_file, "r", encoding="utf-8") as f:
                    content = f.read()

                workspace_pattern = "*.code-workspace"
                if workspace_pattern not in content:
                    # Add workspace pattern at the end
                    if not content.endswith("\n"):
                        content += "\n"
                    content += workspace_pattern + "\n"

                    with open(gitignore_file, "w", encoding="utf-8") as f:
                        f.write(content)

                    print("  ✓ Updated .gitignore")
            except (IOError, OSError) as e:
                print(f"  ⚠️  Error updating .gitignore: {e}")

    def generate_copilot_instructions(self) -> None:
        """Generate GitHub Copilot instruction files if enabled"""
        # Copilot instructions generation disabled for now

    def _create_metadata_template(self, repo_path: Path) -> None:
        """Create a template metadata file"""
        omd_dir = repo_path / ".omd"
        omd_dir.mkdir(exist_ok=True)

        template_file = omd_dir / REPOSITORY_METADATA_FILE
        template_content = """# Please fill out this configuration file

# Languages used in this repository (required)
languages:
  - # terraform, python, javascript, go, etc.

# CI/CD platform where this repository resides (required)
platform: # github, azuredevops, gitlab

# Repository types (required)
types:
  - lib  # app, lib, infra, site, template, tool, config, docs, monorepo, example

# Additional tags for categorization (optional)
tags: []
  - # aws, azure, gcp
"""

        with open(template_file, "w", encoding="utf-8") as f:
            f.write(template_content)

        print(f"📝 Created template metadata file: {template_file}")
        print("   Please edit this file and run the setup again.")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: setup-workspace.py <repository_path>")
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    # Determine tools directory
    script_dir = Path(__file__).parent.resolve()
    tools_dir = script_dir.parent.parent

    generator = WorkspaceGenerator(tools_dir)
    generator.setup_repository(repo_path)


if __name__ == "__main__":
    main()

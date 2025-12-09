#!/usr/bin/env python3
"""
Repository content detection module
Handles auto-detection of languages, platforms, and repository types
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set


class RepositoryDetector:
    """Handles auto-detection of repository characteristics"""

    def detect_languages(self, repo_path: Path) -> List[str]:
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

    def detect_platform(self, repo_path: Path) -> str:
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

    def detect_repository_types(self, repo_path: Path) -> List[str]:
        """Auto-detect repository types based on content"""
        detected_types: Set[str] = set()

        self._detect_infra_type(repo_path, detected_types)
        self._detect_python_lib_type(repo_path, detected_types)
        self._detect_nodejs_type(repo_path, detected_types)
        self._detect_docker_app_type(repo_path, detected_types)
        self._detect_docs_type(repo_path, detected_types)
        self._detect_template_type(repo_path, detected_types)

        return sorted(detected_types) if detected_types else ["lib"]

    def _detect_infra_type(self, repo_path: Path, detected_types: Set[str]) -> None:
        """Check for infrastructure repository patterns"""
        if (repo_path / "main.tf").exists() or (repo_path / "terraform").exists():
            detected_types.add("infra")

        # Check for .tftpl files which indicate terraform templates
        if self._has_files_with_extensions(repo_path, [".tftpl"]):
            detected_types.add("infra")
            detected_types.add("template")

    def _detect_python_lib_type(
        self, repo_path: Path, detected_types: Set[str]
    ) -> None:
        """Check for Python library patterns"""
        if (repo_path / "setup.py").exists() or (repo_path / "pyproject.toml").exists():
            detected_types.add("lib")

    def _detect_nodejs_type(self, repo_path: Path, detected_types: Set[str]) -> None:
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

    def _detect_docker_app_type(
        self, repo_path: Path, detected_types: Set[str]
    ) -> None:
        """Check for Docker application patterns"""
        if (repo_path / "Dockerfile").exists():
            detected_types.add("app")

    def _detect_docs_type(self, repo_path: Path, detected_types: Set[str]) -> None:
        """Check for documentation repository patterns"""
        doc_files = ["README.md", "docs/", "documentation/"]
        if any((repo_path / f).exists() for f in doc_files):
            if not detected_types:
                detected_types.add("docs")

    def _detect_template_type(self, repo_path: Path, detected_types: Set[str]) -> None:
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

#!/usr/bin/env python3
"""
Cross-platform myrepos tooling system
Supports Windows, macOS, and Linux with explicit metadata configuration
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

# Constants
REPOSITORY_METADATA_FILE = 'repository.yaml'


class RepositoryConfig:
    """Handles repository metadata and configuration"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.repo_name = self.repo_path.name
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load repository metadata from .omd/repository.yaml"""
        metadata_file = self.repo_path / '.omd' / REPOSITORY_METADATA_FILE
        
        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Missing required metadata file: {metadata_file}\n"
                f"Please create .omd/{REPOSITORY_METADATA_FILE} with repository configuration."
            )
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {metadata_file}: {e}")
        
        # Validate required fields
        required_fields = ['languages', 'platform', 'types']
        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing required field '{field}' in {metadata_file}")
        
        # Ensure languages is a list
        if isinstance(metadata.get('languages'), str):
            metadata['languages'] = [metadata['languages']]
        
        # No cloud_providers field in simplified schema
            
        # Add computed metadata
        metadata['repo_name'] = self.repo_name
        metadata['repo_path'] = str(self.repo_path)
        
        # Infer client from path: /Data/GIT/{CLIENT}/...
        metadata['client'] = self._infer_client_from_path()
        
        return metadata
    
    def _infer_client_from_path(self) -> str:
        """Infer client from repository path"""
        path_parts = self.repo_path.parts
        try:
            git_index = path_parts.index('GIT')
            if git_index + 1 < len(path_parts):
                return path_parts[git_index + 1]
        except ValueError:
            pass
        return 'unknown'
    
    def get_extensions(self) -> List[str]:
        """Get VS Code extensions for this repository (MINIMAL FALLBACK ONLY)"""
        # Minimal fallback - templates should be used instead
        return ['ms-vscode.vscode-json']
    
    def get_settings(self) -> Dict[str, Any]:
        """Get VS Code settings for this repository (MINIMAL FALLBACK ONLY)"""
        # Minimal fallback - templates should be used instead
        return {
            "files.exclude": {
                "**/.git": True,
                "**/.DS_Store": True
            }
        }


class WorkspaceGenerator:
    """Generates VS Code workspace and configuration files"""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = self.tools_dir / 'templates'
        
        # Setup Jinja2 environment with custom functions
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add load_yaml function to templates
        def load_yaml_func(path):
            config_file = self.templates_dir / path
            if not config_file.exists():
                print(f"  ⚠️  Template config file not found: {path}")
                return {}
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"  ⚠️  Error loading template config {path}: {e}")
                return {}
        
        self.jinja_env.globals['load_yaml'] = load_yaml_func
    
    def setup_repository(self, repo_path: Path) -> None:
        """Setup VS Code workspace and configuration for a repository"""
        try:
            config = RepositoryConfig(repo_path)
            print(f"🔍 Processing repository: {config.repo_name}")
            print("📊 Detected content:")
            print(f"        platform: {config.metadata['platform']}")
            print(f"        languages: {','.join(config.metadata['languages'])}")
            print(f"        types: {','.join(config.metadata['types'])}")
            
            self._create_workspace_file(config)
            self._create_vscode_config(config)
            self._update_gitignore(config)
            self.generate_copilot_instructions(config)
            
            print(f"✅ Setup completed for {config.repo_name}")
            
        except FileNotFoundError:
            print("🔍 No metadata found, auto-detecting repository configuration...")
            self._auto_detect_and_setup(repo_path)
            
        except (ValueError, yaml.YAMLError) as e:
            print(f"❌ Metadata error: {e}")
    
    def _auto_detect_and_setup(self, repo_path: Path) -> None:
        """Auto-detect repository configuration and set up workspace"""
        repo_path = Path(repo_path)
        
        # Auto-detect configuration
        detected_config = {
            'repo_name': repo_path.name,
            'repo_path': str(repo_path),
            'languages': self._detect_languages(repo_path),
            'platform': self._detect_platform(repo_path),
            'types': self._detect_repository_types(repo_path),
            'copilot_instructions': False,  # Default to disabled for auto-detected repos
            'client': self._infer_client_from_path(repo_path)
        }
        
        print("📊 Auto-detected content:")
        print(f"        platform: {detected_config['platform']}")
        print(f"        languages: {','.join(detected_config['languages'])}")
        print(f"        types: {','.join(detected_config['types'])}")
        
        # Save detected configuration first
        self._save_detected_metadata(repo_path, detected_config)
        
        # Now create proper config object using the saved metadata
        config = RepositoryConfig(repo_path)
        
        # Generate workspace files
        self._create_workspace_file(config)
        self._create_vscode_config(config)
        self._update_gitignore(config)
        
        print(f"✅ Auto-setup completed for {config.repo_name}")
        print("💡 Configuration saved to .omd/repository.yaml - edit as needed")
    
    def _detect_languages(self, repo_path: Path) -> List[str]:
        """Auto-detect languages from file extensions"""
        language_patterns = {
            'terraform': ['.tf', '.tfvars', '.hcl'],
            'python': ['.py', '.pyx', '.pyi'],
            'go': ['.go', 'go.mod', 'go.sum'],
            'markdown': ['.md', '.markdown', '.mdx'],
            'yaml': ['.yml', '.yaml'],
            'json': ['.json', '.jsonc'],
            'shell': ['.sh', '.bash', '.zsh'],
            'powershell': ['.ps1', '.psm1', '.psd1'],
            'sql': ['.sql']
        }
        
        detected_languages = set()
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored_path(file_path, repo_path):
                language = self._detect_language_for_file(file_path, language_patterns)
                if language:
                    detected_languages.add(language)
        
        return sorted(detected_languages) if detected_languages else ['markdown']
    
    def _detect_language_for_file(self, file_path: Path, language_patterns: Dict[str, List[str]]) -> Optional[str]:
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
            'github': ['.github/', '.github/workflows/'],
            'azuredevops': ['azure-pipelines.yml', '.azure/', 'azure-pipelines.yaml']
        }
        
        for platform, indicators in platform_indicators.items():
            for indicator in indicators:
                check_path = repo_path / indicator
                if check_path.exists():
                    return platform
        
        return 'github'  # Default fallback
    
    def _detect_repository_types(self, repo_path: Path) -> List[str]:
        """Auto-detect repository types based on content"""
        detected_types = set()
        
        self._detect_infra_type(repo_path, detected_types)
        self._detect_python_lib_type(repo_path, detected_types)
        self._detect_nodejs_type(repo_path, detected_types)
        self._detect_docker_app_type(repo_path, detected_types)
        self._detect_docs_type(repo_path, detected_types)
        
        return sorted(detected_types) if detected_types else ['lib']
    
    def _detect_infra_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for infrastructure repository patterns"""
        if (repo_path / 'main.tf').exists() or (repo_path / 'terraform').exists():
            detected_types.add('infra')
    
    def _detect_python_lib_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Python library patterns"""
        if (repo_path / 'setup.py').exists() or (repo_path / 'pyproject.toml').exists():
            detected_types.add('lib')
    
    def _detect_nodejs_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Node.js project patterns"""
        package_json = repo_path / 'package.json'
        if not package_json.exists():
            return
        
        try:
            with open(package_json, 'r') as f:
                pkg_data = json.load(f)
                if 'next' in pkg_data.get('dependencies', {}):
                    detected_types.add('site')
                elif 'scripts' in pkg_data and 'build' in pkg_data['scripts']:
                    detected_types.add('app')
                else:
                    detected_types.add('lib')
        except (json.JSONDecodeError, IOError):
            detected_types.add('lib')
    
    def _detect_docker_app_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for Docker application patterns"""
        if (repo_path / 'Dockerfile').exists():
            detected_types.add('app')
    
    def _detect_docs_type(self, repo_path: Path, detected_types: set) -> None:
        """Check for documentation repository patterns"""
        doc_files = ['README.md', 'docs/', 'documentation/']
        if any((repo_path / f).exists() for f in doc_files):
            if not detected_types:
                detected_types.add('docs')
    
    def _is_ignored_path(self, file_path: Path, repo_root: Path) -> bool:
        """Check if path should be ignored during detection"""
        ignored_patterns = {
            '.git', '.vscode', '.omd', 'node_modules', '.terraform',
            '__pycache__', '.pytest_cache', '.mypy_cache',
            'venv', '.venv', 'env', '.env', 'dist', 'build'
        }
        
        try:
            path_parts = file_path.relative_to(repo_root).parts
            return any(part.startswith('.') and part in ignored_patterns or part in ignored_patterns 
                      for part in path_parts)
        except ValueError:
            # Path is not relative to repo_root
            return True
    
    def _infer_client_from_path(self, repo_path: Path) -> str:
        """Infer client from repository path"""
        path_parts = repo_path.parts
        try:
            git_index = path_parts.index('GIT')
            if git_index + 1 < len(path_parts):
                return path_parts[git_index + 1]
        except ValueError:
            pass
        return 'unknown'
    
    def _save_detected_metadata(self, repo_path: Path, metadata: Dict[str, Any]) -> None:
        """Save auto-detected metadata to .omd/repository.yaml"""
        omd_dir = repo_path / '.omd'
        omd_dir.mkdir(exist_ok=True)
        
        metadata_file = omd_dir / REPOSITORY_METADATA_FILE
        
        # Remove computed fields before saving
        clean_metadata = {k: v for k, v in metadata.items() 
                         if k not in ['repo_name', 'repo_path', 'client']}
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write("# Auto-detected repository configuration\n")
            f.write("# Edit as needed and re-run setup\n\n")
            yaml.dump(clean_metadata, f, default_flow_style=False, sort_keys=True)
    
    def _create_workspace_file(self, config: RepositoryConfig) -> None:
        """Create VS Code workspace file"""
        workspace_data = {
            "folders": [{"path": "."}]
        }
        
        workspace_file = config.repo_path / f"{config.repo_name}.code-workspace"
        with open(workspace_file, 'w', encoding='utf-8') as f:
            json.dump(workspace_data, f, indent=2)
        
        print(f"  ✓ Generated {workspace_file.name}")
    
    def _create_vscode_config(self, config: RepositoryConfig) -> None:
        """Create VS Code configuration files using templates"""
        vscode_dir = config.repo_path / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        # Settings using template
        settings_file = vscode_dir / 'settings.json'
        try:
            template = self.jinja_env.get_template('.vscode/settings.json.j2')
            settings_content = template.render(metadata=config.metadata)
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(settings_content)
            print("  ✓ Generated .vscode/settings.json (from template)")
        except TemplateNotFound:
            print("  ⚠️  Template .vscode/settings.json.j2 not found, using fallback")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(config.get_settings(), f, indent=2)
            print("  ✓ Generated .vscode/settings.json (fallback)")
        except Exception as e:
            print(f"  ⚠️  Error generating settings.json from template: {e}")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(config.get_settings(), f, indent=2)
            print("  ✓ Generated .vscode/settings.json (fallback)")
        
        # Extensions using template
        extensions_file = vscode_dir / 'extensions.json'
        try:
            template = self.jinja_env.get_template('.vscode/extensions.json.j2')
            extensions_content = template.render(metadata=config.metadata)
            with open(extensions_file, 'w', encoding='utf-8') as f:
                f.write(extensions_content)
            print("  ✓ Generated .vscode/extensions.json (from template)")
        except TemplateNotFound:
            print("  ⚠️  Template .vscode/extensions.json.j2 not found, using fallback")
            extensions_data = {"recommendations": config.get_extensions()}
            with open(extensions_file, 'w', encoding='utf-8') as f:
                json.dump(extensions_data, f, indent=2)
            print("  ✓ Generated .vscode/extensions.json (fallback)")
        except Exception as e:
            print(f"  ⚠️  Error generating extensions.json from template: {e}")
            extensions_data = {"recommendations": config.get_extensions()}
            with open(extensions_file, 'w', encoding='utf-8') as f:
                json.dump(extensions_data, f, indent=2)
            print("  ✓ Generated .vscode/extensions.json (fallback)")
    
    def _update_gitignore(self, config: RepositoryConfig) -> None:
        """Update .gitignore file"""
        gitignore_file = config.repo_path / '.gitignore'
        
        # Read existing .gitignore
        if gitignore_file.exists():
            with open(gitignore_file, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        else:
            lines = []
        
        # Add workspace files to gitignore if not present
        workspace_pattern = '*.code-workspace'
        if workspace_pattern not in lines:
            lines.append(workspace_pattern)
            
            with open(gitignore_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')
            
            print("  ✓ Updated .gitignore")
    
    def generate_copilot_instructions(self, config: RepositoryConfig) -> None:
        """Generate GitHub Copilot instruction files if enabled"""
        # Check if copilot instructions are enabled
        if not config.metadata.get('copilot_instructions', False):
            return
        
        print("🤖 Generating GitHub Copilot instructions...")
        
        # Generate main copilot instructions
        self._generate_main_copilot_instructions(config)
        
        # Generate language-specific instructions
        self._generate_language_copilot_instructions(config)
        
        print("  ✅ Generated Copilot instructions")
    
    def _generate_main_copilot_instructions(self, config: RepositoryConfig) -> None:
        """Generate main .github/copilot-instructions.md file"""
        try:
            template = self.jinja_env.get_template('.github/copilot-instructions.md.j2')
            content = template.render(**config.metadata)
            
            output_file = config.repo_path / '.github' / 'copilot-instructions.md'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except TemplateNotFound:
            print("  ⚠️  Template .github/copilot-instructions.md.j2 not found")
        except Exception as e:
            print(f"  ⚠️  Could not generate main copilot instructions: {e}")
    
    def _generate_language_copilot_instructions(self, config: RepositoryConfig) -> None:
        """Generate language-specific instruction files using templates"""
        instructions_dir = config.repo_path / '.github' / 'instructions'
        instructions_dir.mkdir(parents=True, exist_ok=True)
        
        for language in config.metadata.get('languages', []):
            template_path = f'.github/instructions/{language}.instructions.md.j2'
            
            try:
                template = self.jinja_env.get_template(template_path)
                content = template.render(**config.metadata)
                
                output_file = instructions_dir / f'{language}.instructions.md'
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
            except TemplateNotFound:
                print(f"  ⚠️  Template {template_path} not found")
    def _create_metadata_template(self, repo_path: Path) -> None:
        """Create a template metadata file"""
        omd_dir = repo_path / '.omd'
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
        
        with open(template_file, 'w', encoding='utf-8') as f:
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


if __name__ == '__main__':
    main()
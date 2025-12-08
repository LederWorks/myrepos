#!/usr/bin/env python3
"""
Cross-platform myrepos tooling system
Supports Windows, macOS, and Linux with explicit metadata configuration
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Template, Environment, FileSystemLoader


class RepositoryConfig:
    """Handles repository metadata and configuration"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.repo_name = self.repo_path.name
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Any]:
        """Load repository metadata from .omd/repository.yaml"""
        metadata_file = self.repo_path / '.omd' / 'repository.yaml'
        
        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Missing required metadata file: {metadata_file}\n"
                f"Please create .omd/repository.yaml with repository configuration."
            )
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {metadata_file}: {e}")
        
        # Validate required fields
        required_fields = ['languages', 'platform', 'type']
        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing required field '{field}' in {metadata_file}")
        
        # Ensure languages is a list
        if isinstance(metadata.get('languages'), str):
            metadata['languages'] = [metadata['languages']]
        
        # Ensure cloud_providers is a list  
        if 'cloud_providers' in metadata:
            if isinstance(metadata['cloud_providers'], str):
                metadata['cloud_providers'] = [metadata['cloud_providers']]
        else:
            metadata['cloud_providers'] = []
            
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
        """Get VS Code extensions for this repository"""
        extensions = set()
        
        # Language-specific extensions
        for language in self.metadata['languages']:
            extensions.update(self._get_language_extensions(language))
        
        # Cloud provider extensions
        for provider in self.metadata.get('cloud_providers', []):
            extensions.update(self._get_cloud_extensions(provider))
        
        # Platform-specific extensions
        extensions.update(self._get_platform_extensions(self.metadata['platform']))
        
        # Client-specific extensions
        extensions.update(self._get_client_extensions(self.metadata['client']))
        
        return sorted(list(extensions))
    
    def _get_language_extensions(self, language: str) -> List[str]:
        """Get extensions for a specific language"""
        language_extensions = {
            'terraform': [
                'hashicorp.terraform',
                'ms-vscode.terraform'
            ],
            'python': [
                'ms-python.python',
                'ms-python.pylint',
                'ms-python.black-formatter',
                'ms-python.isort'
            ],
            'javascript': [
                'ms-vscode.vscode-typescript-next',
                'esbenp.prettier-vscode',
                'dbaeumer.vscode-eslint'
            ],
            'typescript': [
                'ms-vscode.vscode-typescript-next',
                'esbenp.prettier-vscode',
                'dbaeumer.vscode-eslint'
            ],
            'go': [
                'golang.go'
            ],
            'rust': [
                'rust-lang.rust-analyzer'
            ],
            'java': [
                'redhat.java',
                'vscjava.vscode-java-pack'
            ],
            'csharp': [
                'ms-dotnettools.csharp'
            ],
            'markdown': [
                'yzhang.markdown-all-in-one',
                'DavidAnson.vscode-markdownlint',
                'bierner.markdown-mermaid',
                'bierner.markdown-preview-github-styles'
            ],
            'yaml': [
                'redhat.vscode-yaml'
            ],
            'json': [
                'ms-vscode.json'
            ],
            'dockerfile': [
                'ms-azuretools.vscode-docker'
            ],
            'shell': [
                'timonwong.shellcheck',
                'foxundermoon.shell-format'
            ],
            'powershell': [
                'ms-vscode.powershell'
            ]
        }
        return language_extensions.get(language, [])
    
    def _get_cloud_extensions(self, provider: str) -> List[str]:
        """Get extensions for cloud providers"""
        cloud_extensions = {
            'aws': [
                'amazonwebservices.aws-toolkit-vscode'
            ],
            'azure': [
                'ms-vscode.azure-account',
                'ms-azuretools.vscode-azureresourcegroups'
            ],
            'gcp': [
                'googlecloudtools.cloudcode'
            ]
        }
        return cloud_extensions.get(provider, [])
    
    def _get_platform_extensions(self, platform: str) -> List[str]:
        """Get extensions for CI/CD platforms"""
        platform_extensions = {
            'github': [
                'github.vscode-pull-request-github',
                'github.copilot',
                'github.copilot-chat'
            ],
            'azuredevops': [
                'ms-vsts.team'
            ],
            'gitlab': [
                'gitlab.gitlab-workflow'
            ]
        }
        return platform_extensions.get(platform, [])
    
    def _get_client_extensions(self, client: str) -> List[str]:
        """Get client-specific extensions"""
        client_extensions = {
            'crayon': [
                'ms-vscode.vscode-json'
            ]
        }
        return client_extensions.get(client, [])
    
    def get_settings(self) -> Dict[str, Any]:
        """Get VS Code settings for this repository"""
        settings = {
            "files.exclude": {
                "**/.git": True,
                "**/.DS_Store": True,
                "**/.omd": True
            },
            "files.watcherExclude": {
                "**/.git/objects/**": True,
                "**/.git/subtree-cache/**": True,
                "**/node_modules/*/**": True
            }
        }
        
        # Merge language-specific settings
        for language in self.metadata['languages']:
            lang_settings = self._get_language_settings(language)
            settings.update(lang_settings)
        
        # Merge cloud provider settings
        for provider in self.metadata.get('cloud_providers', []):
            cloud_settings = self._get_cloud_settings(provider)
            settings.update(cloud_settings)
            
        return settings
    
    def _get_language_settings(self, language: str) -> Dict[str, Any]:
        """Get settings for a specific language"""
        language_settings = {
            'terraform': {
                "terraform.experimentalFeatures.validateOnSave": True,
                "terraform.experimentalFeatures.prefillRequiredFields": True,
                "files.associations": {
                    "*.tf": "terraform",
                    "*.tfvars": "terraform",
                    "*.hcl": "terraform"
                },
                "[terraform]": {
                    "editor.defaultFormatter": "hashicorp.terraform",
                    "editor.formatOnSave": True
                }
            },
            'python': {
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "[python]": {
                    "editor.formatOnSave": True,
                    "editor.defaultFormatter": "ms-python.black-formatter",
                    "editor.codeActionsOnSave": {
                        "source.organizeImports": True
                    }
                }
            },
            'javascript': {
                "typescript.preferences.includePackageJsonAutoImports": "auto",
                "javascript.preferences.includePackageJsonAutoImports": "auto",
                "[javascript]": {
                    "editor.defaultFormatter": "esbenp.prettier-vscode",
                    "editor.formatOnSave": True
                },
                "editor.codeActionsOnSave": {
                    "source.fixAll.eslint": True
                }
            },
            'markdown': {
                "files.associations": {
                    "*.md": "markdown",
                    "*.mdx": "markdown",
                    "*.markdown": "markdown"
                },
                "[markdown]": {
                    "editor.wordWrap": "on",
                    "editor.wordWrapColumn": 100,
                    "editor.quickSuggestions": {
                        "comments": "off",
                        "strings": "off", 
                        "other": "off"
                    },
                    "editor.formatOnSave": True,
                    "editor.formatOnPaste": True,
                    "editor.tabSize": 2,
                    "editor.insertSpaces": True,
                    "editor.defaultFormatter": "yzhang.markdown-all-in-one"
                },
                "markdown.preview.breaks": True,
                "markdown.preview.linkify": True,
                "markdown.preview.typographer": True,
                "markdown.extension.toc.updateOnSave": True,
                "markdown.extension.toc.orderedList": False,
                "markdown.extension.list.indentationSize": "adaptive",
                "markdownlint.config": {
                    "MD013": False,  # Line length
                    "MD033": False,  # Allow inline HTML
                    "MD041": False   # First line in file should be a top level header
                }
            },
            'yaml': {
                "files.associations": {
                    "*.yml": "yaml",
                    "*.yaml": "yaml"
                },
                "[yaml]": {
                    "editor.formatOnSave": True,
                    "editor.tabSize": 2,
                    "editor.insertSpaces": True
                },
                "yaml.format.enable": True,
                "yaml.validate": True,
                "yaml.hover": True,
                "yaml.completion": True
            },
            'json': {
                "[json]": {
                    "editor.formatOnSave": True,
                    "editor.tabSize": 2,
                    "editor.insertSpaces": True
                },
                "[jsonc]": {
                    "editor.formatOnSave": True,
                    "editor.tabSize": 2,
                    "editor.insertSpaces": True
                }
            },
            'dockerfile': {
                "files.associations": {
                    "Dockerfile*": "dockerfile",
                    "*.dockerfile": "dockerfile"
                },
                "[dockerfile]": {
                    "editor.formatOnSave": True
                }
            },
            'shell': {
                "files.associations": {
                    "*.sh": "shellscript",
                    "*.bash": "shellscript",
                    "*.zsh": "shellscript"
                },
                "[shellscript]": {
                    "editor.formatOnSave": True,
                    "editor.tabSize": 4,
                    "editor.insertSpaces": True
                },
                "shellcheck.enable": True,
                "shellformat.effectLanguages": ["shellscript", "dockerfile"]
            }
        }
        return language_settings.get(language, {})
    
    def _get_cloud_settings(self, provider: str) -> Dict[str, Any]:
        """Get settings for cloud providers"""
        cloud_settings = {
            'aws': {
                "aws.telemetry": False,
                "aws.suppressPrompts": {
                    "regionAddAutomatically": True
                }
            },
            'azure': {
                "azure.resourceGroups.groupBy": "resourceType",
                "azureTerraform.terminal": "integrated"
            },
            'gcp': {
                "cloudcode.gke.trust": True,
                "cloudcode.duetAI.inline.enable": False
            }
        }
        return cloud_settings.get(provider, {})


class WorkspaceGenerator:
    """Generates VS Code workspace and configuration files"""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = self.tools_dir / 'templates'
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def setup_repository(self, repo_path: Path) -> None:
        """Setup VS Code workspace and configuration for a repository"""
        try:
            config = RepositoryConfig(repo_path)
            print(f"🔍 Processing repository: {config.repo_name}")
            print(f"📊 Metadata: {config.metadata}")
            
            self._create_workspace_file(config)
            self._create_vscode_config(config)
            self._update_gitignore(config)
            
            print(f"✅ Setup completed for {config.repo_name}")
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            self._create_metadata_template(repo_path)
            
        except (ValueError, yaml.YAMLError) as e:
            print(f"❌ Metadata error: {e}")
    
    def _create_workspace_file(self, config: RepositoryConfig) -> None:
        """Create VS Code workspace file"""
        workspace_data = {
            "folders": [{"path": "."}],
            "extensions": {
                "recommendations": config.get_extensions()
            }
        }
        
        workspace_file = config.repo_path / f"{config.repo_name}.code-workspace"
        with open(workspace_file, 'w', encoding='utf-8') as f:
            json.dump(workspace_data, f, indent=2)
        
        print(f"  ✓ Generated {workspace_file.name}")
    
    def _create_vscode_config(self, config: RepositoryConfig) -> None:
        """Create VS Code configuration files"""
        vscode_dir = config.repo_path / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        # Settings
        settings_file = vscode_dir / 'settings.json'
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(config.get_settings(), f, indent=2)
        print(f"  ✓ Generated .vscode/settings.json")
        
        # Extensions
        extensions_file = vscode_dir / 'extensions.json'
        extensions_data = {"recommendations": config.get_extensions()}
        with open(extensions_file, 'w', encoding='utf-8') as f:
            json.dump(extensions_data, f, indent=2)
        print(f"  ✓ Generated .vscode/extensions.json")
    
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
            
            print(f"  ✓ Updated .gitignore")
    
    def _create_metadata_template(self, repo_path: Path) -> None:
        """Create a template metadata file"""
        omd_dir = repo_path / '.omd'
        omd_dir.mkdir(exist_ok=True)
        
        template_file = omd_dir / 'repository.yaml'
        
        # Try to detect some basic info
        repo_name = repo_path.name
        
        # Basic template
        template_content = """# Repository metadata configuration
# Please fill out this configuration file

# Languages used in this repository (required)
languages:
  - # terraform, python, javascript, go, etc.

# CI/CD platform where this repository resides (required)
platform: # github, azuredevops, gitlab

# Repository type/category (required)  
type: # terraform-module, application, library, template

# Cloud providers this repository targets (optional)
cloud_providers:
  - # aws, azure, gcp
"""
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"📝 Created template metadata file: {template_file}")
        print(f"   Please edit this file and run the setup again.")


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
    script_dir = Path(__file__).parent
    tools_dir = script_dir.parent
    
    generator = WorkspaceGenerator(tools_dir)
    generator.setup_repository(repo_path)


if __name__ == '__main__':
    main()
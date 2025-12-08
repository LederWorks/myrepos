# Template System Architecture

This document describes the Jinja2-based template system that generates VS Code workspace configurations from language and platform templates.

## Template System Overview

The myrepos system uses a template-driven architecture where all VS Code configurations are generated from Jinja2 templates combined with YAML configuration data. This replaces hardcoded Python dictionaries with flexible, maintainable templates.

## Architecture Components

### Template Directory Structure

```
templates/
├── languages/           # Language-specific configurations
│   ├── python.yaml.j2   # Python: debugging, testing, linting
│   ├── go.yaml.j2       # Go: build tools, testing
│   ├── terraform.yaml.j2# Terraform: validation, security
│   └── ...              # Additional languages
├── README.md.j2         # Repository documentation template
└── {{ repo_name }}.code-workspace.j2  # VS Code workspace file
```

### Template Processing Engine

The `WorkspaceGenerator` class provides the core template processing:

```python
class WorkspaceGenerator:
    def __init__(self, tools_dir: Path):
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add template functions
        self.jinja_env.globals['load_yaml'] = self._load_yaml_func
        self.jinja_env.globals['load_enhanced_language_config'] = self._load_language_config
```

## Template Processing Flow

### 1. Repository Analysis
- Load `.omd/repository.yaml` metadata
- Extract languages, platform, and repository types
- Prepare template context with repository information

### 2. Language Template Loading
- For each language in metadata, load `templates/languages/{lang}.yaml.j2`
- Parse template to extract settings, extensions, tasks, launch configs
- Merge configurations from multiple languages

### 3. VS Code File Generation
- Generate `.vscode/settings.json` with merged language settings
- Create `.vscode/extensions.json` with required/recommended extensions  
- Build `.vscode/tasks.json` with language-specific tasks
- Generate `.vscode/launch.json` with debug configurations

### 4. Additional File Creation
- Create repository README.md from template
- Generate VS Code workspace file with proper folder configuration
- Create GitHub Copilot instruction files

## Language Template Format

Each language template follows this structure:

```yaml
# templates/languages/python.yaml.j2
languages:
  python:
    # File type associations
    file_associations:
      "*.py": "python"
      "*.pyi": "python"
    
    # VS Code editor settings
    settings:
      "[python]":
        editor.formatOnSave: true
        editor.defaultFormatter: "ms-python.black-formatter"
      python.defaultInterpreterPath: "./venv/bin/python"
      python.testing.pytestEnabled: true
    
    # Required extensions (must install)
    required_extensions:
      - "ms-python.python"
      - "ms-python.black-formatter"
    
    # Recommended extensions (suggested)
    recommended_extensions:
      - "ms-python.pylint" 
      - "ms-python.mypy-type-checker"
    
    # Build/test tasks
    tasks:
      - label: "Python: Run Tests"
        type: "shell"
        command: "python"
        args: ["-m", "pytest"]
        group: "test"
      
      - label: "Python: Format Code"
        type: "shell"
        command: "python"  
        args: ["-m", "black", "."]
        group: "build"
    
    # Debug configurations
    launch_configurations:
      - name: "Python: Current File"
        type: "debugpy"
        request: "launch"
        program: "${file}"
        console: "integratedTerminal"
        python: "./venv/bin/python"
```

## Template Generation Process

### Settings Merging Algorithm

```python
def _merge_settings(self, languages: List[str], metadata: dict) -> dict:
    """Merge settings from multiple language templates"""
    merged_settings = {}
    
    for language in languages:
        config = self._load_enhanced_language_config(language, metadata)
        if config and 'languages' in config:
            lang_config = config['languages'].get(language, {})
            settings = lang_config.get('settings', {})
            
            # Deep merge settings
            merged_settings.update(settings)
    
    return merged_settings
```

### Extension Collection

```python
def _collect_extensions(self, languages: List[str], platform: str) -> dict:
    """Collect required and recommended extensions"""
    required = set()
    recommended = set()
    
    # Add language extensions
    for language in languages:
        config = self._load_enhanced_language_config(language, metadata)
        if config and 'languages' in config:
            lang_config = config['languages'].get(language, {})
            required.update(lang_config.get('required_extensions', []))
            recommended.update(lang_config.get('recommended_extensions', []))
    
    # Add platform extensions  
    if platform == 'github':
        required.update(['github.vscode-pull-request-github'])
        recommended.update(['github.copilot'])
    elif platform == 'azuredevops':
        required.update(['ms-vsts.team'])
    
    return {
        'required': sorted(list(required)),
        'recommended': sorted(list(recommended))
    }
```

### Task Generation

Tasks are automatically generated from language templates and merged:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Python: Run Tests",
      "type": "shell", 
      "command": "python",
      "args": ["-m", "pytest"],
      "group": "test"
    },
    {
      "label": "Terraform: Validate",
      "type": "shell",
      "command": "terraform", 
      "args": ["validate"],
      "group": "build"
    }
  ]
}
```

## Template Context Variables

Templates have access to repository metadata and computed values:

### Repository Metadata
```yaml
{{ metadata.languages }}        # ['python', 'terraform']
{{ metadata.platform }}         # 'github' | 'azuredevops'
{{ metadata.types }}            # ['app', 'tool']
{{ metadata.repo_name }}        # Repository directory name
{{ metadata.repo_path }}        # Full repository path
```

### Template Functions
```jinja2
{%- set config = load_enhanced_language_config('python', metadata) -%}
{%- for language in metadata.languages -%}
  # Process each language configuration
{%- endfor -%}
```

## Error Handling

### Template Missing
- System logs warning if language template not found
- Continues with basic configuration
- Maintains backward compatibility

### Invalid Template Syntax
- Jinja2 parsing errors are caught and logged
- Falls back to empty configuration for failed templates
- Provides detailed error messages for debugging

### Configuration Merging Conflicts
- Later configurations override earlier ones
- Language-specific settings take precedence over base settings
- Platform settings applied last to ensure correct integration

## Benefits

### Maintainability
- Configuration separated from Python code
- Easy to add new languages without code changes
- Template syntax is more readable than nested dictionaries

### Flexibility  
- Support for complex conditional logic in templates
- Easy customization per language or repository type
- Extensible without breaking existing functionality

### Consistency
- All repositories get consistent tool configurations
- Language best practices built into templates
- Standardized development environment setup

## Usage

The template system is automatically used by the workspace generator:

```bash
python scripts/setup-repository.py /path/to/repo
# Automatically processes templates for detected languages
# Generates complete VS Code workspace configuration
```

Template processing results are logged during generation:

```
📊 Processing templates for: python, terraform, yaml
  ✓ Generated .vscode/settings.json (enhanced: python, terraform, yaml)
  ✓ Generated .vscode/extensions.json (required: 8, recommended: 12)
  ✓ Generated .vscode/tasks.json (tasks: 6 from templates)
  ✓ Generated .vscode/launch.json (configs: 2 from enhanced templates)
```
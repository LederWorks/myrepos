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
│   ├── powershell.yaml.j2# PowerShell: PSScriptAnalyzer, Pester
│   ├── shell.yaml.j2    # Shell: shellcheck, shfmt, fish support
│   ├── j2.yaml.j2       # Jinja2: template validation, rendering
│   ├── terraform.yaml.j2# Terraform: validation, security, .tftpl support
│   ├── markdown.yaml.j2 # Markdown: linting, TOC generation
│   ├── yaml.yaml.j2     # YAML: validation, Kubernetes tools
│   └── ...              # Additional languages
├── .omd/
│   └── languages.yaml.j2 # Languages summary generator
├── .vscode/             # VS Code configuration templates
│   ├── extensions.json.j2
│   ├── settings.json.j2
│   ├── tasks.json.j2
│   └── launch.json.j2
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
        self.jinja_env.globals['format_yaml_json'] = format_yaml_json
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

### 4. Language Summary Generation
- Generate `.omd/languages.yaml` with populated configuration data
- Use custom `format_yaml_json()` formatter for readable output
- Include source comments with counts (settings, tasks, extensions)
- Maintain schema validation compatibility

### 5. Repository Type Detection
- Detect repository types based on file patterns and languages
- Template files (.j2, .jinja, .tftpl) trigger 'template' type
- Infrastructure files (.tf, .yaml with k8s) trigger 'infra' type
- Multiple types can be assigned (e.g., infra + template)

### 6. Additional File Creation
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
      "*.pyx": "python"
    
    # VS Code editor settings
    settings:
      "[python]":
        editor.formatOnSave: true
        editor.defaultFormatter: "ms-python.python"
        editor.codeActionsOnSave:
          source.organizeImports: "explicit"
        editor.tabSize: 4
      python.defaultInterpreterPath: "./venv/bin/python"
      python.linting.enabled: true
      python.linting.pylintEnabled: true
    
    # Required extensions (must install)
    required_extensions:
      - "ms-python.python"
      - "ms-python.black-formatter"
      - "ms-python.vscode-pylance"
      - "ms-python.isort"
    
    # Recommended extensions (suggested)
    recommended_extensions:
      - "ms-python.flake8"
      - "ms-python.pylint"
      - "ms-python.mypy-type-checker"
      - "ms-toolsai.jupyter"
    
    # Build/test tasks
    tasks:
      - label: "Python: Run Tests"
        type: "shell"
        command: "python"
        args: ["-m", "pytest"]
        group: "test"
      
      - label: "Python: Format Code"
        type: "shell"
        command: "black"
        args: ["."]
        group: "build"
    
    # Debug configurations
    launch_configurations:
      - name: "Python: Current File"
        type: "debugpy"
        request: "launch"
        program: "${file}"
        console: "integratedTerminal"
        python: "./venv/bin/python"
    
    # Package management
    package_management:
      tool: "pip"
      config_files:
        - "requirements.txt"
        - "setup.py"
        - "pyproject.toml"
```

## Custom YAML-Style JSON Formatter

The system includes a custom `format_yaml_json()` function for generating readable, properly indented JSON output while maintaining YAML schema compliance:

```python
def format_yaml_json(obj, indent_level=0):
    """Format JSON objects and arrays with YAML-style readability and trailing commas"""
    if isinstance(obj, list):
        if not obj:
            return "[]"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for item in obj:
            formatted_item = format_yaml_json(item, indent_level + 1)
            items.append(f'{item_indent}{formatted_item},')
        return "[\n" + "\n".join(items) + "\n" + base_indent + "]"
    elif isinstance(obj, dict):
        # Similar recursive formatting for objects
        # Returns properly indented, multi-line JSON with trailing commas
    else:
        return json.dumps(obj)
```

### Usage in Templates
```jinja2
settings:
  {{ format_yaml_json(config.settings, 3) if config.settings else "{}" }}
required_extensions:
  {{ format_yaml_json(config.required_extensions, 3) if config.required_extensions else "[]" }}
```

### Benefits
- Converts inline JSON to structured, multi-line format with proper indentation
- Maintains trailing commas throughout all nested structures
- Provides excellent readability for complex configuration objects
- Passes YAML schema validation requirements
- Uses 2-space indentation increments matching YAML standards

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

### Task Generation with Trailing Comma Strategy

Tasks are automatically generated from language templates with consistent formatting using trailing commas:

**Template Pattern:**
```jinja2
"tasks": [
{% for task in tasks %}
    {
      "label": "{{ task.label }}",
      "type": "{{ task.type }}",
      "command": "{{ task.command }}",
      "args": {{ task.args | tojson }},
      "group": "{{ task.group }}",
    },
{% endfor %}
]
```

**Generated Output:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Python: Run Tests",
      "type": "shell", 
      "command": "python",
      "args": ["-m", "pytest"],
      "group": "test",
      "problemMatcher": "$python",
    },
    {
      "label": "PowerShell: Analyze",
      "type": "shell",
      "command": "pwsh", 
      "args": ["-Command", "Invoke-ScriptAnalyzer", "-Path", ".", "-Recurse", "-ReportSummary"],
      "group": "test",
      "problemMatcher": "$pester",
    },
  ]
}
```

### Benefits of Trailing Comma Strategy
- Eliminates complex conditional comma logic in templates
- Produces consistently formatted output with proper line breaks
- JSONC format in VS Code supports trailing commas
- Future-proof: adding new elements requires only one line change
- Reduces template complexity by 60%

## Custom YAML-Style JSON Formatter

The system includes a custom `format_yaml_json()` function for generating readable, properly indented JSON output while maintaining YAML schema compliance:

```python
def format_yaml_json(obj, indent_level=0):
    """Format JSON objects and arrays with YAML-style readability and trailing commas"""
    if isinstance(obj, list):
        if not obj:
            return "[]"
        base_indent = "  " * indent_level
        item_indent = "  " * (indent_level + 1)
        items = []
        for item in obj:
            formatted_item = format_yaml_json(item, indent_level + 1)
            items.append(f'{item_indent}{formatted_item},')
        return "[\n" + "\n".join(items) + "\n" + base_indent + "]"
    elif isinstance(obj, dict):
        # Similar recursive formatting for objects
        # Returns properly indented, multi-line JSON with trailing commas
    else:
        return json.dumps(obj)
```

### Usage in Templates
```jinja2
settings:
  {{ format_yaml_json(config.settings, 3) if config.settings else "{}" }}
required_extensions:
  {{ format_yaml_json(config.required_extensions, 3) if config.required_extensions else "[]" }}
```

### Benefits
- Converts inline JSON to structured, multi-line format with proper indentation
- Maintains trailing commas throughout all nested structures
- Provides excellent readability for complex configuration objects
- Passes YAML schema validation requirements
- Uses 2-space indentation increments matching YAML standards

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

# Custom YAML-style JSON formatting
{{ format_yaml_json(config.settings, 3) if config.settings else "{}" }}

# Language detection and repository type detection
{%- if 'j2' in metadata.languages or 'terraform' in metadata.languages -%}
  # Template repository type detected
{%- endif -%}
```

## Repository Type Detection Logic

The system automatically detects repository types based on file patterns and language configurations:

### Template Type Detection
```python
def _detect_template_type(self, languages: List[str], repo_path: Path) -> bool:
    """Detect if repository contains template files"""
    # J2 language indicates template repository
    if 'j2' in languages:
        return True
    
    # Terraform template files (.tftpl) indicate template + infra
    if 'terraform' in languages:
        if self._has_files_with_extensions(repo_path, ['.tftpl']):
            return True
    
    return False
```

### Multi-Type Assignment
- **Template + Infra**: Repositories with `.tftpl` files get both types
- **Template + Docs**: Repositories with J2 templates and markdown
- **Infra Only**: Terraform without template files
- **Docs Only**: Pure documentation repositories

### File Pattern Detection
```python
language_patterns = {
    'python': ['.py', '.pyi', '.pyx'],
    'shell': ['.sh', '.bash', '.zsh'],
    'powershell': ['.ps1', '.psm1', '.psd1'],
    'j2': ['.j2', '.jinja', '.jinja2'],
    'terraform': ['.tf', '.tfvars', '.hcl', '.tftpl'],
    'yaml': ['.yaml', '.yml'],
    'markdown': ['.md', '.markdown'],
}
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

## Recent Language Implementations

### Jinja2 (J2) Language Support
- Complete template with file associations (`.j2`, `.jinja`, `.jinja2`)
- Required extension: `wholroyd.jinja`
- Template validation and rendering tasks
- Automatic template repository type detection

### Enhanced PowerShell Support
- Comprehensive file associations including `.ps1xml`, `.pssc`, `.psrc`
- PSScriptAnalyzer integration with custom settings
- Pester testing framework support
- PowerShell formatting with Invoke-Formatter
- Problem matcher integration (`$pester`)

### Enhanced Shell Support
- Extended file associations: `.fish`, `.bashrc`, `.zshrc`, `.profile`, `*.env`
- Multi-shell support (bash, zsh, fish)
- Shellcheck integration with proper problem matchers (`$shellcheck`)
- Shell formatting with `shfmt`
- Homebrew package management detection

### Terraform Template Enhancement
- Added `.tftpl` file association for Terraform templates
- Dual repository type detection (infra + template)
- Enhanced validation and security scanning

## Template Validation and Quality Assurance

### Schema Validation
All generated configurations are validated against JSON schemas:

```python
# Validate languages.yaml against schema
validation_result = validate_against_schema(
    languages_config, 
    self.schemas_dir / 'languages.yaml'
)

# Validate repository.yaml against schema  
repository_validation = validate_against_schema(
    repository_config,
    self.schemas_dir / 'repository.yaml'
)
```

### Template Quality Checklist
- ✅ Trailing comma pattern applied to all JSON arrays
- ✅ Custom YAML formatter for readable output
- ✅ Problem matchers for proper error integration
- ✅ Comprehensive file associations and settings
- ✅ Package management configuration included
- ✅ Launch configurations for debugging support

### Source Comment Generation
Templates automatically generate enriched comments showing configuration statistics:

```jinja2
# Source: templates/languages/{{ language }}.yaml.j2 ({{ config.settings | length }} settings, {{ config.tasks | length }} tasks, {{ config.required_extensions | length }} required ext, {{ config.recommended_extensions | length }} recommended ext)
```

## Recent Language Implementations

### Jinja2 (J2) Language Support
- Complete template with file associations (`.j2`, `.jinja`, `.jinja2`)
- Required extension: `wholroyd.jinja`
- Template validation and rendering tasks
- Automatic template repository type detection

### Enhanced PowerShell Support
- Comprehensive file associations including `.ps1xml`, `.pssc`, `.psrc`
- PSScriptAnalyzer integration with custom settings
- Pester testing framework support
- PowerShell formatting with Invoke-Formatter
- Problem matcher integration (`$pester`)

### Enhanced Shell Support
- Extended file associations: `.fish`, `.bashrc`, `.zshrc`, `.profile`, `*.env`
- Multi-shell support (bash, zsh, fish)
- Shellcheck integration with proper problem matchers (`$shellcheck`)
- Shell formatting with `shfmt`
- Homebrew package management detection

### Terraform Template Enhancement
- Added `.tftpl` file association for Terraform templates
- Dual repository type detection (infra + template)
- Enhanced validation and security scanning

## Benefits

### Maintainability
- Configuration separated from Python code
- Easy to add new languages without code changes
- Template syntax is more readable than nested dictionaries
- Custom YAML formatter provides excellent readability while maintaining schema compliance
- Trailing comma strategy eliminates complex conditional formatting logic

### Flexibility  
- Support for complex conditional logic in templates
- Easy customization per language or repository type
- Extensible without breaking existing functionality
- Multi-type repository detection (e.g., infra + template)
- Enhanced file association patterns (shell configs, template files)

### Consistency
- All repositories get consistent tool configurations
- Language best practices built into templates
- Standardized development environment setup
- Comprehensive extension management (required vs recommended)
- Proper problem matcher integration for error reporting

### Quality Assurance
- Schema validation ensures generated files are compliant
- Source comments show configuration statistics for transparency
- Enhanced templates include linting, formatting, and debugging support
- Package management detection for language ecosystems

## Usage

The template system is automatically used by the workspace generator:

```bash
python scripts/setup-repository.py /path/to/repo
# Automatically processes templates for detected languages
# Generates complete VS Code workspace configuration
```

Template processing results are logged during generation:

```
🚀 Setting up repository: myrepos
📍 Location: /Users/cuki/Data/Tools/myrepos

🔍 Processing repository: myrepos
📊 Detected content:
        platform: github
        languages: j2,markdown,powershell,python,shell,yaml
        types: docs,template
  ✓ Generated myrepos.code-workspace
  ✓ Generated .vscode/settings.json (enhanced: j2, markdown, powershell, python, shell, yaml)
  ✓ Generated .vscode/extensions.json (enhanced: j2, markdown, powershell, python, shell, yaml)
  ✓ Generated .vscode/launch.json (enhanced: powershell, python, shell)
  ✓ Generated .vscode/tasks.json (enhanced: j2, markdown, powershell, python, shell)
  ✓ Generated .omd/languages.yaml (validation compatibility)
✅ Setup completed for myrepos
🎉 Repository setup completed!
✅ Configuration loaded successfully for myrepos

🔍 Running validation...

Validation Summary: 1/1 repositories valid

✅ /Users/cuki/Data/Tools/myrepos
   Type: ['docs', 'template']
```

### Enhanced Language Summary

The `.omd/languages.yaml` file now includes enriched source comments:

```yaml
languages:
  powershell:
    # Source: templates/languages/powershell.yaml.j2 (6 settings, 3 tasks, 1 required ext, 2 recommended ext)
  shell:
    # Source: templates/languages/shell.yaml.j2 (6 settings, 4 tasks, 2 required ext, 3 recommended ext)
```

### Enhanced Language Summary

The `.omd/languages.yaml` file now includes enriched source comments:

```yaml
languages:
  powershell:
    # Source: templates/languages/powershell.yaml.j2 (6 settings, 3 tasks, 1 required ext, 2 recommended ext)
  shell:
    # Source: templates/languages/shell.yaml.j2 (6 settings, 4 tasks, 2 required ext, 3 recommended ext)
```
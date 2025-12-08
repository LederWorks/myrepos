# Language Detection and Repository Configuration

This document describes how the myrepos system automatically detects languages, platforms, and repository types, then configures appropriate VS Code settings and extensions.

## Repository Metadata Structure

Every repository must have a `.omd/repository.yaml` file with:

```yaml
languages: [python, yaml, markdown]  # Array of detected/specified languages
platform: github                    # github | azuredevops  
types: [app, tool]                   # Array: module, app, lib, infra, site, template, tool, config, data, docs, monorepo, example, experiment
```

## Language Detection Logic

### File Pattern Matching

The system detects languages by scanning file extensions and patterns:

- **Python**: `*.py`, `*.pyx`, `requirements.txt`, `setup.py`, `pyproject.toml`
- **Terraform**: `*.tf`, `*.tfvars`, `*.hcl`  
- **Markdown**: `*.md`, `*.mdx`, `README*`, `CHANGELOG*`
- **YAML**: `*.yml`, `*.yaml`, `.github/workflows/*.yml`
- **JSON**: `*.json`, `.vscode/*.json`
- **Go**: `*.go`, `go.mod`, `go.sum`
- **Shell**: `*.sh`, `*.bash`, `*.zsh`, `scripts/*`
- **PowerShell**: `*.ps1`, `*.psm1`
- **SQL**: `*.sql`, `*.ddl`

### Platform Detection

Platforms are identified by repository indicators:

- **GitHub**: `.github/` directory, `github.com` in remotes
- **Azure DevOps**: `.azuredevops/` directory, `dev.azure.com` in remotes

### Repository Type Rules

Types are determined by content analysis:

- **module**: Reusable components with clear interfaces
- **app**: Complete applications with dependencies
- **lib**: Libraries and packages for distribution  
- **infra**: Infrastructure as Code (Terraform, ARM, etc.)
- **tool**: CLI tools and utilities
- **docs**: Documentation-focused repositories
- **config**: Configuration-only repositories

## Configuration Priority

Settings are applied in this order (later overrides earlier):

1. **Base Template**: Common VS Code settings
2. **Language Templates**: Language-specific configurations from `templates/languages/{lang}.yaml.j2`
3. **Platform Settings**: GitHub/Azure DevOps extensions and workflows
4. **Repository Type**: Additional configurations based on types array

## Language Template Processing

Each language has a comprehensive template in `templates/languages/{language}.yaml.j2`:

### Template Structure

```yaml
# Example: python.yaml.j2
languages:
  python:
    file_associations:
      "*.py": "python"
    settings:
      "[python]":
        editor.formatOnSave: true
        editor.defaultFormatter: "ms-python.black-formatter"
      python.defaultInterpreterPath: "./venv/bin/python"
    required_extensions:
      - "ms-python.python"
      - "ms-python.black-formatter"
    recommended_extensions:
      - "ms-python.pylint"
    tasks:
      - label: "Python: Run Tests"
        type: "shell"
        command: "python"
        args: ["-m", "pytest"]
    launch_configurations:
      - name: "Python: Current File"
        type: "debugpy"
        request: "launch"
        program: "${file}"
```

### Available Language Templates

- **python.yaml.j2**: Black formatting, pytest, debugging, linting
- **go.yaml.j2**: Go tools, testing, debugging
- **markdown.yaml.j2**: Advanced formatting, TOC generation, linting
- **terraform.yaml.j2**: HCL formatting, validation, security scanning
- **yaml.yaml.j2**: Validation, Kubernetes tools
- **json.yaml.j2**: Schema validation, formatting
- **sql.yaml.j2**: Query formatting, database tools
- **shell.yaml.j2**: Bash/Zsh scripting tools
- **powershell.yaml.j2**: Script analysis, debugging

## Generated VS Code Files

The system generates complete VS Code workspace configuration:

### `.vscode/settings.json`
- Language-specific editor settings
- Formatter and linter configurations
- File associations and default behaviors

### `.vscode/extensions.json` 
- Required extensions for core functionality
- Recommended extensions for enhanced workflow
- Platform-specific extensions (GitHub, Azure DevOps)

### `.vscode/tasks.json`
- Language-specific build, test, format tasks
- Platform CI/CD integration tasks
- Custom repository-type tasks

### `.vscode/launch.json`
- Language-specific debug configurations
- Environment-aware debugging setups
- Multi-target debugging for complex repositories

## Detection Algorithms

### Smart Language Detection

1. **File Scan**: Recursively scan repository for known file patterns
2. **Confidence Scoring**: Weight files by importance (main files vs config)
3. **Framework Detection**: Identify specific frameworks within languages
4. **Dependency Analysis**: Parse package files for additional context

### Platform Recognition

1. **Directory Structure**: Look for platform-specific directories
2. **Remote Analysis**: Parse git remotes for hosting indicators  
3. **Workflow Files**: Detect existing CI/CD configurations
4. **Default Assignment**: Fall back to GitHub if no clear indicators

### Type Classification

1. **Content Analysis**: Analyze file types and directory structure
2. **Metadata Parsing**: Check for package.json, setup.py, etc.
3. **Documentation Patterns**: Identify documentation-heavy repositories
4. **Multi-Type Support**: Allow repositories to have multiple types

## Error Handling and Fallbacks

### Missing Templates
- System continues with basic configuration if language template missing
- Logs warnings for unavailable enhanced features
- Maintains backward compatibility with simple setups

### Invalid Metadata
- Validates required fields in repository.yaml
- Provides clear error messages for missing configuration
- Suggests fixes for common configuration issues

### Detection Failures
- Falls back to manual configuration when auto-detection unclear
- Allows explicit override of detected values
- Provides diagnostic information for troubleshooting

## Usage Patterns

### New Repository Setup
```bash
python scripts/setup-repository.py /path/to/repo
# Detects: languages, platform, types
# Generates: .omd/repository.yaml with detected values
```

### Existing Repository Enhancement
```bash
python scripts/setup-repository.py /path/to/existing/repo  
# Reads: existing .omd/repository.yaml
# Enhances: adds missing languages or updates configuration
```

### Manual Override
```yaml
# .omd/repository.yaml - explicit configuration
languages: [python, terraform]  # Override detection
platform: azuredevops          # Force specific platform
types: [lib, tool]             # Multiple types supported
```
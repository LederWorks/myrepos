# Template-Driven Configuration System

This document describes the new template-driven configuration system that replaces hardcoded Python dictionaries with flexible Jinja2 templates and YAML configuration files.

## Architecture Overview

The system consists of three main components:

### 1. Configuration Files (`templates/config/`)

- **`languages.yaml`**: Contains language-specific VS Code extensions and settings
- **`platforms.yaml`**: Contains platform-specific extensions (GitHub, Azure DevOps, GitLab)
- **`clients.yaml`**: Contains client-specific extensions and customizations

### 2. Jinja2 Templates (`templates/.vscode/`)

- **`settings.json.j2`**: Generates VS Code settings by merging configurations
- **`extensions.json.j2`**: Generates extension recommendations

### 3. Template Engine Integration

The `WorkspaceGenerator` class uses Jinja2 with a custom `load_yaml()` function to dynamically load configuration files within templates.

## Benefits

1. **Maintainability**: Configuration is separated from code logic
2. **Flexibility**: Easy to add new languages, platforms, or clients
3. **No Code Changes**: Adding new configurations requires only YAML updates
4. **Template Reusability**: Templates can be reused across different configurations
5. **Type Safety**: YAML files provide better validation than Python dictionaries

## Configuration Structure

### Language Configuration (`languages.yaml`)

```yaml
python:
  extensions:
    - ms-python.python
    - ms-python.black-formatter
  settings:
    python.defaultInterpreterPath: "./venv/bin/python"
    "[python]":
      editor.formatOnSave: true
```

### Platform Configuration (`platforms.yaml`)

```yaml
github:
  extensions:
    - github.vscode-pull-request-github
    - github.copilot
```

### Template Usage

Templates access configurations using the `load_yaml()` function:

```jinja2
{%- set languages = load_yaml('config/languages.yaml') -%}
{%- for language in metadata.languages -%}
  {# Process language configuration #}
{%- endfor -%}
```

## Migration Benefits

### Before (Hardcoded Python)
- 300+ lines of hardcoded dictionaries
- Code changes required for new languages
- Duplication across methods
- Lint warnings for repeated strings

### After (Template-Driven)
- Flexible YAML configuration
- Template-based generation
- No code changes for new configurations
- Centralized configuration management

## Usage

The system is automatically used by the `WorkspaceGenerator` class. The templates are rendered with the repository metadata and the resulting JSON files are written to `.vscode/`.

### Error Handling

The system includes fallback mechanisms:
- If template rendering fails, it falls back to the legacy hardcoded methods
- Error messages indicate whether templates or fallback methods were used
- Both approaches ensure the system continues to work

## Future Enhancements

1. **Validation**: Add schema validation for YAML configuration files
2. **Conditional Logic**: Add more sophisticated template conditions
3. **User Overrides**: Allow per-repository configuration overrides
4. **Extension Marketplace Integration**: Auto-detect recommended extensions
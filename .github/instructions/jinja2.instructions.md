---
applyTo: "**/*.j2,**/*.jinja,**/*.jinja2,templates/**/*"
---

# Jinja2 Template Development Standards

This document defines comprehensive standards for all Jinja2 templates in the MyRepos project, ensuring consistency, maintainability, and best practices across all template files.

## Template Architecture Overview

The MyRepos system uses Jinja2 templates for generating VS Code workspace configurations, language-specific settings, and platform-specific files. Templates follow a multi-layer approach:

1. **Enhanced Templates** (`templates/languages/*.yaml.j2`) - Rich configurations with all features
2. **Generated VS Code Files** (`.vscode/*.json`) - Applied configurations for development environment  
3. **Schema Validation File** (`.omd/languages.yaml`) - Populated summary for user visibility and validation

## Template Data Flow

```
Enhanced Templates (*.yaml.j2)
    ↓ (load_enhanced_language_config)
Workspace Generator (generator.py)  
    ↓ (generates)
VS Code Files (.vscode/*.json)
    ↓ (extracts for)
Languages Summary (.omd/languages.yaml)
    ↓ (validates against)
Schema (schemas/languages.yaml)
```

## Template Formatting Standards

### Trailing Comma Strategy for JSON Arrays

**Solution Implemented**: Use trailing commas in all JSON array templates to ensure consistent formatting and simpler template logic.

**Benefits**:
- Eliminates complex `{% if not loop.last %}` conditional comma logic
- Produces consistently formatted output with proper line breaks
- Makes templates easier to maintain and debug
- JSONC format in VS Code supports trailing commas
- Future-proof: adding new elements requires only one line change

**Template Pattern**:
```jinja2
"array_property": [
{% for item in items %}
    "{{ item }}",
{% endfor %}
]
```

**Applied To**:
- `templates/.vscode/extensions.json.j2` - Extension recommendations
- `templates/.vscode/launch.json.j2` - Debug configurations
- `templates/.omd/languages.yaml.j2` - Languages configuration summary
- All other array-based VS Code configuration templates

### Custom YAML-Style JSON Formatting

**Advanced Solution**: Implemented custom `format_yaml_json()` function for languages.yaml template to produce readable, properly indented output while maintaining YAML schema compliance.

**Benefits**:
- Converts inline JSON to structured, multi-line format with proper indentation
- Maintains trailing commas throughout all nested structures
- Provides excellent readability for complex configuration objects
- Passes YAML schema validation requirements
- Eliminates need for manual formatting of generated files

**Implementation Details**:
- Added to `scripts/workspace/generator.py` as Jinja2 global function
- Handles nested objects and arrays recursively with proper indentation levels
- Uses 2-space indentation increments matching YAML standards
- Template calls function with appropriate base indentation level (3 for languages.yaml structure)

**Function Signature**:
```python
def format_yaml_json(obj, indent_level=0):
    """Format JSON objects and arrays with YAML-style readability and trailing commas"""
```

**Usage in Templates**:
```jinja2
settings:
  {{ format_yaml_json(config.settings, 3) if config.settings else "{}" }}
```

## Template Development Best Practices

### Template Structure Standards

#### File Naming Conventions
- Use descriptive names that indicate the target output: `settings.json.j2`, `extensions.json.j2`
- Language templates: `{language}.yaml.j2` (e.g., `python.yaml.j2`, `terraform.yaml.j2`)
- Platform templates: Use directory structure to indicate platform (`.azuredevops/`, `.github/`)

#### Template Organization
```jinja2
{# Template header with description #}
{# 
  Template: VS Code Extensions Configuration
  Purpose: Generate language-specific extension recommendations
  Output: .vscode/extensions.json
#}

{# Template variables and configuration #}
{% set base_extensions = [...] %}

{# Main template content with proper indentation #}
{
  "recommendations": [
{% for extension in extensions %}
    "{{ extension }}",
{% endfor %}
  ]
}
```

#### Comment Standards
- Use `{# #}` for template comments (not rendered)
- Add descriptive headers explaining template purpose and output
- Document complex logic with inline comments
- Use section dividers for template organization

```jinja2
{# 
  Template: VS Code Extensions Configuration
  Purpose: Generate extension recommendations based on detected languages
  Output: .vscode/extensions.json
#}

{# Language-specific extension mapping #}
{% set language_extensions = {
    'python': ['ms-python.python', 'ms-python.black-formatter'],
    'go': ['golang.go', 'ms-vscode.go']
} %}

{# Main configuration generation #}
{
  "recommendations": [
    {# Base extensions for all projects #}
{% for extension in base_extensions %}
    "{{ extension }}",
{% endfor %}
    {# Language-specific extensions #}
{% for language in languages %}
  {% if language in language_extensions %}
    {% for extension in language_extensions[language] %}
    "{{ extension }}",
    {% endfor %}
  {% endif %}
{% endfor %}
  ]
}
```

### Variable Handling and Safety

#### Undefined Variable Handling
- Always provide default values for optional variables
- Use the `default()` filter for safe variable access
- Test for variable existence before complex operations

```jinja2
{# Safe variable access with defaults #}
{{ config.description | default('Auto-generated configuration') }}

{# Conditional rendering based on variable existence #}
{% if deployment_platform is defined and deployment_platform %}
"deploymentPlatform": "{{ deployment_platform }}",
{% endif %}

{# Safe list operations #}
{% set extensions = config.extensions | default([]) %}
{% for extension in extensions %}
  "{{ extension }}",
{% endfor %}
```

#### Type Safety and Validation
- Validate variable types before operations
- Handle edge cases gracefully
- Provide meaningful error messages

```jinja2
{# Type checking and validation #}
{% if languages is defined and languages is iterable %}
  {% for language in languages %}
    {% if language is string and language %}
      "{{ language }}": { ... },
    {% endif %}
  {% endfor %}
{% else %}
  {# Error handling or default configuration #}
  "default": { "message": "No languages configured" }
{% endif %}
```

### Template Performance Optimization

#### Efficient Loop Patterns
- Cache complex calculations outside loops
- Use appropriate loop controls (`break`, `continue`)
- Minimize nested loops where possible

```jinja2
{# Pre-calculate complex values #}
{% set filtered_languages = languages | selectattr('enabled') | list %}
{% set has_frontend = 'typescript' in languages or 'javascript' in languages %}

{# Efficient iteration #}
{% for language in filtered_languages %}
  {% if language.config is defined %}
    "{{ language.name }}": {{ language.config | tojson }},
  {% endif %}
{% endfor %}
```

#### Memory Management
- Avoid creating large intermediate lists unnecessarily
- Use generators and filters appropriately
- Clean up temporary variables in long templates

### Error Handling and Debugging

#### Template Debugging Techniques
- Use conditional debug output for development
- Implement graceful degradation for missing data
- Provide informative error messages

```jinja2
{# Debug mode conditional output #}
{% if debug_mode | default(false) %}
  "debug": {
    "template": "{{ template_name }}",
    "variables": {{ template_variables | tojson }},
    "timestamp": "{{ now() }}"
  },
{% endif %}

{# Graceful error handling #}
{% set config_error = false %}
{% if not languages %}
  {% set config_error = true %}
  "error": "No languages specified in configuration",
{% endif %}
```

#### Validation and Testing
- Include validation logic in templates where appropriate
- Test templates with various input combinations
- Document expected input formats and constraints

### Security Considerations

#### Input Sanitization
- Escape user-provided content appropriately
- Validate file paths and names
- Avoid dynamic code execution

```jinja2
{# Safe file path handling #}
"configPath": "{{ config_path | replace('..', '') | trim }}",

{# Content escaping for JSON #}
"description": {{ user_description | tojson }},

{# Safe string interpolation #}
{% set safe_name = repo_name | regex_replace('[^a-zA-Z0-9._-]', '') %}
"name": "{{ safe_name }}",
```

#### Template Injection Prevention
- Never use user input directly in template logic
- Validate all dynamic template paths
- Use allow-lists for template selection

### Integration Standards

#### Cross-Template Consistency
- Use shared template functions for common operations
- Maintain consistent variable naming across templates
- Follow established patterns from other MyRepos templates

#### Generator Integration
- Document required variables from generator.py
- Follow established calling conventions
- Maintain backward compatibility where possible

```jinja2
{# Standard MyRepos template variables #}
{# Required: repo_name, languages, types, ci_platform #}
{# Optional: deployment_platform, detected_languages #}

{# Template header documenting dependencies #}
{#
  Dependencies:
  - repo_name (string): Repository name
  - languages (list): Detected programming languages  
  - types (list): Repository types (lib, app, etc.)
  - ci_platform (string): CI/CD platform (github, azuredevops, etc.)
#}
```

## Quality Assurance Standards

### Template Validation
- Test all conditional branches
- Verify output with various language combinations
- Validate JSON/YAML output syntax
- Check for proper indentation and formatting

### Documentation Requirements
- Document all template variables and their types
- Provide usage examples for complex templates
- Explain integration points with the generator system
- Include troubleshooting guidance for common issues

### Maintenance Guidelines
- Keep templates synchronized with schema changes
- Update templates when new languages are added
- Maintain compatibility with existing configurations
- Follow semantic versioning for breaking template changes

This comprehensive instruction system ensures that all Jinja2 templates in the MyRepos project maintain high quality, consistency, and reliability while providing the flexibility needed for diverse development environments.
- Add descriptive headers explaining template purpose
- Document complex logic or non-obvious template operations
- Include examples for complex template patterns

### Conditional Logic Patterns

#### Proper Conditional Formatting
```jinja2
{# Good: Clean conditional with proper indentation #}
{% if config.has_tasks %}
  "tasks": [
{% for task in config.tasks %}
    {
      "label": "{{ task.label }}",
      "type": "{{ task.type }}",
      "command": "{{ task.command }}",
    },
{% endfor %}
  ],
{% endif %}

{# Bad: Inline conditionals that break formatting #}
"tasks": [{% for task in config.tasks if config.has_tasks %}"{{ task }}",{% endfor %}]
```

#### Variable Validation
```jinja2
{# Validate required variables at template start #}
{% if not config %}
  {% set config = {} %}
{% endif %}

{# Provide sensible defaults #}
{% set settings = config.settings or {} %}
{% set extensions = config.required_extensions or [] %}
```

### Loop and Iteration Patterns

#### Array Generation with Trailing Commas
```jinja2
{# Standard array pattern - always use trailing commas #}
"extensions": [
{% for ext in extensions %}
  "{{ ext }}",
{% endfor %}
]

{# Object array pattern #}
"tasks": [
{% for task in tasks %}
  {
    "label": "{{ task.label }}",
    "command": "{{ task.command }}",
  },
{% endfor %}
]
```

#### Nested Loop Handling
```jinja2
{# Handle nested structures properly #}
"settings": {
{% for category, settings_group in settings.items() %}
  "{{ category }}": {
{% for key, value in settings_group.items() %}
    "{{ key }}": {{ value | tojson }},
{% endfor %}
  },
{% endfor %}
}
```

## Template Content Standards

### JSON Template Guidelines

#### String Escaping
- Use Jinja2's `| tojson` filter for proper JSON string escaping
- Always quote template variables in JSON context
- Handle special characters and unicode properly

```jinja2
{# Proper JSON escaping #}
"description": {{ task.description | tojson }},
"command": {{ task.command | tojson }},
"args": {{ task.args | tojson }},
```

#### Boolean and Number Handling
```jinja2
{# Handle different data types correctly #}
"enabled": {{ config.enabled | lower }},
"port": {{ config.port | int }},
"timeout": {{ config.timeout | float }},
```

### YAML Template Guidelines

#### Indentation Standards
- Use 2-space indentation consistently
- Maintain proper YAML structure alignment
- Use the `format_yaml_json()` function for complex objects

```jinja2
{# Proper YAML indentation #}
settings:
  {{ format_yaml_json(config.settings, 1) if config.settings else "{}" }}

required_extensions:
{% for ext in extensions %}
  - {{ ext }}
{% endfor %}
```

#### YAML-Safe Content
```jinja2
{# Ensure YAML compatibility #}
{% for key, value in metadata.items() %}
{{ key }}: {{ value | yaml_safe }}
{% endfor %}
```

## Error Handling and Validation

### Template Error Prevention

#### Null Safety
```jinja2
{# Always check for null/empty values #}
{% if config and config.extensions %}
"extensions": [
{% for ext in config.extensions %}
  "{{ ext }}",
{% endfor %}
]
{% else %}
"extensions": []
{% endif %}
```

#### Type Checking
```jinja2
{# Validate expected data types #}
{% if config.tasks is iterable and config.tasks is not string %}
{% for task in config.tasks %}
  {# Process task #}
{% endfor %}
{% endif %}
```

### Template Testing Patterns

#### Test Data Validation
- Create test fixtures with various data scenarios
- Test with empty, null, and malformed data
- Validate generated output against target schemas
- Test template rendering with different language combinations

#### Debugging Templates
```jinja2
{# Debug information (remove in production) #}
{% if debug %}
{# DEBUG: Config contents: {{ config | tojson }} #}
{% endif %}

{# Template validation checks #}
{% if not config %}
  {# ERROR: Configuration not provided #}
{% endif %}
```

## Template Quality Standards

### Template Quality Checklist

When creating or updating Jinja2 templates:

- [ ] Use trailing commas for all JSON arrays
- [ ] Avoid complex conditional comma logic (`{% if not loop.last %}`)
- [ ] Ensure consistent indentation and line breaks
- [ ] Test with both single and multiple element arrays
- [ ] Verify JSONC compatibility for VS Code files
- [ ] Validate generated output formatting
- [ ] Include proper template comments and documentation
- [ ] Handle null/empty data gracefully
- [ ] Use appropriate Jinja2 filters for data types
- [ ] Test template rendering across different scenarios

### Performance Considerations

#### Template Efficiency
- Minimize complex calculations within templates
- Use template variables for repeated operations
- Cache frequently accessed template data
- Avoid deeply nested conditional logic

```jinja2
{# Good: Pre-calculate complex values #}
{% set has_python = 'python' in languages %}
{% set has_testing = config.testing_framework is defined %}

{# Use cached values throughout template #}
{% if has_python and has_testing %}
  {# Python testing configuration #}
{% endif %}
```

#### Template Reusability
- Create modular template components
- Use template inheritance for common patterns
- Define reusable macros for complex operations
- Maintain consistent template interfaces

```jinja2
{# Define reusable macros #}
{% macro render_extension_list(extensions) %}
[
{% for ext in extensions %}
  "{{ ext }}",
{% endfor %}
]
{% endmacro %}

{# Use macro throughout template #}
"required": {{ render_extension_list(config.required_extensions) }},
"recommended": {{ render_extension_list(config.recommended_extensions) }},
```

## Integration with MyRepos System

### Language Template Standards

#### Enhanced Language Template Structure
```jinja2
{# Enhanced language template: templates/languages/python.yaml.j2 #}
file_associations:
  - "*.py"
  - "*.pyw"
  - "*.pyi"

settings:
  "[python]":
    editor.formatOnSave: true
    editor.defaultFormatter: "ms-python.python"
  python.defaultInterpreterPath: "./venv/bin/python"

required_extensions:
  - "ms-python.python"
  - "ms-python.black-formatter"

tasks:
  - label: "Python: Run Tests"
    type: "shell"
    command: "python -m pytest"
```

#### VS Code Integration Templates
- Follow VS Code JSON schema requirements
- Support JSONC format with trailing commas
- Generate valid configuration for all VS Code versions
- Test generated configurations in actual VS Code workspaces

### Schema Compliance

#### Template-Schema Alignment
- Ensure generated output validates against JSON schemas
- Use schema-aware template development
- Maintain compatibility with schema versions
- Document schema dependencies in templates

#### Validation Integration
```jinja2
{# Template should generate schema-compliant output #}
{# Reference: schemas/languages.yaml for validation rules #}
{% set config = load_enhanced_language_config(language) %}
{{ format_yaml_json(config, 0) }}
```

## Template Maintenance Standards

### Version Control Standards
- Commit template changes with clear descriptions
- Test template changes across multiple scenarios
- Update related documentation when changing templates
- Maintain backward compatibility when possible

### Documentation Requirements
- Document template purpose and output format
- Include usage examples and test scenarios  
- Explain complex template logic and transformations
- Reference related templates and dependencies

### Template Evolution
- Follow semantic versioning for template changes
- Provide migration guides for breaking changes
- Maintain deprecated templates during transition periods
- Plan template architecture for future extensibility

This comprehensive guide ensures consistent, maintainable, and high-quality Jinja2 template development across the MyRepos project.

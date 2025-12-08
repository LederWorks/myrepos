# Agent Coordination and Language Template Management

This document outlines the coordination process for maintaining language templates and ensuring consistency across the myrepos tooling system.

## Language Template System Architecture

The myrepos system uses a multi-layer approach for language configuration:

1. **Enhanced Templates** (`templates/languages/*.yaml.j2`) - Rich configurations with all features
2. **Generated VS Code Files** (`.vscode/*.json`) - Applied configurations for development environment  
3. **Schema Validation File** (`.omd/languages.yaml`) - Populated summary for user visibility and validation

## Update Process for Language Features

When adding new default settings, extensions, tasks, or configurations to any supported language, follow this sequence:

### 1. Update Enhanced Language Templates
**Location**: `templates/languages/{language}.yaml.j2`

Add new features to the appropriate language template:
- `settings` - VS Code editor configurations
- `required_extensions` - Essential extensions for the language
- `recommended_extensions` - Helpful but optional extensions
- `tasks` - Build, test, format, lint commands
- `launch_configurations` - Debugging setups
- `linting` - Code quality tool configurations
- `package_management` - Language-specific tooling

### 2. Update Languages Template Generator
**Location**: `templates/.omd/languages.yaml.j2`

The languages.yaml generator template must be updated to:
- Extract new configuration data from enhanced templates
- Populate the schema-compliant structure with actual values
- Maintain validation compatibility while showing real data

**Current Issue**: The template generates empty structures instead of extracting actual data from enhanced templates.

### 3. Regenerate Workspace Configuration
**Command**: `python scripts/setup-repository.py /path/to/repo`

This will:
- Process updated enhanced templates
- Generate new VS Code configuration files
- Create populated `.omd/languages.yaml` with actual data
- Validate against schemas

### 4. Test and Validate
**Commands**:
```bash
# Full setup with validation
python scripts/setup-repository.py /path/to/repo

# Validation only
python scripts/setup-repository.py --validate /path/to/repo
```

## Coordination Requirements

### When Adding New Language Support:
1. Create `templates/languages/{language}.yaml.j2` with full configuration
2. Add language to schema pattern in `schemas/languages.yaml` if not already present
3. Update languages.yaml.j2 template to handle the new language
4. Test with a repository that uses the new language

### When Updating Existing Languages:
1. Modify the specific `templates/languages/{language}.yaml.j2` file
2. Ensure changes are reflected in generated `.omd/languages.yaml`
3. Test that VS Code files are updated correctly
4. Validate schema compliance

### When Adding New Configuration Categories:
1. Update enhanced template structure
2. Update `schemas/languages.yaml` schema if needed
3. Update `templates/.omd/languages.yaml.j2` to extract new data
4. Update workspace generator if new VS Code files are needed

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

## Template Formatting Best Practices

### Trailing Comma Strategy for JSON Arrays
**Solution Implemented**: Use trailing commas in all JSON array templates to ensure consistent formatting and simpler template logic.

**Benefits**:
- Eliminates complex `{% if not loop.last %}` conditional comma logic
- Produces consistently formatted output with proper line breaks
- Makes templates easier to maintain and debug
- JSONC format in VS Code supports trailing commas
- Future-proof: adding new elements requires only one line change

**Template Pattern**:
```jinja
"array_property": [
{% for item in items %}
    "{{ item }}",
{% endfor %}
]
```

**Applied To**:
- `templates/.vscode/extensions.json.j2` - Extension recommendations
- `templates/.vscode/launch.json.j2` - Debug configurations
- All other array-based VS Code configuration templates

### Current Implementation Status

**Resolved**: The `templates/.omd/languages.yaml.j2` template now generates populated structures using inline JSON format:
```yaml
languages:
  python:
    # Source: templates/languages/python.yaml.j2 (4 settings, 2 tasks)
    settings: {"[python]": {"editor.defaultFormatter": "ms-python.python", ...}, ...}
    required_extensions: ["ms-python.python", "ms-python.black-formatter", ...]
    recommended_extensions: ["ms-python.flake8", "ms-python.pylint", ...]
    tasks: [{"label": "Python: Run Tests", "command": "python", ...}, ...]
```

**Key Achievements**:
- Schema validation passes with real configuration data
- Enhanced templates successfully integrated with validation system
- VS Code configuration files generate with proper formatting
- Inline JSON format maintains readability while passing validation

## Maintenance Checklist

When making language configuration changes:

- [ ] Enhanced template updated with new features
- [ ] Languages.yaml.j2 template extracts new data correctly
- [ ] VS Code files generate correctly with new features
- [ ] Schema validation passes
- [ ] Generated languages.yaml shows actual populated data
- [ ] **Array templates use trailing comma pattern for consistent formatting**
- [ ] Documentation updated if new configuration categories added
- [ ] Tests pass for affected repositories

### Template Quality Checklist

When creating or updating Jinja2 templates:

- [ ] Use trailing commas for all JSON arrays
- [ ] Avoid complex conditional comma logic (`{% if not loop.last %}`)
- [ ] Ensure consistent indentation and line breaks
- [ ] Test with both single and multiple element arrays
- [ ] Verify JSONC compatibility for VS Code files
- [ ] Validate generated output formatting

## Agent Responsibilities

1. **Template Updates**: Ensure enhanced templates have comprehensive configurations
2. **Data Extraction**: Maintain languages.yaml.j2 to populate with real data using inline JSON format
3. **Validation**: Maintain schema compliance while providing useful information
4. **Consistency**: Keep all language templates following the same structure and patterns
5. **Formatting Standards**: Apply trailing comma pattern to all JSON array templates
6. **Documentation**: Update this guide when new patterns or requirements emerge

## Resolved Issues

### Languages.yaml Schema Compliance ✅
- Successfully converted to inline JSON format for schema validation
- Real configuration data extracted from enhanced templates
- Maintains readability with source comments and counts

### VS Code Configuration Formatting ✅  
- Extensions.json: Clean array formatting with trailing commas
- Launch.json: Proper indentation and line breaks for debug configurations
- Consistent formatting across all generated JSON files

### Template Simplification ✅
- Eliminated complex conditional comma logic in Jinja2 templates
- Standardized on trailing comma approach for all arrays
- Future-proof template patterns for easy maintenance

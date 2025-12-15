# Agent Coordination and Language Template Management

This document provides master project tracking, component status overview, and cross-component coordination for the MyRepos tooling system. It serves as the root-level coordination document in the hierarchical documentation architecture.

## Documentation Architecture

This file is part of the MyRepos hierarchical documentation structure:

```
AGENTS.md (root)                     ← Master tracking & component coordination (this file)
├── .github/copilot-instructions.md  ← GitHub Copilot project context
├── .github/instructions/*.md        ← Technology-specific development standards
└── docs/*.md                        ← Component-specific documentation
```

For GitHub Copilot context and instruction file navigation, see [GitHub Copilot Instructions](.github/copilot-instructions.md).

## System Architecture Overview

The MyRepos system uses a multi-layer approach for language configuration and cross-component coordination:

1. **Enhanced Templates** (`templates/languages/*.yaml.j2`) - Rich configurations with all features
2. **Generated VS Code Files** (`.vscode/*.json`) - Applied configurations for development environment  
3. **Schema Validation File** (`.omd/languages.yaml`) - Populated summary for user visibility and validation

## Component Coordination Process

When adding new default settings, extensions, tasks, or configurations to any supported language, follow this coordination sequence across components:

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

**Implementation Note**: Template development follows comprehensive standards defined in [Jinja2 Instructions](.github/instructions/jinja2.instructions.md).

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

## Cross-Component Coordination Requirements

These coordination requirements ensure consistency across all MyRepos components and maintain integration with the instruction file system and dynamic template generation.

### When Adding New Language Support:
1. **Create Enhanced Language Template**: `templates/languages/{language}.yaml.j2` with full configuration
   - Include file_associations, settings, required_extensions, recommended_extensions, tasks, linting
   - Follow established YAML structure and naming conventions
   - Use proper VS Code setting patterns for language-specific configurations
   - Adhere to template development standards (see [Jinja2 Instructions](.github/instructions/jinja2.instructions.md))

2. **Update Language Detection Logic**: `scripts/workspace/generator.py`
   - Add file extensions to `language_patterns` dictionary in `_detect_languages()` method
   - Include all relevant file extensions (e.g., `.tf`, `.tfvars`, `.hcl` for terraform)

3. **Update Schema Validation**: `schemas/languages.yaml`
   - Add new language to the regex pattern in `patternProperties`
   - Ensure language name matches exactly between template, detection logic, and schema

4. **Update Repository Schema** (if needed): `schemas/repository.yaml`
   - Add language to supported languages enum if not already present
   - Update any repository type detection logic if language implies specific types

5. **Test Language Detection**: Create test files and verify
   - Create sample files with the language's extensions
   - Run setup script to verify language is detected: `python scripts/setup-repository.py /path/to/repo`
   - Check that language appears in generated `.omd/repository.yaml`

6. **Validate Template Generation**: Check VS Code integration
   - Verify extensions are included in `.vscode/extensions.json`
   - Verify settings appear in `.vscode/settings.json`
   - Verify tasks appear in `.vscode/tasks.json` (if applicable)
   - Verify launch configurations appear in `.vscode/launch.json` (if applicable)

7. **Validate Schema Compliance**: Run validation
   - Execute: `python scripts/setup-repository.py --validate /path/to/repo`
   - Ensure no schema validation errors for the new language

8. **Clean Up Test Files**: Remove temporary test files created during validation

### When Updating Existing Languages:
1. **Update Enhanced Template**: Modify `templates/languages/{language}.yaml.j2`
   - Add new settings, extensions, tasks, or other configuration
   - Follow trailing comma patterns for arrays and objects
   - Maintain consistent structure with other language templates

2. **Update Detection Logic** (if adding new file extensions):
   - Add new file extensions to `language_patterns` in `scripts/workspace/generator.py`
   - Update any repository type detection if new file types imply different repository types

3. **Test Configuration Generation**:
   - Create test repository with the language files
   - Run: `python scripts/setup-repository.py /path/to/test-repo`
   - Verify new configurations appear in generated VS Code files

4. **Validate Template Data Extraction**:
   - Check that new configurations appear in `.omd/languages.yaml` with proper formatting
   - Verify trailing commas and indentation are correct using custom YAML-style JSON formatter

5. **Run Schema Validation**:
   - Execute: `python scripts/setup-repository.py --validate /path/to/test-repo`
   - Ensure no validation errors introduced by changes

6. **Test Existing Repositories**: Verify backward compatibility
   - Run setup on existing repositories using the language
   - Ensure no breaking changes to existing configurations

### When Adding New Configuration Categories:
1. **Update Enhanced Template Structure**: Add new category to language templates
   - Define new configuration section (e.g., `package_management`, `debugging`)
   - Follow established YAML structure and naming patterns
   - Apply trailing comma formatting for consistency

2. **Update Languages Schema**: `schemas/languages.yaml`
   - Add new property definition with proper type and description
   - Include validation rules and constraints if applicable
   - Update schema examples if needed

3. **Update Languages Template Generator**: `templates/.omd/languages.yaml.j2`
   - Add extraction logic for new configuration category
   - Use `format_yaml_json()` function for proper formatting
   - Ensure proper indentation level (typically level 3)

4. **Update Workspace Generator** (if new VS Code files needed): `scripts/workspace/generator.py`
   - Add generation logic for new VS Code configuration files
   - Implement data collection from enhanced templates
   - Apply trailing comma formatting patterns

5. **Update Repository Detection** (if category implies repository types):
   - Add detection logic for new configuration patterns
   - Update repository type assignment in `_detect_repository_types()`

6. **Test New Category**:
   - Add new configuration to test language template
   - Generate and verify new configuration appears correctly
   - Test with multiple languages to ensure consistency

7. **Validate Integration**:
   - Run full setup and validation on test repository
   - Verify new category data flows through entire system
   - Check YAML formatting and schema compliance

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

## Template Development Standards

For comprehensive Jinja2 template development guidelines, including formatting best practices, trailing comma strategies, custom YAML-style JSON formatting, and template quality standards, see:

**[Jinja2 Instructions](.github/instructions/jinja2.instructions.md)**

Key template standards implemented:
- **Trailing Comma Strategy**: Eliminates complex conditional comma logic in JSON arrays
- **Custom YAML-Style JSON Formatting**: `format_yaml_json()` function for readable output
- **Template Quality Checklist**: Standardized validation and formatting requirements
- **Cross-Platform Compatibility**: Templates work across all supported platforms

### Current Implementation Status

**Resolved**: The `templates/.omd/languages.yaml.j2` template now generates populated structures using custom YAML-style JSON formatting with real configuration data extracted from enhanced templates:
```yaml
languages:
  python:
    # Source: templates/languages/python.yaml.j2 (4 settings, 2 tasks)
    settings:
      {
        "[python]": {
          "editor.formatOnSave": true,
          "editor.defaultFormatter": "ms-python.python",
          "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit",
          },
        },
        "python.defaultInterpreterPath": "./venv/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
      }
    required_extensions:
      [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.vscode-pylance",
        "ms-python.isort",
      ]
```

**Key Achievements**:
- Schema validation passes with real configuration data
- Enhanced templates successfully integrated with validation system
- VS Code configuration files generate with proper formatting
- Custom YAML-style JSON format maintains excellent readability while passing validation
- Proper indentation and trailing commas throughout all data structures
- Complete language detection and repository type detection system
- J2 and enhanced terraform language support fully implemented

## Cross-Component Maintenance Checklist

When making language configuration changes, ensure coordination across all system components:

- [ ] Enhanced template updated with new features
- [ ] Languages.yaml.j2 template extracts new data correctly
- [ ] VS Code files generate correctly with new features
- [ ] Schema validation passes
- [ ] Generated languages.yaml shows actual populated data
- [ ] **Templates follow formatting standards** (see [Jinja2 Instructions](.github/instructions/jinja2.instructions.md))
- [ ] Documentation updated if new configuration categories added
- [ ] Tests pass for affected repositories

### Template Quality Standards

For complete template quality checklist and development standards, see [Jinja2 Instructions](.github/instructions/jinja2.instructions.md#template-quality-standards).

## Agent Coordination Responsibilities

### Language Template System Coordination

1. **Template Updates**: Ensure enhanced templates have comprehensive configurations across all supported languages
2. **Data Extraction**: Maintain languages.yaml.j2 to populate with real data using inline JSON format
3. **Schema Validation**: Maintain schema compliance while providing useful information across all components
4. **Cross-Component Consistency**: Keep all language templates following the same structure and patterns
5. **Standards Compliance**: Follow comprehensive development guidelines across all instruction files:
   - [Jinja2 Instructions](.github/instructions/jinja2.instructions.md) for template development
   - [Python Instructions](.github/instructions/python.instructions.md) for script development
   - [Scripts Instructions](.github/instructions/scripts.instructions.md) for automation
6. **Documentation Coordination**: Update this guide and coordinate with instruction files when new patterns emerge
7. **Cross-Platform Integration**: Ensure all components work consistently across Windows, Linux, and macOS

### J2 Instruction Templating System Coordination

The MyRepos system includes a dual coordination framework managing both language template generation and dynamic instruction file templating. This section outlines coordination requirements for the J2 instruction templating system that operates alongside the established language template coordination.

#### Instruction File Template Architecture

**Template Structure**: All instruction files in `.github/instructions/` follow a standardized J2 template pattern:
- **YAML Frontmatter**: `applyTo` patterns for file matching and auto-detection
- **Content Sections**: Structured development guidelines with consistent organization
- **Cross-References**: Dynamic links to related instruction files and project components
- **Template Variables**: Configurable content based on repository detection and technology stack

**Dynamic Generation Process**:
1. **Repository Analysis**: Detect languages, frameworks, and project types
2. **Instruction Selection**: Generate only relevant instruction files based on detection
3. **Cross-Reference Generation**: Build dynamic instruction file reference table
4. **Template Rendering**: Apply detected context to J2 instruction templates
5. **Integration**: Coordinate with language template system and VS Code configuration

#### Instruction File Detection and Filtering

**Technology Detection Logic**: Instruction files are generated based on repository analysis:

```python
# Instruction file detection patterns in scripts/workspace/generator.py
instruction_patterns = {
    'markdown.instructions.md': {
        'patterns': ['**/*.md', '**/*.MD', '**/*.markdown'],
        'display_name': '📝 Markdown Instructions',
        'purpose': 'Markdown writing standards, formatting guidelines, and documentation quality assurance'
    },
    'python.instructions.md': {
        'patterns': ['**/*.py', '**/*.pyw', '**/*.pyi', '**/pyproject.toml', '**/requirements*.txt'],
        'display_name': '🐍 Python Instructions', 
        'purpose': 'Python development guidelines, script architecture, testing standards, virtual environment management'
    },
    'go.instructions.md': {
        'patterns': ['backend/**/*.go', 'go.mod', 'go.sum'],
        'display_name': '🔧 Go Instructions',
        'purpose': 'Go development guidelines, project structure, testing standards, dependency management'
    },
    'typescript.instructions.md': {
        'patterns': ['frontend/**/*.ts', 'frontend/**/*.tsx', 'frontend/**/*.json', 'frontend/**/*.js', 'frontend/**/*.jsx'],
        'display_name': '⚛️ TypeScript Instructions',
        'purpose': 'TypeScript/JavaScript development, component architecture, build configuration, package management'
    },
    'github.instructions.md': {
        'patterns': ['.github/**/*.yml', '.github/**/*.yaml', '.github/**/*.md', '**/workflow/**/*', '.github/ISSUE_TEMPLATE/*', '.github/PULL_REQUEST_TEMPLATE/*'],
        'display_name': '🔄 GitHub Instructions',
        'purpose': 'GitHub Actions workflows, repository configuration, issue templates, security practices'
    },
    'scripts.instructions.md': {
        'patterns': ['scripts/**/*.ps1', 'scripts/**/*.sh', 'scripts/**/*.sql'],
        'display_name': '🛠️ Scripts Instructions',
        'purpose': 'Script development standards, cross-platform compatibility, parameter conventions, output formatting'
    },
    'powershell.instructions.md': {
        'patterns': ['scripts/**/*.ps1'],
        'display_name': '📜 PowerShell Instructions',
        'purpose': 'PowerShell-specific standards, CmdletBinding patterns, Windows development'
    },
    'shell.instructions.md': {
        'patterns': ['scripts/**/*.sh'],
        'display_name': '🐚 Shell Instructions', 
        'purpose': 'Shell-specific standards, POSIX compliance, Unix/Linux development'
    },
    'terraform.instructions.md': {
        'patterns': ['**/*.tf', '**/*.hcl', '**/terraform.tf', '**/variables.tf', '**/outputs.tf', '**/locals.tf'],
        'display_name': '🏗️ Terraform Instructions',
        'purpose': 'Terraform development guidelines, IaC best practices, module conventions'
    },
    'jinja2.instructions.md': {
        'patterns': ['**/*.j2', '**/*.jinja', '**/*.jinja2', 'templates/**/*'],
        'display_name': '🎨 Jinja2 Instructions',
        'purpose': 'Jinja2 template development standards, formatting best practices, custom functions, template quality assurance'
    },
    'json.instructions.md': {
        'patterns': ['**/*.json', '**/*.jsonc', '**/*.json5'],
        'display_name': '📊 JSON Instructions',
        'purpose': 'JSON development standards, configuration management, API design, schema validation'
    },
    'yaml.instructions.md': {
        'patterns': ['**/*.yaml', '**/*.yml', '**/*.yaml.j2', '**/*.yml.j2'],
        'display_name': '📄 YAML Instructions',
        'purpose': 'YAML configuration standards, cloud platforms, security, validation, performance optimization'
    },
    'sql.instructions.md': {
        'patterns': ['**/*.sql', '**/migrations/*.sql', '**/schema/*.sql', '**/seeds/*.sql', '**/procedures/*.sql', '**/functions/*.sql', '**/triggers/*.sql', '**/views/*.sql'],
        'display_name': '🗄️ SQL Instructions',
        'purpose': 'Database development standards, query optimization, security, migrations, testing'
    },
    'azuredevops.instructions.md': {
        'patterns': ['**/*'],  # Universal patterns, activated by platform detection
        'display_name': '☁️ Azure DevOps Instructions',
        'purpose': 'CI/CD pipeline configuration, build strategies, work item integration, release management'
    },
    'gcp.instructions.md': {
        'patterns': ['**/*'],  # Universal patterns, activated by platform detection  
        'display_name': '☁️ GCP Instructions',
        'purpose': 'Google Cloud Platform guidelines, resource organization, IAM best practices, service integration'
    },
    'vscode.instructions.md': {
        'patterns': ['.vscode/**/*'],
        'display_name': '💻 VSCode Instructions',
        'purpose': 'VS Code workspace configuration, task automation, debugging, extension recommendations'
    }
}

def detect_required_instructions(repository_path):
    """Detect which instruction files are needed based on repository analysis."""
    detected_instructions = []
    
    for instruction_file, config in instruction_patterns.items():
        patterns = config['patterns']
        
        # Check if any pattern matches files in repository
        for pattern in patterns:
            if glob.glob(os.path.join(repository_path, pattern)):
                detected_instructions.append({
                    'filename': instruction_file,
                    'display_name': config['display_name'],
                    'purpose': config['purpose'],
                    'file_patterns': patterns
                })
                break  # Found match, move to next instruction file
                
    return detected_instructions
```

**Dynamic Instruction Generation**: Only detected technologies generate corresponding instruction files, ensuring clean and relevant AI agent guidance without unnecessary instruction clutter.

#### Instruction Template Implementation

**J2 Template Structure**: Each instruction file becomes a J2 template in `templates/.github/instructions/`:

```jinja2
{# templates/.github/instructions/python.instructions.md.j2 #}
---
applyTo: "{{ python_patterns | join(',') }}"
---
# Python Development Standards and Guidelines

This document provides comprehensive guidelines for Python development in {{ repository.name }}.

{% if repository.has_backend %}
## Backend Development
[Backend-specific Python guidelines]
{% endif %}

{% if repository.has_scripts %}
## Script Development  
[Script-specific Python guidelines]
{% endif %}

{% if repository.languages | length > 1 %}
## Multi-Language Integration
[Guidelines for Python integration with {{ repository.languages | reject('equalto', 'python') | join(', ') }}]
{% endif %}

{# Dynamic cross-references to other detected instruction files #}
## Related Documentation
{% for instruction in detected_instructions %}
{% if instruction.filename != 'python.instructions.md' %}
- **{{ instruction.display_name }}**: [{{ instruction.filename }}]({{ instruction.filename }})
{% endif %}
{% endfor %}
```

**Template Context Variables**:
- `repository`: Repository metadata (name, languages, types, features)
- `detected_instructions`: List of other instruction files being generated
- `language_patterns`: File patterns for the specific language
- `project_structure`: Directory structure and organization patterns

#### Cross-Reference Table Automation

**Dynamic Table Generation**: The `copilot-instructions.md` cross-reference table is automatically generated based on detected instruction files:

```jinja2
| Instruction File | File Pattern | Purpose |
| ---------------- | ------------ | ------- |
{% for instruction in detected_instructions %}
| [{{ instruction.display_name }}](instructions/{{ instruction.filename }}) | {{ instruction.file_patterns | join(', ') }} | {{ instruction.purpose }} |
{% endfor %}
```

**Integration Points**:
- **Repository Detection**: Coordinate with language template detection for consistent technology identification
- **File Pattern Matching**: Align with language template file associations for unified detection logic
- **Documentation Consistency**: Ensure instruction file purposes align with language template descriptions

#### Instruction Template Development Standards

**Template Coordination Requirements**:
1. **Consistent Structure**: All instruction templates follow established organization patterns
2. **YAML Frontmatter**: Standardized `applyTo` patterns matching detection logic
3. **Cross-Reference Integration**: Dynamic links to related instruction files and components
4. **Content Synchronization**: Instruction content aligns with language template configurations
5. **Template Quality**: Follow comprehensive Jinja2 development standards

**Template Update Process**:
1. **Detection Logic Update**: Modify `instruction_patterns` for new technology support
2. **Template Creation**: Create new instruction template following established patterns
3. **Cross-Reference Integration**: Update dynamic table generation to include new instruction
4. **Testing**: Validate instruction generation across different repository types
5. **Documentation**: Update coordination requirements and agent responsibilities

#### Dual-System Maintenance Coordination

**Integrated Maintenance Checklist**:
- [ ] Language template enhancements coordinate with instruction file updates
- [ ] Instruction file detection aligns with language template detection patterns  
- [ ] Cross-reference table generation includes all detected instruction files
- [ ] Template development standards apply to both language and instruction templates
- [ ] Documentation updates reflect changes in both coordination systems
- [ ] Testing validates both language template and instruction file generation
- [ ] Schema compliance maintained across both template systems

**Cross-System Dependencies**:
- **Shared Detection Logic**: Technology identification used by both systems
- **Consistent File Patterns**: Alignment between language templates and instruction files
- **Coordinated Updates**: Changes to detection logic affect both systems
- **Unified Testing**: Validation covers both language and instruction template generation
- **Documentation Synchronization**: Updates to either system require coordination documentation updates

## New Language Template Implementation ✅

### Jinja2 (J2) Language Support
**Implementation**: Created complete `templates/languages/j2.yaml.j2` template following established patterns.

**Features Added**:
- File associations: `.j2`, `.jinja`, `.jinja2` extensions
- Required extension: `wholroyd.jinja` 
- VS Code settings for Jinja2 formatting and linting
- Template validation and rendering tasks
- Automatic template repository type detection

**Repository Detection Logic**:
- J2 files automatically detected and added to languages
- Repositories with J2 files automatically get `template` type
- Integration with existing language detection patterns

### Terraform Template Enhancement ✅
**Enhancement**: Extended terraform language template to support `.tftpl` files.

**Features Added**:
- Added `*.tftpl` file association to terraform language
- Automatic detection of terraform template files
- When `.tftpl` files found, repository gets both `infra` and `template` types
- Maintains existing terraform functionality for `.tf`, `.tfvars`, `.hcl`

**Schema Updates**:
- Added `j2` to supported languages enum in `schemas/languages.yaml`
- Added `j2` language pattern to detection logic in `scripts/workspace/generator.py`
- Enhanced repository type detection with template-specific logic

### TypeScript Instruction Template Enhancement ✅ [NEW]

**Enhancement**: Implemented comprehensive TypeScript instruction template for Node.js and frontend development:

**Implementation Details**:
- Created `templates/.github/instructions/typescript.instructions.md.j2` with complete TypeScript development guidelines
- Added TypeScript detection patterns: `['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx', '**/package.json', '**/tsconfig.json']`
- Integrated React component patterns, service layer architecture, and comprehensive testing standards

**Template Features**:
- **Architecture Guidelines**: Project structure, component organization, service layer patterns
- **Implementation Standards**: TypeScript configuration, React patterns, API client implementation
- **Quality Assurance**: Jest testing setup, ESLint/Prettier configuration, code coverage requirements
- **Development Workflow**: Build processes, hot-reload development, production optimization

**Generated Content**:
- TypeScript-specific development patterns and best practices
- React component templates with proper typing
- Service layer implementation with dependency injection
- Comprehensive testing strategies for TypeScript projects
- Build configuration and deployment guidelines

**Schema Updates**:
- Added `typescript` to supported languages enum in `schemas/repository.yaml`
- Enhanced language detection logic with comprehensive JavaScript/TypeScript file patterns
- Integrated Node.js ecosystem tooling detection (package.json, tsconfig.json)

## Resolved Issues

### Template Implementation Success ✅

**Resolved Issues**: The `templates/.omd/languages.yaml.j2` template now generates populated structures using custom YAML-style JSON formatting with real configuration data extracted from enhanced templates:

```yaml
languages:
  python:
    # Source: templates/languages/python.yaml.j2 (4 settings, 2 tasks)
    settings:
      {
        "[python]": {
          "editor.formatOnSave": true,
          "editor.defaultFormatter": "ms-python.python",
          "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit",
          },
        },
        "python.defaultInterpreterPath": "./venv/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
      }
    required_extensions:
      [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.vscode-pylance",
        "ms-python.isort",
      ]
```

For complete implementation details, formatting standards, and troubleshooting guides, see [Jinja2 Instructions](.github/instructions/jinja2.instructions.md).

## Change Coordination Requirements

### Cross-Component Impact Assessment
When making changes to any MyRepos component:

- **Component Dependencies**: Consider how changes affect workspace generation, validation, and template rendering
- **Platform Compatibility**: Ensure changes work consistently across GitHub, Azure DevOps, and local development
- **Language Integration**: Verify changes don't break existing language configurations
- **Schema Compliance**: Maintain validation compliance throughout the change process
- **AI Integration**: Update instruction files to reflect new patterns or capabilities

### Documentation Maintenance Standards

- **AGENTS.md**: Update component status, coordination requirements, and implementation tracking
- **copilot-instructions.md**: Update project overview and instruction file references for functional changes
- **Instruction Files**: Update technology-specific guidance for relevant changes
- **docs/ Files**: Update technical documentation for system architecture or process changes
- **Schema Files**: Update JSON schemas for any configuration structure changes
- **Templates**: Update template comments and documentation for template modifications

### Coordination Workflow

1. **Assessment**: Evaluate cross-component impact of proposed changes
2. **Planning**: Update relevant instruction files and documentation
3. **Implementation**: Make changes while maintaining cross-platform compatibility
4. **Validation**: Test changes across all supported platforms and languages
5. **Documentation**: Update this coordination document to reflect new patterns
6. **AI Integration**: Ensure instruction files provide appropriate guidance for AI agents

This comprehensive coordination system ensures that MyRepos maintains consistency, quality, and AI-assisted development capabilities across all components and platforms.

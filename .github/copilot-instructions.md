---
applyTo: "**"
---

# GitHub Copilot Instructions

## 🏗️ Project Overview

MyRepos Tools is a comprehensive Python-based repository management system designed for managing multiple Git repositories with VS Code workspace generation, schema-based configuration, and automated setup. The platform provides unified tooling for workspace configuration, language-specific template generation, and cross-platform development environment management.

### Core Architecture Philosophy

MyRepos treats every repository as an individual workspace while preserving organizational hierarchies and cross-repository relationships. Key architectural principles:

- **Template-Based Generation**: Each workspace generated from Jinja2 templates with language-specific configurations
- **Schema Validation**: Repository structure maintained through JSON schema validation
- **Multi-Language Native**: Simultaneous support for 10+ programming languages with specialized configurations  
- **Extensible Templates**: Support for custom templates beyond predefined language structures
- **Cross-Platform Compatibility**: Unified tooling for Windows, Linux, and macOS environments
- **AI Integration**: Comprehensive instruction files for intelligent development assistance

## 📚 Instruction Files Reference

This project uses modular instruction files for platform-specific development guidelines. Each file contains targeted guidance for specific components or technologies:

### Instruction Standards

The MyRepos project follows a hierarchical documentation architecture designed for AI agent navigation and comprehensive development guidance:

```
AGENTS.md (root)                     ← Master tracking & component coordination
├── .github/copilot-instructions.md  ← GitHub Copilot project context (this file)
├── .github/instructions/*.md        ← Technology-specific development standards
└── docs/*.md                        ← Component-specific documentation
```

#### Documentation Hierarchy Purpose

- **[Root AGENTS.md](../AGENTS.md)**: Master project tracking, component status overview, cross-component coordination
- **copilot-instructions.md** (this file): GitHub Copilot context and instruction file navigation
- **\*.instructions.md**: Technology-specific development standards and implementation patterns
- **docs/\*.md**: Detailed documentation for specific systems and processes

#### AI Agent Navigation Pattern

1. **Start Here**: copilot-instructions.md provides project context and instruction file overview
2. **Technology Guidance**: Use appropriate \*.instructions.md for specific development tasks
3. **Component Tracking**: Reference relevant component documentation for detailed status and roadmaps
4. **Cross-Reference**: AGENTS.md files and instruction files cross-reference for comprehensive guidance

### Core Instruction Files

| Instruction File | File Pattern | Purpose |
|------------------|--------------|---------|
| [📝 Markdown Instructions](instructions/markdown.instructions.md) | `**/*.md`, `**/*.MD`, `**/*.markdown`, `/*.md`, `/*.MD`, `/*.markdown` | Markdown writing standards, formatting guidelines, and documentation quality assurance |
| [🐍 Python Instructions](instructions/python.instructions.md) | `**/*.py`, `**/*.pyw`, `**/*.pyi`, `**/setup.py`, `**/setup.cfg`, `**/pyproject.toml`, `**/.python-version`, `**/requirements*.txt`, `**/Pipfile`, `**/poetry.lock` | Python development guidelines, script architecture, testing standards, virtual environment management |
| [🔧 Go Instructions](instructions/go.instructions.md) | `backend/**/*.go`, `go.mod`, `go.sum` | Go development guidelines, project structure, testing standards, dependency management |
| [⚛️ TypeScript Instructions](instructions/typescript.instructions.md) | `frontend/**/*.ts`, `frontend/**/*.tsx`, `frontend/**/*.json`, `frontend/**/*.js`, `frontend/**/*.jsx` | TypeScript/JavaScript development, component architecture, build configuration, package management |
| [🔄 GitHub Instructions](instructions/github.instructions.md) | `.github/**/*.yml`, `.github/**/*.yaml`, `.github/**/*.md`, `**/workflow/**/*`, `.github/ISSUE_TEMPLATE/*`, `.github/PULL_REQUEST_TEMPLATE/*` | GitHub Actions workflows, repository configuration, issue templates, security practices |
| [🛠️ Scripts Instructions](instructions/scripts.instructions.md) | `scripts/**/*.ps1`, `scripts/**/*.sh`, `scripts/**/*.sql` | Script development standards, cross-platform compatibility, parameter conventions, output formatting |
| [📜 PowerShell Instructions](instructions/powershell.instructions.md) | `scripts/**/*.ps1` | PowerShell-specific standards, CmdletBinding patterns, Windows development |
| [🐚 Shell Instructions](instructions/shell.instructions.md) | `scripts/**/*.sh` | Shell-specific standards, POSIX compliance, Unix/Linux development |
| [🏗️ Terraform Instructions](instructions/terraform.instructions.md) | `**/*.tf`, `**/*.hcl`, `**/terraform.tf`, `**/variables.tf`, `**/outputs.tf`, `**/locals.tf` | Terraform development guidelines, IaC best practices, module conventions |
| [🎨 Jinja2 Instructions](instructions/jinja2.instructions.md) | `**/*.j2`, `**/*.jinja`, `**/*.jinja2`, `templates/**/*` | Jinja2 template development standards, formatting best practices, custom functions, template quality assurance |
| [📊 JSON Instructions](instructions/json.instructions.md) | `**/*.json`, `**/*.jsonc`, `**/*.json5` | JSON development standards, configuration management, API design, schema validation |
| [📄 YAML Instructions](instructions/yaml.instructions.md) | `**/*.yaml`, `**/*.yml`, `**/*.yaml.j2`, `**/*.yml.j2` | YAML configuration standards, cloud platforms, security, validation, performance optimization |
| [🗄️ SQL Instructions](instructions/sql.instructions.md) | `**/*.sql`, `**/migrations/*.sql`, `**/schema/*.sql`, `**/seeds/*.sql`, `**/procedures/*.sql`, `**/functions/*.sql`, `**/triggers/*.sql`, `**/views/*.sql` | Database development standards, query optimization, security, migrations, testing |
| [☁️ Azure DevOps Instructions](instructions/azuredevops.instructions.md) | `**/*` | CI/CD pipeline configuration, build strategies, work item integration, release management |
| [☁️ GCP Instructions](instructions/gcp.instructions.md) | `**/*` | Google Cloud Platform guidelines, resource organization, IAM best practices, service integration |
| [💻 VSCode Instructions](instructions/vscode.instructions.md) | `.vscode/**/*` | VS Code workspace configuration, task automation, debugging, extension recommendations |

### When to Use Each Instruction File

- **Markdown Instructions**: When creating or editing documentation, README files, or any markdown content
- **Python Instructions**: When working on setup scripts, workspace generators, validation tools, or any Python development
- **TypeScript Instructions**: When developing frontend applications, build configurations, or Node.js tooling
- **GitHub Workflow Instructions**: When setting up CI/CD pipelines, configuring repository settings, or managing collaborative workflows
- **Scripts Instructions**: When creating or modifying build scripts, development automation, cross-platform scripts, or deployment automation
- **PowerShell Instructions**: When developing PowerShell scripts specifically, working with Windows-specific features, or dealing with CmdletBinding patterns
- **Shell Instructions**: When developing shell scripts specifically, working with Unix/Linux environments, or ensuring POSIX compliance
- **Terraform Instructions**: When working with Infrastructure as Code, Terraform modules, or cloud resource management
- **Jinja2 Instructions**: When creating or modifying Jinja2 templates, working with template formatting, implementing custom functions, or ensuring template quality standards
- **JSON Instructions**: When working with JSON configuration files, API design, schema validation, or data formatting
- **YAML Instructions**: When working with YAML configuration files, cloud platforms, CI/CD configurations, or Kubernetes manifests
- **SQL Instructions**: When working with database design, query optimization, migrations, stored procedures, or database testing
- **Azure DevOps Instructions**: When configuring CI/CD pipelines, Azure DevOps integration, or DevOps workflows
- **GCP Instructions**: When working with Google Cloud Platform resources, IAM policies, or GCP-specific integrations
- **VS Code Instructions**: When configuring development environment, setting up debugging, managing tasks, or optimizing workspace settings

### Cross-Reference Guidelines

These instruction files work together to provide comprehensive development guidance:

1. **Documentation Standards**: All technical writing should follow the markdown instructions
2. **Full-Stack Development**: Python and TypeScript instructions complement each other for complete tooling development
3. **Configuration Management**: JSON and YAML instructions provide standards for configuration files across all platforms
4. **Data Management**: SQL instructions support database design and optimization across all application tiers
5. **DevOps Integration**: GitHub workflow and Azure DevOps instructions support the development processes defined in platform-specific files
6. **Scripts & Automation**: Scripts instructions provide standards for build automation, development workflows, and cross-platform compatibility
7. **Development Environment**: VS Code instructions provide workspace optimization and task automation for efficient development
8. **Quality Assurance**: Each instruction file includes testing and quality standards appropriate to its domain

## 📂 Repository Structure

```
myrepos/
├── .github/                          # GitHub configuration and workflows
│   ├── instructions/                 # Technology-specific development guidelines
│   │   ├── markdown.instructions.md  # Markdown development standards
│   │   ├── python.instructions.md   # Python development standards
│   │   ├── go.instructions.md       # Go development standards
│   │   ├── typescript.instructions.md # TypeScript/JavaScript standards
│   │   ├── github.instructions.md   # GitHub workflow and CI/CD guidelines
│   │   ├── scripts.instructions.md  # Script development and automation standards
│   │   ├── powershell.instructions.md # PowerShell-specific development standards
│   │   ├── shell.instructions.md    # Shell-specific development standards
│   │   ├── terraform.instructions.md # Terraform/IaC development standards
│   │   ├── jinja2.instructions.md   # Jinja2 template development standards
│   │   ├── json.instructions.md     # JSON development standards
│   │   ├── yaml.instructions.md     # YAML configuration standards
│   │   ├── sql.instructions.md      # SQL database development standards
│   │   ├── azuredevops.instructions.md # Azure DevOps integration standards
│   │   ├── gcp.instructions.md      # Google Cloud Platform guidelines
│   │   └── vscode.instructions.md   # VS Code workspace configuration
│   └── copilot-instructions.md      # GitHub Copilot project context (this file)
│
├── .vscode/                          # VS Code workspace configuration (generated)
│   ├── tasks.json                   # Task automation (build, test, lint)
│   ├── settings.json                # Editor and language settings
│   └── extensions.json              # Recommended extensions
│
├── scripts/                          # Python tooling and automation
│   ├── setup-repository.py          # Main repository setup script
│   ├── setup.sh                     # Unix/Linux setup wrapper
│   ├── setup.ps1                    # Windows PowerShell setup wrapper
│   ├── workspace/                   # Workspace generation modules
│   │   ├── generator.py             # Main workspace generator
│   │   ├── detection.py             # Repository detection logic
│   │   ├── config.py                # Configuration management
│   │   └── templates.py             # Template context and utilities
│   └── validation/                  # Configuration validation
│       └── validator.py             # JSON schema validation
│
├── templates/                        # Jinja2 template system
│   ├── languages/                   # Enhanced language configurations
│   │   ├── python.yaml.j2           # Complete Python configuration
│   │   ├── go.yaml.j2               # Complete Go configuration
│   │   ├── typescript.yaml.j2       # Complete TypeScript configuration
│   │   ├── terraform.yaml.j2        # Complete Terraform configuration
│   │   ├── markdown.yaml.j2         # Complete Markdown configuration
│   │   ├── powershell.yaml.j2       # Complete PowerShell configuration
│   │   ├── shell.yaml.j2            # Complete Bash/Shell configuration
│   │   ├── j2.yaml.j2               # Complete Jinja2 template configuration
│   │   ├── json.yaml.j2             # Complete JSON configuration
│   │   ├── yaml.yaml.j2             # Complete YAML configuration
│   │   └── sql.yaml.j2              # Complete SQL configuration
│   ├── .vscode/                     # VS Code template files
│   │   ├── settings.json.j2         # Settings template with platform configs
│   │   ├── extensions.json.j2       # Extensions template with platform configs
│   │   ├── launch.json.j2           # Launch configurations template
│   │   └── tasks.json.j2            # Tasks template
│   ├── .omd/                        # Metadata templates
│   │   └── languages.yaml.j2        # Language summary template
│   ├── .azuredevops/               # Azure DevOps templates
│   │   └── pull_request_template/   # PR template generation
│   └── {{ repo_name }}.code-workspace.j2 # VS Code workspace template
│
├── schemas/                          # JSON schema definitions
│   ├── repository.yaml              # Repository metadata schema
│   ├── languages.yaml               # Language configuration schema
│   ├── platform.yaml                # Platform configuration schema
│   └── workspace.yaml               # Workspace schema
│
├── docs/                            # Project documentation
│   ├── template-system.md           # Template system documentation
│   └── detection-and-configuration.md # Configuration detection guide
│
├── requirements.txt                 # Python dependencies
├── myrepos.code-workspace          # VS Code workspace configuration
├── AGENTS.md                       # Master project tracking and coordination
└── README.md                       # Project overview and usage guide
```

## 🎯 Development Guidelines

For detailed platform-specific coding guidelines, please refer to the appropriate instruction files:

- **Python Development**: See [Python Instructions](instructions/python.instructions.md) for script architecture, virtual environment management, and testing standards
- **Template Development**: See [AGENTS.md](../AGENTS.md) for template formatting and best practices
- **Documentation**: See [Markdown Instructions](instructions/markdown.instructions.md) for writing standards and formatting guidelines
- **Configuration Management**: See [JSON Instructions](instructions/json.instructions.md) and [YAML Instructions](instructions/yaml.instructions.md) for configuration file standards
- **Database Development**: See [SQL Instructions](instructions/sql.instructions.md) for database design, optimization, and migration strategies
- **CI/CD & Repository Management**: See [GitHub Workflow Instructions](instructions/github.instructions.md) for workflow automation and collaboration processes
- **Scripts & Automation**: See [Scripts Instructions](instructions/scripts.instructions.md) for build automation, development workflows, and cross-platform script development

### General Development Principles

- **Template-Driven Architecture**: Follow template-based configuration pattern for workspace generation
- **Schema Validation**: Ensure all generated configurations validate against JSON schemas
- **Cross-Platform Compatibility**: Write code that works consistently across Windows, Linux, and macOS
- **Language-Specific Optimization**: Leverage language-specific templates for optimal VS Code integration
- **Modular Design**: Use modular architecture for generator, detection, config, and template components
- **Documentation Standards**: Maintain comprehensive documentation with examples and best practices
- **Quality Assurance**: Include validation, testing, and quality checks in all development processes
- **AI Integration**: Provide comprehensive instruction files for intelligent development assistance

## 🔧 Development Workflow

For detailed script development guidelines including cross-platform compatibility, parameter standards, and automation best practices, see [Scripts Instructions](instructions/scripts.instructions.md).

### Cross-Platform Development Commands

MyRepos provides comprehensive workspace generation and validation through Python-based scripts that work across Windows, Linux, and macOS:

#### Unix/Linux/macOS (Bash)

```bash
# Setup repository with workspace generation
python3 scripts/setup-repository.py /path/to/repository

# Setup with validation only
python3 scripts/setup-repository.py --validate /path/to/repository

# Cross-platform setup wrapper
./scripts/setup.sh /path/to/repository
```

#### Windows (PowerShell)

```powershell
# Setup repository with workspace generation
python scripts/setup-repository.py C:\path\to\repository

# Setup with validation only
python scripts/setup-repository.py --validate C:\path\to\repository

# Cross-platform setup wrapper
.\scripts\setup.ps1 C:\path\to\repository
```

### Template Development Standards

All templates in the MyRepos project follow comprehensive standards for cross-platform compatibility, consistent configuration interfaces, and maintainable template structures. For detailed guidelines on:

- **Language Templates**: Enhanced YAML configurations with complete VS Code integration
- **Jinja2 Patterns**: Template inheritance, formatting, and best practices
- **Schema Compliance**: Validation requirements and structure standards
- **Cross-Platform Generation**: Template compatibility across operating systems

See [AGENTS.md](../AGENTS.md) for complete template development guidelines and coordination requirements.

### Testing Guidelines

- Write validation tests for all template generations
- Create integration tests for workspace generation workflows
- Use test fixtures for consistent repository structures
- Mock external dependencies (file systems, VS Code extensions)
- Utilize comprehensive validation suites for different repository types
- Generate validation reports to track template effectiveness
- Support cross-platform testing on Windows, Linux, and macOS

#### Test Suite Organization

- **templates**: Template generation and Jinja2 rendering tests
- **validation**: Schema validation and compliance tests  
- **detection**: Repository language and platform detection tests
- **integration**: End-to-end workspace generation tests
- **schemas**: JSON schema validation and structure tests
- **all**: Complete test suite (default)

## 🌐 Multi-Language Integration

### Language Template Pattern

```python
class LanguageConfig:
    def __init__(self, language_name: str):
        self.name = language_name
        self.file_associations = []
        self.settings = {}
        self.required_extensions = []
        self.recommended_extensions = []
        self.tasks = []
        self.launch_configurations = []
        self.linting = {}
        
    def to_vscode_config(self) -> dict:
        """Convert to VS Code configuration format"""
        pass
        
    def validate_schema(self) -> bool:
        """Validate against language schema"""
        pass

# Supported languages with full template integration
supported_languages = {
    'python': PythonConfig,
    'go': GoConfig, 
    'typescript': TypeScriptConfig,
    'terraform': TerraformConfig,
    'markdown': MarkdownConfig,
    'powershell': PowerShellConfig,
    'shell': ShellConfig,
    'j2': Jinja2Config,
    'json': JsonConfig,
    'yaml': YamlConfig,
    'sql': SqlConfig
}
```

### Repository Detection

- Use consistent language detection patterns across repository types
- Implement platform-specific detection (GitHub, Azure DevOps, GitLab)
- Support cross-language relationships and dependencies
- Enable repository type inference through file patterns
- Preserve repository structure while adding enhanced configurations

## 🔍 Schema Design Patterns

### Repository Metadata Structure

```yaml
# .omd/repository.yaml - Generated repository metadata
repository:
  name: "example-repo"
  platform: "github"  # or "azuredevops"
  languages:
    - "python"
    - "markdown"
  types:
    - "tooling"
    - "template"
  detected_features:
    has_tests: true
    has_docs: true
    has_ci: true
```

### Language Configuration Schema

```yaml
# Generated from templates/languages/{language}.yaml.j2
languages:
  python:
    settings:
      "[python]":
        "editor.formatOnSave": true
        "editor.defaultFormatter": "ms-python.python"
    required_extensions:
      - "ms-python.python" 
      - "ms-python.black-formatter"
    tasks:
      - label: "Python: Run Tests"
        type: "shell"
        command: "python -m pytest"
```

## 🚀 Deployment Considerations

### Repository Setup Deployment

- Support automated repository initialization across platforms
- Generate workspace configurations that work immediately after clone
- Implement cross-platform setup scripts for environment preparation  
- Provide Docker containers for consistent development environments

### Security Best Practices

- Validate all template inputs and generated configurations
- Use safe YAML loading to prevent code injection
- Implement proper file path validation for cross-platform security
- Sanitize repository names and paths in generated configurations
- Secure template rendering against malicious input

## 🧪 When Suggesting Code

### For Python Script Changes

- Consider cross-platform file path handling using `pathlib`
- Ensure virtual environment compatibility across operating systems
- Add appropriate error handling for file system operations
- Consider template rendering performance and memory usage
- Think about schema validation and user feedback

### For Template Changes

- Ensure Jinja2 templates render correctly across platforms
- Consider VS Code configuration compatibility
- Think about language-specific requirements and constraints
- Ensure generated JSON/YAML is properly formatted
- Consider template inheritance and reusability patterns

### For Schema Changes  

- Maintain backward compatibility when possible
- Update documentation and examples for schema changes
- Consider validation error messages and user experience
- Think about schema versioning for breaking changes
- Ensure proper JSON Schema validation rules

## 🎨 Template Design Guidelines

### Design Principles

- Clean and consistent template structure across languages
- Modular template design that supports inheritance
- Comprehensive language support with sensible defaults
- Cross-platform compatibility in all generated configurations
- Extensible design following established patterns

### Template Patterns

- Create reusable template components for common configurations
- Use consistent variable naming across template files
- Implement proper error handling and validation in templates
- Support both simple and complex configuration scenarios
- Provide comprehensive examples and documentation

## 📋 Primary Development Rules

### Always Update the Complete Stack

When making any changes to the MyRepos system:

1. **Template Updates**: Update enhanced language templates in `templates/languages/`
2. **Schema Validation**: Ensure changes comply with JSON schemas in `schemas/`
3. **Documentation Updates**: Update `README.md`, `AGENTS.md`, and relevant `docs/` files
4. **Instruction Files**: Update relevant `.github/instructions/*.md` files for technology-specific guidance
5. **Cross-Platform Testing**: Validate changes work across Windows, Linux, and macOS
6. **Template Generation**: Regenerate workspace configurations using updated templates
7. **Validation**: Run full schema validation to ensure consistency

### Documentation Maintenance Standards

- **README.md**: Update project overview, features, and usage examples for any functional changes
- **AGENTS.md**: Update component status, coordination requirements, and implementation tracking
- **docs/**: Update technical documentation for system architecture or process changes
- **Instruction Files**: Update technology-specific guidance for relevant changes
- **Schema Files**: Update JSON schemas for any configuration structure changes
- **Templates**: Update template comments and documentation for template modifications

### Change Coordination Requirements

- **Cross-Component Impact**: Consider how changes affect workspace generation, validation, and template rendering
- **Platform Compatibility**: Ensure changes work consistently across GitHub, Azure DevOps, and local development
- **Language Integration**: Verify changes don't break existing language configurations
- **Schema Compliance**: Maintain validation compliance throughout the change process
- **AI Integration**: Update instruction files to reflect new patterns or capabilities

This comprehensive instruction system ensures that GitHub Copilot understands the MyRepos project structure, development patterns, and coordination requirements to provide contextually appropriate suggestions for this repository management and workspace generation platform.

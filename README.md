# MyRepos Tools

A comprehensive toolset for managing multiple Git repositories with VS Code workspace generation, schema-based configuration, and automated setup.

## Overview

This toolkit provides Python-based tools to enhance the [myrepos](https://myrepos.branchable.com/) workflow by:

- 🏗️ **Generating VS Code workspace files** with language-specific configurations
- 📋 **Schema-based repository configuration** for consistent metadata management
- 🤖 **Automated Copilot instructions** generation for different repository types
- 🔧 **Cross-platform setup scripts** for repository initialization
- ✅ **Configuration validation** to ensure consistency across repositories

## Repository Structure

```
myrepos/
├── scripts/                          # Python setup and generation scripts
│   ├── setup-workspace.py           # Main workspace generator
│   ├── generate-copilot-instructions.py # Copilot instructions generator  
│   ├── setup-repository.py          # Repository initialization
│   └── validate-schemas.py          # Configuration validation
├── schemas/                          # YAML schemas for configuration
│   ├── repository.yaml              # Base repository metadata schema
│   ├── language.yaml                # Language-specific configuration schema
│   ├── platform.yaml                # CI/CD platform configuration schema
│   ├── workspace.yaml               # VS Code workspace configuration schema
│   ├── index.yaml                   # Schema relationships and validation rules
│   └── README.md                    # Schema documentation
├── templates/                        # Template files
│   └── repository.yaml              # Default repository metadata template
├── requirements.txt                  # Python dependencies
└── README.md                        # This file
```

## Features

### 🏗️ Workspace Generation

- **Language-aware configurations**: Automatic VS Code settings for 25+ programming languages
- **Extension management**: Smart extension recommendations based on repository content
- **Cross-platform compatibility**: Works on macOS, Linux, and Windows
- **Metadata-driven**: Uses explicit `.omd/repository.yaml` files for configuration

### 📋 Schema System

**Repository Types**: 13 flexible repository categories:
- `module`, `app`, `lib`, `infra`, `site`, `template`, `tool`, `config`, `data`, `docs`, `monorepo`, `example`, `experiment`

**Language Support**: 25+ languages including:
- Programming: Python, JavaScript, TypeScript, Go, Rust, Java, C#, etc.
- Configuration: YAML, JSON, Terraform, Dockerfile
- Documentation: Markdown with comprehensive formatting and linting
- Scripting: Shell, PowerShell

**Platform Integration**: GitHub, Azure DevOps, GitLab, Bitbucket, etc.

### 🤖 Copilot Instructions

Automatically generates repository-specific GitHub Copilot instructions:
- Language-specific coding standards and best practices
- Documentation writing guidelines for Markdown
- Platform-specific workflow instructions
- Repository type-appropriate development patterns

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize a Repository

```bash
# Create repository metadata
python scripts/setup-repository.py /path/to/your/repo

# Edit the generated .omd/repository.yaml file to match your repository
```

### 3. Generate Workspace Configuration

```bash
# Generate VS Code workspace and settings
python scripts/setup-workspace.py /path/to/your/repo

# Generate Copilot instructions
python scripts/generate-copilot-instructions.py /path/to/your/repo
```

### 4. Validate Configuration

```bash
# Validate repository configuration against schemas
python scripts/validate-schemas.py --repository /path/to/your/repo
```

## Repository Configuration

### Basic Repository Metadata (`.omd/repository.yaml`)

```yaml
languages:
  - python
  - markdown
  - yaml
platform: github
repository_type: app
targets:
  - web
  - api
tags:
  - backend
  - microservice
```

### Language-Specific Configuration (`.omd/language.yaml`)

```yaml
languages:
  python:
    settings:
      "[python]":
        editor.formatOnSave: true
        editor.defaultFormatter: "ms-python.black-formatter"
    required_extensions:
      - "ms-python.python"
      - "ms-python.black-formatter"
```

## Integration with MyRepos

Add to your `.mrconfig`:

```ini
[DEFAULT]
setup = python ~/Data/Tools/myrepos/scripts/setup-repository.py "$MR_REPO"
workspace = python ~/Data/Tools/myrepos/scripts/setup-workspace.py "$MR_REPO"
copilot = python ~/Data/Tools/myrepos/scripts/generate-copilot-instructions.py "$MR_REPO"
validate = python ~/Data/Tools/myrepos/scripts/validate-schemas.py --repository "$MR_REPO"
```

Then use with myrepos:

```bash
# Set up all repositories
mr -j4 run setup

# Generate workspaces for all repositories  
mr -j4 run workspace

# Generate Copilot instructions
mr -j4 run copilot

# Validate all configurations
mr -j4 run validate
```

## Schema Validation

The schema system ensures consistency across repositories:

```bash
# Validate a single repository
python scripts/validate-schemas.py --repository /path/to/repo

# JSON output for automation
python scripts/validate-schemas.py --repository /path/to/repo --json-output
```

## Language-Specific Features

### Markdown Support
- Comprehensive documentation standards and formatting
- Automatic table of contents generation
- Linting with configurable rules
- GitHub Flavored Markdown preview

### Python Support
- Virtual environment detection
- Black formatting and import sorting
- Testing framework integration
- Type hint validation

### Terraform Support
- HCL formatting and validation
- Provider version constraints
- Cloud provider best practices
- Security scanning integration

### JavaScript/TypeScript Support
- ESLint and Prettier integration
- Package.json dependency management
- Testing framework setup
- Modern ES6+ standards

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Testing

```bash
# Run schema validation tests
python scripts/validate-schemas.py --schemas-dir schemas --repository ./test-repos/sample

# Test workspace generation
python scripts/setup-workspace.py ./test-repos/sample
```

## Requirements

- Python 3.7+
- PyYAML 6.0+
- Jinja2 3.0+
- jsonschema 4.0+
- VS Code (for workspace features)
- Git
- myrepos (optional, for batch operations)

## License

MIT License - see LICENSE file for details.

## Related Projects

- [myrepos](https://myrepos.branchable.com/) - Multiple repository management tool
- [VS Code](https://code.visualstudio.com/) - Code editor and workspace management
- [GitHub Copilot](https://github.com/features/copilot) - AI pair programming
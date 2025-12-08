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
│   ├── workspace/
│   │   └── generator.py              # Main workspace generator
│   └── validation/
│       └── validator.py              # Configuration validation
├── templates/                        # Jinja2 templates and configuration
│   ├── config/                       # YAML configuration files
│   │   ├── languages.yaml            # Language-specific configurations
│   │   ├── platforms.yaml            # Platform-specific configurations
│   │   └── clients.yaml              # Client-specific configurations
│   └── .vscode/                      # VS Code template files
│       ├── settings.json.j2          # Settings template
│       └── extensions.json.j2        # Extensions template
├── docs/                             # Documentation
│   └── TEMPLATE_SYSTEM.md            # Template system documentation
├── venv/                             # Python virtual environment
└── README.md                         # This file
```

## Features

### 🏗️ Workspace Generation

- **Template-driven configurations**: Jinja2 templates with YAML configuration files for flexible setup
- **Language-aware settings**: Comprehensive VS Code settings for 9 programming languages
- **Smart extension recommendations**: Auto-generated extension lists based on detected languages and platforms
- **Auto-detection capabilities**: Automatically detects languages, platforms, and repository types
- **Metadata-driven**: Uses `.omd/repository.yaml` files with auto-generation fallback

### 📋 Configuration System

**Repository Types**: Flexible repository categories:
- `app`, `lib`, `infra`, `site`, `docs`, and more

**Language Support**: 9 languages with comprehensive configurations:
- **Programming**: Python, Go, SQL
- **Configuration**: YAML, JSON, Terraform
- **Documentation**: Markdown with advanced formatting and linting
- **Scripting**: Shell, PowerShell

**Platform Integration**: GitHub, Azure DevOps with automatic CI/CD detection

**Template-Driven Architecture**: All configurations managed via YAML files and Jinja2 templates

### 🤖 Copilot Instructions

Generates repository-specific GitHub Copilot instructions when enabled:
- Language-specific coding standards and best practices
- Documentation writing guidelines for Markdown
- Platform-specific workflow instructions
- Repository type-appropriate development patterns

**Note**: Copilot instruction generation is optional and controlled by the `copilot_instructions` flag in repository metadata.

## Quick Start

### 1. Set Up Python Virtual Environment

**Quick Setup (Automated):**
```bash
# Use the setup script (recommended)
./scripts/setup.sh

# Or on Windows
.\scripts\setup.ps1
```

**Manual Setup:**
```bash
# Navigate to the myrepos directory
cd /Users/cuki/Data/Tools/myrepos

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
python3 -m pip install --upgrade pip

# Install required dependencies
pip install PyYAML jsonschema jinja2
```

**Troubleshooting:**
```bash
# If you get "ModuleNotFoundError: No module named 'jinja2'"
source venv/bin/activate
pip install jinja2

# Always activate the virtual environment before using the tools
source venv/bin/activate
```

### 2. Generate Workspace Configuration

```bash
# Complete repository setup with auto-detection
# This will auto-detect languages, platform, and repository types
python scripts/setup-repository.py /path/to/your/repo

# Works with both new repositories and existing .omd/repository.yaml metadata
python scripts/setup-repository.py /path/to/your/repo
```

### 3. Validate Configuration (Optional)

```bash
# Validate repository configuration against schemas
python scripts/validation/validator.py --repository /path/to/your/repo
```

## Repository Configuration

### Auto-Generated Repository Metadata (`.omd/repository.yaml`)

```yaml
# Auto-detected repository configuration
# Edit as needed and re-run setup

copilot_instructions: false
languages:
- markdown
- python
- yaml
platform: github
types:
- docs
```

### Template-Driven Configuration

Configurations are managed through YAML files in `templates/config/`:
- `languages.yaml`: Language-specific VS Code extensions and settings
- `platforms.yaml`: Platform-specific extensions (GitHub, Azure DevOps, etc.)
- `clients.yaml`: Client-specific customizations

These files are processed by Jinja2 templates to generate VS Code settings and extensions.

## Integration with MyRepos

Add to your `.mrconfig`:

```ini
[DEFAULT]
# Complete repository setup (with auto-detection and validation)
setup = python ~/Data/Tools/myrepos/scripts/setup-repository.py "$MR_REPO"

# Validate repository configuration only
validate = python ~/Data/Tools/myrepos/scripts/validation/validator.py --repository "$MR_REPO"
```

Then use with myrepos:

```bash
# Setup all repositories (with auto-detection and validation)
mr -j4 run setup

# Validate all configurations only
mr -j4 run validate
```

## Configuration Validation

The validation system ensures repository configurations are correct:

```bash
# Validate a single repository
python scripts/validation/validator.py --repository /path/to/repo

# JSON output for automation
python scripts/validation/validator.py --repository /path/to/repo --json-output

# Use with myrepos for all repositories
mr run validate
```

## Language-Specific Features

### Markdown Support
- Comprehensive formatting with yzhang.markdown-all-in-one
- Linting with DavidAnson.vscode-markdownlint
- Mermaid diagram support
- GitHub preview styles
- Configurable word wrap and formatting

### Python Support
- Black formatting (ms-python.black-formatter)
- Import sorting with isort
- Pylint integration
- Virtual environment path configuration
- Code actions on save

### Terraform Support
- HashiCorp Terraform extension
- Auto-formatting on save
- Validation on save
- HCL file associations

### YAML Support
- RedHat YAML extension
- Format on save
- Validation and hover support
- Proper indentation (2 spaces)

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
# Test complete setup on myrepos itself
python scripts/setup-repository.py /Users/cuki/Data/Tools/myrepos

# Test validation only
python scripts/validation/validator.py --repository /Users/cuki/Data/Tools/myrepos

# Test with a sample repository
python scripts/setup-repository.py /path/to/test/repo
```

## Requirements

- Python 3.7+
- PyYAML 6.0+
- Jinja2 3.0+
- jsonschema 4.0+
- VS Code (for workspace features)
- Git
- myrepos (optional, for batch operations)

### Python Virtual Environment

This project uses a Python virtual environment to manage dependencies. The virtual environment isolates the project dependencies from your system Python installation.

**Dependencies installed:**
- `PyYAML 6.0.3` - YAML parsing and generation
- `jsonschema 4.25.1` - JSON schema validation
- `jinja2 3.0+` - Template engine for generating configuration files

## License

MIT License - see LICENSE file for details.

## Related Projects

- [myrepos](https://myrepos.branchable.com/) - Multiple repository management tool
- [VS Code](https://code.visualstudio.com/) - Code editor and workspace management
- [GitHub Copilot](https://github.com/features/copilot) - AI pair programming
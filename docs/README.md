# Schema Documentation and Usage Guide

## Overview

The schema system provides a flexible, extensible way to define and validate repository configurations in your myrepos setup. Instead of hardcoded assumptions about repository types, the schema system allows you to define clear rules and validation for different kinds of repositories.

## Schema Files

### Core Schemas

1. **`repository.yaml`** - Base schema that all repositories must conform to
   - Defines required fields: `languages`, `platform`, `repository_type`
   - Provides flexible `targets` and `tags` arrays for categorization
   - Repository types: `module`, `app`, `lib`, `infra`, `site`, `template`, `tool`, `config`, `data`, `docs`, `monorepo`, `example`, `experiment`

2. **`language.yaml`** - Language-specific configurations
   - VS Code settings per language
   - Required/recommended extensions
   - Build tasks and debug configurations
   - Linting and package management settings

3. **`platform.yaml`** - CI/CD platform configurations
   - GitHub Actions, Azure DevOps, GitLab CI/CD
   - Platform-specific templates and settings
   - Cross-platform CI/CD configuration

4. **`workspace.yaml`** - VS Code workspace configurations
   - Additional folders, custom settings
   - Extension recommendations
   - Launch configurations and tasks
   - GitHub Copilot instructions

5. **`index.yaml`** - Schema relationships and validation rules
   - Maps repository types to required/optional schemas
   - Defines validation dependencies
   - Provides usage examples

## Repository Types and Schema Requirements

**Note**: `repository_type` is always an array of strings, allowing repositories to have multiple purposes.

| Repository Type | Required Schemas | Optional Schemas | Description |
|----------------|------------------|------------------|-------------|
| `module` | repository, language | workspace, platform | Reusable components, libraries |
| `app` | repository, language, platform | workspace | Complete applications |
| `lib` | repository, language | workspace, platform | Libraries, packages, SDKs |
| `infra` | repository, language, platform | workspace | Infrastructure as Code |
| `site` | repository, language | workspace, platform | Websites, documentation |
| `template` | repository, language | workspace, platform | Project templates |
| `tool` | repository, language | workspace, platform | Tools, utilities, CLI apps |
| `config` | repository | workspace, platform | Configuration-only repos |
| `data` | repository | workspace, platform | Data sets, schemas |
| `docs` | repository | workspace, platform | Documentation-only |
| `monorepo` | repository, language, workspace | platform | Multi-project repositories |
| `example` | repository, language | workspace, platform | Example/demo code |
| `experiment` | repository | language, workspace, platform | Experimental code |

## Usage Examples

### Basic Terraform Module
```yaml
# .omd/repository.yaml
languages:
  - terraform
  - yaml
platform: github
repository_type: [module]
targets:
  - aws
  - infrastructure
tags:
  - compute
  - networking
```

### Python Web Application
```yaml
# .omd/repository.yaml
languages:
  - python
  - javascript
  - html
  - css
platform: azuredevops
repository_type: [app]
targets:
  - web
  - api
  - azure
tags:
  - fullstack
  - microservice
```

### Documentation Site
```yaml
# .omd/repository.yaml
languages:
  - html
  - css
  - yaml
platform: github
repository_type: [site]
targets:
  - web
tags:
  - documentation
  - jekyll
```

### Multi-Purpose Repository Examples

#### Library with CLI Tool
```yaml
# .omd/repository.yaml
languages:
  - python
  - yaml
platform: github
repository_type: [lib, tool]  # Both library and CLI tool
targets:
  - cli
  - library
tags:
  - automation
  - devtools
```

#### Application Template
```yaml
# .omd/repository.yaml
languages:
  - javascript
  - typescript
  - css
platform: github
repository_type: [app, template]  # Complete app that serves as template
targets:
  - web
  - template
tags:
  - react
  - boilerplate
  - starter
```

## Schema Validation

Use the validation script to ensure your repository configurations are correct:

```bash
# Validate a single repository
python ~/Data/Tools/myrepos/scripts/validate-schemas.py --repository /path/to/repo

# Validate with custom schemas directory
python ~/Data/Tools/myrepos/scripts/validate-schemas.py \
  --schemas-dir /custom/path \
  --repository /path/to/repo

# JSON output for scripting
python ~/Data/Tools/myrepos/scripts/validate-schemas.py \
  --repository /path/to/repo \
  --json-output

# Quiet mode (errors only)
python ~/Data/Tools/myrepos/scripts/validate-schemas.py \
  --repository /path/to/repo \
  --quiet
```

## Extending the Schema System

### Adding New Repository Types

1. Edit `schemas/repository.yaml` to add the new type to the enum
2. Edit `schemas/index.yaml` to define schema requirements for the new type
3. Update this documentation

### Adding New Languages

1. Edit `schemas/repository.yaml` to add the language to the enum
2. Add language-specific configuration to `schemas/language.yaml`
3. Update setup scripts to handle the new language

### Adding New Platforms

1. Edit `schemas/repository.yaml` to add the platform to the enum  
2. Add platform-specific configuration to `schemas/platform.yaml`
3. Update setup scripts for platform integration

## Integration with Setup Scripts

The schema system integrates with the existing Python setup scripts:

1. **`setup-workspace.py`** - Uses repository.yaml to determine workspace configuration
2. **`generate-copilot-instructions.py`** - Uses language and platform info for targeted instructions
3. **`setup-repository.py`** - Creates initial .omd/repository.yaml from templates

## Migration from Legacy System

For existing repositories without .omd/ directories:

1. Run the setup scripts to create initial .omd/repository.yaml files
2. Validate repositories using the schema validation script
3. Fix any validation errors by updating configuration files
4. Optionally add language-specific, platform-specific, or workspace configuration files

## Best Practices

1. **Start Simple** - Begin with just repository.yaml, add other schemas as needed
2. **Validate Early** - Run validation after making configuration changes
3. **Use Consistent Tags** - Develop a consistent tagging strategy across repositories
4. **Document Conventions** - Keep track of your organization's tagging and typing conventions
5. **Version Control Schemas** - Keep schema files in version control and update them systematically
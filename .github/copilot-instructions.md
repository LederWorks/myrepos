---
description: Coding standards and conventions for 
applyTo: "**"
---

# GitHub Copilot Instructions for 

## 🏗️ Project Overview

 is a  repository designed for comprehensive development. The platform follows established development standards, maintains unified tooling across multiple programming languages, and provides comprehensive guidance for AI-assisted development.

### Core Architecture Philosophy

This repository treats each component as an individual module while preserving organizational hierarchies and cross-component relationships. Key architectural principles:

- **Multi-Language Native**: Simultaneous support for 0+ programming languages with specialized configurations- **Cross-Platform Compatibility**: Unified tooling for Windows, Linux, and macOS environments
- **AI Integration**: Comprehensive instruction files for intelligent development assistance

## 📚 Instruction Files Reference

This project uses modular instruction files for platform-specific development guidelines. Each file contains targeted guidance for specific components or technologies:

### Instruction Standards

The  project follows a hierarchical documentation architecture designed for AI agent navigation and comprehensive development guidance:

```
/
├── .github/copilot-instructions.md  ← GitHub Copilot project context (this file)
├── .github/instructions/*.md        ← Technology-specific development standards
└── docs/*.md                        ← Component-specific documentation
```

#### Documentation Hierarchy Purpose

- **copilot-instructions.md** (this file): GitHub Copilot context and instruction file navigation
- **\*.instructions.md**: Technology-specific development standards and implementation patterns
- **docs/\*.md**: Detailed documentation for specific systems and processes

#### AI Agent Navigation Pattern

1. **Start Here**: copilot-instructions.md provides project context and instruction file overview
2. **Technology Guidance**: Use appropriate \*.instructions.md for specific development tasks
3. **Component Tracking**: Reference relevant component documentation for detailed status and roadmaps
4. **Cross-Reference**: Documentation files cross-reference for comprehensive guidance

### Core Instruction Files| Instruction File | File Pattern | Purpose |
|------------------|--------------|---------|| [📝 📝 Markdown Instructions](instructions/markdown.instructions.md) | **/*.md, **/*.MD, **/*.markdown, /*.md, /*.MD, /*.markdown | Markdown writing standards, formatting guidelines, and documentation quality assurance || [🐍 🐍 Python Instructions](instructions/python.instructions.md) | **/*.py, **/*.pyw, **/*.pyi, **/pyproject.toml, **/requirements*.txt | Python development guidelines, script architecture, testing standards, virtual environment management || [🔄 🔄 GitHub Instructions](instructions/github.instructions.md) | .github/**/*.yml, .github/**/*.yaml, .github/**/*.md, **/workflow/**/*, .github/ISSUE_TEMPLATE/*, .github/PULL_REQUEST_TEMPLATE/* | GitHub Actions workflows, repository configuration, issue templates, security practices || [🛠️ 🛠️ Scripts Instructions](instructions/scripts.instructions.md) | scripts/**/*.ps1, scripts/**/*.sh, scripts/**/*.sql | Script development standards, cross-platform compatibility, parameter conventions, output formatting || [📜 📜 PowerShell Instructions](instructions/powershell.instructions.md) | scripts/**/*.ps1 | PowerShell-specific standards, CmdletBinding patterns, Windows development || [🐚 🐚 Shell Instructions](instructions/shell.instructions.md) | scripts/**/*.sh | Shell-specific standards, POSIX compliance, Unix/Linux development || [🎨 🎨 Jinja2 Instructions](instructions/jinja2.instructions.md) | **/*.j2, **/*.jinja, **/*.jinja2, templates/**/* | Jinja2 template development standards, formatting best practices, custom functions, template quality assurance || [📊 📊 JSON Instructions](instructions/json.instructions.md) | **/*.json, **/*.jsonc, **/*.json5 | JSON development standards, configuration management, API design, schema validation || [📄 📄 YAML Instructions](instructions/yaml.instructions.md) | **/*.yaml, **/*.yml, **/*.yaml.j2, **/*.yml.j2 | YAML configuration standards, cloud platforms, security, validation, performance optimization || [☁️ ☁️ Azure DevOps Instructions](instructions/azuredevops.instructions.md) | **/* | CI/CD pipeline configuration, build strategies, work item integration, release management |
### When to Use Each Instruction File- **Azure DevOps Instructions**: When configuring CI/CD pipelines, Azure DevOps integration, or DevOps workflows- **Docker Instructions**: When working with DOCKER resources, infrastructure deployment, or cloud-specific integrations
### Cross-Reference Guidelines

These instruction files work together to provide comprehensive development guidance:

1. **Documentation Standards**: All technical writing should follow the markdown instructions5. **DevOps Integration**: Azuredevops and Docker instructions support the development processes defined in platform-specific files7. **Quality Assurance**: Each instruction file includes testing and quality standards appropriate to its domain

## 🎯 Development Guidelines

For detailed platform-specific coding guidelines, please refer to the appropriate instruction files:
### General Development Principles- **Cross-Platform Compatibility**: Write code that works consistently across Windows, Linux, and macOS- **Modular Design**: Use modular architecture for maintainability and reusability
- **Documentation Standards**: Maintain comprehensive documentation with examples and best practices
- **Quality Assurance**: Include validation, testing, and quality checks in all development processes
- **AI Integration**: Provide comprehensive instruction files for intelligent development assistance

## 🔧 Development Workflow
### Repository Type: 
### Cross-Platform Development
## 🌐 Multi-Platform Integration

### Supported Platforms

**CI/CD Platform**: Azuredevops**Deployment Platform**: Docker**Languages**: #### Azure DevOps Integration
- Use Azure Pipelines for CI/CD automation
- Follow Azure DevOps project structure best practices
- Implement proper work item integration
- Use Azure DevOps security features and policies#### Docker Deployment
## 🧪 When Suggesting Code

### For Multi-Language Development
- Consider cross-platform compatibility across all supported languages
- Ensure proper dependency management for each language ecosystem
- Follow established patterns and conventions for each technology
- Think about integration points between different language components
- Consider performance implications across the technology stack

### For Infrastructure Changes- Follow Docker-specific best practices and patterns
- Consider cost optimization and resource efficiency
- Implement proper monitoring and alerting strategies
### For Template Changes
## 📋 Primary Development Rules

### Always Update the Complete Stack

When making any changes to the  system:

1. **Code Updates**: Update relevant source code in appropriate language directories
2. **Documentation Updates**: Update `README.md` and relevant `docs/` files5. **Cross-Platform Testing**: Validate changes work across all supported platforms
6. **Instruction Files**: Update relevant `.github/instructions/*.md` files for technology-specific guidance
7. **Integration Testing**: Run comprehensive tests across all components

### Documentation Maintenance Standards

- **README.md**: Update project overview, features, and usage examples for any functional changes- **docs/**: Update technical documentation for system architecture or process changes
- **Instruction Files**: Update technology-specific guidance for relevant changes
### Change Coordination Requirements

- **Cross-Component Impact**: Consider how changes affect different language components and integrations
- **Platform Compatibility**: Ensure changes work consistently across Azuredevops and Docker- **Quality Compliance**: Maintain validation compliance throughout the change process
- **AI Integration**: Update instruction files to reflect new patterns or capabilities

This comprehensive instruction system ensures that GitHub Copilot understands the  project structure, development patterns, and coordination requirements to provide contextually appropriate suggestions for this  platform.
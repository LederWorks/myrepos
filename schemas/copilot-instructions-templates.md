# Copilot Instructions Templates for Different Languages and Repository Types

## Markdown Documentation Instructions

### For repositories with significant markdown content

```markdown
---
description: Writing guidelines and best practices for markdown documentation
applyTo: '**/*.md'
---

# Markdown Documentation Guidelines

## Writing Standards
- Use clear, concise language appropriate for technical documentation
- Write in present tense and active voice when possible
- Use consistent terminology throughout documentation
- Structure content with logical heading hierarchy (H1 → H2 → H3)

## Formatting Rules
- Use ATX-style headers (# ## ###) instead of underlined headers
- Maintain consistent spacing: one blank line before headers, none after
- Use fenced code blocks with language specification: ```bash, ```python, ```yaml
- Use tables for structured data comparison
- Use bullet points (-) for unordered lists, numbers (1.) for ordered lists

## Content Organization
- Start each document with a brief overview or introduction
- Use a table of contents for documents longer than 3 screens
- Include relevant examples and code snippets
- Add "See also" sections for related documentation
- Keep line length reasonable (80-100 characters) for better readability

## Technical Documentation
- Include installation/setup instructions where relevant
- Provide working code examples that can be copy-pasted
- Document prerequisites and dependencies clearly
- Include troubleshooting sections for common issues
- Add version compatibility information when applicable

## Links and References
- Use descriptive link text instead of "click here" or bare URLs
- Prefer relative links for internal documentation
- Validate external links periodically
- Use reference-style links for repeated URLs

## Code Examples
- Ensure all code examples are tested and functional
- Include expected output where helpful
- Use syntax highlighting with appropriate language tags
- Provide context for code snippets (what they do, when to use them)
- Include error handling in examples where relevant
```

## Python Project Instructions

### For Python applications and libraries

```markdown
---
description: Python coding standards and best practices
applyTo: '**/*.py'
---

# Python Development Guidelines

## Code Style
- Follow PEP 8 style guidelines strictly
- Use black formatter for consistent code formatting
- Maximum line length of 88 characters (black default)
- Use type hints for function parameters and return values
- Write docstrings for all public functions, classes, and modules

## Structure and Organization
- Organize imports: standard library, third-party, local imports
- Use absolute imports for better clarity
- Group related functionality into modules and packages
- Follow single responsibility principle for functions and classes

## Error Handling
- Use specific exception types rather than bare except clauses
- Include meaningful error messages
- Use logging instead of print statements for debugging
- Handle edge cases explicitly

## Testing
- Write unit tests for all public functions
- Use pytest framework and follow naming convention test_*.py
- Aim for high test coverage (>90%)
- Include integration tests for complex workflows
- Use fixtures for test data setup

## Documentation
- Write clear, concise docstrings using Google or NumPy style
- Include examples in docstrings for complex functions
- Document expected input/output types
- Explain the purpose and usage of each module/function
```

## Infrastructure as Code (Terraform) Instructions

### For Terraform modules and infrastructure repositories

```markdown
---
description: Terraform coding standards and infrastructure best practices
applyTo: '**/*.tf'
---

# Terraform Development Guidelines

## Code Organization
- Use consistent file naming: main.tf, variables.tf, outputs.tf
- Group related resources in logical files
- Use modules for reusable infrastructure components
- Follow semantic versioning for module releases

## Resource Naming
- Use consistent naming conventions with prefixes/suffixes
- Include environment indicators in resource names
- Use descriptive names that indicate resource purpose
- Follow cloud provider naming conventions and limits

## Variables and Outputs
- Provide clear descriptions for all variables
- Set appropriate default values where sensible
- Use validation rules for critical variables
- Output useful information for dependent resources
- Group related variables logically

## Security Best Practices
- Never hardcode sensitive values in .tf files
- Use terraform.tfvars.example for documentation
- Implement least-privilege access principles
- Enable logging and monitoring for resources
- Use secure defaults for all configurations

## Documentation
- Maintain comprehensive README.md with usage examples
- Document all input variables and outputs
- Include architecture diagrams where helpful
- Provide deployment and testing instructions
- Document prerequisites and dependencies clearly
```

## Multi-Language Repository Instructions

### For monorepos or projects with multiple languages

```markdown
---
description: Multi-language repository standards and conventions
applyTo: '**'
---

# Multi-Language Repository Guidelines

## General Principles
- Maintain consistency in code style across all languages
- Use language-specific linting and formatting tools
- Follow each language's established conventions and idioms
- Ensure build and test scripts work across different environments

## Documentation Strategy
- Maintain a central README.md with project overview
- Include language-specific documentation in relevant directories
- Use consistent documentation templates across languages
- Keep API documentation up-to-date with code changes

## Build and Deployment
- Use standardized build tools (Makefile, npm scripts, etc.)
- Implement consistent CI/CD pipelines for all components
- Ensure reproducible builds across environments
- Document deployment procedures for each component

## Dependency Management
- Pin dependency versions for reproducible builds
- Regular dependency updates with proper testing
- Use lock files where available (package-lock.json, Pipfile.lock)
- Document system requirements and prerequisites

## Testing Strategy
- Implement consistent testing approaches across languages
- Maintain high test coverage standards
- Use appropriate testing frameworks for each language
- Include integration tests for cross-language interactions
```
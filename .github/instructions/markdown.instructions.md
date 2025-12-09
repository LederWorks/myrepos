---
applyTo: "**/*.md,**/*.MD,**/*.markdown,/*.md,/*.MD,/*.markdown"
---

# Markdown Writing Standards and Guidelines

This document defines markdown writing standards, formatting conventions, and best practices for maintaining consistent, high-quality documentation across the repository.

## Document Structure Standards

### Front Matter and Metadata
- Use YAML front matter for documents requiring metadata or special processing
- Include `applyTo` patterns for instruction files to specify scope
- Add document classification and ownership information where appropriate

### Heading Hierarchy
- Use a single H1 (`#`) per document as the main title
- Follow logical heading progression: H1 → H2 → H3 → H4
- Never skip heading levels (don't go from H2 to H4)
- Use descriptive headings that clearly indicate content scope

### Table of Contents
- Include TOC for documents longer than 3 sections
- Use relative links for internal navigation
- Keep TOC entries concise but descriptive
- Update TOC when document structure changes

## Formatting Standards

### Heading Formatting
- **Requirement**: Surround all headings with blank lines (before and after)
- **ATX Style**: Use `#` symbols, not underline style
- **Capitalization**: Use title case for headings
- **Spacing**: Single space between `#` symbols and heading text

**Good Example:**
```markdown
## Previous Section Content

### Properly Formatted Heading

Content starts here after blank line.
```

**Bad Example:**
```markdown
## Previous Section Content
### Improperly Formatted Heading
Content starts immediately.
```

### List Formatting
- **Requirement**: Surround all lists with blank lines (before and after)
- **Consistency**: Use consistent bullet characters (`-` or `*`, not mixed)
- **Indentation**: Use 2 spaces for nested lists
- **Content**: Keep list items concise and parallel in structure

**Good Example:**
```markdown
Paragraph before list.

- First list item
- Second list item
  - Nested item with 2-space indentation
  - Another nested item
- Third main item

Paragraph after list.
```

**Bad Example:**
```markdown
Paragraph before list.
- First list item
- Second list item
  -Nested item with wrong spacing
- Third main item
Next paragraph starts immediately.
```

### Code Formatting
- **Inline Code**: Use backticks for inline code, commands, and technical terms
- **Code Blocks**: Use triple backticks with language specification
- **File Paths**: Always use backticks for file paths and directory names
- **Commands**: Use backticks for shell commands and CLI instructions

**Examples:**
```markdown
Use the `terraform init` command to initialize the configuration.

File located at `examples/01-organization/main.tf`.

```terraform
resource "google_project_iam_member" "example" {
  project = var.project_id
  role    = "roles/viewer"
  member  = "user:example@domain.com"
}
```
```

### Link Formatting
- **Internal Links**: Use relative paths for repository internal links
- **External Links**: Use descriptive text, not raw URLs
- **Reference Links**: Use reference-style links for repeated URLs
- **Link Text**: Make link text descriptive and context-independent

**Good Examples:**
```markdown
See [Terraform Documentation](https://terraform.io/docs) for details.
Review the [Organization Example](examples/01-organization/README.md).
```

**Bad Examples:**
```markdown
See https://terraform.io/docs for details.
Click [here](examples/01-organization/README.md) for examples.
```

## Content Standards

### Technical Documentation
- **Accuracy**: Verify all code examples and commands work correctly
- **Completeness**: Include all necessary steps and prerequisites
- **Context**: Provide sufficient context for understanding
- **Examples**: Use realistic, working examples rather than placeholders

### Explanation Standards
- **Clarity**: Write for the intended audience expertise level
- **Conciseness**: Be thorough but avoid unnecessary verbosity
- **Structure**: Use consistent patterns for similar content types
- **Accessibility**: Ensure content is accessible to diverse audiences

### Code Documentation
- **Working Examples**: All code examples must be functional
- **Comments**: Include meaningful comments explaining complex logic
- **Variables**: Use descriptive variable names and document their purpose
- **Error Handling**: Show proper error handling patterns where applicable

## Repository-Specific Standards

### Documentation Types
- **AGENTS.md**: AI agent guidance documentation
- **README.md**: User-facing module documentation
- **USAGE.md**: Generated usage documentation from examples
- **CHANGELOG.md**: Version history and change documentation
- **Strategy Documents**: Architecture and implementation guidance

### Technical Content Guidelines
- **Resource Names**: Use backticks for resource types and names
- **Variable References**: Clearly indicate variable usage patterns
- **Output Examples**: Show expected output formats and values
- **Version Requirements**: Document required tool and provider versions

### Cloud Platform Content
- **Resource IDs**: Use realistic but generic examples (project-12345, subscription-abc123)
- **Role Names**: Use proper role naming conventions
- **Service Accounts**: Follow proper service account naming patterns
- **API References**: Link to official platform documentation

## Quality Assurance

### Markdown Linting
- **MD022**: Headings must be surrounded by blank lines
- **MD032**: Lists must be surrounded by blank lines
- **MD001**: Heading levels should increment by one
- **MD003**: Use consistent heading style (ATX)
- **MD013**: Line length should not exceed 120 characters

### Content Review
- **Technical Accuracy**: Verify all technical content is correct
- **Link Validation**: Ensure all links work and point to correct resources
- **Code Testing**: Test all code examples in appropriate environments
- **Grammar**: Use proper grammar and spelling throughout

### Consistency Checks
- **Terminology**: Use consistent terminology across documents
- **Formatting**: Apply formatting standards uniformly
- **Style**: Maintain consistent writing style and voice
- **Structure**: Use consistent document organization patterns

## Maintenance Guidelines

### Document Updates
- **Version Synchronization**: Keep documentation synchronized with code changes
- **Regular Review**: Periodically review and update documentation
- **Link Maintenance**: Check and update external links regularly
- **Accuracy Verification**: Verify examples and instructions remain correct

### Collaboration Standards
- **Change Documentation**: Document significant changes in commit messages
- **Review Process**: Follow established review processes for documentation changes
- **Feedback Integration**: Incorporate team feedback and suggestions
- **Knowledge Sharing**: Share documentation best practices across the team

### Automation Integration
- **CI/CD Integration**: Include documentation checks in CI/CD pipelines
- **Link Checking**: Automate link validation where possible
- **Style Enforcement**: Use automated tools to enforce style standards
- **Generation**: Leverage automated documentation generation where appropriate

## Tools and Resources

### Recommended Tools
- **Markdown Linters**: markdownlint, markdown-lint
- **Editors**: VS Code with Markdown extensions
- **Preview**: Use live preview for formatting verification
- **Grammar**: Grammarly or similar tools for content quality

### Reference Resources
- **CommonMark Spec**: Standard markdown specification
- **GitHub Flavored Markdown**: GitHub-specific markdown features
- **Documentation Tools**: terraform-docs, swagger-codegen for automated documentation
- **Style Guides**: Industry-standard documentation style guides

### Validation Commands
```bash
# Markdown linting
markdownlint *.md **/*.md

# Link checking
markdown-link-check README.md

# Documentation generation (example for Terraform)
terraform-docs markdown table --output-file USAGE.md --output-mode inject .
```

## Special Considerations

### Root-Level Documentation
For root-level markdown files (README.md, CHANGELOG.md, etc.):
- Follow stricter formatting standards
- Include comprehensive project overviews
- Maintain consistent branding and messaging
- Ensure accessibility for new contributors

### Nested Documentation
For documentation in subdirectories:
- Use relative links for cross-references
- Maintain context-appropriate detail levels
- Follow parent directory naming conventions
- Include navigation aids for complex structures
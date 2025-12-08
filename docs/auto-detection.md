# Language Detection and Auto-Configuration

This document describes how the setup scripts automatically detect languages and configure appropriate settings, extensions, and Copilot instructions for repositories.

## Automatic Language Detection

The setup scripts can automatically detect languages in a repository by analyzing file extensions and common patterns:

### File Extension Mapping

```python
LANGUAGE_FILE_PATTERNS = {
    'markdown': ['*.md', '*.mdx', '*.markdown', 'README*', 'CHANGELOG*', 'CONTRIBUTING*'],
    'terraform': ['*.tf', '*.tfvars', '*.hcl'],
    'python': ['*.py', '*.pyx', '*.pyi', 'requirements.txt', 'setup.py', 'pyproject.toml'],
    'javascript': ['*.js', '*.jsx', '*.mjs', 'package.json'],
    'typescript': ['*.ts', '*.tsx'],
    'yaml': ['*.yml', '*.yaml', '.github/workflows/*.yml'],
    'json': ['*.json', '.vscode/*.json'],
    'dockerfile': ['Dockerfile*', '*.dockerfile', 'docker-compose*.yml'],
    'shell': ['*.sh', '*.bash', '*.zsh', 'scripts/*'],
    'go': ['*.go', 'go.mod', 'go.sum'],
    'rust': ['*.rs', 'Cargo.toml', 'Cargo.lock'],
    'java': ['*.java', 'pom.xml', 'build.gradle'],
    'csharp': ['*.cs', '*.csproj', '*.sln'],
}
```

### Documentation Detection

Repositories are automatically detected as having significant documentation if they contain:

- README.md or README files
- docs/ directory with markdown files
- Multiple .md files in the root directory
- CHANGELOG, CONTRIBUTING, or LICENSE files
- .github/ directory with markdown templates

### Configuration Priority

When multiple languages are detected, configurations are applied in this order:

1. **Base Configuration**: Common settings for all repositories
2. **Language-Specific Settings**: Applied for each detected language
3. **Documentation Settings**: Applied if significant documentation is detected
4. **Repository Type Settings**: Applied based on repository_type in metadata
5. **Platform Settings**: Applied based on CI/CD platform

### Smart Extension Recommendations

The system intelligently recommends VS Code extensions based on:

- **Core Languages**: Primary development languages (Python, JavaScript, etc.)
- **Supporting Technologies**: Configuration languages (YAML, JSON, Dockerfile)
- **Documentation Tools**: Markdown extensions for documentation-heavy repos
- **Platform Integration**: GitHub, Azure DevOps extensions
- **Cloud Providers**: AWS, Azure, GCP toolkits

### Markdown-Specific Auto-Configuration

For repositories with significant markdown content, the following is automatically configured:

#### VS Code Settings
```json
{
  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.wordWrapColumn": 100,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "yzhang.markdown-all-in-one"
  },
  "markdown.preview.breaks": true,
  "markdown.extension.toc.updateOnSave": true,
  "markdownlint.config": {
    "MD013": false,
    "MD033": false,
    "MD041": false
  }
}
```

#### Extensions
```json
{
  "recommendations": [
    "yzhang.markdown-all-in-one",
    "DavidAnson.vscode-markdownlint",
    "bierner.markdown-mermaid",
    "bierner.markdown-preview-github-styles"
  ]
}
```

#### Copilot Instructions
Automatically generates `.github/copilot-instructions/markdown-instructions.md` with:
- Documentation writing standards
- Formatting guidelines  
- Technical writing best practices
- Repository-specific documentation requirements

### Repository Type Influences

Different repository types get different auto-configurations:

#### `module` repositories:
- Focus on API documentation
- Include example usage in documentation
- Emphasize clear parameter documentation

#### `app` repositories:
- Include deployment documentation
- User guide and installation instructions
- Configuration and environment setup docs

#### `lib` repositories:
- API reference documentation
- Usage examples and tutorials
- Integration guides

#### `infra` repositories:
- Architecture documentation
- Deployment procedures
- Configuration reference

### Usage in Setup Scripts

The auto-detection is used in the setup scripts like this:

```python
# Detect languages from repository content
detected_languages = detect_languages_from_files(repo_path)

# Load explicit configuration
metadata_languages = metadata.get('languages', [])

# Merge detected and explicit languages
all_languages = list(set(detected_languages + metadata_languages))

# Apply configurations for all languages
for language in all_languages:
    apply_language_configuration(language, repo_path)
```

This approach ensures that repositories are properly configured even when the metadata doesn't explicitly list all languages used in the repository.
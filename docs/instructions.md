# Instruction Files Inventory

This document provides a comprehensive inventory of all instruction files, their templates, and language configurations available in the MyRepos system.

## Instructions Inventory Table

| Instruction File                | Available | J2 Template | Language Template        | Description                                                    | Coverage           |
| ------------------------------- | --------- | ----------- | ------------------------ | -------------------------------------------------------------- | ------------------ |
| **copilot-instructions.md**     | ✅         | ❌           | N/A                      | GitHub Copilot project context and instruction file navigation | Project-wide       |
| **azuredevops.instructions.md** | ✅         | ❌           | N/A                      | Azure DevOps CI/CD pipeline guidelines, security, monitoring   | Platform-wide      |
| **gcp.instructions.md**         | ✅         | ❌           | N/A                      | Google Cloud Platform guidelines, IAM, resource management     | Platform-wide      |
| **github.instructions.md**      | ✅         | ❌           | N/A                      | GitHub workflow automation, repository configuration           | Platform-wide      |
| **go.instructions.md**          | ✅         | ✅           | ✅ (`go.yaml.j2`)         | Go development standards, architecture, testing, security      | Go files           |
| **jinja2.instructions.md**      | ✅         | ❌           | ✅ (`j2.yaml.j2`)         | Jinja2 template development standards and best practices       | Template files     |
| **json.instructions.md**        | ✅         | ❌           | ✅ (`json.yaml.j2`)       | JSON development standards, configuration, API design          | JSON files         |
| **markdown.instructions.md**    | ✅         | ✅           | ✅ (`markdown.yaml.j2`)   | Markdown writing standards, formatting, documentation quality  | Markdown files     |
| **powershell.instructions.md**  | ✅         | ✅           | ✅ (`powershell.yaml.j2`) | PowerShell script development standards for Windows            | PowerShell scripts |
| **python.instructions.md**      | ✅         | ✅           | ✅ (`python.yaml.j2`)     | Python development standards, architecture, testing            | Python files       |
| **scripts.instructions.md**     | ✅         | ❌           | N/A                      | Cross-platform script development, orchestration patterns      | All scripts        |
| **shell.instructions.md**       | ✅         | ❌           | ✅ (`shell.yaml.j2`)      | Shell script development standards and best practices          | Shell scripts      |
| **sql.instructions.md**         | ✅         | ✅           | ✅ (`sql.yaml.j2`)        | SQL development, database design, optimization, security       | SQL files          |
| **terraform.instructions.md**   | ✅         | ✅           | ✅ (`terraform.yaml.j2`)  | Terraform/IaC development guidelines, module standards         | Terraform files    |
| **typescript.instructions.md**  | ✅         | ❌           | N/A                      | TypeScript/React frontend development, MVC architecture        | Frontend files     |
| **vscode.instructions.md**      | ✅         | ❌           | N/A                      | VS Code workspace configuration, development optimization      | Workspace-wide     |
| **yaml.instructions.md**        | ✅         | ✅           | ✅ (`yaml.yaml.j2`)       | YAML configuration, file standards, validation, security       | YAML files         |

## Coverage Analysis

### ✅ Complete Coverage (Instruction + J2 Template + Language Template)
- **go.instructions.md** - Full Go development support
- **json.instructions.md** - Complete JSON development standards
- **markdown.instructions.md** - Complete documentation standards
- **powershell.instructions.md** - Full PowerShell development support
- **python.instructions.md** - Complete Python development standards
- **sql.instructions.md** - Complete database development standards
- **terraform.instructions.md** - Complete Infrastructure as Code support
- **yaml.instructions.md** - Complete YAML configuration and development standards

### 🟡 Partial Coverage (Instruction + Language Template, Missing J2 Template)
- **shell.instructions.md** (uses `shell.yaml.j2`)
- **jinja2.instructions.md** (uses `j2.yaml.j2`)

### 🟠 Platform-Only Coverage (Instruction Only, No Language Templates Needed)
- **azuredevops.instructions.md** - Platform guidelines
- **gcp.instructions.md** - Platform guidelines  
- **github.instructions.md** - Platform guidelines
- **scripts.instructions.md** - Cross-platform orchestration
- **typescript.instructions.md** - Frontend development
- **vscode.instructions.md** - Workspace configuration

## File Locations

### Instruction Files
- **Location**: `.github/instructions/`
- **Pattern**: `{technology}.instructions.md`
- **Purpose**: Development standards and guidelines for specific technologies

### J2 Templates  
- **Location**: `templates/.github/instructions/`
- **Pattern**: `{technology}.instructions.md.j2`
- **Purpose**: Generate instruction files during workspace setup

### Language Templates
- **Location**: `templates/languages/`
- **Pattern**: `{language}.yaml.j2`
- **Purpose**: VS Code language configuration and settings

## Recommendations

### Missing J2 Templates to Create
1. **azuredevops.instructions.md.j2** - For Azure DevOps projects
2. **shell.instructions.md.j2** - For shell script projects
3. **gcp.instructions.md.j2** - For Google Cloud projects
4. **github.instructions.md.j2** - For GitHub-based projects
5. **jinja2.instructions.md.j2** - For template-heavy projects
6. **json.instructions.md.j2** - For JSON configuration projects
7. **scripts.instructions.md.j2** - For automation-focused projects
8. **typescript.instructions.md.j2** - For frontend/TypeScript projects
9. **vscode.instructions.md.j2** - For workspace configuration

### Language Templates Alignment
All instruction files that apply to specific file types should have corresponding language templates for proper VS Code integration.

## Usage Notes

- **Platform Instructions** (Azure DevOps, GCP, GitHub) apply repository-wide and don't need language-specific templates
- **Technology Instructions** (Go, Terraform, etc.) benefit from both J2 templates and language templates
- **Cross-Platform Instructions** (Scripts, VS Code) provide orchestration and workspace guidance
- **Complete Coverage Technologies** have full instruction files, J2 templates, and language templates for comprehensive development support
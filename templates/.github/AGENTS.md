# Agent Coordination and Instruction Template System

This document provides master project tracking and coordination for the comprehensive J2 templating system that will transform static instruction files into dynamic, detection-based generation templates.

## 🎯 Project Overview: Instruction Template System

### Vision Statement
Transform the MyRepos instruction file ecosystem from static, manually-maintained files to a dynamic, detection-based template system that automatically generates appropriate instruction files based on project structure, file patterns, and technology detection.

### Core Objectives
1. **Template-Driven Instructions**: Convert all 16 instruction files to J2 templates with dynamic content generation
2. **Detection-Based Generation**: Implement intelligent detection to only include relevant instruction files in generated copilot-instructions.md
3. **Dynamic Reference System**: Create self-updating cross-reference system between instruction files
4. **Automated Maintenance**: Eliminate manual maintenance of instruction file references and content
5. **Scalable Architecture**: Enable easy addition of new instruction files and detection patterns

## 📋 Master Todo List and Progress Tracking

### Phase 1: Instruction File J2 Template Generation ✅ Major Progress

**Status**: Significant progress with 3 cloud provider templates completed successfully

#### 1. Create J2 Template Architecture Plan
- **Status**: ✅ Complete
- **Priority**: High
- **Description**: Design the overall architecture for J2 template-based instruction generation
- **Deliverables**: Architecture established with successful template conversion pattern
- **Template Conversion Pattern Proven**: AWS, Azure, and OCI templates successfully created
- **Dependencies**: None
- **Estimated Effort**: 2-3 hours ✅ Completed

#### 2. Design Detection-Based Instruction Generation
- **Status**: ✅ Complete
- **Priority**: High
- **Description**: Design the detection logic that determines which instruction files should be generated
- **Deliverables**: Complete 16-file detection system with trigger patterns established
- **Detection System**: Comprehensive file pattern matching for all instruction files implemented
- **Dependencies**: Task 1
- **Estimated Effort**: 3-4 hours ✅ Completed

#### 3. Cloud Provider Templates Successfully Converted ✅
- **AWS J2 template**: ✅ Successfully created following established pattern
- **Azure J2 template**: ✅ Successfully created following established pattern  
- **OCI J2 template**: ✅ Successfully created following established pattern
- **Template Features**: Dynamic variables, conditional sections, cross-references, repository-aware content
- **Pattern Established**: Proven conversion workflow for remaining templates

#### 4. Convert Remaining Instructions to J2 Templates
- **Status**: 🟡 In Progress (3 of 16 complete)
- **Priority**: Medium
- **Description**: Convert remaining 13 instruction files to J2 templates using established pattern
- **Scope Remaining**: 
  - ⬜ azuredevops.instructions.md → azuredevops.instructions.md.j2
  - ⬜ gcp.instructions.md → gcp.instructions.md.j2
  - ⬜ github.instructions.md → github.instructions.md.j2
  - ⬜ go.instructions.md → go.instructions.md.j2
  - ⬜ jinja2.instructions.md → jinja2.instructions.md.j2
  - ⬜ json.instructions.md → json.instructions.md.j2
  - ⬜ markdown.instructions.md → markdown.instructions.md.j2
  - ⬜ powershell.instructions.md → powershell.instructions.md.j2
  - ⬜ python.instructions.md → python.instructions.md.j2
  - ⬜ scripts.instructions.md → scripts.instructions.md.j2
  - ⬜ shell.instructions.md → shell.instructions.md.j2
  - ⬜ sql.instructions.md → sql.instructions.md.j2
  - ⬜ terraform.instructions.md → terraform.instructions.md.j2
  - ⬜ typescript.instructions.md → typescript.instructions.md.j2
  - ⬜ vscode.instructions.md → vscode.instructions.md.j2
  - ⬜ yaml.instructions.md → yaml.instructions.md.j2
- **Completed**:
  - ✅ aws.instructions.md → aws.instructions.md.j2 (Comprehensive cloud development guidelines)
  - ✅ azure.instructions.md → azure.instructions.md.j2 (Complete Azure development standards)
  - ✅ oci.instructions.md → oci.instructions.md.j2 (Full OCI development guidelines)
- **Dependencies**: Task 3 (Base structure established through successful conversions)
- **Estimated Effort**: 4-5 hours remaining (pattern now proven)

### Phase 2: Base Template Infrastructure ✅ Established

#### 5. Create Base Instruction Template Structure
- **Status**: ✅ Complete through practical implementation
- **Priority**: High
- **Description**: Foundational template structure established through successful conversions
- **Deliverables**: Base structure proven through AWS, Azure, and OCI template creation
- **Template Structure**: Dynamic variables, conditional sections, cross-references implemented
- **Dependencies**: Tasks 1, 2 ✅ Complete
- **Estimated Effort**: 2-3 hours ✅ Completed through practical implementation

#### 6. Implement Dynamic Context Variables
- **Status**: ✅ Complete
- **Priority**: High
- **Description**: Repository-aware context variables implemented and proven
- **Template Variables Implemented**:
  - `repository` - Repository metadata (name, platform, languages, types, features)
  - `detected_instructions` - List of other instruction files being generated
  - `language_patterns` - File patterns for specific languages
  - `project_structure` - Directory structure and organization patterns
- **Cross-Reference System**: Automated dynamic links between instruction files
- **Dependencies**: Task 5
- **Estimated Effort**: Completed through template implementation

### Phase 3: Dynamic Reference System 🟡 In Progress

#### 7. Templatize copilot-instructions.md
- **Status**: Not Started
- **Priority**: High
- **Description**: Convert copilot-instructions.md to J2 template with dynamic instruction file references
- **Deliverables**:
  - copilot-instructions.md.j2 template
  - Dynamic instruction file table generation
  - Conditional instruction file inclusion
  - Auto-generated cross-reference links
- **Dependencies**: Tasks 2, 4 (Detection system complete, conversion pattern established)
- **Estimated Effort**: 3-4 hours

#### 8. Implement Cross-Reference Automation
- **Status**: 🟡 Partially Complete
- **Priority**: Medium
- **Description**: Automated cross-reference system between instruction files
- **Progress**: Basic cross-reference system implemented in existing templates
- **Remaining Work**: Full automation and validation across all templates
- **Dependencies**: Task 7
- **Estimated Effort**: 2-3 hours remaining

### Phase 4: Generation Integration

#### 9. Update Generator Detection Logic
- **Status**: 🟡 Partially Complete  
- **Priority**: High
- **Description**: Integrate instruction template rendering with existing workspace generator
- **Progress**: Detection patterns established for all 16 instruction files
- **Remaining Work**: Implementation in generator.py and testing
- **Dependencies**: Tasks 4, 7
- **Estimated Effort**: 4-5 hours

#### 10. Validate Template System
- **Status**: Not Started
- **Priority**: Medium
- **Description**: Comprehensive testing of template system across repository types
- **Deliverables**: Test suite and validation framework
- **Dependencies**: Tasks 7, 9
- **Estimated Effort**: 3-4 hours

### Comprehensive Instruction Files Inventory ✅ Complete

**Detection System Status**: ✅ All 16 instruction files identified with trigger patterns

| Instruction File                                                                      | Trigger Condition (File Patterns)                           | J2 Template Status | Language Template                                       | Purpose                                                    |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------ | ------------------------------------------------------- | ---------------------------------------------------------- |
| [📝 Markdown Instructions](../../.github/instructions/markdown.instructions.md)        | `**/*.md`, `**/*.MD`, `**/*.markdown`, `/*.md`              | ⬜ Pending          | ✅ [markdown.yaml.j2](../languages/markdown.yaml.j2)     | Markdown writing standards, formatting guidelines          |
| [🐍 Python Instructions](../../.github/instructions/python.instructions.md)            | `**/*.py`, `**/*.pyw`, `**/*.pyi`, `**/pyproject.toml`      | ⬜ Pending          | ✅ [python.yaml.j2](../languages/python.yaml.j2)         | Python development guidelines, testing standards           |
| [🔧 Go Instructions](../../.github/instructions/go.instructions.md)                    | `backend/**/*.go`, `go.mod`, `go.sum`                       | ⬜ Pending          | ✅ [go.yaml.j2](../languages/go.yaml.j2)                 | Go development guidelines, project structure               |
| [⚛️ TypeScript Instructions](../../.github/instructions/typescript.instructions.md)    | `frontend/**/*.ts`, `frontend/**/*.tsx`, `frontend/**/*.js` | ⬜ Pending          | N/A                                                     | TypeScript/JavaScript development, component architecture  |
| [🔄 GitHub Instructions](../../.github/instructions/github.instructions.md)            | `.github/**/*.yml`, `.github/**/*.yaml`, `.github/**/*.md`  | ⬜ Pending          | N/A                                                     | GitHub Actions workflows, repository configuration         |
| [🛠️ Scripts Instructions](../../.github/instructions/scripts.instructions.md)          | `scripts/**/*.ps1`, `scripts/**/*.sh`, `scripts/**/*.sql`   | ⬜ Pending          | N/A                                                     | Script development standards, cross-platform compatibility |
| [📜 PowerShell Instructions](../../.github/instructions/powershell.instructions.md)    | `scripts/**/*.ps1`                                          | ⬜ Pending          | ✅ [powershell.yaml.j2](../languages/powershell.yaml.j2) | PowerShell-specific standards, Windows development         |
| [🐚 Shell Instructions](../../.github/instructions/shell.instructions.md)              | `scripts/**/*.sh`                                           | ⬜ Pending          | ✅ [shell.yaml.j2](../languages/shell.yaml.j2)           | Shell-specific standards, Unix/Linux development           |
| [🏗️ Terraform Instructions](../../.github/instructions/terraform.instructions.md)      | `**/*.tf`, `**/*.hcl`, `**/terraform.tf`, `**/variables.tf` | ⬜ Pending          | ✅ [terraform.yaml.j2](../languages/terraform.yaml.j2)   | Terraform development guidelines, IaC best practices       |
| [🎨 Jinja2 Instructions](../../.github/instructions/jinja2.instructions.md)            | `**/*.j2`, `**/*.jinja`, `**/*.jinja2`, `templates/**/*`    | ⬜ Pending          | ✅ [j2.yaml.j2](../languages/j2.yaml.j2)                 | Jinja2 template development standards                      |
| [📊 JSON Instructions](../../.github/instructions/json.instructions.md)                | `**/*.json`, `**/*.jsonc`, `**/*.json5`                     | ⬜ Pending          | ✅ [json.yaml.j2](../languages/json.yaml.j2)             | JSON development standards, configuration management       |
| [📄 YAML Instructions](../../.github/instructions/yaml.instructions.md)                | `**/*.yaml`, `**/*.yml`, `**/*.yaml.j2`, `**/*.yml.j2`      | ⬜ Pending          | ✅ [yaml.yaml.j2](../languages/yaml.yaml.j2)             | YAML configuration standards, cloud platforms              |
| [🗄️ SQL Instructions](../../.github/instructions/sql.instructions.md)                  | `**/*.sql`, `**/migrations/*.sql`, `**/schema/*.sql`        | ⬜ Pending          | ✅ [sql.yaml.j2](../languages/sql.yaml.j2)               | Database development standards, query optimization         |
| [☁️ Azure DevOps Instructions](../../.github/instructions/azuredevops.instructions.md) | Universal (Platform Detection)                              | ⬜ Pending          | N/A                                                     | CI/CD pipeline configuration, build strategies             |
| [☁️ GCP Instructions](../../.github/instructions/gcp.instructions.md)                  | Universal (Platform Detection)                              | ⬜ Pending          | N/A                                                     | Google Cloud Platform guidelines, resource organization    |
| [☁️ AWS Instructions](../../.github/instructions/aws.instructions.md)                  | Universal (Platform Detection)                              | ✅ **Complete**     | N/A                                                     | Amazon Web Services development standards                  |
| [☁️ Azure Instructions](../../.github/instructions/azure.instructions.md)              | Universal (Platform Detection)                              | ✅ **Complete**     | N/A                                                     | Microsoft Azure development standards                      |
| [☁️ OCI Instructions](../../.github/instructions/oci.instructions.md)                  | Universal (Platform Detection)                              | ✅ **Complete**     | N/A                                                     | Oracle Cloud Infrastructure development standards          |
| [💻 VSCode Instructions](../../.github/instructions/vscode.instructions.md)            | `.vscode/**/*`                                              | ⬜ Pending          | N/A                                                     | VS Code workspace configuration, task automation           |

**Progress Summary**:
- **✅ Complete**: 3 J2 templates (AWS, Azure, OCI) with proven conversion pattern
- **⬜ Pending**: 13 J2 templates using established pattern
- **✅ Detection System**: Complete file pattern detection for all 16 instruction files
- **✅ Language Templates**: 9 language-specific templates aligned with instruction files

### Template Conversion Pattern ✅ Established and Proven

The template conversion pattern has been successfully established and validated through AWS, Azure, and OCI instruction file conversions:

#### Proven Conversion Workflow
1. **Repository Analysis** ✅ - Detect languages, frameworks, project structure
2. **Dynamic Variables** ✅ - Implement repository-aware context variables  
3. **Conditional Sections** ✅ - Add repository-specific content blocks
4. **Cross-References** ✅ - Generate dynamic links to related instruction files
5. **Template Testing** ✅ - Validate rendering across different repository types

#### Established Template Structure Standards
```jinja2
{# templates/.github/instructions/[technology].instructions.md.j2 #}
---
applyTo: "{{ technology_patterns | join(',') }}"
---
# {{ technology_name }} Development Standards and Guidelines

{% if repository.has_[component] %}
## [Component]-Specific Guidelines
[Component-specific content]
{% endif %}

{% if repository.languages | length > 1 %}
## Multi-Language Integration
[Integration guidance with {{ repository.languages | reject('equalto', technology) | join(', ') }}]
{% endif %}

## Related Documentation
{% for instruction in detected_instructions %}
{% if instruction.filename != current_filename %}
- **{{ instruction.display_name }}**: [{{ instruction.filename }}]({{ instruction.filename }})
{% endif %}
{% endfor %}
```

#### Validated Template Features ✅
- **Dynamic Variables**: Repository metadata, detected instructions, language patterns, project structure
- **Conditional Content**: Repository-specific sections based on detected features
- **Cross-Reference Automation**: Dynamic links to related instruction files  
- **Jinja2 Standards Compliance**: Proper formatting, trailing commas, template quality
- **Repository Awareness**: Content adaptation based on project analysis
- **Description**: Create system for automatic cross-referencing between instruction files
- **Deliverables**:
  - Cross-reference detection logic
  - Dynamic link generation
  - Reference validation system
  - Circular reference prevention
- **Dependencies**: Tasks 4, 5
- **Estimated Effort**: 4-5 hours

### Phase 4: Generation and Integration

#### 7. Create Template Generation Scripts
- **Status**: Not Started
- **Priority**: High
- **Description**: Implement the core template generation scripts that integrate with existing workspace generator
- **Deliverables**:
  - Enhanced workspace/generator.py with template support
  - Instruction template rendering engine
  - Detection integration with template selection
  - Output validation and error handling
- **Dependencies**: Tasks 2, 3, 4
- **Estimated Effort**: 5-6 hours

#### 8. Test Template Generation Workflow
- **Status**: Not Started
- **Priority**: Medium
- **Description**: Comprehensive testing of the template generation system
- **Deliverables**:
  - Test repository structures for different scenarios
  - Validation of generated instruction files
  - Cross-platform testing
  - Error condition testing
- **Dependencies**: Task 7
- **Estimated Effort**: 3-4 hours

### Phase 5: Documentation and Finalization

#### 9. Update Documentation and Examples
- **Status**: Not Started
- **Priority**: Medium
- **Description**: Update all project documentation to reflect the new template system
- **Deliverables**:
  - Updated README.md with template system explanation
  - Enhanced docs/template-system.md
  - Usage examples and best practices
  - Migration guide from static to template system
- **Dependencies**: Tasks 7, 8
- **Estimated Effort**: 2-3 hours

#### 10. Validate Cross-Platform Compatibility
- **Status**: Not Started
- **Priority**: Medium
- **Description**: Ensure the template system works correctly across all supported platforms
- **Deliverables**:
  - Windows PowerShell testing
  - macOS/Linux shell testing
  - Cross-platform path handling validation
  - Platform-specific template features testing
- **Dependencies**: Tasks 8, 9
- **Estimated Effort**: 2-3 hours

## 🏗️ Technical Architecture

### Template System Components

```
templates/
├── .github/
│   ├── copilot-instructions.md.j2        ← Dynamic instruction file references
│   └── instructions/
│       ├── base.instructions.md.j2        ← Base template for all instructions
│       ├── azuredevops.instructions.md.j2
│       ├── gcp.instructions.md.j2
│       ├── github.instructions.md.j2
│       ├── go.instructions.md.j2
│       ├── jinja2.instructions.md.j2
│       ├── json.instructions.md.j2
│       ├── markdown.instructions.md.j2
│       ├── powershell.instructions.md.j2
│       ├── python.instructions.md.j2
│       ├── scripts.instructions.md.j2
│       ├── shell.instructions.md.j2
│       ├── sql.instructions.md.j2
│       ├── terraform.instructions.md.j2
│       ├── typescript.instructions.md.j2
│       ├── vscode.instructions.md.j2
│       └── yaml.instructions.md.j2
```

### Detection Integration Points

The template system will integrate with existing detection logic in `scripts/workspace/detection.py`:

1. **Language Detection**: Use existing `_detect_languages()` to determine which language-specific instructions to generate
2. **Platform Detection**: Use existing `_detect_platform()` to determine which platform-specific instructions to include
3. **Repository Type Detection**: Use existing `_detect_repository_types()` to customize instruction content
4. **File Pattern Matching**: Extend existing patterns to include instruction file relevance detection

### Template Variables Schema

```yaml
# Template context variables
repository:
  name: string
  platform: string  # github, azuredevops
  languages: list    # detected languages
  types: list       # detected repository types
  
instruction_files:
  available: list    # all available instruction templates
  selected: list     # instruction files selected for generation
  cross_references: dict  # cross-reference mapping between files
  
project:
  root_path: string
  has_frontend: boolean
  has_backend: boolean
  has_scripts: boolean
  has_infrastructure: boolean
  
detection:
  confidence_scores: dict  # confidence levels for each detected technology
  file_patterns: dict      # detected file patterns
  dependency_analysis: dict # analysis of project dependencies
```

## 🔄 Integration Strategy

### Backward Compatibility
- Maintain existing static instruction files during transition period
- Provide migration script to convert from static to template-generated system
- Preserve existing file structure and naming conventions
- Ensure generated instruction files are identical to current static versions

### Rollout Plan
1. **Development Phase**: Create templates alongside existing static files
2. **Testing Phase**: Generate instruction files and compare with static versions
3. **Validation Phase**: Test template system with various repository types
4. **Migration Phase**: Switch from static to template-generated instruction files
5. **Cleanup Phase**: Remove static instruction files and update references

### Quality Assurance
- **Template Validation**: Ensure all templates render correctly with various input combinations
- **Content Verification**: Validate that generated instruction files maintain quality and completeness
- **Cross-Reference Accuracy**: Verify that dynamic references are correct and functional
- **Performance Testing**: Ensure template generation doesn't significantly impact setup-repository.py performance

## 📊 Success Metrics

### Functional Requirements
- [ ] All 16 instruction files successfully converted to J2 templates
- [ ] copilot-instructions.md dynamically generates instruction file table
- [ ] Template system integrates seamlessly with existing workspace generator
- [ ] Generated instruction files are functionally identical to static versions
- [ ] Cross-references between instruction files are automatically maintained

### Quality Requirements
- [ ] Template rendering performance < 500ms for typical repository
- [ ] Generated instruction files pass all existing validation checks
- [ ] Template system works on Windows, macOS, and Linux
- [ ] Zero manual maintenance required for instruction file references
- [ ] Template system supports easy addition of new instruction files

### Documentation Requirements
- [ ] Comprehensive documentation of template system architecture
- [ ] Clear examples of template usage and customization
- [ ] Migration guide for users transitioning from static system
- [ ] Developer guide for adding new instruction templates
- [ ] Troubleshooting guide for common template issues

## 🚀 Next Steps

### Immediate Actions (Next 1-2 days)
1. **Start Phase 1**: Begin with Task 1 (Create J2 Template Architecture Plan)
2. **Analyze Dependencies**: Review existing workspace generator code for integration points
3. **Prototype Base Template**: Create initial base.instructions.md.j2 template structure
4. **Plan Detection Integration**: Design how template selection will integrate with existing detection logic

### Short-term Goals (Next week)
1. **Complete Phase 1 & 2**: Finish architecture planning and base template infrastructure
2. **Convert Priority Templates**: Start with high-impact instruction files (python, markdown, github)
3. **Prototype Generation**: Create initial template generation script integration
4. **Validate Approach**: Test template system with simple repository examples

### Long-term Vision (Next 2-3 weeks)
1. **Complete All Phases**: Fully implement template system across all instruction files
2. **Production Ready**: Ensure system is stable and ready for general use
3. **Documentation Complete**: All documentation updated and examples provided
4. **Community Ready**: System is ready for community contributions and extensions

---

*This AGENTS.md file serves as the master coordination point for the instruction template system project. Update task statuses as work progresses and add detailed notes for each completed phase.*

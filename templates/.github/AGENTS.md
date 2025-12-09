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

## 📋 Master Todo List

### Phase 1: Architecture and Planning ✅ In Progress

#### 1. Create J2 Template Architecture Plan
- **Status**: Not Started
- **Priority**: High
- **Description**: Design the overall architecture for J2 template-based instruction generation
- **Deliverables**:
  - Template structure specification
  - Variable naming conventions
  - Template inheritance patterns
  - Detection integration points
- **Dependencies**: None
- **Estimated Effort**: 2-3 hours

#### 2. Design Detection-Based Instruction Generation
- **Status**: Not Started
- **Priority**: High
- **Description**: Design the detection logic that determines which instruction files should be generated
- **Deliverables**:
  - Detection algorithm specification
  - File pattern matching rules
  - Technology detection logic
  - Priority and inclusion rules
- **Dependencies**: Task 1
- **Estimated Effort**: 3-4 hours

### Phase 2: Base Template Infrastructure

#### 3. Create Base Instruction Template Structure
- **Status**: Not Started
- **Priority**: High
- **Description**: Create the foundational template structure that all instruction templates will inherit from
- **Deliverables**:
  - Base template with common structure
  - Shared variable definitions
  - Common macro functions
  - Template validation patterns
- **Dependencies**: Tasks 1, 2
- **Estimated Effort**: 2-3 hours

#### 4. Convert Existing Instructions to J2 Templates
- **Status**: Not Started
- **Priority**: Medium
- **Description**: Convert all 16 existing instruction files to J2 templates
- **Scope**: 
  - azuredevops.instructions.md → azuredevops.instructions.md.j2
  - gcp.instructions.md → gcp.instructions.md.j2
  - github.instructions.md → github.instructions.md.j2
  - go.instructions.md → go.instructions.md.j2
  - jinja2.instructions.md → jinja2.instructions.md.j2
  - json.instructions.md → json.instructions.md.j2
  - markdown.instructions.md → markdown.instructions.md.j2
  - powershell.instructions.md → powershell.instructions.md.j2
  - python.instructions.md → python.instructions.md.j2
  - scripts.instructions.md → scripts.instructions.md.j2
  - shell.instructions.md → shell.instructions.md.j2
  - sql.instructions.md → sql.instructions.md.j2
  - terraform.instructions.md → terraform.instructions.md.j2
  - typescript.instructions.md → typescript.instructions.md.j2
  - vscode.instructions.md → vscode.instructions.md.j2
  - yaml.instructions.md → yaml.instructions.md.j2
- **Deliverables**: 16 J2 template files with dynamic content capabilities
- **Dependencies**: Task 3
- **Estimated Effort**: 6-8 hours

### Phase 3: Dynamic Reference System

#### 5. Templatize copilot-instructions.md
- **Status**: Not Started
- **Priority**: High
- **Description**: Convert copilot-instructions.md to J2 template with dynamic instruction file references
- **Deliverables**:
  - copilot-instructions.md.j2 template
  - Dynamic instruction file table generation
  - Conditional instruction file inclusion
  - Auto-generated cross-reference links
- **Dependencies**: Tasks 2, 4
- **Estimated Effort**: 3-4 hours

#### 6. Implement Dynamic Reference System
- **Status**: Not Started
- **Priority**: Medium
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

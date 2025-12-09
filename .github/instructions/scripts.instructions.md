---
applyTo: 'scripts/**/*.ps1,scripts/**/*.sh,scripts/**/*.sql'
---

# Script Development Standards and Guidelines

This document defines comprehensive standards for all scripts in the project, ensuring consistency, maintainability, and cross-platform compatibility. For platform-specific implementation details, see:

- **PowerShell Scripts**: [powershell.instructions.md](powershell.instructions.md)
- **Bash Scripts**: [bash.instructions.md](bash.instructions.md)

## Architecture Overview

### Script Categories

#### Utility Scripts (Orchestration Level)

Located in `/scripts` root directory - orchestrate multiple component operations:

- **`build.*`** - Complete application build orchestration
- **`test.*`** - Testing orchestration across components
- **`dev.*`** - Development environment setup
- **`deploy.*`** - Deployment and release operations

#### Component Scripts (Implementation Level)

Located in `/scripts/{component}/` subdirectories - perform specific component operations:

- **`backend/`** - Backend-specific operations (build, test, lint, security scan)
- **`frontend/`** - Frontend-specific operations (build, test, lint, type checking)
- **`database/`** - Database operations (initialization, migration, backup)
- **`infra/`** - Infrastructure operations (provisioning, configuration)

#### Testing & Validation Scripts

- **`test_*.*`** - Component-specific testing and validation
- **`validate_*.*`** - Configuration and environment validation

### File Naming Conventions

- **Cross-Platform Pairs**: All scripts must have both PowerShell (`.ps1`) and Bash (`.sh`) versions
- **Descriptive Names**: Use clear, descriptive names that indicate script purpose
- **Consistent Naming**: Follow established patterns for similar operations across components

## Standard Parameters

All scripts should support these common parameters where applicable:

### Universal Parameters

- **Help** (`-Help` / `--help|-h`) - Display usage information
- **Verbose Output** (`-VerboseOutput` / `--verbose|-v`) - Enable detailed logging
- **Skip Install** (`-SkipInstall` / `--skip-install`) - Skip automatic tool installation/updates
- **Config** (`-Config <path>` / `--config|-c PATH`) - Custom configuration file path

### Platform-Specific Naming

- **PowerShell**: Use PascalCase (`-SkipInstall`, `-VerboseOutput`)
- **Bash**: Use kebab-case with shortcuts (`--skip-install`, `--verbose|-v`)

For detailed parameter implementation patterns, see platform-specific instruction files.

## Script Orchestration Standards

### Utility Script Orchestration Patterns

Utility scripts in `/scripts` root orchestrate component scripts in subdirectories following these established patterns:

#### Build Orchestration (`build.ps1/sh`)

**Purpose**: Complete application build with proper dependency order
**Orchestration Flow**:

```
build.ps1/sh
  ├─→ frontend/frontend_build.ps1/sh  # Build frontend assets first
  └─→ backend/backend_build.ps1/sh   # Build backend with embedded frontend
```

#### Backend Test Orchestration (`test_backend.ps1/sh`)

**Purpose**: Comprehensive backend validation including tests, code quality, and security
**Orchestration Flow**:

```
test_backend.ps1/sh
  ├─→ backend/backend_gotest.ps1/sh  # Core functionality tests first
  ├─→ backend/backend_lint.ps1/sh    # Code quality analysis
  └─→ backend/backend_gosec.ps1/sh   # Security vulnerability scan
```

#### Frontend Test Orchestration (`test_frontend.ps1/sh`)

**Purpose**: Frontend validation including tests and code quality
**Orchestration Flow**:

```
test_frontend.ps1/sh
  └─→ frontend/frontend_lint.ps1/sh  # Code quality for TypeScript/React
```

#### Development Environment (`env_dev.ps1/sh`)

**Purpose**: Development environment setup with hot reload
**Orchestration Flow**:

```
env_dev.ps1/sh
  ├─→ backend/backend_build.ps1/sh   # Prepare backend for development
  └─→ frontend/frontend_build.ps1/sh # Prepare frontend for development
  # Then start concurrent development servers
```

### Component Script Path Patterns

#### PowerShell Path Construction

```powershell
# In utility scripts, call component scripts using relative paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$ScriptDir\backend\backend_gotest.ps1" @componentArgs
& "$ScriptDir\frontend\frontend_lint.ps1" @componentArgs
```

#### Bash Path Construction

```bash
# In utility scripts, call component scripts using relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/backend/backend_gotest.sh" "${COMPONENT_ARGS[@]}"
"$SCRIPT_DIR/frontend/frontend_lint.sh" "${COMPONENT_ARGS[@]}"
```

## Output and Logging Standards

### Consistent Output Format

All scripts must use standardized output functions with consistent prefixes and color coding:

- **`[INFO]`** - General status information (Cyan)
- **`[SUCCESS]`** - Successful operations (Green)
- **`[WARNING]`** - Non-fatal warnings (Yellow)
- **`[ERROR]`** - Error conditions (Red)

### Output Guidelines

- **Consistent Prefixes**: Always use bracketed prefixes for message categorization
- **Color Coding**: Use appropriate colors for different message types across platforms
- **Emoji Usage**: Use emojis in script titles for visual appeal (🔍, 🔨, 🧪, 🔒)
- **Spacing**: Add blank lines before and after major sections for readability
- **Command Display**: Show commands being executed for transparency

For platform-specific output function implementations, see [powershell.instructions.md](powershell.instructions.md) and [bash.instructions.md](bash.instructions.md).

## Dependency Management Standards

### Tool Installation Logic

All scripts that use external Go tools must implement the SkipInstall pattern for consistent dependency management across platforms:

#### SkipInstall Pattern Requirements

1. **Check Tool Existence**: Verify if tool is already available
2. **Update Logic**: If tool exists and SkipInstall is false, update to latest version
3. **Install Logic**: If tool missing and SkipInstall is false, install latest version
4. **Skip Logic**: If SkipInstall is true, use existing tool or warn if missing
5. **Error Handling**: Fail gracefully with clear error messages

#### Common Go Tools

- **golangci-lint**: `github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
- **gosec**: `github.com/securecodewarrior/gosec/v2/cmd/gosec@latest`
- **go-callvis**: `github.com/ofabry/go-callvis@latest`

For platform-specific dependency management implementations, see [powershell.instructions.md](powershell.instructions.md) and [bash.instructions.md](bash.instructions.md).

## Error Handling Standards

### Basic Error Handling Requirements

1. **Fail Fast**: Scripts should exit immediately on critical errors
2. **Clear Messages**: Provide specific error messages with context
3. **Exit Codes**: Use appropriate exit codes (0 for success, 1+ for errors)
4. **Resource Cleanup**: Clean up temporary files and processes on exit

### Cross-Platform Error Handling

Both PowerShell and Bash scripts must implement consistent error handling patterns with platform-appropriate syntax.

For platform-specific error handling implementations, see [powershell.instructions.md](powershell.instructions.md) and [bash.instructions.md](bash.instructions.md).

## Cross-Platform Compatibility

### Path Handling

Both PowerShell and Bash scripts must handle paths correctly across different operating systems.

#### Path Standards

- Use platform-appropriate path construction methods
- Handle spaces in paths correctly
- Use relative paths for component script orchestration
- Calculate project root directory consistently

### Variable Naming

- **PowerShell**: Use PascalCase for variables (`$ProjectRoot`, `$ConfigPath`)
- **Bash**: Use UPPER_SNAKE_CASE for variables (`PROJECT_ROOT`, `CONFIG_PATH`)

For platform-specific path handling implementations, see [powershell.instructions.md](powershell.instructions.md) and [bash.instructions.md](bash.instructions.md).

## Script Categories and Standards

### Backend Tooling Scripts

Scripts that manage Go development tools (`backend/backend_lint`, `backend/backend_gosec`, `backend/backend_callgraph`):

#### Required Parameters

- `SkipInstall` - Skip automatic tool installation/updates
- `VerboseOutput` - Enable verbose output
- `Help` - Display usage information

#### Required Features

- Automatic tool installation and updates
- Cross-platform compatibility
- Comprehensive error handling
- Clear status reporting

### Build Scripts

Scripts that compile and package the application (`build_all`, `backend/backend_build`):

#### Required Features

- Clear build step reporting
- Artifact location reporting
- Error handling with cleanup
- Cross-platform output paths

### Development Scripts

Scripts that set up development environments (`env_dev`):

#### Required Features

- Prerequisite checking
- Service startup coordination
- Clear status reporting
- Graceful shutdown handling

### API Testing Scripts

Scripts that test and validate API endpoints (`test_apis`):

#### Required Parameters

- `BaseUrl` - API base URL (default: http://localhost:8080)
- `Endpoint` - Specific endpoint to test (default: all)
- `Verbose` - Enable verbose output with request/response details
- `Help` - Display usage information

#### Required Features

- Comprehensive endpoint coverage (health, resources, search, schemas, terraform, mcp, audit, discovery)
- Color-coded output for success/failure status
- Detailed request/response logging in verbose mode
- Proper error handling and reporting
- Test result summary with pass/fail counts
- Support for testing specific endpoint groups
- JSON request body validation

## Testing Standards

### Script Testing Requirements

All scripts must be testable with:

#### Basic Functionality Tests

- Help display (`-Help` / `--help`)
- Parameter validation
- Error condition handling
- Success path execution

#### Cross-Platform Tests

- Verify identical behavior between PowerShell and Bash versions
- Test path handling on different platforms
- Validate output formatting consistency

### Manual Testing Checklist

Before committing script changes:

1. **Help Display**: Verify help shows correctly
2. **Parameter Parsing**: Test all parameter combinations
3. **Error Handling**: Test with missing dependencies
4. **SkipInstall Logic**: Test both with and without flag
5. **Cross-Platform**: Test on both Windows and Linux/macOS
6. **Output Formatting**: Verify colors and spacing

## Documentation Standards

### Inline Documentation

- Add comments for complex logic
- Document parameter purposes
- Explain non-obvious operations
- Include examples for complex patterns

### Help Text Requirements

All scripts must include:

- Clear usage syntax
- All available options with descriptions
- Examples showing common usage patterns
- Prerequisites or dependencies

For platform-specific help text implementation patterns, see [powershell.instructions.md](powershell.instructions.md) and [bash.instructions.md](bash.instructions.md).

## Version Control Standards

### Commit Standards

- Always commit PowerShell and Bash versions together
- Test both versions before committing
- Include clear commit messages describing script changes
- Update this instruction file when adding new patterns

### Script Synchronization

- Keep PowerShell and Bash versions functionally identical
- Maintain consistent parameter names (accounting for platform conventions)
- Ensure identical output messages and formatting
- Test cross-platform compatibility regularly

## Security Standards

### Input Validation

```powershell
# PowerShell: Validate file paths
if ($Config) {
    if (-not (Test-Path $Config)) {
        Write-Error "Config file not found: $Config"
        exit 1
    }
}
```

```bash
# Bash: Validate file paths
if [ -n "$CONFIG" ] && [ ! -f "$CONFIG" ]; then
    print_error "Config file not found: $CONFIG"
    exit 1
fi
```

### Safe Execution

- Always validate external tool availability
- Use parameterized execution where possible
- Avoid eval or dynamic command construction
- Sanitize user inputs

## Performance Standards

### Efficient Execution

- Cache command existence checks where possible
- Minimize redundant operations
- Use appropriate process execution methods
- Provide progress feedback for long operations

### Resource Management

- Clean up temporary files
- Handle process cleanup gracefully
- Avoid memory leaks in long-running operations
- Release file handles properly

## Maintenance Standards

### Regular Updates

- Update dependency versions regularly
- Test scripts with new tool versions
- Update help text when adding features
- Maintain compatibility with older tool versions when possible

### Documentation Synchronization

- Update this instruction file when adding new patterns
- Keep script help text current
- Document breaking changes clearly
- Maintain examples with current syntax

This instruction file should be updated whenever new script patterns are established or existing patterns are modified to ensure consistency across the entire project.
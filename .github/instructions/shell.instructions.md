---
applyTo: 'scripts/**/*.sh'
---

# Shell Script Development Standards

This document defines comprehensive shell scripting standards and best practices for consistent, maintainable, and secure shell script development across all projects.

## Shell Script Structure

### Script Header Format

```bash
#!/bin/bash

# [Project Name] [Purpose] Script
# [Brief description of what the script does]

set -e

# Default values
VERBOSE=false
SKIP_INSTALL=false
CONFIG=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --skip-install)
            SKIP_INSTALL=true
            shift
            ;;
        --config|-c)
            CONFIG="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --verbose, -v         Enable verbose output"
            echo "  --skip-install        Skip automatic tool installation/updates"
            echo "  --config, -c PATH     Use custom config file"
            echo "  --help, -h            Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
```

### Parameter Standards

#### Common Parameters

All shell scripts should support these standard parameters where applicable:

- `--help|-h` - Display help information
- `--verbose|-v` - Enable verbose output
- `--skip-install` - Skip automatic tool installation/updates
- `--config|-c PATH` - Custom configuration file path

#### Parameter Naming Conventions

- Use **kebab-case** for long options (`--skip-install`, `--verbose-output`)
- Provide **single-letter shortcuts** where logical (`-v`, `-c`, `-h`)
- Use **descriptive long names** for clarity
- **Always validate** parameter values before use

#### Argument Parsing Best Practices

```bash
# Handle options with values correctly
while [[ $# -gt 0 ]]; do
    case $1 in
        --config|-c)
            if [[ -z "$2" ]] || [[ "$2" == --* ]]; then
                echo "Error: --config requires a value"
                exit 1
            fi
            CONFIG="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --skip-install)
            SKIP_INSTALL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done
```

## Output and Logging Standards

### Color-Coded Output Functions

```bash
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[VERBOSE]${NC} $1"
    fi
}
```

### Output Guidelines

- **Consistent Prefixes**: Use `[INFO]`, `[SUCCESS]`, `[WARNING]`, `[ERROR]` prefixes
- **Color Coding**: Always use appropriate colors for different message types
- **Color Safety**: Ensure colors work in different terminal environments
- **Spacing**: Add blank lines before and after major sections for readability

## Path Handling Standards

### Cross-Platform Path Construction

```bash
# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# For component scripts in subdirectories (scripts/backend/, scripts/frontend/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

# Use proper path construction
CONFIG_PATH="$PROJECT_ROOT/.golangci.yml"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Change directories safely
cd "$BACKEND_DIR" || {
    print_error "Failed to change to backend directory: $BACKEND_DIR"
    exit 1
}
```

### Variable Naming

- Use **UPPER_SNAKE_CASE** for variables (`PROJECT_ROOT`, `CONFIG_PATH`, `SCRIPT_DIR`)
- Use descriptive names that clearly indicate purpose
- Prefer full words over abbreviations (`CONFIG_PATH` vs `CFG_PATH`)
- Quote variables to handle spaces in paths: `"$PROJECT_ROOT"`

## Dependency Management

### Tool Installation Pattern

All shell scripts that use external Go tools must implement the skip-install pattern:

```bash
if command -v tool-name &> /dev/null; then
    if [ "$SKIP_INSTALL" = false ]; then
        print_status "tool-name found, updating to latest version..."
        go install package@latest
        if [ $? -eq 0 ]; then
            print_success "tool-name updated to latest version"
        else
            print_warning "Failed to update tool-name, using existing version"
        fi
    else
        print_status "tool-name found, skipping update (skip-install flag set)"
    fi
else
    if [ "$SKIP_INSTALL" = false ]; then
        print_status "tool-name not found, installing..."
        go install package@latest
        if [ $? -ne 0 ]; then
            print_error "Failed to install tool-name!"
            exit 1
        fi
        print_success "tool-name installed successfully"
    else
        print_error "tool-name not found and skip-install flag is set!"
        print_warning "Please install manually: go install package@latest"
        exit 1
    fi
fi
```

### Command Existence Checking

```bash
# Check for required tools
check_dependencies() {
    local missing_tools=()

    for tool in go npm node; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_warning "Please install missing tools before continuing"
        exit 1
    fi
}
```

### Common Go Tools

- **golangci-lint**: `github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
- **gosec**: `github.com/securecodewarrior/gosec/v2/cmd/gosec@latest`
- **go-callvis**: `github.com/ofabry/go-callvis@latest`

## Error Handling Standards

### Error Action Settings

```bash
# Set at script start
set -e          # Exit on any command failure
set -u          # Exit on undefined variable usage
set -o pipefail # Exit on any failure in pipeline
```

### Process Execution with Error Checking

```bash
# For commands that may fail
if tool "${ARGS[@]}"; then
    print_success "Operation completed successfully!"
else
    exit_code=$?
    print_error "Operation failed! (Exit code: $exit_code)"
    exit 1
fi

# For commands where you need the exit code
go build -o output
exit_code=$?
if [ $exit_code -eq 0 ]; then
    print_success "Go build successful"
else
    print_error "Go build failed with exit code: $exit_code"
    exit 1
fi
```

### Conditional Error Handling

```bash
# When you want to continue despite errors
set +e  # Temporarily disable exit on error
npm install
npm_exit_code=$?
set -e  # Re-enable exit on error

if [ $npm_exit_code -ne 0 ]; then
    print_warning "npm install had issues, but continuing..."
fi
```

### Function Error Handling

```bash
# Functions should return appropriate exit codes
validate_config() {
    local config_file="$1"

    if [ ! -f "$config_file" ]; then
        print_error "Config file not found: $config_file"
        return 1
    fi

    if [[ ! "$config_file" =~ \.(yaml|yml|json)$ ]]; then
        print_error "Config file must be .yaml, .yml, or .json"
        return 1
    fi

    return 0
}

# Usage
if ! validate_config "$CONFIG"; then
    exit 1
fi
```

## Orchestration Patterns

### Component Script Path Construction

```bash
# In utility scripts, call component scripts using relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENT_SCRIPT="$SCRIPT_DIR/backend/backend_gotest.sh"

if [ -f "$COMPONENT_SCRIPT" ]; then
    "$COMPONENT_SCRIPT" "${COMPONENT_ARGS[@]}"
else
    print_warning "Component script not found: $COMPONENT_SCRIPT"
fi
```

### Parameter Passing

```bash
# Prepare component script arguments
COMPONENT_ARGS=()
if [ "$VERBOSE" = true ]; then
    COMPONENT_ARGS+=(--verbose)
fi
if [ "$SKIP_INSTALL" = true ]; then
    COMPONENT_ARGS+=(--skip-install)
fi
if [ -n "$CONFIG" ]; then
    COMPONENT_ARGS+=(--config "$CONFIG")
fi

# Call component script with arguments
"$COMPONENT_SCRIPT" "${COMPONENT_ARGS[@]}"
```

### Array Handling

```bash
# Proper array initialization and usage
declare -a TOOLS=("golangci-lint" "gosec" "go")
declare -a MISSING_TOOLS=()

# Iterating over arrays
for tool in "${TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

# Checking array length
if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    print_error "Missing tools: ${MISSING_TOOLS[*]}"
fi
```

## Security Standards

### Input Validation

```bash
# Validate file paths
validate_file_path() {
    local file_path="$1"

    if [ -z "$file_path" ]; then
        print_error "File path cannot be empty"
        return 1
    fi

    # Check for directory traversal attempts
    if [[ "$file_path" == *".."* ]]; then
        print_error "File path cannot contain directory traversal sequences"
        return 1
    fi

    # Validate file exists
    if [ ! -f "$file_path" ]; then
        print_error "File not found: $file_path"
        return 1
    fi

    return 0
}

# Usage in script
if [ -n "$CONFIG" ]; then
    if ! validate_file_path "$CONFIG"; then
        exit 1
    fi
fi
```

### Safe Execution

```bash
# Always quote variables to prevent word splitting
cd "$PROJECT_ROOT" || exit 1

# Use arrays for commands with multiple arguments
COMMAND_ARGS=("--config" "$CONFIG" "--verbose")
tool "${COMMAND_ARGS[@]}"

# Avoid eval and dynamic command construction
# Bad: eval "go $DYNAMIC_ARGS"
# Good: go "${PREDEFINED_ARGS[@]}"
```

### Environment Variable Handling

```bash
# Safely handle environment variables
SIROS_ENV="${SIROS_ENV:-development}"
SIROS_LOG_LEVEL="${SIROS_LOG_LEVEL:-info}"

# Validate critical environment variables
if [ -z "$HOME" ]; then
    print_error "HOME environment variable is not set"
    exit 1
fi
```

## Performance Standards

### Efficient Execution

```bash
# Cache command existence checks
NPM_EXISTS=false
if command -v npm &> /dev/null; then
    NPM_EXISTS=true
fi

# Use NPM_EXISTS throughout script
if [ "$NPM_EXISTS" = true ]; then
    npm install
fi

# Minimize subprocess creation
# Bad: Multiple calls to basename
for file in *.txt; do
    name=$(basename "$file" .txt)
done

# Good: Use parameter expansion
for file in *.txt; do
    name="${file%.txt}"
done
```

### Resource Management

```bash
# Clean up temporary files
TEMP_FILES=()
cleanup() {
    for temp_file in "${TEMP_FILES[@]}"; do
        [ -f "$temp_file" ] && rm -f "$temp_file"
    done
}

# Set up cleanup trap
trap cleanup EXIT

# Create temporary files
TEMP_FILE=$(mktemp)
TEMP_FILES+=("$TEMP_FILE")
```

### Process Management

```bash
# Handle background processes
BACKGROUND_PIDS=()

start_background_process() {
    local command="$1"
    $command &
    local pid=$!
    BACKGROUND_PIDS+=("$pid")
    print_status "Started background process: $command (PID: $pid)"
}

cleanup_background_processes() {
    for pid in "${BACKGROUND_PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            print_status "Terminating background process: $pid"
            kill "$pid" 2>/dev/null || true
        fi
    done
}

trap cleanup_background_processes EXIT
```

## Testing Standards

### Manual Testing Checklist

Before committing shell script changes:

1. **Help Display**: Test `--help` parameter displays correctly
2. **Parameter Parsing**: Test all parameter combinations
3. **Error Handling**: Test with missing dependencies and invalid inputs
4. **Skip Install Logic**: Test both with and without `--skip-install` flag
5. **Path Resolution**: Test from different working directories
6. **Output Formatting**: Verify colors display correctly in different terminals
7. **Shell Compatibility**: Test on bash 4.0+ and other shells where possible

### Common Test Scenarios

```bash
# Test help
./script.sh --help

# Test verbose output
./script.sh --verbose

# Test with custom config
./script.sh --config custom.yaml

# Test skip install
./script.sh --skip-install

# Test error conditions
./script.sh --config nonexistent.yaml

# Test unknown options
./script.sh --unknown-option
```

### Validation Functions

```bash
# Test script components
test_functions() {
    print_status "Testing script functions..."

    # Test print functions
    print_status "Testing status output"
    print_success "Testing success output"
    print_warning "Testing warning output"
    print_error "Testing error output"

    # Test path resolution
    if [ -d "$PROJECT_ROOT" ]; then
        print_success "Project root found: $PROJECT_ROOT"
    else
        print_error "Project root not found: $PROJECT_ROOT"
        return 1
    fi

    return 0
}
```

## Documentation Standards

### Help Text Requirements

All shell scripts must include comprehensive help:

```bash
show_help() {
    cat << EOF
🔍 Siros [Tool Name]

DESCRIPTION:
  Brief description of what the script does and its purpose.

USAGE:
  $0 [OPTIONS]

OPTIONS:
  --verbose, -v         Enable verbose output with detailed logging
  --skip-install        Skip automatic tool installation/updates
  --config, -c PATH     Use custom config file (yaml/yml/json)
  --help, -h            Show this help message

EXAMPLES:
  $0                          # Run with default settings
  $0 --verbose               # Run with verbose output
  $0 --config custom.yml     # Use custom configuration

DEPENDENCIES:
  - Tool Name (auto-installed if missing)
  - Prerequisites or manual setup requirements

EOF
}
```

### Inline Documentation

```bash
# Complex operations should be documented
# This section handles tool installation and version checking
# because different environments may have different tool versions

# Multi-line operations should explain the workflow
# 1. Check if tool exists
# 2. Install or update if needed
# 3. Verify installation success
```

### Function Documentation

```bash
# Function documentation format
#
# Validates a configuration file path and format
#
# Arguments:
#   $1 - Path to configuration file
#
# Returns:
#   0 - Validation successful
#   1 - Validation failed
#
# Example:
#   if validate_config_file "$CONFIG_PATH"; then
#       echo "Config is valid"
#   fi
validate_config_file() {
    local config_file="$1"
    # Implementation...
}
```

## Version Control Standards

### Commit Standards

- Always commit PowerShell and shell versions together
- Test shell scripts on multiple shells (bash, zsh) where possible
- Include clear commit messages describing shell-specific changes
- Update related instruction files when adding new shell patterns

### Shell Compatibility

```bash
# Ensure compatibility with bash 4.0+
# Check for required bash features
if [ "${BASH_VERSION%%.*}" -lt 4 ]; then
    print_error "This script requires bash 4.0 or later"
    exit 1
fi

# Use POSIX-compliant constructs when possible
# Avoid bash-specific features unless necessary
```

### Portability Considerations

```bash
# Use portable commands
# Good: command -v tool
# Bad: which tool

# Use portable test constructs
# Good: [ -f "$file" ]
# Bad: [[ -f $file ]]

# Quote variables consistently
# Good: cd "$directory"
# Bad: cd $directory
```

## Maintenance Standards

### Regular Updates

- Update shell-specific dependency patterns
- Test scripts with new shell versions
- Keep help text current with parameter changes
- Monitor for shell scripting best practice updates

### Documentation Synchronization

- Update this instruction file when adding new shell patterns
- Keep shell help text consistent with PowerShell equivalents
- Document shell-specific limitations or features
- Maintain examples with current shell syntax

This instruction file should be updated whenever new shell-specific patterns are established or existing patterns are modified to ensure consistency across all shell scripts in the project.
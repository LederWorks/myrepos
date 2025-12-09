---
applyTo: 'scripts/**/*.ps1'
---

# PowerShell Script Development Standards

This document defines PowerShell-specific standards for all PowerShell scripts in the project, ensuring consistency, maintainability, and best practices across all `.ps1` files.

## PowerShell Script Structure

### Script Header Format

```powershell
# [Project Name] [Purpose] Script for PowerShell
# [Brief description of what the script does]

[CmdletBinding()]
param(
    [switch]$VerboseOutput,
    [switch]$SkipInstall,
    [string]$Config = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "🔍 [Project Name] [Tool Name]" -ForegroundColor Blue
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\scripts\script_name.ps1 [options]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -VerboseOutput      Enable verbose output"
    Write-Host "  -SkipInstall        Skip automatic tool installation/updates"
    Write-Host "  -Config <path>      Use custom config file"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\scripts\component\script_name.ps1                    # Run with default settings"
    Write-Host "  .\scripts\component\script_name.ps1 -VerboseOutput     # Run with verbose output"
    exit 0
}

# Set error action preference
$ErrorActionPreference = "Stop"
```

### Parameter Standards

#### Common Parameters

All PowerShell scripts should support these standard parameters where applicable:

- `[switch]$Help` - Display help information
- `[switch]$VerboseOutput` - Enable verbose output (avoid $Verbose due to [CmdletBinding()] conflicts)
- `[switch]$SkipInstall` - Skip automatic tool installation/updates
- `[string]$Config` - Custom configuration file path

#### Parameter Naming Conventions

- Use **PascalCase** for switch parameters (`-SkipInstall`, `-VerboseOutput`)
- Use **PascalCase** for string parameters (`-Config`, `-TestSuite`)
- Always include parameter type declarations (`[switch]`, `[string]`)
- Provide default values where appropriate (`[string]$Config = ""`)

#### [CmdletBinding()] Best Practices

When using `[CmdletBinding()]`:

- **Always use `-VerboseOutput`** instead of `-Verbose` to avoid conflicts with built-in `$VerbosePreference`
- **Avoid common parameter names** that PowerShell reserves (Verbose, Debug, ErrorAction, etc.)
- **Test parameter conflicts** by running with `-Verbose` flag to ensure no conflicts

## Output and Logging Standards

### Color-Coded Output Functions

```powershell
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}
```

### Output Guidelines

- **Consistent Prefixes**: Use `[INFO]`, `[SUCCESS]`, `[WARNING]`, `[ERROR]` prefixes
- **Color Coding**: Always use appropriate colors for different message types
- **Emoji Usage**: Use emojis in script titles for visual appeal (🔍, 🔨, 🧪, 🔒)
- **Spacing**: Add blank lines before and after major sections for readability

## Path Handling Standards

### Cross-Platform Path Construction

```powershell
# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# For component scripts in subdirectories (scripts/backend/, scripts/frontend/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $ScriptsDir

# Use Join-Path for path construction
$ConfigPath = Join-Path $ProjectRoot ".golangci.yml"
$BackendDir = Join-Path $ProjectRoot "backend"

# Change directories safely
Set-Location $BackendDir
```

### Variable Naming

- Use **PascalCase** for variables (`$ProjectRoot`, `$ConfigPath`, `$ScriptDir`)
- Use descriptive names that clearly indicate purpose
- Prefer full words over abbreviations (`$ConfigPath` vs `$CfgPath`)

## Dependency Management

### Tool Installation Pattern

All PowerShell scripts that use external Go tools must implement the SkipInstall pattern:

```powershell
$toolPath = Get-Command tool-name -ErrorAction SilentlyContinue
if ($toolPath) {
    if (-not $SkipInstall) {
        Write-Status "tool-name found, updating to latest version..."
        go install package@latest
        if ($LASTEXITCODE -eq 0) {
            Write-Success "tool-name updated to latest version"
        }
        else {
            Write-Warning "Failed to update tool-name, using existing version"
        }
    }
    else {
        Write-Status "tool-name found, skipping update (SkipInstall flag set)"
    }
}
else {
    if (-not $SkipInstall) {
        Write-Status "tool-name not found, installing..."
        go install package@latest
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install tool-name!"
            exit 1
        }
        Write-Success "tool-name installed successfully"
    }
    else {
        Write-Error "tool-name not found and SkipInstall flag is set!"
        Write-Warning "Please install manually: go install package@latest"
        exit 1
    }
}
```

### Common Go Tools

- **golangci-lint**: `github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
- **gosec**: `github.com/securecodewarrior/gosec/v2/cmd/gosec@latest`
- **go-callvis**: `github.com/ofabry/go-callvis@latest`

## Error Handling Standards

### Error Action Preference

```powershell
# Set at script start
$ErrorActionPreference = "Stop"
```

### Process Execution with Error Checking

```powershell
# For external commands with exit codes
$process = Start-Process -FilePath "tool" -ArgumentList $args -NoNewWindow -Wait -PassThru
$exitCode = $process.ExitCode

if ($exitCode -eq 0) {
    Write-Success "Operation completed successfully!"
}
else {
    Write-Error "Operation failed! (Exit code: $exitCode)"
    exit 1
}

# For Go commands and npm commands
go build -o output.exe
if ($LASTEXITCODE -ne 0) {
    Write-Error "Go build failed!"
    exit 1
}

npm install
if ($LASTEXITCODE -ne 0) {
    Write-Error "npm install failed!"
    exit 1
}
```

### Try-Catch Blocks

```powershell
try {
    # Risky operation
    Set-Location $SomeDirectory
    # More operations
}
catch {
    Write-Error "Operation failed: $($_.Exception.Message)"
    exit 1
}
finally {
    # Cleanup operations
    Set-Location $OriginalLocation
}
```

## Orchestration Patterns

### Component Script Path Construction

```powershell
# In utility scripts, call component scripts using relative paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$componentScript = Join-Path $ScriptDir "backend\backend_gotest.ps1"

if (Test-Path $componentScript) {
    & $componentScript @componentArgs
}
else {
    Write-Warning "Component script not found: $componentScript"
}
```

### Parameter Passing

```powershell
# Prepare component script arguments
$componentArgs = @()
if ($VerboseOutput) { $componentArgs += "-VerboseOutput" }
if ($SkipInstall) { $componentArgs += "-SkipInstall" }
if ($Config) { $componentArgs += "-Config"; $componentArgs += $Config }

# Call component script with splatting
& $componentScript @componentArgs
```

## Security Standards

### Input Validation

```powershell
# Validate file paths
if ($Config) {
    if (-not (Test-Path $Config)) {
        Write-Error "Config file not found: $Config"
        exit 1
    }

    # Validate file extension
    $extension = [System.IO.Path]::GetExtension($Config)
    if ($extension -notin @('.yaml', '.yml', '.json')) {
        Write-Error "Config file must be .yaml, .yml, or .json"
        exit 1
    }
}

# Validate string parameters
if ([string]::IsNullOrWhiteSpace($SomeParameter)) {
    Write-Error "Parameter cannot be empty"
    exit 1
}
```

### Safe Execution

- Always validate external tool availability before use
- Use parameterized execution where possible
- Avoid `Invoke-Expression` or dynamic command construction
- Sanitize user inputs before file operations

## Performance Standards

### Efficient Execution

```powershell
# Cache command existence checks
$npmExists = Get-Command npm -ErrorAction SilentlyContinue
if ($npmExists) {
    # Use npm commands
}

# Minimize redundant operations
if (-not $dependenciesChecked) {
    # Check dependencies once
    $dependenciesChecked = $true
}

# Use appropriate process execution methods
Start-Process vs Invoke-Expression vs &
```

### Resource Management

```powershell
# Clean up temporary files
$tempFiles = @()
try {
    $tempFile = New-TemporaryFile
    $tempFiles += $tempFile
    # Use temp file
}
finally {
    $tempFiles | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
}

# Handle process cleanup gracefully
$backgroundProcesses = @()
try {
    $process = Start-Process -PassThru -FilePath "long-running-tool"
    $backgroundProcesses += $process
}
finally {
    $backgroundProcesses | ForEach-Object {
        if (-not $_.HasExited) {
            $_.Kill()
        }
    }
}
```

## Testing Standards

### Manual Testing Checklist

Before committing PowerShell script changes:

1. **Help Display**: Test `-Help` parameter displays correctly
2. **Parameter Parsing**: Test all parameter combinations
3. **Error Handling**: Test with missing dependencies and invalid inputs
4. **SkipInstall Logic**: Test both with and without `-SkipInstall` flag
5. **Path Resolution**: Test from different working directories
6. **Output Formatting**: Verify colors and spacing display correctly
7. **PowerShell Versions**: Test on PowerShell 5.1 and 7+ where possible

### Common Test Scenarios

```powershell
# Test help
.\script.ps1 -Help

# Test verbose output
.\script.ps1 -VerboseOutput

# Test with custom config
.\script.ps1 -Config "custom.yaml"

# Test skip install
.\script.ps1 -SkipInstall

# Test error conditions
.\script.ps1 -Config "nonexistent.yaml"
```

## Documentation Standards

### Help Text Requirements

All PowerShell scripts must include comprehensive help:

```powershell
if ($Help) {
    Write-Host "🔍 Siros [Tool Name]" -ForegroundColor Blue
    Write-Host ""
    Write-Host "DESCRIPTION:" -ForegroundColor Yellow
    Write-Host "  Brief description of what the script does and its purpose."
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\scripts\script_name.ps1 [options]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -VerboseOutput      Enable verbose output with detailed logging"
    Write-Host "  -SkipInstall        Skip automatic tool installation/updates"
    Write-Host "  -Config <path>      Use custom config file (yaml/yml/json)"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\scripts\script_name.ps1                    # Run with default settings"
    Write-Host "  .\scripts\script_name.ps1 -VerboseOutput     # Run with verbose output"
    Write-Host "  .\scripts\script_name.ps1 -Config custom.yml # Use custom configuration"
    Write-Host ""
    Write-Host "DEPENDENCIES:" -ForegroundColor Yellow
    Write-Host "  - Tool Name (auto-installed if missing)"
    Write-Host "  - Prerequisites or manual setup requirements"
    exit 0
}
```

### Inline Documentation

```powershell
# Complex operations should be documented
# This section handles tool installation and version checking
# because different environments may have different tool versions

# Multi-line operations should explain the workflow
# 1. Check if tool exists
# 2. Install or update if needed
# 3. Verify installation success
```

## Version Control Standards

### Commit Standards

- Always commit PowerShell and Bash versions together
- Test PowerShell scripts on both Windows PowerShell 5.1 and PowerShell 7+
- Include clear commit messages describing PowerShell-specific changes
- Update related instruction files when adding new PowerShell patterns

### PowerShell Version Compatibility

- Write scripts compatible with PowerShell 5.1 minimum
- Use PowerShell 7+ features only when necessary and document requirements
- Test cmdlet availability before use (e.g., `Get-Command Test-Path -ErrorAction SilentlyContinue`)
- Provide fallbacks for newer PowerShell features when possible

## Maintenance Standards

### Regular Updates

- Update PowerShell-specific dependency patterns
- Test scripts with new PowerShell versions
- Keep help text current with parameter changes
- Monitor for PowerShell best practice updates

### Documentation Synchronization

- Update this instruction file when adding new PowerShell patterns
- Keep PowerShell help text consistent with Bash equivalents
- Document PowerShell-specific limitations or features
- Maintain examples with current PowerShell syntax

This instruction file should be updated whenever new PowerShell-specific patterns are established or existing patterns are modified to ensure consistency across all PowerShell scripts in the project.
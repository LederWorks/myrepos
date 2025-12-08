# MyRepos Tools Setup Script (PowerShell)
# Sets up Python virtual environment with required dependencies

$ErrorActionPreference = "Stop"

Write-Host "🔧 Setting up MyRepos Tools..." -ForegroundColor Green

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "📁 Project directory: $ProjectRoot" -ForegroundColor Cyan

# Navigate to project root
Set-Location $ProjectRoot

# Check if Python 3 is available
try {
    $PythonVersion = python --version 2>$null
    if (-not $PythonVersion) {
        $PythonVersion = python3 --version 2>$null
    }
    
    if (-not $PythonVersion) {
        throw "Python not found"
    }
    
    Write-Host "🐍 Python version: $PythonVersion" -ForegroundColor Yellow
    
    # Use python3 if available, otherwise python
    $PythonCmd = "python3"
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        $PythonCmd = "python"
    }
    
} catch {
    Write-Host "❌ Error: Python 3 is required but not found." -ForegroundColor Red
    Write-Host "   Please install Python 3.7+ and try again." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    & $PythonCmd -m venv venv
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    & "venv\Scripts\Activate.ps1"
    $ActivateScript = "venv\Scripts\Activate.ps1"
} else {
    # For PowerShell Core on Linux/macOS
    & "venv/bin/Activate.ps1"
    $ActivateScript = "source venv/bin/activate"
}

# Check if activation was successful
if ($env:VIRTUAL_ENV) {
    $VenvName = Split-Path -Leaf $env:VIRTUAL_ENV
    Write-Host "✅ Virtual environment activated: $VenvName" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
& $PythonCmd -m pip install --upgrade pip

# Install required dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install PyYAML jsonschema jinja2

Write-Host ""
Write-Host "✅ Setup complete! Virtual environment is active." -ForegroundColor Green
Write-Host ""
Write-Host "🚀 You can now use the tools directly:" -ForegroundColor Cyan

if ($IsWindows -or $env:OS -eq "Windows_NT") {
    Write-Host "   python scripts\setup-repository.py C:\path\to\your\repo          # Setup + validation (default)" -ForegroundColor White
    Write-Host "   python scripts\setup-repository.py --validate C:\path\to\your\repo       # Validation only" -ForegroundColor White
    Write-Host "   python scripts\setup-repository.py --quiet C:\path\to\your\repo         # Quiet mode" -ForegroundColor White
} else {
    Write-Host "   python scripts/setup-repository.py /path/to/your/repo          # Setup + validation (default)" -ForegroundColor White
    Write-Host "   python scripts/setup-repository.py --validate /path/to/your/repo       # Validation only" -ForegroundColor White
    Write-Host "   python scripts/setup-repository.py --quiet /path/to/your/repo         # Quiet mode" -ForegroundColor White
}

Write-Host ""
Write-Host "🔄 Virtual environment management:" -ForegroundColor Cyan
Write-Host "   • Currently active: $VenvName" -ForegroundColor White
Write-Host "   • To deactivate when done: deactivate" -ForegroundColor White
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    Write-Host "   • To reactivate later: venv\Scripts\Activate.ps1" -ForegroundColor White
} else {
    Write-Host "   • To reactivate later: source venv/bin/activate" -ForegroundColor White
}
Write-Host ""
Write-Host "💡 The virtual environment will remain active in this terminal session." -ForegroundColor Yellow
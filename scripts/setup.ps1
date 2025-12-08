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
} else {
    # For PowerShell Core on Linux/macOS
    & "venv/bin/Activate.ps1"
}

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
& $PythonCmd -m pip install --upgrade pip

# Install required dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install PyYAML jsonschema jinja2

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 To use the tools:" -ForegroundColor Cyan

if ($IsWindows -or $env:OS -eq "Windows_NT") {
    Write-Host "   venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "   python scripts\workspace\generator.py C:\path\to\your\repo" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Remember to activate the virtual environment before using the tools:" -ForegroundColor Yellow
    Write-Host "   venv\Scripts\Activate.ps1" -ForegroundColor White
} else {
    Write-Host "   source venv/bin/activate" -ForegroundColor White  
    Write-Host "   python scripts/workspace/generator.py /path/to/your/repo" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Remember to activate the virtual environment before using the tools:" -ForegroundColor Yellow
    Write-Host "   source venv/bin/activate" -ForegroundColor White
}
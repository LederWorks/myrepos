#!/bin/bash

# MyRepos Tools Setup Script
# Sets up Python virtual environment with required dependencies

set -e  # Exit on any error

echo "🔧 Setting up MyRepos Tools..."

# Get the script directory (works even when called from elsewhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 Project directory: $PROJECT_ROOT"

# Navigate to project root
cd "$PROJECT_ROOT"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found."
    echo "   Please install Python 3.7+ and try again."
    exit 1
fi

echo "🐍 Python version: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $(basename "$VIRTUAL_ENV")"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install required dependencies
echo "📥 Installing dependencies..."
pip install PyYAML jsonschema jinja2

echo ""
echo "✅ Setup complete! Virtual environment is active."
echo ""
echo "🚀 You can now use the tools directly:"
echo "   python scripts/setup-repository.py /path/to/your/repo          # Setup + validation (default)"
echo "   python scripts/setup-repository.py --validate /path/to/your/repo       # Validation only"
echo "   python scripts/setup-repository.py --quiet /path/to/your/repo         # Quiet mode"
echo ""
echo "🔄 Virtual environment management:"
echo "   • Currently active: $(basename "$VIRTUAL_ENV")"
echo "   • To deactivate when done: deactivate"
echo "   • To reactivate later: source venv/bin/activate"
echo ""
echo "💡 The virtual environment will remain active in this terminal session."
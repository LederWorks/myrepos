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

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install required dependencies
echo "📥 Installing dependencies..."
pip install PyYAML jsonschema jinja2

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To use the tools:"
echo "   source venv/bin/activate"
echo "   python scripts/workspace/generator.py /path/to/your/repo"
echo ""
echo "💡 Remember to activate the virtual environment before using the tools:"
echo "   source venv/bin/activate"
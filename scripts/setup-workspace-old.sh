#!/bin/bash
# scripts/setup-workspace.sh - Setup VS Code workspace and configuration files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(dirname "$SCRIPT_DIR")"
LIB_DIR="$TOOLS_DIR/lib"
TEMPLATES_DIR="$TOOLS_DIR/templates"

# Source the metadata detection library
source "$LIB_DIR/detect-metadata.sh"

# Check dependencies
check_dependencies || exit 1

# Get current repository path
REPO_PATH="$PWD"
REPO_NAME=$(basename "$REPO_PATH")

echo "🔍 Detecting metadata for repository: $REPO_NAME"

# Detect repository metadata
METADATA=$(detect_repo_metadata "$REPO_PATH")
echo "📊 Detected metadata:"
echo "$METADATA" | python3 -m json.tool

# Extract and export individual variables from JSON
export REPO_CLIENT=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['client'])")
export REPO_PLATFORM=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['platform'])") 
export REPO_CLOUD_PROVIDER=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['cloud_provider'])")
export REPO_LANGUAGE=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['language'])")
export REPO_TYPE=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['repo_type'])")
export REPO_NAME=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['repo_name'])")
export REPO_PATH=$(echo "$METADATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['repo_path'])")

echo ""
echo "📁 Setting up workspace and VS Code configuration..."

# Create .vscode directory if it doesn't exist
mkdir -p .vscode

# Generate workspace file
echo "  • Generating ${REPO_NAME}.code-workspace"
render_template "$TEMPLATES_DIR/workspace.json.j2" "${REPO_NAME}.code-workspace"

# Generate VS Code settings
echo "  • Generating .vscode/settings.json"
render_template "$TEMPLATES_DIR/vscode-settings.json.j2" ".vscode/settings.json"

# Generate VS Code extensions
echo "  • Generating .vscode/extensions.json"
render_template "$TEMPLATES_DIR/vscode-extensions.json.j2" ".vscode/extensions.json"

# Update .gitignore
echo "  • Updating .gitignore"
{
    grep -v "\.code-workspace" .gitignore 2>/dev/null || true
    echo "*.code-workspace"
} > .gitignore.tmp && mv .gitignore.tmp .gitignore

echo ""
echo "✅ Setup completed for $REPO_NAME"
echo "   Generated files:"
echo "   - ${REPO_NAME}.code-workspace"
echo "   - .vscode/settings.json"
echo "   - .vscode/extensions.json"
echo "   - Updated .gitignore"
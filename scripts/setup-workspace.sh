#!/bin/bash
# Wrapper script for backward compatibility with mr run

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call the Python script with the current directory as the repository path
python3 "$SCRIPT_DIR/setup-repository.py" "$PWD" --workspace-only
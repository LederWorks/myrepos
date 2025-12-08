#!/usr/bin/env python3
"""
Complete repository setup script
Handles workspace configuration and Copilot instructions generation
"""

import sys
from pathlib import Path

# Import our modules
sys.path.insert(0, str(Path(__file__).parent))

from setup_workspace import WorkspaceGenerator, RepositoryConfig
from generate_copilot_instructions import CopilotInstructionsGenerator


def main():
    """Main entry point for complete repository setup"""
    if len(sys.argv) < 2:
        print("Usage: setup-repository.py <repository_path> [--workspace-only] [--copilot-only]")
        print("")
        print("Options:")
        print("  --workspace-only    Generate only VS Code workspace configuration")
        print("  --copilot-only      Generate only Copilot instructions")
        print("  (default)           Generate both workspace and Copilot instructions")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1]).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Parse command line options
    workspace_only = '--workspace-only' in sys.argv
    copilot_only = '--copilot-only' in sys.argv
    
    # Determine tools directory
    script_dir = Path(__file__).parent
    tools_dir = script_dir.parent
    
    print(f"🚀 Setting up repository: {repo_path.name}")
    print(f"📍 Location: {repo_path}")
    print("")
    
    # Setup workspace configuration
    if not copilot_only:
        print("📁 Setting up VS Code workspace configuration...")
        workspace_generator = WorkspaceGenerator(tools_dir)
        workspace_generator.setup_repository(repo_path)
        print("")
    
    # Generate Copilot instructions
    if not workspace_only:
        print("🤖 Generating GitHub Copilot instructions...")
        copilot_generator = CopilotInstructionsGenerator(tools_dir)
        copilot_generator.generate_instructions(repo_path)
        print("")
    
    print("🎉 Repository setup completed!")
    
    # Show next steps if metadata file was created
    metadata_file = repo_path / '.omd' / 'repository.yaml'
    if metadata_file.exists():
        try:
            config = RepositoryConfig(repo_path)
            print(f"✅ Configuration loaded successfully for {config.metadata['client']}/{config.repo_name}")
        except (FileNotFoundError, ValueError) as e:
            print(f"📝 Next step: Edit {metadata_file} and run the setup again")


if __name__ == '__main__':
    main()
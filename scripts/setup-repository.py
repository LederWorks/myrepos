#!/usr/bin/env python3
"""
Complete repository setup script
Handles workspace configuration and Copilot instructions generation
"""

import sys
from pathlib import Path

# Import our modules
sys.path.insert(0, str(Path(__file__).parent))

from workspace import WorkspaceGenerator, RepositoryConfig


def main():
    """Main entry point for complete repository setup"""
    if len(sys.argv) < 2:
        print("Usage: setup-repository.py <repository_path>")
        print("")
        print("Generates VS Code workspace configuration and GitHub Copilot instructions")
        print("based on repository metadata in .omd/repository.yaml")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1]).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Determine tools directory
    script_dir = Path(__file__).parent
    tools_dir = script_dir.parent
    
    print(f"🚀 Setting up repository: {repo_path.name}")
    print(f"📍 Location: {repo_path}")
    print("")
    
    # Setup workspace configuration (includes Copilot instructions if enabled)
    workspace_generator = WorkspaceGenerator(tools_dir)
    workspace_generator.setup_repository(repo_path)
    
    print("🎉 Repository setup completed!")
    
    # Show next steps if metadata file was created
    metadata_file = repo_path / '.omd' / 'repository.yaml'
    if metadata_file.exists():
        try:
            config = RepositoryConfig(repo_path)
            print(f"✅ Configuration loaded successfully for {config.metadata['client']}/{config.repo_name}")
        except (FileNotFoundError, ValueError):
            print(f"📝 Next step: Edit {metadata_file} and run the setup again")


if __name__ == '__main__':
    main()
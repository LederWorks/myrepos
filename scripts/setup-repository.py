#!/usr/bin/env python3
"""
Complete repository setup and validation script
Handles workspace configuration, Copilot instructions generation, and validation
"""

import argparse
import sys
from pathlib import Path

# Import our modules
sys.path.insert(0, str(Path(__file__).parent))

from validation.validator import SchemaValidator
from workspace.generator import RepositoryConfig, WorkspaceGenerator


def main():
    """Main entry point for repository setup and validation"""
    parser = argparse.ArgumentParser(
        description='Repository setup and validation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Complete repository setup with validation (default)
  python setup-repository.py /path/to/repo
  
  # Setup without validation
  python setup-repository.py --no-validate /path/to/repo
  
  # Validation only
  python setup-repository.py --validate /path/to/repo
  
  # Quiet mode (errors only)
  python setup-repository.py --quiet /path/to/repo
  
  # JSON output for automation
  python setup-repository.py --validate --json /path/to/repo
        """
    )
    
    parser.add_argument('repository_path', type=Path, 
                       help='Path to the repository')
    parser.add_argument('--validate', action='store_true',
                       help='Only validate configuration, do not setup')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation after setup')
    parser.add_argument('--json', action='store_true',
                       help='Output validation results in JSON format')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress all output except errors')
    
    args = parser.parse_args()
    
    if not args.repository_path.exists():
        print(f"Error: Repository path does not exist: {args.repository_path}")
        sys.exit(1)
    
    repo_path = args.repository_path.resolve()
    
    # Determine tools directory
    script_dir = Path(__file__).parent
    tools_dir = script_dir.parent
    
    # Handle validation-only mode
    if args.validate:
        return validate_repository(repo_path, tools_dir, args.json, args.quiet)
    
    # Normal setup mode
    if not args.quiet:
        print(f"🚀 Setting up repository: {repo_path.name}")
        print(f"📍 Location: {repo_path}")
        print("")
    
    # Setup workspace configuration (includes Copilot instructions if enabled)
    workspace_generator = WorkspaceGenerator(tools_dir)
    workspace_generator.setup_repository(repo_path)
    
    if not args.quiet:
        print("🎉 Repository setup completed!")
        
        # Show next steps if metadata file was created
        metadata_file = repo_path / '.omd' / 'repository.yaml'
        if metadata_file.exists():
            try:
                config = RepositoryConfig(repo_path)
                print(f"✅ Configuration loaded successfully for {config.repo_name}")
            except (FileNotFoundError, ValueError):
                print(f"📝 Next step: Edit {metadata_file} and run the setup again")
    
    # Run validation by default (unless --no-validate is specified)
    if not args.no_validate:
        if not args.quiet:
            print("\n🔍 Running validation...")
        return validate_repository(repo_path, tools_dir, args.json, args.quiet)
    
    return 0
def validate_repository(repo_path: Path, tools_dir: Path, json_output: bool = False, quiet: bool = False) -> int:
    """Validate repository configuration"""
    schemas_dir = tools_dir / 'schemas'
    
    if not schemas_dir.exists():
        print(f"Error: Schemas directory not found: {schemas_dir}", file=sys.stderr)
        return 1
    
    validator = SchemaValidator(schemas_dir)
    results = validator.validate_repository(repo_path)
    
    if json_output:
        import json
        print(json.dumps(results, indent=2))
    else:
        from validation.validator import print_results
        print_results([results], quiet)
    
    return 0 if results["valid"] else 1


if __name__ == '__main__':
    main()
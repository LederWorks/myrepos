# Repository Configuration Schema Validator
# A comprehensive validation tool for myrepos .omd/ configuration files

"""
Schema Validation Tool for Repository Configuration

This tool validates .omd/ configuration files against YAML schemas to ensure
repositories are properly configured with correct metadata, language settings,
platform configurations, and workspace setups.

Usage:
    python validate-schemas.py --repository /path/to/repo
    python validate-schemas.py --all-repositories
    python validate-schemas.py --schemas-dir /custom/schemas/path
"""

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install PyYAML", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json

class SchemaValidator:
    """Validates repository configuration files against YAML schemas."""
    
    def __init__(self, schemas_dir: Path):
        """Initialize validator with schemas directory."""
        self.schemas_dir = schemas_dir
        self.schemas = {}
        self.index = {}
        self._load_schemas()
        self._load_index()
    
    def _load_schemas(self):
        """Load all YAML schemas from the schemas directory."""
        for schema_file in self.schemas_dir.glob("*.yaml"):
            if schema_file.name == "index.yaml":
                continue
            
            try:
                with open(schema_file, 'r') as f:
                    schema_content = yaml.safe_load(f)
                    self.schemas[schema_file.stem] = schema_content
            except Exception as e:
                print(f"Warning: Could not load schema {schema_file}: {e}", file=sys.stderr)
    
    def _load_index(self):
        """Load the schema index that defines relationships."""
        index_file = self.schemas_dir / "index.yaml"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    self.index = yaml.safe_load(f)
            except Exception as e:
                print(f"Warning: Could not load index file: {e}", file=sys.stderr)
    
    def get_required_schemas(self, repository_type: str) -> List[str]:
        """Get required schemas for a repository type."""
        if not self.index or 'repository_schemas' not in self.index:
            return ['repository']
        
        type_schemas = self.index['repository_schemas'].get('type_specific_schemas', {})
        if repository_type in type_schemas:
            required = type_schemas[repository_type].get('required_schemas', [])
            # Remove .yaml extension for schema lookup
            return [schema.replace('.yaml', '') for schema in required]
        
        return ['repository']  # Default to base schema
    
    def get_optional_schemas(self, repository_type: str) -> List[str]:
        """Get optional schemas for a repository type."""
        if not self.index or 'repository_schemas' not in self.index:
            return []
        
        type_schemas = self.index['repository_schemas'].get('type_specific_schemas', {})
        if repository_type in type_schemas:
            optional = type_schemas[repository_type].get('optional_schemas', [])
            # Remove .yaml extension for schema lookup
            return [schema.replace('.yaml', '') for schema in optional]
        
        return []
    
    def validate_file(self, file_path: Path, schema_name: str) -> tuple[bool, List[str]]:
        """Validate a single file against a schema."""
        if schema_name not in self.schemas:
            return False, [f"Schema '{schema_name}' not found"]
        
        if not file_path.exists():
            return False, [f"File '{file_path}' not found"]
        
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            
            # Validate against schema
            jsonschema.validate(data, self.schemas[schema_name])
            return True, []
            
        except yaml.YAMLError as e:
            return False, [f"YAML parsing error: {e}"]
        except jsonschema.ValidationError as e:
            return False, [f"Schema validation error: {e.message}"]
        except Exception as e:
            return False, [f"Unexpected error: {e}"]
    
    def validate_repository(self, repo_path: Path) -> Dict[str, Any]:
        """Validate all configuration files in a repository's .omd directory."""
        omd_dir = repo_path / ".omd"
        if not omd_dir.exists():
            return {
                "valid": False,
                "errors": ["No .omd directory found"],
                "repository_path": str(repo_path)
            }
        
        results = {
            "repository_path": str(repo_path),
            "valid": True,
            "errors": [],
            "warnings": [],
            "files_validated": {},
            "repository_type": None
        }
        
        # First, validate repository.yaml to get the repository type
        repo_config_file = omd_dir / "repository.yaml"
        if repo_config_file.exists():
            valid, errors = self.validate_file(repo_config_file, 'repository')
            results["files_validated"]["repository.yaml"] = {
                "valid": valid,
                "errors": errors
            }
            
            if valid:
                with open(repo_config_file, 'r') as f:
                    repo_config = yaml.safe_load(f)
                    results["repository_type"] = repo_config.get("repository_type")
            else:
                results["valid"] = False
                results["errors"].extend([f"repository.yaml: {error}" for error in errors])
        else:
            results["valid"] = False
            results["errors"].append("Required file repository.yaml not found")
            return results
        
        # Get required and optional schemas for this repository type
        repo_type = results["repository_type"]
        if repo_type:
            required_schemas = self.get_required_schemas(repo_type)
            optional_schemas = self.get_optional_schemas(repo_type)
            
            # Validate required schemas
            for schema_name in required_schemas:
                if schema_name == 'repository':  # Already validated
                    continue
                    
                config_file = omd_dir / f"{schema_name}.yaml"
                if config_file.exists():
                    valid, errors = self.validate_file(config_file, schema_name)
                    results["files_validated"][f"{schema_name}.yaml"] = {
                        "valid": valid,
                        "errors": errors
                    }
                    
                    if not valid:
                        results["valid"] = False
                        results["errors"].extend([f"{schema_name}.yaml: {error}" for error in errors])
                else:
                    # Required schema file is missing
                    results["valid"] = False
                    results["errors"].append(f"Required file {schema_name}.yaml not found for repository type '{repo_type}'")
            
            # Validate optional schemas if they exist
            for schema_name in optional_schemas:
                config_file = omd_dir / f"{schema_name}.yaml"
                if config_file.exists():
                    valid, errors = self.validate_file(config_file, schema_name)
                    results["files_validated"][f"{schema_name}.yaml"] = {
                        "valid": valid,
                        "errors": errors
                    }
                    
                    if not valid:
                        results["warnings"].extend([f"{schema_name}.yaml: {error}" for error in errors])
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Validate repository configuration files against schemas')
    parser.add_argument('--schemas-dir', type=Path, 
                       default=Path.home() / 'Data' / 'Tools' / 'myrepos' / 'schemas',
                       help='Path to schemas directory')
    parser.add_argument('--repository', type=Path,
                       help='Path to specific repository to validate')
    parser.add_argument('--all-repositories', action='store_true',
                       help='Validate all repositories in myrepos configuration')
    parser.add_argument('--json-output', action='store_true',
                       help='Output results in JSON format')
    parser.add_argument('--quiet', action='store_true',
                       help='Only show errors')
    
    args = parser.parse_args()
    
    if not args.schemas_dir.exists():
        print(f"Error: Schemas directory not found: {args.schemas_dir}", file=sys.stderr)
        sys.exit(1)
    
    validator = SchemaValidator(args.schemas_dir)
    
    if args.repository:
        # Validate single repository
        results = validator.validate_repository(args.repository)
        
        if args.json_output:
            print(json.dumps(results, indent=2))
        else:
            print_results([results], args.quiet)
            
        sys.exit(0 if results["valid"] else 1)
    
    elif args.all_repositories:
        # TODO: Integrate with myrepos to find all repositories
        print("Error: --all-repositories not yet implemented", file=sys.stderr)
        sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)

def print_results(results_list: List[Dict[str, Any]], quiet: bool = False):
    """Print validation results in human-readable format."""
    total_repos = len(results_list)
    valid_repos = sum(1 for r in results_list if r["valid"])
    
    if not quiet:
        print(f"\nValidation Summary: {valid_repos}/{total_repos} repositories valid\n")
    
    for results in results_list:
        repo_path = results["repository_path"]
        
        if results["valid"]:
            if not quiet:
                print(f"✅ {repo_path}")
                if results["repository_type"]:
                    print(f"   Type: {results['repository_type']}")
                if results["warnings"]:
                    for warning in results["warnings"]:
                        print(f"   ⚠️  {warning}")
        else:
            print(f"❌ {repo_path}")
            if results["repository_type"]:
                print(f"   Type: {results['repository_type']}")
            for error in results["errors"]:
                print(f"   🔥 {error}")
        
        if not quiet:
            print()

if __name__ == "__main__":
    main()
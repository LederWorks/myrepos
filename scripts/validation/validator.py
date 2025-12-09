# Repository Configuration Schema Validator
# A comprehensive validation tool for myrepos .omd/ configuration files

"""
Schema Validation Tool for Repository Configuration

This tool validates .omd/ configuration files against YAML schemas to ensure
repositories are properly configured with correct metadata, language settings,
platform configurations, and workspace setups.

Usage:
    python validate-schemas.py --repository /path/to/repo
    python validate-schemas.py --schemas-dir /custom/schemas/path

    # Use with myrepos to validate all repositories:
    mr run 'python /path/to/validate-schemas.py --repository "$MR_REPO"'
"""

try:
    import os
    import sys

    import yaml
except ImportError:
    print(
        "Error: PyYAML is required. Install with: pip install PyYAML", file=sys.stderr
    )
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print(
        "Error: jsonschema is required. Install with: pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(1)

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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
                with open(schema_file, "r") as f:
                    schema_content = yaml.safe_load(f)
                    self.schemas[schema_file.stem] = schema_content
            except Exception as e:
                print(
                    f"Warning: Could not load schema {schema_file}: {e}",
                    file=sys.stderr,
                )

    def _load_index(self):
        """Load the schema index that defines relationships."""
        index_file = self.schemas_dir / "index.yaml"
        if index_file.exists():
            try:
                with open(index_file, "r") as f:
                    self.index = yaml.safe_load(f)
            except Exception as e:
                print(f"Warning: Could not load index file: {e}", file=sys.stderr)

    def get_required_schemas(self, repository_types: List[str]) -> List[str]:
        """Get required schemas for repository types (array)."""
        if not self.index or "repository_schemas" not in self.index:
            return ["repository"]

        type_schemas = self.index["repository_schemas"].get("type_specific_schemas", {})
        all_required = {"repository"}  # Always include base schema

        for repo_type in repository_types:
            if repo_type in type_schemas:
                required = type_schemas[repo_type].get("required_schemas", [])
                all_required.update(
                    [schema.replace(".yaml", "") for schema in required]
                )

        return list(all_required)

    def get_optional_schemas(self, repository_types: List[str]) -> List[str]:
        """Get optional schemas for repository types (array)."""
        if not self.index or "repository_schemas" not in self.index:
            return []

        type_schemas = self.index["repository_schemas"].get("type_specific_schemas", {})
        all_optional = set()

        for repo_type in repository_types:
            if repo_type in type_schemas:
                optional = type_schemas[repo_type].get("optional_schemas", [])
                all_optional.update(
                    [schema.replace(".yaml", "") for schema in optional]
                )

        return list(all_optional)

    def validate_file(
        self, file_path: Path, schema_name: str
    ) -> tuple[bool, List[str]]:
        """Validate a single file against a schema."""
        if schema_name not in self.schemas:
            return False, [f"Schema '{schema_name}' not found"]

        if not file_path.exists():
            return False, [f"File '{file_path}' not found"]

        try:
            with open(file_path, "r") as f:
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
            return self._create_error_result(repo_path, ["No .omd directory found"])

        results = self._create_initial_results(repo_path)

        # Validate repository.yaml first to get the repository type
        if not self._validate_main_config(omd_dir, results):
            return results

        # Validate type-specific schemas
        self._validate_type_specific_schemas(omd_dir, results)

        return results

    def _create_error_result(
        self, repo_path: Path, errors: List[str]
    ) -> Dict[str, Any]:
        """Create error result dictionary."""
        return {"valid": False, "errors": errors, "repository_path": str(repo_path)}

    def _create_initial_results(self, repo_path: Path) -> Dict[str, Any]:
        """Create initial results dictionary."""
        return {
            "repository_path": str(repo_path),
            "valid": True,
            "errors": [],
            "warnings": [],
            "files_validated": {},
            "repository_type": None,
        }

    def _validate_main_config(self, omd_dir: Path, results: Dict[str, Any]) -> bool:
        """Validate the main repository.yaml file and extract repository type."""
        repo_config_file = omd_dir / "repository.yaml"
        if not repo_config_file.exists():
            results["valid"] = False
            results["errors"].append("Required file repository.yaml not found")
            return False

        valid, errors = self.validate_file(repo_config_file, "repository")
        results["files_validated"]["repository.yaml"] = {
            "valid": valid,
            "errors": errors,
        }

        if valid:
            with open(repo_config_file, "r") as f:
                repo_config = yaml.safe_load(f)
                results["repository_type"] = repo_config.get("types")
            return True
        else:
            results["valid"] = False
            results["errors"].extend([f"repository.yaml: {error}" for error in errors])
            return False

    def _validate_type_specific_schemas(self, omd_dir: Path, results: Dict[str, Any]):
        """Validate schemas specific to the repository type."""
        repo_type = results["repository_type"]
        if not repo_type:
            return

        required_schemas = self.get_required_schemas(repo_type)
        optional_schemas = self.get_optional_schemas(repo_type)

        self._validate_required_schemas(omd_dir, results, required_schemas, repo_type)
        self._validate_optional_schemas(omd_dir, results, optional_schemas)

    def _validate_required_schemas(
        self,
        omd_dir: Path,
        results: Dict[str, Any],
        required_schemas: List[str],
        repo_type: List[str],
    ):
        """Validate required schemas for the repository type."""
        for schema_name in required_schemas:
            if schema_name == "repository":  # Already validated
                continue

            config_file = omd_dir / f"{schema_name}.yaml"
            if config_file.exists():
                self._validate_and_record_schema(
                    config_file, schema_name, results, is_required=True
                )
            else:
                results["valid"] = False
                results["errors"].append(
                    f"Required file {schema_name}.yaml not found for repository type '{repo_type}'"
                )

    def _validate_optional_schemas(
        self, omd_dir: Path, results: Dict[str, Any], optional_schemas: List[str]
    ):
        """Validate optional schemas if they exist."""
        for schema_name in optional_schemas:
            config_file = omd_dir / f"{schema_name}.yaml"
            if config_file.exists():
                self._validate_and_record_schema(
                    config_file, schema_name, results, is_required=False
                )

    def _validate_and_record_schema(
        self,
        config_file: Path,
        schema_name: str,
        results: Dict[str, Any],
        is_required: bool,
    ):
        """Validate a schema file and record the results."""
        valid, errors = self.validate_file(config_file, schema_name)
        results["files_validated"][f"{schema_name}.yaml"] = {
            "valid": valid,
            "errors": errors,
        }

        if not valid:
            if is_required:
                results["valid"] = False
                results["errors"].extend(
                    [f"{schema_name}.yaml: {error}" for error in errors]
                )
            else:
                results["warnings"].extend(
                    [f"{schema_name}.yaml: {error}" for error in errors]
                )


def main():
    parser = argparse.ArgumentParser(
        description="Validate repository configuration files against schemas"
    )
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        default=Path.home() / "Data" / "Tools" / "myrepos" / "schemas",
        help="Path to schemas directory",
    )
    parser.add_argument(
        "--repository", type=Path, help="Path to specific repository to validate"
    )
    parser.add_argument(
        "--json-output", action="store_true", help="Output results in JSON format"
    )
    parser.add_argument("--quiet", action="store_true", help="Only show errors")

    args = parser.parse_args()

    if not args.schemas_dir.exists():
        print(
            f"Error: Schemas directory not found: {args.schemas_dir}", file=sys.stderr
        )
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

    else:
        parser.print_help()
        sys.exit(1)


def print_results(results_list: List[Dict[str, Any]], quiet: bool = False):
    """Print validation results in human-readable format."""
    _print_summary(results_list, quiet)

    for results in results_list:
        _print_repository_result(results, quiet)


def _print_summary(results_list: List[Dict[str, Any]], quiet: bool):
    """Print validation summary statistics."""
    if quiet:
        return

    total_repos = len(results_list)
    valid_repos = sum(1 for r in results_list if r["valid"])
    print(f"\nValidation Summary: {valid_repos}/{total_repos} repositories valid\n")


def _print_repository_result(results: Dict[str, Any], quiet: bool):
    """Print results for a single repository."""
    repo_path = results["repository_path"]

    if results["valid"]:
        _print_valid_repository(results, repo_path, quiet)
    else:
        _print_invalid_repository(results, repo_path)

    if not quiet:
        print()


def _print_valid_repository(results: Dict[str, Any], repo_path: str, quiet: bool):
    """Print results for a valid repository."""
    if quiet:
        return

    print(f"✅ {repo_path}")
    _print_repository_type(results)
    _print_warnings(results)


def _print_invalid_repository(results: Dict[str, Any], repo_path: str):
    """Print results for an invalid repository."""
    print(f"❌ {repo_path}")
    _print_repository_type(results)
    _print_errors(results)


def _print_repository_type(results: Dict[str, Any]):
    """Print repository type if available."""
    if results["repository_type"]:
        print(f"   Type: {results['repository_type']}")


def _print_warnings(results: Dict[str, Any]):
    """Print warnings for a repository."""
    for warning in results["warnings"]:
        print(f"   ⚠️  {warning}")


def _print_errors(results: Dict[str, Any]):
    """Print errors for a repository."""
    for error in results["errors"]:
        print(f"   🔥 {error}")


if __name__ == "__main__":
    main()

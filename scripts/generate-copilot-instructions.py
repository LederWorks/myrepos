#!/usr/bin/env python3
"""
Copilot instructions generator for repositories
Generates .github/copilot-instructions/*.md files based on repository metadata
"""

import os
from pathlib import Path
from typing import Dict, List
import yaml


class CopilotInstructionsGenerator:
    """Generates Copilot instruction files based on repository metadata"""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = self.tools_dir / 'templates' / 'copilot-instructions'
        
    def generate_instructions(self, repo_path: Path) -> None:
        """Generate Copilot instruction files for a repository"""
        repo_path = Path(repo_path)
        
        # Load repository metadata
        metadata_file = repo_path / '.omd' / 'repository.yaml'
        if not metadata_file.exists():
            print(f"❌ No metadata file found: {metadata_file}")
            return
            
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)
        
        # Infer client from path for internal use
        metadata['client'] = self._infer_client_from_path(repo_path)
        
        # Create copilot instructions directory
        instructions_dir = repo_path / '.github' / 'copilot-instructions'
        instructions_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate instructions for each language
        for language in metadata.get('languages', []):
            self._generate_language_instructions(instructions_dir, language, metadata)
        
        # Generate cloud provider instructions
        for provider in metadata.get('cloud_providers', []):
            self._generate_cloud_instructions(instructions_dir, provider, metadata)
        
        # Generate platform instructions
        self._generate_platform_instructions(instructions_dir, metadata.get('platform'), metadata)
        
        print(f"✅ Generated Copilot instructions in {instructions_dir}")
    
    def _infer_client_from_path(self, repo_path: Path) -> str:
        """Infer client from repository path"""
        path_parts = repo_path.parts
        try:
            git_index = path_parts.index('GIT')
            if git_index + 1 < len(path_parts):
                return path_parts[git_index + 1]
        except ValueError:
            pass
        return 'unknown'
    
    def _generate_language_instructions(self, instructions_dir: Path, language: str, metadata: Dict) -> None:
        """Generate language-specific instructions"""
        instructions = {
            'terraform': f"""# Terraform Instructions for {metadata.get('repo_name', 'Repository')}

## Code Style and Standards
- Use consistent naming conventions: snake_case for resources and variables
- Always include descriptions for variables and outputs
- Use data sources instead of hardcoded values when possible
- Follow the standard module structure: main.tf, variables.tf, outputs.tf
- Use locals for computed values and complex expressions

## Best Practices
- Always include version constraints for providers
- Use terraform fmt before committing
- Include validation rules for variables when appropriate
- Use meaningful resource names that reflect their purpose
- Add tags to all resources that support them

## Cloud Provider: {', '.join(metadata.get('cloud_providers', []))}
- Follow cloud provider best practices and naming conventions
- Use provider-specific data sources for dynamic values
- Implement proper IAM policies with least privilege principle
""",
            'python': f"""# Python Instructions for {metadata.get('repo_name', 'Repository')}

## Code Style and Standards
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write comprehensive docstrings for modules, classes, and functions
- Use meaningful variable and function names
- Keep functions small and focused on single responsibility

## Best Practices  
- Use virtual environments for dependency management
- Include requirements.txt or pyproject.toml
- Write unit tests with pytest
- Use logging instead of print statements
- Handle exceptions appropriately with try/except blocks
- Use f-strings for string formatting

## Project Structure
- Organize code into logical modules and packages
- Include __init__.py files for packages
- Use main() function as entry point
- Separate configuration from code
""",
            'javascript': f"""# JavaScript/TypeScript Instructions for {metadata.get('repo_name', 'Repository')}

## Code Style and Standards
- Use ES6+ features and modern JavaScript syntax
- Prefer const/let over var
- Use meaningful variable and function names
- Follow consistent indentation (2 spaces)
- Use semicolons consistently

## Best Practices
- Use async/await for asynchronous operations
- Handle errors appropriately with try/catch
- Use modules (import/export) for code organization  
- Implement proper error handling and validation
- Use ESLint and Prettier for code quality
- Write unit tests with Jest or similar framework

## Project Structure
- Use package.json for dependency management
- Organize code into logical modules
- Use environment variables for configuration
- Include .gitignore for node_modules and build artifacts
""",
            'markdown': f"""# Markdown Documentation Instructions for {metadata.get('repo_name', 'Repository')}

## Writing Standards
- Use clear, concise language appropriate for technical documentation
- Write in present tense and active voice when possible
- Use consistent terminology throughout documentation
- Structure content with logical heading hierarchy (H1 → H2 → H3)
- Keep line length reasonable (80-100 characters) for better readability

## Formatting Rules
- Use ATX-style headers (# ## ###) instead of underlined headers
- Maintain consistent spacing: one blank line before headers, none after
- Use fenced code blocks with language specification: ```bash, ```python, ```yaml
- Use tables for structured data comparison
- Use bullet points (-) for unordered lists, numbers (1.) for ordered lists
- Use reference-style links for repeated URLs

## Content Organization
- Start each document with a brief overview or introduction
- Use a table of contents for documents longer than 3 screens
- Include relevant examples and code snippets
- Add "See also" sections for related documentation
- Document prerequisites and dependencies clearly

## Technical Documentation
- Include installation/setup instructions where relevant
- Provide working code examples that can be copy-pasted
- Include expected output where helpful
- Add troubleshooting sections for common issues
- Include version compatibility information when applicable

## Code Examples
- Ensure all code examples are tested and functional
- Use syntax highlighting with appropriate language tags
- Provide context for code snippets (what they do, when to use them)
- Include error handling in examples where relevant
- Document command-line options and parameters clearly

## Repository Type: {metadata.get('repository_type', 'Unknown')}
- Follow documentation standards appropriate for {metadata.get('repository_type', 'this')} repositories
- Include API documentation if applicable
- Document deployment and configuration procedures
""",
            'yaml': f"""# YAML Configuration Instructions for {metadata.get('repo_name', 'Repository')}

## Structure and Format
- Use consistent indentation (2 spaces, no tabs)
- Quote strings that contain special characters or start with numbers
- Use explicit document start (---) and end (...) markers when needed
- Keep lines under 120 characters when possible

## Best Practices
- Use descriptive keys that clearly indicate their purpose
- Group related configuration items logically
- Include comments for complex configurations
- Validate YAML syntax before committing
- Use anchors (&) and aliases (*) for repeated values

## Documentation
- Include inline comments for non-obvious configurations
- Document required vs optional fields
- Provide examples of valid values
- Include schema validation where applicable

## Repository Type: {metadata.get('repository_type', 'Unknown')}
- Follow YAML conventions appropriate for {metadata.get('repository_type', 'this')} type
- Include validation schemas where beneficial
- Document configuration dependencies and relationships
""",
            'json': f"""# JSON Configuration Instructions for {metadata.get('repo_name', 'Repository')}

## Format Standards
- Use consistent indentation (2 spaces)
- Always use double quotes for strings
- No trailing commas (invalid JSON)
- Use meaningful key names that are self-documenting

## Best Practices
- Validate JSON syntax before committing
- Use schema validation where applicable (JSON Schema)
- Keep nested objects shallow when possible
- Use arrays for ordered data, objects for key-value pairs
- Include version information in configuration files

## Documentation
- Provide JSON Schema files for complex configurations
- Include example files with common use cases
- Document required vs optional fields
- Explain the purpose and valid values for each field

## Repository Type: {metadata.get('repository_type', 'Unknown')}
- Follow JSON conventions appropriate for {metadata.get('repository_type', 'this')} repositories
- Include validation and linting in CI/CD pipelines
""",
            'dockerfile': f"""# Dockerfile Instructions for {metadata.get('repo_name', 'Repository')}

## Best Practices
- Use official base images when possible
- Use specific version tags, avoid 'latest'
- Minimize the number of layers by combining RUN commands
- Use multi-stage builds to reduce image size
- Add labels for metadata and maintainer information

## Security
- Run containers as non-root user when possible
- Use COPY instead of ADD unless you need ADD's extra functionality
- Don't include secrets in the image (use build-time secrets)
- Regularly update base images for security patches
- Scan images for vulnerabilities

## Optimization
- Order Dockerfile instructions from least to most frequently changing
- Use .dockerignore to exclude unnecessary files
- Cache package manager dependencies in separate layers
- Clean up package manager cache in the same RUN command

## Documentation
- Include comments explaining complex steps
- Document exposed ports and volumes
- Provide examples of how to build and run the container
- Document environment variables and their purposes
""",
            'shell': f"""# Shell Script Instructions for {metadata.get('repo_name', 'Repository')}

## Shell Standards
- Use #!/bin/bash or #!/bin/sh shebang appropriately
- Set strict error handling: set -euo pipefail
- Use [[ ]] for conditional tests instead of [ ]
- Quote variables to prevent word splitting: "$variable"
- Use ${{variable}} for parameter expansion

## Best Practices
- Include usage information and help text
- Validate input parameters and provide meaningful error messages
- Use functions to organize code and avoid repetition
- Handle signals appropriately (trap)
- Make scripts idempotent when possible

## Documentation
- Include header comments explaining script purpose
- Document required parameters and environment variables
- Provide usage examples
- Include exit codes documentation
- Add inline comments for complex logic

## Error Handling
- Check command exit codes explicitly
- Provide meaningful error messages
- Clean up temporary files on exit
- Log important operations and errors
"""
        }
        
        if language in instructions:
            file_path = instructions_dir / f"{language}-instructions.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(instructions[language])
            print(f"  ✓ Generated {file_path.name}")
    
    def _generate_cloud_instructions(self, instructions_dir: Path, provider: str, metadata: Dict) -> None:
        """Generate cloud provider-specific instructions"""
        instructions = {
            'aws': f"""# AWS Instructions for {metadata.get('repo_name', 'Repository')}

## Security Best Practices
- Use IAM roles instead of access keys when possible
- Implement least privilege access policies
- Enable CloudTrail for audit logging
- Use AWS Secrets Manager for sensitive data
- Enable encryption at rest and in transit

## Resource Management  
- Use consistent tagging strategy across all resources
- Implement proper resource naming conventions
- Use CloudFormation or Terraform for infrastructure as code
- Monitor costs with Cost Explorer and budgets
- Use AWS Config for compliance monitoring

## Development Practices
- Use AWS CLI profiles for different environments
- Test infrastructure changes in development environments first
- Use AWS SDK best practices for API calls
- Implement proper error handling and retries
""",
            'azure': f"""# Azure Instructions for {metadata.get('repo_name', 'Repository')}

## Security Best Practices
- Use Azure Active Directory for authentication
- Implement RBAC with least privilege principle
- Use Azure Key Vault for secrets management
- Enable Azure Security Center recommendations
- Use managed identities when possible

## Resource Management
- Use consistent naming conventions and tags
- Organize resources in logical resource groups
- Use Azure Resource Manager templates or Terraform
- Monitor costs with Cost Management
- Implement proper backup and disaster recovery

## Development Practices  
- Use Azure CLI or PowerShell for automation
- Test changes in development subscriptions first
- Use Application Insights for monitoring
- Implement proper logging and diagnostics
""",
            'gcp': f"""# Google Cloud Platform Instructions for {metadata.get('repo_name', 'Repository')}

## Security Best Practices
- Use Google Cloud IAM with least privilege
- Enable audit logging and monitoring
- Use Google Secret Manager for sensitive data
- Implement VPC security controls
- Use service accounts for application authentication

## Resource Management
- Use consistent labeling across all resources
- Organize resources in logical projects
- Use Cloud Deployment Manager or Terraform
- Monitor costs with Cloud Billing
- Implement proper backup strategies

## Development Practices
- Use gcloud CLI for automation and management
- Test infrastructure in development projects
- Use Cloud Monitoring and Logging
- Follow Google Cloud best practices documentation
"""
        }
        
        if provider in instructions:
            file_path = instructions_dir / f"{provider}-instructions.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(instructions[provider])
            print(f"  ✓ Generated {file_path.name}")
    
    def _generate_platform_instructions(self, instructions_dir: Path, platform: str, metadata: Dict) -> None:
        """Generate CI/CD platform-specific instructions"""
        instructions = {
            'github': f"""# GitHub Instructions for {metadata.get('repo_name', 'Repository')}

## Repository Management
- Use meaningful commit messages following conventional commits
- Create pull requests for all changes
- Use branch protection rules for main branch
- Enable dependabot for dependency updates
- Use GitHub Issues for tracking work

## CI/CD Best Practices
- Use GitHub Actions for automation
- Implement proper testing in CI pipeline
- Use secrets for sensitive configuration
- Cache dependencies to speed up builds
- Use environments for deployment approvals

## Code Quality
- Use pre-commit hooks for code formatting
- Implement code review requirements
- Use status checks for required CI passes
- Enable security scanning with CodeQL
- Use GitHub Copilot for code assistance
""",
            'azuredevops': f"""# Azure DevOps Instructions for {metadata.get('repo_name', 'Repository')}

## Repository Management  
- Use meaningful commit messages and work item linking
- Create pull requests with proper reviewers
- Use branch policies for protection
- Link commits to work items
- Use Azure Repos Git workflows

## CI/CD Best Practices
- Use Azure Pipelines YAML for pipeline as code  
- Implement proper testing stages
- Use variable groups for configuration
- Implement approval processes for production
- Use Azure Artifacts for package management

## Code Quality
- Enable branch policies with build validation
- Use SonarQube or similar for code analysis
- Implement security scanning in pipelines
- Use pull request templates
- Enable work item integration
"""
        }
        
        if platform in instructions:
            file_path = instructions_dir / f"{platform}-instructions.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(instructions[platform])
            print(f"  ✓ Generated {file_path.name}")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: generate-copilot-instructions.py <repository_path>")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1]).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Determine tools directory
    script_dir = Path(__file__).parent
    tools_dir = script_dir.parent
    
    generator = CopilotInstructionsGenerator(tools_dir)
    generator.generate_instructions(repo_path)


if __name__ == '__main__':
    main()
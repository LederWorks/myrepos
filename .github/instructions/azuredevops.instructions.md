---
applyTo: "**/*"
---
# Azure DevOps Integration Guidelines

This document outlines comprehensive guidelines for working with Azure DevOps as a CI/CD platform, covering pipeline configuration, security, and best practices for any project type.

## Pipeline Configuration

### Pipeline Structure
- All pipeline configurations are located in the `azure-pipelines/` directory
- Pipeline files follow the naming convention: `<pipeline-type>_<scope>_<purpose>.yaml`
- Use YAML pipelines exclusively for consistency and version control

### Pipeline Types
- **build.yaml**: Main build and compilation pipeline
- **test.yaml**: Testing pipeline with unit, integration, and end-to-end tests
- **deploy.yaml**: Deployment pipeline with environment-specific configurations
- **release.yaml**: Semantic versioning and release automation
- **security.yaml**: Security and compliance scanning (SAST, DAST, dependency scanning)
- **quality.yaml**: Code quality analysis and metrics

### Agent Requirements
- Use appropriate agent pools based on workload requirements (Windows, Linux, macOS)
- Agents must have required tools and runtime environments installed
- Configure agent permissions following principle of least privilege
- Use self-hosted agents for specific security or performance requirements

## Build and Deployment Strategy

### Build Operations
- **Compilation**: Use appropriate build tools for the technology stack
- **Testing**: Run unit tests, integration tests, and quality checks
- **Packaging**: Create deployable artifacts with proper versioning
- **Validation**: Perform syntax checking, linting, and security scanning

### Dependency Management
- Cache dependencies to improve build performance
- Use lock files where appropriate for reproducible builds
- Regularly update dependencies and scan for vulnerabilities
- Separate development, test, and production dependency management

### Artifact Management
- Store build artifacts in Azure Artifacts or appropriate artifact storage
- Implement proper versioning strategy (semantic versioning recommended)
- Retention policies for artifacts based on environment and compliance requirements
- Secure artifact storage with appropriate access controls

## Branch Protection and Validation

### Branch Policies
- All commits must pass pipeline validation before merge
- Require pull request reviews before merging to main/master branch
- Automatically trigger appropriate pipelines based on changed files

### Pre-merge Validation
- **Syntax validation**: terraform validate, terraform fmt
- **Security scanning**: Checkov and other security tools
- **Documentation**: Ensure CHANGELOG.md is updated appropriately
- **Version synchronization**: Verify version consistency across files

### Commit Message Validation
- Follow conventional commit message format
- Subject line limited to 50 characters
- Reference work items or issues when applicable
- Use descriptive branch names that indicate the purpose of changes

### Pre-merge Validation
- **Syntax validation**: terraform validate, terraform fmt
- **Security scanning**: Checkov and other security tools
- **Documentation**: Ensure CHANGELOG.md is updated appropriately
- **Version synchronization**: Verify version consistency across files

### Commit Message Validation
- Follow conventional commit message format
- Subject line limited to 50 characters
- Reference work items or issues when applicable
- Use descriptive branch names that indicate the purpose of changes

## Work Item Integration

### Linking Strategy
- Link commits to Azure DevOps work items using #workitem syntax
- Use consistent work item types (User Story, Bug, Task) based on change type
- Reference work items in pull request descriptions

### Traceability
- Maintain traceability from requirements through deployment
- Use work item tags to categorize changes (feature, enhancement, bugfix)
- Track deployment success/failure back to originating work items

## Work Item Integration

### Linking Strategy
- Link commits to Azure DevOps work items using #workitem syntax
- Use consistent work item types (User Story, Bug, Task) based on change type
- Reference work items in pull request descriptions

### Traceability
- Maintain traceability from requirements through deployment
- Use work item tags to categorize changes (feature, enhancement, bugfix)
- Track deployment success/failure back to originating work items

## Release Management

### Version Control
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Automated version bumping through semantic release pipeline
- Tag releases appropriately with version numbers

### Changelog Management
- Automated changelog generation based on conventional commits
- Manual changelog updates for complex changes
- Sync changelog with release notes in Azure DevOps

### Deployment Gates
- Manual approval required for production deployments
- Automated deployment to development/staging environments
- Environment-specific variable groups for configuration

## Security and Compliance

### Service Connections
- Use service principals with minimal required permissions
- Rotate service connection credentials regularly
- Separate service connections for different environments

### Secrets Management
- Store sensitive values in Azure Key Vault
- Reference secrets through Azure DevOps variable groups
- Never commit sensitive values to the repository

### Compliance Scanning
- Integrate security scanning tools (Checkov, Terrascan) in pipelines
- Fail builds on critical security findings
- Generate compliance reports for audit purposes

## Release Management

### Version Control
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Automated version bumping through semantic release pipeline
- Tag releases appropriately with version numbers

### Changelog Management
- Automated changelog generation based on conventional commits
- Manual changelog updates for complex changes
- Sync changelog with release notes in Azure DevOps

### Deployment Gates
- Manual approval required for production deployments
- Automated deployment to development/staging environments
- Environment-specific variable groups for configuration

## Security and Compliance

### Service Connections
- Use service principals with minimal required permissions
- Rotate service connection credentials regularly
- Separate service connections for different environments

### Secrets Management
- Store sensitive values in Azure Key Vault
- Reference secrets through Azure DevOps variable groups
- Never commit sensitive values to the repository

### Compliance Scanning
- Integrate security scanning tools (Checkov, Terrascan) in pipelines
- Fail builds on critical security findings
- Generate compliance reports for audit purposes

## Monitoring and Logging

### Pipeline Monitoring
- Enable pipeline analytics and reporting
- Set up alerts for pipeline failures
- Monitor pipeline performance and optimization opportunities

### Deployment Tracking
- Track deployment success/failure rates
- Monitor infrastructure changes through pipeline logs
- Maintain deployment history for rollback purposes

## Troubleshooting

### Common Issues
- **Lock file conflicts**: Ensure *.lock.hcl files are not committed
- **State conflicts**: Verify backend configuration and permissions
- **Provider version issues**: Check agent capabilities and provider requirements

### Debug Strategies
- Enable verbose logging in pipelines for troubleshooting
- Use pipeline artifacts to preserve diagnostic information
- Leverage Azure DevOps logging and debugging features

## Monitoring and Logging

### Pipeline Monitoring
- Enable pipeline analytics and reporting
- Set up alerts for pipeline failures
- Monitor pipeline performance and optimization opportunities

### Deployment Tracking
- Track deployment success/failure rates
- Monitor infrastructure changes through pipeline logs
- Maintain deployment history for rollback purposes

## Troubleshooting

### Common Issues
- **Lock file conflicts**: Ensure *.lock.hcl files are not committed
- **State conflicts**: Verify backend configuration and permissions
- **Provider version issues**: Check agent capabilities and provider requirements

### Debug Strategies
- Enable verbose logging in pipelines for troubleshooting
- Use pipeline artifacts to preserve diagnostic information
- Leverage Azure DevOps logging and debugging features
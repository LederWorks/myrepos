---
applyTo: "**/*"
---
# Google Cloud Platform (GCP) Guidelines

This document outlines comprehensive guidelines for developing applications and infrastructure on Google Cloud Platform, covering resource organization, security, IAM, and operational best practices.

## GCP Resource Organization

### Hierarchy Structure
- Follow GCP resource hierarchy: Organization → Folder → Project → Resources
- Understand the inheritance model for IAM policies and organizational policies
- Design modules to work at appropriate hierarchy levels (organization, folder, project)
- Support both single-project and multi-project deployments

### Resource Naming
- Follow GCP naming conventions and constraints for each resource type
- Use the external naming convention module for consistent resource naming
- Only expose `*_suffix` variables to maintain naming consistency
- Generate names for both standalone resources and collections

### Project Structure
- Design for multi-project scenarios where appropriate
- Consider project quotas and limitations in module design
- Support cross-project resource references when needed
- Handle project creation vs. existing project scenarios

## IAM Best Practices

### Principle of Least Privilege
- Grant the minimum permissions necessary for the intended function
- Use predefined roles when they provide appropriate permissions
- Create custom roles only when predefined roles are insufficient
- Regularly audit and review granted permissions

### Role Management
- Understand the difference between primitive, predefined, and custom roles
- Use predefined roles whenever possible for better maintainability
- Document custom role permissions clearly with business justification
- Follow role naming conventions: `projects/{project}/roles/{role-id}`

### Service Account Management
- Create service accounts with specific, limited purposes
- Use descriptive names and descriptions for service accounts
- Implement service account key rotation strategies
- Prefer workload identity federation over service account keys when possible

### Policy Bindings
- Use resource-level bindings for fine-grained access control
- Understand conditional IAM policies and their appropriate use cases
- Implement policy inheritance patterns correctly
- Handle policy conflicts and inheritance chains properly

### Member Types
- Support all GCP member types: user, serviceAccount, group, domain, allUsers, allAuthenticatedUsers
- Validate member format according to GCP requirements
- Handle group memberships and nested group scenarios
- Support external identity providers and federated users

## Security Considerations

### Identity and Access
- Implement proper identity verification for all access patterns
- Use Cloud Identity or Google Workspace for user management where appropriate
- Configure appropriate session management and MFA requirements
- Monitor and log all IAM changes through Cloud Audit Logs

### Data Protection
- Classify data sensitivity levels and apply appropriate access controls
- Implement encryption at rest and in transit
- Use Customer-Managed Encryption Keys (CMEK) where required
- Follow data residency and compliance requirements

### Network Security
- Implement proper VPC security controls when IAM modules interact with networking
- Use Private Google Access for secure communication
- Configure appropriate firewall rules and security policies
- Consider VPC Service Controls for additional data protection

### Monitoring and Auditing
- Enable Cloud Audit Logs for all IAM operations
- Configure appropriate log retention policies
- Set up monitoring and alerting for suspicious IAM activities
- Regular access reviews and permission audits

## GCP API and Service Management

### API Enablement
- Ensure required APIs are enabled before creating resources
- Handle API enablement dependencies properly
- Consider API quotas and rate limits in module design
- Implement proper error handling for API-related issues

### Service Dependencies
- Understand service interdependencies (e.g., Cloud Resource Manager, IAM, Cloud Billing)
- Handle service enablement timing and dependencies
- Consider regional and global service availability
- Plan for service deprecation and migration paths

### Resource Quotas
- Design modules to work within default quotas
- Provide guidance on quota increases when necessary
- Handle quota exceeded errors gracefully
- Document quota requirements in module documentation

## Regional and Multi-Regional Considerations

### Resource Location
- Understand which resources are global, regional, or zonal
- Design for appropriate geographic distribution
- Consider data locality and compliance requirements
- Handle cross-region dependencies appropriately

### Disaster Recovery
- Design IAM policies that support disaster recovery scenarios
- Consider cross-region backup and restoration procedures
- Plan for regional service outages and failover scenarios
- Document recovery procedures for IAM configurations

## GCP-Specific Resource Management

### Resource Deletion and Lifecycle
- Understand GCP resource deletion policies and soft delete behaviors
- Implement proper resource lifecycle management
- Handle resource dependencies during destruction
- Consider resource recovery and undelete capabilities

### Billing and Cost Management
- Understand how IAM affects billing account access
- Implement proper billing account IAM policies
- Consider cost allocation and project billing structures
- Monitor and control costs through appropriate IAM restrictions

### Organization Policies
- Understand the interaction between IAM and organization policies
- Design modules that work within organizational constraints
- Handle organization policy inheritance and overrides
- Consider boolean, list, and restore-default policy types

## Integration with GCP Services

### Cloud Resource Manager
- Understand project, folder, and organization resource management
- Handle resource hierarchy operations properly
- Consider resource move operations and their IAM implications
- Support both existing and new resource creation patterns

### Cloud Asset Inventory
- Design modules to work with asset inventory and discovery
- Consider searchability and discoverability of created resources
- Implement proper tagging and labeling strategies
- Support asset export and analysis workflows

### Cloud Security Command Center
- Ensure created resources integrate properly with Security Command Center
- Follow security best practices that align with CSCC findings
- Consider security insights and recommendations in module design
- Support security posture monitoring and alerting

## Testing and Validation

### GCP Resource Testing
- Test modules against actual GCP resources, not mocks
- Validate IAM policy propagation timing and eventual consistency
- Test cross-project and cross-organization scenarios
- Verify resource cleanup and state management

### Environment Isolation
- Use separate GCP projects for development, staging, and production testing
- Implement proper test data isolation and cleanup
- Consider test resource quotas and cost implications
- Document test setup and teardown procedures
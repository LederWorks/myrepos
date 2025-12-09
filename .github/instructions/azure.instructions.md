---
applyTo: "**/*"
---

# Azure Development Standards and Guidelines

This document provides comprehensive guidelines for developing applications and infrastructure on Microsoft Azure, covering resource organization, security, identity management, and operational best practices.

## Azure Resource Organization

### Hierarchy Structure
- Follow Azure resource hierarchy: Management Group → Subscription → Resource Group → Resources
- Understand the inheritance model for Azure policies and role-based access control
- Design modules to work at appropriate hierarchy levels (management group, subscription, resource group)
- Support both single-subscription and multi-subscription deployments

### Resource Naming
- Follow Azure naming conventions and constraints for each resource type
- Use consistent naming patterns across all Azure resources
- Implement standardized naming conventions using variables or locals
- Generate names for both standalone resources and collections
- Consider Azure naming limitations (length, allowed characters, uniqueness requirements)

### Resource Group Structure
- Design for appropriate resource grouping by lifecycle, environment, or application
- Consider resource group limitations and regional constraints
- Support cross-resource group references when needed
- Handle resource group creation vs. existing resource group scenarios
- Plan for resource group deletion and dependency management

## Identity and Access Management (IAM)

### Azure Active Directory (Azure AD)
- Implement proper Azure AD tenant structure and organization
- Use Azure AD groups for role assignment rather than individual users
- Follow principle of least privilege for all role assignments
- Implement conditional access policies where appropriate
- Support multi-tenant scenarios when required

### Role-Based Access Control (RBAC)
- Use built-in Azure roles when they provide appropriate permissions
- Create custom roles only when built-in roles are insufficient
- Document custom role permissions clearly with business justification
- Follow role assignment best practices at appropriate scopes
- Implement role assignment inheritance patterns correctly

### Managed Identity Management
- Use managed identities instead of service principals when possible
- Implement system-assigned managed identities for single-resource scenarios
- Use user-assigned managed identities for multi-resource scenarios
- Avoid storing credentials in code or configuration files
- Implement proper managed identity lifecycle management

### Service Principal Management
- Create service principals with specific, limited purposes when managed identities aren't suitable
- Use descriptive names and descriptions for service principals
- Implement certificate-based authentication over client secrets when possible
- Rotate credentials regularly and implement automated rotation where feasible
- Document service principal usage and ownership clearly

## Security Best Practices

### Network Security
- Implement Virtual Network (VNet) security controls appropriately
- Use Network Security Groups (NSGs) for traffic filtering
- Configure appropriate subnet segmentation and routing
- Implement Azure Firewall or third-party network virtual appliances when needed
- Use Private Endpoints for secure service connectivity

### Data Protection
- Classify data sensitivity levels and apply appropriate protection measures
- Implement encryption at rest using Azure Key Vault or customer-managed keys
- Use encryption in transit for all data communication
- Follow data residency and compliance requirements (GDPR, CCPA, etc.)
- Implement data loss prevention (DLP) policies where required

### Key and Secret Management
- Use Azure Key Vault for all secrets, keys, and certificates
- Implement proper Key Vault access policies and RBAC
- Use Key Vault references in applications instead of hardcoded secrets
- Implement key rotation policies and automated rotation where possible
- Monitor and audit Key Vault access and usage

### Monitoring and Auditing
- Enable Azure Activity Log for all subscription-level operations
- Configure diagnostic settings for all Azure resources
- Set up Azure Monitor and Application Insights for comprehensive monitoring
- Implement security monitoring with Azure Security Center/Microsoft Defender for Cloud
- Regular security assessments and vulnerability scanning

## Azure Service Management

### Compute Services
- Choose appropriate compute services (VMs, App Service, Container Instances, AKS, Functions)
- Implement proper sizing and scaling strategies
- Use availability sets or availability zones for high availability
- Configure backup and disaster recovery for virtual machines
- Implement proper monitoring and alerting for compute resources

### Storage Services
- Select appropriate storage types (Blob, File, Queue, Table, Disk)
- Implement proper access tiers and lifecycle management
- Configure redundancy options based on availability requirements
- Use storage security features (encryption, access policies, network restrictions)
- Monitor storage performance and costs

### Database Services
- Choose appropriate database services (SQL Database, Cosmos DB, PostgreSQL, MySQL)
- Implement proper backup and point-in-time recovery strategies
- Configure high availability and disaster recovery
- Use appropriate security features (TDE, Always Encrypted, firewall rules)
- Monitor database performance and optimize costs

### Networking Services
- Design proper network topology with hub-and-spoke or virtual WAN
- Implement load balancing strategies (Application Gateway, Load Balancer, Traffic Manager)
- Configure DNS services (Azure DNS, Private DNS zones)
- Use appropriate connectivity options (VPN Gateway, ExpressRoute)
- Monitor network performance and security

## Infrastructure as Code (IaC)

### Azure Resource Manager (ARM) Templates
- Use ARM templates for consistent resource deployment
- Implement proper parameterization and variable usage
- Use nested templates and linked templates for modularity
- Follow ARM template best practices for security and performance
- Implement proper error handling and rollback strategies

### Bicep Development
- Use Bicep as a domain-specific language (DSL) for ARM templates
- Implement modular Bicep files for reusability
- Use Bicep parameters and variables effectively
- Follow Bicep best practices for readability and maintainability
- Integrate Bicep with CI/CD pipelines

### Terraform on Azure
- Use the Azure Provider (azurerm) for Terraform deployments
- Implement proper state management with Azure Storage
- Use Terraform modules for reusable infrastructure patterns
- Follow Terraform best practices for Azure resource management
- Implement proper authentication and authorization for Terraform

## DevOps and CI/CD

### Azure DevOps Services
- Use Azure Repos for source control management
- Implement Azure Pipelines for CI/CD automation
- Use Azure Artifacts for package management
- Configure Azure Test Plans for testing workflows
- Integrate with Azure Boards for work item tracking

### GitHub Integration
- Use GitHub Actions with Azure service connections
- Implement proper secret management for GitHub workflows
- Use Azure CLI and PowerShell in GitHub Actions
- Configure proper authentication with Azure from GitHub
- Monitor and audit GitHub-to-Azure deployments

### Deployment Strategies
- Implement blue-green deployments for zero-downtime updates
- Use deployment slots for App Service applications
- Configure rolling updates for container applications
- Implement canary deployments for gradual rollouts
- Use feature flags for controlled feature releases

## Cost Management and Optimization

### Cost Monitoring
- Implement Azure Cost Management and Billing monitoring
- Set up cost alerts and budgets for proactive management
- Use resource tagging for cost allocation and chargeback
- Monitor and analyze spending patterns regularly
- Implement showback and chargeback processes

### Resource Optimization
- Right-size virtual machines and other compute resources
- Use reserved instances and savings plans for predictable workloads
- Implement auto-scaling for variable workloads
- Use spot instances for non-critical, interruptible workloads
- Optimize storage costs with appropriate access tiers

### Governance and Policies
- Implement Azure Policy for compliance and governance
- Use management groups for policy inheritance
- Configure resource locks to prevent accidental deletion
- Implement proper tagging strategies for resource management
- Monitor policy compliance and remediation

## Disaster Recovery and Business Continuity

### Backup Strategies
- Implement Azure Backup for virtual machines and data
- Configure geo-redundant backup storage where appropriate
- Use application-consistent backup for database workloads
- Test backup and restore procedures regularly
- Document recovery time objectives (RTO) and recovery point objectives (RPO)

### Site Recovery
- Use Azure Site Recovery for disaster recovery scenarios
- Configure replication for critical virtual machines and applications
- Test failover and failback procedures regularly
- Document disaster recovery procedures and contact information
- Implement cross-region disaster recovery for critical workloads

### High Availability Design
- Design applications for high availability across availability zones
- Use load balancers and application gateways for traffic distribution
- Implement database high availability with Always On or replication
- Design stateless applications for better scalability and availability
- Monitor application health and implement automatic failover where possible

## Compliance and Regulatory Requirements

### Data Governance
- Implement data classification and labeling strategies
- Use Azure Information Protection for sensitive data
- Configure data retention and deletion policies
- Implement data lineage and audit trails
- Support regulatory compliance requirements (HIPAA, PCI DSS, SOX)

### Security Compliance
- Use Azure Security Center/Microsoft Defender for Cloud for security posture management
- Implement security baselines and benchmarks
- Configure security policies and compliance monitoring
- Perform regular security assessments and penetration testing
- Maintain security documentation and incident response procedures

### Audit and Reporting
- Enable audit logging for all critical resources and operations
- Implement centralized log management with Azure Monitor Logs
- Configure compliance reporting and dashboards
- Perform regular compliance assessments and remediation
- Maintain audit trails for regulatory requirements

## Performance Optimization

### Application Performance
- Use Application Insights for application performance monitoring
- Implement performance testing and optimization strategies
- Configure auto-scaling based on performance metrics
- Optimize database queries and indexing strategies
- Use Content Delivery Network (CDN) for global content distribution

### Network Performance
- Optimize network topology for performance and cost
- Use Azure Front Door for global load balancing and acceleration
- Configure ExpressRoute for predictable network performance
- Monitor network latency and throughput
- Implement network optimization strategies

### Storage Performance
- Choose appropriate storage performance tiers
- Optimize disk performance for virtual machines
- Use premium storage for high-performance workloads
- Implement caching strategies (Azure Cache for Redis)
- Monitor storage performance metrics and optimize accordingly

## Multi-Cloud and Hybrid Scenarios

### Hybrid Cloud Architecture
- Design for hybrid connectivity with Azure Arc
- Implement consistent management across on-premises and cloud
- Use Azure Stack for on-premises Azure services
- Configure hybrid identity with Azure AD Connect
- Implement hybrid backup and disaster recovery strategies

### Multi-Cloud Integration
- Design for cloud portability where business requirements dictate
- Use open standards and avoid vendor lock-in where possible
- Implement consistent security and governance across clouds
- Monitor costs and performance across multiple cloud providers
- Maintain skill sets for multiple cloud platforms

## Troubleshooting and Support

### Common Issues
- Network connectivity problems and resolution strategies
- Authentication and authorization troubleshooting
- Performance bottlenecks identification and resolution
- Cost optimization and billing issue resolution
- Service-specific troubleshooting guides

### Support Resources
- Use Azure Support plans appropriately based on business needs
- Leverage Azure community forums and documentation
- Implement proper logging and monitoring for troubleshooting
- Maintain runbooks for common operational procedures
- Document known issues and their resolutions

### Monitoring and Alerting
- Configure comprehensive monitoring for all critical resources
- Set up proactive alerting for potential issues
- Implement automated remediation where possible
- Use Azure Service Health for service issue notifications
- Monitor and respond to security alerts promptly

This comprehensive guide ensures consistent, secure, and efficient Azure development practices while following Microsoft's recommended patterns and industry best practices.
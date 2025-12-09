---
applyTo: "**/*"
---

# Oracle Cloud Infrastructure (OCI) Development Standards and Guidelines

This document provides comprehensive guidelines for developing applications and infrastructure on Oracle Cloud Infrastructure (OCI), covering resource organization, security, identity management, and operational best practices.

## OCI Resource Organization

### Tenancy and Compartment Structure
- Follow OCI tenancy hierarchy: Root Compartment → Sub-Compartments → Resources
- Design compartment structure based on business units, environments, or projects
- Use compartments for isolation, access control, and cost management
- Implement naming conventions that reflect organizational structure
- Support multi-compartment deployments for enterprise scenarios

### Resource Naming Standards
- Follow OCI naming conventions and constraints for each service
- Use consistent naming patterns across all OCI resources
- Implement standardized naming using tags and resource naming
- Generate names for both standalone resources and collections
- Consider service-specific naming limitations and character restrictions

### Resource Tagging Strategy
- Implement comprehensive tagging for cost allocation and management
- Use consistent tag keys across all resources (Environment, Project, Owner, CostCenter)
- Automate tag application through Infrastructure as Code
- Enforce tagging policies using OCI policies and governance
- Design for tag-based access control and billing allocation

## Identity and Access Management (IAM)

### OCI IAM Best Practices
- Follow principle of least privilege for all policies
- Use groups instead of individual user assignments
- Implement proper policy structure with explicit permissions
- Avoid using tenancy administrator for day-to-day operations
- Enable MFA for all users with console access

### Policy Management
- Use OCI managed policies when they provide appropriate permissions
- Create custom policies only when managed policies are insufficient
- Document custom policy permissions clearly with business justification
- Implement policy inheritance through compartment hierarchy
- Use policy conditions for fine-grained access control

### Identity Providers and Federation
- Integrate with external identity providers (Active Directory, SAML, OIDC)
- Implement federated authentication for enterprise environments
- Use identity domains for user lifecycle management
- Configure single sign-on (SSO) for improved user experience
- Implement proper user provisioning and deprovisioning workflows

### Service Principals and Dynamic Groups
- Use instance principals for compute instance access to OCI services
- Implement dynamic groups for resource-based authentication
- Avoid embedding credentials in application code or configuration
- Use OCI Vault for secrets management
- Implement proper credential rotation strategies

## Security Best Practices

### Network Security
- Implement Virtual Cloud Network (VCN) with proper subnet design
- Use Security Lists and Network Security Groups for traffic control
- Configure appropriate route tables and gateways
- Implement Web Application Firewall (WAF) for application protection
- Use Service Gateway and NAT Gateway for secure service communication

### Data Protection
- Classify data sensitivity and apply appropriate protection measures
- Implement encryption at rest using OCI Vault or customer-managed keys
- Use encryption in transit for all data communication (TLS/SSL)
- Follow data residency and compliance requirements
- Implement data loss prevention and monitoring strategies

### OCI Vault and Key Management
- Use OCI Vault for centralized key and secret management
- Implement proper vault policies and access controls
- Use customer-managed keys for sensitive data encryption
- Implement key rotation policies and automated rotation
- Monitor and audit key usage through audit logs

### Security Monitoring and Compliance
- Enable Cloud Guard for comprehensive security monitoring
- Use Security Zones for automated security policy enforcement
- Configure vulnerability scanning for compute instances
- Implement security baselines and configuration management
- Monitor and respond to security alerts promptly

## OCI Service Management

### Compute Services
- Choose appropriate compute services (VM, Bare Metal, Container Engine, Functions)
- Implement proper instance shapes and auto-scaling strategies
- Use multiple Availability Domains for high availability
- Configure backup strategies for boot and block volumes
- Implement proper monitoring and alerting for compute resources

### Storage Services
- Select appropriate storage services (Object Storage, Block Volume, File Storage)
- Implement proper bucket policies and access controls
- Configure appropriate storage tiers and lifecycle policies
- Use cross-region replication for disaster recovery
- Monitor storage costs and optimize usage patterns

### Database Services
- Choose appropriate database services (Autonomous Database, Database Cloud Service, MySQL)
- Implement high availability with Data Guard or clustering
- Configure automated backups and point-in-time recovery
- Use read replicas for read scaling and disaster recovery
- Monitor database performance and implement optimization strategies

### Networking Services
- Design proper network architecture with VCN peering or transit routing
- Implement load balancing with Load Balancer service
- Configure DNS services with DNS management
- Use FastConnect or VPN for hybrid connectivity
- Monitor network performance and implement optimization strategies

## Infrastructure as Code (IaC)

### OCI Resource Manager
- Use Resource Manager for Terraform-based infrastructure deployment
- Implement proper stack organization and state management
- Use Resource Manager configurations and variables
- Follow Resource Manager best practices for security and performance
- Implement proper rollback and error handling strategies

### Terraform on OCI
- Use the OCI Provider for Terraform deployments
- Implement proper state management with Object Storage
- Use Terraform modules for reusable infrastructure patterns
- Follow Terraform best practices for OCI resource management
- Implement proper authentication using instance principals or API keys

### OCI CLI and SDK Integration
- Use OCI CLI for automation and scripting
- Implement proper authentication and configuration
- Use OCI SDKs for application integration
- Follow SDK best practices for error handling and retry logic
- Implement proper logging and debugging for automation

## DevOps and CI/CD

### OCI DevOps Services
- Use DevOps service for CI/CD automation
- Implement build pipelines with proper artifact management
- Configure deployment pipelines with approval gates
- Use code repositories for source control management
- Integrate with external CI/CD tools and platforms

### Container and Kubernetes Management
- Use Container Engine for Kubernetes (OKE) for container workloads
- Implement proper cluster configuration and node pool management
- Configure auto-scaling for containerized applications
- Use Container Registry for secure image storage
- Implement proper logging and monitoring for containers

### Application Deployment Strategies
- Implement blue-green deployments for zero-downtime updates
- Configure canary deployments for gradual rollouts
- Use rolling updates for stateless applications
- Implement automated testing at multiple deployment stages
- Use Functions service for serverless application deployment

## Cost Management and Optimization

### Cost Monitoring and Analysis
- Use Cost Analysis and Budgets for cost tracking
- Implement cost allocation through compartments and tags
- Set up budget alerts for proactive cost management
- Monitor and analyze usage patterns and trends
- Implement automated cost optimization strategies

### Resource Optimization
- Right-size compute instances using usage metrics
- Use preemptible instances for fault-tolerant workloads
- Implement auto-scaling for variable workloads
- Optimize storage costs with appropriate tiers
- Use cost optimization recommendations and advisors

### Governance and Compliance
- Implement policies for resource governance
- Use compartments for organizational isolation
- Configure audit logging for compliance requirements
- Implement resource quotas and limits
- Monitor compliance with governance policies

## High Availability and Disaster Recovery

### Multi-AD and Multi-Region Deployments
- Design applications across multiple Availability Domains
- Use Load Balancer for traffic distribution
- Implement database high availability with Data Guard
- Design stateless applications for better scalability
- Use multiple regions for disaster recovery scenarios

### Backup and Recovery Strategies
- Implement automated backup strategies for all critical data
- Use cross-region backup replication for disaster recovery
- Configure point-in-time recovery for databases
- Test backup and restore procedures regularly
- Document Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)

### Business Continuity Planning
- Design applications for multi-region deployment
- Use DNS failover for automatic traffic routing
- Implement data replication strategies across regions
- Configure cross-region disaster recovery procedures
- Monitor application health across all regions

## Monitoring and Observability

### OCI Monitoring Integration
- Use Monitoring service for comprehensive resource monitoring
- Implement custom metrics for application-specific monitoring
- Configure alarms for proactive alerting
- Use Logging service for centralized log management
- Implement log analytics for troubleshooting and insights

### Application Performance Monitoring
- Use Application Performance Monitoring (APM) for distributed tracing
- Implement custom instrumentation and metrics collection
- Monitor application performance and user experience
- Configure performance alerting and automated remediation
- Use health checks for service availability monitoring

### Operations Insights and Analytics
- Enable Operations Insights for automated performance analysis
- Use Management Agent for comprehensive system monitoring
- Configure capacity planning and resource optimization
- Implement predictive analytics for proactive management
- Monitor and optimize resource utilization patterns

## Database Design and Management

### Autonomous Database Services
- Choose appropriate Autonomous Database workload types (OLTP, DW, JSON)
- Implement proper database security and access controls
- Use Autonomous Database features for performance optimization
- Configure automated patching and maintenance
- Monitor database performance with built-in tools

### Traditional Database Services
- Select appropriate database editions based on requirements
- Implement high availability with Data Guard
- Configure backup and recovery strategies
- Use database performance monitoring and tuning
- Implement proper database security and encryption

### Data Integration and Analytics
- Use Data Integration service for ETL/ELT workflows
- Implement data lake architecture with Object Storage
- Use Analytics Cloud for business intelligence
- Configure appropriate data retention and archiving
- Monitor data pipeline performance and optimization

## Compliance and Regulatory Requirements

### Data Governance and Privacy
- Implement data classification and protection strategies
- Use Data Safe for database security assessment
- Configure data retention and deletion policies
- Implement data lineage tracking and audit capabilities
- Support regulatory compliance requirements (GDPR, HIPAA, SOX)

### Security Compliance Frameworks
- Implement security best practices and benchmarks
- Use Security Zones for automated compliance enforcement
- Configure compliance monitoring and reporting
- Perform regular security assessments and penetration testing
- Maintain security documentation and incident response procedures

### Audit and Compliance Reporting
- Enable comprehensive audit logging across all services
- Implement centralized log management and retention
- Configure compliance dashboards and reporting
- Perform regular compliance assessments and remediation
- Maintain audit trails for regulatory requirements

## Performance Optimization

### Application Performance Tuning
- Use Content Delivery Network for global content delivery
- Implement caching strategies with appropriate services
- Optimize database queries and indexing strategies
- Use connection pooling and connection management
- Monitor and optimize application response times

### Network Performance Optimization
- Design network architecture for optimal performance
- Use FastConnect for predictable network performance
- Configure appropriate bandwidth and routing
- Monitor network latency and throughput
- Implement network optimization strategies

### Storage Performance Tuning
- Choose appropriate block volume performance tiers
- Implement proper I/O optimization strategies
- Use appropriate storage classes for different workloads
- Monitor storage performance metrics
- Optimize storage costs while maintaining performance

## Hybrid and Multi-Cloud Integration

### Hybrid Cloud Architecture
- Design for hybrid connectivity with on-premises systems
- Use FastConnect for dedicated network connectivity
- Implement consistent security and governance policies
- Configure hybrid identity and access management
- Monitor and manage hybrid deployments

### Multi-Cloud Strategy
- Design for cloud portability where business requirements dictate
- Use open standards and avoid vendor lock-in
- Implement consistent monitoring and management
- Plan for data mobility and integration across clouds
- Maintain skills and expertise across multiple platforms

## Troubleshooting and Support

### Common Issues Resolution
- Network connectivity troubleshooting across regions and on-premises
- IAM policy and permission troubleshooting
- Performance bottleneck identification and resolution
- Cost optimization and billing issue resolution
- Service-specific troubleshooting procedures

### OCI Support Integration
- Choose appropriate support level based on business requirements
- Leverage OCI documentation and knowledge base
- Use support ticket system for technical issues
- Implement proper escalation procedures for critical issues
- Document common issues and resolution procedures

### Operational Excellence
- Implement operational best practices and frameworks
- Use automation for routine operational tasks
- Configure comprehensive monitoring and alerting
- Maintain operational runbooks and procedures
- Implement continuous improvement processes

## Migration and Modernization

### Cloud Migration Strategies
- Assess current infrastructure and applications
- Choose appropriate migration strategies (lift-and-shift, refactor, rebuild)
- Use migration tools and services for data transfer
- Implement phased migration approach
- Test and validate migrated applications

### Application Modernization
- Evaluate applications for cloud-native patterns
- Implement microservices and containerization
- Use serverless computing where appropriate
- Modernize data architecture and analytics
- Implement DevOps and automation practices

### Legacy System Integration
- Design integration patterns for legacy systems
- Use middleware and integration services
- Implement API gateways for service exposure
- Plan for gradual legacy system retirement
- Maintain business continuity during transition

This comprehensive guide ensures consistent, secure, and efficient OCI development practices while following Oracle's recommended patterns and industry best practices.
---
applyTo: "**/*"
---

# AWS Development Standards and Guidelines

This document provides comprehensive guidelines for developing applications and infrastructure on Amazon Web Services (AWS), covering resource organization, security, identity management, and operational best practices.

## AWS Resource Organization

### Account Structure
- Follow AWS multi-account strategy with AWS Organizations for enterprise environments
- Implement proper account hierarchy: Root Organization → Organizational Units → Member Accounts
- Use separate accounts for different environments (development, staging, production)
- Design modules to work across account boundaries where appropriate
- Support both single-account and multi-account deployments

### Resource Naming
- Follow AWS naming conventions and constraints for each service
- Use consistent naming patterns across all AWS resources
- Implement standardized naming conventions using tags and resource naming
- Generate names for both standalone resources and collections
- Consider AWS service-specific naming limitations and requirements

### Resource Tagging Strategy
- Implement comprehensive tagging strategy for cost allocation and management
- Use consistent tag keys across all resources (Environment, Project, Owner, CostCenter)
- Automate tag application through Infrastructure as Code
- Enforce tagging policies using AWS Config and Service Control Policies
- Design for tag-based access control and billing allocation

## Identity and Access Management (IAM)

### AWS IAM Best Practices
- Follow principle of least privilege for all IAM policies
- Use IAM roles instead of IAM users for programmatic access
- Implement proper IAM policy structure with explicit permissions
- Avoid using AWS root account for day-to-day operations
- Enable MFA for all IAM users with console access

### Role-Based Access Control
- Use AWS managed policies when they provide appropriate permissions
- Create custom policies only when managed policies are insufficient
- Document custom policy permissions clearly with business justification
- Implement role assumption patterns for cross-account access
- Use IAM policy conditions for fine-grained access control

### Service-Linked Roles and Service Roles
- Use service-linked roles for AWS services when available
- Implement service roles for EC2 instances, Lambda functions, and other compute resources
- Avoid embedding credentials in application code or configuration
- Use AWS Systems Manager Parameter Store or AWS Secrets Manager for secrets
- Implement proper credential rotation strategies

### Cross-Account Access
- Design IAM roles for secure cross-account resource access
- Use external IDs for enhanced security in cross-account scenarios
- Implement proper trust policies with condition constraints
- Document cross-account access patterns and dependencies
- Monitor and audit cross-account role usage

## Security Best Practices

### Network Security
- Implement Virtual Private Cloud (VPC) with proper subnet design
- Use Security Groups and Network ACLs for defense in depth
- Configure appropriate routing tables and internet gateways
- Implement AWS WAF and Shield for application protection
- Use VPC Endpoints for secure service communication

### Data Protection
- Classify data sensitivity and apply appropriate protection measures
- Implement encryption at rest using AWS KMS or customer-managed keys
- Use encryption in transit for all data communication (TLS/SSL)
- Follow data residency and compliance requirements
- Implement data loss prevention and monitoring strategies

### Key Management Service (KMS)
- Use AWS KMS for centralized key management
- Implement proper key policies and IAM permissions
- Use customer-managed keys for sensitive data encryption
- Implement key rotation policies and automated rotation
- Monitor and audit key usage through CloudTrail

### Secrets Management
- Use AWS Secrets Manager for database credentials and API keys
- Implement automatic secret rotation where possible
- Use Systems Manager Parameter Store for configuration parameters
- Avoid hardcoding secrets in application code or infrastructure templates
- Implement proper secret access logging and monitoring

## AWS Service Management

### Compute Services
- Choose appropriate compute services (EC2, ECS, EKS, Lambda, Fargate)
- Implement proper instance sizing and auto-scaling strategies
- Use multiple Availability Zones for high availability
- Configure backup strategies for EC2 instances and EBS volumes
- Implement proper monitoring and alerting for compute resources

### Storage Services
- Select appropriate storage services (S3, EBS, EFS, FSx)
- Implement proper S3 bucket policies and access controls
- Configure appropriate storage classes and lifecycle policies
- Use S3 Cross-Region Replication for disaster recovery
- Monitor storage costs and optimize usage patterns

### Database Services
- Choose appropriate database services (RDS, DynamoDB, DocumentDB, Aurora)
- Implement Multi-AZ deployments for high availability
- Configure automated backups and point-in-time recovery
- Use read replicas for read scaling and disaster recovery
- Monitor database performance and implement optimization strategies

### Networking Services
- Design proper network architecture with VPC peering or Transit Gateway
- Implement load balancing with Application Load Balancer and Network Load Balancer
- Configure DNS services with Route 53 for high availability
- Use Direct Connect or VPN for hybrid connectivity
- Monitor network performance and implement optimization strategies

## Infrastructure as Code (IaC)

### AWS CloudFormation
- Use CloudFormation for consistent resource deployment
- Implement proper template organization with nested stacks
- Use CloudFormation parameters and mappings effectively
- Follow CloudFormation best practices for security and performance
- Implement proper rollback and error handling strategies

### AWS CDK Development
- Use AWS CDK for programmatic infrastructure definition
- Implement reusable CDK constructs and patterns
- Follow CDK best practices for maintainability and testing
- Use CDK context and feature flags appropriately
- Integrate CDK with CI/CD pipelines for automated deployment

### Terraform on AWS
- Use the AWS Provider for Terraform deployments
- Implement proper state management with S3 and DynamoDB
- Use Terraform modules for reusable infrastructure patterns
- Follow Terraform best practices for AWS resource management
- Implement proper authentication using IAM roles

## DevOps and CI/CD

### AWS DevOps Services
- Use AWS CodeCommit for source control (or integrate with GitHub)
- Implement CodePipeline for CI/CD automation
- Use CodeBuild for build and test automation
- Configure CodeDeploy for application deployment strategies
- Integrate with AWS X-Ray for distributed tracing

### CI/CD Pipeline Design
- Implement multi-stage pipelines with proper approval gates
- Use blue-green deployments for zero-downtime updates
- Configure canary deployments for gradual rollouts
- Implement automated testing at multiple pipeline stages
- Use AWS Systems Manager for deployment automation

### Container Orchestration
- Use Amazon ECS or EKS for container workloads
- Implement proper task definitions and service configurations
- Configure auto-scaling for containerized applications
- Use AWS Fargate for serverless container execution
- Implement proper logging and monitoring for containers

## Cost Management and Optimization

### Cost Monitoring
- Use AWS Cost Explorer and Cost and Usage Reports
- Implement cost allocation tags for detailed billing analysis
- Set up billing alerts and budgets for proactive cost management
- Monitor and analyze Reserved Instance and Savings Plans utilization
- Implement automated cost optimization strategies

### Resource Optimization
- Right-size EC2 instances using AWS Compute Optimizer
- Use Spot Instances for fault-tolerant and flexible workloads
- Implement auto-scaling for variable workloads
- Optimize storage costs with appropriate S3 storage classes
- Use AWS Trusted Advisor for cost optimization recommendations

### Governance and Compliance
- Implement AWS Config for resource compliance monitoring
- Use Service Control Policies (SCPs) for organizational governance
- Configure AWS CloudTrail for audit logging and compliance
- Implement resource tagging policies for cost allocation
- Monitor compliance with AWS Security Hub and AWS Well-Architected Tool

## High Availability and Disaster Recovery

### Multi-AZ Deployments
- Design applications across multiple Availability Zones
- Use Elastic Load Balancing for traffic distribution
- Implement database Multi-AZ deployments for automatic failover
- Design stateless applications for better scalability
- Use Auto Scaling Groups for automatic instance replacement

### Backup and Recovery
- Implement automated backup strategies for all critical data
- Use AWS Backup for centralized backup management
- Configure cross-region backup replication for disaster recovery
- Test backup and restore procedures regularly
- Document Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)

### Cross-Region Architecture
- Design applications for multi-region deployment where required
- Use Route 53 health checks for DNS failover
- Implement data replication strategies across regions
- Configure cross-region disaster recovery procedures
- Monitor application health across all regions

## Monitoring and Observability

### CloudWatch Integration
- Use CloudWatch metrics for comprehensive resource monitoring
- Implement custom metrics for application-specific monitoring
- Configure CloudWatch alarms for proactive alerting
- Use CloudWatch Logs for centralized log management
- Implement CloudWatch Insights for log analysis and troubleshooting

### Application Performance Monitoring
- Use AWS X-Ray for distributed application tracing
- Implement Application Insights and custom instrumentation
- Monitor application performance metrics and user experience
- Configure performance alerting and automated remediation
- Use AWS Personal Health Dashboard for service issue notifications

### Security Monitoring
- Enable AWS CloudTrail for all API activity logging
- Use AWS Config for resource configuration monitoring
- Implement AWS Security Hub for centralized security findings
- Configure Amazon GuardDuty for threat detection
- Monitor and respond to security alerts promptly

## Serverless Architecture

### AWS Lambda Best Practices
- Design functions for single responsibility and statelessness
- Implement proper error handling and retry logic
- Use appropriate memory and timeout configurations
- Implement Lambda layers for shared code and dependencies
- Monitor Lambda performance and cost optimization

### Event-Driven Architecture
- Use Amazon EventBridge for event routing and processing
- Implement proper event schema design and versioning
- Use SQS and SNS for reliable message processing
- Design for eventual consistency in distributed systems
- Implement proper dead letter queue handling

### API Gateway Integration
- Use API Gateway for RESTful API management
- Implement proper authentication and authorization
- Configure request/response transformation and validation
- Use API Gateway caching for performance optimization
- Monitor API usage and implement rate limiting

## Database Design and Management

### Relational Databases (RDS/Aurora)
- Choose appropriate database engine based on requirements
- Implement proper database security with encryption and access controls
- Use Parameter Groups for database configuration management
- Implement read replicas for read scaling and disaster recovery
- Monitor database performance with Performance Insights

### NoSQL Databases (DynamoDB)
- Design appropriate partition key and sort key strategies
- Implement proper access patterns and query optimization
- Use DynamoDB Streams for real-time data processing
- Configure appropriate read/write capacity and auto-scaling
- Monitor DynamoDB performance and cost optimization

### Data Warehousing and Analytics
- Use Amazon Redshift for data warehousing requirements
- Implement proper data lake architecture with S3 and Lake Formation
- Use Amazon Athena for serverless query processing
- Configure appropriate data lifecycle and archiving strategies
- Monitor query performance and cost optimization

## Compliance and Regulatory Requirements

### Data Governance
- Implement data classification and protection strategies
- Use AWS Macie for sensitive data discovery and protection
- Configure data retention and deletion policies
- Implement data lineage tracking and audit capabilities
- Support regulatory compliance requirements (GDPR, HIPAA, PCI DSS)

### Security Compliance Frameworks
- Implement AWS security best practices and benchmarks
- Use AWS Security Hub for compliance posture management
- Configure compliance monitoring with AWS Config Rules
- Perform regular security assessments and penetration testing
- Maintain security documentation and incident response procedures

### Audit and Reporting
- Enable comprehensive audit logging with CloudTrail and Config
- Implement centralized log management and retention
- Configure compliance reporting and dashboards
- Perform regular compliance assessments and remediation
- Maintain audit trails for regulatory requirements

## Performance Optimization

### Application Performance
- Use CloudFront CDN for global content delivery and caching
- Implement ElastiCache for in-memory caching strategies
- Optimize database queries and indexing strategies
- Use connection pooling and connection management best practices
- Monitor and optimize application response times

### Network Performance
- Design network architecture for optimal performance and cost
- Use placement groups for high-performance computing workloads
- Configure appropriate instance types for network-intensive applications
- Monitor network latency and throughput across regions
- Implement network optimization strategies

### Storage Performance
- Choose appropriate EBS volume types based on performance requirements
- Use S3 Transfer Acceleration for global data uploads
- Implement proper S3 multipart upload strategies
- Monitor storage performance metrics and optimize accordingly
- Use appropriate storage classes for cost and performance balance

## Troubleshooting and Support

### Common Issues Resolution
- Network connectivity troubleshooting across VPCs and regions
- IAM permissions and policy troubleshooting
- Performance bottleneck identification and resolution
- Cost anomaly investigation and optimization
- Service-specific troubleshooting procedures

### AWS Support Integration
- Choose appropriate AWS Support plan based on business requirements
- Leverage AWS Trusted Advisor recommendations
- Use AWS Personal Health Dashboard for proactive issue identification
- Implement proper escalation procedures for critical issues
- Document common issues and resolution procedures

### Operational Excellence
- Implement AWS Well-Architected Framework principles
- Use AWS Systems Manager for operational automation
- Configure comprehensive monitoring and alerting strategies
- Maintain operational runbooks and procedures
- Implement continuous improvement processes

This comprehensive guide ensures consistent, secure, and efficient AWS development practices while following Amazon's Well-Architected Framework principles and industry best practices.
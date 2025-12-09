---
applyTo: "**/*.yaml,**/*.yml,**/*.yaml.j2,**/*.yml.j2"
---

# YAML Development Standards and Guidelines

This document defines comprehensive standards for YAML file development, configuration management, and template creation across all projects, ensuring consistency, maintainability, and best practices.

## YAML File Structure Standards

### File Naming Conventions

- Use **lowercase** with **kebab-case** for multi-word files: `database-config.yaml`
- Use **descriptive names** that indicate purpose: `deployment-config.yaml`, `ci-pipeline.yml`
- Prefer **`.yaml`** extension over `.yml` for clarity and consistency
- Use **`.yml`** only when character limits require it (legacy systems, specific tools)

### File Organization

```yaml
# Header comment explaining the file purpose
# Author: Team Name
# Last Modified: YYYY-MM-DD
# Purpose: Brief description of configuration

# Version information (for configuration files)
apiVersion: v1
kind: ConfigMap

# Metadata section
metadata:
  name: application-config
  namespace: production
  labels:
    app: myapp
    environment: production
    version: "1.0.0"

# Main configuration data
data:
  database:
    host: "localhost"
    port: 5432
    name: "myapp_db"
    ssl_mode: "require"
  
  cache:
    provider: "redis"
    ttl: 3600
    cluster_mode: true
```

## YAML Syntax Standards

### Indentation and Spacing

- Use **2 spaces** for indentation consistently
- **Never use tabs** - configure editor to show whitespace
- **Align values** at the same indentation level
- Add **blank lines** between major sections for readability

```yaml
# ✅ GOOD: Consistent 2-space indentation
application:
  name: "myapp"
  version: "1.0.0"
  
  database:
    host: "localhost"
    port: 5432
    
  cache:
    enabled: true
    ttl: 3600

# ❌ BAD: Inconsistent indentation
application:
    name: "myapp"
  version: "1.0.0"
database:
      host: "localhost"
   port: 5432
```

### Quoting Standards

- **Quote strings** that contain special characters, numbers that should be strings, or reserved words
- **Consistent quoting** within the same configuration section
- **Boolean values** should not be quoted: `true`, `false`, `null`
- **Numeric values** should not be quoted unless they need to be strings

```yaml
# ✅ GOOD: Appropriate quoting
database:
  host: "localhost"        # String value
  port: 5432               # Numeric value
  ssl_enabled: true        # Boolean value
  version: "14.5"          # Version as string
  password: ""             # Empty string
  
environment:
  NODE_ENV: "production"   # Environment variable
  DEBUG: false             # Boolean flag
  API_VERSION: "v1"        # Version identifier

# ❌ BAD: Incorrect quoting
database:
  host: localhost          # Should be quoted for consistency
  port: "5432"             # Numeric value quoted unnecessarily
  ssl_enabled: "true"      # Boolean quoted as string
```

### Array and Object Formatting

#### Compact Arrays (Short Lists)
```yaml
# ✅ GOOD: Short arrays on single line
tags: ["production", "web", "api"]
ports: [80, 443, 8080]
environments: ["dev", "staging", "prod"]
```

#### Multi-line Arrays (Complex Items)
```yaml
# ✅ GOOD: Complex arrays with proper formatting
servers:
  - name: "web-01"
    ip: "192.168.1.10"
    role: "frontend"
    
  - name: "web-02" 
    ip: "192.168.1.11"
    role: "frontend"
    
  - name: "db-01"
    ip: "192.168.1.20"
    role: "database"
```

#### Complex Objects
```yaml
# ✅ GOOD: Nested object structure
application:
  metadata:
    name: "myapp"
    version: "1.0.0"
    description: "Production web application"
    
  configuration:
    database:
      primary:
        host: "db.example.com"
        port: 5432
        ssl: true
      replica:
        host: "db-replica.example.com"
        port: 5432
        readonly: true
        
    cache:
      redis:
        cluster: ["redis-01:6379", "redis-02:6379", "redis-03:6379"]
        password: "${REDIS_PASSWORD}"
        db: 0
```

## Configuration Management Standards

### Environment-Specific Configurations

#### Base Configuration Pattern
```yaml
# base-config.yaml - Common settings
application:
  name: "myapp"
  log_level: "info"
  
database:
  pool_size: 10
  timeout: 30
  
cache:
  provider: "redis"
  ttl: 3600
```

#### Environment Overrides
```yaml
# production-config.yaml - Production-specific overrides
application:
  log_level: "warn"
  debug: false
  
database:
  pool_size: 50
  ssl: true
  backup_enabled: true
  
monitoring:
  enabled: true
  metrics_endpoint: "/metrics"
  health_check: "/health"
```

#### Development Configuration
```yaml
# development-config.yaml - Development-specific settings
application:
  log_level: "debug"
  debug: true
  hot_reload: true
  
database:
  host: "localhost"
  ssl: false
  
cache:
  enabled: false  # Disable for development simplicity
```

### Variable Substitution and Templating

#### Environment Variable References
```yaml
# Use consistent environment variable patterns
database:
  host: "${DATABASE_HOST:-localhost}"
  port: "${DATABASE_PORT:-5432}"
  username: "${DATABASE_USERNAME}"
  password: "${DATABASE_PASSWORD}"
  
application:
  secret_key: "${SECRET_KEY}"
  debug: "${DEBUG:-false}"
  log_level: "${LOG_LEVEL:-info}"
```

#### Conditional Configuration
```yaml
# Use YAML anchors and references for reusable configuration
defaults: &defaults
  timeout: 30
  retries: 3
  ssl_verify: true

production:
  <<: *defaults
  environment: "production"
  log_level: "warn"
  
development:
  <<: *defaults
  environment: "development"
  log_level: "debug"
  ssl_verify: false
```

## Security Standards

### Sensitive Data Handling

#### Secure Configuration Patterns
```yaml
# ✅ GOOD: Use environment variables for secrets
database:
  host: "db.example.com"
  port: 5432
  username: "${DB_USERNAME}"
  password: "${DB_PASSWORD}"  # Never hardcode passwords
  
api:
  base_url: "https://api.example.com"
  api_key: "${API_KEY}"      # Use environment variables
  
encryption:
  key_file: "/etc/ssl/certs/app.key"
  cert_file: "/etc/ssl/certs/app.crt"

# ❌ BAD: Hardcoded sensitive information
database:
  username: "admin"
  password: "supersecret123"  # Never do this!
  
api:
  api_key: "ak-1234567890abcdef"  # Security risk!
```

#### File Permissions and Access
```yaml
# Document expected file permissions in comments
# File should be readable only by application user (600)
# Path: /etc/myapp/secure-config.yaml
# Permissions: -rw------- (600)

application:
  private_key: "/etc/ssl/private/app.key"
  certificate: "/etc/ssl/certs/app.crt"
  
security:
  jwt_secret: "${JWT_SECRET}"
  encryption_key: "${ENCRYPTION_KEY}"
```

### Input Validation and Sanitization

```yaml
# Validation rules for configuration values
validation:
  database:
    host:
      required: true
      type: "hostname"
      pattern: "^[a-zA-Z0-9.-]+$"
    port:
      required: true
      type: "integer"
      min: 1
      max: 65535
      
  application:
    log_level:
      required: false
      type: "string"
      enum: ["debug", "info", "warn", "error"]
    debug:
      required: false
      type: "boolean"
```

## Cloud Platform Configuration

### Kubernetes Configuration

#### Pod Specification
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: production
  labels:
    app: myapp
    version: "1.0.0"
    environment: production
    
spec:
  containers:
    - name: myapp
      image: "myregistry/myapp:1.0.0"
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
          
      env:
        - name: DATABASE_HOST
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: host
              
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: password
              
      resources:
        requests:
          memory: "256Mi"
          cpu: "250m"
        limits:
          memory: "512Mi"
          cpu: "500m"
          
      livenessProbe:
        httpGet:
          path: "/health"
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
        
      readinessProbe:
        httpGet:
          path: "/ready"
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
```

#### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
  labels:
    app: myapp
    
spec:
  selector:
    app: myapp
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  web:
    image: "myapp:latest"
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - BUILD_ENV=production
        
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      
    ports:
      - "8080:8080"
      
    depends_on:
      - database
      - cache
      
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
      
    restart: unless-stopped
    
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
      
  database:
    image: "postgres:14-alpine"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      
    ports:
      - "5432:5432"
      
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
      
  cache:
    image: "redis:7-alpine"
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### CI/CD Pipeline Configuration

#### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
    
env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16, 18, 20]
        
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run tests
        run: npm test
        
      - name: Generate coverage
        run: npm run coverage
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        
  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## Data Serialization and APIs

### API Response Formatting

```yaml
# OpenAPI/Swagger specification
openapi: 3.0.3
info:
  title: "MyApp API"
  version: "1.0.0"
  description: "Production API for MyApp"
  contact:
    name: "API Support"
    email: "api-support@example.com"
    
servers:
  - url: "https://api.example.com/v1"
    description: "Production server"
  - url: "https://staging-api.example.com/v1"
    description: "Staging server"
    
paths:
  /users:
    get:
      summary: "List users"
      parameters:
        - name: page
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
            
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
            
      responses:
        '200':
          description: "Successful response"
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
                    
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        created_at:
          type: string
          format: date-time
          
    Pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
        total:
          type: integer
          minimum: 0
        has_more:
          type: boolean
```

### Configuration Schema Definition

```yaml
# JSON Schema for configuration validation
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://example.com/schemas/app-config.json"

title: "Application Configuration"
type: object

required:
  - application
  - database

properties:
  application:
    type: object
    required:
      - name
      - version
    properties:
      name:
        type: string
        pattern: "^[a-z][a-z0-9-]*[a-z0-9]$"
        minLength: 3
        maxLength: 50
      version:
        type: string
        pattern: "^\\d+\\.\\d+\\.\\d+$"
      log_level:
        type: string
        enum: ["debug", "info", "warn", "error"]
        default: "info"
      debug:
        type: boolean
        default: false
        
  database:
    type: object
    required:
      - host
      - port
      - name
    properties:
      host:
        type: string
        format: hostname
      port:
        type: integer
        minimum: 1
        maximum: 65535
      name:
        type: string
        pattern: "^[a-zA-Z][a-zA-Z0-9_]*$"
      ssl:
        type: boolean
        default: true
      pool_size:
        type: integer
        minimum: 1
        maximum: 100
        default: 10
```

## Performance and Optimization

### Large Configuration Files

#### Modular Configuration
```yaml
# main-config.yaml - Import other configuration files
application: !include application-config.yaml
database: !include database-config.yaml
cache: !include cache-config.yaml
monitoring: !include monitoring-config.yaml
```

#### Streaming and Memory Management
```yaml
# Configuration for handling large datasets
processing:
  batch_size: 1000
  memory_limit: "512MB"
  streaming_enabled: true
  
  chunking:
    enabled: true
    chunk_size: 100
    parallel_processing: true
    max_workers: 4
    
file_handling:
  max_file_size: "100MB"
  compression: "gzip"
  temp_directory: "/tmp/processing"
```

### Caching Strategies

```yaml
cache:
  levels:
    # Memory cache (fastest)
    memory:
      enabled: true
      max_size: "256MB"
      ttl: 300  # 5 minutes
      
    # Redis cache (shared)
    redis:
      enabled: true
      cluster: ["redis-01:6379", "redis-02:6379"]
      ttl: 3600  # 1 hour
      
    # File cache (persistent)
    file:
      enabled: true
      directory: "/var/cache/myapp"
      max_size: "1GB"
      ttl: 86400  # 24 hours
      
  strategies:
    user_sessions: "memory"
    api_responses: "redis"
    computed_data: "file"
```

## Validation and Testing

### Schema Validation

```yaml
# Use yamllint for syntax validation
extends: default

rules:
  line-length:
    max: 120
    level: warning
    
  indentation:
    spaces: 2
    indent-sequences: true
    
  comments:
    min-spaces-from-content: 1
    
  truthy:
    allowed-values: ['true', 'false']
    check-keys: true
```

### Configuration Testing

```yaml
# Test configuration for different environments
test_scenarios:
  - name: "production_config"
    config_file: "production-config.yaml"
    expected_values:
      application.log_level: "warn"
      database.ssl: true
      cache.enabled: true
      
  - name: "development_config"
    config_file: "development-config.yaml"
    expected_values:
      application.log_level: "debug"
      database.ssl: false
      
  - name: "invalid_config"
    config_file: "invalid-config.yaml"
    expect_error: true
    error_message: "Missing required field: database.host"
```

### Automated Validation Pipeline

```yaml
# CI/CD validation steps
validation:
  steps:
    - name: "yaml_syntax"
      command: "yamllint *.yaml"
      
    - name: "schema_validation"
      command: "ajv validate -s schema.json -d config.yaml"
      
    - name: "security_scan"
      command: "checkov -f config.yaml"
      
    - name: "environment_test"
      command: "python test_config.py"
```

## Documentation Standards

### Inline Documentation

```yaml
# Application Configuration
# This file contains the main configuration for the production environment
# Last updated: 2023-12-09
# Owner: Platform Team <platform@example.com>

# Core application settings
application:
  name: "myapp"                    # Application identifier
  version: "1.0.0"                # Semantic version
  log_level: "warn"               # Logging verbosity for production
  
  # Feature flags for gradual rollouts
  features:
    new_dashboard: true           # Enable new dashboard UI
    beta_api: false              # Disable beta API endpoints
    metrics_collection: true     # Enable performance metrics
    
# Database configuration
# Primary PostgreSQL database for application data
database:
  host: "${DATABASE_HOST}"        # Database hostname (from env var)
  port: 5432                     # Standard PostgreSQL port
  name: "myapp_production"       # Production database name
  ssl: true                      # Require SSL connections
  
  # Connection pooling settings
  pool:
    min_connections: 5           # Minimum pool size
    max_connections: 50          # Maximum pool size
    idle_timeout: 300           # Seconds before closing idle connections
```

### Configuration Change Management

```yaml
# Change log embedded in configuration
changelog:
  - version: "1.0.0"
    date: "2023-12-09"
    author: "team@example.com"
    changes:
      - "Initial production configuration"
      - "Added database SSL requirement"
      
  - version: "1.0.1"
    date: "2023-12-10"
    author: "ops@example.com"
    changes:
      - "Increased database connection pool size"
      - "Added Redis cache configuration"
      
# Configuration metadata
metadata:
  schema_version: "2.0"
  last_validated: "2023-12-09T10:30:00Z"
  validation_tool: "ajv"
  checksum: "sha256:abc123..."
```

## Error Handling and Debugging

### Configuration Error Patterns

```yaml
# Error handling configuration
error_handling:
  default_behavior: "log_and_continue"
  
  # Specific error handling rules
  rules:
    - type: "database_connection"
      behavior: "retry"
      max_retries: 3
      backoff: "exponential"
      
    - type: "cache_miss"
      behavior: "fallback"
      fallback_action: "fetch_from_database"
      
    - type: "api_timeout"
      behavior: "circuit_breaker"
      threshold: 5
      timeout: 30
      
  # Logging configuration for errors
  logging:
    level: "error"
    format: "json"
    include_stack_trace: true
    destination: "stderr"
```

### Debug Configuration

```yaml
# Debug settings (only for development/staging)
debug:
  enabled: false                 # Never enable in production
  
  # Debug features
  features:
    request_logging: false       # Log all HTTP requests
    query_logging: false         # Log all database queries
    cache_tracing: false         # Trace cache operations
    performance_metrics: true    # Enable performance monitoring
    
  # Debug endpoints (remove in production)
  endpoints:
    health_detailed: "/debug/health"
    metrics: "/debug/metrics"
    config_dump: "/debug/config"  # Never expose in production!
```

## Maintenance and Updates

### Version Control Best Practices

- **Use semantic versioning** for configuration files when appropriate
- **Tag configuration changes** with clear commit messages
- **Review configuration changes** through pull requests
- **Test configurations** in staging environments before production
- **Document breaking changes** in configuration updates

### Automated Configuration Management

```yaml
# Configuration management automation
automation:
  validation:
    pre_commit: true             # Validate before commits
    ci_pipeline: true           # Validate in CI/CD
    
  deployment:
    blue_green: true            # Use blue-green deployments
    rollback_enabled: true      # Enable automatic rollback
    
  monitoring:
    config_drift_detection: true
    change_notifications: true
    
  backup:
    enabled: true
    frequency: "daily"
    retention: "30d"
    encryption: true
```

### Configuration Security Scanning

```yaml
# Security scanning configuration
security:
  scanning:
    enabled: true
    tools:
      - "checkov"               # Infrastructure security
      - "kics"                  # Configuration security
      - "terrascan"            # Policy validation
      
  policies:
    no_hardcoded_secrets: true
    ssl_required: true
    secure_defaults: true
    
  reporting:
    format: "sarif"
    destination: "security-reports/"
    fail_on_high: true
```

This comprehensive YAML instruction file provides enterprise-grade standards for YAML development, covering configuration management, security, performance, and best practices across all common use cases.
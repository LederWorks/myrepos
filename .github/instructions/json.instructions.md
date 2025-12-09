---
applyTo: "**/*.json,**/*.jsonc,**/*.json5"
---

# JSON Development Standards and Guidelines

This document provides comprehensive guidelines for JSON file development, ensuring consistency, maintainability, and best practices across all JSON configurations, data files, and API schemas.

## JSON File Types and Usage

### Configuration Files
- **package.json** - Node.js package configuration
- **tsconfig.json** - TypeScript compiler configuration
- **launch.json** - VS Code debug configurations
- **settings.json** - VS Code workspace settings
- **tasks.json** - VS Code task definitions

### Data and Schema Files
- **API Schemas** - OpenAPI/Swagger definitions
- **Data Files** - Static data, fixtures, test data
- **Translation Files** - i18n/l10n language files
- **Manifest Files** - Application manifests and metadata

### Build and CI/CD Files
- **Workflow Configurations** - GitHub Actions, Azure DevOps
- **Docker Compose** - Container orchestration
- **Environment Configs** - Development, staging, production settings

## Formatting Standards

### Indentation and Spacing
- **Use 2-space indentation** consistently throughout all JSON files
- **No trailing commas** in standard JSON (use JSONC for comments and trailing commas)
- **Consistent spacing** around colons and commas
- **Proper line breaks** for readability

**Good Example:**
```json
{
  "name": "example-project",
  "version": "1.0.0",
  "scripts": {
    "build": "npm run build:prod",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21"
  }
}
```

**Bad Example:**
```json
{
"name":"example-project",
"version":"1.0.0","scripts":{"build":"npm run build:prod","test":"jest --coverage"},
"dependencies":{"express":"^4.18.0","lodash":"^4.17.21",}
}
```

### Object and Array Formatting

#### Small Objects (≤3 properties)
```json
{
  "name": "value",
  "count": 42,
  "active": true
}
```

#### Large Objects (>3 properties)
```json
{
  "name": "complex-configuration",
  "version": "2.1.0",
  "description": "Detailed configuration object",
  "author": "Development Team",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/example/repo.git"
  }
}
```

#### Array Formatting
```json
{
  "simple": ["item1", "item2", "item3"],
  "complex": [
    {
      "id": 1,
      "name": "First Item"
    },
    {
      "id": 2,
      "name": "Second Item"
    }
  ]
}
```

## Schema Design Patterns

### Property Naming Conventions
- **Use camelCase** for property names (`firstName`, `createdAt`)
- **Be descriptive** and avoid abbreviations (`description` not `desc`)
- **Use consistent naming** across related schemas
- **Avoid reserved keywords** and special characters

### Data Type Guidelines

#### Strings
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "description": "Multi-line descriptions should be\nclear and concise",
  "enum": "active" // Use enums for constrained values
}
```

#### Numbers
```json
{
  "age": 25,
  "price": 29.99,
  "count": 0,
  "percentage": 0.85
}
```

#### Booleans
```json
{
  "isActive": true,
  "hasPermission": false,
  "enabled": true
}
```

#### Arrays
```json
{
  "tags": ["development", "json", "standards"],
  "coordinates": [40.7128, -74.0060],
  "items": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ]
}
```

#### Objects
```json
{
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "zipCode": "10001",
    "country": "US"
  },
  "metadata": {
    "createdAt": "2023-12-09T10:30:00Z",
    "updatedAt": "2023-12-09T15:45:00Z",
    "version": "1.2.0"
  }
}
```

### Null and Optional Values
```json
{
  "requiredField": "value",
  "optionalField": null,
  "conditionalField": "present when condition is met"
}
```

## Configuration File Standards

### package.json Best Practices
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Clear, concise project description",
  "main": "dist/index.js",
  "scripts": {
    "build": "npm run build:prod",
    "build:dev": "webpack --mode development",
    "build:prod": "webpack --mode production",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/**/*.{js,ts}",
    "lint:fix": "eslint src/**/*.{js,ts} --fix"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "webpack": "^5.75.0"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
```

### tsconfig.json Structure
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### VS Code Configuration Standards

#### settings.json
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "files.associations": {
    "*.json": "jsonc"
  },
  "json.schemas": [
    {
      "fileMatch": ["**/config/*.json"],
      "url": "./schemas/config-schema.json"
    }
  ]
}
```

#### tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build Project",
      "type": "shell",
      "command": "npm",
      "args": ["run", "build"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$tsc"]
    }
  ]
}
```

## API Schema Design

### RESTful API Response Format
```json
{
  "data": {
    "id": "12345",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "createdAt": "2023-12-09T10:30:00Z"
    }
  },
  "meta": {
    "timestamp": "2023-12-09T15:45:00Z",
    "version": "1.0"
  }
}
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "meta": {
    "timestamp": "2023-12-09T15:45:00Z",
    "requestId": "req-12345"
  }
}
```

### Pagination Format
```json
{
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 100,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

## Validation and Schema Standards

### JSON Schema Definition
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/user.schema.json",
  "title": "User",
  "description": "User account information",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "Unique user identifier (UUID)"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "User's full name"
    },
    "email": {
      "type": "string",
      "format": "email",
      "description": "User's email address"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150,
      "description": "User's age in years"
    }
  },
  "required": ["id", "name", "email"],
  "additionalProperties": false
}
```

### Environment Configuration Schema
```json
{
  "development": {
    "database": {
      "host": "localhost",
      "port": 5432,
      "name": "myapp_dev",
      "ssl": false
    },
    "logging": {
      "level": "debug",
      "console": true,
      "file": false
    }
  },
  "production": {
    "database": {
      "host": "${DB_HOST}",
      "port": "${DB_PORT}",
      "name": "${DB_NAME}",
      "ssl": true
    },
    "logging": {
      "level": "error",
      "console": false,
      "file": true
    }
  }
}
```

## Security Best Practices

### Sensitive Data Handling
- **Never include credentials** in JSON files committed to version control
- **Use environment variable placeholders** for sensitive values
- **Implement proper access controls** for configuration files
- **Validate all input data** against schemas

### Input Sanitization
```json
{
  "validation": {
    "maxLength": 1000,
    "allowedCharacters": "alphanumeric",
    "escapeHtml": true,
    "trimWhitespace": true
  }
}
```

### CORS Configuration
```json
{
  "cors": {
    "origin": ["https://example.com", "https://app.example.com"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allowedHeaders": ["Content-Type", "Authorization"],
    "credentials": true,
    "maxAge": 86400
  }
}
```

## Performance Considerations

### Large JSON Files
- **Minimize nesting depth** (prefer flat structures when possible)
- **Use consistent property ordering** for better compression
- **Consider pagination** for large datasets
- **Implement streaming** for very large files

### Caching Strategies
```json
{
  "cache": {
    "ttl": 3600,
    "strategy": "lru",
    "maxSize": "100MB",
    "compression": true
  }
}
```

### Optimization Techniques
```json
{
  "optimization": {
    "minify": true,
    "compress": true,
    "removeComments": true,
    "deduplication": true
  }
}
```

## Development Tools Integration

### VS Code Integration
- **JSON Language Server** - Syntax highlighting and validation
- **JSON Schema Validation** - Real-time error detection
- **Auto-formatting** - Consistent code formatting
- **IntelliSense** - Auto-completion based on schemas

### Linting Configuration
```json
{
  "jsonlint": {
    "rules": {
      "indent": 2,
      "trailing-comma": false,
      "duplicate-keys": "error",
      "quotes": "double"
    }
  }
}
```

### Testing Standards
```json
{
  "test-data": {
    "valid": {
      "description": "Valid test case",
      "input": {"name": "Test", "value": 123},
      "expected": {"status": "success"}
    },
    "invalid": {
      "description": "Invalid input test case",
      "input": {"name": "", "value": "invalid"},
      "expected": {"status": "error", "code": "VALIDATION_ERROR"}
    }
  }
}
```

## Documentation Standards

### Inline Documentation
- **Use descriptive property names** that explain their purpose
- **Include examples** in schema definitions
- **Document data relationships** and constraints
- **Provide usage examples** for complex configurations

### Schema Documentation
```json
{
  "title": "Application Configuration",
  "description": "Main configuration file for the application",
  "examples": [
    {
      "server": {
        "port": 3000,
        "host": "localhost"
      },
      "database": {
        "url": "postgresql://localhost:5432/myapp"
      }
    }
  ]
}
```

## Migration and Versioning

### Schema Evolution
- **Use semantic versioning** for schema changes
- **Maintain backward compatibility** when possible
- **Provide migration guides** for breaking changes
- **Document all schema changes** in changelog

### Version Management
```json
{
  "schema": {
    "version": "2.1.0",
    "compatibleWith": ["2.0.0", "2.1.0"],
    "migrationPath": {
      "from": "1.x.x",
      "to": "2.0.0",
      "guide": "/docs/migration-v2.md"
    }
  }
}
```

## Quality Assurance

### Validation Checklist
- [ ] **Syntax Validation** - Valid JSON syntax
- [ ] **Schema Compliance** - Matches defined schema
- [ ] **Required Fields** - All required properties present
- [ ] **Data Types** - Correct types for all values
- [ ] **Constraints** - Min/max lengths, ranges, patterns
- [ ] **Security** - No sensitive data exposed

### Automated Testing
```json
{
  "test-suite": {
    "schema-validation": {
      "command": "ajv validate -s schema.json -d data.json",
      "required": true
    },
    "format-check": {
      "command": "prettier --check **/*.json",
      "required": true
    },
    "lint": {
      "command": "jsonlint **/*.json",
      "required": true
    }
  }
}
```

## Common Patterns and Anti-Patterns

### ✅ Good Patterns
```json
{
  "timestamp": "2023-12-09T15:45:00Z",
  "currency": "USD",
  "amount": 2999,
  "tags": ["important", "urgent"],
  "metadata": {
    "source": "api",
    "version": "1.0"
  }
}
```

### ❌ Anti-Patterns to Avoid
```json
{
  "ts": "12/09/23 3:45 PM",
  "curr": "Dollar",
  "amt": "$29.99",
  "tags": "important,urgent",
  "meta": "source=api;version=1.0"
}
```

## Maintenance Guidelines

### Regular Reviews
- **Schema Updates** - Keep schemas current with application changes
- **Performance Monitoring** - Monitor JSON processing performance
- **Security Audits** - Regular security reviews of configurations
- **Documentation Updates** - Keep documentation synchronized with changes

### Best Practices Enforcement
- **Code Reviews** - Include JSON files in review processes
- **Automated Checks** - CI/CD validation of JSON files
- **Style Guides** - Enforce consistent formatting standards
- **Training** - Team education on JSON best practices

This comprehensive guide ensures consistent, maintainable, and high-quality JSON development across all projects while following industry best practices and security standards.
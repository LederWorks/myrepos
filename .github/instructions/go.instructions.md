---
applyTo: 'backend/**/*.go,go.mod,go.sum'
---

# Go Development Standards

This document provides comprehensive guidelines for Go development, covering code style, architecture patterns, testing, security, and best practices for building robust, maintainable Go applications.

## Code Style Guidelines

### Function Naming and Structure

```go
// Use clear, descriptive function names
func CreateMultiCloudResource(ctx context.Context, req CreateResourceRequest) (*Resource, error)

// Implement proper error handling
if err != nil {
    return nil, fmt.Errorf("failed to create resource: %w", err)
}

// Use context for cancellation and timeouts
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
```

### Unused Parameter Handling

Go linting tools (revive, golangci-lint) detect unused parameters automatically. Follow these guidelines:

#### Renaming Unused Parameters

- **Prefix with underscore `_`** for unused parameters that must be kept for interface compliance
- **Use blank identifier `_`** for completely ignored parameters
- **Keep original names** when parameters might be used in future implementations

```go
// Interface compliance - keep parameter for future use
func (s *Service) ProcessData(ctx context.Context, data map[string]interface{}, _metadata ResourceMetadata) error {
    // metadata might be used later, so prefix with _
    return s.process(ctx, data)
}

// Completely unused parameter - use blank identifier
func (s *Service) HandleRequest(_ context.Context, req Request) Response {
    // context not needed in this implementation
    return s.handleSync(req)
}

// Mock implementations - often have unused parameters
func (m *MockService) CreateResource(_ context.Context, _req CreateResourceRequest, _actor string) (*Resource, error) {
    return m.mockResource, nil
}
```

#### When to Rename Back

The linter will detect if you use a parameter that starts with `_`:

- **`revive` linter** warns about used parameters with `_` prefix
- **Rename back to original name** when implementing functionality that uses the parameter
- **Keep descriptive names** for parameters that are actively used

```go
// Before implementing
func (s *Service) ProcessWithMetadata(ctx context.Context, data map[string]interface{}, _metadata ResourceMetadata) error {
    return s.process(ctx, data) // metadata not used yet
}

// After implementing metadata processing
func (s *Service) ProcessWithMetadata(ctx context.Context, data map[string]interface{}, metadata ResourceMetadata) error {
    enriched := s.enrichWithMetadata(data, metadata) // now metadata is used
    return s.process(ctx, enriched)
}
```

#### Interface Design Considerations

- **Keep consistent signatures** across interface implementations
- **Document unused parameters** in interface comments
- **Consider future extensibility** when designing interfaces

````go
type ResourceProcessor interface {
    // Process processes resource data
    // ctx: request context for cancellation
    // data: resource data to process
    // metadata: resource metadata (may be unused in some implementations)
    // actor: user performing the action (for audit trail)
    Process(ctx context.Context, data map[string]interface{}, metadata ResourceMetadata, actor string) error
}
```

### Import Management and Duplicate Import Prevention (dupImport)

The `dupImport` linter warning occurs when the same package is imported multiple times, often with different aliases or as both normal and blank imports.

#### Common Duplicate Import Scenarios

**❌ BAD: Same package imported multiple times**
```go
import (
    "database/sql"
    "github.com/lib/pq"           // Normal import for using pq.Array()
    _ "github.com/lib/pq"         // Blank import for driver registration - DUPLICATE!
)
```

**❌ BAD: Different aliases for same package**
```go
import (
    pq "github.com/lib/pq"
    "github.com/lib/pq"          // DUPLICATE with different alias
)
```

**✅ GOOD: Single import when package is actively used**
```go
import (
    "database/sql"
    "github.com/lib/pq"          // Single import - handles both usage and driver registration
)

func example() {
    // Use package functions directly
    rows, err := db.Query("SELECT * FROM table", pq.Array(values))
    var stringArray pq.StringArray
}
```

**✅ GOOD: Blank import when only driver registration is needed**
```go
import (
    "database/sql"
    _ "github.com/lib/pq"        // Only for side effects (driver registration)
)

func example() {
    // Only using standard database/sql, no pq-specific functions
    db, err := sql.Open("postgres", connectionString)
}
```

#### Driver Registration vs Active Usage

**Database Drivers** often need special consideration:

```go
// When you need pq-specific functions (Array, StringArray, etc.)
import (
    "database/sql"
    "github.com/lib/pq"          // Normal import - covers driver registration too
)

// When you only need the driver registered
import (
    "database/sql"
    _ "github.com/lib/pq"        // Blank import for driver registration only
)
```

#### Import Organization Best Practices

**✅ GOOD: Properly organized imports**
```go
import (
    // Standard library imports first
    "context"
    "database/sql"
    "encoding/json"
    "fmt"
    "log"
    "time"

    // Third-party imports
    "github.com/lib/pq"

    // Local project imports
    "github.com/LederWorks/siros/backend/internal/config"
    "github.com/LederWorks/siros/backend/pkg/types"
)
```

#### Resolving Duplicate Import Issues

**Step 1: Identify the purpose**
- Is the package used for function calls? → Use normal import
- Is it only needed for side effects (like driver registration)? → Use blank import
- Is it used for both? → Normal import handles both cases

**Step 2: Remove duplicates**
```go
// Before (duplicate imports)
import (
    "github.com/lib/pq"
    _ "github.com/lib/pq" // PostgreSQL driver
)

// After (single import for active usage)
import (
    "github.com/lib/pq"   // Handles both usage and driver registration
)
```

**Step 3: Verify functionality**
- Ensure driver registration still works
- Verify package functions are accessible
- Run tests to confirm no regressions

#### Common Patterns in Siros

**Database Operations:**
```go
import (
    "database/sql"
    "github.com/lib/pq"  // For pq.Array(), pq.StringArray, and driver registration
)

func (s *Storage) CreateResource(ctx context.Context, resource *types.Resource) error {
    query := `INSERT INTO resources (...) VALUES (...)`
    _, err := s.db.ExecContext(ctx, query,
        pq.Array(resource.Children),    // Using pq functions
        pq.Array(resource.Vector),
    )
    return err
}
```

**AWS SDK Imports:**
```go
import (
    "github.com/aws/aws-sdk-go-v2/service/ec2"
    ec2types "github.com/aws/aws-sdk-go-v2/service/ec2/types"  // Alias to avoid conflicts
)
```

#### Tools and Automation

**goimports** automatically organizes imports:
```bash
# Format imports automatically
goimports -w .

# Check import formatting
goimports -d .
```

**IDE Integration:**
- Configure VS Code to run goimports on save
- Use golangci-lint with dupImport rule enabled
- Set up pre-commit hooks to catch import issues early

This prevents dupImport warnings and maintains clean, organized import sections throughout the codebase.

### API Design Patterns

#### Constructor Functions and Return Types

**Rule**: Exported constructor functions should return **interface types**, not unexported concrete types.

**Problem - unexported-return Warning**:
```go
// ❌ BAD: Exported function returning unexported type
func NewBlockchainRepository(db *sql.DB) *blockchainRepository {
    return &blockchainRepository{db: db}
}
```

**Issues with this pattern**:
- Users can't effectively work with the returned type
- Requires type assertions for any meaningful operations
- Inconsistent API design (public function, private return)
- Harder to test and mock

**Solution**:
```go
// ✅ GOOD: Exported function returning exported interface
func NewBlockchainRepository(db *sql.DB) BlockchainRepository {
    return &blockchainRepository{db: db}
}
```

**Benefits of interface returns**:
- **Clean API**: Users work with well-defined interfaces
- **Testability**: Easy to mock for unit tests
- **Flexibility**: Implementation can change without breaking callers
- **Consistency**: Public functions return public types

#### Common Unexported-Return Scenarios

**❌ BAD: Repository constructors returning concrete types**
```go
// Violates unexported-return rule
func NewResourceRepository(db *sql.DB) *resourceRepository {
    return &resourceRepository{db: db}
}

func NewSchemaRepository(db *sql.DB) *schemaRepository {
    return &schemaRepository{db: db}
}

func NewBlockchainRepository(db *sql.DB) *blockchainRepository {
    return &blockchainRepository{db: db}
}
```

**✅ GOOD: Repository constructors returning interfaces**
```go
// Proper API design with interface returns
func NewResourceRepository(db *sql.DB) ResourceRepository {
    return &resourceRepository{db: db}
}

func NewSchemaRepository(db *sql.DB) SchemaRepository {
    return &schemaRepository{db: db}
}

func NewBlockchainRepository(db *sql.DB) BlockchainRepository {
    return &blockchainRepository{db: db}
}
```

#### Service Layer API Design

**❌ BAD: Service constructors with inconsistent returns**
```go
// Mixing concrete types and interfaces
func NewResourceService(repo *resourceRepository) *resourceService {
    return &resourceService{repo: repo}
}

func NewSearchService(repo ResourceRepository) searchService {
    return searchService{repo: repo}
}
```

**✅ GOOD: Consistent interface-based API**
```go
// All service constructors return interfaces
func NewResourceService(repo ResourceRepository) ResourceService {
    return &resourceService{repo: repo}
}

func NewSearchService(repo ResourceRepository) SearchService {
    return &searchService{repo: repo}
}

func NewSchemaService(repo SchemaRepository) SchemaService {
    return &schemaService{repo: repo}
}
```

#### Factory Pattern Implementation

**✅ GOOD: Factory functions with proper interface returns**
```go
// Services factory returning interfaces
type Services struct {
    Resource  ResourceService
    Search    SearchService
    Schema    SchemaService
    Terraform TerraformService
    MCP       MCPService
}

func NewServices(repos *Repositories, logger *log.Logger) *Services {
    return &Services{
        Resource:  NewResourceService(repos.Resource, logger),      // Interface return
        Search:    NewSearchService(repos.Resource, logger),       // Interface return
        Schema:    NewSchemaService(repos.Schema, logger),         // Interface return
        Terraform: NewTerraformService(repos.Resource, logger),    // Interface return
        MCP:       NewMCPService(repos.Resource, logger),          // Interface return
    }
}

// Repositories factory returning interfaces
type Repositories struct {
    Resource   ResourceRepository
    Schema     SchemaRepository
    Blockchain BlockchainRepository
}

func NewRepositories(db *sql.DB, logger *log.Logger) *Repositories {
    return &Repositories{
        Resource:   NewResourceRepository(db),      // Interface return
        Schema:     NewSchemaRepository(db),        // Interface return
        Blockchain: NewBlockchainRepository(db),    // Interface return
    }
}
```

#### Testing Interface Compatibility

Always verify that your implementations satisfy the interfaces:

```go
// Compile-time interface compliance checks
var (
    _ ResourceRepository   = (*resourceRepository)(nil)
    _ SchemaRepository     = (*schemaRepository)(nil)
    _ BlockchainRepository = (*blockchainRepository)(nil)
    _ ResourceService      = (*resourceService)(nil)
    _ SearchService        = (*searchService)(nil)
)
```

#### Migration Strategy for Existing Code

When fixing unexported-return warnings:

1. **Define the interface** (if it doesn't exist)
2. **Update the constructor** to return the interface
3. **Update all call sites** to use interface types
4. **Add compile-time checks** to verify implementation

```go
// Step 1: Define interface
type ExampleService interface {
    DoSomething(ctx context.Context, data string) error
}

// Step 2: Update constructor
func NewExampleService(dep Dependency) ExampleService { // Was: *exampleService
    return &exampleService{dep: dep}
}

// Step 3: Update callers
var service ExampleService = NewExampleService(dep) // Was: *exampleService

// Step 4: Add compile-time check
var _ ExampleService = (*exampleService)(nil)
```

#### Repository Pattern Implementation

```go
// Interface definition (exported)
type ResourceRepository interface {
    Create(ctx context.Context, resource *models.Resource) error
    GetByID(ctx context.Context, id string) (*models.Resource, error)
    Update(ctx context.Context, resource *models.Resource) error
    Delete(ctx context.Context, id string) error
}

// Implementation (unexported)
type resourceRepository struct {
    db *sql.DB
}

// Constructor (exported function returning exported interface)
func NewResourceRepository(db *sql.DB) ResourceRepository {
    return &resourceRepository{db: db}
}
```

### Heavy Parameter Optimization (hugeParam)

The `hugeParam` linter warning occurs when large structs (typically >96 bytes) are passed by value instead of by pointer, causing expensive copying operations.

#### Identifying Heavy Parameters

Common heavy parameter candidates in Siros:
- **models.SearchQuery** (104 bytes) - search filters and pagination
- **models.Schema** (112 bytes) - resource schema definitions
- **models.ResourceMetadata** (104 bytes) - resource enrichment data
- **models.TerraformKey** (96 bytes) - Terraform resource keys
- **config.ProvidersConfig** (176 bytes) - cloud provider configurations

#### Heavy Parameter Best Practices

**❌ BAD: Passing large structs by value**
```go
// Heavy parameter - causes expensive copying
func (s *schemaService) CreateSchema(ctx context.Context, schema models.Schema) error {
    return s.repo.Create(ctx, &schema) // Converting to pointer anyway
}

// Heavy parameter in repository
func (r *resourceRepository) List(ctx context.Context, query models.SearchQuery) ([]models.Resource, error) {
    // query struct copied on every call
    return r.performQuery(ctx, query)
}

// Heavy parameter in provider manager
func NewManager(cfg config.ProvidersConfig) *Manager {
    return &Manager{config: cfg} // Large struct copied
}
```

**✅ GOOD: Using pointer parameters**
```go
// Pointer parameter - no copying overhead
func (s *schemaService) CreateSchema(ctx context.Context, schema *models.Schema) error {
    return s.repo.Create(ctx, schema) // Already a pointer
}

// Pointer parameter in repository
func (r *resourceRepository) List(ctx context.Context, query *models.SearchQuery) ([]models.Resource, error) {
    // Only pointer copied, struct shared
    return r.performQuery(ctx, query)
}

// Pointer parameter in provider manager
func NewManager(cfg *config.ProvidersConfig) *Manager {
    return &Manager{config: *cfg} // Copy only when needed
}
```

#### Interface Design for Heavy Parameters

Update interface definitions to use pointers for heavy parameters:

```go
// Service interfaces with pointer parameters
type SchemaService interface {
    CreateSchema(ctx context.Context, schema *models.Schema) error
    UpdateSchema(ctx context.Context, name, provider string, schema *models.Schema) error
}

type ResourceRepository interface {
    List(ctx context.Context, query *models.SearchQuery) ([]models.Resource, error)
    Search(ctx context.Context, query *models.SearchQuery) ([]models.Resource, error)
}

type VectorService interface {
    GenerateVector(ctx context.Context, data map[string]interface{}, metadata *models.ResourceMetadata) ([]float32, error)
}
```

#### Call Site Updates

When updating function signatures, remember to update all call sites:

```go
// Before: passing structs by value
resource, err := service.CreateResource(ctx, createRequest)
results, err := repo.List(ctx, searchQuery)
vector, err := vectorSvc.GenerateVector(ctx, data, metadata)

// After: passing pointers
resource, err := service.CreateResource(ctx, &createRequest)
results, err := repo.List(ctx, &searchQuery)
vector, err := vectorSvc.GenerateVector(ctx, data, &metadata)
```

#### Performance Benefits

- **Memory**: Eliminates large struct copying (104-176 bytes → 8 bytes pointer)
- **CPU**: Reduces allocation overhead in high-frequency operations
- **Cache**: Better CPU cache utilization with pointer sharing
- **Scalability**: Improved performance under load with frequent API calls

#### Nil Safety Considerations

When using pointer parameters, always validate against nil:

```go
func (s *schemaService) CreateSchema(ctx context.Context, schema *models.Schema) error {
    if schema == nil {
        return errors.New("schema cannot be nil")
    }

    if err := schema.Validate(); err != nil {
        return fmt.Errorf("schema validation failed: %w", err)
    }

    return s.repo.Create(ctx, schema)
}
```

### Range Value Copy Optimization (rangeValCopy)

The `rangeValCopy` linter warning occurs when range loops copy large structs (typically >256 bytes) on each iteration, causing performance overhead.

#### Identifying Range Value Copy Issues

Common scenarios in Siros that trigger this warning:
- **models.Resource** (~256 bytes) - core resource struct iterations
- **AWS SDK types** (688-960 bytes) - EC2 instances, RDS instances
- **Terraform types** (264 bytes) - terraform resource processing

#### Range Value Copy Best Practices

**❌ BAD: Copying large structs in range loops**
```go
// Copies 256 bytes per iteration
for i, resource := range resources {
    results[i] = SearchResult{
        "id":   resource.ID,     // resource copied from slice
        "name": resource.Name,
        "data": resource.Data,
    }
}

// Copies 688 bytes per AWS instance iteration
for _, instance := range reservation.Instances {
    resource := convertEC2Instance(instance) // instance copied
    resources = append(resources, resource)
}

// Copies 264 bytes per terraform resource iteration
for _, resource := range terraformResources {
    converted := convertTerraformResource(resource) // resource copied
    results = append(results, converted)
}
```

**✅ GOOD: Using pointer iteration or indexing**

**Option 1: Pointer Iteration (recommended for modification)**
```go
// Zero-copy iteration with pointers
for i := range resources {
    resource := &resources[i] // Point to original, no copy
    results[i] = SearchResult{
        "id":   resource.ID,
        "name": resource.Name,
        "data": resource.Data,
    }
}

// Zero-copy AWS instance processing
for i := range reservation.Instances {
    instance := &reservation.Instances[i] // Point to original
    resource := convertEC2Instance(instance)
    resources = append(resources, resource)
}
```

**Option 2: Index-Based Access (recommended for read-only)**
```go
// Index-based access, no copying
for i := 0; i < len(resources); i++ {
    results[i] = SearchResult{
        "id":   resources[i].ID,    // Direct slice access
        "name": resources[i].Name,
        "data": resources[i].Data,
    }
}

// Index-based terraform processing
for i := 0; i < len(terraformResources); i++ {
    converted := convertTerraformResource(&terraformResources[i])
    results = append(results, converted)
}
```

**Option 3: Range with Pointer (Go 1.22+)**
```go
// Modern Go pointer range (requires Go 1.22+)
for _, resource := range &resources {
    results = append(results, SearchResult{
        "id":   resource.ID,
        "name": resource.Name,
        "data": resource.Data,
    })
}
```

#### Performance Comparison

```go
// SLOW: 256 bytes × 1000 resources = 256KB copied
for _, resource := range resources {
    processResource(resource) // Expensive copy
}

// FAST: 8 bytes × 1000 resources = 8KB (pointer overhead only)
for i := range resources {
    processResource(&resources[i]) // Pointer passing
}
```

#### When to Use Each Pattern

**Use Pointer Iteration (`&slice[i]`) when:**
- Modifying struct fields during iteration
- Passing structs to functions expecting pointers
- Working with large structs (>100 bytes)
- Performance is critical

**Use Index-Based Access (`slice[i]`) when:**
- Read-only operations on struct fields
- Simple field access without function calls
- Backward compatibility with older Go versions

**Use Traditional Range when:**
- Working with small structs (<50 bytes)
- Copying is intentional (avoiding shared state)
- Iterating primitive types (int, string, etc.)

#### Real-World Siros Examples

```go
// Search service optimization
func (s *searchService) convertToSearchResults(resources []models.Resource) []SearchResult {
    results := make([]SearchResult, len(resources))

    // OPTIMIZED: Pointer iteration to avoid 256-byte copies
    for i := range resources {
        resource := &resources[i]
        results[i] = SearchResult{
            "id":          resource.ID,
            "type":        resource.Type,
            "provider":    resource.Provider,
            "name":        resource.Name,
            "created_at":  resource.CreatedAt,
            "modified_at": resource.ModifiedAt,
        }
    }

    return results
}

// AWS provider optimization
func (p *AWSProvider) processEC2Instances(reservation *ec2.Reservation) []models.Resource {
    var resources []models.Resource

    // OPTIMIZED: Index-based iteration for large AWS structs
    for i := 0; i < len(reservation.Instances); i++ {
        instance := &reservation.Instances[i]
        resource := p.convertEC2Instance(instance)
        resources = append(resources, resource)
    }

    return resources
}

// Terraform importer optimization
func (si *StateImporter) processResources(tfResources []types.TerraformResource) []types.Resource {
    var resources []types.Resource

    // OPTIMIZED: Range with pointer access
    for i := range tfResources {
        tfResource := &tfResources[i]
        for j := range tfResource.Instances {
            instance := &tfResource.Instances[j]
            resource, err := si.convertTerraformResource(tfResource, instance)
            if err != nil {
                continue
            }
            resources = append(resources, *resource)
        }
    }

    return resources
}
```

## Architecture Guidelines

### MVC Pattern Implementation

Follow the Model-View-Controller pattern with clean separation of concerns:

#### Controllers (`internal/controllers/`)
Controllers handle HTTP requests and orchestrate business logic without containing it:

```go
type ResourceController struct {
    resourceService services.ResourceService
    vectorService   services.VectorService
    auditService   services.AuditService
    logger         *log.Logger
}

func (c *ResourceController) CreateResource(w http.ResponseWriter, r *http.Request) {
    // 1. Parse and validate request
    var req CreateResourceRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        views.WriteError(w, http.StatusBadRequest, "invalid request body", err)
        return
    }

    // 2. Delegate to service layer
    resource, err := c.resourceService.CreateResource(r.Context(), req)
    if err != nil {
        views.WriteError(w, http.StatusInternalServerError, "failed to create resource", err)
        return
    }

    // 3. Format response via view layer
    views.WriteResourceResponse(w, http.StatusCreated, resource)
}
````

**Controller Standards:**

- **Thin Controllers**: Only handle HTTP concerns, delegate business logic to services
- **Validation**: Validate input before passing to service layer
- **Error Handling**: Convert service errors to appropriate HTTP responses
- **Logging**: Log request processing for debugging and audit
- **Context Propagation**: Pass context through all service calls

#### Models (`internal/models/`)

Models define data structures and core business logic:

```go
type Resource struct {
    ID           string                 `json:"id" db:"id"`
    Type         string                 `json:"type" db:"type"`
    Provider     string                 `json:"provider" db:"provider"`
    Name         string                 `json:"name" db:"name"`
    Data         map[string]interface{} `json:"data" db:"data"`
    Metadata     ResourceMetadata       `json:"metadata" db:"metadata"`
    Vector       []float32              `json:"vector,omitempty" db:"vector"`
    ParentID     *string                `json:"parent_id,omitempty" db:"parent_id"`
    CreatedAt    time.Time              `json:"created_at" db:"created_at"`
    ModifiedAt   time.Time              `json:"modified_at" db:"modified_at"`
}

func (r *Resource) Validate() error {
    if r.ID == "" {
        return errors.New("resource ID is required")
    }
    if r.Type == "" {
        return errors.New("resource type is required")
    }
    if r.Provider == "" {
        return errors.New("resource provider is required")
    }
    return nil
}

func (r *Resource) GenerateVector(vectorizer VectorService) error {
    // Business logic for vector generation
    vector, err := vectorizer.GenerateVector(r.Data, r.Metadata)
    if err != nil {
        return fmt.Errorf("failed to generate vector: %w", err)
    }
    r.Vector = vector
    return nil
}
```

**Model Standards:**

- **Data Validation**: Models enforce business rules and data integrity
- **Immutable Core**: Use value objects where appropriate
- **Business Logic**: Encapsulate domain-specific operations
- **Vector Operations**: Include vector-specific methods
- **Audit Trail**: Support blockchain change tracking

#### Views (`internal/views/`)

Views handle response formatting and data presentation:

```go
type APIResponse struct {
    Data    interface{} `json:"data,omitempty"`
    Error   *APIError   `json:"error,omitempty"`
    Meta    *Meta       `json:"meta,omitempty"`
}

type APIError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    Details string `json:"details,omitempty"`
}

func WriteResourceResponse(w http.ResponseWriter, status int, resource *models.Resource) {
    response := APIResponse{
        Data: resource,
        Meta: &Meta{
            Timestamp: time.Now(),
            Version:   "1.0",
        },
    }
    WriteJSONResponse(w, status, response)
}

func WriteError(w http.ResponseWriter, status int, message string, err error) {
    response := APIResponse{
        Error: &APIError{
            Code:    fmt.Sprintf("E%d", status),
            Message: message,
            Details: err.Error(),
        },
    }
    WriteJSONResponse(w, status, response)
}
```

**View Standards:**

- **Consistent Formatting**: Use standardized response structures
- **Data Sanitization**: Remove sensitive information from responses
- **Content Negotiation**: Support multiple response formats
- **Error Standardization**: Consistent error response format
- **Security**: Prevent information leakage in error messages

#### Services (`internal/services/`)

Services contain business logic and coordinate between models and repositories:

```go
type ResourceService interface {
    CreateResource(ctx context.Context, req CreateResourceRequest) (*models.Resource, error)
    GetResource(ctx context.Context, id string) (*models.Resource, error)
    UpdateResource(ctx context.Context, id string, updates ResourceUpdates) (*models.Resource, error)
    DeleteResource(ctx context.Context, id string) error
    ListResources(ctx context.Context, filters ResourceFilters) ([]*models.Resource, error)
}

type resourceService struct {
    repo        repositories.ResourceRepository
    vectorRepo  repositories.VectorRepository
    auditRepo   repositories.BlockchainRepository
    vectorizer  VectorService
}

func (s *resourceService) CreateResource(ctx context.Context, req CreateResourceRequest) (*models.Resource, error) {
    // Business logic and orchestration
    resource := &models.Resource{
        ID:       generateID(),
        Type:     req.Type,
        Provider: req.Provider,
        Name:     req.Name,
        Data:     req.Data,
        Metadata: enrichMetadata(req.Metadata),
        CreatedAt: time.Now(),
        ModifiedAt: time.Now(),
    }

    // Validate business rules
    if err := resource.Validate(); err != nil {
        return nil, fmt.Errorf("validation failed: %w", err)
    }

    // Generate vector
    if err := resource.GenerateVector(s.vectorizer); err != nil {
        return nil, fmt.Errorf("vector generation failed: %w", err)
    }

    // Store in database
    if err := s.repo.Create(ctx, resource); err != nil {
        return nil, fmt.Errorf("storage failed: %w", err)
    }

    // Record in blockchain
    if err := s.auditRepo.RecordChange(ctx, resource.ID, "CREATE", resource); err != nil {
        return nil, fmt.Errorf("audit recording failed: %w", err)
    }

    return resource, nil
}
```

#### Repositories (`internal/repositories/`)

Repositories handle data access and persistence:

```go
type ResourceRepository interface {
    Create(ctx context.Context, resource *models.Resource) error
    GetByID(ctx context.Context, id string) (*models.Resource, error)
    Update(ctx context.Context, resource *models.Resource) error
    Delete(ctx context.Context, id string) error
    List(ctx context.Context, filters ResourceFilters) ([]*models.Resource, error)
}

type resourceRepository struct {
    db *sql.DB
}

func (r *resourceRepository) Create(ctx context.Context, resource *models.Resource) error {
    query := `
        INSERT INTO resources (id, type, provider, name, data, metadata, vector, parent_id, created_at, modified_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    `
    _, err := r.db.ExecContext(ctx, query,
        resource.ID, resource.Type, resource.Provider, resource.Name,
        resource.Data, resource.Metadata, resource.Vector, resource.ParentID,
        resource.CreatedAt, resource.ModifiedAt,
    )
    if err != nil {
        return fmt.Errorf("failed to insert resource: %w", err)
    }
    return nil
}
```

## Code Style Guidelines

### Function Naming and Structure

```go
// Use clear, descriptive function names
func CreateMultiCloudResource(ctx context.Context, req CreateResourceRequest) (*Resource, error)

// Implement proper error handling
if err != nil {
    return nil, fmt.Errorf("failed to create resource: %w", err)
}

// Use context for cancellation and timeouts
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
```

### Architecture Patterns

- Follow **clean architecture** principles with clear layer separation
- Implement **dependency injection** for testability using interfaces
- Use **interfaces** for abstractions between layers
- Apply **single responsibility principle** to each component

## API Development

### HTTP Routing

- Use **Gorilla Mux** for HTTP routing
- Implement **middleware** for CORS, logging, and authentication
- Follow **REST conventions** for endpoint design
- Provide **JSON responses** with consistent error formats
- Support **filtering, pagination, and sorting** for list endpoints

### REST API Structure

```
GET    /api/v1/resources              # List resources with filtering
POST   /api/v1/resources              # Create new resource
GET    /api/v1/resources/{id}         # Get specific resource
PUT    /api/v1/resources/{id}         # Update resource
DELETE /api/v1/resources/{id}         # Delete resource

POST   /api/v1/search                 # Semantic search
GET    /api/v1/schemas                # List available schemas
POST   /api/v1/terraform/import       # Import Terraform state

POST   /api/v1/mcp/initialize         # MCP protocol endpoints
POST   /api/v1/mcp/resources/list
POST   /api/v1/mcp/resources/read

GET    /api/v1/relationships/{id}     # Get resource relationships
POST   /api/v1/discovery/scan         # Trigger cloud resource discovery
GET    /api/v1/blockchain/audit/{id}  # Get resource audit trail
```

## Database Integration

### PostgreSQL with pgvector

- Use **PostgreSQL** with **pgvector** extension for vector operations
- Implement **prepared statements** to prevent SQL injection
- Use **database transactions** for atomic operations
- Create **proper indexes** for query performance
- Design **vector similarity queries** for resource relationship discovery
- Implement **blockchain record insertion** for all resource changes

### Transaction Management

```go
func (s *resourceService) CreateResourceWithAudit(ctx context.Context, req CreateResourceRequest) (*models.Resource, error) {
    tx, err := s.db.BeginTx(ctx, nil)
    if err != nil {
        return nil, fmt.Errorf("failed to begin transaction: %w", err)
    }
    defer tx.Rollback()

    // Create resource
    resource, err := s.createResourceInTx(ctx, tx, req)
    if err != nil {
        return nil, err
    }

    // Record audit trail
    if err := s.recordAuditInTx(ctx, tx, resource.ID, "CREATE", resource); err != nil {
        return nil, err
    }

    if err := tx.Commit(); err != nil {
        return nil, fmt.Errorf("failed to commit transaction: %w", err)
    }

    return resource, nil
}
```

## Multi-Cloud Provider Integration

### Provider Pattern

```go
type CloudProvider interface {
    ListResources(ctx context.Context, filters ResourceFilters) ([]Resource, error)
    GetResource(ctx context.Context, id string) (*Resource, error)
    CreateResource(ctx context.Context, spec ResourceSpec) (*Resource, error)
    UpdateResource(ctx context.Context, id string, updates ResourceUpdates) (*Resource, error)
    DeleteResource(ctx context.Context, id string) error
    DiscoverRelationships(ctx context.Context, resourceID string) ([]Relationship, error)
}

// Implement for each cloud provider
type AWSProvider struct {
    ec2Client    *ec2.Client
    s3Client     *s3.Client
    rdsClient    *rds.Client
    vpcClient    *ec2.Client
}

type AzureProvider struct {
    resourceClient   *armresources.Client
    networkClient    *armnetwork.Client
    computeClient    *armcompute.Client
}

type GCPProvider struct {
    computeService   *compute.Service
    storageClient    *storage.Client
    resourceManager  *cloudresourcemanager.Service
}

type OCIProvider struct {
    computeClient    core.ComputeClient
    networkClient    core.VirtualNetworkClient
    identityClient   identity.IdentityClient
}
```

### Resource Management

- Store resources as **individual vectors** with original CSP structure
- Enrich with **metadata**: parent_id, created, created_by, modified, modified_by, IAM
- Support **custom schemas** beyond predefined cloud resource types
- Implement **deduplication logic** to identify related resources without merging
- Maintain **cross-cloud relationship** discovery through vector queries

## Testing Standards

### Unit Testing

```go
func TestCreateResource(t *testing.T) {
    // Setup
    mockStorage := &MockStorage{}
    service := NewResourceService(mockStorage)

    // Test case
    resource, err := service.CreateResource(context.Background(), validRequest)

    // Assertions
    assert.NoError(t, err)
    assert.NotNil(t, resource)
    assert.Equal(t, "expected-name", resource.Name)
}
```

### Controller Testing

```go
func TestResourceController_CreateResource(t *testing.T) {
    // Setup
    mockService := &MockResourceService{}
    controller := NewResourceController(mockService, logger)

    // Mock expectations
    expectedResource := &models.Resource{ID: "test-id", Name: "test"}
    mockService.On("CreateResource", mock.Anything, mock.Anything).Return(expectedResource, nil)

    // Test
    req := httptest.NewRequest("POST", "/resources", strings.NewReader(`{"name":"test"}`))
    w := httptest.NewRecorder()

    controller.CreateResource(w, req)

    // Assertions
    assert.Equal(t, http.StatusCreated, w.Code)
    mockService.AssertExpectations(t)
}
```

### Service Testing

```go
func TestResourceService_CreateResource(t *testing.T) {
    // Setup with mocked dependencies
    mockRepo := &MockResourceRepository{}
    mockVectorRepo := &MockVectorRepository{}
    mockAuditRepo := &MockBlockchainRepository{}
    service := NewResourceService(mockRepo, mockVectorRepo, mockAuditRepo, vectorizer)

    // Test business logic in isolation
    resource, err := service.CreateResource(context.Background(), validRequest)

    assert.NoError(t, err)
    assert.NotNil(t, resource)
    mockRepo.AssertExpectations(t)
}
```

### Test Suite Organization

- **models**: Business logic and validation tests
- **services**: Business logic orchestration tests
- **controllers**: HTTP handler and API tests
- **repositories**: Data access layer tests
- **integration**: End-to-end tests with real dependencies

## Security Best Practices

### Secure File Operations and Path Handling

The `G304` security warning indicates potential file inclusion vulnerabilities (CWE-22). Follow these patterns for secure file operations:

#### Path Validation and Sanitization

**❌ BAD: Unsanitized file path usage**

```go
// Vulnerable to directory traversal attacks
func loadConfig(path string) error {
    data, err := os.ReadFile(path) // G304 - potential security issue
    if err != nil {
        return err
    }
    // ... process data
}
```

**✅ GOOD: Comprehensive path validation**

```go
import (
    "filepath"
    "strings"
    "os"
    "fmt"
)

func validateConfigPath(path string) (string, error) {
    // Reject empty paths
    if path == "" {
        return "", fmt.Errorf("config path cannot be empty")
    }

    // Clean the path to resolve any . or .. elements
    cleanPath := filepath.Clean(path)

    // Reject paths that try to traverse directories with ..
    if strings.Contains(cleanPath, "..") {
        return "", fmt.Errorf("config path cannot contain directory traversal sequences")
    }

    // Ensure the path has a valid extension for config files
    ext := filepath.Ext(cleanPath)
    validExts := []string{".yaml", ".yml", ".json"}
    validExt := false
    for _, validExtension := range validExts {
        if ext == validExtension {
            validExt = true
            break
        }
    }
    if !validExt {
        return "", fmt.Errorf("config file must have a valid extension (.yaml, .yml, .json)")
    }

    // Convert to absolute path for consistency
    absPath, err := filepath.Abs(cleanPath)
    if err != nil {
        return "", fmt.Errorf("failed to resolve absolute path: %w", err)
    }

    return absPath, nil
}

func loadConfigFile(cfg *Config, path string) error {
    // Validate and sanitize the file path
    cleanPath, err := validateConfigPath(path)
    if err != nil {
        return fmt.Errorf("invalid config file path: %w", err)
    }

    // Check if file exists
    if _, err := os.Stat(cleanPath); err != nil {
        if os.IsNotExist(err) {
            return nil // File doesn't exist - use defaults
        }
        return fmt.Errorf("failed to access config file: %w", err)
    }

    // Read the file safely with justified nosec comment
    // #nosec G304 -- Path is validated by validateConfigPath() which prevents directory traversal
    data, err := os.ReadFile(cleanPath)
    if err != nil {
        return fmt.Errorf("failed to read config file: %w", err)
    }

    // Parse configuration data
    if err := yaml.Unmarshal(data, cfg); err != nil {
        return fmt.Errorf("failed to parse config file: %w", err)
    }

    return nil
}
```

#### Security Testing for File Operations

Always test path validation with security-focused test cases:

```go
func TestValidateConfigPath(t *testing.T) {
    tests := []struct {
        name        string
        path        string
        expectError bool
        errorMsg    string
    }{
        {
            name:        "valid yaml config",
            path:        "config.yaml",
            expectError: false,
        },
        {
            name:        "valid json config",
            path:        "config.json",
            expectError: false,
        },
        {
            name:        "directory traversal attempt",
            path:        "../../../etc/passwd",
            expectError: true,
            errorMsg:    "directory traversal",
        },
        {
            name:        "invalid extension",
            path:        "config.txt",
            expectError: true,
            errorMsg:    "valid extension",
        },
        {
            name:        "empty path",
            path:        "",
            expectError: true,
            errorMsg:    "cannot be empty",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := validateConfigPath(tt.path)
            if tt.expectError {
                assert.Error(t, err)
                if tt.errorMsg != "" {
                    assert.Contains(t, err.Error(), tt.errorMsg)
                }
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

#### Using nosec Comments Properly

When security scanners flag legitimate usage, use justified nosec comments:

```go
// Justified nosec usage - explains why the usage is safe
// nosec G304 -- Path is validated by validateConfigPath() which prevents directory traversal
data, err := os.ReadFile(cleanPath)

// Also acceptable with specific CWE reference
// nosec G304:CWE-22 -- Input sanitized through comprehensive path validation
content, err := ioutil.ReadFile(sanitizedPath)
```

**Guidelines for nosec comments:**

- Always include **justification** explaining why the usage is safe
- Reference the **validation function** that makes it secure
- Be **specific** about the protection mechanism
- **Review regularly** to ensure justification remains valid

### Input Validation

- Validate **all user inputs** at the controller layer
- Use **parameterized queries** to prevent SQL injection
- Implement **input sanitization** for all user-provided data
- Use **struct tags** for validation rules
- **Validate file paths** before any file system operations
- **Sanitize file names** and reject directory traversal attempts

### Error Handling

- Use **structured logging** for debugging and monitoring
- **Sanitize sensitive data** in logs and responses
- Implement **proper error wrapping** with context
- Provide **meaningful error messages** without exposing internals
- **Avoid information leakage** in error messages about file system structure

### Authentication & Authorization

- Implement **middleware** for authentication
- Use **context** to pass user information through request pipeline
- Validate **permissions** at the service layer
- Implement **audit logging** for security events

### Database Security

- Use **parameterized queries** exclusively to prevent SQL injection
- Validate **all database inputs** before query construction
- Implement **least privilege** database access
- Use **connection pooling** with proper credential management

```go
// ✅ GOOD: Parameterized query
func (r *resourceRepository) GetByID(ctx context.Context, id string) (*models.Resource, error) {
    query := `SELECT id, type, provider, name, data FROM resources WHERE id = $1`
    var resource models.Resource
    err := r.db.QueryRowContext(ctx, query, id).Scan(
        &resource.ID, &resource.Type, &resource.Provider, &resource.Name, &resource.Data,
    )
    return &resource, err
}

// ❌ BAD: String concatenation (SQL injection risk)
func (r *resourceRepository) GetByID(ctx context.Context, id string) (*models.Resource, error) {
    query := fmt.Sprintf("SELECT * FROM resources WHERE id = '%s'", id) // Vulnerable!
    // ... rest of implementation
}
```

## Development Commands

### Cross-Platform Development

```bash
# Linux/macOS
cd backend && go run ./cmd/siros-server
go test ./...
go build -o siros-server ./cmd/siros-server

# Windows
cd backend; go run ./cmd/siros-server
go test ./...
go build -o siros-server.exe ./cmd/siros-server
```

### Testing

```bash
# Run comprehensive test suite
./scripts/test.sh                    # Linux/macOS
.\scripts\test.ps1                   # Windows

# Run specific test suite with coverage
./scripts/test.sh --suite models --coverage     # Linux/macOS
.\scripts\test.ps1 -TestSuite models -Coverage  # Windows
```

## Performance Considerations

### Database Optimization

- Use **connection pooling** for database connections
- Implement **proper indexing** for vector similarity queries
- Use **prepared statements** for frequently executed queries
- Consider **read replicas** for high-traffic scenarios

### Concurrency

- Think about **concurrency** and **race conditions**
- Use **context** for cancellation and timeouts
- Implement **proper locking** for shared resources
- Consider **worker pools** for parallel processing

### Memory Management

- Be mindful of **memory allocation** for large datasets
- Use **streaming** for large data processing
- Implement **proper cleanup** of resources
- Monitor **garbage collection** performance

## Deployment Considerations

### Single Binary Deployment

- **Embed frontend assets** in Go binary using `embed.FS`
- Support **configuration via files and environment variables**
- Implement **graceful shutdown** and **health checks**
- Provide **Docker images** for containerized deployment

### Configuration Management

- Use **environment variables** for sensitive configuration
- Provide **default values** for optional settings
- Implement **configuration validation** at startup
- Support **hot reloading** of non-sensitive configuration

### Monitoring and Observability

- Implement **structured logging** with appropriate levels
- Add **metrics collection** for key operations
- Include **health check endpoints** for monitoring
- Implement **distributed tracing** for complex operations
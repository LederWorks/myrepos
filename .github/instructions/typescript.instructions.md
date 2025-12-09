---
applyTo: "frontend/**/*.ts,frontend/**/*.tsx,frontend/**/*.json,frontend/**/*.js,frontend/**/*.jsx"
---

# TypeScript Frontend Development Instructions

This document provides comprehensive guidelines for developing modern frontend applications using React, TypeScript, and current web development practices following MVC architecture patterns.

## Architecture Guidelines

### MVC Pattern Implementation

Follow the Model-View-Controller pattern with clean separation of concerns:

#### Controllers (`src/controllers/`)
Frontend controllers manage application state and business logic:

```typescript
interface EntityController {
    createEntity(entity: CreateEntityRequest): Promise<Entity>;
    updateEntity(id: string, updates: Partial<Entity>): Promise<Entity>;
    deleteEntity(id: string): Promise<void>;
    listEntities(filters?: EntityFilters): Promise<Entity[]>;
    searchEntities(query: string, filters?: SearchFilters): Promise<Entity[]>;
}

class ResourceControllerImpl implements ResourceController {
    constructor(
        private resourceService: ResourceService,
        private notificationService: NotificationService
    ) {}

    async createResource(resource: CreateResourceRequest): Promise<Resource> {
        try {
            const newResource = await this.resourceService.createResource(resource);
            this.notificationService.showSuccess('Resource created successfully');
            return newResource;
        } catch (error) {
            this.notificationService.showError('Failed to create resource');
            throw error;
        }
    }

    async listResources(filters?: ResourceFilters): Promise<Resource[]> {
        try {
            return await this.resourceService.listResources(filters);
        } catch (error) {
            this.notificationService.showError('Failed to load resources');
            throw error;
        }
    }
}
```

#### Models (`src/models/`)
Frontend models define TypeScript interfaces and validation:

```typescript
interface Entity {
    id: string;
    type: string;
    name: string;
    data: Record<string, any>;
    metadata: EntityMetadata;
    parentId?: string;
    createdAt: string;
    modifiedAt: string;
}

interface EntityMetadata {
    createdBy: string;
    modifiedBy: string;
    tags?: Record<string, string>;
    category?: string;
    environment?: string;
    custom?: Record<string, any>;
}

class EntityValidator {
    static validate(entity: Partial<Entity>): ValidationResult {
        const errors: string[] = [];
        
        if (!entity.id?.trim()) {
            errors.push('Entity ID is required');
        }
        
        if (!entity.type?.trim()) {
            errors.push('Entity type is required');
        }
        
        if (!entity.name?.trim()) {
            errors.push('Entity name is required');
        }
        
        return {
            isValid: errors.length === 0,
            errors
        };
    }
}

interface ValidationResult {
    isValid: boolean;
    errors: string[];
}
```

#### Views (`src/components/`)
React components handle UI presentation:

```tsx
interface ResourceListProps {
    resources: Resource[];
    onEdit: (resource: Resource) => void;
    onDelete: (resourceId: string) => void;
    loading?: boolean;
    error?: string;
}

export const ResourceList: React.FC<ResourceListProps> = ({
    resources,
    onEdit,
    onDelete,
    loading = false,
    error
}) => {
    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    return (
        <div className="resource-list">
            {resources.map(resource => (
                <ResourceCard
                    key={resource.id}
                    resource={resource}
                    onEdit={() => onEdit(resource)}
                    onDelete={() => onDelete(resource.id)}
                />
            ))}
        </div>
    );
};
```

## Component Architecture

### Functional Components with Hooks
```tsx
// Use functional components with hooks
interface ResourceCardProps {
    resource: Resource;
    onEdit: (resource: Resource) => void;
    onDelete: (resourceId: string) => void;
    className?: string;
}

export const ResourceCard: React.FC<ResourceCardProps> = ({ 
    resource, 
    onEdit, 
    onDelete,
    className = ''
}) => {
    const [isLoading, setIsLoading] = useState(false);
    const [showDetails, setShowDetails] = useState(false);

    const handleEdit = useCallback(() => {
        onEdit(resource);
    }, [resource, onEdit]);

    const handleDelete = useCallback(async () => {
        if (window.confirm('Are you sure you want to delete this resource?')) {
            setIsLoading(true);
            try {
                await onDelete(resource.id);
            } finally {
                setIsLoading(false);
            }
        }
    }, [resource.id, onDelete]);

    return (
        <div className={`resource-card ${className}`}>
            <div className="resource-header">
                <h3>{resource.name}</h3>
                <span className="resource-type">{resource.type}</span>
                <span className="resource-provider">{resource.provider}</span>
            </div>
            
            {showDetails && (
                <div className="resource-details">
                    <pre>{JSON.stringify(resource.data, null, 2)}</pre>
                </div>
            )}
            
            <div className="resource-actions">
                <button onClick={() => setShowDetails(!showDetails)}>
                    {showDetails ? 'Hide' : 'Show'} Details
                </button>
                <button onClick={handleEdit} disabled={isLoading}>
                    Edit
                </button>
                <button onClick={handleDelete} disabled={isLoading}>
                    {isLoading ? 'Deleting...' : 'Delete'}
                </button>
            </div>
        </div>
    );
};
```

### Custom Hooks for Reusable Logic
```tsx
// Custom hook for resource management
export const useResources = () => {
    const [resources, setResources] = useState<Resource[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchResources = useCallback(async (filters?: ResourceFilters) => {
        setLoading(true);
        setError(null);
        try {
            const data = await resourceService.listResources(filters);
            setResources(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch resources');
        } finally {
            setLoading(false);
        }
    }, []);

    const createResource = useCallback(async (resource: CreateResourceRequest) => {
        try {
            const newResource = await resourceService.createResource(resource);
            setResources(prev => [...prev, newResource]);
            return newResource;
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to create resource');
            throw err;
        }
    }, []);

    const updateResource = useCallback(async (id: string, updates: Partial<Resource>) => {
        try {
            const updatedResource = await resourceService.updateResource(id, updates);
            setResources(prev => prev.map(r => r.id === id ? updatedResource : r));
            return updatedResource;
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to update resource');
            throw err;
        }
    }, []);

    const deleteResource = useCallback(async (id: string) => {
        try {
            await resourceService.deleteResource(id);
            setResources(prev => prev.filter(r => r.id !== id));
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to delete resource');
            throw err;
        }
    }, []);

    return {
        resources,
        loading,
        error,
        fetchResources,
        createResource,
        updateResource,
        deleteResource
    };
};
```

## State Management

### React Hooks for Local State
- Use **useState** for component-local state
- Use **useEffect** for side effects and lifecycle events
- Use **useReducer** for complex state logic
- Use **useCallback** and **useMemo** for performance optimization

### Context API for Global State
```tsx
interface AppContextType {
    user: User | null;
    theme: 'light' | 'dark';
    notifications: Notification[];
    setUser: (user: User | null) => void;
    setTheme: (theme: 'light' | 'dark') => void;
    addNotification: (notification: Omit<Notification, 'id'>) => void;
    removeNotification: (id: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [theme, setTheme] = useState<'light' | 'dark'>('light');
    const [notifications, setNotifications] = useState<Notification[]>([]);

    const addNotification = useCallback((notification: Omit<Notification, 'id'>) => {
        const id = generateId();
        setNotifications(prev => [...prev, { ...notification, id }]);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            setNotifications(prev => prev.filter(n => n.id !== id));
        }, 5000);
    }, []);

    const removeNotification = useCallback((id: string) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    }, []);

    const value = {
        user,
        theme,
        notifications,
        setUser,
        setTheme,
        addNotification,
        removeNotification
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export const useApp = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useApp must be used within an AppProvider');
    }
    return context;
};
```

## API Integration

### Type-Safe API Client
```typescript
// Create type-safe API client functions
class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = '/api/v1') {
        this.baseUrl = baseUrl;
    }

    private async request<T>(
        endpoint: string, 
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(errorData?.error?.message || `HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data.data || data;
    }

    async get<T>(endpoint: string): Promise<T> {
        return this.request<T>(endpoint, { method: 'GET' });
    }

    async post<T>(endpoint: string, body?: any): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: body ? JSON.stringify(body) : undefined,
        });
    }

    async put<T>(endpoint: string, body?: any): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'PUT',
            body: body ? JSON.stringify(body) : undefined,
        });
    }

    async delete<T>(endpoint: string): Promise<T> {
        return this.request<T>(endpoint, { method: 'DELETE' });
    }
}

export const apiClient = new ApiClient();

// Resource-specific API functions
export async function fetchResources(filters?: ResourceFilters): Promise<Resource[]> {
    const queryParams = filters ? `?${new URLSearchParams(filters as any).toString()}` : '';
    return apiClient.get<Resource[]>(`/resources${queryParams}`);
}

export async function createResource(resource: CreateResourceRequest): Promise<Resource> {
    return apiClient.post<Resource>('/resources', resource);
}

export async function updateResource(id: string, updates: Partial<Resource>): Promise<Resource> {
    return apiClient.put<Resource>(`/resources/${id}`, updates);
}

export async function deleteResource(id: string): Promise<void> {
    return apiClient.delete<void>(`/resources/${id}`);
}

export async function searchResources(query: string, filters?: SearchFilters): Promise<Resource[]> {
    return apiClient.post<Resource[]>('/search', { query, filters });
}
```

## Styling Guidelines

### CSS-in-JS with styled-components (if used)
```tsx
import styled from 'styled-components';

const ResourceCardContainer = styled.div<{ isSelected?: boolean }>`
    border: 1px solid ${props => props.theme.colors.border};
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    background-color: ${props => props.isSelected ? props.theme.colors.selected : props.theme.colors.background};
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
    &:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
`;

const ResourceHeader = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    h3 {
        margin: 0;
        color: ${props => props.theme.colors.primary};
    }
`;
```

### CSS Modules (alternative approach)
```tsx
import styles from './ResourceCard.module.css';

export const ResourceCard: React.FC<ResourceCardProps> = ({ resource }) => {
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h3 className={styles.title}>{resource.name}</h3>
                <span className={styles.type}>{resource.type}</span>
            </div>
        </div>
    );
};
```

### Responsive Design Principles
- Use **CSS Grid** and **Flexbox** for layouts
- Implement **mobile-first** responsive design
- Use **CSS custom properties** for theming
- Follow **consistent spacing** and **typography** scales

## Error Handling and Loading States

### Error Boundaries
```tsx
interface ErrorBoundaryState {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends React.Component<
    React.PropsWithChildren<{}>,
    ErrorBoundaryState
> {
    constructor(props: React.PropsWithChildren<{}>) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): ErrorBoundaryState {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <h2>Something went wrong</h2>
                    <p>{this.state.error?.message}</p>
                    <button onClick={() => this.setState({ hasError: false })}>
                        Try again
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}
```

### Loading States and Skeletons
```tsx
export const ResourceCardSkeleton: React.FC = () => {
    return (
        <div className="resource-card skeleton">
            <div className="skeleton-header">
                <div className="skeleton-text skeleton-title"></div>
                <div className="skeleton-text skeleton-type"></div>
            </div>
            <div className="skeleton-content">
                <div className="skeleton-text"></div>
                <div className="skeleton-text"></div>
                <div className="skeleton-text short"></div>
            </div>
        </div>
    );
};

export const ResourceListWithLoading: React.FC<ResourceListProps> = ({ 
    resources, 
    loading, 
    error,
    ...props 
}) => {
    if (loading) {
        return (
            <div className="resource-list">
                {Array.from({ length: 5 }, (_, i) => (
                    <ResourceCardSkeleton key={i} />
                ))}
            </div>
        );
    }

    if (error) {
        return <ErrorMessage message={error} />;
    }

    return <ResourceList resources={resources} {...props} />;
};
```

## Testing Standards

### Component Testing with React Testing Library
```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ResourceCard } from './ResourceCard';

const mockResource: Resource = {
    id: '1',
    name: 'Test Resource',
    type: 'aws_instance',
    provider: 'aws',
    data: {},
    metadata: {
        createdBy: 'test-user',
        modifiedBy: 'test-user'
    },
    createdAt: '2023-01-01T00:00:00Z',
    modifiedAt: '2023-01-01T00:00:00Z'
};

describe('ResourceCard', () => {
    it('renders resource information correctly', () => {
        const onEdit = jest.fn();
        const onDelete = jest.fn();

        render(
            <ResourceCard 
                resource={mockResource} 
                onEdit={onEdit} 
                onDelete={onDelete} 
            />
        );

        expect(screen.getByText('Test Resource')).toBeInTheDocument();
        expect(screen.getByText('aws_instance')).toBeInTheDocument();
        expect(screen.getByText('aws')).toBeInTheDocument();
    });

    it('calls onEdit when edit button is clicked', () => {
        const onEdit = jest.fn();
        const onDelete = jest.fn();

        render(
            <ResourceCard 
                resource={mockResource} 
                onEdit={onEdit} 
                onDelete={onDelete} 
            />
        );

        fireEvent.click(screen.getByText('Edit'));
        expect(onEdit).toHaveBeenCalledWith(mockResource);
    });

    it('shows confirmation dialog when delete is clicked', async () => {
        const onEdit = jest.fn();
        const onDelete = jest.fn();
        
        // Mock window.confirm
        window.confirm = jest.fn(() => true);

        render(
            <ResourceCard 
                resource={mockResource} 
                onEdit={onEdit} 
                onDelete={onDelete} 
            />
        );

        fireEvent.click(screen.getByText('Delete'));
        
        await waitFor(() => {
            expect(window.confirm).toHaveBeenCalledWith(
                'Are you sure you want to delete this resource?'
            );
            expect(onDelete).toHaveBeenCalledWith('1');
        });
    });
});
```

### Custom Hook Testing
```tsx
import { renderHook, act } from '@testing-library/react';
import { useResources } from './useResources';

// Mock the API service
jest.mock('../services/resourceService', () => ({
    listResources: jest.fn(),
    createResource: jest.fn(),
    updateResource: jest.fn(),
    deleteResource: jest.fn(),
}));

describe('useResources', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('fetches resources successfully', async () => {
        const mockResources = [mockResource];
        (resourceService.listResources as jest.Mock).mockResolvedValue(mockResources);

        const { result } = renderHook(() => useResources());

        expect(result.current.loading).toBe(false);
        expect(result.current.resources).toEqual([]);

        await act(async () => {
            await result.current.fetchResources();
        });

        expect(result.current.loading).toBe(false);
        expect(result.current.resources).toEqual(mockResources);
        expect(result.current.error).toBeNull();
    });

    it('handles fetch error correctly', async () => {
        const errorMessage = 'Failed to fetch';
        (resourceService.listResources as jest.Mock).mockRejectedValue(new Error(errorMessage));

        const { result } = renderHook(() => useResources());

        await act(async () => {
            await result.current.fetchResources();
        });

        expect(result.current.loading).toBe(false);
        expect(result.current.resources).toEqual([]);
        expect(result.current.error).toBe(errorMessage);
    });
});
```

## Accessibility Guidelines

### Semantic HTML
- Use **semantic HTML elements** (`<main>`, `<nav>`, `<section>`, `<article>`, etc.)
- Implement **proper heading hierarchy** (h1 → h2 → h3)
- Use **descriptive link text** and **button labels**
- Include **alt text** for images and **aria-labels** for icon buttons

### Keyboard Navigation
```tsx
export const ResourceCard: React.FC<ResourceCardProps> = ({ resource, onEdit, onDelete }) => {
    const handleKeyDown = (event: React.KeyboardEvent, action: () => void) => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            action();
        }
    };

    return (
        <div 
            className="resource-card"
            tabIndex={0}
            role="button"
            aria-label={`Resource: ${resource.name}`}
            onKeyDown={(e) => handleKeyDown(e, () => onEdit(resource))}
        >
            <div className="resource-content">
                <h3>{resource.name}</h3>
                <p>{resource.type}</p>
            </div>
            
            <div className="resource-actions">
                <button 
                    onClick={() => onEdit(resource)}
                    aria-label={`Edit ${resource.name}`}
                >
                    Edit
                </button>
                <button 
                    onClick={() => onDelete(resource.id)}
                    aria-label={`Delete ${resource.name}`}
                >
                    Delete
                </button>
            </div>
        </div>
    );
};
```

## Performance Optimization

### React.memo and useMemo
```tsx
export const ResourceCard = React.memo<ResourceCardProps>(({ resource, onEdit, onDelete }) => {
    const formattedDate = useMemo(() => {
        return new Date(resource.modifiedAt).toLocaleDateString();
    }, [resource.modifiedAt]);

    const handleEdit = useCallback(() => {
        onEdit(resource);
    }, [resource, onEdit]);

    return (
        <div className="resource-card">
            <h3>{resource.name}</h3>
            <p>Last modified: {formattedDate}</p>
            <button onClick={handleEdit}>Edit</button>
        </div>
    );
});
```

### Code Splitting and Lazy Loading
```tsx
import { lazy, Suspense } from 'react';

const ResourceDetails = lazy(() => import('./ResourceDetails'));
const GraphView = lazy(() => import('./GraphView'));

export const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route 
                    path="/resources/:id" 
                    element={
                        <Suspense fallback={<LoadingSpinner />}>
                            <ResourceDetails />
                        </Suspense>
                    } 
                />
                <Route 
                    path="/graph" 
                    element={
                        <Suspense fallback={<LoadingSpinner />}>
                            <GraphView />
                        </Suspense>
                    } 
                />
            </Routes>
        </Router>
    );
};
```

## Development Commands

### Cross-Platform Development
```bash
# Development
cd frontend && npm run dev         # All platforms
npm run dev                        # If in frontend directory

# Building
npm run build                      # Production build
npm run preview                    # Preview production build

# Testing
npm test                           # Run tests
npm run test:coverage              # Run tests with coverage
npm run test:watch                 # Run tests in watch mode

# Linting and Formatting
npm run lint                       # ESLint
npm run lint:fix                   # ESLint with auto-fix
npm run format                     # Prettier formatting
```

## TypeScript Best Practices

### Type Definitions
- Use **interface** for object shapes that might be extended
- Use **type** for unions, primitives, and computed types
- Prefer **strict mode** TypeScript configuration
- Use **generic types** for reusable components and functions

### Error Handling
```typescript
// Custom error types
export class ApiError extends Error {
    constructor(
        message: string,
        public status: number,
        public code?: string
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

// Type-safe error handling
export const handleApiError = (error: unknown): string => {
    if (error instanceof ApiError) {
        return `API Error (${error.status}): ${error.message}`;
    }
    
    if (error instanceof Error) {
        return error.message;
    }
    
    return 'An unknown error occurred';
};
```

### Environment Configuration
```typescript
// Environment variables with type safety
interface Environment {
    apiBaseUrl: string;
    appName: string;
    version: string;
    isDevelopment: boolean;
    isProduction: boolean;
}

export const env: Environment = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    appName: import.meta.env.VITE_APP_NAME || 'Application',
    version: import.meta.env.VITE_APP_VERSION || '1.0.0',
    isDevelopment: import.meta.env.DEV,
    isProduction: import.meta.env.PROD,
};
```
---
applyTo: "**/*.py,**/*.pyw,**/*.pyi,**/setup.py,**/setup.cfg,**/pyproject.toml,**/.python-version,**/requirements*.txt,**/Pipfile,**/poetry.lock"
---

# Python Development Standards and Guidelines

This document provides comprehensive guidelines for Python development, covering code style, architecture patterns, testing, security, and best practices for building robust, maintainable Python applications.

## Code Style Guidelines

### PEP 8 Compliance and Extensions

Follow PEP 8 as the foundation, with these specific guidelines:

#### Import Organization
```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

# Third-party imports
import requests
import pandas as pd
from flask import Flask, request, jsonify

# Local application imports
from .models import User, Database
from .utils import validation, logging
from ..config import settings
```

#### Function and Class Design
```python
class UserService:
    """Service class for managing user operations.
    
    This class handles CRUD operations for users and provides
    business logic for user management functionality.
    """
    
    def __init__(self, database: Database) -> None:
        """Initialize UserService with database connection.
        
        Args:
            database: Database instance for data operations
        """
        self._db = database
        self._logger = logging.get_logger(__name__)
    
    def create_user(
        self, 
        name: str, 
        email: str, 
        age: Optional[int] = None
    ) -> User:
        """Create a new user with validation.
        
        Args:
            name: User's full name (required)
            email: Valid email address (required)
            age: User's age in years (optional)
            
        Returns:
            User: Created user instance
            
        Raises:
            ValidationError: If input data is invalid
            DatabaseError: If user creation fails
        """
        # Validate input data
        if not validation.is_valid_email(email):
            raise ValidationError(f"Invalid email format: {email}")
        
        if age is not None and not (0 <= age <= 150):
            raise ValidationError(f"Invalid age: {age}")
        
        # Create user
        try:
            user = User(name=name, email=email, age=age)
            return self._db.save(user)
        except Exception as e:
            self._logger.error(f"Failed to create user: {e}")
            raise DatabaseError("User creation failed") from e
```

#### Type Annotations
Use comprehensive type hints for better code clarity and IDE support:

```python
from typing import Dict, List, Optional, Union, Callable, Any, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum

# Type variables for generics
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Status(Enum):
    """Enumeration for operation status."""
    PENDING = "pending"
    COMPLETED = "completed" 
    FAILED = "failed"

@dataclass
class Response(Generic[T]):
    """Generic response wrapper for API operations."""
    data: T
    status: Status
    message: Optional[str] = None
    errors: List[str] = None

    def __post_init__(self) -> None:
        if self.errors is None:
            self.errors = []

def process_data(
    data: List[Dict[str, Any]], 
    transformer: Callable[[Dict[str, Any]], T],
    filter_func: Optional[Callable[[T], bool]] = None
) -> Response[List[T]]:
    """Process data with transformation and optional filtering.
    
    Args:
        data: List of dictionaries to process
        transformer: Function to transform each dictionary
        filter_func: Optional function to filter results
        
    Returns:
        Response containing processed data
    """
    try:
        results = [transformer(item) for item in data]
        
        if filter_func:
            results = [item for item in results if filter_func(item)]
            
        return Response(
            data=results,
            status=Status.COMPLETED,
            message=f"Successfully processed {len(results)} items"
        )
    except Exception as e:
        return Response(
            data=[],
            status=Status.FAILED,
            message="Processing failed",
            errors=[str(e)]
        )
```

## Architecture Patterns

### Project Structure Standards

#### Package Organization
```
project/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py              # Application entry point
│       ├── config/              # Configuration management
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── database.py
│       ├── models/              # Data models and schemas
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── base.py
│       ├── services/            # Business logic layer
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── auth_service.py
│       ├── controllers/         # API controllers/handlers
│       │   ├── __init__.py
│       │   ├── user_controller.py
│       │   └── auth_controller.py
│       ├── repositories/        # Data access layer
│       │   ├── __init__.py
│       │   ├── user_repository.py
│       │   └── base_repository.py
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── validation.py
│       │   ├── logging.py
│       │   └── helpers.py
│       └── exceptions/          # Custom exceptions
│           ├── __init__.py
│           ├── base.py
│           └── validation.py
├── tests/                       # Test files
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
├── requirements/                # Dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── pyproject.toml              # Project configuration
├── README.md
└── .python-version             # Python version specification
```

### Dependency Injection Pattern
```python
from abc import ABC, abstractmethod
from typing import Protocol

class DatabaseProtocol(Protocol):
    """Protocol for database operations."""
    
    def save(self, entity: Any) -> Any:
        """Save entity to database."""
        ...
    
    def find_by_id(self, entity_id: str) -> Optional[Any]:
        """Find entity by ID."""
        ...

class UserRepository:
    """Repository for user data operations."""
    
    def __init__(self, database: DatabaseProtocol) -> None:
        self._db = database
    
    def create_user(self, user: User) -> User:
        """Create user in database."""
        return self._db.save(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._db.find_by_id(user_id)

class UserService:
    """Service for user business logic."""
    
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        """Register new user with business logic."""
        # Business logic here
        user = User(name=name, email=email)
        return self._repository.create_user(user)
```

### Configuration Management
```python
from pydantic import BaseSettings, Field
from typing import Optional
import os

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    name: str = Field(env="DB_NAME")
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASSWORD")
    ssl_mode: str = Field(default="prefer", env="DB_SSL_MODE")
    
    @property
    def url(self) -> str:
        """Generate database URL."""
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
            f"?sslmode={self.ssl_mode}"
        )

class AppSettings(BaseSettings):
    """Application configuration settings."""
    
    app_name: str = Field(default="MyApp", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(env="SECRET_KEY")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database settings
    database: DatabaseSettings = DatabaseSettings()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = AppSettings()
```

## Error Handling and Logging

### Custom Exception Hierarchy
```python
class AppError(Exception):
    """Base exception for application errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__

class ValidationError(AppError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field

class NotFoundError(AppError):
    """Raised when requested resource is not found."""
    
    def __init__(self, resource: str, identifier: str) -> None:
        message = f"{resource} with ID '{identifier}' not found"
        super().__init__(message, "NOT_FOUND")
        self.resource = resource
        self.identifier = identifier

class DatabaseError(AppError):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message, "DATABASE_ERROR")
        self.original_error = original_error
```

### Structured Logging
```python
import logging
import json
from datetime import datetime
from typing import Any, Dict

class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
            
        return json.dumps(log_entry)

def setup_logging(log_level: str = "INFO") -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )
    
    # Set structured formatter for all handlers
    formatter = StructuredFormatter()
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)

def get_logger(name: str) -> logging.Logger:
    """Get logger instance with structured formatting."""
    return logging.getLogger(name)
```

## Testing Standards

### Unit Testing with pytest
```python
import pytest
from unittest.mock import Mock, patch
from myproject.services.user_service import UserService
from myproject.models.user import User
from myproject.exceptions import ValidationError

class TestUserService:
    """Test suite for UserService class."""
    
    @pytest.fixture
    def mock_repository(self) -> Mock:
        """Create mock repository for testing."""
        return Mock()
    
    @pytest.fixture
    def user_service(self, mock_repository: Mock) -> UserService:
        """Create UserService instance with mocked dependencies."""
        return UserService(repository=mock_repository)
    
    def test_create_user_success(self, user_service: UserService, mock_repository: Mock) -> None:
        """Test successful user creation."""
        # Arrange
        expected_user = User(id="123", name="John Doe", email="john@example.com")
        mock_repository.create_user.return_value = expected_user
        
        # Act
        result = user_service.register_user("John Doe", "john@example.com")
        
        # Assert
        assert result == expected_user
        mock_repository.create_user.assert_called_once()
        
    def test_create_user_invalid_email(self, user_service: UserService) -> None:
        """Test user creation with invalid email."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.register_user("John Doe", "invalid-email")
        
        assert "Invalid email format" in str(exc_info.value)
    
    @pytest.mark.parametrize("name,email,expected_error", [
        ("", "john@example.com", "Name cannot be empty"),
        ("John", "", "Email cannot be empty"),
        ("A" * 256, "john@example.com", "Name too long"),
    ])
    def test_create_user_validation_errors(
        self, 
        user_service: UserService, 
        name: str, 
        email: str, 
        expected_error: str
    ) -> None:
        """Test various validation error scenarios."""
        with pytest.raises(ValidationError) as exc_info:
            user_service.register_user(name, email)
        
        assert expected_error in str(exc_info.value)
```

### Integration Testing
```python
import pytest
from httpx import AsyncClient
from myproject.main import app
from myproject.database import get_database
from tests.fixtures import test_database

@pytest.mark.asyncio
class TestUserAPI:
    """Integration tests for User API endpoints."""
    
    async def test_create_user_endpoint(self, test_client: AsyncClient) -> None:
        """Test user creation endpoint."""
        # Arrange
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        
        # Act
        response = await test_client.post("/api/users", json=user_data)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == user_data["name"]
        assert response_data["email"] == user_data["email"]
        assert "id" in response_data
    
    async def test_get_user_endpoint(self, test_client: AsyncClient, sample_user: User) -> None:
        """Test user retrieval endpoint."""
        # Act
        response = await test_client.get(f"/api/users/{sample_user.id}")
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == sample_user.id
        assert response_data["name"] == sample_user.name
```

### Test Configuration
```python
# conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from myproject.main import app
from myproject.database import Database

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_client():
    """Create test client for API testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def test_database():
    """Create test database instance."""
    db = Database(url="sqlite:///:memory:")
    db.create_tables()
    yield db
    db.drop_tables()
```

## Security Best Practices

### Input Validation and Sanitization
```python
from pydantic import BaseModel, validator, Field
import re
from typing import Optional

class UserCreateRequest(BaseModel):
    """Request model for user creation with validation."""
    
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    
    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate and sanitize name field."""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', v.strip())
        if not sanitized:
            raise ValueError('Name cannot be empty after sanitization')
        return sanitized
    
    @validator('email')
    def validate_email_domain(cls, v: str) -> str:
        """Additional email validation."""
        domain = v.split('@')[1]
        if domain in ['tempmail.com', 'throwaway.email']:
            raise ValueError('Temporary email addresses not allowed')
        return v.lower()

def sanitize_sql_input(value: str) -> str:
    """Sanitize input to prevent SQL injection."""
    # Remove or escape dangerous characters
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    sanitized = value
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized
```

### Authentication and Authorization
```python
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Service for authentication and authorization."""
    
    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None

# Role-based access control
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def require_role(required_role: Role):
    """Decorator for role-based access control."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract user role from context (request, session, etc.)
            user_role = get_current_user_role()  # Implementation depends on framework
            
            if user_role != required_role:
                raise PermissionError(f"Required role: {required_role.value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Secrets Management
```python
import os
from cryptography.fernet import Fernet
from typing import Optional

class SecretsManager:
    """Secure secrets management."""
    
    def __init__(self) -> None:
        # Load encryption key from environment or key management service
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable not set")
        self.cipher_suite = Fernet(key.encode())
    
    def encrypt_secret(self, secret: str) -> str:
        """Encrypt sensitive data."""
        return self.cipher_suite.encrypt(secret.encode()).decode()
    
    def decrypt_secret(self, encrypted_secret: str) -> str:
        """Decrypt sensitive data."""
        return self.cipher_suite.decrypt(encrypted_secret.encode()).decode()
    
    def get_database_url(self) -> str:
        """Get database URL with decrypted password."""
        encrypted_password = os.environ.get('DB_PASSWORD_ENCRYPTED')
        if encrypted_password:
            password = self.decrypt_secret(encrypted_password)
        else:
            password = os.environ.get('DB_PASSWORD', '')
        
        return f"postgresql://{os.environ.get('DB_USER')}:{password}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
```

## Performance Optimization

### Async Programming Patterns
```python
import asyncio
import aiohttp
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

class AsyncDataProcessor:
    """Asynchronous data processing service."""
    
    def __init__(self) -> None:
        self.session: Optional[aiohttp.ClientSession] = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
        self.executor.shutdown(wait=True)
    
    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from URL asynchronously."""
        async with self.session.get(url) as response:
            return await response.json()
    
    async def fetch_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch data from multiple URLs concurrently."""
        tasks = [self.fetch_data(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def cpu_intensive_task(self, data: List[int]) -> int:
        """Run CPU-intensive task in thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self._process_data_sync, 
            data
        )
    
    def _process_data_sync(self, data: List[int]) -> int:
        """Synchronous CPU-intensive processing."""
        return sum(x * x for x in data)

# Usage
async def main():
    async with AsyncDataProcessor() as processor:
        urls = ["https://api1.com", "https://api2.com", "https://api3.com"]
        results = await processor.fetch_multiple(urls)
        
        cpu_result = await processor.cpu_intensive_task(list(range(10000)))
        print(f"CPU task result: {cpu_result}")
```

### Caching Strategies
```python
import functools
import pickle
from typing import Any, Callable, Optional
import redis
from datetime import timedelta

class CacheManager:
    """Redis-based cache manager."""
    
    def __init__(self, redis_url: str) -> None:
        self.redis_client = redis.from_url(redis_url)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            cached_value = self.redis_client.get(key)
            return pickle.loads(cached_value) if cached_value else None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: timedelta = timedelta(hours=1)) -> None:
        """Set value in cache with TTL."""
        try:
            serialized_value = pickle.dumps(value)
            self.redis_client.setex(key, ttl, serialized_value)
        except Exception:
            pass  # Log error in production
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        self.redis_client.delete(key)

# Cache decorator
def cached(ttl: timedelta = timedelta(hours=1), key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator

# Global cache manager instance
cache_manager = CacheManager("redis://localhost:6379")

@cached(ttl=timedelta(minutes=30), key_prefix="user_")
def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Get user profile with caching."""
    # Expensive database operation
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}
```

## Database Integration

### SQLAlchemy Best Practices
```python
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class User(Base):
    """User model with SQLAlchemy."""
    
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"

class Post(Base):
    """Post model with foreign key relationship."""
    
    __tablename__ = 'posts'
    
    id = Column(String, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(String, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    author = relationship("User", back_populates="posts")

class DatabaseManager:
    """Database connection and session management."""
    
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(
            database_url,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
            echo=False  # Set to True for SQL debugging
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self) -> None:
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    def drop_tables(self) -> None:
        """Drop all database tables (for testing)."""
        Base.metadata.drop_all(bind=self.engine)

class UserRepository:
    """Repository pattern for User operations."""
    
    def __init__(self, db_session: Session) -> None:
        self.db = db_session
    
    def create(self, user: User) -> User:
        """Create new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List users with pagination."""
        return self.db.query(User).offset(offset).limit(limit).all()
    
    def update(self, user: User) -> User:
        """Update existing user."""
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
```

## Development Tools and Environment

### Project Configuration (pyproject.toml)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "1.0.0"
description = "Python project following best practices"
authors = [{name = "Development Team", email = "dev@example.com"}]
license = {file = "LICENSE"}
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]
test = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",
]

[project.scripts]
myproject = "myproject.main:main"

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["myproject"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=myproject",
    "--cov-report=html",
    "--cov-report=term-missing",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["myproject"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "setup.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Pre-commit Configuration (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings, flake8-import-order]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-requests]
```

### Development Scripts
```python
#!/usr/bin/env python3
"""Development utility scripts."""

import subprocess
import sys
from pathlib import Path

def run_tests(coverage: bool = True) -> int:
    """Run test suite with optional coverage."""
    cmd = ["python", "-m", "pytest"]
    if coverage:
        cmd.extend(["--cov=myproject", "--cov-report=html", "--cov-report=term"])
    
    return subprocess.call(cmd)

def run_linting() -> int:
    """Run all linting tools."""
    commands = [
        ["python", "-m", "black", "--check", "."],
        ["python", "-m", "isort", "--check-only", "."],
        ["python", "-m", "flake8", "."],
        ["python", "-m", "mypy", "myproject"],
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.call(cmd)
        if result != 0:
            return result
    
    return 0

def format_code() -> int:
    """Format code using black and isort."""
    commands = [
        ["python", "-m", "black", "."],
        ["python", "-m", "isort", "."],
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.call(cmd)
        if result != 0:
            return result
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py <command>")
        print("Commands: test, lint, format")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        sys.exit(run_tests())
    elif command == "lint":
        sys.exit(run_linting())
    elif command == "format":
        sys.exit(format_code())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

## Quality Assurance and Best Practices

### Code Quality Checklist
- [ ] **Type Hints**: All functions have proper type annotations
- [ ] **Docstrings**: All modules, classes, and functions documented
- [ ] **Error Handling**: Proper exception handling and custom exceptions
- [ ] **Testing**: Comprehensive unit and integration test coverage (>90%)
- [ ] **Security**: Input validation, SQL injection prevention, secrets management
- [ ] **Performance**: Async patterns where appropriate, caching strategies
- [ ] **Logging**: Structured logging with appropriate levels
- [ ] **Configuration**: Environment-based configuration management

### Development Workflow
1. **Setup Environment**: Use virtual environments (venv, conda, or poetry)
2. **Install Dependencies**: `pip install -e .[dev]` for development dependencies
3. **Pre-commit Hooks**: Install and configure pre-commit hooks
4. **Code Development**: Follow TDD (Test-Driven Development) practices
5. **Code Quality**: Run linting and type checking before commits
6. **Testing**: Maintain high test coverage and run tests frequently
7. **Documentation**: Keep docstrings and README updated
8. **Security Review**: Regular security audits and dependency updates

### Performance Monitoring
```python
import time
import functools
from typing import Callable

def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"{func.__name__} executed in {execution_time:.4f} seconds")
    return wrapper

# Memory profiling
import tracemalloc

def profile_memory(func: Callable) -> Callable:
    """Decorator to profile memory usage."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"{func.__name__} - Current memory: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB")
    return wrapper
```

This comprehensive Python instruction file provides world-class development standards covering all aspects of Python development, from basic syntax to advanced architectural patterns, ensuring robust, maintainable, and secure Python applications.
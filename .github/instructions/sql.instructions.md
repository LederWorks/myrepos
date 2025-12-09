---
applyTo: "**/*.sql,**/migrations/*.sql,**/schema/*.sql,**/seeds/*.sql,**/procedures/*.sql,**/functions/*.sql,**/triggers/*.sql,**/views/*.sql"
---

# SQL Development Standards and Guidelines

This document provides comprehensive guidelines for SQL development, covering database design, query optimization, security, migrations, and best practices for building robust, maintainable database systems.

## Database Design Standards

### Table Design Principles

#### Naming Conventions
```sql
-- Tables: Use plural nouns with snake_case
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes: Descriptive names indicating purpose
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_name_search ON users(first_name, last_name);

-- Foreign keys: Clear relationship indication
ALTER TABLE posts ADD CONSTRAINT fk_posts_author_id 
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE;

-- Check constraints: Business rule enforcement
ALTER TABLE users ADD CONSTRAINT chk_users_email_format 
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
```

#### Primary Key Strategy
```sql
-- Use UUIDs for distributed systems and security
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(20) NOT NULL UNIQUE, -- Human-readable identifier
    customer_id UUID NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status order_status_enum NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Use BIGSERIAL for high-performance sequential needs
CREATE TABLE analytics_events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_id UUID,
    data JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Composite keys for junction tables
CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by UUID NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users(id)
);
```

#### Data Types and Constraints
```sql
-- Use appropriate data types for efficiency and clarity
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    weight_grams INTEGER CHECK (weight_grams > 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    category_id UUID NOT NULL,
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT chk_products_name_length CHECK (LENGTH(name) >= 3),
    CONSTRAINT chk_products_price_precision CHECK (price = ROUND(price, 2)),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Enums for controlled vocabularies
CREATE TYPE order_status_enum AS ENUM (
    'pending',
    'confirmed',
    'processing',
    'shipped',
    'delivered',
    'cancelled',
    'refunded'
);

CREATE TYPE user_role_enum AS ENUM (
    'admin',
    'manager',
    'user',
    'guest'
);
```

### Indexing Strategy

#### Performance Indexes
```sql
-- Single column indexes for frequent WHERE clauses
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Composite indexes for multi-column queries (order matters!)
CREATE INDEX idx_orders_customer_status_date ON orders(customer_id, status, created_at);
CREATE INDEX idx_products_category_active ON products(category_id, is_active);

-- Partial indexes for filtered queries
CREATE INDEX idx_orders_pending ON orders(created_at) 
    WHERE status = 'pending';

CREATE INDEX idx_users_active_email ON users(email) 
    WHERE is_active = TRUE;

-- Expression indexes for computed queries
CREATE INDEX idx_users_full_name ON users(LOWER(first_name || ' ' || last_name));
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- JSONB indexes for JSON queries
CREATE INDEX idx_products_metadata ON products USING GIN(metadata);
CREATE INDEX idx_analytics_data_type ON analytics_events USING GIN((data->>'event_type'));
```

#### Index Maintenance
```sql
-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;

-- Analyze index size and efficiency
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Query Optimization

### Efficient Query Patterns

#### SELECT Statement Best Practices
```sql
-- Always specify columns explicitly (avoid SELECT *)
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name,
    p.title AS profile_title
FROM users u
LEFT JOIN profiles p ON u.id = p.user_id
WHERE u.is_active = TRUE
    AND u.created_at >= '2024-01-01'
ORDER BY u.created_at DESC
LIMIT 50;

-- Use CASE for conditional logic
SELECT 
    id,
    name,
    price,
    CASE 
        WHEN price >= 100 THEN 'Premium'
        WHEN price >= 50 THEN 'Standard'
        ELSE 'Economy'
    END AS price_tier,
    CASE 
        WHEN is_active THEN 'Available'
        ELSE 'Discontinued'
    END AS availability_status
FROM products
WHERE category_id = $1;

-- Window functions for analytics
SELECT 
    order_id,
    customer_id,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS order_rank,
    LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY created_at) AS previous_order_amount,
    AVG(total_amount) OVER (PARTITION BY customer_id) AS customer_avg_order
FROM orders
WHERE created_at >= '2024-01-01';
```

#### JOIN Optimization
```sql
-- Use appropriate JOIN types
-- INNER JOIN: Only matching records
SELECT 
    o.id,
    o.total_amount,
    c.email,
    c.first_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'completed'
    AND o.created_at >= CURRENT_DATE - INTERVAL '30 days';

-- LEFT JOIN: Include all records from left table
SELECT 
    c.id,
    c.email,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id 
    AND o.status = 'completed'
WHERE c.is_active = TRUE
GROUP BY c.id, c.email
ORDER BY total_spent DESC;

-- EXISTS for existence checks (often faster than JOIN)
SELECT c.id, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.id 
        AND o.total_amount > 1000
        AND o.created_at >= '2024-01-01'
);
```

#### Subquery Optimization
```sql
-- Correlated subqueries with proper indexing
SELECT 
    c.id,
    c.email,
    (
        SELECT COUNT(*)
        FROM orders o
        WHERE o.customer_id = c.id
            AND o.status = 'completed'
    ) AS completed_orders,
    (
        SELECT MAX(o.created_at)
        FROM orders o
        WHERE o.customer_id = c.id
    ) AS last_order_date
FROM customers c
WHERE c.is_active = TRUE;

-- Common Table Expressions (CTEs) for readability
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', created_at) AS month,
        SUM(total_amount) AS total_sales,
        COUNT(*) AS order_count
    FROM orders
    WHERE status = 'completed'
        AND created_at >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', created_at)
),
sales_growth AS (
    SELECT 
        month,
        total_sales,
        order_count,
        LAG(total_sales) OVER (ORDER BY month) AS prev_month_sales,
        (total_sales - LAG(total_sales) OVER (ORDER BY month)) / 
            LAG(total_sales) OVER (ORDER BY month) * 100 AS growth_percentage
    FROM monthly_sales
)
SELECT 
    month,
    total_sales,
    order_count,
    ROUND(growth_percentage, 2) AS growth_percentage
FROM sales_growth
ORDER BY month;
```

### Query Performance Analysis

#### EXPLAIN and Query Planning
```sql
-- Basic EXPLAIN for execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT o.id, o.total_amount, c.email
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
    AND c.is_active = TRUE
ORDER BY o.created_at DESC;

-- EXPLAIN with detailed analysis
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)
SELECT 
    category_id,
    COUNT(*) AS product_count,
    AVG(price) AS avg_price,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS active_count
FROM products
GROUP BY category_id
HAVING COUNT(*) > 10;

-- Query performance monitoring
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

## Database Security

### Access Control and Permissions

#### Role-Based Access Control
```sql
-- Create application-specific roles
CREATE ROLE app_read_only;
CREATE ROLE app_read_write;
CREATE ROLE app_admin;

-- Grant appropriate permissions
GRANT CONNECT ON DATABASE myapp TO app_read_only;
GRANT USAGE ON SCHEMA public TO app_read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read_only;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO app_read_only;

GRANT app_read_only TO app_read_write;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_read_write;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_read_write;

GRANT app_read_write TO app_admin;
GRANT CREATE ON SCHEMA public TO app_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_admin;

-- Create application users
CREATE USER app_api WITH PASSWORD 'secure_password_here';
CREATE USER app_batch WITH PASSWORD 'secure_password_here';
CREATE USER app_readonly WITH PASSWORD 'secure_password_here';

-- Assign roles to users
GRANT app_read_write TO app_api;
GRANT app_admin TO app_batch;
GRANT app_read_only TO app_readonly;

-- Row-level security example
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_orders_policy ON orders
    FOR ALL
    TO app_read_write
    USING (customer_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY admin_orders_policy ON orders
    FOR ALL
    TO app_admin
    USING (true);
```

#### Input Validation and Sanitization
```sql
-- Use parameterized queries (prevent SQL injection)
-- Good practice in application code:
-- SELECT * FROM users WHERE email = $1 AND is_active = $2

-- Database-level validation with constraints
ALTER TABLE users ADD CONSTRAINT chk_users_email_valid
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

ALTER TABLE products ADD CONSTRAINT chk_products_price_positive
    CHECK (price > 0);

ALTER TABLE orders ADD CONSTRAINT chk_orders_total_reasonable
    CHECK (total_amount >= 0 AND total_amount <= 1000000);

-- Function for safe user input handling
CREATE OR REPLACE FUNCTION sanitize_search_term(search_term TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Remove potentially dangerous characters
    search_term := regexp_replace(search_term, '[;''"\\]', '', 'g');
    -- Limit length
    search_term := substring(search_term, 1, 100);
    -- Trim whitespace
    search_term := trim(search_term);
    
    RETURN search_term;
END;
$$ LANGUAGE plpgsql;
```

#### Data Encryption and Sensitive Data
```sql
-- Use pgcrypto for encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Store sensitive data encrypted
CREATE TABLE user_sensitive_data (
    user_id UUID PRIMARY KEY,
    encrypted_ssn BYTEA,
    encrypted_credit_card BYTEA,
    encryption_key_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Function to encrypt sensitive data
CREATE OR REPLACE FUNCTION encrypt_sensitive_data(
    data TEXT,
    key_data TEXT
) RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(data, key_data);
END;
$$ LANGUAGE plpgsql;

-- Function to decrypt sensitive data
CREATE OR REPLACE FUNCTION decrypt_sensitive_data(
    encrypted_data BYTEA,
    key_data TEXT
) RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(encrypted_data, key_data);
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL; -- Handle decryption errors gracefully
END;
$$ LANGUAGE plpgsql;

-- Hash passwords securely
CREATE OR REPLACE FUNCTION hash_password(password TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN crypt(password, gen_salt('bf', 12));
END;
$$ LANGUAGE plpgsql;

-- Verify passwords
CREATE OR REPLACE FUNCTION verify_password(password TEXT, hash TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN hash = crypt(password, hash);
END;
$$ LANGUAGE plpgsql;
```

## Database Migrations

### Migration Structure and Versioning

#### Migration File Organization
```sql
-- migrations/001_initial_schema.up.sql
-- Create initial database structure
BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create enums
CREATE TYPE user_status_enum AS ENUM ('active', 'inactive', 'suspended');

-- Create tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    status user_status_enum NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Insert default data
INSERT INTO users (email, password_hash, first_name, last_name, status)
VALUES ('admin@example.com', crypt('admin_password', gen_salt('bf')), 'Admin', 'User', 'active');

COMMIT;
```

```sql
-- migrations/001_initial_schema.down.sql
-- Rollback script for migration 001
BEGIN;

DROP TABLE IF EXISTS users CASCADE;
DROP TYPE IF EXISTS user_status_enum;
DROP EXTENSION IF EXISTS "uuid-ossp";
DROP EXTENSION IF EXISTS "pgcrypto";

COMMIT;
```

#### Migration Best Practices
```sql
-- migrations/002_add_products_table.up.sql
BEGIN;

-- Always use IF NOT EXISTS for idempotency
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category_id UUID NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

-- Create indexes after table creation
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);

-- Insert reference data
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Clothing', 'Apparel and fashion items'),
    ('Books', 'Books and educational materials')
ON CONFLICT (name) DO NOTHING;

COMMIT;
```

#### Data Migration Patterns
```sql
-- migrations/003_migrate_user_data.up.sql
-- Safe data migration with validation
BEGIN;

-- Add new columns with defaults
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP WITH TIME ZONE;

-- Update existing data in batches
DO $$
DECLARE
    batch_size INTEGER := 1000;
    processed INTEGER := 0;
    total_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_count FROM users WHERE email_verified IS NULL;
    
    WHILE processed < total_count LOOP
        UPDATE users 
        SET email_verified = TRUE,
            updated_at = NOW()
        WHERE id IN (
            SELECT id FROM users 
            WHERE email_verified IS NULL 
            LIMIT batch_size
        );
        
        processed := processed + batch_size;
        
        -- Log progress
        RAISE NOTICE 'Processed % of % users', processed, total_count;
        
        -- Commit batch and continue
        COMMIT;
        BEGIN;
    END LOOP;
END $$;

COMMIT;
```

## Stored Procedures and Functions

### Function Development Standards

#### Business Logic Functions
```sql
-- Calculate customer lifetime value
CREATE OR REPLACE FUNCTION calculate_customer_ltv(
    p_customer_id UUID,
    p_months INTEGER DEFAULT 12
) RETURNS DECIMAL(10,2) AS $$
DECLARE
    ltv_amount DECIMAL(10,2);
    avg_monthly_spend DECIMAL(10,2);
    months_active INTEGER;
BEGIN
    -- Validate inputs
    IF p_customer_id IS NULL THEN
        RAISE EXCEPTION 'Customer ID cannot be null';
    END IF;
    
    IF p_months <= 0 THEN
        RAISE EXCEPTION 'Months must be greater than zero';
    END IF;
    
    -- Calculate average monthly spend
    SELECT 
        COALESCE(AVG(monthly_total), 0),
        COUNT(*)
    INTO avg_monthly_spend, months_active
    FROM (
        SELECT 
            DATE_TRUNC('month', created_at) as month,
            SUM(total_amount) as monthly_total
        FROM orders
        WHERE customer_id = p_customer_id
            AND status = 'completed'
            AND created_at >= NOW() - INTERVAL '1 year'
        GROUP BY DATE_TRUNC('month', created_at)
    ) monthly_orders;
    
    -- Calculate LTV projection
    IF months_active > 0 THEN
        ltv_amount := avg_monthly_spend * LEAST(p_months, months_active * 2);
    ELSE
        ltv_amount := 0;
    END IF;
    
    RETURN ltv_amount;
END;
$$ LANGUAGE plpgsql;

-- Usage example with error handling
SELECT 
    customer_id,
    email,
    calculate_customer_ltv(customer_id, 24) as projected_ltv_24m
FROM customers
WHERE is_active = TRUE
ORDER BY projected_ltv_24m DESC;
```

#### Data Processing Functions
```sql
-- Audit trail function
CREATE OR REPLACE FUNCTION create_audit_record()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert audit record for any table change
    INSERT INTO audit_log (
        table_name,
        operation,
        row_id,
        old_data,
        new_data,
        changed_by,
        changed_at
    ) VALUES (
        TG_TABLE_NAME,
        TG_OP,
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END,
        current_setting('app.current_user_id', true),
        NOW()
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Create audit table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    row_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Apply audit trigger to tables
CREATE TRIGGER audit_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION create_audit_record();

CREATE TRIGGER audit_orders_trigger
    AFTER INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE FUNCTION create_audit_record();
```

#### Utility Functions
```sql
-- Generate human-readable IDs
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS VARCHAR(20) AS $$
DECLARE
    prefix VARCHAR(5) := 'ORD';
    timestamp_part VARCHAR(10);
    random_part VARCHAR(5);
    sequence_part VARCHAR(5);
BEGIN
    -- Get timestamp component (YYYYMMDD)
    timestamp_part := TO_CHAR(NOW(), 'YYYYMMDD');
    
    -- Get random component
    random_part := LPAD(FLOOR(RANDOM() * 99999)::TEXT, 5, '0');
    
    -- Combine parts
    RETURN prefix || timestamp_part || random_part;
END;
$$ LANGUAGE plpgsql;

-- Email validation function
CREATE OR REPLACE FUNCTION is_valid_email(email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
           AND LENGTH(email) <= 254
           AND email NOT LIKE '%..'
           AND email NOT LIKE '.%'
           AND email NOT LIKE '%.'
           AND SPLIT_PART(email, '@', 2) ~ '^[A-Za-z0-9.-]+$';
END;
$$ LANGUAGE plpgsql;
```

## Database Monitoring and Maintenance

### Performance Monitoring Queries

#### Database Health Checks
```sql
-- Database size and growth
SELECT 
    datname AS database_name,
    pg_size_pretty(pg_database_size(datname)) AS size,
    pg_database_size(datname) AS size_bytes
FROM pg_database 
WHERE datistemplate = FALSE
ORDER BY pg_database_size(datname) DESC;

-- Table sizes and row counts
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes,
    n_tup_ins AS inserts,
    n_tup_upd AS updates,
    n_tup_del AS deletes,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan AS scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

#### Connection and Lock Monitoring
```sql
-- Active connections and queries
SELECT 
    pid,
    usename AS username,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    EXTRACT(EPOCH FROM (NOW() - query_start)) AS query_duration_seconds,
    LEFT(query, 100) AS query_preview
FROM pg_stat_activity
WHERE state != 'idle'
    AND pid != pg_backend_pid()
ORDER BY query_start;

-- Blocking queries and locks
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement,
    blocked_activity.application_name AS blocked_application,
    blocking_activity.application_name AS blocking_application,
    blocked_locks.mode AS blocked_mode,
    blocking_locks.mode AS blocking_mode
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.GRANTED;
```

### Maintenance Scripts

#### Automated Cleanup and Optimization
```sql
-- Vacuum and analyze maintenance
CREATE OR REPLACE FUNCTION maintain_table_stats()
RETURNS TEXT AS $$
DECLARE
    table_record RECORD;
    maintenance_log TEXT := '';
BEGIN
    -- Loop through tables that need maintenance
    FOR table_record IN 
        SELECT schemaname, tablename, n_dead_tup, n_live_tup
        FROM pg_stat_user_tables
        WHERE n_dead_tup > 1000 
           OR (n_dead_tup > 0 AND n_dead_tup::FLOAT / GREATEST(n_live_tup, 1) > 0.1)
    LOOP
        -- Vacuum and analyze table
        EXECUTE format('VACUUM ANALYZE %I.%I', table_record.schemaname, table_record.tablename);
        maintenance_log := maintenance_log || format('Vacuumed %s.%s (dead tuples: %s)' || E'\n', 
                                                   table_record.schemaname, 
                                                   table_record.tablename, 
                                                   table_record.n_dead_tup);
    END LOOP;
    
    RETURN COALESCE(maintenance_log, 'No tables required maintenance');
END;
$$ LANGUAGE plpgsql;

-- Archive old data function
CREATE OR REPLACE FUNCTION archive_old_audit_logs(
    p_retention_days INTEGER DEFAULT 90
) RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER;
    cutoff_date TIMESTAMP WITH TIME ZONE;
BEGIN
    cutoff_date := NOW() - INTERVAL '1 day' * p_retention_days;
    
    -- Move old records to archive table
    INSERT INTO audit_log_archive 
    SELECT * FROM audit_log 
    WHERE changed_at < cutoff_date;
    
    GET DIAGNOSTICS archived_count = ROW_COUNT;
    
    -- Delete old records from main table
    DELETE FROM audit_log 
    WHERE changed_at < cutoff_date;
    
    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;
```

## Testing and Quality Assurance

### Database Testing Strategies

#### Unit Testing for Functions
```sql
-- Test framework setup
CREATE SCHEMA IF NOT EXISTS tests;

CREATE OR REPLACE FUNCTION tests.assert_equals(
    expected ANYELEMENT,
    actual ANYELEMENT,
    test_name TEXT DEFAULT 'Assertion'
) RETURNS BOOLEAN AS $$
BEGIN
    IF expected IS DISTINCT FROM actual THEN
        RAISE EXCEPTION 'Test failed: % - Expected: %, Actual: %', test_name, expected, actual;
    END IF;
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Test cases for calculate_customer_ltv function
CREATE OR REPLACE FUNCTION tests.test_calculate_customer_ltv()
RETURNS SETOF TEXT AS $$
DECLARE
    test_customer_id UUID;
    test_ltv DECIMAL(10,2);
BEGIN
    -- Setup test data
    test_customer_id := gen_random_uuid();
    
    INSERT INTO customers (id, email, first_name, last_name) VALUES
        (test_customer_id, 'test@example.com', 'Test', 'Customer');
    
    INSERT INTO orders (customer_id, total_amount, status, created_at) VALUES
        (test_customer_id, 100.00, 'completed', NOW() - INTERVAL '30 days'),
        (test_customer_id, 150.00, 'completed', NOW() - INTERVAL '60 days'),
        (test_customer_id, 200.00, 'completed', NOW() - INTERVAL '90 days');
    
    -- Test normal case
    SELECT calculate_customer_ltv(test_customer_id, 12) INTO test_ltv;
    RETURN NEXT tests.assert_equals(1800.00, test_ltv, 'LTV calculation for 12 months');
    
    -- Test with null customer ID (should raise exception)
    BEGIN
        SELECT calculate_customer_ltv(NULL, 12) INTO test_ltv;
        RETURN NEXT 'FAIL: Should have raised exception for null customer ID';
    EXCEPTION
        WHEN OTHERS THEN
            RETURN NEXT 'PASS: Correctly raised exception for null customer ID';
    END;
    
    -- Cleanup test data
    DELETE FROM orders WHERE customer_id = test_customer_id;
    DELETE FROM customers WHERE id = test_customer_id;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Run test
SELECT tests.test_calculate_customer_ltv();
```

#### Performance Testing
```sql
-- Performance test for query optimization
CREATE OR REPLACE FUNCTION tests.performance_test_user_orders()
RETURNS TABLE(
    test_name TEXT,
    execution_time_ms NUMERIC,
    rows_returned BIGINT
) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    row_count BIGINT;
BEGIN
    -- Test 1: Query with proper indexing
    test_name := 'User orders with index';
    start_time := clock_timestamp();
    
    SELECT COUNT(*) INTO row_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE c.email = 'test@example.com'
        AND o.created_at >= '2024-01-01';
    
    end_time := clock_timestamp();
    execution_time_ms := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
    rows_returned := row_count;
    RETURN NEXT;
    
    -- Test 2: Query without optimal indexing (for comparison)
    test_name := 'User orders full table scan';
    start_time := clock_timestamp();
    
    SELECT COUNT(*) INTO row_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE UPPER(c.email) = 'TEST@EXAMPLE.COM'  -- Forces full scan
        AND o.created_at >= '2024-01-01';
    
    end_time := clock_timestamp();
    execution_time_ms := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
    rows_returned := row_count;
    RETURN NEXT;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Run performance test
SELECT * FROM tests.performance_test_user_orders();
```

## Development Workflow and Best Practices

### Code Review Checklist
- [ ] **Schema Changes**: Reviewed for breaking changes and backward compatibility
- [ ] **Indexing Strategy**: Appropriate indexes created for query patterns  
- [ ] **Data Types**: Optimal data types chosen for storage and performance
- [ ] **Constraints**: Business rules enforced through database constraints
- [ ] **Security**: No SQL injection vulnerabilities, proper access controls
- [ ] **Performance**: Query plans analyzed, no unnecessary full table scans
- [ ] **Migration Safety**: Migrations are reversible and handle edge cases
- [ ] **Documentation**: Complex queries and functions are well documented
- [ ] **Testing**: Unit tests for functions, integration tests for workflows

### Environment Management

#### Development Database Setup
```sql
-- Development database initialization script
-- dev_setup.sql

-- Create development-specific extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create development roles
CREATE ROLE dev_read_write;
GRANT CONNECT ON DATABASE myapp_dev TO dev_read_write;
GRANT USAGE ON SCHEMA public TO dev_read_write;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dev_read_write;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dev_read_write;

-- Create test data generator
CREATE OR REPLACE FUNCTION generate_test_data(num_users INTEGER DEFAULT 100)
RETURNS TEXT AS $$
DECLARE
    i INTEGER;
    user_id UUID;
BEGIN
    FOR i IN 1..num_users LOOP
        user_id := gen_random_uuid();
        
        INSERT INTO customers (id, email, first_name, last_name) VALUES
            (user_id, 
             'user' || i || '@example.com',
             'User',
             i::TEXT);
        
        -- Generate random orders for each user
        INSERT INTO orders (customer_id, total_amount, status, created_at)
        SELECT 
            user_id,
            ROUND((RANDOM() * 1000)::NUMERIC, 2),
            (ARRAY['pending', 'completed', 'cancelled'])[FLOOR(RANDOM() * 3) + 1],
            NOW() - INTERVAL '1 day' * FLOOR(RANDOM() * 365)
        FROM generate_series(1, FLOOR(RANDOM() * 5) + 1);
    END LOOP;
    
    RETURN format('Generated test data for %s users', num_users);
END;
$$ LANGUAGE plpgsql;
```

### Documentation Standards

#### Function and Procedure Documentation
```sql
-- Well-documented function example
/**
 * Calculates the monthly recurring revenue (MRR) for a given time period
 * 
 * @param p_start_date The start date for the calculation period
 * @param p_end_date The end date for the calculation period  
 * @param p_include_trials Whether to include trial subscriptions in the calculation
 * 
 * @returns The total MRR as a decimal value
 * 
 * @example
 * SELECT calculate_mrr('2024-01-01', '2024-01-31', false);
 * 
 * @note This function only includes completed and active subscriptions
 * @note Trial subscriptions are excluded by default to provide accurate revenue figures
 * 
 * @author Development Team
 * @created 2024-01-15
 * @modified 2024-02-01 - Added trial subscription parameter
 */
CREATE OR REPLACE FUNCTION calculate_mrr(
    p_start_date DATE,
    p_end_date DATE,
    p_include_trials BOOLEAN DEFAULT FALSE
) RETURNS DECIMAL(12,2) AS $$
-- Function implementation here
$$ LANGUAGE plpgsql;
```

This comprehensive SQL instruction file provides world-class database development standards covering schema design, query optimization, security, migrations, stored procedures, monitoring, and testing practices for building robust, scalable database systems.
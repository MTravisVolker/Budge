-- Create the database
CREATE DATABASE budg;

-- Connect to the database
\c budg;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE api_token (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    token TEXT NOT NULL UNIQUE,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE TABLE oauth_account (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    provider VARCHAR(50) NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, account_id)
);

CREATE TABLE bill_status (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    name VARCHAR(100) NOT NULL,
    archived BOOLEAN DEFAULT FALSE,
    highlight_color_hex VARCHAR(7)
);

CREATE TABLE recurrence (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    name VARCHAR(100) NOT NULL,
    calculation VARCHAR(20),
    archived BOOLEAN DEFAULT FALSE
);

CREATE TABLE category (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    name VARCHAR(100) NOT NULL,
    archived BOOLEAN DEFAULT FALSE
);

CREATE TABLE bank_account (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    name VARCHAR(100) NOT NULL,
    url VARCHAR(100) CHECK (url ~ '^https?://'),
    recurrence SMALLINT REFERENCES recurrence(id),
    recurrence_value INTEGER CHECK (recurrence_value > 0),
    archived BOOLEAN DEFAULT FALSE,
    font_color_hex VARCHAR(7) NOT NULL CHECK (font_color_hex ~ '^#[0-9A-Fa-f]{6}$')
);

CREATE TABLE bills (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    name VARCHAR(100) NOT NULL,
    default_amount_due DECIMAL(10,2) NOT NULL,
    url VARCHAR(100) CHECK (url ~ '^https?://'),
    archived BOOLEAN DEFAULT FALSE,
    default_draft_account SMALLINT REFERENCES bank_account(id),
    category SMALLINT REFERENCES category(id),
    recurrence SMALLINT REFERENCES recurrence(id),
    recurrence_value INTEGER CHECK (recurrence_value > 0)
);

CREATE TABLE due_bills (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    bill SMALLINT NOT NULL REFERENCES bills(id),
    recurrence SMALLINT REFERENCES recurrence(id),
    recurrence_value INTEGER CHECK (recurrence_value > 0),
    priority INTEGER NOT NULL DEFAULT 0,
    due_date DATE NOT NULL,
    pay_date DATE,
    min_amount_due DECIMAL(10,2) NOT NULL,
    total_amount_due DECIMAL(10,2) NOT NULL,
    status SMALLINT REFERENCES bill_status(id),
    archived BOOLEAN DEFAULT FALSE,
    confirmation VARCHAR(100),
    notes TEXT,
    draft_account SMALLINT REFERENCES bank_account(id)
);

CREATE TABLE bank_account_instance (
    id SMALLSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    bank_account SMALLINT NOT NULL REFERENCES bank_account(id),
    priority INTEGER NOT NULL DEFAULT 0,
    due_date DATE NOT NULL,
    pay_date DATE,
    status SMALLINT REFERENCES bill_status(id),
    archived BOOLEAN DEFAULT FALSE,
    current_balance DECIMAL(10,2) NOT NULL
);

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES "user"(id),
    table_name VARCHAR(50) NOT NULL,
    row_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('add', 'update', 'delete')),
    value_before_change TEXT,
    value_after_change TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_api_token_user_id ON api_token(user_id);
CREATE INDEX idx_oauth_account_user_id ON oauth_account(user_id);
CREATE INDEX idx_bill_status_user_id ON bill_status(user_id);
CREATE INDEX idx_bill_status_name ON bill_status(name);
CREATE INDEX idx_recurrence_user_id ON recurrence(user_id);
CREATE INDEX idx_recurrence_name ON recurrence(name);
CREATE INDEX idx_category_user_id ON category(user_id);
CREATE INDEX idx_category_name ON category(name);
CREATE INDEX idx_bank_account_user_id ON bank_account(user_id);
CREATE INDEX idx_bank_account_name ON bank_account(name);
CREATE INDEX idx_bank_account_recurrence ON bank_account(recurrence);
CREATE INDEX idx_bills_user_id ON bills(user_id);
CREATE INDEX idx_bills_name ON bills(name);
CREATE INDEX idx_bills_default_draft_account ON bills(default_draft_account);
CREATE INDEX idx_bills_category ON bills(category);
CREATE INDEX idx_due_bills_user_id ON due_bills(user_id);
CREATE INDEX idx_due_bills_bill ON due_bills(bill);
CREATE INDEX idx_due_bills_recurrence ON due_bills(recurrence);
CREATE INDEX idx_due_bills_due_date ON due_bills(due_date);
CREATE INDEX idx_due_bills_pay_date ON due_bills(pay_date);
CREATE INDEX idx_due_bills_status ON due_bills(status);
CREATE INDEX idx_due_bills_draft_account ON due_bills(draft_account);
CREATE INDEX idx_due_bills_priority ON due_bills(priority);
CREATE INDEX idx_bank_account_instance_user_id ON bank_account_instance(user_id);
CREATE INDEX idx_bank_account_instance_bank_account ON bank_account_instance(bank_account);
CREATE INDEX idx_bank_account_instance_due_date ON bank_account_instance(due_date);
CREATE INDEX idx_bank_account_instance_pay_date ON bank_account_instance(pay_date);
CREATE INDEX idx_bank_account_instance_status ON bank_account_instance(status);
CREATE INDEX idx_bank_account_instance_priority ON bank_account_instance(priority);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_log_row_id ON audit_log(row_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);

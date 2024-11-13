-- Create table 'extract'
CREATE TABLE BankExtract (
    id SERIAL PRIMARY KEY,
    agency_number VARCHAR(10) NOT NULL,
    account_number VARCHAR(10) NOT NULL,
    start_date VARCHAR(100) NOT NULL,
    end_date VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table 'balance'
CREATE TABLE balance (
    id SERIAL PRIMARY KEY,
    agency_number VARCHAR(10) NOT NULL,
    account_number VARCHAR(10) NOT NULL,
    value VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Criação da tabela 'tokens'
CREATE TYPE TokenType AS ENUM ('consult', 'pix');

CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR NOT NULL,
    token_type TokenType NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table 'fund_secret'
CREATE TABLE fund_secret (
    id SERIAL PRIMARY KEY,
    fund_number INT NOT NULL,
    balance_service_key INT NOT NULL,
    extract_service_key INT NOT NULL,
    transfer_service_key INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Criação da tabela 'workspace'
CREATE TABLE workspace (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(50) UNIQUE NOT NULL,
    account VARCHAR(50) UNIQUE NOT NULL,
    agency VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela 'transfer'
CREATE TYPE Payment AS ENUM ('yes', 'no');

CREATE TABLE transfer (
    id SERIAL PRIMARY KEY,
    transfer_id VARCHAR(50) UNIQUE NOT NULL,
    workspace_id INT NOT NULL,
    value VARCHAR(50) NOT NULL,
    payment_confirm Payment NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);

-- Create table 'request'
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    request_type VARCHAR(255) NOT NULL,
    extract_key INT,
    balance_key INT NOT NULL,
    tokens_key INT,
    transfer_key INT,
    workspace_key INT,
    method VARCHAR(50) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    status_code INT NOT NULL,
    response JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (extract_key) REFERENCES BankExtract(id),
    FOREIGN KEY (balance_key) REFERENCES balance(id),
    FOREIGN KEY (tokens_key) REFERENCES tokens(id),
    FOREIGN KEY (transfer_key) REFERENCES transfer(id),
    FOREIGN KEY (workspace_key) REFERENCES workspace(id)
);

-- Create indices
CREATE INDEX ix_request_id_created_at ON requests (id, created_at);
CREATE INDEX ix_extract_id_created_at ON BankExtract (id, created_at);
CREATE INDEX ix_balance_id_created_at ON balance (id, created_at);
CREATE INDEX ix_secret_id_created_at ON fund_secret (id, created_at);

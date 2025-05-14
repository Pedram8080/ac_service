#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    -- Create database if not exists
    SELECT 'CREATE DATABASE ac_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ac_db')\gexec

    -- Set password for postgres user
    ALTER USER postgres WITH PASSWORD 'admin123';

    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE ac_db TO postgres;

    -- Connect to ac_db and set up extensions
    \c ac_db
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    
    -- Set up some basic configurations
    ALTER DATABASE ac_db SET timezone TO 'UTC';
    ALTER DATABASE ac_db SET client_encoding TO 'UTF8';
    ALTER DATABASE ac_db SET default_transaction_isolation TO 'read committed';
EOSQL 
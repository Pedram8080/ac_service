#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE ac_db;
    ALTER USER postgres WITH PASSWORD 'admin123';
    GRANT ALL PRIVILEGES ON DATABASE ac_db TO postgres;
EOSQL 
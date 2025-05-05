#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ac_user WITH PASSWORD 'ac_pass';
    CREATE DATABASE ac_db;
    GRANT ALL PRIVILEGES ON DATABASE ac_db TO ac_user;
EOSQL 
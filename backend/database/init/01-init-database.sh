#!/bin/sh
set -eu

psql \
  --username "${POSTGRES_USER}" \
  --dbname "postgres" \
  --set=ON_ERROR_STOP=1 \
  --set=app_db_name="${APP_DB_NAME}" \
  --set=app_db_user="${APP_DB_USER}" \
  --set=app_db_password="${APP_DB_PASSWORD}" <<'SQL'
SELECT format(
  'CREATE ROLE %I LOGIN',
  :'app_db_user'
)
WHERE NOT EXISTS (
  SELECT 1 FROM pg_roles WHERE rolname = :'app_db_user'
)\gexec

SELECT format(
  'ALTER ROLE %I PASSWORD %L',
  :'app_db_user',
  :'app_db_password'
)\gexec

SELECT format(
  'CREATE DATABASE %I',
  :'app_db_name'
)
WHERE NOT EXISTS (
  SELECT 1 FROM pg_database WHERE datname = :'app_db_name'
)\gexec

SELECT format(
  'ALTER DATABASE %I OWNER TO %I',
  :'app_db_name',
  :'app_db_user'
)\gexec
SQL

psql \
  --username "${POSTGRES_USER}" \
  --dbname "${APP_DB_NAME}" \
  --set=ON_ERROR_STOP=1 \
  --set=app_db_user="${APP_DB_USER}" <<'SQL'
ALTER SCHEMA public OWNER TO :"app_db_user";
GRANT ALL ON SCHEMA public TO :"app_db_user";
SQL

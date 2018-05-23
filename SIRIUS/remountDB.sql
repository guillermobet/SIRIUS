REVOKE ALL PRIVILEGES ON DATABASE sirius FROM sirius;
DROP USER sirius;
DROP DATABASE sirius;

CREATE DATABASE sirius;
CREATE USER sirius WITH PASSWORD 'black';
ALTER ROLE sirius SET client_encoding TO 'utf8';
ALTER ROLE sirius SET default_transaction_isolation TO 'read committed';
ALTER ROLE sirius SET timezone TO 'America/Caracas';
GRANT ALL PRIVILEGES ON DATABASE sirius TO sirius;

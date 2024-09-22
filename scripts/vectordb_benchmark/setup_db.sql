CREATE ROLE main_user WITH LOGIN PASSWORD '123456';
CREATE DATABASE main_database;
\connect main_database
GRANT ALL PRIVILEGES ON DATABASE main_database TO main_user;
GRANT USAGE ON SCHEMA public TO main_user;
GRANT CREATE ON SCHEMA public TO main_user;
CREATE EXTENSION vector;



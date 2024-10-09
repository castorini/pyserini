#!/bin/bash
# Check if data directory is provided
if [ $# -eq 0 ]; then
    echo "Please provide the data directory path as an argument."
    exit 1
fi

DATA_DIR=$1

# Create data directory if it doesn't exist
if [ ! -d "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo "Created data directory: $DATA_DIR"
fi

# Initialize PostgreSQL database
initdb -D "$DATA_DIR"

# Start PostgreSQL server
pg_ctl -D "$DATA_DIR" -l logfile start

# Wait for the server to start
sleep 5

# Connect to PostgreSQL and run commands
psql -d postgres -f setup_db.sql

echo "Database initialization and setup completed."

# Note: Keep the server running. To stop it later, use:
# pg_ctl -D "$DATA_DIR" stop

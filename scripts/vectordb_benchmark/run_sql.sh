#!/bin/bash

# Check if all required arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <sql_script_path> <username> <database_name>"
    exit 1
fi

# Assign input arguments to variables
SQL_SCRIPT=$1
USERNAME=$2
DATABASE=$3

# Check if the SQL script file exists
if [ ! -f "$SQL_SCRIPT" ]; then
    echo "Error: SQL script file '$SQL_SCRIPT' not found."
    exit 1
fi

# Execute the SQL script using psql
psql -U "$USERNAME" -d "$DATABASE" -f "$SQL_SCRIPT" -v ON_ERROR_STOP=1 --echo-all

# Check the exit status of psql
if [ $? -eq 0 ]; then
    echo "SQL script executed successfully."
else
    echo "Error: SQL script execution failed."
    exit 1
fi
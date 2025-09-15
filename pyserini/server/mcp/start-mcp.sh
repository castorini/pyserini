#!/bin/bash

# NOTE: change the BASH_HOME and CONDA_ENV variables to match your setup
BASH_HOME="$HOME/.bashrc" 
CONDA_ENV="pyserini" 

set -e

cleanup() {
    echo "Received termination signal, shutting down gracefully..."
    # Kill any background processes if needed
    jobs -p | xargs -r kill
    exit 0
}

trap cleanup SIGTERM SIGINT

source "${BASH_HOME}"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo -e "Error: conda not found. Please ensure conda is installed and in PATH."
    exit 1
fi

eval "$(conda shell.bash hook)"

# Check if the conda environment exists
if ! conda env list | grep -q "^${CONDA_ENV} "; then
    echo -e "Error: Conda environment '${CONDA_ENV}' not found."
    echo "Available environments:"
    conda env list
    exit 1
fi

conda activate ${CONDA_ENV}
# Verify pyserini is available
if ! python -c "import pyserini.server.mcp" &> /dev/null; then
    echo -e "Error: pyserini.server.mcp module not found in environment '${CONDA_ENV}'"
    exit 1
fi


# Run the MCP server
python -m pyserini.server.mcp 

#!/bin/bash

# Create and start a screen session named "benchmarking"
screen -dmS benchmarking
screen -S benchmarking -X stuff "conda activate pyserini\n"

# Run the benchmark.py script in the background within the "benchmarking" session
screen -S benchmarking -X stuff "./benchmark_msmarco_duckdb.sh\n"

# Detach from the screen session and return to the main terminal
screen -d benchmarking

echo "Benchmarking script is running in the background in the 'benchmarking' screen session."
echo "You can reattach to the session later with the command: screen -r benchmarking"

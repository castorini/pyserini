#!/usr/bin/env bash
set -euo pipefail

tasks=(
  earth-science psychology biology economics pony robotics stackoverflow
  sustainable-living aops leetcode theoremqa-theorems theoremqa-questions
)

mkdir -p runs

for task in "${tasks[@]}"; do
  python -m pyserini.search.lucene \
    --index "bright-$task" \
    --topics "bright-$task" \
    --output "runs/run.bright.bm25.$task.txt" \
    --output-format trec \
    --hits 1000 --bm25 --remove-query

  python -m pyserini.search.lucene \
    --index "bright-$task" \
    --topics "bright-$task" \
    --output "runs/run.bright.bm25qs.$task.txt" \
    --output-format trec \
    --hits 1000 --bm25qs --remove-query
done

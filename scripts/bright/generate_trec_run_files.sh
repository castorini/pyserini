#!/usr/bin/env bash
set -euo pipefail

# Read the tasks array
readarray -d '' -t TASKS < <(python - <<'PY' "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"; pwd)/tasks.py"
import sys, importlib.util as u
s=u.spec_from_file_location("t", sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m)
for x in m.TASKS: print(x, end='\0')
PY
)

# Replace underscores with dashes:
for i in "${!TASKS[@]}"; do
  TASKS[$i]="${TASKS[$i]//_/-}"
done

mkdir -p runs

for task in ${TASKS[@]}; do
  python -m pyserini.search.lucene \
    --index bright-$task \
    --topics bright-$task \
    --output runs/run.bright.bm25.$task.txt \
    --output-format trec \
    --hits 1000 --bm25 --remove-query

  python -m pyserini.search.lucene \
    --index bright-$task \
    --topics bright-$task \
    --output runs/run.bright.bm25qs.$task.txt \
    --output-format trec \
    --hits 1000 --bm25qs --remove-query
done

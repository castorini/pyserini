#!/usr/bin/env bash

# Read the tasks array
readarray -d '' -t TASKS < <(python - <<'PY' "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"; pwd)/tasks.py"
import sys, importlib.util as u
s=u.spec_from_file_location("t", sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m)
for x in m.TASKS: print(x, end='\0')
PY
)

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
OUTPUT_DIR='./output_dir' # ---> change to where JSON outputs & plots will be saved
CACHE_DIR='./cache_dir'  # ---> change to your cache dir
MAKE_PLOTS=1  # set to 0 if you don't want pdf plots
# ------------------------------------------------------------

echo ">>> Processing tasks: ${TASKS[*]}"

if [[ $MAKE_PLOTS -eq 1 ]]; then
  python -m scripts.bright.dataset_analysis \
    --tasks ${TASKS[@]} \
    --cache-dir $CACHE_DIR \
    --output-dir $OUTPUT_DIR \
    --plots \
    --mode document
  python -m scripts.bright.dataset_analysis \
    --tasks ${TASKS[@]} \
    --cache-dir $CACHE_DIR \
    --output-dir $OUTPUT_DIR \
    --plots \
    --mode query
else
  python -m scripts.bright.dataset_analysis \
    --tasks ${TASKS[@]} \
    --cache-dir $CACHE_DIR \
    --output-dir $OUTPUT_DIR \
    --mode document
  python -m scripts.bright.dataset_analysis \
    --tasks ${TASKS[@]} \
    --cache-dir $CACHE_DIR \
    --output-dir $OUTPUT_DIR \
    --mode query
fi

echo "All tasks processed. Results in: $OUTPUT_DIR/"
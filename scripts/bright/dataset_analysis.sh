#!/usr/bin/env bash

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
TASKS=(
  'biology' 'earth_science' 'economics' 'pony'
  'psychology' 'robotics' 'stackoverflow' 'sustainable_living'
  'aops' 'leetcode' 'theoremqa_theorems' 'theoremqa_questions'
)
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
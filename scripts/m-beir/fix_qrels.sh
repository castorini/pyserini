#!/bin/bash

for file in collections/m-beir/*.txt; do
    if [[ -f "$file" ]]; then
        base_name="${file%.txt}"
        fixed_file="${base_name}_fixed.txt"
        
        echo "Processing: $file -> $fixed_file"
        cut -d' ' -f1-4 "$file" > "$fixed_file"
    fi
done

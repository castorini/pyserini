#!/usr/bin/env python3
"""
Convert MS MARCO queries to Pyserini topics format
"""

import sys
import os

def convert_queries_to_topics(queries_path, output_path):
    """Convert MS MARCO queries to Pyserini topics format"""
    
    with open(queries_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Parse TSV line: id \t query
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                query_id, query_text = parts
                # Write in Pyserini topics format: id \t query
                f_out.write(f"{query_id}\t{query_text}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_queries_to_topics.py <queries.tsv> <output.txt>")
        sys.exit(1)
    
    queries_path = sys.argv[1]
    output_path = sys.argv[2]
    
    convert_queries_to_topics(queries_path, output_path)
    print(f"Converted {queries_path} to {output_path}")

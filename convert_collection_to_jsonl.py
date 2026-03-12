#!/usr/bin/env python3
"""
Convert MS MARCO TSV collection to JSONL format
"""

import json
import sys
import os

def convert_collection_to_jsonl(collection_path, output_folder):
    """Convert MS MARCO TSV collection to JSONL files"""
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Read the TSV collection
    with open(collection_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Split into chunks of 1M lines (except last chunk)
    chunk_size = 1000000
    total_docs = len(lines)
    num_chunks = (total_docs + chunk_size - 1) // chunk_size
    
    print(f"Converting {total_docs} documents to JSONL format...")
    print(f"Creating {num_chunks} chunks of up to {chunk_size} documents each")
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min((chunk_idx + 1) * chunk_size, total_docs)
        
        output_file = os.path.join(output_folder, f'collection{chunk_idx}.jsonl')
        
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in lines[start_idx:end_idx]:
                # Parse TSV line: id \t content
                parts = line.strip().split('\t', 1)
                if len(parts) == 2:
                    doc_id, content = parts
                    
                    # Create JSON object
                    json_obj = {
                        "id": doc_id,
                        "contents": content
                    }
                    
                    # Write to JSONL file
                    out_f.write(json.dumps(json_obj) + '\n')
        
        print(f"Chunk {chunk_idx + 1}/{num_chunks}: {end_idx - start_idx} documents -> {output_file}")
    
    print(f"Conversion complete! {total_docs} documents converted to {num_chunks} JSONL files.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_collection_to_jsonl.py --collection-path <path> --output-folder <folder>")
        sys.exit(1)
    
    collection_path = sys.argv[1]
    output_folder = sys.argv[2]
    
    convert_collection_to_jsonl(collection_path, output_folder)

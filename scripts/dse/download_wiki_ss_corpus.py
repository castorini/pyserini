#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Download the Wiki-SS (Wikipedia Screenshot) corpus from HuggingFace.

This script downloads the Wiki-SS corpus used for DSE experiments and creates
a corpus.jsonl file for indexing with Pyserini. The script preserves original
image bytes to maintain exact file sizes and compression.

Usage:
    python scripts/dse/download_wiki_ss_corpus.py [--output-dir OUTPUT_DIR]
"""

import argparse
import json
import os

from datasets import load_dataset, Image
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description='Download Wiki-SS corpus for DSE experiments.')
    parser.add_argument('--output-dir', type=str, default='collections/wiki-ss',
                        help='Output directory for the corpus (default: collections/wiki-ss)')
    args = parser.parse_args()

    output_dir = args.output_dir
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    print(f"Downloading Wiki-SS corpus to {output_dir}...")
    print("This may take a while as the corpus contains ~1.2M screenshots.")

    # Load dataset with decode=False to preserve original image bytes
    # This maintains exact file sizes and compression from the dataset
    ds = load_dataset('Tevatron/wiki-ss-corpus', split='train')
    ds = ds.cast_column('image', Image(decode=False))
    
    print("Preserving original image bytes - files will match dataset exactly.")
    print(f'Total documents: {len(ds)}')

    corpus_path = os.path.join(output_dir, 'corpus.jsonl')
    
    # Check for existing progress to support resume
    existing_ids = set()
    if os.path.exists(corpus_path):
        with open(corpus_path, 'r') as f:
            for line in f:
                try:
                    existing_ids.add(json.loads(line)['id'])
                except:
                    pass
        print(f"Found {len(existing_ids)} already processed documents, resuming...")
    
    mode = 'a' if existing_ids else 'w'
    with open(corpus_path, mode) as corpus_file:
        for item in tqdm(ds, desc="Processing documents"):
            docid = item['docid']
            if docid in existing_ids:
                continue
            
            img_path = os.path.join(images_dir, f"{docid}.jpg")
            
            # Write original bytes directly to preserve exact compression
            image_data = item['image']
            if not isinstance(image_data, dict) or image_data.get('bytes') is None:
                raise ValueError(f"Expected image bytes for docid {docid}, got {type(image_data)}")
            
            with open(img_path, 'wb') as img_file:
                img_file.write(image_data['bytes'])
            
            entry = {'id': docid, 'contents': img_path}
            corpus_file.write(json.dumps(entry) + '\n')

    print(f"Download complete!")
    print(f"   Images saved to: {images_dir}")
    print(f"   Corpus file: {corpus_path}")


if __name__ == '__main__':
    main()

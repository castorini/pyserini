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
Download Wiki-SS-NQ test queries in TSV format for Wiki-SS experiments.

This script downloads the wiki-ss-nq test set and extracts queries in TSV format
for use with Pyserini's dense retrieval and evaluation.

Usage:
    python scripts/dse/download_wiki_ss_nq_queries.py [--output-dir OUTPUT_DIR]
"""

import argparse
import os

from datasets import load_dataset
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description='Download Wiki-SS-NQ test queries for Wiki-SS experiments.')
    parser.add_argument('--output-dir', type=str, default='collections/wiki-ss',
                        help='Output directory for the queries (default: collections/wiki-ss)')
    args = parser.parse_args()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    print(f"Downloading Wiki-SS-NQ queries...")
    
    # Load wiki-ss-nq dataset
    nq = load_dataset("Tevatron/wiki-ss-nq", split='test')

    # Extract queries to TSV file
    queries_path = os.path.join(output_dir, 'wiki-ss-nq-test-queries.tsv')
    
    with open(queries_path, 'w') as queries_file:
        for example in tqdm(nq, desc="Processing queries", unit="queries"):
            query_id = str(example['query_id'])
            query_text = example['query']
            
            # Write query in TSV format: query_id \t query_text
            queries_file.write(f"{query_id}\t{query_text}\n")

    print(f"✅ Download complete!")
    print(f"   Queries saved to: {queries_path}")
    print(f"   Total queries: {len(nq)}")


if __name__ == '__main__':
    main()

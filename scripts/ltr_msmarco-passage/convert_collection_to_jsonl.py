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

import json
import os
import argparse

"""
convert collection to jsonl
"""
def convert_collection(args):
    print('Converting collection...')
    file_index = 0
    with open(args.collection_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            doc_json = line.rstrip()

            if i % args.max_docs_per_file == 0:
                if i > 0:
                    output_jsonl_file.close()
                output_path = os.path.join(args.output_folder, 'docs{:02d}.json'.format(file_index))
                output_jsonl_file = open(output_path, 'w', encoding='utf-8', newline='\n')
                file_index += 1
            output_jsonl_file.write(doc_json + '\n')

            if i % 100000 == 0:
                print(f'Converted {i:,} docs, writing into file {file_index}')

    output_jsonl_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MSMARCO tsv collection into jsonl files for Anserini.')
    parser.add_argument('--collection-path', required=True, help='Path to MS MARCO tsv collection.')
    parser.add_argument('--output-folder', required=True, help='Output folder.')
    parser.add_argument('--max-docs-per-file', default=1000000, type=int,
                        help='Maximum number of documents in each jsonl file.')

    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    convert_collection(args)
    print('Done!')
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
import argparse
import pickle
import csv
from tqdm import tqdm
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert KILT 100 words passage tsv into a 100-words Passage-level JSONL that can be processed by Pyserini')
    parser.add_argument('--input', required=True, help='Path to the kilt_w100_title.tsv file')
    parser.add_argument('--mapping', required=True, help='Path to the mapping_KILT_title.p file')
    parser.add_argument('--output-dir', required=True, help='Path to the output directory')
    parser.add_argument('--concat-title', action="store_true", default=False, help='Concatenate the title into each paragraph')

    args = parser.parse_args()

    # Map of title -> wikipedia id
    KILT_mapping = pickle.load(open(args.mapping, "rb"))

    not_found = set()
    with open(args.input, 'r') as f, open(os.path.join(args.output_dir, '100w_passage_kilt_knowledgesource.jsonl'), 'w') as outp:
        tsv = csv.reader(f, delimiter="\t")
        next(tsv)  # Get rid of headers
        for row in tqdm(tsv, mininterval=10.0, maxinterval=20.0):
            i = row[0]
            text = row[1]
            title = row[2]

            if title not in KILT_mapping:
                not_found.add(f"{title}#{i}")
                continue

            wikipedia_id = str(KILT_mapping[title])

            doc = {}

            doc["id"] = f"{wikipedia_id}#{i}"
            doc["wikipedia_title"] = title
            doc["wikipedia_id"] = wikipedia_id
            doc["contents"] = f"{title}\n{text}" if args.concat_title else text

            _ = outp.write(json.dumps(doc))
            _ = outp.write('\n')
    print(f"Not found: {not_found}")


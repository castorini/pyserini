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

import argparse
import json
import os

from datasets import load_dataset
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, default='adjusted_qrels')
    parser.add_argument('--cache-dir', type=str, default='cache')
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    for task in [
        'biology',
        'earth_science',
        'economics',
        'psychology',
        'robotics',
        'stackoverflow',
        'sustainable_living',
        'leetcode',
        'pony',
        'aops',
        'theoremqa_theorems',
        'theoremqa_questions',
    ]:
        examples = load_dataset('xlangai/bright', 'examples', cache_dir=args.cache_dir)[
            task
        ]
        doc_pairs = load_dataset(
            'xlangai/bright', 'documents', cache_dir=args.cache_dir
        )[task]
        unique_documents = {}
        for dp in doc_pairs:
            content = dp['content'].strip()
            if content not in unique_documents:
                unique_documents[content] = []
            unique_documents[content].append(dp['id'])
        doc_id_mappings = {}
        for _, doc_groups in unique_documents.items():
            for id in doc_groups:
                doc_id_mappings[id] = doc_groups
        ground_truth = {}
        missing_gold_ids = []
        for e in tqdm(examples):
            qid = e['id']
            ground_truth[qid] = {}
            for gid in e['gold_ids']:
                for did in doc_id_mappings[gid]:
                    ground_truth[qid][did] = 1
                    if did not in e['gold_ids']:
                        missing_gold_ids.append({'qid': qid, 'did': did})
            for did in e['excluded_ids']:
                assert not did in ground_truth[qid]
        task_name = task.replace('_', '-')
        with open(
            os.path.join(args.output_dir, f'qrels.bright-{task_name}.txt'), 'w'
        ) as f:
            for qid, docs in ground_truth.items():
                for did in docs:
                    f.write(f'{qid}\t0\t{did}\t1\n')
        with open(
            os.path.join(args.output_dir, f'{task_name}-missing_gold_dids.json'), 'w'
        ) as f:
            json.dump(missing_gold_ids, f)


if __name__ == '__main__':
    main()

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
import os
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interpolate runs')
    parser.add_argument('--run1', required=True, help='retrieval run1')
    parser.add_argument('--run2', required=True, help='retrieval run2')
    parser.add_argument('--start-weight', type=float, required=True, help='start hybrid alpha')
    parser.add_argument('--end-weight', type=float, required=True, help='end hybrid alpha')
    parser.add_argument('--step', type=float, required=True, help='changes of alpha per step')
    parser.add_argument('--output-dir', required=True, help='hybrid result')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    run1_result = {}
    with open(args.run1) as f:
        for line in f:
            qid, _, docid, rank, score, _ = line.rstrip().split()
            score = float(score)
            if qid in run1_result:
                run1_result[qid][docid] = score
            else:
                run1_result[qid] = {docid: score}
    run2_result = {}
    with open(args.run2) as f:
        for line in f:
            qid, _, docid, rank, score, _ = line.rstrip().split()
            score = float(score)
            if qid in run2_result:
                run2_result[qid][docid] = score
            else:
                run2_result[qid] = {docid: score}

    hybrid_result = {}

    for alpha in np.arange(args.start_weight, args.end_weight, args.step):
        output_f = open(args.output_dir, 'w')
        for key in tqdm(list(run1_result.keys())):
            run1_hits = {docid: float(run1_result[key][docid]) for docid in run1_result[key]}
            run2_hits = {docid: float(run2_result[key][docid]) for docid in run2_result[key]}
            hybrid_scores = []
            min_run1_score = min(run1_hits.values())
            min_run2_score = min(run2_hits.values())
            for doc in set(run1_hits.keys()) | set(run2_hits.keys()):
                if doc not in run1_hits:
                    score = alpha * run2_hits[doc] + min_run1_score
                elif doc not in run2_hits:
                    score = alpha * min_run2_score + run1_hits[doc]
                else:
                    score = alpha * run2_hits[doc] + run1_hits[doc]
                hybrid_scores.append((doc, score))
            hybrid_scores = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)
            for idx, item in enumerate(hybrid_scores):
                output_f.write(f'{key} Q0 {item[0]} {idx+1} {item[1]} hybrid\n')
        output_f.close()

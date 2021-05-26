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

    for alpha in np.arange(args.start_weight, args.end_weight, args.step):
        run1_result = json.load(open(args.run1))
        run2_result = json.load(open(args.run2))
        hybrid_result = {}
        for key in tqdm(list(run1_result.keys())):
            question = run1_result[key]['question']
            answers = run1_result[key]['answers']
            run2_contexts = run2_result[key]['contexts']
            run1_contexts = run1_result[key]['contexts']
            run1_hits = {hit['docid']: float(hit['score']) for hit in run1_contexts}
            run2_hits = {hit['docid']: float(hit['score']) for hit in run2_contexts}
            hybrid_scores = {}
            run1_scores = {}
            run2_scores = {}
            min_run1_score = min(run1_hits.values())
            min_run2_score = min(run2_hits.values())
            for doc in set(run1_hits.keys()) | set(run2_hits.keys()):
                if doc not in run1_hits:
                    score = alpha * run2_hits[doc] + min_run1_score
                    run2_scores[doc] = run2_hits[doc]
                    run1_scores[doc] = -1
                elif doc not in run2_hits:
                    score = alpha * min_run2_score + run1_hits[doc]
                    run2_scores[doc] = -1
                    run1_scores[doc] = run1_hits[doc]
                else:
                    score = alpha * run2_hits[doc] + run1_hits[doc]
                    run2_scores[doc] = run2_hits[doc]
                    run1_scores[doc] = run1_hits[doc]
                hybrid_scores[doc] = score
            total_ids = []
            total_context = []
            for sctx, dctx in zip(run2_contexts, run1_contexts):
                if sctx['docid'] not in total_ids:
                    total_ids.append(sctx['docid'])
                    sctx['score'] = hybrid_scores[sctx['docid']]
                    sctx['run2_score'] = run2_scores[sctx['docid']]
                    sctx['run1_score'] = run1_scores[sctx['docid']]
                    total_context.append(sctx)
                if dctx['docid'] not in total_ids:
                    total_ids.append(dctx['docid'])
                    dctx['score'] = hybrid_scores[dctx['docid']]
                    dctx['run2_score'] = run2_scores[dctx['docid']]
                    dctx['run1_score'] = run1_scores[dctx['docid']]
                    total_context.append(dctx)
            total_context = sorted(total_context, key=lambda x: x['score'], reverse=True)
            hybrid_result[key] = {'question': question, 'answers': answers, 'contexts': total_context}
        json.dump(hybrid_result, open(os.path.join(args.output_dir, f'run_fused_weight_{alpha}.json'), 'w'), indent=4)

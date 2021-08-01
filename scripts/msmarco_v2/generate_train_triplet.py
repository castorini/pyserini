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
# This file generate the training triple .tsv in `qid\tpos-docid\tneg-docid` format per line
# for both MS MARCO Document and Passage collections
#
# Usage:
# python scripts/msmarco_v2/generate_train_triplet.py \
#   -r v2_train_top100.txt \
#   -q v2_train_qrels.tsv \
#   -nneg 40 \
#   -o train-triple-ids.nneg-40.tsv
#   -topk 1000

import os
import random
import argparse
from collections import defaultdict
from tqdm import tqdm

def load_qrels(fn):
    """
    Loading trec format query relevance file into a dictionary
    :param fn: qrel file path
    :return: dict, in format {qid: {docid: label, ...}, ...}
    """
    qrels = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, docid, label = line.strip().split()
            qrels[qid][docid] = int(label)
    return qrels


def load_run(fn, topk):
    """
    Loading trec format runfile into a dictionary
    :param fn: runfile path
    :param topk: top results to include
    :return: dict, in format {qid: [docid, ...], ...}
    """
    run = defaultdict(list)
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, docid, _, score, _ = line.strip().split()
            run[qid].append((docid, float(score)))

    sorted_run = defaultdict(list)
    for query_id, docid_scores in tqdm(run.items()):
        docid_scores.sort(key=lambda x: x[1], reverse=True)
        doc_ids = [doc_id for doc_id, _ in docid_scores][:topk]
        sorted_run[query_id] = doc_ids

    return sorted_run


def open_as_write(fn):
    parent = os.path.dirname(fn)
    if parent != "":
        os.makedirs(parent, exist_ok=True)
    return open(fn, "w")


def main(args):
    assert args.output.endswith(".tsv")
    n_neg = args.n_neg_per_query
    require_pos_in_topk = args.require_pos_in_topk
    run = load_run(args.run_file, args.topk)
    qrels = load_qrels(args.qrel_file)
    n_not_in_topk, n_total = 0, len(qrels)

    with open_as_write(args.output) as fout:
        for n_processed, qid in tqdm(enumerate(qrels)):
            if qid not in run:
                continue

            top_k = run[qid]
            if require_pos_in_topk:
                pos_docids = [docid for docid in top_k if qrels[qid].get(docid, 0) > 0]
            else:
                pos_docids = [docid for docid in qrels[qid] if qrels[qid][docid] > 0]

            neg_docids = [docid for docid in top_k if qrels[qid].get(docid, 0) == 0]

            if len(pos_docids) == 0:
                n_not_in_topk += 1

            for pos_docid in pos_docids:
                sampled_neg_docids = random.choices(neg_docids, k=n_neg)
                lines = [f"{qid}\t{pos_docid}\t{neg_docid}\n" for neg_docid in sampled_neg_docids]
                fout.writelines(lines)

    print(f"Finished. {n_not_in_topk} out of {n_total} queries have no positive document in the runfile.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate MS MARCO V2 training triple .tsv')
    parser.add_argument('--run-file', '-r', required=True, help='MS MARCO V2 doc or passage train_top100.txt path.')
    parser.add_argument('--qrel-file', '-q', required=True, help='MS MARCO V2 doc or passsage train_qrels.tsv path.')
    parser.add_argument('--output', '-o', required=True, help='output training triple .tsv path')
    parser.add_argument('--n-neg-per-query', '-nneg', default=40, type=int, help='number of negative documents sampled for each query')
    parser.add_argument('--topk' , default=1000, type=int, help='top-k documents in the run file from which we sample negatives')
    parser.add_argument('--require-pos-in-topk', action='store_true', default=False, help='if specified, then only keep the positive documents if they appear in the given runfile')
    args = parser.parse_args()

    random.seed(123_456)
    main(args)

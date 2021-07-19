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
# 	-r v2_train_top100.txt \
# 	-q v2_train_qrels.tsv \
# 	-nneg 40 \
# 	-o train-triple-ids.nneg-40.tsv

import os
import random
import argparse
from collections import defaultdict


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


def load_runs(fn):
    """
    Loading trec format runfile into a dictionary
    :param fn: runfile path
    :return: dict, in format {qid: {docid: score, ...}, ...}
    """
    runs = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, docid, _, score, _ = line.strip().split()
            runs[qid][docid] = float(score)
    return runs


def open_as_write(fn):
	parent = os.path.dirname(fn)
	if parent != "":
		os.makedirs(parent, exist_ok=True)
	return open(fn, "w")


def main(args):
	assert args.output.endswith(".tsv")
	n_neg = args.n_neg_per_query
	runs = load_runs(args.run_file)
	qrels = load_qrels(args.qrel_file)
	n_not_in_topk, n_total = 0, len(qrels)

	with open_as_write(args.output) as fout:
		for n_processed, qid in enumerate(qrels):
			if n_processed > 0 and n_processed % 10_000:
				print(f"[{n_processed:6}/{n_total}] queries processed.")

			if qid not in runs:
				continue

			top_k = runs[qid]
			pos_docids = [docid for docid in top_k if qrels[qid].get(docid, 0) > 0]
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
	parser.add_argument('--n-neg-per-query', default=40, help='number of negative documents sampled for each query')
	args = parser.parse_args()

	random.seed(123_456)
	main(args)

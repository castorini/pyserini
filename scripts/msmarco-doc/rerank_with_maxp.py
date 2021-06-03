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

"""Script that takes a base run for MS MARCO doc and reranks it using MaxP BM25.
For each topic, each document in the base run is segmented into passages; a new index is built over these passages,
and then MaxP retrieval is performed using this index. These MaxP results are then fused with the original base run."""

import argparse
import csv
import json
import os
import shutil
import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

from pyserini.trectools import TrecRun
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def load_queries(query_file: str):
    queries = []
    with open(query_file, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            queries.append([row[0], row[1]])
    return queries


def generate_passage_collection(docs, collection_path):
    with open(collection_path, 'w') as writer:
        for doc in docs:
            docid = doc['docid']
            doc_tokens = doc['text'].split()

            for i in range(0, len(doc_tokens), 100):
                passage = ' '.join(doc_tokens[i: i + 150])
                json_doc = {"id": docid, "contents": passage}
                writer.write(json.dumps(json_doc) + '\n')


def bm25(qid, query, docs, index_path):
    s = SimpleSearcher(index_path)
    hits = s.search(query, 1000)

    n = 1
    seen_docids = {}
    with open(f'run-passage-{qid}.txt', 'w') as writer:
        for i in range(0, len(hits)):
            if hits[i].docid in seen_docids:
                continue
            writer.write(f'{qid} Q0 {hits[i].docid} {n} {hits[i].score:.5f} pyserini\n')
            n = n + 1
            seen_docids[hits[i].docid] = 1

    with open(f'run-doc-{qid}.txt', 'w') as writer:
        for doc in docs:
            writer.write(f'{qid} Q0 {doc["docid"]} {doc["rank"]} {doc["score"]} base\n')
            n = n + 1

    os.system(f'python -m pyserini.fusion --method rrf --runs run-passage-{qid}.txt run-doc-{qid}.txt ' +
              f'--output run-rrf-{qid}.txt --runtag test')
    fused_run = TrecRun(f'run-rrf-{qid}.txt')

    output = []
    for idx, r in fused_run.get_docs_by_topic(qid).iterrows():
        output.append([qid, r["docid"], r["rank"]])

    return output


def ance(qid, query, docs, index_path):
    searcher = SimpleDenseSearcher(index_path,  'castorini/ance-msmarco-doc-maxp')
    hits = searcher.search(query, 1000)

    output = []
    n = 1
    seen_docids = {}
    for i in range(0, len(hits)):
        if hits[i].docid in seen_docids:
            continue
        output.append([qid, hits[i].docid, n])
        n = n + 1
        seen_docids[hits[i].docid] = 1

    return output


def rerank(cache, qid, query, docs, reranker):
    # Check if we're using a cache:
    if cache:
        root = cache
    else:
        root = '.'

    collection_dir = os.path.join(root, f'docs-{qid}')
    collection_path = os.path.join(root, f'docs-{qid}/docs.json')
    index_path = ''
    if reranker == 'bm25':
        index_path = os.path.join(root, f'qid-index-{qid}')
    elif reranker == 'ance':
        index_path = os.path.join(root, f'qid-dindex-{qid}')

    if not os.path.exists(index_path):
        # Create a passage collection from docs:
        if not os.path.exists(collection_dir):
            os.mkdir(collection_dir)
        generate_passage_collection(docs, collection_path)

        # Build index over this passage collection:
        if reranker == 'bm25':
            os.system(f'python -m pyserini.index -collection JsonCollection ' +
                      f'-generator DefaultLuceneDocumentGenerator -threads 1 ' +
                      f'-input {collection_dir} -index {index_path}')
        elif reranker == 'ance':
            os.system(f'python -m pyserini.dindex --corpus {collection_dir} ' +
                      f'--encoder castorini/ance-msmarco-doc-maxp --index {index_path} --batch 64 --device cpu')

    output = []
    # Choose which reranker to use:
    if reranker == 'bm25':
        output = bm25(qid, query, docs, index_path)
    elif reranker == 'ance':
        output = ance(qid, query, docs, index_path)

    # If we're using a cache, don't clean up:
    if not args.cache:
        shutil.rmtree(collection_dir)
        shutil.rmtree(index_path)

    # Clean up run files.
    if reranker == 'bm25':
        os.remove(f'run-passage-{qid}.txt')
        os.remove(f'run-doc-{qid}.txt')
        os.remove(f'run-rrf-{qid}.txt')

    return output


def main(args):
    if args.cache and not os.path.exists(args.cache):
        os.mkdir(args.cache)

    # Load queries:
    queries = load_queries(args.queries)
    # Load base run to rerank:
    base_run = TrecRun(args.input)

    # SimpleSearcher to fetch document texts.
    searcher = SimpleSearcher.from_prebuilt_index('msmarco-doc')

    output = []

    if args.bm25:
        reranker = 'bm25'
    elif args.ance:
        reranker = 'ance'
    elif not args.identity:
        sys.exit('Unknown reranking method!')

    cnt = 1
    for row in queries:
        qid = int(row[0])
        query = row[1]
        print(f'{cnt} {qid} {query}')
        qid_results = base_run.get_docs_by_topic(qid)

        # Don't actually do reranking, just pass along the base run:
        if args.identity:
            rank = 1
            for docid in qid_results['docid'].tolist():
                output.append([qid, docid, rank])
                rank = rank + 1
            cnt = cnt + 1
            continue

        # Gather results for reranking:
        results_to_rerank = []
        for index, result in qid_results.iterrows():
            raw_doc = searcher.doc(result['docid']).raw().lstrip('<TEXT>').rstrip('</TEXT>')
            results_to_rerank.append({'docid': result['docid'],
                                      'rank': result['rank'],
                                      'score': result['score'],
                                      'text': raw_doc})

        # Perform the actual reranking:
        output.extend(rerank(args.cache, qid, query, results_to_rerank, reranker))
        cnt = cnt + 1

    # Write the output run file:
    with open(args.output, 'w') as writer:
        for r in output:
            writer.write(f'{r[0]}\t{r[1]}\t{r[2]}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--queries', type=str, help='Queries.', required=True)
    parser.add_argument('--input', type=str, help='Base run.', required=True)
    parser.add_argument('--output', type=str, help='Output.', required=True)
    parser.add_argument('--cache', type=str, help='Cache directory.', required=False)
    parser.add_argument('--identity', action='store_true', help="Identity reranker.")
    parser.add_argument('--bm25', action='store_true', help="BM25 reranker.")
    parser.add_argument('--ance', action='store_true', help="ANCE reranker.")

    args = parser.parse_args()
    main(args)

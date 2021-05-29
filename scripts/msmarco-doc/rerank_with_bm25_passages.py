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


def load_queries(query_file: str):
    queries = []
    with open(query_file, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            queries.append([row[0], row[1]])
    return queries


def generate_passage_collection(searcher, docids, collection_path):
    with open(collection_path, 'w') as writer:
        for doc in docids:
            raw_doc = searcher.doc(doc).raw()
            raw_doc = raw_doc.lstrip('<TEXT>')
            raw_doc = raw_doc.rstrip('</TEXT>')
            doc_tokens = raw_doc.split()

            for i in range(0, len(doc_tokens), 100):
                passage = ' '.join(doc_tokens[i: i + 150])
                json_doc = {"id": doc, "contents": passage}
                writer.write(json.dumps(json_doc) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--queries', type=str, help='Queries.', required=True)
    parser.add_argument('--input', type=str, help='Base run.', required=True)
    parser.add_argument('--output', type=str, help='Output.', required=True)

    args = parser.parse_args()

    # Load queries:
    queries = load_queries(args.queries)
    # Load base run to rerank:
    base_run = TrecRun(args.input)

    # SimpleSearcher to fetch document texts.
    searcher = SimpleSearcher.from_prebuilt_index('msmarco-doc')

    output = []

    cnt = 1
    for row in queries:
        qid = int(row[0])
        query = row[1]
        print(f'{cnt} {qid} {query}')
        docids = base_run.get_docs_by_topic(qid)['docid'].tolist()

        # Create a passage collection from docs:
        collection_dir = f'docs-{qid}'
        collection_path = f'docs-{qid}/docs.json'
        if not os.path.exists(collection_dir):
            os.mkdir(collection_dir)
        generate_passage_collection(searcher, docids, collection_path)

        # Build index over this passage collection:
        index_path = f'qid-index-{qid}'
        os.system(f'python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator ' +
                  f'-threads 1 -input {collection_dir} -index {index_path}')

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

        base = base_run.get_docs_by_topic(qid)
        n = 1
        with open(f'run-doc-{qid}.txt', 'w') as writer:
            for idx, r in base.iterrows():
                writer.write(f'{qid} Q0 {r[2]} {n} {r[4]:.5f} base\n')
                n = n + 1

        os.system(f'python -m pyserini.fusion --method rrf --runs run-passage-{qid}.txt run-doc-{qid}.txt ' +
                  f'--output run-rrf-{qid}.txt --runtag test')
        fused_run = TrecRun(f'run-rrf-{qid}.txt')

        for idx, r in fused_run.get_docs_by_topic(qid).iterrows():
            output.append(f'{qid}\t{r["docid"]}\t{r["rank"]}')

        shutil.rmtree(collection_dir)
        shutil.rmtree(index_path)

        # Clean up run files.
        os.remove(f'run-passage-{qid}.txt')
        os.remove(f'run-doc-{qid}.txt')
        os.remove(f'run-rrf-{qid}.txt')
        cnt = cnt + 1

    with open(args.output, 'w') as writer:
        for r in output:
            writer.write(f'{r}\n')

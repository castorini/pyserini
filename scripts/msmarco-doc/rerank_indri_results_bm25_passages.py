import csv
import json
import os
import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

from pyserini.trectools import TrecRun
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher.from_prebuilt_index('msmarco-doc')

queries = []
with open('scripts/msmarco-doc/msmarco-docdev-queries.tsv', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        queries.append([row[0], row[1]])

indri_run = TrecRun('scripts/msmarco-doc/msmarco-docdev-top100')

#print(indri_run.topics())
#print(len(indri_run))

#print(indri_run.get_docs_by_topic(174249))

output = []

for row in queries: #[:100]:
    qid = int(row[0])
    query = row[1]
    print(f'{qid} {query}')
    docs = indri_run.get_docs_by_topic(qid)['docid'].tolist()
    dir = f'collections2/docs-{qid}'
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(f'{dir}/docs.json', 'w') as writer:
        for doc in docs:
            #print(searcher.doc(doc).raw())
            raw_doc = searcher.doc(doc).raw()
            raw_doc = raw_doc.lstrip('<TEXT>')
            raw_doc = raw_doc.rstrip('</TEXT>')
            #print(f"#########{repr(raw_doc)}")

            doc_tokens = raw_doc.split()
            #print(doc_tokens)

            for i in range(0, len(doc_tokens), 100):
                passage = ' '.join(doc_tokens[i: i + 150])
                json_doc = {"id": doc, "contents": passage}
                writer.write(json.dumps(json_doc) + '\n')

    os.system(f'python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator ' +
              f'-threads 1 -input collections2/docs-{qid} -index indexes2/qid-index-{qid}')

    s = SimpleSearcher(f'indexes2/qid-index-{qid}')
    s.set_bm25(2.0, 0.6)
    hits = s.search(query, 1000)

    n = 1
    seen_docids = {}
    for i in range(0, len(hits)):
        if hits[i].docid in seen_docids:
            continue
        output.append(f'{qid}\t{hits[i].docid}\t{n}')
        print(f'{n:2} {hits[i].docid:7} {hits[i].score:.5f}')
        n = n + 1
        seen_docids[hits[i].docid] = 1
        if n > 10:
            break

with open(f'reranked_run.txt', 'w') as writer:
    for r in output:
        writer.write(f'{r}\n')

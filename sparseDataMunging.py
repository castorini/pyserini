import json
from pyserini.search.lucene import LuceneSearcher

with open('collections/nfcorpus/pyserini-corpus/corpus.jsonl', 'w') as out:
    with open('collections/nfcorpus/corpus.jsonl', 'r') as f:
        for line in f:
            l = json.loads(line)
            s = json.dumps({'id': l['_id'], 'contents': l['title'] + ' ' + l['text']})
            out.write(s + '\n')

searcher = LuceneSearcher('indexes/lucene.nfcorpus')
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.4f}')
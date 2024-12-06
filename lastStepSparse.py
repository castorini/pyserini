from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader
from pyserini.analysis import Analyzer, get_lucene_analyzer


from tqdm import tqdm

import json

searcher = LuceneSearcher('indexes/lucene.nfcorpus')
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.4f}')

#Doing retrieval by hand

index_reader = LuceneIndexReader('indexes/lucene.nfcorpus')
tf = index_reader.get_document_vector('MED-4555')
bm25_weights = \
    {term: index_reader.compute_bm25_term_weight('MED-4555', term, analyzer=None) \
     for term in tf.keys()}

print(json.dumps(bm25_weights, indent=4, sort_keys=True))

#Encoding query
analyzer = Analyzer(get_lucene_analyzer())
query_tokens = analyzer.analyze('How to Help Prevent Abdominal Aortic Aneurysms')
multihot_query_weights = {k: 1 for k in query_tokens}

def dot(q_weights, d_weights):
    return sum({term: d_weights[term] \
                for term in d_weights.keys() & \
                q_weights.keys()}.values())

print(dot(multihot_query_weights, bm25_weights))


searcher = LuceneSearcher('indexes/lucene.nfcorpus')
index_reader = LuceneIndexReader('indexes/lucene.nfcorpus')

scores = []
# Iterate through all docids in the index.
for i in tqdm(range(0, searcher.num_docs)):
    docid = searcher.doc(i).get('id')
    # Reconstruct the BM25 document vector.
    tf = index_reader.get_document_vector(docid)
    bm25_weights = \
        {term: index_reader.compute_bm25_term_weight(docid, term, analyzer=None) \
         for term in tf.keys()}
    # Compute and retain the query-document score.
    score = dot(multihot_query_weights, bm25_weights)
    scores.append([docid, score])

# Sort by score descending.
scores.sort(key=lambda x: -x[1])

for s in scores[:10]:
    print(f'{s[0]} {s[1]:.4f}')
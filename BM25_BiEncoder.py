from pyserini.index.lucene import IndexReader
import json

# materialize (i.e., reconstruct) the BM25 document vector for a particular document
index_reader = IndexReader('indexes/lucene-index-msmarco-passage')
tf = index_reader.get_document_vector('7187158')
bm25_weights = \
    {term: index_reader.compute_bm25_term_weight('7187158', term, analyzer=None) \
     for term in tf.keys()}

print(json.dumps(bm25_weights, indent=4, sort_keys=True))
print("="*50)

#  generates the query representation:
from pyserini.analysis import Analyzer, get_lucene_analyzer

analyzer = Analyzer(get_lucene_analyzer())
query_tokens = analyzer.analyze('what is paula deen\'s brother')
multihot_query_weights = {k: 1 for k in query_tokens}
print(query_tokens)
print("="*50)

# compute the inner product between the query vector and the document vector
import numpy as np

# Gather up the dimensions (i.e., the combined dictionary).
terms = set.union(set(bm25_weights.keys()), set(multihot_query_weights.keys()))

bm25_vec = np.array([ bm25_weights.get(t, 0) for t in terms ])
multihot_qvec = np.array([ multihot_query_weights.get(t, 0) for t in terms ])

print(np.dot(multihot_qvec, bm25_vec))
print("="*50)

# OR

print(sum({term: bm25_weights[term] \
     for term in bm25_weights.keys() & \
     multihot_query_weights.keys()}.values()))
print("="*50)

# searching with the same query using Lucene:

from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/lucene-index-msmarco-passage')
hits = searcher.search('what is paula deen\'s brother')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
print("="*50)

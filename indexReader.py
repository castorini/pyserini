from pyserini.index.lucene import LuceneIndexReader
import json

index_reader = LuceneIndexReader('indexes/lucene-index-msmarco-passage')
tf = index_reader.get_document_vector('7187158')
bm25_weights = \
    {term: index_reader.compute_bm25_term_weight('7187158', term, analyzer=None) \
     for term in tf.keys()}

print(json.dumps(bm25_weights, indent=4, sort_keys=True))
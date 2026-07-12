"""
Pyserini Conceptual Framework Demo
BM25 as a Bi-Encoder

Flow:
1. Read BM25 document vector
2. Build query vector
3. Compute dot product manually
4. Verify using Lucene search
5. Retrieve original document
"""

import json
import numpy as np

from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.index.lucene import LuceneIndexReader
from pyserini.search.lucene import LuceneSearcher


print("=" * 80)
print("STEP 1: BM25 DOCUMENT VECTOR")
print("=" * 80)

index_reader = LuceneIndexReader(
    "indexes/lucene-index-msmarco-passage"
)

docid = "7187158"

tf = index_reader.get_document_vector(docid)

bm25_weights = {
    term: index_reader.compute_bm25_term_weight(
        docid,
        term,
        analyzer=None,
    )
    for term in tf.keys()
}

print(json.dumps(bm25_weights, indent=4, sort_keys=True))


print("\n")
print("=" * 80)
print("STEP 2: QUERY VECTOR")
print("=" * 80)

query = "what is paula deen's brother"

analyzer = Analyzer(get_lucene_analyzer())

query_tokens = analyzer.analyze(query)

print("Query Tokens:")
print(query_tokens)

multihot_query_weights = {
    token: 1
    for token in query_tokens
}

print("\nMulti-hot Query Vector:")
print(multihot_query_weights)


print("\n")
print("=" * 80)
print("STEP 3: MANUAL DOT PRODUCT")
print("=" * 80)

terms = set.union(
    set(bm25_weights.keys()),
    set(multihot_query_weights.keys()),
)

bm25_vec = np.array(
    [
        bm25_weights.get(term, 0)
        for term in terms
    ]
)

query_vec = np.array(
    [
        multihot_query_weights.get(term, 0)
        for term in terms
    ]
)

score = np.dot(query_vec, bm25_vec)

print(f"Manual Dot Product Score: {score:.6f}")


print("\n")
print("=" * 80)
print("STEP 4: SHORTCUT DOT PRODUCT")
print("=" * 80)

shortcut_score = sum(
    {
        term: bm25_weights[term]
        for term in (
            bm25_weights.keys()
            &
            multihot_query_weights.keys()
        )
    }.values()
)

print(f"Shortcut Score: {shortcut_score:.6f}")


print("\n")
print("=" * 80)
print("STEP 5: LUCENE SEARCH")
print("=" * 80)

searcher = LuceneSearcher(
    "indexes/lucene-index-msmarco-passage"
)

searcher.set_bm25(0.82, 0.68)

hits = searcher.search(query)

print("Top 10 Results:\n")

for i, hit in enumerate(hits[:10], start=1):
    print(
        f"{i:2d}. "
        f"DocID={hit.docid}   "
        f"Score={hit.score:.6f}"
    )


print("\n")
print("=" * 80)
print("STEP 6: VERIFY")
print("=" * 80)

print(f"Manual Score : {score:.6f}")
print(f"Lucene Score : {hits[0].score:.6f}")


print("\n")
print("=" * 80)
print("STEP 7: RETRIEVED DOCUMENT")
print("=" * 80)

print(hits[0].lucene_document.get("raw"))
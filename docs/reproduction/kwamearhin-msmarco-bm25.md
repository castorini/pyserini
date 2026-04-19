Reproduced BM25 baseline for MS MARCO passage ranking using Pyserini.

Environment and Set-up:

OS: Windows 11 (WSL2 Ubuntu 22.04)
Python: 3.11
Java: OpenJDK 11/21
Pyserini: 1.2.0
Hardware: CPU-only

Issues and Results:

MRR@10 = 0.199 (msmarco-passage-dev-subset)

Used prebuilt msmarco-v1-passage index and executed BM25 retrieval with hits=1000.
Evaluation performed using msmarco_passage_eval.

Results are consistent with the expected Pyserini BM25 baseline (~0.19–0.20).

No issues encountered.

Single-line command:

python -m pyserini.search.lucene --index msmarco-v1-passage --topics msmarco-passage-dev-subset --output run.msmarco-pyserini.bm25.txt --bm25 --hits 1000

Index

Used prebuilt index: msmarco-v1-passage (automatically downloaded by Pyserini).
No local indexing was performed.

Evaluation:

python -m pyserini.eval.msmarco_passage_eval run.msmarco-pyserini.bm25.txt

Results

Expected MRR@10: ~0.19–0.20
Observed MRR@10: 0.199

Notes

No issues encountered. Results are consistent with the reported Pyserini BM25 baseline.
No major issues observed.


# A Conceptual Framework for Retrieval

This section reproduces the “A Conceptual Framework for Retrieval” stage in the Pyserini onboarding.

**Environment & Setup:**

- OS: Ubuntu 22.04  
- Python 3.10.12  
- Java: OpenJDK 21  
- Pyserini installed via pip  
- Index used: msmarco-v1-passage  

**Steps performed:**

1. **Configured JVM classpath in Python:**

```python
from pyserini.setup import configure_classpath
configure_classpath()

2. Loaded Lucene index and retrieved a document:

from pyserini.index.lucene import LuceneIndexReader

index_reader = LuceneIndexReader('indexes/lucene-index-msmarco-passage')
doc = index_reader.document('7187158')
print(doc)

Output:

{
  "id" : "7187158",
  "contents" : "Paula Deen and her brother Earl W. Bubba Hiers are being sued by a former general manager at Uncle Bubba's..."
}

3. Created query multi-hot vector:

from pyserini.analysis import Analyzer, get_lucene_analyzer

analyzer = Analyzer(get_lucene_analyzer())
query_tokens = analyzer.analyze("what is paula deen's brother")
multihot_query_weights = {k: 1 for k in query_tokens}

print("Tokens:", query_tokens)
print("Multi-hot vector:", multihot_query_weights)

Output:

Tokens: ['what', 'paula', 'deen', 'brother']
Multi-hot vector: {'what': 1, 'paula': 1, 'deen': 1, 'brother': 1}

4. Performed BM25 top-k search:

from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/lucene-index-msmarco-passage')
hits = searcher.search("what is paula deen's brother")

for i in range(10):
    print(f"{i+1} {hits[i].docid} {hits[i].score:.5f}")

Output:

 1 7187158 17.94950
 2 7187157 17.66560
 3 7187163 17.39060
 4 7546327 17.03410
 5 7187160 16.56520
 6 8227279 15.74180
 7 2298838 15.60820
 8 7617404 15.40040
 9 7187156 15.27550
10 2298839 14.97780

Conceptual notes (bi-encoder framework):

BM25 produces sparse lexical vectors (unsupervised).
Queries are represented as multi-hot vectors.
Documents are represented as sparse BM25 vectors.
Relevance is computed via the inner product of query and document vectors.
Dense retrieval models use learned dense vectors via transformers (not covered in this stage).
This completes the conceptual framework stage before moving on to dense retrieval experiments.

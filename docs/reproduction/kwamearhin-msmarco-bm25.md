# MS MARCO BM25 Reproduction Log (Pyserini)
Successfully reproduced the Pyserini BM25 baseline for MS MARCO Passage Ranking.

Environment:
- Windows 11 with WSL2 (Ubuntu 22.04)
- Python 3.11
- Pyserini installed via pip
- OpenJDK installed
- Maven installed
Installation:
pip install pyserini

sudo apt update
sudo apt install -y openjdk-11-jdk maven

Verify installation:

java -version
mvn -version

Retrieval

Multi-line command:

python -m pyserini.search.lucene \
  --index msmarco-v1-passage \
  --topics msmarco-passage-dev-subset \
  --output run.msmarco-pyserini.bm25.txt \
  --bm25 \
  --hits 1000

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


### A Conceptual Framework for Retrieval

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

**## BGE-base Baseline for NFCorpus**

Environment:
- Linux / Ubuntu
- Python 3.10+
- Pyserini installed in local environment
- CPU-only (for encoding); Faiss used for indexing and retrieval
- HuggingFace model: BAAI/bge-base-en-v1.5

Data:
- Dataset: NFCorpus (BEIR)
- Corpus size: 3,633 documents
- Queries munged to TSV; qrels munged to TREC format

Indexing:
```bash
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/nfcorpus.bge-base-en-v1.5 \
          --to-faiss \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32

Retrieval:
python -m pyserini.search.faiss \
  --encoder-class auto --encoder BAAI/bge-base-en-v1.5 --l2-norm \
  --pooling mean \
  --index indexes/nfcorpus.bge-base-en-v1.5 \
  --topics collections/nfcorpus/queries.tsv \
  --output runs/run.beir.bge-base-en-v1.5.nfcorpus.txt \
  --batch 128 --threads 8 \
  --hits 1000

Evaluation:
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels \
  runs/run.beir.bge-base-en-v1.5.nfcorpus.txt

Results:
ndcg_cut_10    all   0.3682

Interactive Retrieval:
from pyserini.search.faiss import FaissSearcher
from pyserini.encode import AutoQueryEncoder

encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)
searcher = FaissSearcher('indexes/nfcorpus.bge-base-en-v1.5', encoder)
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')

Sample output:
 1 MED-4555 0.764650
 2 MED-4424 0.683133
 3 MED-4421 0.680794
 4 MED-4560 0.679586
 5 MED-2750 0.666892
 6 MED-2939 0.665468
 7 MED-2946 0.662942
 8 MED-1663 0.661462
 9 MED-3436 0.656931
10 MED-4993 0.656215

Confirms that interactive retrieval matches batch retrieval results

Notes:

Used CPU for encoding; batch size adjusted for performance
Retrieval uses exact dot-product similarity (Faiss flat index)
HuggingFace model requires authentication token if exceeding rate limits
Workflow can also be performed with Contriever as an alternative dense retriever

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

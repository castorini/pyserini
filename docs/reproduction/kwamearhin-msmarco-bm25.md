# MS MARCO BM25 Reproduction Log (Pyserini)

Successfully reproduced the Pyserini BM25 baseline for MS MARCO Passage Ranking.

Environment:
- Windows 11 with WSL2 (Ubuntu 22.04)
- Python 3.11
- Pyserini installed via pip
- OpenJDK installed
- Maven installed

Command used:

python -m pyserini.search.lucene \
--index msmarco-v1-passage \
--topics msmarco-passage-dev-subset \
--output run.msmarco-pyserini.bm25.txt \
--bm25 \
--hits 1000

Evaluation:

MRR@10 ≈ 0.199

No major issues observed.

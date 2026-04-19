Reproduced BM25 baseline for MS MARCO passage ranking using Pyserini.

Environment:
- OS: Windows 11 (WSL2 Ubuntu 22.04)
- Python: 3.11
- Java: OpenJDK 11/21
- Pyserini: 1.2.0
- Hardware: CPU-only

Retrieval:
python -m pyserini.search.lucene \
  --index msmarco-v1-passage \
  --topics msmarco-passage-dev-subset \
  --output run.msmarco-pyserini.bm25.txt \
  --bm25 \
  --hits 1000

Evaluation:
python -m pyserini.eval.msmarco_passage_eval run.msmarco-pyserini.bm25.txt

Results:
MRR@10 = 0.199 (msmarco-passage-dev-subset)

Notes:
Results are consistent with the expected Pyserini BM25 baseline (~0.19–0.20). No issues encountered during execution.


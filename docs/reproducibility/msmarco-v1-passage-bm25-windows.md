# Reproduction Log: BM25 Retrieval on MS MARCO v1 Passage

## Environment
OS: Windows 10
Python: 3.14.3
Java: OpenJDK 21 (Temurin)

## Retrieval Command
python -m pyserini.search.lucene --index msmarco-v1-passage --topics msmarco-passage-dev-subset --output run.txt --bm25

## Evaluation Command
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.txt

## Result
MRR@10 = 0.187

## Notes
Experiment reproduced successfully on Windows.
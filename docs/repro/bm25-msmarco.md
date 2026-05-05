## Commands Used

```bash
python -m pyserini.search.lucene \
  --index msmarco-passage \
  --bm25 \
  --topics msmarco-passage-dev-subset \
  --output run.txt \
  --output-format msmarco

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset run.txt
```
## BM25 MS MARCO Reproduction

Environment:
- WSL2 Ubuntu
- Pyserini
- Java 21

Result:
MRR@10 = 0.1874

Notes:
- Installed Java manually
- Fixed Pyserini environment issues
- Learned MS MARCO evaluation pipeline




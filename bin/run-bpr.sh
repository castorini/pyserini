#!/bin/sh

date

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.bpr-single-nq \
  --topics dpr-nq-test \
  --encoded-queries bpr_single_nq-nq-test \
  --output runs/run.bpr.rerank.nq-test.nq.hash.trec \
  --batch-size 512 --threads 16 \
  --hits 100 --binary-hits 1000 \
  --searcher bpr --rerank

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr \
  --topics dpr-nq-test \
  --input runs/run.bpr.rerank.nq-test.nq.hash.trec \
  --output runs/run.bpr.rerank.nq-test.nq.hash.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.bpr.rerank.nq-test.nq.hash.json \
  --topk 20 100

date

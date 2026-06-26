#!/bin/sh

date

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.bpr-single-nq \
  --topics dpr-nq-test \
  --encoder castorini/bpr-nq-question-encoder \
  --encoder-class bpr \
  --output runs/run.bpr.rerank.nq-test.nq.hash.otf.trec \
  --batch-size 512 --threads 16 \
  --hits 100 --binary-hits 1000 \
  --searcher bpr --rerank

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr \
  --topics dpr-nq-test \
  --input runs/run.bpr.rerank.nq-test.nq.hash.otf.trec \
  --output runs/run.bpr.rerank.nq-test.nq.hash.otf.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.bpr.rerank.nq-test.nq.hash.otf.json \
  --topk 20 100

date

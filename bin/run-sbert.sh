#!/bin/sh

date

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.sbert \
  --topics msmarco-passage-dev-subset \
  --encoded-queries sbert-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.sbert.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.sbert.tsv \
  --output runs/run.msmarco-passage.sbert.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.sbert.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.sbert \
         --encoded-queries sbert-msmarco-passage-dev-subset \
  sparse --index msmarco-passage \
  fusion --alpha 0.015  \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.sbert.bm25.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bm25.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.sbert.bm25.tsv \
  --output runs/run.msmarco-passage.sbert.bm25.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.sbert.bm25.trec

##
## Everything again, except with on-the-fly encoding
##

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.sbert \
  --topics msmarco-passage-dev-subset \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --output runs/run.msmarco-passage.sbert.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.sbert.tsv \
  --output runs/run.msmarco-passage.sbert.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.sbert.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.sbert \
         --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  sparse --index msmarco-passage \
  fusion --alpha 0.015  \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.sbert.bm25.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval \
  msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bm25.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.sbert.bm25.tsv \
  --output runs/run.msmarco-passage.sbert.bm25.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.sbert.bm25.trec

date

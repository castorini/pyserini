#!/bin/sh

date

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.distilbert-dot-tas_b-b256 \
  --topics msmarco-passage-dev-subset \
  --encoded-queries distilbert_tas_b-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv \
  --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-tas_b-b256.trec

###

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.distilbert-dot-tas_b-b256 \
  --topics msmarco-passage-dev-subset \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.distilbert-dot-tas_b-b256.tsv \
  --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-tas_b-b256.trec

date

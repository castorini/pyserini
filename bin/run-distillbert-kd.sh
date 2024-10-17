#!/bin/sh

date

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.distilbert-dot-margin-mse-t2 \
  --topics msmarco-passage-dev-subset \
  --encoded-queries distilbert_kd-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec

###

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.distilbert-dot-margin-mse-t2 \
  --topics msmarco-passage-dev-subset \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec

date

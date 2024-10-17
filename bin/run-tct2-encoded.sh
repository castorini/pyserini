#!/bin/sh

date

## MS MARCO Passage

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert-v2 \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert-v2.tsv \
  --output runs/run.msmarco-passage.tct_colbert-v2.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2.trec


python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert-v2-hn \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-hn-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2-hn.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hn.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert-v2-hn.tsv \
  --output runs/run.msmarco-passage.tct_colbert-v2-hn.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hn.trec


python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert-v2-hnp \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2-hnp.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert-v2-hnp.tsv \
  --output runs/run.msmarco-passage.tct_colbert-v2-hnp.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.trec


python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.tct_colbert-v2-hnp \
         --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  sparse --index msmarco-v1-passage \
  fusion --alpha 0.06 \
  run    --topics msmarco-passage-dev-subset \
         --output-format msmarco \
         --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bm25.tsv \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.bm25.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bm25.tsv \
  --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bm25.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.bm25.trec


python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.tct_colbert-v2-hnp \
         --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  sparse --index msmarco-v1-passage.d2q-t5 \
  fusion --alpha 0.1 \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.tct_colbert-v2-hnp.doc2queryT5.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.doc2queryT5.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert-v2-hnp.doc2queryT5.tsv \
  --output runs/run.msmarco-passage.tct_colbert-v2-hnp.doc2queryT5.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert-v2-hnp.doc2queryT5.trec

date

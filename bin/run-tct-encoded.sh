#!/bin/sh

date

## MS MARCO Passage Ranking

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert.tsv \
  --output runs/run.msmarco-passage.tct_colbert.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.trec

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert.hnsw \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert.hnsw.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.hnsw.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert.hnsw.tsv \
  --output runs/run.msmarco-passage.tct_colbert.hnsw.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.hnsw.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.tct_colbert \
         --encoded-queries tct_colbert-msmarco-passage-dev-subset \
  sparse --index msmarco-v1-passage \
  fusion --alpha 0.12 \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.tct_colbert.bm25.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.bm25.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert.bm25.tsv \
  --output runs/run.msmarco-passage.tct_colbert.bm25.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.bm25.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-passage.tct_colbert \
         --encoded-queries tct_colbert-msmarco-passage-dev-subset \
  sparse --index msmarco-v1-passage.d2q-t5 \
  fusion --alpha 0.22 \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.tct_colbert.d2q-t5.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.d2q-t5.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.tct_colbert.d2q-t5.tsv \
  --output runs/run.msmarco-passage.tct_colbert.d2q-t5.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.tct_colbert.d2q-t5.trec


## MS MARCO Document Ranking

python -m pyserini.search.faiss \
  --index msmarco-v1-doc.tct_colbert \
  --topics msmarco-doc-dev \
  --encoded-queries tct_colbert-msmarco-doc-dev \
  --output runs/run.msmarco-doc.passage.tct_colbert.txt \
  --output-format msmarco \
  --batch-size 512 --threads 16 \
  --hits 1000 --max-passage --max-passage-hits 100

python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.passage.tct_colbert.txt

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.passage.tct_colbert.txt \
  --output runs/run.msmarco-doc.passage.tct_colbert.trec

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev \
  runs/run.msmarco-doc.passage.tct_colbert.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-doc.tct_colbert \
         --encoded-queries tct_colbert-msmarco-doc-dev \
  sparse --index msmarco-v1-doc-segmented \
  fusion --alpha 0.25 \
  run    --topics msmarco-doc-dev \
         --output runs/run.msmarco-doc.tct_colbert.bm25.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16 \
         --hits 1000 --max-passage --max-passage-hits 100

python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.tct_colbert.bm25.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.tct_colbert.bm25.tsv \
  --output runs/run.msmarco-doc.tct_colbert.bm25.trec

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev \
  runs/run.msmarco-doc.tct_colbert.bm25.trec

python -m pyserini.search.hybrid \
  dense  --index msmarco-v1-doc.tct_colbert \
         --encoded-queries tct_colbert-msmarco-doc-dev \
  sparse --index msmarco-v1-doc-segmented.d2q-t5 \
  fusion --alpha 0.32 \
  run    --topics msmarco-doc-dev \
         --output runs/run.msmarco-doc.tct_colbert.d2q-t5.tsv \
         --output-format msmarco \
         --batch-size 512 --threads 16 \
         --hits 1000 --max-passage --max-passage-hits 100

python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.tct_colbert.d2q-t5.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.tct_colbert.d2q-t5.tsv \
  --output runs/run.msmarco-doc.tct_colbert.d2q-t5.trec

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev \
  runs/run.msmarco-doc.tct_colbert.d2q-t5.trec

date

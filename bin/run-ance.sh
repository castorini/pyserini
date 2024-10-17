#!/bin/sh

date

## MS MARCO Passage

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.ance \
  --topics msmarco-passage-dev-subset \
  --encoded-queries ance-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.ance.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.ance.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.ance.tsv \
  --output runs/run.msmarco-passage.ance.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.ance.trec

## MS MARCO Document

python -m pyserini.search.faiss \
  --index msmarco-v1-doc.ance-maxp \
  --topics msmarco-doc-dev \
  --encoded-queries ance_maxp-msmarco-doc-dev \
  --output runs/run.msmarco-doc.passage.ance-maxp.txt \
  --output-format msmarco \
  --batch-size 512 --threads 16 \
  --hits 1000 --max-passage --max-passage-hits 100

python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.passage.ance-maxp.txt

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.passage.ance-maxp.txt \
  --output runs/run.msmarco-doc.passage.ance-maxp.trec

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev \
  runs/run.msmarco-doc.passage.ance-maxp.trec

## Natural Questions (NQ)

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.ance-multi \
  --topics dpr-nq-test \
  --encoded-queries ance_multi-nq-test \
  --output runs/run.ance.nq-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-test \
  --index wikipedia-dpr \
  --input runs/run.ance.nq-test.multi.trec \
  --output runs/run.ance.nq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.ance.nq-test.multi.json \
  --topk 20 100

## Trivia QA

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.ance-multi \
  --topics dpr-trivia-test \
  --encoded-queries ance_multi-trivia-test \
  --output runs/run.ance.trivia-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/run.ance.trivia-test.multi.trec \
  --output runs/run.ance.trivia-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.ance.trivia-test.multi.json \
  --topk 20 100

##
## Everything again, except with on-the-fly encoding
##

## MS MARCO Passage

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.ance \
  --topics msmarco-passage-dev-subset \
  --encoder castorini/ance-msmarco-passage \
  --output runs/run.msmarco-passage.ance.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16

python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.ance.tsv

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.ance.tsv \
  --output runs/run.msmarco-passage.ance.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.ance.trec

## MS MARCO Document

python -m pyserini.search.faiss \
  --index msmarco-v1-doc.ance-maxp \
  --topics msmarco-doc-dev \
  --encoder castorini/ance-msmarco-doc-maxp \
  --output runs/run.msmarco-doc.passage.ance-maxp.txt \
  --output-format msmarco \
  --batch-size 512 --threads 16 \
  --hits 1000 --max-passage --max-passage-hits 100

python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.passage.ance-maxp.txt

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.passage.ance-maxp.txt \
  --output runs/run.msmarco-doc.passage.ance-maxp.trec

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev \
  runs/run.msmarco-doc.passage.ance-maxp.trec

## Natural Questions (NQ)

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.ance-multi \
  --topics dpr-nq-test \
  --encoder castorini/ance-dpr-question-multi \
  --output runs/run.ance.nq-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-test \
  --index wikipedia-dpr \
  --input runs/run.ance.nq-test.multi.trec \
  --output runs/run.ance.nq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.ance.nq-test.multi.json \
  --topk 20 100

## Trivia QA

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.ance-multi \
  --topics dpr-trivia-test \
  --encoder castorini/ance-dpr-question-multi \
  --output runs/run.ance.trivia-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/run.ance.trivia-test.multi.trec \
  --output runs/run.ance.trivia-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.ance.trivia-test.multi.json \
  --topk 20 100

date

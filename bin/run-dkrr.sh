#!/bin/sh

date

## Natural Questions

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics dpr-nq-dev \
  --encoded-queries dkrr-dpr-nq-retriever-dpr-nq-dev \
  --output runs/run.dpr-dkrr-nq.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics nq-test \
  --encoded-queries dkrr-dpr-nq-retriever-nq-test \
  --output runs/run.dpr-dkrr-nq.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.dev.trec \
  --output runs/run.dpr-dkrr-nq.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.test.trec \
  --output runs/run.dpr-dkrr-nq.test.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.test.json \
  --topk 5 20 100 500 1000

## TriviaQA (TQA)

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-dev \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-dev \
  --output runs/run.dpr-dkrr-trivia.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-test \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-test \
  --output runs/run.dpr-dkrr-trivia.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.dev.trec \
  --output runs/run.dpr-dkrr-trivia.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.test.trec \
  --output runs/run.dpr-dkrr-trivia.test.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.test.json \
  --topk 5 20 100 500 1000

##
## Everything again, except with on-the-fly encoding
##

## Natural Questions

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics dpr-nq-dev \
  --encoder castorini/dkrr-dpr-nq-retriever \
  --output runs/run.dpr-dkrr-nq.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics nq-test \
  --encoder castorini/dkrr-dpr-nq-retriever \
  --output runs/run.dpr-dkrr-nq.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.dev.trec \
  --output runs/run.dpr-dkrr-nq.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.test.trec \
  --output runs/run.dpr-dkrr-nq.test.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.test.json \
  --topk 5 20 100 500 1000

## TriviaQA (TQA)

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-dev \
  --encoder castorini/dkrr-dpr-tqa-retriever \
  --output runs/run.dpr-dkrr-trivia.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-test \
  --encoder castorini/dkrr-dpr-tqa-retriever \
  --output runs/run.dpr-dkrr-trivia.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.dev.trec \
  --output runs/run.dpr-dkrr-trivia.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.test.trec \
  --output runs/run.dpr-dkrr-trivia.test.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.test.json \
  --topk 5 20 100 500 1000

date

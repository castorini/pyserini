#!/bin/sh

date

## Natural Questions (NQ) with DPR-Multi

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-nq-test \
  --encoder facebook/dpr-question_encoder-multiset-base \
  --output runs/run.otf.dpr.nq-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.otf.dpr.nq-test.multi.trec \
  --output runs/run.otf.dpr.nq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.nq-test.multi.json \
  --topk 20 100

python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --output runs/run.otf.dpr.nq-test.bm25.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.otf.dpr.nq-test.bm25.trec \
  --output runs/run.otf.dpr.nq-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.nq-test.bm25.json \
  --topk 20 100

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoder facebook/dpr-question_encoder-multiset-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.3 \
  run    --topics dpr-nq-test \
         --output runs/run.otf.dpr.nq-test.multi.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.otf.dpr.nq-test.multi.bm25.trec \
  --output runs/run.otf.dpr.nq-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.nq-test.multi.bm25.json \
  --topk 20 100


## TriviaQA with DPR-Multi

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-trivia-test \
  --encoder facebook/dpr-question_encoder-multiset-base \
  --output runs/run.otf.dpr.trivia-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.otf.dpr.trivia-test.multi.trec \
  --output runs/run.otf.dpr.trivia-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.trivia-test.multi.json \
  --topk 20 100

python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --output runs/run.otf.dpr.trivia-test.bm25.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.otf.dpr.trivia-test.bm25.trec \
  --output runs/run.otf.dpr.trivia-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.trivia-test.bm25.json \
  --topk 20 100

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoder facebook/dpr-question_encoder-multiset-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 0.95 \
  run    --topics dpr-trivia-test \
         --output runs/run.otf.dpr.trivia-test.multi.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.otf.dpr.trivia-test.multi.bm25.trec \
  --output runs/run.otf.dpr.trivia-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.trivia-test.multi.bm25.json \
  --topk 20 100


## WebQuestions (WQ) with DPR-Multi

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-wq-test \
  --encoder facebook/dpr-question_encoder-multiset-base \
  --output runs/run.otf.dpr.wq-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.otf.dpr.wq-test.multi.trec \
  --output runs/run.otf.dpr.wq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.wq-test.multi.json \
  --topk 20 100

python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --output runs/run.otf.dpr.wq-test.bm25.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.otf.dpr.wq-test.bm25.trec \
  --output runs/run.otf.dpr.wq-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.wq-test.bm25.json \
  --topk 20 100

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoder facebook/dpr-question_encoder-multiset-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 0.95 \
  run    --topics dpr-wq-test \
         --output runs/run.otf.dpr.wq-test.multi.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.otf.dpr.wq-test.multi.bm25.trec \
  --output runs/run.otf.dpr.wq-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.wq-test.multi.bm25.json \
  --topk 20 100


## CuratedTREC with DPR-Multi

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-curated-test \
  --encoder facebook/dpr-question_encoder-multiset-base \
  --output runs/run.otf.dpr.curated-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.otf.dpr.curated-test.multi.trec \
  --output runs/run.otf.dpr.curated-test.multi.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.curated-test.multi.json \
  --topk 20 100 \
  --regex

python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --output runs/run.otf.dpr.curated-test.bm25.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.otf.dpr.curated-test.bm25.trec \
  --output runs/run.otf.dpr.curated-test.bm25.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.curated-test.bm25.json \
  --topk 20 100 \
  --regex

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoder facebook/dpr-question_encoder-multiset-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.05 \
  run    --topics dpr-curated-test \
         --output runs/run.otf.dpr.curated-test.multi.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.otf.dpr.curated-test.multi.bm25.trec \
  --output runs/run.otf.dpr.curated-test.multi.bm25.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.curated-test.multi.bm25.json \
  --topk 20 100 \
  --regex


## SQuAD with DPR-Multi

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-squad-test \
  --encoder facebook/dpr-question_encoder-multiset-base \
  --output runs/run.otf.dpr.squad-test.multi.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.otf.dpr.squad-test.multi.trec \
  --output runs/run.otf.dpr.squad-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.squad-test.multi.json \
  --topk 20 100

python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --output runs/run.otf.dpr.squad-test.bm25.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.otf.dpr.squad-test.bm25.trec \
  --output runs/run.otf.dpr.squad-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.squad-test.bm25.json \
  --topk 20 100

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoder facebook/dpr-question_encoder-multiset-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 2.00 \
  run    --topics dpr-squad-test \
         --output runs/run.otf.dpr.squad-test.multi.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.otf.dpr.squad-test.multi.bm25.trec \
  --output runs/run.otf.dpr.squad-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.squad-test.multi.bm25.json \
  --topk 20 100


## Natural Questions (NQ) with DPR-Single

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-single-nq \
  --topics dpr-nq-test \
  --encoder facebook/dpr-question_encoder-single-nq-base \
  --output runs/run.otf.dpr.nq-test.single.trec \
  --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.otf.dpr.nq-test.single.trec \
  --output runs/run.otf.dpr.nq-test.single.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.nq-test.single.json \
  --topk 20 100

python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-single-nq \
         --encoder facebook/dpr-question_encoder-single-nq-base \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.2 \
  run    --topics dpr-nq-test \
         --output runs/run.otf.dpr.nq-test.single.bm25.trec \
         --batch-size 512 --threads 16

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-test \
  --index wikipedia-dpr-100w \
  --input runs/run.otf.dpr.nq-test.single.bm25.trec \
  --output runs/run.otf.dpr.nq-test.single.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.otf.dpr.nq-test.single.bm25.json \
  --topk 20 100

date

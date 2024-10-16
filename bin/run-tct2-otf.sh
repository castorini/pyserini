#!/bin/sh

date

## MS MARCO Passage

python -m pyserini.search.faiss \
  --index msmarco-v1-passage.tct_colbert-v2 \
  --topics msmarco-passage-dev-subset \
  --encoder castorini/tct_colbert-v2-msmarco \
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
  --encoder castorini/tct_colbert-v2-hn-msmarco \
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
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
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
         --encoder castorini/tct_colbert-v2-hnp-msmarco \
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
         --encoder castorini/tct_colbert-v2-hnp-msmarco \
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


## MS MARCO Doc

python -m pyserini.search.faiss \
  --index msmarco-v1-doc-segmented.tct_colbert-v2-hnp \
  --topics msmarco-doc-dev \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --output-format msmarco \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index msmarco-v1-doc-segmented.tct_colbert-v2-hnp \
  --topics dl19-doc \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index msmarco-v1-doc-segmented.tct_colbert-v2-hnp \
  --topics dl20 \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.dl20-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 512 --threads 16


python -m pyserini.eval.msmarco_doc_eval \
  --judgments msmarco-doc-dev \
  --run runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt

python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.trec

python -m pyserini.eval.trec_eval -c -m recall.100 -m map -m ndcg_cut.10 \
  msmarco-doc-dev runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.trec


python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 dl19-doc \
  runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt

python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 dl20-doc \
  runs/run.dl20-doc.passage.tct_colbert-v2-hnp-maxp.txt

date

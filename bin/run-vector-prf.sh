#!/bin/sh

date

# DL19, ANCE

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.ance.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.ance.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.ance.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL19, TCT v1

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL19, TCT v2

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct2.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct2.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.tct2.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL19, DistillBERT KD

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-kd.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-kd.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-kd.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL19, DistillBERT TASB

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-tasb.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-tasb.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.distilbert-tasb.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL19, SBERT

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl19.base

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl19.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl19-passage \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl19.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.sbert.dl19.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.sbert.dl19.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl19-passage runs/run.sbert.dl19.rocchio_prf5_a0.4_b0.6.trec

# DL20, ANCE

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.ance.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.ance.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.ance.dl20.rocchio_prf5_a0.4_b0.6.trec

# DL20, TCT v1

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct.dl20.rocchio_prf5_a0.4_b0.6.trec

# DL20, TCT v2

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct2.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct2.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.tct2.dl20.rocchio_prf5_a0.4_b0.6.trec

# DL20, DistillBERT KD

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-kd.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-kd.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-kd.dl20.rocchio_prf5_a0.4_b0.6.trec

# DL20, DistillBERT TASB

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-tasb.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-tasb.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.distilbert-tasb.dl20.rocchio_prf5_a0.4_b0.6.trec

# DL20, SBERT

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl20.base

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl20.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics dl20 \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.dl20.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.sbert.dl20.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.sbert.dl20.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10,100 -m recall.1000 -l 2 dl20-passage runs/run.sbert.dl20.rocchio_prf5_a0.4_b0.6.trec

# MS MARCO, ANCE

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-ance-bf \
  --encoder castorini/ance-msmarco-passage \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.ance.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.ance.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.ance.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.ance.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.ance.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.ance.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.ance.msmarco.rocchio_prf5_a0.4_b0.6.trec


# MS MARCO, TCT v1

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-bf \
  --encoder castorini/tct_colbert-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct.msmarco.rocchio_prf5_a0.4_b0.6.trec

# MS MARCO, TCT v2

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.tct2.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct2.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct2.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.tct2.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct2.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct2.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.tct2.msmarco.rocchio_prf5_a0.4_b0.6.trec

# MS MARCO, DistillBERT KD

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-kd.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-kd.msmarco.rocchio_prf5_a0.4_b0.6.trec

# MS MARCO, DistillBERT TASB

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
  --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.distilbert-tasb.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.distilbert-tasb.msmarco.rocchio_prf5_a0.4_b0.6.trec

# MS MARCO, SBERT

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.msmarco.base

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.msmarco.average_prf3.trec \
  --prf-depth 3 \
  --prf-method avg

python -m pyserini.search.faiss \
  --topics msmarco-passage-dev-subset \
  --index msmarco-passage-sbert-bf \
  --encoder sentence-transformers/msmarco-distilbert-base-v3 \
  --batch-size 64 \
  --threads 12 \
  --output runs/run.sbert.msmarco.rocchio_prf5_a0.4_b0.6.trec \
  --prf-depth 5 \
  --prf-method rocchio \
  --rocchio-topk 5 \
  --rocchio-alpha 0.4 \
  --rocchio-beta 0.6

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.sbert.msmarco.base
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.sbert.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.sbert.msmarco.rocchio_prf5_a0.4_b0.6.trec

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.sbert.msmarco.base
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.sbert.msmarco.average_prf3.trec
python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset runs/run.sbert.msmarco.rocchio_prf5_a0.4_b0.6.trec

date

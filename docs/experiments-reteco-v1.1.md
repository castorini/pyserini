# Pyserini: Reproducing RETECO v1.1 Track 1a BM25QS Baselines

This guide covers query-side BM25 (BM25QS) retrieval on [RETECO v1.1](https://huggingface.co/datasets/DataScience-UIBK/RETECO-SemEval2027) **Track 1a** (whole-query retrieval).

Pyserini provides a [prebuilt Track 1 index](prebuilt-indexes.md) named `reteco-v1.1-track1-{domain}` for each of the 13 domains: bitcoin, cardano, economics, genealogy, history, hsm, iota, law, monero, politics, quant, travel, and workplace.

The indexes were built from [commit `c21e10ba8aa60eaa201f60fc4604364469c5ec17` of the RETECO dataset on Hugging Face](https://huggingface.co/datasets/DataScience-UIBK/RETECO-SemEval2027/commit/c21e10ba8aa60eaa201f60fc4604364469c5ec17).

## Batch Retrieval Run

Run query-side BM25 (`k1=0.9`, `b=0.4`, top 1000). This example uses iota dev; change `domain` and `split` for other conditions.

```bash
domain=iota
split=dev
topics="reteco-v1.1-track1a-${domain}.${split}"
dir="runs/reteco-v1.1/${topics}"
mkdir -p "$dir"

python -m pyserini.search.lucene \
  --index "reteco-v1.1-track1-${domain}" \
  --topics "$topics" \
  --output "$dir/bm25qs.trec" \
  --bm25qs --k1 0.9 --b 0.4 --hits 1000
```

## Evaluation

```bash
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 \
  "$topics" "$dir/bm25qs.trec"
```

## BM25QS Baseline Results

Track 1a nDCG@10 (train: 1,211 queries; dev: 519 queries). The macro score is the unweighted mean across domains. BM25QS is close to, but not identical to, the official gensim BM25 baseline.

| Domain | Train | Dev |
|:---|---:|---:|
| bitcoin | 0.0845 | 0.0364 |
| cardano | 0.1801 | 0.1027 |
| economics | 0.0355 | 0.0466 |
| genealogy | 0.1183 | 0.1854 |
| history | 0.0640 | 0.0851 |
| hsm | 0.1767 | 0.2437 |
| iota | 0.1228 | 0.3243 |
| law | 0.0905 | 0.0574 |
| monero | 0.0378 | 0.0320 |
| politics | 0.2802 | 0.2607 |
| quant | 0.0255 | 0.0204 |
| travel | 0.0504 | 0.0270 |
| workplace | 0.0798 | 0.0398 |
| **Domain macro** | **0.1036** | **0.1124** |

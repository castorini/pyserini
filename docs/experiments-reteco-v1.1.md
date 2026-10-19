# Pyserini: Reproducing RETECO v1.1 Track 1a BM25 Baselines

This guide covers BM25 and query-side BM25 (BM25QS) retrieval on [RETECO v1.1](https://huggingface.co/datasets/DataScience-UIBK/RETECO-SemEval2027) **Track 1a** (whole-query retrieval).

Pyserini provides a [prebuilt Track 1 index](prebuilt-indexes.md) named `reteco-v1.1-track1-{domain}` for each of the 13 domains:
bitcoin, cardano, economics, genealogy, history, hsm, iota, law, monero, politics, quant, travel, and workplace.

The indexes were built from [commit `c21e10b` of the RETECO dataset on Hugging Face](https://huggingface.co/datasets/DataScience-UIBK/RETECO-SemEval2027/commit/c21e10ba8aa60eaa201f60fc4604364469c5ec17).

## Batch Retrieval Run

Run query-side BM25 (`k1=0.9`, `b=0.4`, top 1000).
Pyserini downloads the named index, topics, and qrels automatically.
This example uses iota dev; change `domain` and `split` for other conditions.

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

To reproduce the standard BM25 results, replace `--bm25qs` with `--bm25` and write to `$dir/bm25.trec`.

## Evaluation

```bash
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 \
  "$topics" "$dir/bm25qs.trec"
```

## BM25 and BM25QS Baseline Results

Track 1a nDCG@10 (train: 1,211 queries; dev: 519 queries), compared with the v1.1 results in the [official baseline table](https://github.com/DataScienceUIBK/RETECO/blob/5616900ce9f982e329a8b4ea5673ff0ebc007026/starter_kit/BASELINE_RESULTS.md).
The [RETECO starter kit](https://github.com/DataScienceUIBK/RETECO/tree/5616900ce9f982e329a8b4ea5673ff0ebc007026/starter_kit) provides the official baseline implementation.
Scores are averaged over queries within each domain.
The macro row is the unweighted mean across domains.

| Domain           | BM25 train | BM25QS train | Official train |   BM25 dev | BM25QS dev | Official dev |
| :--------------- | ---------: | -----------: | -------------: | ---------: | ---------: | -----------: |
| bitcoin          |     0.0468 |       0.0845 |         0.0856 |     0.0300 |     0.0364 |       0.0370 |
| cardano          |     0.1753 |       0.1801 |         0.1848 |     0.1144 |     0.1027 |       0.1027 |
| economics        |     0.0361 |       0.0355 |         0.0382 |     0.0269 |     0.0466 |       0.0467 |
| genealogy        |     0.0639 |       0.1183 |         0.1242 |     0.1476 |     0.1854 |       0.1949 |
| history          |     0.0336 |       0.0640 |         0.0654 |     0.0428 |     0.0851 |       0.0873 |
| hsm              |     0.1703 |       0.1767 |         0.1736 |     0.2366 |     0.2437 |       0.2489 |
| iota             |     0.0352 |       0.1228 |         0.1563 |     0.3852 |     0.3243 |       0.3309 |
| law              |     0.0399 |       0.0905 |         0.0946 |     0.0294 |     0.0574 |       0.0574 |
| monero           |     0.0288 |       0.0378 |         0.0382 |     0.0249 |     0.0320 |       0.0320 |
| politics         |     0.2664 |       0.2802 |         0.2810 |     0.2129 |     0.2607 |       0.2625 |
| quant            |     0.0128 |       0.0255 |         0.0255 |     0.0000 |     0.0204 |       0.0237 |
| travel           |     0.0412 |       0.0504 |         0.0506 |     0.0322 |     0.0270 |       0.0442 |
| workplace        |     0.0622 |       0.0798 |         0.0798 |     0.0000 |     0.0398 |       0.0230 |
| **Domain macro** | **0.0779** |   **0.1036** |     **0.1075** | **0.0987** | **0.1124** |   **0.1147** |

BM25QS approximates the official gensim BM25 implementation but does not reproduce its rankings exactly.

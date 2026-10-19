# Pyserini: Reproducing RETECO v1.1 Track 1a BM25QS Baselines

This guide covers query-side BM25 (BM25QS) retrieval on [RETECO v1.1](https://huggingface.co/datasets/DataScience-UIBK/RETECO-SemEval2027) **Track 1a** (whole-query retrieval).

Pyserini provides these [prebuilt Track 1 indexes](prebuilt-indexes.md), one per domain:

- `reteco-v1.1-track1-bitcoin`, `reteco-v1.1-track1-cardano`, `reteco-v1.1-track1-economics`
- `reteco-v1.1-track1-genealogy`, `reteco-v1.1-track1-history`, `reteco-v1.1-track1-hsm`
- `reteco-v1.1-track1-iota`, `reteco-v1.1-track1-law`, `reteco-v1.1-track1-monero`
- `reteco-v1.1-track1-politics`, `reteco-v1.1-track1-quant`, `reteco-v1.1-track1-travel`, `reteco-v1.1-track1-workplace`

The indexes use RETECO v1.1 revision `c21e10ba8aa60eaa201f60fc4604364469c5ec17`.

## Data Prep

Download topics and qrels from the [Castorini eval catalog](https://github.com/castorini/eval/tree/5a26fd8d1a9e8408ae9a2606e95852312f1e0062). This example uses **iota dev**; change `domain` and `split` for other conditions.

```bash
split=dev
domain=iota
name="reteco-v1.1-track1a-${domain}.${split}"
dir="runs/reteco-v1.1/${name}"
mkdir -p "$dir"
export RETECO_NAME="$name" RETECO_DIR="$dir"

python - <<'PY'
import gzip
import json
import os
from pathlib import Path
from urllib.request import urlopen

rev = '5a26fd8d1a9e8408ae9a2606e95852312f1e0062'
url = f'https://raw.githubusercontent.com/castorini/eval/{rev}/'
name = os.environ['RETECO_NAME']
out = Path(os.environ['RETECO_DIR'])
with urlopen(f'{url}topics/topics.{name}.tsv.gz') as response:
    rows = gzip.decompress(response.read()).decode('utf-8').splitlines()
topics = {qid: {'title': text} for qid, text in (row.split('\t', 1) for row in rows)}
(out / 'topics.json').write_text(json.dumps(topics, ensure_ascii=False), encoding='utf-8')
with urlopen(f'{url}qrels/qrels.{name}.txt') as response:
    (out / 'qrels.txt').write_bytes(response.read())
PY
```

## Batch Retrieval Run

Run query-side BM25 (`k1=0.9`, `b=0.4`, top 1000):

```bash
python -m pyserini.search.lucene \
  --index "reteco-v1.1-track1-${domain}" \
  --topics "$dir/topics.json" \
  --output "$dir/bm25qs.trec" \
  --bm25qs --k1 0.9 --b 0.4 --hits 1000
```

## Evaluation

```bash
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 \
  "$dir/qrels.txt" "$dir/bm25qs.trec"
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

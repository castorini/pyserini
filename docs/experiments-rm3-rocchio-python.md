# Pyserini versus Anserini Pseudo-Relevance Feedback

This document reports results from re-implementing Anserini's RM3 and Rocchio pseudo-relevance feedback methods in Python. We compare the Python implementations against the corresponding Java implementations in Anserini.

These experiments were run on April 26, 2026, using Pyserini with Lucene 10.4.

## Rocchio Feedback: Python versus Java

We run the Rocchio experiments using Pyserini's Lucene search module with BM25 + Rocchio. For TREC DL 2019-2020, we use the `msmarco-v1-passage-full` index with topics `dl19-passage` and `dl20-passage`. For TREC DL 2021-2023, we use the `msmarco-v2-passage-full` index with topics `dl21`, `dl22`, and `dl23`.

Each run uses either the Python Rocchio implementation, `--rocchio-py`, or the Java Rocchio implementation, `--rocchio`. All experiments use the default Rocchio parameters.

We run the experiments using the following commands:

Python Rocchio on `msmarco-v1-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v1-passage-full \
  --topics <dl19-passage|dl20-passage> \
  --output <run-file> \
  --bm25 --rocchio-py
```

Java Rocchio on `msmarco-v1-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v1-passage-full \
  --topics <dl19-passage|dl20-passage> \
  --output <run-file> \
  --bm25 --rocchio
```

Python Rocchio on `msmarco-v2-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage-full \
  --topics <dl21|dl22|dl23> \
  --output <run-file> \
  --bm25 --rocchio-py
```

Java Rocchio on `msmarco-v2-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage-full \
  --topics <dl21|dl22|dl23> \
  --output <run-file> \
  --bm25 --rocchio
```

## Rocchio Effectiveness

| Topic | Index | Method | nDCG@10 | Recall@1000 |
|---|---|---|---:|---:|
| `dl19` | `msmarco-v1-passage-full` | `rocchio-py` | 0.5275 | 0.7946 |
| `dl19` | `msmarco-v1-passage-full` | `rocchio` | 0.5275 | 0.7948 |
| `dl20` | `msmarco-v1-passage-full` | `rocchio-py` | 0.4875 | 0.8330 |
| `dl20` | `msmarco-v1-passage-full` | `rocchio` | 0.4908 | 0.8327 |
| `dl21` | `msmarco-v2-passage-full` | `rocchio-py` | 0.4547 | 0.6709 |
| `dl21` | `msmarco-v2-passage-full` | `rocchio` | 0.4544 | 0.6709 |
| `dl22` | `msmarco-v2-passage-full` | `rocchio-py` | 0.2745 | 0.3639 |
| `dl22` | `msmarco-v2-passage-full` | `rocchio` | 0.2742 | 0.3639 |
| `dl23` | `msmarco-v2-passage-full` | `rocchio-py` | 0.2642 | 0.4798 |
| `dl23` | `msmarco-v2-passage-full` | `rocchio` | 0.2653 | 0.4810 |

## Latency

Latency is averaged over three measured runs after one warmup run on the WATGPU CPU node `watgpu608`. `Queries/s` is computed as `Queries / Avg Search Seconds`.

| Topic | Index | Method | Avg Search Seconds | Queries | Queries/s |
|---|---|---|---:|---:|---:|
| `dl19` | `msmarco-v1-passage-full` | `rocchio-py` | 11.868 | 43 | 3.62 |
| `dl19` | `msmarco-v1-passage-full` | `rocchio` | 10.601 | 43 | 4.06 |
| `dl20` | `msmarco-v1-passage-full` | `rocchio-py` | 24.018 | 200 | 8.33 |
| `dl20` | `msmarco-v1-passage-full` | `rocchio` | 12.827 | 200 | 15.59 |
| `dl21` | `msmarco-v2-passage-full` | `rocchio-py` | 116.961 | 477 | 4.08 |
| `dl21` | `msmarco-v2-passage-full` | `rocchio` | 26.076 | 477 | 18.29 |
| `dl22` | `msmarco-v2-passage-full` | `rocchio-py` | 109.533 | 500 | 4.56 |
| `dl22` | `msmarco-v2-passage-full` | `rocchio` | 26.001 | 500 | 19.23 |
| `dl23` | `msmarco-v2-passage-full` | `rocchio-py` | 168.508 | 700 | 4.15 |
| `dl23` | `msmarco-v2-passage-full` | `rocchio` | 33.425 | 700 | 20.94 |

## RM3 Feedback: Python versus Java

We next run the same comparison with BM25 + RM3, again using Pyserini's Lucene search module and the same TREC DL topics and indexes described above.

We run the experiments using the following commands:

Python RM3 on `msmarco-v1-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v1-passage-full \
  --topics <dl19-passage|dl20-passage> \
  --output <run-file> \
  --bm25 --rm3-py
```

Java RM3 on `msmarco-v1-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v1-passage-full \
  --topics <dl19-passage|dl20-passage> \
  --output <run-file> \
  --bm25 --rm3
```

Python RM3 on `msmarco-v2-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage-full \
  --topics <dl21|dl22|dl23> \
  --output <run-file> \
  --bm25 --rm3-py
```

Java RM3 on `msmarco-v2-passage-full`:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage-full \
  --topics <dl21|dl22|dl23> \
  --output <run-file> \
  --bm25 --rm3
```

## RM3 Effectiveness

| Topic | Index | Method | nDCG@10 | Recall@1000 |
|---|---|---|---:|---:|
| `dl19` | `msmarco-v1-passage-full` | `rm3-py` | 0.5146 | 0.7952 |
| `dl19` | `msmarco-v1-passage-full` | `rm3` | 0.5147 | 0.7950 |
| `dl20` | `msmarco-v1-passage-full` | `rm3-py` | 0.4889 | 0.8292 |
| `dl20` | `msmarco-v1-passage-full` | `rm3` | 0.4924 | 0.8292 |
| `dl21` | `msmarco-v2-passage-full` | `rm3-py` | 0.4454 | 0.6618 |
| `dl21` | `msmarco-v2-passage-full` | `rm3` | 0.4455 | 0.6616 |
| `dl22` | `msmarco-v2-passage-full` | `rm3-py` | 0.2683 | 0.3559 |
| `dl22` | `msmarco-v2-passage-full` | `rm3` | 0.2686 | 0.3559 |
| `dl23` | `msmarco-v2-passage-full` | `rm3-py` | 0.2602 | 0.4745 |
| `dl23` | `msmarco-v2-passage-full` | `rm3` | 0.2602 | 0.4748 |

## Latency

Latency is averaged over three measured runs after one warmup run on the WATGPU CPU node `watgpu608`. `Queries/s` is computed as `Queries / Avg Search Seconds`.

| Topic | Index | Method | Avg Search Seconds | Queries | Queries/s |
|---|---|---|---:|---:|---:|
| `dl19` | `msmarco-v1-passage-full` | `rm3-py` | 11.715 | 43 | 3.67 |
| `dl19` | `msmarco-v1-passage-full` | `rm3` | 9.275 | 43 | 4.64 |
| `dl20` | `msmarco-v1-passage-full` | `rm3-py` | 20.096 | 200 | 9.95 |
| `dl20` | `msmarco-v1-passage-full` | `rm3` | 11.153 | 200 | 17.93 |
| `dl21` | `msmarco-v2-passage-full` | `rm3-py` | 102.175 | 477 | 4.67 |
| `dl21` | `msmarco-v2-passage-full` | `rm3` | 23.270 | 477 | 20.50 |
| `dl22` | `msmarco-v2-passage-full` | `rm3-py` | 96.225 | 500 | 5.20 |
| `dl22` | `msmarco-v2-passage-full` | `rm3` | 22.701 | 500 | 22.03 |
| `dl23` | `msmarco-v2-passage-full` | `rm3-py` | 144.725 | 700 | 4.84 |
| `dl23` | `msmarco-v2-passage-full` | `rm3` | 28.199 | 700 | 24.82 |

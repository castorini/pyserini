# Pyserini: IRST on MS MARCO V1 Collections

This guide describes how to reproduce the IRST (Information Retrieval as Statistical Translation) experiments on the MS MARCO V1 collections, as described in the following paper:

> Yuqi Liu, Chengcheng Hu, and Jimmy Lin. [Another Look at Information Retrieval as Statistical Translation.](https://cs.uwaterloo.ca/~jimmylin/publications/Liu_etal_SIGIR2022.pdf) _Proceedings of the 45th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2022)_, July 2022.

Below, we discuss passage ranking and two document ranking conditions (full docs and segmented docs).

## Passage Ranking

Here, we start directly from our pre-built indexes and already-trained IRST models.
The IBM model we use is referenced in [Boytsov et al. (2021)](https://arxiv.org/abs/2102.06815).
For training the model from scratch, consult the [guide in FlexNeuART](https://github.com/oaqa/FlexNeuART/tree/master/demo).

The following commands will reproduce the results in Table 1 of our paper:

**IRST (Sum)**

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-passage-dev-subset \
  --index msmarco-v1-passage \
  --output runs/run.irst-sum.passage.dev.txt \
  --alpha 0.1
```

**IRST (Max)**

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-passage-dev-subset \
  --index msmarco-v1-passage \
  --output runs/run.irst-max.passage.dev.txt \
  --alpha 0.3 \
  --max-sim
```

The option `--topics` specifies the different topics.
The choices are:

+ MS MARCO V1 passage dev queries: `msmarco-passage-dev-subset` (per above)
+ TREC DL 2019 passage: `dl19-passage`
+ TREC DL 2020 passage: `dl20`

To evaluate results, use `trec_eval`.
For MS MARCO V1 passage:

```bash
python -m pyserini.eval.trec_eval -c -M 10 -m ndcg_cut.10 -m map -m recip_rank \
  msmarco-passage-dev-subset runs/run.irst-sum.passage.dev.txt
```

For TREC DL 2019, not that we need to specify `-l 2`:

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -l 2 \
  dl19-passage runs/run.irst-sum.dl19.txt
```

Similarly, for TREC DL 2020:

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -l 2 \
  dl20-passage runs/run.irst-sum.dl20.txt
```

The results should match Table 1 from our paper, repeated below:

|                              | MS MARCO Dev | TREC 2019 |       | TREC 2020 |       |
|:-----------------------------|-------------:|----------:|------:|----------:|------:|
|                              |       MRR@10 |   nDCG@10 |   MAP |   nDCG@10 |   MAP |
| (1a) BM25 (k1= 0.82, b=0.68) |        0.188 |     0.497 | 0.290 |     0.488 | 0.288 |
| (2a) BM25 + IRST (Sum)       |        0.221 |     0.526 | 0.328 |     0.558 | 0.352 |
| (2b) BM25 + IRST (Max)       |        0.215 |     0.537 | 0.329 |     0.547 | 0.336 |

The BM25 baseline is provided for reference.

## Document Ranking

In the paper, we explore two different conditions for document ranking: full documents and segmented documents.

For full documents:

**IRST (Sum)**

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-doc-dev \
  --index msmarco-v1-doc \
  --output runs/run.irst-sum.doc-full.dev.txt \
  --alpha 0.3 \
  --hits 1000
```

**IRST (Max)**

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-doc-dev \
  --index msmarco-v1-doc \
  --output runs/run.irst-max.doc-full.dev.txt \
  --alpha 0.3 \
  --hits 1000 \
  --max-sim
```

For segmented documents:

**IRST (Sum)** 

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-doc-dev \
  --index msmarco-v1-doc-segmented \
  --output runs/run.irst-sum.doc-seg.dev.txt \
  --alpha 0.3 \
  --segments \
  --hits 10000
```

**IRST (Max)**

```bash
python -m pyserini.search.lucene.irst \
  --topics msmarco-doc-dev \
  --index msmarco-v1-doc-segmented \
  --output runs/run.irst-max.doc-seg.dev.txt \
  --alpha 0.3 \
  --hits 10000 \
  --segments \
  --max-sim
```

The option `--topics` specifies the different topics.
The choices are:

+ MS MARCO V1 doc dev queries: `msmarco-doc-dev` (per above)
+ TREC DL 2019 passage: `dl19-passage`
+ TREC DL 2020 passage: `dl20`

To evaluate results, use `trec_eval`.
For MS MARCO V1 doc:

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m ndcg_cut.10 -m map -m recip_rank \
  msmarco-doc-dev runs/run.irst-sum.doc-full.dev.txt
```

For TREC DL 2019:

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map -m ndcg_cut.10 \
  dl19-doc runs/run.irst-sum.doc-full.dl19.txt
```

Similarly, for TREC DL 2020:

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map -m ndcg_cut.10 \
  dl20-doc runs/run.irst-sum.doc-full.dl20.txt
```

The results should match Table 1 from our paper, repeated below:

|                              | MS MARCO Dev | TREC 2019 |       | TREC 2020 |       |
|:-----------------------------|-------------:|----------:|------:|----------:|------:|
|                              |       MRR@10 |   nDCG@10 |   MAP |   nDCG@10 |   MAP |
| **Document (Full)**          |              |           |       |           |       |
| (2a) BM25 (k1= 0.82, b=0.68) |        0.249 |     0.510 | 0.241 |     0.528 | 0.378 |
| (2b) BM25 + IRST (Sum)       |        0.302 |     0.549 | 0.252 |     0.556 | 0.383 |
| (2c) BM25 + IRST (Max)       |        0.252 |     0.491 | 0.220 |     0.502 | 0.337 |
| **Document (Segmented)**     |              |           |       |           |       |
| (3a) BM25 (k1= 0.82, b=0.68) |        0.269 |     0.529 | 0.240 |     0.531 | 0.362 |
| (3b) BM25 + IRST (Sum)       |        0.296 |     0.560 | 0.271 |     0.534 | 0.376 |
| (3c) BM25 + IRST (Max)       |        0.259 |     0.520 | 0.243 |     0.509 | 0.350 |

The BM25 baselines are provided for reference.

## Reproduction Log[*](reproducibility.md)

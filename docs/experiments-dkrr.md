# Pyserini: Reproducing DKRR Results

DKRR (Distilling Knowledge from Reader to Retriever) is a technique to learn retriever models described in the following paper:

> Gautier Izacard and Edouard Grave. [Distilling Knowledge from Reader to Retriever for Question Answering](https://arxiv.org/abs/2012.04584). *arXiv:2012.04584*, 2020.

We have incorporated this work into Pyserini.
In particular, we have taken the pretrained `nq_retriever` and `tqa_retriever` models from the [DKRR repo](https://github.com/facebookresearch/FiD), used them to index English Wikipedia, and then incorporate into the dense retrieval framework in Pyserini.

This guide provides instructions to reproduce our results.

## Natural Questions

Running DKRR retrieval on nq-test and dpr-nq-dev of the Natural Questions dataset:

```bash
$ python -m pyserini.search.faiss \
  --index wikipedia-dpr-dkrr-nq \
  --topics nq-test \
  --encoded-queries dkrr-dpr-nq-retriever-nq-test \
  --output runs/nq.dkrr.ans.test.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12

$ python -m pyserini.search.faiss \
  --index wikipedia-dpr-dkrr-nq \
  --topics dpr-nq-dev \
  --encoded-queries dkrr-dpr-nq-retriever-dpr-nq-dev \
  --output runs/dpr-nq.dkrr.ans.dev.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12  
```
Alternatively, replace --encoded-queries dkrr-dpr-nq-retriever-nq-test and --encoded-queries dkrr-dpr-nq-retriever-dpr-nq-dev with --encoder castorini/dkrr-dpr-nq-retriever for on-the-fly query encoding.

To evaluate, convert the TREC output format to DPR's json format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wikipedia-dpr \
  --input runs/nq.dkrr.ans.test.trec \
  --output runs/nq.dkrr.ans.test.json

$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-dev \
  --index wikipedia-dpr \
  --input runs/dpr-nq.dkrr.ans.dev.trec \
  --output runs/dpr-nq.dkrr.ans.dev.json
```

Evaluating:

```bash
$ python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/nq.dkrr.ans.test.json \
  --topk 5 20 100 500 1000

$ python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/dpr-nq.dkrr.ans.dev.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   | ours (nq-test) | ours (dpr-nq-dev) | orig (dpr-nq-dev) |
|:---------|---------------:|------------------:|------------------:|
| Top-5    |          73.80 |             72.40 |                   |
| Top-20   |          84.27 |             82.36 |              82.4 |
| Top-100  |          89.34 |             87.87 |              87.9 |
| Top-500  |          92.24 |             90.37 |                   |
| Top-1000 |          93.43 |             91.30 |                   |

For reference, reported results from the paper (Table 7) are shown in the "orig" column.

## TriviaQA (TQA)

Running DKRR retrieval on dpr-trivia-test and dpr-trivia-dev of the TriviaQA dataset:

```bash
$ python -m pyserini.search.faiss \
  --index wikipedia-dpr-dkrr-tqa \
  --topics dpr-trivia-test \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-test \
  --output runs/dpr-trivia.dkrr.ans.test.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12

$ python -m pyserini.search.faiss \
  --index wikipedia-dpr-dkrr-tqa \
  --topics dpr-trivia-dev \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-dev \
  --output runs/dpr-trivia.dkrr.ans.dev.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12
```
Alternatively, replace --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-test and --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-dev with --encoder castorini/dkrr-dpr-tqa-retriever for on-the-fly query encoding.

To evaluate, convert the TREC output format to DPR's json format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/dpr-trivia.dkrr.ans.test.trec \
  --output runs/dpr-trivia.dkrr.ans.test.json

$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-dev \
  --index wikipedia-dpr \
  --input runs/dpr-trivia.dkrr.ans.dev.trec \
  --output runs/dpr-trivia.dkrr.ans.dev.json
```

Evaluating:

```bash
$ python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/dpr-trivia.dkrr.ans.test.json \
  --topk 5 20 100 500 1000

$ python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/dpr-trivia.dkrr.ans.dev.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   | ours (dpr-trivia-test) | ours (dpr-trivia-dev) | orig (dpr-trivia-dev) |
|:---------|-----------------------:|----------------------:|----------------------:|
| Top-5    |                  77.23 |                 77.31 |                       |
| Top-20   |                  83.74 |                 83.63 |                  83.5 |
| Top-100  |                  87.78 |                 87.39 |                  87.4 |
| Top-500  |                  89.87 |                 89.77 |                       |
| Top-1000 |                  90.63 |                 90.35 |                       |

For reference, reported results from the paper (Table 7) are shown in the "orig" column.


## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))

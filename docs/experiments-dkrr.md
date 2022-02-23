# Pyserini: Reproducing DKRR Results

DKRR (Distilling Knowledge from Reader to Retriever) is a technique to learn retriever models described in the following paper:

> Gautier Izacard and Edouard Grave. [Distilling Knowledge from Reader to Retriever for Question Answering](https://arxiv.org/abs/2012.04584). *arXiv:2012.04584*, 2020.

We have incorporated this work into Pyserini.
In particular, we have taken the pretrained `nq_retriever` and `tqa_retriever` models from the [DKRR repo](https://github.com/facebookresearch/FiD), used them to index English Wikipedia, and then incorporate into the dense retrieval framework in Pyserini.

This guide provides instructions to reproduce our results.

## Natural Questions

Running DKRR retrieval (here we are performing on-the-fly query encoding):

```bash
python -m pyserini.dsearch \
  --index wikipedia-dpr-dkrr-nq \
  --topics nq-test \
  --encoder castorini/dkrr-dpr-nq-retriever \
  --output runs/nq.dkrr.ans.test.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12
```

To evaluate, convert the TREC output format to DPR's json format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wikipedia-dpr \
  --input runs/nq.dkrr.ans.test.trec \
  --output runs/nq.dkrr.ans.test.json
```

Evaluating:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/nq.dkrr.ans.test.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   |  ours | orig |
|:---------|------:|-----:|
| Top-5    | 73.80 |
| Top-20   | 84.27 |
| Top-100  | 89.34 |
| Top-500  | 92.24 |
| Top-1000 | 93.43 |

For reference, reported results from the paper are shown in the "orig" column.

**TODO:** Add comparison scores from original paper.

## TriviaQA (TQA)

Running DKRR retrieval (here we are performing on-the-fly query encoding):

```bash
python -m pyserini.dsearch \
  --index wikipedia-dpr-dkrr-tqa \
  --topics dpr-trivia-test \
  --encoder castorini/dkrr-dpr-tqa-retriever \
  --output runs/dpr-trivia.dkrr.ans.test.trec \
  --query-prefix question: \
  --batch-size 36 --threads 12
```

To evaluate, convert the TREC output format to DPR's json format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/dpr-trivia.dkrr.ans.test.trec \
  --output runs/dpr-trivia.dkrr.ans.test.json
```

Evaluating:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/dpr-trivia.dkrr.ans.test.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   |  ours | orig |
|:---------|------:|-----:|
| Top-5    | 77.23 |
| Top-20   | 83.74 |
| Top-100  | 87.78 |
| Top-500  | 89.87 |
| Top-1000 | 90.63 |

For reference, reported results from the paper are shown in the "orig" column.

**TODO:** Add comparison scores from original paper.


## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))

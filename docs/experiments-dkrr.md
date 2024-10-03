# Pyserini: Reproducing DKRR Results

DKRR (Distilling Knowledge from Reader to Retriever) is a technique to learn retriever models described in the following paper:

> Gautier Izacard and Edouard Grave. [Distilling Knowledge from Reader to Retriever for Question Answering](https://arxiv.org/abs/2012.04584). *arXiv:2012.04584*, 2020.

We have incorporated this work into Pyserini.
In particular, we have taken the pretrained `nq_retriever` and `tqa_retriever` models from the [DKRR repo](https://github.com/facebookresearch/FiD), used them to index English Wikipedia, and then incorporate into the dense retrieval framework in Pyserini.

This guide provides instructions to reproduce our results.

## Natural Questions

Running DKRR retrieval on `dpr-nq-dev` and `nq-test` of the Natural Questions dataset:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics dpr-nq-dev \
  --encoded-queries dkrr-dpr-nq-retriever-dpr-nq-dev \
  --output runs/run.dpr-dkrr-nq.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-nq \
  --topics nq-test \
  --encoded-queries dkrr-dpr-nq-retriever-nq-test \
  --output runs/run.dpr-dkrr-nq.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16
```

Alternatively, replace `--encoded-queries ...` with `--encoder castorini/dkrr-dpr-nq-retriever` for on-the-fly query encoding.

To evaluate, convert the TREC output format to DPR's json format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.dev.trec \
  --output runs/run.dpr-dkrr-nq.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-nq.test.trec \
  --output runs/run.dpr-dkrr-nq.test.json
```

Evaluating:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-nq.test.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   | `dpr-nq-dev` (ours) | `dpr-nq-dev` (orig) | `nq-test` (ours) |
|:---------|--------------------:|--------------------:|-----------------:|
| Top-5    |               72.40 |                     |            73.80 | 
| Top-20   |               82.36 |                82.4 |            84.27 |
| Top-100  |               87.87 |                87.9 |            89.34 |
| Top-500  |               90.37 |                     |            92.24 |
| Top-1000 |               91.30 |                     |            93.43 |

For reference, reported results from the paper (Table 8) are shown in the "orig" column.

## TriviaQA (TQA)

Running DKRR retrieval on `dpr-trivia-dev` and `dpr-trivia-test` of the TriviaQA dataset:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-dev \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-dev \
  --output runs/run.dpr-dkrr-trivia.dev.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16

python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dkrr-tqa \
  --topics dpr-trivia-test \
  --encoded-queries dkrr-dpr-tqa-retriever-dpr-tqa-test \
  --output runs/run.dpr-dkrr-trivia.test.trec \
  --query-prefix question: \
  --batch-size 512 --threads 16
```
Alternatively, replace `--encoded-queries ...` with `--encoder castorini/dkrr-dpr-tqa-retriever` for on-the-fly query encoding.

To evaluate, convert the TREC output format to DPR's json format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-dev \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.dev.trec \
  --output runs/run.dpr-dkrr-trivia.dev.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wikipedia-dpr \
  --input runs/run.dpr-dkrr-trivia.test.trec \
  --output runs/run.dpr-dkrr-trivia.test.json
```

Evaluating:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.dev.json \
  --topk 5 20 100 500 1000

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dpr-dkrr-trivia.test.json \
  --topk 5 20 100 500 1000
```

The expected results are as follows, shown in the "ours" column:

| Metric   | `dpr-trivia-dev` (ours) | `dpr-trivia-dev` (orig) | `dpr-trivia-test` (ours) |
|:---------|------------------------:|------------------------:|-------------------------:|
| Top-5    |                   77.31 |                         |                    77.23 |
| Top-20   |                   83.63 |                    83.5 |                    83.74 |
| Top-100  |                   87.39 |                    87.4 |                    87.78 |
| Top-500  |                   89.77 |                         |                    89.87 |
| Top-1000 |                   90.35 |                         |                    90.63 |

For reference, reported results from the paper (Table 8) are shown in the "orig" column.

## Hybrid sparse-dense retrieval with GAR-T5

Running hybrid sparse-dense retrieval with DKKR and [GAR-T5](https://github.com/castorini/pyserini/blob/master/docs/experiments-gar-t5.md) is detailed in [experiments-gar-t5.md](https://github.com/castorini/pyserini/blob/master/docs/experiments-gar-t5.md#hybrid-sparse-dense-retrieval-with-dkrr)

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2022-12-23 (commit [`90676b`](https://github.com/castorini/pyserini/commit/90676b351b47585084aa8136265d02a67ced3803))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2023-01-10 (commit [`7dafc4`](https://github.com/castorini/pyserini/commit/7dafc4f918bd44ada3771a5c81692ab19cc2cae9))

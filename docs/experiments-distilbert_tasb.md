# Pyserini: Reproducing DistilBERT KD TASB Results

This guide provides instructions to reproduce the DistilBERT KD TASB dense retrieval model on the MS MARCO passage ranking task, described in the following paper:

> Sebastian Hofstätter, Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin, Allan Hanbury. [Efficiently Teaching an Effective Dense Retriever with Balanced Topic Aware Sampling.](https://arxiv.org/abs/2104.06967) _SIGIR 2021_.

Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

Dense retrieval, with brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
                             --encoded-queries distilbert_tas_b-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.bf.tsv \
                             --output-format msmarco
```

Replace `--encoded-queries` with `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` for on-the-fly query encoding.

To evaluate:


```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.distilbert-dot-tas_b-b256.bf.tsv
#####################
MRR @10: 0.3443
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.distilbert-dot-tas_b-b256.bf.tsv --output runs/run.msmarco-passage.distilbert-dot-tas_b-b256.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.distilbert-dot-tas_b-b256.bf.trec
map                     all     0.3514
recall_1000             all     0.9771
```

## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-05-28 (commit [`102ed2`](https://github.com/castorini/pyserini/commit/102ed2b2e8770978e4b3e09804913dcffb63c4a7))

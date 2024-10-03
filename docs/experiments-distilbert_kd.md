# Pyserini: Reproducing DistilBERT KD Results

This guide provides instructions to reproduce the DistilBERT KD dense retrieval model on the MS MARCO passage ranking task, described in the following paper:

> Sebastian Hofstätter, Sophia Althammer, Michael Schröder, Mete Sertkan, and Allan Hanbury. [Improving Efficient Neural Ranking Models with Cross-Architecture Knowledge Distillation.](https://arxiv.org/abs/2010.02666) arXiv:2010.02666, October 2020. 

Note that we often observe minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

Dense retrieval, with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index msmarco-v1-passage.distilbert-dot-margin-mse-t2 \
  --topics msmarco-passage-dev-subset \
  --encoded-queries distilbert_kd-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output-format msmarco \
  --batch-size 512 --threads 16
```

Replace `--encoded-queries` with `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` for on-the-fly query encoding.

To evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv
```

Results:

```
#####################
MRR @10: 0.3251
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.tsv \
  --output runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
  runs/run.msmarco-passage.distilbert-dot-margin_mse-t2.trec
```

Results:

```
map                     all     0.3309
recall_1000             all     0.9553
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-26 (commit [`854c19`](https://github.com/castorini/pyserini/commit/854c1930ba00819245c0a9fbcf2090ce14db4db0))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2022-12-23 (commit [`0c495c`](https://github.com/castorini/pyserini/commit/0c495cf2999dda980eb1f85efa30a4323cef5855))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2023-01-10 (commit [`7dafc4`](https://github.com/castorini/pyserini/commit/7dafc4f918bd44ada3771a5c81692ab19cc2cae9))

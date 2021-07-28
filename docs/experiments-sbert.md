# Pyserini: Reproducing SBERT Results

This guide provides instructions to reproduce the SBERT dense retrieval models for MS MARCO passage ranking (v3) described [here](https://github.com/UKPLab/sentence-transformers/blob/master/docs/pretrained-models/msmarco-v3.md).

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

Dense retrieval, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-sbert-bf \
                             --encoded-queries sbert-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.sbert.bf.tsv \
                             --output-format msmarco
```

Replace `--encoded-queries` by `--encoder sentence-transformers/msmarco-distilbert-base-v3` for on-the-fly query encoding.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.tsv
#####################
MRR @10: 0.3314
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.sbert.bf.tsv --output runs/run.msmarco-passage.sbert.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.trec
map                     all     0.3373
recall_1000             all     0.9558
```

Hybrid retrieval with dense-sparse representations (without document expansion):
- dense retrieval with SBERT, brute force index.
- sparse retrieval with BM25 `msmarco-passage` (i.e., default bag-of-words) index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-sbert-bf \
                                    --encoded-queries sbert-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.015  \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.sbert.bf.bm25.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

Replace `--encoded-queries` by `--encoder sentence-transformers/msmarco-distilbert-base-v3` for on-the-fly query encoding.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.bm25.tsv
#####################
MRR @10: 0.3379
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.sbert.bf.bm25.tsv --output runs/run.msmarco-passage.sbert.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.bm25.trec
map                     all     0.3445
recall_1000             all     0.9659
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-02 (commit [`8dcf99`](https://github.com/castorini/pyserini/commit/8dcf99982a7bfd447ce9182ff219a9dad2ddd1f2))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-26 (commit [`854c19`](https://github.com/castorini/pyserini/commit/854c1930ba00819245c0a9fbcf2090ce14db4db0))

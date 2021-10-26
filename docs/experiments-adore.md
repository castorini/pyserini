# Pyserini: Reproducing ADORE Results

This guide provides instructions to reproduce the following dense retrieval work:

> Jingtao Zhan, Jiaxin Mao, Yiqun Liu, Jiafeng Guo, Min Zhang, Shaoping Ma. [Optimizing Dense Retrieval Model Training with Hard Negatives](https://arxiv.org/pdf/2104.08051.pdf)

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## MS MARCO Passage

**ADORE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-adore-bf \
                             --encoded-queries adore-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.adore.bf.tsv \
                             --output-format msmarco
```

The option `--encoded-queries` specifies the use of encoded queries (i.e., queries that have already been converted into dense vectors and cached).

Unfortunately, the "on-the-fly" query encoding, ie, convert text queries into dense vectors as part of the dense retrieval process is not available for this model. This is because the original ADORE implementation is based on an old version of transformers (`transformers=2.8.0`). Pyserini uses a higher version so that the base model (`roberta-base`) performs differently.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.adore.bf.tsv 
#####################
MRR @10: 0.34661947969254514
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.adore.bf.tsv --output runs/run.msmarco-passage.adore.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.ance.bf.trec
map                   	all	0.3523
recall_1000           	all	0.9688
```

## TREC DL2019 Passage

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dl19-passage  \
                             --index msmarco-passage-adore-bf \
                             --encoded-queries adore-dl19-passage \ 
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.dl19-passage.adore.bf.trec
```

Same as above, you cannot use the "on-the-fly" query encoding feature.

To evaluate:

```bash
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -m recall.1000 -l 2 dl19-passage runs/run.dl19-passage.adore.bf.trec
map                     all     0.4188
recall_1000             all     0.7759
ndcg_cut_10             all     0.6832
```

## TREC DL2020 Passage

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dl20  \
                             --index msmarco-passage-adore-bf \
                             --encoded-queries adore-dl20-passage \ 
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.dl20-passage.adore.bf.trec
```

Same as above, you cannot use the "on-the-fly" query encoding feature.

To evaluate:

```bash
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -m recall.1000 -l 2 dl20-passage runs/run.dl20-passage.adore.bf.trec
map                     all     0.4418
recall_1000             all     0.8151
ndcg_cut_10             all     0.6655
```

## Reproduction Log[*](reproducibility.md)


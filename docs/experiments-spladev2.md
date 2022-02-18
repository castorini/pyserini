# Pyserini: SPLADEv2 on MS MARCO V1 Passage Ranking

This page describes how to reproduce with Pyserini the DistilSPLADE-max experiments in the following paper:

> Thibault Formal, Carlos Lassance, Benjamin Piwowarski, Stéphane Clinchant. [SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval.](https://arxiv.org/abs/2109.10086) _arXiv:2109.10086_.

Here, we start with a version of the MS MARCO passage corpus that has already been processed with SPLADE, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved. As SPLADE weights are given in fp16, they have been converted to integer by taking the round of weight*100.

## Data Prep

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with SPLADE processing:

```bash
# Alternate mirrors of the same data, pick one:
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-distill-splade-max.tar -P collections/
wget https://vault.cs.uwaterloo.ca/s/poCLbJDMm7JxwPk/download -O collections/msmarco-passage-distill-splade-max.tar

tar xvf collections/msmarco-passage-distill-splade-max.tar -C collections/
```

To confirm, `msmarco-passage-distill-splade-max.tar` is 9.9 GB and has MD5 checksum `95b89a7dfd88f3685edcc2d1ffb120d1`.

## Indexing

We can now index these documents:

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/msmarco-passage-distill-splade-max \
  --index indexes/lucene-index.msmarco-passage-distill-splade-max \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized
```

The important indexing options to note here are `--impact --pretokenized`: the first tells Anserini not to encode BM25 doc lengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the SPLADEv2 tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 30 minutes.

## Retrieval

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries.
First, fetch the MS MARCO passage ranking dev set queries: 

```bash
# Alternate mirrors of the same data, pick one:
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-passage.dev-subset.distill-splade-max.tsv.gz -P collections/
wget https://vault.cs.uwaterloo.ca/s/DrL4HLqgmT6orJL/download -O collections/topics.msmarco-passage.dev-subset.distill-splade-max.tsv.gz
```

The MD5 checksum of the topics file is `621a58df9adfbba8d1a23e96d8b21cb7`.

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-passage-distill-splade-max` in the command below.

We can now run retrieval:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-distill-splade-max \
  --topics collections/topics.msmarco-passage.dev-subset.distill-splade-max.tsv.gz \
  --output runs/run.msmarco-passage-distill-splade-max.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Note that the important option here is `--impact`, where we specify impact scoring.
A complete run can take around half an hour.

*Note from authors*: We are still investigating why it takes so long using Pyserini, while the same model (including distilbert query encoder forward pass in CPU) takes only **10 minutes** on similar hardware using a numba implementation for the inverted index and using sequential processing (only one query at a time).

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-distill-splade-max.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.36852691363078205
QueriesRanked: 6980
#####################
```

The final evaluation metric is very close to the one reported in the paper (0.368).

Alternatively, we can use one-the-fly query encoding.

First, download the model checkpoint from NAVER's [website](https://europe.naverlabs.com/research/machine-learning-and-optimization/splade-models/):

```bash
wget https://download-de.europe.naverlabs.com/Splade_Release_Jan22/distilsplade_max.tar.gz
tar -xvf distilsplade_max.tar.gz
mv distilsplade_max distill-splade-max
```

Then run retrieval with `--encoder distill-splade-max`:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-distill-splade-max \
  --topics msmarco-passage-dev-subset \
  --encoder distill-splade-max \
  --output runs/run.msmarco-passage-distill-splade-max.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

And then evaluate: 

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-distill-splade-max.tsv
```

The results should be something along these lines:

```
#####################
MRR @10: 0.3684321417201083
QueriesRanked: 6980
#####################
```

There might be small differences in score due to non-determinism in neural inference; see [these notes](reproducibility.md) for detail.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-10-05 (commit [`58d286c`](https://github.com/castorini/pyserini/commit/58d286c3f9fe845e261c271f2a0f514462844d97))
+ Results reproduced by [@MXueguang](https://github.com/MXueguang) on 2021-10-07 (commit [`5d05426`](https://github.com/castorini/pyserini/commit/5d05426e1b40c513c6fa739a236b9c025b1a62fd))
+ Results reproduced by [@prasys](https://github.com/prasys) on 2021-02-14 (commit [`3732c8e`](https://github.com/castorini/pyserini/commit/3732c8e3f1b72113a3961444b1ac37878afcbb64))

# Pyserini: DeepImpact on MS MARCO V1 Passage Ranking

This page describes how to reproduce the DeepImpact experiments in the following paper:

> Antonio Mallia, Omar Khattab, Nicola Tonellotto, and Torsten Suel. [Learning Passage Impacts for Inverted Indexes.](https://dl.acm.org/doi/10.1145/3404835.3463030) _SIGIR 2021_.

Here, we start with a version of the MS MARCO passage corpus that has already been processed with DeepImpact, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.

## Data Prep

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with DeepImpact processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-deepimpact.tar -P collections/

tar xvf collections/msmarco-passage-deepimpact.tar -C collections/
```

To confirm, `msmarco-passage-deepimpact.tar` is 3.6 GB and has MD5 checksum `fe827eb13ca3270bebe26b3f6b99f550`.

## Indexing

We can now index these docs:

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/msmarco-passage-deepimpact/ \
  --index indexes/lucene-index.msmarco-passage-deepimpact/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized
```

The important indexing options to note here are `--impact --pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the DeepImpact tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 15 minutes.

## Retrieval

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-passage-deepimpact` in the command below.

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries, which are already included in Pyserini.
We can run retrieval as follows:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-deepimpact/ \
  --topics msmarco-passage-dev-subset-deepimpact \
  --output runs/run.msmarco-passage-deepimpact.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Note that the important option here is `--impact`, where we specify impact scoring.
A complete run should take around five minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-deepimpact.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.3252764133351524
QueriesRanked: 6980
#####################
```

The final evaluation metric is very close to the one reported in the paper (0.326).

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-14 (commit [`ed88e4c`](https://github.com/castorini/pyserini/commit/ed88e4c3ea9ce3bf71c06297c1768d93154d74a8))
+ Results reproduced by [@qiaoyf96](https://github.com/qiaoyf96) on 2021-10-01 (commit [`bebe9de`](https://github.com/castorini/pyserini/commit/bebe9de01cfd6e81ef46bd2ea7a7c3ca86b001ed))
+ Results reproduced by [@namespace-Pt](https://github.com/namespace-Pt) on 2021-12-07 (commit [`7249409`](https://github.com/castorini/pyserini/commit/7249409269095cd65259eb8a7c5131d3b9323068))

# Pyserini: DeepImpact for MS MARCO V1 Passage Ranking

This page describes how to reproduce the DeepImpact experiments in the following paper:

> Antonio Mallia, Omar Khattab, Nicola Tonellotto, and Torsten Suel. [Learning Passage Impacts for Inverted Indexes.](https://dl.acm.org/doi/10.1145/3404835.3463030) _SIGIR 2021_.

Here, we start with a version of the MS MARCO passage corpus that has already been processed with DeepImpact, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.

Note that Anserini provides [a comparable reproduction guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-deepimpact.md) based on Java.

## Data Prep

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with DeepImpact processing:

```bash
# Alternate mirrors of the same data, pick one:
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-deepimpact-b8.tar -P collections/
wget https://vault.cs.uwaterloo.ca/s/57AE5aAjzw2ox2n/download -O collections/msmarco-passage-deepimpact-b8.tar

tar xvf collections/msmarco-passage-deepimpact-b8.tar -C collections/
```

To confirm, `msmarco-passage-deepimpact-b8.tar` is ~3.6 GB and has MD5 checksum `3c317cb4f9f9bcd3bbec60f05047561a`.

## Indexing

We can now index these docs:

```bash
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-deepimpact-b8/ \
 -index indexes/lucene-index.msmarco-passage.deepimpact-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the DeepImpact tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 15 minutes.

## Retrieval

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries.
First, fetch the MS MARCO passage ranking dev set queries: 

```
# Alternate mirrors of the same data, pick one:
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-passage.dev-subset.deepimpact.tsv.gz -P collections/
wget https://vault.cs.uwaterloo.ca/s/NYibRJ9bXs5PspH/download -O collections/topics.msmarco-passage.dev-subset.deepimpact.tsv.gz
```
The MD5 checksum of the topics file is `88a2987d6a25b1be11c82e87677a262e`.

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-passage-deepimpact` in the command below.

We can now run retrieval:

```bash
python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.deepimpact.tsv.gz \
                          --index indexes/lucene-index.msmarco-passage.deepimpact-b8 \
                          --output runs/run.msmarco-passage.deepimpact-b8.tsv \
                          --impact \
                          --hits 1000 --batch 36 --threads 12 \
                          --output-format msmarco
```

Note that the important option here is `-impact`, where we specify impact scoring.
A complete run should take around five minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.deepimpact-b8.tsv
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

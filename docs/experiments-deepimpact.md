# Pyserini: DeepImpact for MS MARCO Passage Ranking

This page describes how to reproduce the DeepImpact experiments in the following paper:

> Antonio Mallia, Omar Khattab, Nicola Tonellotto, and Torsten Suel. [Learning Passage Impacts for Inverted Indexes.](https://dl.acm.org/doi/10.1145/3404835.3463030) _SIGIR 2021_.

Here, we start with a version of the MS MARCO passage corpus that has already been processed with DeepImpact, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.

Note that Anserini provides [a comparable reproduction guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-deepimpact.md) based on Java.
Here, we can get _exactly_ the same results from Python.


## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with DeepImpact processing:

```bash
wget https://git.uwaterloo.ca/jimmylin/deep-impact/raw/master/msmarco-passage-deepimpact-b8.tar.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/8xabiYom7nYJcB7/download -O collections/msmarco-passage-deepimpact-b8.tar.gz

tar -xzvf collections/msmarco-passage-deepimpact-b8.tar.gz -C collections/
```

To confirm, `msmarco-passage-deepimpact-b8.tar.gz` should have MD5 checksum of `8ea0ebdd707d5853a87940e5bdfd9b00`.


## Indexing

We can now index these docs:

```bash
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-deepimpact-b8/ \
 -index indexes/lucene-index.msmarco-passage-deepimpact-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 18 -storeRaw
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the DeepImpact tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 18 threads, per above), indexing takes around ten minutes.


## Retrieval

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries.
First, fetch the MS MARCO passage ranking dev set queries: 

```
wget https://git.uwaterloo.ca/jimmylin/deep-impact/raw/master/topics.msmarco-passage.dev-subset.deep-impact.tsv -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/py2CToTmaz6FoTq/download -O collections/topics.msmarco-passage.dev-subset.deep-impact.tsv
```

We can now run retrieval:

```bash
$ python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.deep-impact.tsv \
                            --index indexes/lucene-index.msmarco-passage-deepimpact-b8 \
                            --output runs/run.msmarco-passage-deepimpact-b8.tsv \
                            --impact \
                            --hits 1000 --batch 36 --threads 12 \
                            --output-format msmarco
```

Query evaluation is much slower than with bag-of-words BM25; a complete run can take around half an hour.
Note that the important option here is `-impact`, where we specify impact scoring.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-deepimpact-b8.tsv
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

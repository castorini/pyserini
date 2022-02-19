# Pyserini: uniCOIL w/ TILDE on MS MARCO V1 Passage Ranking

This page describes how to reproduce experiments using uniCOIL with TILDE document expansion on the MS MARCO passage corpus, as described in the following paper:

> Shengyao Zhuang and Guido Zuccon. [Fast Passage Re-ranking with Contextualized Exact Term
Matching and Efficient Passage Expansion.](https://arxiv.org/pdf/2108.08513) _arXiv:2108.08513_.

The original uniCOIL model is described here:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In the original uniCOIL paper, doc2query-T5 is used to perform document expansion, which is slow and expensive.
As an alternative, Zhuang and Zuccon proposed to use the TILDE model to expand the documents instead, resulting in a faster and cheaper process that is just as effective.
For details of how to use TILDE to expand documents, please refer to the [TILDE repo](https://github.com/ielab/TILDE).
For additional details on the original uniCOIL design (with doc2query-T5 expansion), please refer to the [COIL repo](https://github.com/luyug/COIL/tree/main/uniCOIL).

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL + TILDE, i.e., gone through document expansion and term re-weighting.
Thus, no neural inference is involved.

## Data Prep

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil-tilde-expansion.tar -P collections/

tar xvf collections/msmarco-passage-unicoil-tilde-expansion.tar -C collections/
```

To confirm, `msmarco-passage-unicoil-tilde-expansion.tar` is 3.9 GB and has MD5 checksum `1685aee10071441987ad87f2e91f1706`.

## Indexing

We can now index these docs:

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/msmarco-passage-unicoil-tilde-expansion/ \
  --index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized
```

The important indexing options to note here are `--impact --pretokenized`: the first tells Pyserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 25 minutes.

## Retrieval

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-passage-unicoil-tilde` in the command below.

We can now run retrieval using the `ielab/unicoil-tilde200-msmarco-passage` model available on Huggingface's model hub to encode the queries:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion \
  --topics msmarco-passage-dev-subset \
  --encoder ielab/unicoil-tilde200-msmarco-passage \
  --output runs/run.msmarco-passage-unicoil-tilde-expansion.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `--impact`, where we specify impact scoring. 
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run typically takes around 25 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-tilde-expansion.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.3495203984172459
QueriesRanked: 6980
#####################
```

There might be small differences in score due to non-determinism in neural inference; see [these notes](reproducibility.md) for detail.
The above score was obtained on Linux.

Alternatively, we can use pre-tokenized queries with pre-computed weights, which are already included in Pyserini.
We can run retrieval as follows:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion \
  --topics msmarco-passage-dev-subset-unicoil-tilde \
  --output runs/run.msmarco-passage-unicoil-tilde-expansion.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Here, we also specify `--impact` for impact scoring.
Since we're not applying neural inference over the queries, retrieval is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-tilde-expansion.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.34957184927457136
QueriesRanked: 6980
#####################
```

Note that in this case, the results should be deterministic.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-09-08 (commit [`f026b87`](https://github.com/castorini/pyserini/commit/f026b871e0e581743fcb09d1eb309e9698767a8d))
+ Results reproduced by [@MXueguang](https://github.com/MXueguang) on 2021-09-10 (commit [`c71a69e`](https://github.com/castorini/pyserini/commit/c71a69e2dfad487e492b9b2b3c21b9b9c2e7cdb5))

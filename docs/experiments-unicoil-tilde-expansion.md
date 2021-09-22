# Pyserini: uniCOIL (w/ TILDE) for MS MARCO (V1) Passage Ranking

This page describes how to reproduce experiments using uniCOIL with TILDE document expansion on the MS MARCO passage corpus, as described in the following paper:

> Shengyao Zhuang and Guido Zuccon. [Fast Passage Re-ranking with Contextualized Exact Term
Matching and Efficient Passage Expansion.](https://arxiv.org/pdf/2108.08513) _arXiv:2108.08513_.

The original uniCOIL model is described here:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In the original uniCOIL paper, doc2query-T5 is used to perform document expansion, which is slow and expensive.
As an alternative, Zhuang and Zuccon proposed to use the TILDE model to expand the documents instead, resulting in a faster and cheaper process that is just as effective.
For details of how to use TILDE to expand documents, please refer to the [TIDLE repo](https://github.com/ielab/TILDE).
For additional details on the original uniCOIL design (with doc2query-T5 expansion), please refer to the [COIL repo](https://github.com/luyug/COIL/tree/main/uniCOIL).

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL + TILDE, i.e., gone through document expansion and term re-weighting.
Thus, no neural inference is involved.

## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://git.uwaterloo.ca/jimmylin/unicoil/-/raw/master/msmarco-passage-unicoil-tilde-expansion-b8.tar -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/6LECmLdiaBoPwrL/download -O collections/msmarco-passage-unicoil-tilde-expansion-b8.tar

tar -xvf collections/msmarco-passage-unicoil-tilde-expansion-b8.tar -C collections/
```

To confirm, `msmarco-passage-unicoil-tilde-expansion-b8.tar` is around 4 GB and should have an MD5 checksum of `be0a786033140ebb7a984a3e155c19ae`.

## Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-unicoil-tilde-expansion-b8/ \
 -index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Pyserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around half an hour.

## Retrieval

We can now run retrieval:

```bash
python -m pyserini.search --topics msmarco-passage-dev-subset \
                          --encoder ielab/unicoil-tilde200-msmarco-passage \
                          --index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8 \
                          --output runs/run.msmarco-passage-unicoil-tilde-expansion-b8.tsv \
                          --impact \
                          --hits 1000 --batch 32 --threads 12 \
                          --output-format msmarco
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `-impact`, where we specify impact scoring. 
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run typically takes around 20 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-tilde-expansion-b8.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.3495203984172459
QueriesRanked: 6980
#####################
```

There might be small differences in score due to platform differences in neural inference.
The above score was obtained on Linux; macOS results may be slightly different.

Alternatively, we can use pre-tokenized queries with pre-computed weights.
First, fetch the queries:

```
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-passage.dev-subset.unicoil-tilde-expansion.tsv.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/GZEPQkNQGoszHTx/download -O collections/topics.msmarco-passage.dev-subset.unicoil-tilde-expansion.tsv.gz
```

The MD5 checksum of the topics file should be `860267a6f6c72f22d006dd5c1c20f885`.

We can now run retrieval:

```bash
python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.unicoil-tilde-expansion.tsv.gz \
                          --index indexes/lucene-index.msmarco-passage-unicoil-tilde-expansion-b8 \
                          --output runs/run.msmarco-passage-unicoil-tilde-expansion-b8.tsv \
                          --impact \
                          --hits 1000 --batch 32 --threads 12 \
                          --output-format msmarco
```

Here, we also specify `-impact` for impact scoring.
Since we're not applying neural inference over the queries, retrieval is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-tilde-expansion-b8.tsv
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

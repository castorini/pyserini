# Pyserini: SPLADE_v2 for MS MARCO Passage Ranking

This page describes how to reproduce the DistilSPLADE-max experiments in the following paper:

> Thibault Formal, Carlos Lassance, Benjamin Piwowarski, Stéphane Clinchant. [SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval.](https://arxiv.org/abs/2109.10086).

Here, we start with a version of the MS MARCO passage corpus that has already been processed with SPLADE, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved. As the weights of splade are given in fp16, they have been converted to integer by taking the round of weight*100.


## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with SPLADE processing:

```bash
#Provisory mirror
wget https://www.dropbox.com/s/459eb572gp73ewe/msmarco-passage-DistilSPLADE-max.tar.gz?dl=0 -O collections/msmarco-passage-DistilSPLADE-max.tar.gz


tar -xzvf collections/msmarco-passage-DistilSPLADE-max.tar.gz -C collections/
```

To confirm, `msmarco-passage-DistilSPLADE-max.tar.gz` should have MD5 checksum of `e0b24bbadac7af138cc0e46df2159659`.


## Indexing

We can now index these docs:

```bash
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-DistilSPLADE-max/ \
 -index indexes/lucene-index.msmarco-passage-DistilSPLADE-max \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 18 -storeRaw
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the SPLADE tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 18 threads, per above), indexing takes around twenty minutes.


## Retrieval

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries.
First, fetch the MS MARCO passage ranking dev set queries: 

```
# Provisory mirror
wget https://www.dropbox.com/s/fwodo2uwrqpxfs2/topics.msmarco-passage.dev-subset.distilSPLADE-max.tsv?dl=0 -O collections/topics.msmarco-passage.dev-subset.distilSPLADE-max.tsv
```

We can now run retrieval:

```bash
$ python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.distilSPLADE-max.tsv \
                            --index indexes/lucene-index.msmarco-passage-DistilSPLADE-max \
                            --output runs/run.msmarco-passage-distilSPLADE-max.tsv \
                            --impact \
                            --hits 1000 --batch 36 --threads 12 \
                            --output-format msmarco
```

Query evaluation is much slower than with bag-of-words BM25; a complete run can take around half an hour. Note that the important option here is `-impact`, where we specify impact scoring.

*Note from authors*: We are still investigating why it takes so long using pyserini, the same model (including distilbert forward in CPU) takes only 10 minutes on similar hardware using a numba implementation for the inverted index and using sequential processing (only 1-query at a time).

The output is in MS MARCO output format, so we can directly evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-distilSPLADE-max.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.36852691363078205
QueriesRanked: 6980
#####################
```

The final evaluation metric is very close to the one reported in the paper (0.368).


## Reproduction Log[*](reproducibility.md)


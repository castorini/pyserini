# Pyserini: uniCOIL for MS MARCO Passage Ranking

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

Here, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.


## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://git.uwaterloo.ca/jimmylin/unicoil/-/raw/master/msmarco-passage-unicoil-b8.tar -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/Rm6fknT432YdBts/download -O collections/msmarco-passage-unicoil-b8.tar

tar -xvf collections/msmarco-passage-unicoil-b8.tar -C collections/
```

To confirm, `msmarco-passage-unicoil-b8.tar` should have MD5 checksum of `eb28c059fad906da2840ce77949bffd7`.


## Indexing

Release Soon, see Anserini for now

## Retrieval

To ensure that the tokenization in the index aligns exactly with the queries, we use pre-tokenized queries.
First, fetch the MS MARCO passage ranking dev set queries: 

```bash
wget https://git.uwaterloo.ca/jimmylin/unicoil/-/raw/master/topics.msmarco-passage.dev-subset.unicoil.tsv.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/QGoHeBm4YsAgt6H/download -O collections/topics.msmarco-passage.dev-subset.unicoil.tsv.gz

gzip -d collections/topics.msmarco-passage.dev-subset.unicoil.tsv.gz
```

We can now run retrieval:

```bash
$ python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.unicoil.tsv \
                            --index indexes/lucene-index.msmarco-passage-deepimpact-b8 \
                            --output runs/run.msmarco-passage-deepimpact-b8.tsv \
                            --impact \
                            --hits 1000 --batch 36 --threads 12 \
                            --output-format msmarco
```

Evaluate:
```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-deepimpact-b8.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.35155222404147896
QueriesRanked: 6980
#####################
```


## Reproduction Log[*](reproducibility.md)


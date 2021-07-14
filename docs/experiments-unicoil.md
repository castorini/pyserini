# Pyserini: uniCOIL for MS MARCO Passage Ranking

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

Note: This page is just exactly like [Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-unicoil.md), except you can do it from Python.

## Train & inference with uniCOIL
Here, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.
To see the details on how to train uniCOIL and do inference, please see [here](https://github.com/luyug/COIL/tree/main/uniCOIL).

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

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-unicoil-b8/ \
 -index indexes/lucene-index.msmarco-passage-unicoil-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12 -storeRaw -optimize
```

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
                            --index indexes/lucene-index.msmarco-passage-unicoil-b8 \
                            --output runs/run.msmarco-passage-unicoil-b8.tsv \
                            --impact \
                            --hits 1000 --batch 36 --threads 12 \
                            --output-format msmarco
```

Evaluate:
```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-b8.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.35155222404147896
QueriesRanked: 6980
#####################
```


## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-07-13 (commit [`228d5c9`](https://github.com/castorini/pyserini/commit/228d5c9c4ae0810702feccf8829b71682dd4955c))

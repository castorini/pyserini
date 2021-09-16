# Pyserini: uniCOIL (w/ doc2query-T5) for MS MARCO (V1)

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.
For details on how to train uniCOIL and perform inference, please see [this guide](https://github.com/luyug/COIL/tree/main/uniCOIL).

Note that Anserini provides [a comparable reproduction guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-unicoil.md) based on Java.
Here, we can get _exactly_ the same results from Python.

# Passage Ranking
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

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-unicoil-b8/ \
 -index indexes/lucene-index.msmarco-passage-unicoil-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12 -storeRaw -optimize
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 20 minutes.


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

Query evaluation is much slower than with bag-of-words BM25; a complete run can take around 15 minutes.
Note that the important option here is `-impact`, where we specify impact scoring.

The output is in MS MARCO output format, so we can directly evaluate:

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

# Document Ranking
## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://www.dropbox.com/s/86f1011xb92adbk/msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar.gz -P collections/

tar -xvf collections/msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar.gz -C collections/
```

To confirm, `msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar.gz` should have MD5 checksum of `a1c95132830906b599d137f28089ceae`.

## Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-doc-per-passage-expansion-unicoil-d2q-b8/ \
 -index indexes/lucene-index.msmarco-doc-unicoil-d2q-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 72 -optimize
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 20 minutes.

## Retrieval
We can now run retrieval:

```bash
$ python -m pyserini.search --topics msmarco-doc-dev \
                            --index indexes/lucene-index.msmarco-doc-unicoil-d2q-b8 \
                            --encoder castorini/unicoil-d2q-msmarco-passage \
                            --output runs/run.msmarco-doc-unicoil-d2q-b8.tsv \
                            --impact \
                            --hits 1000 --batch 36 --threads 12 \
                            --max-passage --max-passage-hits 100 \
                            --output-format msmarco
```


Query evaluation is much slower than with bag-of-words BM25; a complete run can take around 30 minutes.
Note that the important option here is `-impact`, where we specify impact scoring.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc-unicoil-d2q-b8.tsv
```

The results should be as follows:

```
#####################
MRR @100: 0.3530641289682811
QueriesRanked: 5193
#####################
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-07-13 (commit [`228d5c9`](https://github.com/castorini/pyserini/commit/228d5c9c4ae0810702feccf8829b71682dd4955c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-14 (commit [`ed88e4c`](https://github.com/castorini/pyserini/commit/ed88e4c3ea9ce3bf71c06297c1768d93154d74a8))

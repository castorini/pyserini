# Pyserini: uniCOIL (w/ doc2query-T5) for MS MARCO (V1)

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.
For details on how to train uniCOIL and perform inference, please see [this guide](https://github.com/luyug/COIL/tree/main/uniCOIL).

Note that Anserini provides [a comparable reproduction guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-unicoil.md) based on Java.

## Passage Ranking

### Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil-b8.tar -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/Rm6fknT432YdBts/download -O collections/msmarco-passage-unicoil-b8.tar

tar -xvf collections/msmarco-passage-unicoil-b8.tar -C collections/
```

To confirm, `msmarco-passage-unicoil-b8.tar` should have MD5 checksum of `eb28c059fad906da2840ce77949bffd7`.

### Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-passage-unicoil-b8/ \
 -index indexes/lucene-index.msmarco-passage-unicoil-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 20 minutes.

### Retrieval

We can now run retrieval:

```bash
python -m pyserini.search --topics msmarco-passage-dev-subset \
                          --encoder castorini/unicoil-d2q-msmarco-passage \
                          --index indexes/lucene-index.msmarco-passage-unicoil-b8 \
                          --output runs/run.msmarco-passage-unicoil-b8.tsv \
                          --impact \
                          --hits 1000 --batch 36 --threads 12 \
                          --output-format msmarco
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `-impact`, where we specify impact scoring.
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run can take around 30 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-b8.tsv
```

The results should be something along these lines:

```
#####################
MRR @10: 0.3508734138354477
QueriesRanked: 6980
#####################
```

There might be small differences in score due to platform differences in neural inference.
The above score was obtained on Linux; macOS results may be slightly different.

Alternatively, we can use pre-tokenized queries with pre-computed weights.
First, fetch the MS MARCO passage ranking dev set queries:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-passage.dev-subset.unicoil.tsv.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/QGoHeBm4YsAgt6H/download -O collections/topics.msmarco-passage.dev-subset.unicoil.tsv.gz
```

The MD5 checksum of the topics file is `1af1da05ae5fe0b9d8ddf2d143b6e7f8`.

We can now run retrieval:

```bash
python -m pyserini.search --topics collections/topics.msmarco-passage.dev-subset.unicoil.tsv.gz \
                          --index indexes/lucene-index.msmarco-passage-unicoil-b8 \
                          --output runs/run.msmarco-passage-unicoil-b8.tsv \
                          --impact \
                          --hits 1000 --batch 36 --threads 12 \
                          --output-format msmarco
```

Here, we also specify `-impact` for impact scoring.
Since we're not applying neural inference over the queries, speed is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage-unicoil-b8.tsv
```

The results should be as follows:

```
#####################
MRR @10: 0.35155222404147896
QueriesRanked: 6980
#####################
```

Note that in this case, the results should be deterministic.

## Document Ranking

### Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/ZmF6SKpgMZJYXd6/download -O collections/msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar

tar -xvf collections/msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar -C collections/
```

To confirm, `msmarco-doc-per-passage-expansion-unicoil-d2q-b8.tar` should have MD5 checksum of `88f365b148c7702cf30c0fb95af35149`.

### Indexing

We can now index these docs:

```
python -m pyserini.index -collection JsonVectorCollection \
 -input collections/msmarco-doc-per-passage-expansion-unicoil-d2q-b8/ \
 -index indexes/lucene-index.msmarco-doc-unicoil-d2q-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12
```

The important indexing options to note here are `-impact -pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around an hour.

### Retrieval

We can now run retrieval:

```bash
python -m pyserini.search --topics msmarco-doc-dev \
                          --encoder castorini/unicoil-d2q-msmarco-passage \
                          --index indexes/lucene-index.msmarco-doc-unicoil-d2q-b8 \
                          --output runs/run.msmarco-doc-unicoil-d2q-b8.tsv \
                          --impact \
                          --hits 1000 --batch 36 --threads 12 \
                          --max-passage --max-passage-hits 100 \
                          --output-format msmarco
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `-impact`, where we specify impact scoring.
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run can take around 40 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc-unicoil-d2q-b8.tsv
```

The results should be something along these lines:

```
#####################
MRR @100: 0.3530641289682811
QueriesRanked: 5193
#####################
```

There might be small differences in score due to platform differences in neural inference.
The above score was obtained on Linux; macOS results may be slightly different.

Alternatively, we can use pre-tokenized queries with pre-computed weights.
First, fetch the MS MARCO passage ranking dev set queries:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/topics.msmarco-doc.dev.unicoil.tsv.gz -P collections/

# Alternate mirror
wget https://vault.cs.uwaterloo.ca/s/6D5JtJQxYpPbByM/download -O collections/topics.msmarco-doc.dev.unicoil.tsv.gz
```

The MD5 checksum of the topics file is `40e5f64500272ecde270e55beecd5e94`.

We can now run retrieval:

```bash
python -m pyserini.search --topics collections/topics.msmarco-doc.dev.unicoil.tsv.gz \
                          --index indexes/lucene-index.msmarco-doc-unicoil-d2q-b8 \
                          --output runs/run.msmarco-doc-unicoil-d2q-b8.tsv \
                          --impact \
                          --hits 1000 --batch 36 --threads 12 \
                          --max-passage --max-passage-hits 100 \
                          --output-format msmarco
```

Here, we also specify `-impact` for impact scoring.
Since we're not applying neural inference over the queries, speed is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc-unicoil-d2q-b8.tsv
```

The results should be as follows:

```
#####################
MRR @100: 0.352997702662614
QueriesRanked: 5193
#####################
```

Note that in this case, the results should be deterministic.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-07-13 (commit [`228d5c9`](https://github.com/castorini/pyserini/commit/228d5c9c4ae0810702feccf8829b71682dd4955c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-14 (commit [`ed88e4c`](https://github.com/castorini/pyserini/commit/ed88e4c3ea9ce3bf71c06297c1768d93154d74a8))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-09-17 (commit [`79eb5cf`](https://github.com/castorini/pyserini/commit/79eb5cf49d50443efc75c718bcf7c7a887ec176f))
+ Results reproduced by [@mayankanand007](https://github.com/mayankanand007) on 2021-09-18 (commit [`331dfe7`](https://github.com/castorini/pyserini/commit/331dfe7b2801cca09fbbb971b017073bf6f726ad))
+ Results reproduced by [@apokali](https://github.com/apokali) on 2021-09-23 (commit [`82f8422`](https://github.com/castorini/pyserini/commit/82f842218f8c5c7c451b2e463774d7bdf6bc0653))

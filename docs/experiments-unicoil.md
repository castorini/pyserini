# Pyserini: uniCOIL w/ doc2query-T5 on MS MARCO V1

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

In this guide, we start with a version of the MS MARCO passage corpus that has already been processed with uniCOIL, i.e., gone through document expansion and term reweighting.
Thus, no neural inference is involved.
For details on how to train uniCOIL and perform inference, please see [this guide](https://github.com/luyug/COIL/tree/main/uniCOIL).

## Passage Ranking

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

### Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-passage-unicoil.tar -P collections/

tar xvf collections/msmarco-passage-unicoil.tar -C collections/
```

To confirm, `msmarco-passage-unicoil.tar` is 3.4 GB and has MD5 checksum `78eef752c78c8691f7d61600ceed306f`.

### Indexing

We can now index these docs:

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/msmarco-passage-unicoil/ \
  --index indexes/lucene-index.msmarco-passage-unicoil/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized
```

The important indexing options to note here are `--impact --pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around 15 minutes.

### Retrieval

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-v1-passage-unicoil` in the command below.

We can now run retrieval using the `castorini/unicoil-msmarco-passage` model available on Huggingface's model hub to encode the queries:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-unicoil/ \
  --topics msmarco-passage-dev-subset \
  --encoder castorini/unicoil-msmarco-passage \
  --output runs/run.msmarco-passage.unicoil.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `--impact`, where we specify impact scoring.
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run typically takes around 30 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.unicoil.tsv
```

The results should be something along these lines:

```
#####################
MRR @10: 0.3508734138354477
QueriesRanked: 6980
#####################
```

There might be small differences in score due to non-determinism in neural inference; see [these notes](reproducibility.md) for detail.
The above score was obtained on Linux.

Alternatively, we can use pre-tokenized queries with pre-computed weights, which are already included in Pyserini.
We can run retrieval as follows:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-passage-unicoil/ \
  --topics msmarco-passage-dev-subset-unicoil-d2q \
  --output runs/run.msmarco-passage.unicoil.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact
```

Here, we also specify `--impact` for impact scoring.
Since we're not applying neural inference over the queries, speed is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.unicoil.tsv
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

> You can skip the data prep and indexing steps if you use our pre-built indexes. Skip directly down to the "Retrieval" section below.

### Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO passage dataset with uniCOIL processing:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/msmarco-doc-segmented-unicoil.tar -P collections/

tar xvf collections/msmarco-doc-segmented-unicoil.tar -C collections/
```

To confirm, `msmarco-doc-segmented-unicoil.tar` is 19 GB and has MD5 checksum `6a00e2c0c375cb1e52c83ae5ac377ebb`.

### Indexing

We can now index these docs:

```bash
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/msmarco-doc-segmented-unicoil/ \
  --index indexes/lucene-index.msmarco-doc-segmented-unicoil/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized
```

The important indexing options to note here are `--impact --pretokenized`: the first tells Anserini not to encode BM25 doclengths into Lucene's norms (which is the default) and the second option says not to apply any additional tokenization on the uniCOIL tokens.

The indexing speed may vary; on a modern desktop with an SSD (using 12 threads, per above), indexing takes around an hour.

### Retrieval

> If you've skipped the data prep and indexing steps and wish to directly use our pre-built indexes, use `--index msmarco-v1-doc-segmented-unicoil` in the command below.

We can now run retrieval:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-doc-segmented-unicoil \
  --topics msmarco-doc-dev \
  --encoder castorini/unicoil-msmarco-passage \
  --output runs/run.msmarco-doc-segmented-unicoil.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 --max-passage --max-passage-hits 100 \
  --impact
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `--impact`, where we specify impact scoring.
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.
A complete run can take around 40 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc-segmented-unicoil.tsv
```

The results should be something along these lines:

```
#####################
MRR @100: 0.3530641289682811
QueriesRanked: 5193
#####################
```

There might be small differences in score due to non-determinism in neural inference; see [these notes](reproducibility.md) for detail.
The above score was obtained on Linux.

Alternatively, we can use pre-tokenized queries with pre-computed weights, which are already included in Pyserini.
We can run retrieval as follows:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index.msmarco-doc-segmented-unicoil \
  --topics msmarco-doc-dev-unicoil \
  --output runs/run.msmarco-doc-segmented-unicoil.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 --max-passage --max-passage-hits 100 \
  --impact
```

Here, we also specify `--impact` for impact scoring.
Since we're not applying neural inference over the queries, speed is faster, typically less than 10 minutes.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc-segmented-unicoil.tsv
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
+ Results reproduced by [@yuki617](https://github.com/yuki617) on 2022-02-08 (commit [`e03e068`](https://github.com/castorini/pyserini/commit/e03e06880ad4f6d67a1666c1dd45ce4250adc95d))

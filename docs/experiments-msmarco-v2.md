# Pyserini: BM25 Baselines for the MS MARCO V2 Collections

This guide contains instructions for running baselines on the MS MARCO V2 passage and document test collections,
which mirrors a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md) except that everything is in Python here (no Java).
To reduce duplication of content, this guide will refer to the Anserini for shared instructions and descriptions.

## Data Prep

These instructions are exactly the same as in the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).

## Passage Collection

This is the minimal indexing command:

```
python -m pyserini.index --collection MsMarcoV2PassageCollection \
                         --generator DefaultLuceneDocumentGenerator \
                         --input collections/msmarco_v2_passage \
                         --index indexes/lucene-index.msmarco-v2-passage \
                         --threads 12
```

Adjust `-threads` as appropriate.
Different configurations (`-storePositions`, `-storeDocvectors`, `-storeRaw`) support different features, but require different amounts of disk space; for the detailed tradeoffs, see the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
The above minimal index should be ~11 GB.

Perform a run on the dev queries:

```
python -m pyserini.search --index indexes/lucene-index.msmarco-v2-passage \
                          --topics msmarco-v2-passage-dev \
                          --output runs/run.msmarco-v2-passage.dev.txt \
                          --bm25 \
                          --hits 1000 \
                          --batch-size 36 \
                          --threads 12
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-passage-dev runs/run.msmarco-v2-passage.dev.txt
Results:
map                   	all	0.0709
recip_rank            	all	0.0719

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 msmarco-v2-passage-dev runs/run.msmarco-v2-passage.dev.txt
Results:
recall_100            	all	0.3397
recall_1000           	all	0.5733
```

These results should be the same as in the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
To run on the `dev2` queries, just change everything from `msmarco-v2-passage-dev` to `msmarco-v2-passage-dev2`.

## Passage Collection (Augmented)

Refer to the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md) on how this collection was prepared.
This is the minimal indexing command:

```
python -m pyserini.index --collection MsMarcoV2PassageCollection \
                         --generator DefaultLuceneDocumentGenerator \
                         --input collections/msmarco_v2_passage_augmented \
                         --index indexes/lucene-index.msmarco-v2-passage-augmented \
                         --threads 12
```

Adjust `-threads` as appropriate.
Different configurations (`-storePositions`, `-storeDocvectors`, `-storeRaw`) support different features, but require different amounts of disk space; for the detailed tradeoffs, see the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
The above minimal index should be ~19 GB.

Perform a run on the dev queries:

```
python -m pyserini.search --index indexes/lucene-index.msmarco-v2-passage-augmented \
                          --topics msmarco-v2-passage-dev \
                          --output runs/run.msmarco-v2-passage-augmented.dev.txt \
                          --bm25 \
                          --hits 1000 \
                          --batch-size 36 \
                          --threads 12
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-passage-dev runs/run.msmarco-v2-passage-augmented.dev.txt
Results:
map                   	all	0.0863
recip_rank            	all	0.0872

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 msmarco-v2-passage-dev runs/run.msmarco-v2-passage-augmented.dev.txt
Results:
recall_100            	all	0.4030
recall_1000           	all	0.6925
```

These results should be the same as in the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
To run on the `dev2` queries, just change everything from `msmarco-v2-passage-dev` to `msmarco-v2-passage-dev2`.

## Document Collection

This is the minimal indexing command:

```
python -m pyserini.index --collection MsMarcoV2DocCollection \
                         --generator DefaultLuceneDocumentGenerator \
                         --input collections/msmarco_v2_doc \
                         --index indexes/lucene-index.msmarco-v2-doc \
                         --threads 12
```

Adjust `-threads` as appropriate.
Different configurations (`-storePositions`, `-storeDocvectors`, `-storeRaw`) support different features, but require different amounts of disk space; for the detailed tradeoffs, see the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
The above minimal index should be ~9.6 GB.

Perform a run on the dev queries:

```
python -m pyserini.search --index indexes/lucene-index.msmarco-v2-doc \
                          --topics msmarco-v2-doc-dev \
                          --output runs/run.msmarco-v2-doc.dev.txt \
                          --bm25 \
                          --hits 1000 \
                          --batch-size 36 \
                          --threads 12
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-doc-dev runs/run.msmarco-v2-doc.dev.txt
Results:
map                   	all	0.1552
recip_rank            	all	0.1572

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 msmarco-v2-doc-dev runs/run.msmarco-v2-doc.dev.txt
Results:
recall_100            	all	0.5956
recall_1000           	all	0.8054
```

These results should be the same as in the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
To run on the `dev2` queries, just change everything from `msmarco-v2-doc-dev` to `msmarco-v2-doc-dev2`.

## Document Collection (Segmented)

Refer to the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md) on how this collection was prepared.
This is the minimal indexing command:

```
python -m pyserini.index --collection MsMarcoV2DocCollection \
                         --generator DefaultLuceneDocumentGenerator \
                         --input collections/msmarco_v2_doc_segmented \
                         --index indexes/lucene-index.msmarco-v2-doc-segmented \
                         --threads 12
```

Adjust `-threads` as appropriate.
Different configurations (`-storePositions`, `-storeDocvectors`, `-storeRaw`) support different features, but require different amounts of disk space; for the detailed tradeoffs, see the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
The above minimal index should be ~27 GB.

Perform a run on the dev queries:

```bash
python -m pyserini.search --index indexes/lucene-index.msmarco-v2-doc-segmented \
                          --topics msmarco-v2-doc-dev \
                          --index indexes/lucene-index.msmarco-v2-doc-segmented  \
                          --output runs/run.msmarco-v2-doc-segmented.dev.txt \
                          --hits 10000 \
                          --batch 36 \
                          --threads 12 \
                          --max-passage-hits 1000 \
                          --max-passage
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-doc-dev runs/run.msmarco-v2-doc-segmented.dev.txt
Results:
map                   	all	0.1875
recip_rank            	all	0.1896

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 msmarco-v2-doc-dev runs/run.msmarco-v2-doc-segmented.dev.txt
Results:
recall_100            	all	0.6555
recall_1000           	all	0.8542
```

These results should be the same as in the [Anserini guide](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md).
To run on the `dev2` queries, just change everything from `msmarco-v2-doc-dev` to `msmarco-v2-doc-dev2`.

## Reproduction Log[*](reproducibility.md)


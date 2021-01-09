# Pyserini: BM25 Baseline for MS MARCO Document Retrieval

This guide contains instructions for running BM25 baselines on the [MS MARCO *document* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-doc.md), except that everything is in Python here (no Java).
Note that there is a separate guide for the [MS MARCO *passage* ranking task](experiments-msmarco-passage.md).

## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO document dataset:

```
mkdir collections/msmarco-doc

wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs.trec.gz -P collections/msmarco-doc

# Alternative mirror:
# wget https://www.dropbox.com/s/w6caao3sfx9nluo/msmarco-docs.trec.gz -P collections/msmarco-doc
```

To confirm, `msmarco-docs.trec.gz` should have MD5 checksum of `d4863e4f342982b51b9a8fc668b2d0c0`.

There's no need to uncompress the file, as Anserini can directly index gzipped files.
Build the index with the following command:

```
python -m pyserini.index -collection CleanTrecCollection \
 -generator DefaultLuceneDocumentGenerator -threads 1 -input collections/msmarco-doc \
 -index indexes/msmarco-doc/lucene-index.msmarco-doc.pos+docvectors+rawdocs \
 -storePositions -storeDocvectors -storeRaw >& logs/log.msmarco-doc.pos+docvectors+rawdocs &
```

Note that the indexing program simply dispatches command-line arguments to an underlying Java program, and so we use the Java single dash convention, e.g., `-index` and not `--index`.

On a modern desktop with an SSD, indexing takes around 40 minutes.
There should be a total of 3,213,835 documents indexed.


## Performing Retrieval on the Dev Queries

After indexing finishes, we can do a retrieval run.
The dev queries are already stored in our repo:

```
python -m pyserini.search --topics msmarco_doc_dev \
 --index indexes/msmarco-doc/lucene-index.msmarco-doc.pos+docvectors+rawdocs \
 --output runs/run.msmarco-doc.dev.bm25.txt --bm25
```

On a modern desktop with an SSD, the run takes around 12 minutes.

## Evaluating the Results

After the run completes, we can evaluate with `trec_eval`:

```
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -mrecall.1000 tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/run.msmarco-doc.dev.bm25.txt
map                   	all	0.2310
recall_1000           	all	0.8856
```

Let's compare to the baselines provided by Microsoft.
First, download:

```
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-top100.gz -P runs
gunzip runs/msmarco-docdev-top100.gz
```

Then, run `trec_eval` to compare.
Note that to be fair, we restrict evaluation to top 100 hits per topic (which is what Microsoft provides):

```
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -M 100 tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/msmarco-docdev-top100
map                   	all	0.2219

$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -M 100 tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/run.msmarco-doc.dev.bm25.txt
map                   	all	0.2303
```

We see that "out of the box" Anserini is already better!

## Replication Log

+ Results replicated by [@JeffreyCA](https://github.com/JeffreyCA) on 2020-09-14 (commit [`49fd7cb`](https://github.com/castorini/pyserini/commit/49fd7cb8fd802493dc34f5cb33767d2e72e19f13))
+ Results replicated by [@jhuang265](https://github.com/jhuang265) on 2020-09-14 (commit [`2ed2acc`](https://github.com/castorini/pyserini/commit/2ed2acc62e445e3e887c6cf853ccc0b0b3b57534))
+ Results replicated by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2020-11-12 (commit [`55c3dbc`](https://github.com/castorini/pyserini/commit/55c3dbc607d72b5318bff14ee4f89dc73e019386))
+ Results replicated by [@rakeeb123](https://github.com/rakeeb123) on 2020-12-07 (commit [`3bcd4e5`](https://github.com/castorini/pyserini/commit/3bcd4e52beb327d55ae6d3c8f6bc94351a6d1449))
+ Results replicated by [@jrzhang12](https://github.com/jrzhang12) on 2021-01-03 (commit [`7caedfc`](https://github.com/castorini/pyserini/commit/7caedfc150f916de302297406c45dead27b475ba))
+ Results replicated by [@HEC2018](https://github.com/HEC2018) on 2021-01-04 (commit [`46a6d47`](https://github.com/castorini/pyserini/commit/46a6d472267a559152495d004c2a12f8e95e53f0))
+ Results replicated by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-08 (commit [`aeec31f`](https://github.com/castorini/pyserini/commit/aeec31fbe17d39ecf3081597b4832f5af57ea549))

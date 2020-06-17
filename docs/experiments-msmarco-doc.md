# Pyserini: BM25 Baseline for MS MARCO Document Retrieval

This guide contains instructions for running BM25 baselines on the [MS MARCO *doc* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-doc.md), except that everything is in Python here (no Java).
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
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -mrecall.1000 collections/msmarco-doc/queries-and-qrels/msmarco-docdev-qrels.tsv runs/run.msmarco-doc.dev.bm25.txt
map                   	all	0.2310
recall_1000           	all	0.8856
```

Let's compare to the baselines provided by Microsoft (note that to be fair, we restrict evaluation to top 100 hits per topic):

```
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -M 100 collections/msmarco-doc/queries-and-qrels/msmarco-docdev-qrels.tsv collections/msmarco-doc/queries-and-qrels/msmarco-docdev-top100
map                   	all	0.2219

$ tools/eval/trec_eval.9.0.4/trec_eval -c -mmap -M 100 collections/msmarco-doc/queries-and-qrels/msmarco-docdev-qrels.tsv runs/run.msmarco-doc.dev.bm25.txt
map                   	all	0.2303
```

We see that "out of the box" Anserini is already better!

## Replication Log

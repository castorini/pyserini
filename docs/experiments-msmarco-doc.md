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
The final log lines should look something like this:

```
2020-01-14 16:36:30,954 INFO  [main] index.IndexCollection (IndexCollection.java:851) - ============ Final Counter Values ============
2020-01-14 16:36:30,955 INFO  [main] index.IndexCollection (IndexCollection.java:852) - indexed:        3,213,835
2020-01-14 16:36:30,955 INFO  [main] index.IndexCollection (IndexCollection.java:853) - unindexable:            0
2020-01-14 16:36:30,955 INFO  [main] index.IndexCollection (IndexCollection.java:854) - empty:                  0
2020-01-14 16:36:30,955 INFO  [main] index.IndexCollection (IndexCollection.java:855) - skipped:                0
2020-01-14 16:36:30,955 INFO  [main] index.IndexCollection (IndexCollection.java:856) - errors:                 0
2020-01-14 16:36:30,961 INFO  [main] index.IndexCollection (IndexCollection.java:859) - Total 3,213,835 documents indexed in 00:45:32
```

## Performing Retrieval on the Dev Queries

Let's download the queries and qrels:

```
mkdir collections/msmarco-doc/queries-and-qrels
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-doctrain-queries.tsv.gz -P collections/msmarco-doc/queries-and-qrels
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-doctrain-top100.gz -P collections/msmarco-doc/queries-and-qrels
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-doctrain-qrels.tsv.gz -P collections/msmarco-doc/queries-and-qrels

wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-queries.tsv.gz -P collections/msmarco-doc/queries-and-qrels
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-top100.gz -P collections/msmarco-doc/queries-and-qrels
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-qrels.tsv.gz -P collections/msmarco-doc/queries-and-qrels

# Alternative mirrors:
# wget https://www.dropbox.com/s/p6k7ph7v0r400ab/msmarco-doctrain-queries.tsv.gz -P collections/msmarco-doc/queries-and-qrels
# wget https://www.dropbox.com/s/zyt1n2gpylt0dhj/msmarco-doctrain-top100.gz -P collections/msmarco-doc/queries-and-qrels
# wget https://www.dropbox.com/s/7xw812wpf4t3fpu/msmarco-doctrain-qrels.tsv.gz -P collections/msmarco-doc/queries-and-qrels
# wget https://www.dropbox.com/s/d5wcox23s17wpf1/msmarco-docdev-queries.tsv.gz -P collections/msmarco-doc/queries-and-qrels
# wget https://www.dropbox.com/s/vamkn5dppjhygm5/msmarco-docdev-top100.gz -P collections/msmarco-doc/queries-and-qrels
# wget https://www.dropbox.com/s/9ad6f8midcmlrrx/msmarco-docdev-qrels.tsv.gz -P collections/msmarco-doc/queries-and-qrels

gunzip collections/msmarco-doc/queries-and-qrels/*.gz
```

Here are the sizes:

```
$ wc collections/msmarco-doc/queries-and-qrels/*.tsv
    5193   20772  108276 collections/msmarco-doc/queries-and-qrels/msmarco-docdev-qrels.tsv
    5193   35787  220304 collections/msmarco-doc/queries-and-qrels/msmarco-docdev-queries.tsv
  367013 1468052 7539008 collections/msmarco-doc/queries-and-qrels/msmarco-doctrain-qrels.tsv
  367013 2551279 15480364 collections/msmarco-doc/queries-and-qrels/msmarco-doctrain-queries.tsv
  744412 4075890 23347952 total
```

There are indeed lots of training queries!
In this guide, to save time, we are only going to perform retrieval on the dev queries.
This can be accomplished as follows:

```
python -m pyserini.search --index indexes/msmarco-doc/lucene-index.msmarco-doc.pos+docvectors+rawdocs \
 --topicreader TsvInt --topics collections/msmarco-doc/queries-and-qrels/msmarco-docdev-queries.tsv \
 --output runs/run.msmarco-doc.dev.bm25.txt -bm25
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

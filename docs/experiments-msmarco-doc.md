# Anserini: BM25 Baselines for MS MARCO Doc Retrieval

This page contains instructions for running BM25 baselines on the [MS MARCO *document* ranking task](https://microsoft.github.io/msmarco/).
Note that there is a separate [MS MARCO *passage* ranking task](experiments-msmarco-passage.md).

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
nohup sh target/appassembler/bin/IndexCollection -collection CleanTrecCollection \
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
target/appassembler/bin/SearchCollection -topicreader TsvInt \
 -index indexes/msmarco-doc/lucene-index.msmarco-doc.pos+docvectors+rawdocs \
 -topics collections/msmarco-doc/queries-and-qrels/msmarco-docdev-queries.tsv \
 -output runs/run.msmarco-doc.dev.bm25.txt -bm25
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

## BM25 Tuning

It is well known that BM25 parameter tuning is important.
The above instructions use the Anserini (system-wide) default of `k1=0.9`, `b=0.4`.

Let's try to do better!
We tuned BM25 using the queries found [here](https://github.com/castorini/Anserini-data/tree/master/MSMARCO): these are five different sets of 10k samples from the training queries (using the `shuf` command).
Tuning was performed on each individual set (grid search, in tenth increments) and then we averaged parameter values across all five sets (this has the effect of regularization).
Here, we optimized for average precision (AP).
The tuned parameters using this approach are `k1=3.44`, `b=0.87`.

To perform a run with these parameters, issue the following command:

```
target/appassembler/bin/SearchCollection -topicreader TsvString \
 -index indexes/msmarco-doc/lucene-index.msmarco-doc.pos+docvectors+rawdocs \
 -topics collections/msmarco-doc/queries-and-qrels/msmarco-docdev-queries.tsv \
 -output runs/run.msmarco-doc.dev.bm25.tuned.txt -bm25 -bm25.k1 3.44 -bm25.b 0.87
```

Here's the comparison between the Anserini default and tuned parameters:

Setting                     | AP     | Recall@1000 |
:---------------------------|-------:|------------:|
Default (`k1=0.9`, `b=0.4`) | 0.2310 | 0.8856
Tuned (`k1=3.44`, `b=0.87`) | 0.2788 | 0.9326

As expected, BM25 tuning makes a big difference!

## Replication Log

+ Results replicated by [@edwinzhng](https://github.com/edwinzhng) on 2020-01-14 (commit [`3964169`](https://github.com/castorini/anserini/commit/3964169bf82a3783f9298907d9794f0bddf306f0))
+ Results replicated by [@nikhilro](https://github.com/nikhilro) on 2020-01-21 (commit [`631589e`](https://github.com/castorini/anserini/commit/631589e9e08326373f46555e007e6c302c19126d))
+ Results replicated by [@yuki617](https://github.com/yuki617) on 2020-03-29 (commit [`074723c`](https://github.com/castorini/anserini/commit/074723cbb10660fb9be2bfe6325739ab5fe0dd8d))
+ Results replicated by [@HangCui0510](https://github.com/HangCui0510) on 2020-04-23 (commit [`0ae567d`](https://github.com/castorini/anserini/commit/0ae567df5c8a70ac211efd958c9ca1ff609ff782))
+ Results replicated by [@x65han](https://github.com/x65han) on 2020-04-25 (commit [`f5496b9`](https://github.com/castorini/anserini/commit/f5496b905246084070f959e59626c6323210c3f2))
+ Results replicated by [@y276lin](https://github.com/y276lin) on 2020-04-26 (commit [`8f48f8e`](https://github.com/castorini/anserini/commit/8f48f8e40a37e5f6b5910a3a3b5c050a0f9be914))
+ Results replicated by [@stephaniewhoo](http://github.com/stephaniewhoo) on 2020-04-26 (commit [`8f48f8e`](https://github.com/castorini/anserini/commit/8f48f8e40a37e5f6b5910a3a3b5c050a0f9be914))
+ Results replicated by [@YimingDou](https://github.com/YimingDou) on 2020-05-14 (commit [`3b0a642`](https://github.com/castorini/anserini/commit/3b0a6420e49863d9fe5908cf6e99582eb2d2882e))
+ Results replicated by [@richard3983](https://github.com/richard3983) on 2020-05-14 (commit [`a65646f`](https://github.com/castorini/anserini/commit/a65646fe203bf5c9c32189a56082d6f4d3bc340d))
+ Results replicated by [@MXueguang](https://github.com/MXueguang) on 2020-05-20 (commit [`3b2751e`](https://github.com/castorini/anserini/commit/3b2751e2d02a9d530e1c3d30b91083faeece8982))
+ Results replicated by [@shaneding](https://github.com/shaneding) on 2020-05-23 (commit [`b6e0367`](https://github.com/castorini/anserini/commit/b6e0367ef4e2b4fce9d81c8397ef1188e35971e7))
+ Results replicated by [@kelvin-jiang](https://github.com/kelvin-jiang) on 2020-05-24 (commit [`b6e0367`](https://github.com/castorini/anserini/commit/b6e0367ef4e2b4fce9d81c8397ef1188e35971e7))
+ Results replicated by [@adamyy](https://github.com/adamyy) on 2020-05-28 (commit [`a1ecfa4`](https://github.com/castorini/anserini/commit/a1ecfa4aa38fb8a0cf41575d47629ba1c69228fb))
+ Results replicated by [@TianchengY](https://github.com/TianchengY) on 2020-05-28 (commit [`2947a16`](https://github.com/castorini/anserini/commit/2947a1622efae35637b83e321aba8e6fccd43489))
+ Results replicated by [@stariqmi](https://github.com/stariqmi) on 2020-05-28 (commit [`4914305`](https://github.com/castorini/anserini/commit/455169ea6a09f637817a6c4b4f6837dcc845f5f7))
+ Results replicated by [@justinborromeo](https://github.com/justinborromeo) on 2020-06-11 (commit[`7954eab`](https://github.com/castorini/anserini/commit/7954eab43f17bb8d254987d5873933c0b9596bb4))

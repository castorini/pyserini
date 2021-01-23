# Pyserini: BM25 Baseline for MS MARCO Document Retrieval

This guide contains instructions for running BM25 baselines on the [MS MARCO *document* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-doc.md), except that everything is in Python here (no Java).
Note that there is a separate guide for the [MS MARCO *passage* ranking task](experiments-msmarco-passage.md).

## Data Prep

The guide requires the [development installation](https://github.com/castorini/pyserini/#development-installation) for additional resource that are not shipped with the Python module; for the (more limited) runs that directly work from the Python module installed via `pip`, see [this guide](https://github.com/castorini/pyserini/blob/master/docs/pypi-replication.md).

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
 -index indexes/lucene-index-msmarco-doc -storePositions -storeDocvectors -storeRaw
```

Note that the indexing program simply dispatches command-line arguments to an underlying Java program, and so we use the Java single dash convention, e.g., `-index` and not `--index`.

On a modern desktop with an SSD, indexing takes around 40 minutes.
There should be a total of 3,213,835 documents indexed.

## Performing Retrieval on the Dev Queries

The 5193 queries in the development set are already stored in the repo.
Let's take a peek:

```bash
$ head tools/topics-and-qrels/topics.msmarco-doc.dev.txt
174249	does xpress bet charge to deposit money in your account
320792	how much is a cost to run disneyland
1090270	botulinum definition
1101279	do physicians pay for insurance from their salaries?
201376	here there be dragons comic
54544	blood diseases that are sexually transmitted
118457	define bona fides
178627	effects of detox juice cleanse
1101278	do prince harry and william have last names
68095	can hives be a sign of pregnancy
$ wc tools/topics-and-qrels/topics.msmarco-doc.dev.txt
    5193   35787  220304 tools/topics-and-qrels/topics.msmarco-doc.dev.txt
```

Each line contains a tab-delimited (query id, query) pair.
Conveniently, Pyserini already knows how to load and iterate through these pairs.
We can now perform retrieval using these queries:

```bash
python -m pyserini.search --topics msmarco_doc_dev \
 --index indexes/lucene-index-msmarco-doc \
 --output runs/run.msmarco-doc.bm25tuned.txt \
 --bm25 --msmarco --hits 100 --k1 4.46 --b 0.82
```

Here, we set the BM25 parameters to `k1=4.46`, `b=0.82` (tuned by grid search).
The option `--msmarco` says to generate output in the MS MARCO output format.
The option `--hits` specifies the number of documents to return per query.
Note that for the [MS MARCO Document Ranking Leaderboard](https://microsoft.github.io/MSMARCO-Document-Ranking-Submissions/leaderboard/), the official metric is MRR@100, so submissions should only return 100 hits per query. 

Retrieval speed will vary by hardware:
On a reasonably modern CPU with an SSD, we might get around 18 qps (queries per second), and so the entire run should finish in under five minutes (using a single thread).
We can perform multi-threaded retrieval by using the `--threads` and `--batch-size` arguments.
For example, setting `--threads 16 --batch-size 64` on a CPU with sufficient cores, the entire run will finish in under a minute.

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:

```bash
$ python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
   --run runs/run.msmarco-doc.bm25tuned.txt
#####################
MRR @100: 0.2770296928568702
QueriesRanked: 5193
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@100.
For that we first need to convert the run file into TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py \
   --input runs/run.msmarco-doc.bm25tuned.txt --output runs/run.msmarco-doc.bm25tuned.trec
```

And then run the `trec_eval` tool:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.100 -mmap \
   tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/run.msmarco-doc.bm25tuned.trec
map                   	all	0.2770
recall_100            	all	0.8076
```

Let's compare to the baseline provided by Microsoft.
First, download:

```
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-top100.gz -P runs
gunzip runs/msmarco-docdev-top100.gz
```

Then, run `trec_eval` to compare:

```
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.100 -mmap \
   tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/msmarco-docdev-top100
map                   	all	0.2219
recall_100            	all	0.7564
```

We can see that Anserini's (tuned) BM25 baseline is already much better than the baseline provided by the organizers.

## Replication Log

+ Results replicated by [@JeffreyCA](https://github.com/JeffreyCA) on 2020-09-14 (commit [`49fd7cb`](https://github.com/castorini/pyserini/commit/49fd7cb8fd802493dc34f5cb33767d2e72e19f13))
+ Results replicated by [@jhuang265](https://github.com/jhuang265) on 2020-09-14 (commit [`2ed2acc`](https://github.com/castorini/pyserini/commit/2ed2acc62e445e3e887c6cf853ccc0b0b3b57534))
+ Results replicated by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2020-11-12 (commit [`55c3dbc`](https://github.com/castorini/pyserini/commit/55c3dbc607d72b5318bff14ee4f89dc73e019386))
+ Results replicated by [@rakeeb123](https://github.com/rakeeb123) on 2020-12-07 (commit [`3bcd4e5`](https://github.com/castorini/pyserini/commit/3bcd4e52beb327d55ae6d3c8f6bc94351a6d1449))
+ Results replicated by [@jrzhang12](https://github.com/jrzhang12) on 2021-01-03 (commit [`7caedfc`](https://github.com/castorini/pyserini/commit/7caedfc150f916de302297406c45dead27b475ba))
+ Results replicated by [@HEC2018](https://github.com/HEC2018) on 2021-01-04 (commit [`46a6d47`](https://github.com/castorini/pyserini/commit/46a6d472267a559152495d004c2a12f8e95e53f0))
+ Results replicated by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-08 (commit [`aeec31f`](https://github.com/castorini/pyserini/commit/aeec31fbe17d39ecf3081597b4832f5af57ea549))

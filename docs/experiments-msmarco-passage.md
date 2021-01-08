# Pyserini: BM25 Baseline for MS MARCO Passage Retrieval

This guide contains instructions for running BM25 baselines on the [MS MARCO *passage* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md), except that everything is in Python here (no Java).
Note that there is a separate guide for the [MS MARCO *document* ranking task](experiments-msmarco-doc.md).

## Data Prep

We're going to use `collections/msmarco-passage/` as the working directory.
First, we need to download and extract the MS MARCO passage dataset:

```bash
mkdir collections/msmarco-passage

wget https://msmarco.blob.core.windows.net/msmarcoranking/collectionandqueries.tar.gz -P collections/msmarco-passage

# Alternative mirror:
# wget https://www.dropbox.com/s/9f54jg2f71ray3b/collectionandqueries.tar.gz -P collections/msmarco-passage

tar xvfz collections/msmarco-passage/collectionandqueries.tar.gz -C collections/msmarco-passage
```

To confirm, `collectionandqueries.tar.gz` should have MD5 checksum of `31644046b18952c1386cd4564ba2ae69`.

Next, we need to convert the MS MARCO tsv collection into Anserini's jsonl files (which have one json object per line):

```bash
python tools/scripts/msmarco/convert_collection_to_jsonl.py \
 --collection-path collections/msmarco-passage/collection.tsv \
 --output-folder collections/msmarco-passage/collection_jsonl
```

The above script should generate 9 jsonl files in `collections/msmarco-passage/collection_jsonl`, each with 1M lines (except for the last one, which should have 841,823 lines).

We can now index these docs as a `JsonCollection` using Anserini:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 9 -input collections/msmarco-passage/collection_jsonl \
 -index indexes/msmarco-passage/lucene-index-msmarco -storePositions -storeDocvectors -storeRaw
```

Note that the indexing program simply dispatches command-line arguments to an underlying Java program, and so we use the Java single dash convention, e.g., `-index` and not `--index`.

Upon completion, we should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD, indexing takes a couple of minutes.

## Performing Retrieval on the Dev Queries

Since queries of the set are too many (+100k), it would take a long time to retrieve all of them. To speed this up, we use only the queries that are in the qrels file:

```bash
python tools/scripts/msmarco/filter_queries.py \
 --qrels collections/msmarco-passage/qrels.dev.small.tsv \
 --queries collections/msmarco-passage/queries.dev.tsv \
 --output collections/msmarco-passage/queries.dev.small.tsv
```

The output queries file should contain 6980 lines.
We can now perform a retrieval run using this smaller set of queries:

```bash
python tools/scripts/msmarco/retrieve.py --hits 1000 --threads 1 \
 --index indexes/msmarco-passage/lucene-index-msmarco \
 --queries collections/msmarco-passage/queries.dev.small.tsv \
 --output runs/run.msmarco-passage.dev.small.tsv
```

Note that by default, the above script uses BM25 with tuned parameters `k1=0.82`, `b=0.68`.
The option `--hits` specifies the of documents per query to be retrieved.
Thus, the output file should have approximately 6980 × 1000 = 6.9M lines.

Retrieval speed will vary by machine:
On a modern desktop with an SSD, we can get ~0.07 s/query, so the run should finish in under ten minutes.
We can perform multi-threaded retrieval by changing the `--threads` argument.

## Evaluating the Results

Finally, we can evaluate the retrieved documents using this the official MS MARCO evaluation script:

```bash
python tools/scripts/msmarco/msmarco_eval.py \
 collections/msmarco-passage/qrels.dev.small.tsv runs/run.msmarco-passage.dev.small.tsv
```

And the output should be like this:

```
#####################
MRR @10: 0.18741227770955546
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
python tools/scripts/msmarco/convert_msmarco_to_trec_run.py \
 --input runs/run.msmarco-passage.dev.small.tsv \
 --output runs/run.msmarco-passage.dev.small.trec

python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
 --input collections/msmarco-passage/qrels.dev.small.tsv \
 --output collections/msmarco-passage/qrels.dev.small.trec
```

And run the `trec_eval` tool:

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
 collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.dev.small.trec
```

The output should be:

```
map                   	all	0.1957
recall_1000           	all	0.8573
```

Average precision or AP (also called mean average precision, MAP) and recall@1000 (recall at rank 1000) are the two metrics we care about the most.
AP captures aspects of both precision and recall in a single metric, and is the most common metric used by information retrieval researchers.
On the other hand, recall@1000 provides the upper bound effectiveness of downstream reranking modules (i.e., rerankers are useless if there isn't a relevant document in the results).

## Replication Log

+ Results replicated by [@JeffreyCA](https://github.com/JeffreyCA) on 2020-09-14 (commit [`49fd7cb`](https://github.com/castorini/pyserini/commit/49fd7cb8fd802493dc34f5cb33767d2e72e19f13))
+ Results replicated by [@jhuang265](https://github.com/jhuang265) on 2020-09-14 (commit [`2ed2acc`](https://github.com/castorini/pyserini/commit/2ed2acc62e445e3e887c6cf853ccc0b0b3b57534))
+ Results replicated by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2020-11-11 (commit [`8172015`](https://github.com/Dahlia-Chehata/pyserini/commit/817201553d790c8b53a3aef17ed87721a9d35595))
+ Results replicated by [@rakeeb123](https://github.com/rakeeb123) on 2020-12-07 (commit [`3bcd4e5`](https://github.com/castorini/pyserini/commit/3bcd4e52beb327d55ae6d3c8f6bc94351a6d1449))
+ Results replicated by [@jrzhang12](https://github.com/jrzhang12) on 2021-01-03 (commit [`7caedfc`](https://github.com/castorini/pyserini/commit/7caedfc150f916de302297406c45dead27b475ba))
+ Results replicated by [@HEC2018](https://github.com/HEC2018) on 2021-01-04 (commit [`46a6d47`](https://github.com/castorini/pyserini/commit/46a6d472267a559152495d004c2a12f8e95e53f0))
+ Results replicated by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-08 (commit [`0d0628f`](https://github.com/castorini/anserini/commit/0d0628f24fb3e764df94aaf240c496482250deed))

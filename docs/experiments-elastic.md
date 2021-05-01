# Pyserini: Multi-field Baseline for MS MARCO Document Ranking

This page contains instructions for reproducing the "Elasticsearch optimized
multi_match best_fields" entry (2020/11/25) on the the [MS MARCO Document Ranking Leaderboard](https://microsoft.github.io/MSMARCO-Document-Ranking-Submissions/leaderboard/) using Pyserini.
Details behind this run are described in this [blog post](https://www.elastic.co/blog/improving-search-relevance-with-data-driven-query-optimization);
the official leaderboard submission corresponds to the run denoted "multi_match best_fields tuned (all-in-one): all
params" in the blog post.

This run makes sure to preserve the distinction between document fields when
preparing and indexing documents. For ranking, we use a disjunction max query to
combine score contributions across fields; the weights for the disjunction max
query are taken from the blog post reference above.

To match the leaderboard results, this run makes use of a custom stopwords file
[`elastic-msmarco-stopwords.txt`](elastic-msmarco-stopwords.txt). The file contains the default English stopwords
from Lucene, plus some additional words targeted at question-style queries.

## Data Prep

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO document dataset:

```
mkdir collections/msmarco-doc
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs.tsv.gz -P collections/msmarco-doc
gunzip collections/msmarco-doc/msmarco-docs.tsv.gz
```

To confirm, `msmarco-docs.tsv.gz` should have an MD5 checksum of `103b19e21ad324d8a5f1ab562425c0b4`.

First we need to convert the file to JSON lines format. Each document will
correspond to a JSON object with distinct fields for title, URL, and body:

```bash
python tools/scripts/msmarco/convert_doc_collection_to_jsonl.py \
  --collection-path collections/msmarco-doc/msmarco-docs.tsv \
  --output-folder collections/msmarco-doc-json
```

We then build the index with the following command:

```bash
python -m pyserini.index -threads 4 -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -input collections/msmarco-doc-json/ \
  -index indexes/msmarco-doc/lucene-index-msmarco -storeRaw \
  -stopwords docs/elastic-msmarco-stopwords.txt
```

On a modern desktop with an SSD, indexing takes around 15 minutes.
There should be a total of 3,201,821 documents indexed.

## Performing Retrieval on the Dev Queries

After indexing finishes, we can do a retrieval run. A few minor details to pay
attention to: the official metric is MRR@100, so we want to only return the top
100 hits, and the submission files to the leaderboard have a slightly different
format.

```bash
python -m pyserini.search --output-format msmarco --hits 100 \
  --topics msmarco-doc-dev \
  --index indexes/msmarco-doc/lucene-index-msmarco/ \
  --output runs/run.msmarco-doc.leaderboard-dev.elastic.txt \
  --bm25 --k1 1.2 --b 0.75 \
  --fields contents=10.0 title=8.63280262513067 url=0.0 \
  --dismax --dismax.tiebreaker 0.3936135232328522 \
  --stopwords docs/elastic-msmarco-stopwords.txt
```

After the run completes, we can evaluate the results:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.leaderboard-dev.elastic.txt
#####################
MRR @100: 0.3071421845448626
QueriesRanked: 5193
#####################
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-03-10 (commit [`8d51d9`](https://github.com/castorini/pyserini/commit/8d51d9c2ebc0d39e37e3ccda63085de50d536fcb))

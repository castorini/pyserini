# Reproducing Results Directly via PyPI Package

It's easy to reproduce runs on many "standard" IR test collections directly from the PyPI package (i.e., with only `pip install`)!
The following results can be reproduced with v0.10.1.0 or anything later, including HEAD.

## Robust04

BM25 baseline from the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md) on TREC Disks 4 &amp; 5: 

```bash
$ python -m pyserini.search --topics robust04 --index robust04 --output run.robust04.txt --bm25
```

To evaluate:

```bash
$ python -m pyserini.eval.trec_eval -m map -m P.30 robust04 run.robust04.txt
map                   	all	0.2531
P_30                  	all	0.3102
```

## MS MARCO Passage Ranking

MS MARCO passage ranking task, BM25 baseline:

```bash
$ python -m pyserini.search --topics msmarco-passage-dev-subset --index msmarco-passage --output run.msmarco-passage.txt --bm25 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.msmarco-passage.txt
#####################
MRR @10: 0.18741227770955546
QueriesRanked: 6980
#####################
```

MS MARCO passage ranking task, BM25 baseline with [docTTTTTquery expansions](http://doc2query.ai/):

```bash
$ python -m pyserini.search --topics msmarco-passage-dev-subset --index msmarco-passage-expanded --output run.msmarco-passage.expanded.txt --bm25 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset run.msmarco-passage.expanded.txt
#####################
MRR @10: 0.281560751807885
QueriesRanked: 6980
#####################
```

## MS MARCO Document Ranking

MS MARCO document ranking task, BM25 baseline:

```bash
$ python -m pyserini.search --topics msmarco-doc-dev --index msmarco-doc --output run.msmarco-doc.doc.txt --bm25 --hits 100 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run run.msmarco-doc.doc.txt
#####################
MRR @100: 0.2770296928568702
QueriesRanked: 5193
#####################
```

MS MARCO document ranking task, BM25 baseline with [docTTTTTquery expansions](http://doc2query.ai/) (per-document):

```bash
$ python -m pyserini.search --topics msmarco-doc-dev --index msmarco-doc-expanded-per-doc --output run.msmarco-doc.doc-expanded.txt --bm25 --hits 100 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run run.msmarco-doc.doc-expanded.txt
#####################
MRR @100: 0.3265190296491929
QueriesRanked: 5193
#####################
```

MS MARCO document ranking task, BM25 baseline, but with documents segmented into passages and selecting the best-scoring passage per document:

```bash
$ python -m pyserini.search --topics msmarco-doc-dev --index msmarco-doc-per-passage --output run.msmarco-doc.passage.txt --bm25 --hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run run.msmarco-doc.passage.txt
#####################
MRR @100: 0.275120210994691
QueriesRanked: 5193
#####################
```

MS MARCO document ranking task, BM25 baseline with [docTTTTTquery expansions](http://doc2query.ai/) (per-passage):

```bash
$ python -m pyserini.search --topics msmarco-doc-dev --index msmarco-doc-expanded-per-passage --output run.msmarco-doc.passage-expanded.txt --bm25 --hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco
```

Evaluation command:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run run.msmarco-doc.passage-expanded.txt
#####################
MRR @100: 0.3208186157918374
QueriesRanked: 5193
#####################
```

## Notes

There are minor differences between v0.10.1.0 to v0.11.0.0 due to changes in the iteration order of the MS MARCO queries (see [#309](https://github.com/castorini/pyserini/pull/309/)).

Prior to v0.10.1.0, the above commands get different results:

+ With `pyserini==0.10.0.0`, hits are hard coded to 1000 (see [here](https://github.com/castorini/pyserini/blob/pyserini-0.10.0.0/pyserini/search/__main__.py#L110)), even though for MS MARCO doc we only evaluate top 100 hits.
+ With `pyserini==0.10.0.1`, the number hits have been parameterized (see [here](https://github.com/castorini/pyserini/blob/pyserini-0.10.0.1/pyserini/search/__main__.py#L112)), although retrieval is performed using default BM25 parameters.
+ With `pyserini==0.10.1.0`, `pyserini.search` automatically sets BM25 parameters depending on task (see [here](https://github.com/castorini/pyserini/blob/pyserini-0.10.1.0/pyserini/search/__main__.py#L73)).

For additional details, see the snapshot of this documentation page at [`pyserini-0.10.1.0`](https://github.com/castorini/pyserini/blob/pyserini-0.10.1.0/docs/pypi-replication.md), which is just before the document has been updated for `pyserini==0.10.1.0`.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@MXueguang](https://github.com/MXueguang) on 2021-01-05 (commit [`b6da95a`](https://github.com/castorini/pyserini/commit/b6da95aaf81ebb26d51be5c7f2cf68b44361307b))

 

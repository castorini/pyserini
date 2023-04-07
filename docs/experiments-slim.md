# Pyserini: Reproducing SLIM on MS MARCO Passages-v1

This guide describes how to reproduce the SLIM experiments in the following paper:

> Minghan Li, Sheng-Chieh Lin, Xueguang Ma, Jimmy Lin. [SLIM: Sparsified Late Interaction for Multi-Vector Retrieval with
Inverted Indexes.](https://arxiv.org/abs/2302.06587) _arXiv:2302.06587_.

The training code is provided [here](https://github.com/alexlimh/SLIM).

Due to naming conflict with [Lucence optimation](https://github.com/castorini/pyserini/blob/f010aa17a8f51887c056bff2f52f85d78e6eb27b/pyserini/resources/index-metadata/lucene-index.msmarco-v1-passage-slim.20220131.9ea315.README.md), we use `slimr` to denote our model which stands for ''slim retrieval''.

To reproduce the non-distilled version of SLIM, we run retrieval using the `castorini/slimr-msmarco-passage` model available on Huggingface's model hub:

```bash
python -m pyserini.search.lucene \
  --index msmarco-v1-passage-slimr \
  --topics msmarco-passage-dev-subset \
  --encoder castorini/slimr-msmarco-passage \
  --encoded-corpus scipy-sparse-vectors.msmarco-v1-passage-slimr \
  --output runs/run.msmarco-passage.slimr.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact --min-idf 3
```

Here, we are using the transformer model to encode the queries on the fly using the CPU.
Note that the important option here is `--impact`, where we specify impact scoring.
With these impact scores, query evaluation is already slower than bag-of-words BM25; on top of that we're adding neural inference on the CPU.

The output is in MS MARCO output format, so we can directly evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.slimr.tsv

#####################
MRR @10: 0.3581149656615276
QueriesRanked: 6980
#####################
```

For the distilled version, we could follow the similar procedure of indexing and retrieval:

Retrieval
```bash
python -m pyserini.search.lucene \
  --index msmarco-v1-passage-slimr-pp \
  --topics msmarco-passage-dev-subset \
  --encoder castorini/slimr-pp-msmarco-passage \
  --encoded-corpus scipy-sparse-vectors.msmarco-v1-passage-slimr-pp \
  --output runs/run.msmarco-passage.slimr-pp.tsv \
  --output-format msmarco \
  --batch 36 --threads 12 \
  --hits 1000 \
  --impact --min-idf 3
```

Evaluation
```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.slimr-pp.tsv

#####################
MRR @10: 0.40315936689862253
QueriesRanked: 6974
#####################
```
The final QueriesRanked is less than 6980, which results from the excessive pruning using min-idf=3, and therefore some queries' representations are completely pruned and therefore they return no ranking list. To avoid this, use smaller min-idf which, however, might increase the search latency.


## Reproduction Log[*](reproducibility.md)


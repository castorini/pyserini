# Pyserini: Reproducing ANCE-PRF Results

This guide provides instructions to reproduce the ANCE-PRF results from the following work:

> HongChien Yu, Chenyan Xiong, Jamie Callan. [Improving Query Representations for Dense Retrieval with Pseudo Relevance Feedback](https://arxiv.org/abs/2108.13454)

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.


## Summary
Here's how our results stack up:

### Passage Ranking Datasets

#### TREC DL 2019 Passage

| Dataset              | Model                | Method                  | nDCG@10 | Recall@1000 |
|:---------------------|:---------------------|:------------------------|:-------:|:-----------:|
| TREC DL 2019 Passage | ANCE                 | Original                | 0.6452  | 0.7554      |
| TREC DL 2019 Passage | ANCE-PRF             | PRF 3                   | 0.6776  | 0.7915      |
| TREC DL 2020 Passage | ANCE                 | Original                | 0.6458  | 0.7764      |
| TREC DL 2020 Passage | ANCE-PRF             | PRF 3                   | 0.6736  | 0.7942      |
| MS MARCO V1 Passage  | ANCE                 | Original                | 0.3877  | 0.9584      | 
| MS MARCO V1 Passage  | ANCE-PRF             | PRF 3                   | 0.3991  | 0.9596      |

## Reproducing ANCE-PRF Results

To reproduce the ANCE-PRF results, it has certain limitations. 

First of all, different PRF depths need to use different `--ance-prf-encoder`, the one we provided is only for `k=3`, which means it can only do `--prf-depth 3`.

Second, it takes two more parameters, one `--ance-prf-encoder` which points to the checkpoint directory, and `--sparse-index` that points to a lucene index.

For the lucene index, it needs to have `--storeRaw` enabled when building the index.

To reproduce `TREC DL 2019 Passage`, use the command below, change `--ance-prf-encoder` to the path that stores the checkpoint:
```
$ python -m pyserini.dsearch --topics dl19-passage \                                               
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 32 \
    --output runs/run.dl19-passage.ance-prf3.trec \
    --prf-depth 3 \
    --prf-method ance-prf \
    --threads 12 \
    --sparse-index msmarco-passage \
    --ance-prf-encoder ckpt/ance_prf_k3_checkpoint
```

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.1000 -l 2 dl19-passage runs/run.dl19-passage.ance-prf3.trec
ndcg_cut_10         all     0.6776
recall_1000         all     0.7915
```

For `TREC DL 2020 Passage`:
```
$ python -m pyserini.dsearch --topics dl20 \                                               
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 32 \
    --output runs/run.dl20-passage.ance-prf3.trec \
    --prf-depth 3 \
    --prf-method ance-prf \
    --threads 12 \
    --sparse-index msmarco-passage \
    --ance-prf-encoder ckpt/ance_prf_k3_checkpoint
```

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.1000 -l 2 dl20-passage runs/run.dl20-passage.ance-prf3.trec
ndcg_cut_10         all     0.6736
recall_1000         all     0.7942
```

For `MS MARCO V1 Passage`:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \                                               
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 32 \
    --output runs/run.marco-passagev1.ance-prf3.tsv \
    --prf-depth 3 \
    --prf-method ance-prf \
    --threads 12 \
    --sparse-index msmarco-passage \
    --ance-prf-encoder ckpt/ance_prf_k3_checkpoint \
    --output-format msmarco
```

To evaluate:
```
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.marco-passagev1.ance-prf3.tsv
#####################
MRR @10: 0.34179202483285515
QueriesRanked: 6980
#####################
```

```
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.marco-passagev1.ance-prf3.tsv --output runs/run.marco-passagev1.ance-prf3.trec
$ python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.1000 msmarco-passage-dev-subset runs/run.marco-passagev1.ance-prf3.trec
ndcg_cut_10         all     0.3991
recall_1000         all     0.9596
```


## Reproduction Log[*](reproducibility.md)

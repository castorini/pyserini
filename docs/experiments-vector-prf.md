# Pyserini: Reproducing Vector PRF Results

This guide provides instructions to reproduce the Vector PRF in the following work and on all datasets and DR models available in Pyserini:

> Hang Li, Ahmed Mourad, Shengyao Zhuang, Bevan Koopman, Guido Zuccon. [Pseudo Relevance Feedback with Deep Language Models and Dense Retrievers: Successes and Pitfalls](https://arxiv.org/pdf/2108.11044.pdf)

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.


## Summary
Here's how our results stack up against all available models and datasets in Pyserini:

### Passage Ranking Datasets

#### TREC DL 2019 Passage

| Model                | Method                  | MAP    | nDCG@100 | Recall@1000 |
|:---------------------|:------------------------|:------:|:--------:|:-----------:|
| ANCE                 | Original                | 0.3710 | 0.5540   | 0.7554      |
| ANCE                 | Average PRF 3           | 0.4247 | 0.5937   | 0.7739      |
| ANCE                 | Rocchio PRF 5 A0.4 B0.6 | 0.4211 | 0.5928   | 0.7825      |
| TCT-ColBERT V1       | Original                | 0.3906 | 0.5730   | 0.7916      |
| TCT-ColBERT V1       | Average PRF 3           | 0.4336 | 0.6119   | 0.8230      |
| TCT-ColBERT V1       | Rocchio PRF 5 A0.4 B0.6 | 0.4463 | 0.6143   | 0.8393      |
| TCT-ColBERT V2       | Original                | 0.4269 | 0.6129   | 0.8342      |
| TCT-ColBERT V2       | Average PRF 3           | 0.4766 | 0.6487   | 0.8574      |
| TCT-ColBERT V2       | Rocchio PRF 5 A0.4 B0.6 | 0.4709 | 0.6435   | 0.8496      |
| DistillBERT KD       | Original                | 0.3759 | 0.5765   | 0.6853      |
| DistillBERT KD       | Average PRF 3           | 0.4362 | 0.6217   | 0.7180      |
| DistillBERT KD       | Rocchio PRF 5 A0.4 B0.6 | 0.4378 | 0.6189   | 0.7291      |
| DistillBERT Balanced | Original                | 0.4761 | 0.6360   | 0.7826      |
| DistillBERT Balanced | Average PRF 3           | 0.5057 | 0.6526   | 0.8054      |
| DistillBERT Balanced | Rocchio PRF 5 A0.4 B0.6 | 0.5249 | 0.6684   | 0.8352      |
| SBERT                | Original                | 0.4060 | 0.5985   | 0.7872      |
| SBERT                | Average PRF 3           | 0.4354 | 0.6149   | 0.7937      |
| SBERT                | Rocchio PRF 5 A0.4 B0.6 | 0.4371 | 0.6149   | 0.7941      |
| ADORE                | Original                | 0.4188 | 0.5946   | 0.7759      |
| ADORE                | Average PRF 3           | 0.4672 | 0.6263   | 0.7890      |
| ADORE                | Rocchio PRF 5 A0.4 B0.6 | 0.4629 | 0.6325   | 0.7950      |


#### TREC DL 2020 Passage

| Model                | Method                  | MAP    | nDCG@100 | Recall@1000 |
|:---------------------|:------------------------|:------:|:--------:|:-----------:|
| ANCE                 | Original                | 0.4076 | 0.5679   | 0.7764      |
| ANCE                 | Average PRF 3           | 0.4325 | 0.5793   | 0.7909      |
| ANCE                 | Rocchio PRF 5 A0.4 B0.6 | 0.4315 | 0.5800   | 0.7957      |
| TCT-ColBERT V1       | Original                | 0.4290 | 0.5826   | 0.8181      |
| TCT-ColBERT V1       | Average PRF 3           | 0.4725 | 0.6101   | 0.8667      |
| TCT-ColBERT V1       | Rocchio PRF 5 A0.4 B0.6 | 0.4625 | 0.6056   | 0.8576      |
| TCT-ColBERT V2       | Original                | 0.4717 | 0.6200   | 0.8407      |
| TCT-ColBERT V2       | Average PRF 3           | 0.4701 | 0.6209   | 0.8739      |
| TCT-ColBERT V2       | Rocchio PRF 5 A0.4 B0.6 | 0.4819 | 0.6324   | 0.8760      |
| DistillBERT KD       | Original                | 0.3909 | 0.5728   | 0.6893      |
| DistillBERT KD       | Average PRF 3           | 0.3955 | 0.5755   | 0.7279      |
| DistillBERT KD       | Rocchio PRF 5 A0.4 B0.6 | 0.3990 | 0.5760   | 0.7222      |
| DistillBERT Balanced | Original                | 0.4755 | 0.6346   | 0.8009      |
| DistillBERT Balanced | Average PRF 3           | 0.4873 | 0.6449   | 0.8392      |
| DistillBERT Balanced | Rocchio PRF 5 A0.4 B0.6 | 0.4846 | 0.6470   | 0.8262      |
| SBERT                | Original                | 0.4124 | 0.5734   | 0.7937      |
| SBERT                | Average PRF 3           | 0.4258 | 0.5781   | 0.8169      |
| SBERT                | Rocchio PRF 5 A0.4 B0.6 | 0.4342 | 0.5851   | 0.8226      |
| ADORE                | Original                | 0.4418 | 0.5949   | 0.8151      |
| ADORE                | Average PRF 3           | 0.4706 | 0.6176   | 0.8323      |
| ADORE                | Rocchio PRF 5 A0.4 B0.6 | 0.4760 | 0.6193   | 0.8251      |

#### MS MARCO Passage V1

The PRF does not perform well with sparse judgements like in MS MARCO, the results here are just complements.

| Model                | Method                  | MAP    | nDCG@100 | Recall@1000 |
|:---------------------|:------------------------|:------:|:--------:|:-----------:|
| ANCE                 | Original                | 0.3363 | 0.4457   | 0.9584      | 
| ANCE                 | Average PRF 3           | 0.3132 | 0.4246   | 0.9490      | 
| ANCE                 | Rocchio PRF 5 A0.4 B0.6 | 0.3116 | 0.4250   | 0.9547      |
| TCT-ColBERT V1       | Original                | 0.3416 | 0.4514   | 0.9640      | 
| TCT-ColBERT V1       | Average PRF 3           | 0.2882 | 0.4014   | 0.9452      | 
| TCT-ColBERT V1       | Rocchio PRF 5 A0.4 B0.6 | 0.2809 | 0.3988   | 0.9543      | 
| TCT-ColBERT V2       | Original                | 0.3504 | 0.4625   | 0.9679      | 
| TCT-ColBERT V2       | Average PRF 3           | 0.3055 | 0.4189   | 0.9547      | 
| TCT-ColBERT V2       | Rocchio PRF 5 A0.4 B0.6 | 0.3002 | 0.4190   | 0.9627      | 
| DistillBERT KD       | Original                | 0.3309 | 0.4391   | 0.9553      | 
| DistillBERT KD       | Average PRF 3           | 0.2830 | 0.3940   | 0.9325      | 
| DistillBERT KD       | Rocchio PRF 5 A0.4 B0.6 | 0.2787 | 0.3937   | 0.9432      | 
| DistillBERT Balanced | Original                | 0.3515 | 0.4651   | 0.9771      | 
| DistillBERT Balanced | Average PRF 3           | 0.2978 | 0.4150   | 0.9613      | 
| DistillBERT Balanced | Rocchio PRF 5 A0.4 B0.6 | 0.2969 | 0.4178   | 0.9702      | 
| SBERT                | Original                | 0.3373 | 0.4453   | 0.9558      | 
| SBERT                | Average PRF 3           | 0.3094 | 0.4183   | 0.9446      | 
| SBERT                | Rocchio PRF 5 A0.4 B0.6 | 0.3034 | 0.4157   | 0.9529      |
| ADORE                | Original                | 0.3523 | 0.4637   | 0.9688      |
| ADORE                | Average PRF 3           | 0.3188 | 0.4330   | 0.9583      |
| ADORE                | Rocchio PRF 5 A0.4 B0.6 | 0.3209 | 0.4376   | 0.9669      |

## Reproducing Results

To reproduce the Average Vector PRF on different models, same command with different parameter values can be used:
```
$ python -m pyserini.dsearch --topics topic \
    --index index \
    --encoder encoder \
    --batch-size 64 \
    --threads 12 \
    --output runs/run.average_prf3.trec \
    --prf-depth 3 \
    --prf-method avg
```

To reproduce the Rocchio Vector PRF on different models, similar with Average:
```
$ python -m pyserini.dsearch --topics topic \
    --index index \
    --encoder encoder \
    --batch-size 64 \
    --threads 12 \
    --output runs/run.rocchio_prf5_a0.4_b0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6
```

For different models and datasets, the `--topics`, `--index`, and `--encoder` are different, since Pyserini has all these datasets available, we can pass in
different values to run on different datasets.

`--topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `dl19-passage` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `dl20` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `msmarco-passage-dev-subset` <br />

`--index`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;ANCE index with MS MARCO V1 passage collection: `msmarco-passage-ance-bf` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TCT-ColBERT V1 index with MS MARCO V1 passage collection: `msmarco-passage-tct_colbert-bf` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TCT-ColBERT V2 index with MS MARCO V1 passage collection: `msmarco-passage-tct_colbert-v2-bf` <br />
&nbsp;&nbsp;&nbsp;&nbsp;DistillBERT KD index with MS MARCO V1 passage collection: `msmarco-passage-distilbert-dot-margin_mse-T2-bf` <br />
&nbsp;&nbsp;&nbsp;&nbsp;DistillBERT Balanced index with MS MARCO V1 passage collection: `msmarco-passage-distilbert-dot-tas_b-b256-bf` <br />
&nbsp;&nbsp;&nbsp;&nbsp;SBERT index with MS MARCO V1 passage collection: `msmarco-passage-sbert-bf` <br />

_Note: TREC DL 2019, TREC DL 2020, and MS MARCO Passage V1 use the same passage collection, so the index of the same model will be the same among these three datasets._<br />

`--encoder`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;ANCE: `castorini/ance-msmarco-passage` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TCT-ColBERT V1: `castorini/tct_colbert-msmarco` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TCT-ColBERT V2: `castorini/tct_colbert-v2-hnp-msmarco` <br />
&nbsp;&nbsp;&nbsp;&nbsp;DistillBERT KD: `sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` <br />
&nbsp;&nbsp;&nbsp;&nbsp;DistillBERT Balanced: `sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` <br />
&nbsp;&nbsp;&nbsp;&nbsp;SBERT: `sentence-transformers/msmarco-distilbert-base-v3` <br />

_Note: If you have pre-computed queries available, the `--encoder` can be replaced with `--encoded-queries` to avoid "on-the-fly" query encoding by passing in the path to your pre-computed query file. 
For example, Pyserini has the ANCE pre-computed query available for MS MARCO Passage V1, so instead of using `--encoder castorini/ance-msmarco-passage`,
one can use `--encoded-queries ance-msmarco-passage-dev-subset`. For ADORE model, you can only use `--encoded-queries`, otf encoding is not available._

With these parameters, one can easily reproduce the results above, for example, to reproduce `TREC DL 2019 Passage with ANCE Average Vector PRF 3` the command will be:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --threads 12 \
    --output runs/run.ance.dl19-passage.average_prf3.trec \
    --prf-depth 3 \
    --prf-method avg
```

To reproduce `TREC DL 2019 Passage with ANCE Rocchio Vector PRF 5 Alpha 0.4 Beta 0.6`, the command will be:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --threads 12 \
    --output runs/run.ance.dl19-passage.rocchio_prf5_a0.4_b0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6
```

To evaluate, we use `trec_eval` built in Pyserini:

For TREC DL 2019, use this command to evaluate your run file:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.ance.dl19-passage.average_prf3.trec
map                 all     0.4247
ndcg_cut_100        all     0.5937
recall_1000         all     0.7739
```
Qrels file is available in Pyserini, so just replace the `runs/run.ance.dl19-passage.average_prf3.trec` with your own run file path to test your reproduced results.

Similarly, for TREC DL 2020:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.ance.dl20-passage.average_prf3.trec
map                 all     0.4325
ndcg_cut_100        all     0.5793
recall_1000         all     0.7909
```
Qrels file also available in Pyserini, just replace the `runs/run.ance.dl20-passage.average_prf3.trec` with your own run file path to test your reproduced results.

For MS MARCO Passage V1, no need to use `-l 2` option:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.ance.msmarco-passage.average_prf3.trec
map                 all     0.3132
ndcg_cut_100        all     0.4246
recall_1000         all     0.9490
```
Qrels file already available, replace the `runs/run.ance.msmarco-passage.average_prf3.trec` with your own run file path to test your reproduced results.

## Reproduction Log[*](reproducibility.md)

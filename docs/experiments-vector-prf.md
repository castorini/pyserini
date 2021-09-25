# Pyserini: Reproducing ANCE Results

This guide provides instructions to reproduce the Vector PRF in the following work:

> Hang Li, Ahmed Mourad, Shengyao Zhuang, Bevan Koopman, Guido Zuccon. [Pseudo Relevance Feedback with Deep Language Models and Dense Retrievers: Successes and Pitfalls](https://arxiv.org/pdf/2108.11044.pdf)

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## TREC DL 2019

For testing with TREC DL 2019 Passage Ranking dataset, the collection is the same as MS MARCO Passage Ranking dataset,
the index, query and qrels are already available in Pyserini, 
so to reproduce the results, just copy and paste the following commands in terminal, hit `enter` and Voilà!

**ANCE + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.ance.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
The option `--encoder castorini/ance-msmarco-passage` is used to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process. 
To use the pre-encoded query file, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.ance.avg.prf3.trec
map                 all     0.4247
ndcg_cut_100        all     0.5937
recall_1000         all     0.7739
```

**ANCE + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.ance.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.ance.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4211
ndcg_cut_100        all     0.5928
recall_1000         all     0.7825
```

**TCT-ColBERT V1 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.tctv1.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.tctv1.avg.prf3.trec
map                 all     0.4336
ndcg_cut_100        all     0.6119
recall_1000         all     0.8230
```

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4463
ndcg_cut_100        all     0.6143
recall_1000         all     0.8393
```

**TCT-ColBERT V2 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.tctv2.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.tctv2.avg.prf3.trec
map                 all     0.4766
ndcg_cut_100        all     0.6487
recall_1000         all     0.8574
```

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4709
ndcg_cut_100        all     0.6435
recall_1000         all     0.8496
```

**SBERT + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.sbert.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.sbert.avg.prf3.trec
map                 all     0.4354
ndcg_cut_100        all     0.6149
recall_1000         all     0.7937
```

**SBERT + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.sbert.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.sbert.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4371
ndcg_cut_100        all     0.6149
recall_1000         all     0.7941
```

**DistillBERT KD + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.distillbert.kd.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.distillbert.kd.avg.prf3.trec
map                 all     0.4362
ndcg_cut_100        all     0.6217
recall_1000         all     0.7180
```

**DistillBERT KD + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4378
ndcg_cut_100        all     0.6189
recall_1000         all     0.7291
```

**DistillBERT Balanced + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.distillbert.balanced.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.distillbert.balanced.avg.prf3.trec
map                 all     0.5057
ndcg_cut_100        all     0.6526
recall_1000         all     0.7180
```

**DistillBERT Balanced + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl19-passage \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2019.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl19-passage runs/run.trec_dl_2019.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.5249
ndcg_cut_100        all     0.6684
recall_1000         all     0.8352
```

## TREC DL 2020

For testing with TREC DL 2020 Passage Ranking dataset, the query and qrels files are already available in Pyserini, run the commands below without any further efforts.

**ANCE + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.ance.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
The option `--encoder castorini/ance-msmarco-passage` is used to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process. 
To use the pre-encoded query file, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.ance.avg.prf3.trec
map                 all     0.4325
ndcg_cut_100        all     0.5793
recall_1000         all     0.7909
```

**ANCE + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.ance.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2019.ance.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4315
ndcg_cut_100        all     0.5800
recall_1000         all     0.7957
```

**TCT-ColBERT V1 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.tctv1.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.tctv1.avg.prf3.trec
map                 all     0.4725
ndcg_cut_100        all     0.6101
recall_1000         all     0.8667
```

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4625
ndcg_cut_100        all     0.6056
recall_1000         all     0.8576
```

**TCT-ColBERT V2 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.tctv2.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.tctv2.avg.prf3.trec
map                 all     0.4701
ndcg_cut_100        all     0.6209
recall_1000         all     0.8739
```

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4819
ndcg_cut_100        all     0.6324
recall_1000         all     0.8760
```

**SBERT + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.sbert.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.sbert.avg.prf3.trec
map                 all     0.4258
ndcg_cut_100        all     0.5781
recall_1000         all     0.8169
```

**SBERT + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.sbert.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.sbert.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4342
ndcg_cut_100        all     0.5851
recall_1000         all     0.8226
```

**DistillBERT KD + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.distillbert.kd.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.distillbert.kd.avg.prf3.trec
map                 all     0.3955
ndcg_cut_100        all     0.5755
recall_1000         all     0.7279
```

**DistillBERT KD + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2019.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.3990
ndcg_cut_100        all     0.5760
recall_1000         all     0.7222
```

**DistillBERT Balanced + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.distillbert.balanced.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.distillbert.balanced.avg.prf3.trec
map                 all     0.4873
ndcg_cut_100        all     0.6449
recall_1000         all     0.8392
```

**DistillBERT Balanced + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics dl20 \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 -l 2 dl20-passage runs/run.trec_dl_2020.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.4846
ndcg_cut_100        all     0.6470
recall_1000         all     0.8262
```

## MS MARCO Passage (V1)

For testing with MS MARCO (V1) Passage Ranking dataset, the query and qrels files are already available in Pyserini, run the commands below without any further efforts.

**ANCE + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.msmarco-passage.ance.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
The option `--encoder castorini/ance-msmarco-passage` is used to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process. 
To use the pre-encoded query file, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.ance.avg.prf3.trec
map                 all     0.3132
ndcg_cut_100        all     0.4246
recall_1000         all     0.9490
```

**ANCE + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-ance-bf \
    --encoder castorini/ance-msmarco-passage \
    --batch-size 64 \
    --output runs/run.msmarco-passage.ance.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/ance-msmarco-passage` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.ance.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.3116
ndcg_cut_100        all     0.4250
recall_1000         all     0.9547
```

**TCT-ColBERT V1 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.tctv1.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.tctv1.avg.prf3.trec
map                 all     0.2882
ndcg_cut_100        all     0.4014
recall_1000         all     0.9452
```

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-tct_colbert-bf \
    --encoder castorini/tct_colbert-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.tctv1.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.2809
ndcg_cut_100        all     0.3988
recall_1000         all     0.9543
```

**TCT-ColBERT V2 + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.tctv2.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.tctv2.avg.prf3.trec
map                 all     0.3055
ndcg_cut_100        all     0.4189
recall_1000         all     0.9547
```

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-tct_colbert-v2-bf \
    --encoder castorini/tct_colbert-v2-hnp-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder castorini/tct_colbert-v2-hnp-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.tctv2.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.3002
ndcg_cut_100        all     0.4190
recall_1000         all     0.9627
```

**SBERT + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.msmarco-passage.sbert.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.avg.prf3.trec
map                 all     0.3094
ndcg_cut_100        all     0.4183
recall_1000         all     0.9446
```

**SBERT + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-sbert-bf \
    --encoder sentence-transformers/msmarco-distilbert-base-v3 \
    --batch-size 64 \
    --output runs/run.msmarco-passage.sbert.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sentence-transformers/msmarco-distilbert-base-v3` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.3034
ndcg_cut_100        all     0.4157
recall_1000         all     0.9529
```

**DistillBERT KD + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.trec_dl_2020.distillbert.kd.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.distillbert.kd.avg.prf3.trec
map                 all     0.2830
ndcg_cut_100        all     0.3940
recall_1000         all     0.9325
```

**DistillBERT KD + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.distillbert.kd.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.2787
ndcg_cut_100        all     0.3937
recall_1000         all     0.9432
```

**DistillBERT Balanced + Vector PRF** with Average approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.distillbert.balanced.avg.prf3.trec \
    --prf-depth 3 \
    --prf-method avg \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.distillbert.balanced.avg.prf3.trec
map                 all     0.2978
ndcg_cut_100        all     0.4150
recall_1000         all     0.9613
```

**DistillBERT Balanced + Vector PRF** with Rocchio approach:
```
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
    --index msmarco-passage-distilbert-dot-tas_b-b256-bf \
    --encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco \
    --batch-size 64 \
    --output runs/run.msmarco-passage.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec \
    --prf-depth 5 \
    --prf-method rocchio \
    --rocchio-alpha 0.4 \
    --rocchio-beta 0.6 \
    --threads 12
```
Same as above, replace `--encoder sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco` with `--encoded-queries` that points to the pre-encoded query file to skip query encoding.

To evaluate:
```
$ python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.100 -m recall.1000 msmarco-passage-dev-subset runs/run.msmarco-passage.distillbert.balanced.rocchio.prf5.alpha0.4.beta0.6.trec
map                 all     0.2969
ndcg_cut_100        all     0.4178
recall_1000         all     0.9702
```

## Reproduction Log[*](reproducibility.md)

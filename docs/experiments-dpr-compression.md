# Pyserini: DPR Index Compression
This page describes how to reproduce the DPR compression experiments in the following paper:

> Xueguang Ma, Minghan Li, Kai Sun, Ji Xin, and Jimmy Lin. 
> [Simple and Effective Unsupervised Redundancy Elimination to Compress Dense Vectors for Passage Retrieval.](https://cs.uwaterloo.ca/~jimmylin/publications/Ma_etal_EMNLP2021.pdf)
> _EMNLP 2021_, November 2021.

In this page, we focus on Natural Question as an example.
To reproduce results for other datasets, simply reply the topics `dpr-nq-test` into other datasets. e.g. (`dpr-trivia-qa`)

## Summary

| Experiments      | base index              | pca model        | pq-m | Top20 (paper) | Top100 (paper) | size | 
|------------------|-------------------------|------------------|---------|-------|--------|----------|
| `DPR-768`          | [dindex-dpr-multi-pca768](https://www.dropbox.com/s/8v8ar8dhs1n0m1p/dindex-dpr-multi-pca768.tar.gz) | N/A              | N/A  | 79.4 (79.4) | 87.0 (87.0)  | 61G
| `DPR-768-PQ2`    | as above                | N/A              | 192  | 77.9 (77.9)  | 86.3 (86.3)  | 3.8G |
| `DPR-PCA256`     | [dindex-dpr-multi-pca256](https://www.dropbox.com/s/rd6d0whgoj5as2m/dindex-dpr-multi-pca256.tar.gz) | [dpr-multi-pca256](https://www.dropbox.com/s/apfl83pqeo2o45q/dpr-multi-pca256) | N/A  | 77.6 (77.2)  | 85.6 (85.5)   | 21G | 
| `DPR-PCA256-PQ2` | as above                | as above       | 64   | 76.2 (74.8)  | 84.7 (84.1)  | 1.3G  
| `DPR-PCA128`     | [dindex-dpr-multi-pca128](https://www.dropbox.com/s/nq62qhodd237p9t/dindex-dpr-multi-pca128.tar.gz) | [dpr-multi-pca128](https://www.dropbox.com/s/d3osk3cjrgiawdp/dpr-multi-pca128) | N/A  | 75.9 (75.3)  | 84.7 (84.3)   | 11G |
| `DPR-PCA128-PQ2` | as above                | as above         | 32   | 73.5 (72.3)  | 83.3 (82.9)  | 0.6G | 

## Preparation
1. Download query encoder checkpoint
```bash
wget https://www.dropbox.com/s/a0phk75crcwlrgv/dpr-multi-question-encoder.tar.gz
tar -xvf dpr-multi-question-encoder.tar.gz
rm dpr-multi-question-encoder.tar.gz
```

2. Download pre-built index and PCA model from the summary table above.
> We use the setting for `DPR-PCA128-PQ2` as example below:
```bash
wget https://www.dropbox.com/s/nq62qhodd237p9t/dindex-dpr-multi-pca128.tar.gz
tar -xvf dindex-dpr-multi-pca128.tar.gz
rm dindex-dpr-multi-pca128.tar.gz
wget https://www.dropbox.com/s/d3osk3cjrgiawdp/dpr-multi-pca128
```
3. Setting variables for specific experiment.
> We use the setting for `DPR-PCA128-PQ2` as example below:
```bash
QUERY_ENCODER=dpr-multi-question-encoder
BASE_DINDEX=dindex-dpr-multi-pca128
TARGET_DINDEX=dindex-dpr-multi-pca128-pq2
PCA=dpr-multi-pca128
PQ_M=32
DIMENSION=128
```

## Product Quantization
Conduct Product Quantization on pre-built index
```bash
python -m pyserini.index.faiss --input ${BASE_DINDEX} \
                               --output ${TARGET_DINDEX} \
                               --dim ${DIMENSION} \
                               --pq --pq-m ${PQ_M}
```

## Retrieval
```bash
python -m pyserini.dsearch --topics dpr-nq-test \
                           --index ${TARGET_DINDEX} \
                           --encoder ${QUERY_ENCODER} \
                           --pca-model ${PCA} \
                           --output run.dpr.nq-test.trec \
                           --hits 100 \
                           --batch-size 36 \
                           --threads 36
```

## Evaluation
Convert trec format into json format with raw text
```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                              --index wikipedia-dpr \
                                                              --input run.dpr.nq-test.trec \
                                                              --output run.dpr.nq-test.json
```

```bash
python -m pyserini.eval.evaluate_dpr_retrieval --retrieval run.dpr.nq-test.json --topk 20 100
Top20	accuracy: 0.7349
Top100	accuracy: 0.8330
```



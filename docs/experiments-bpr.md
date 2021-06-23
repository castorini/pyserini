# Pyserini: Reproducing BPR Results

[Binary passage retriever](https://arxiv.org/abs/2106.00882) (BPR) is a two-stage ranking approach that represents the passages in both binary codes and dense vectors for memory efficiency and effectiveness.

We have replicated BPR's results and incorporated the technique into Pyserini.
To be clear, we started with model checkpoint and index releases in the official [BPR repo](https://github.com/studio-ousia/bpr) and did _not_ train the query and passage encoders from scratch.

This guide provides instructions to reproduce the BPR's results.
We cover only retrieval here; for end-to-end answer extraction, please see [this guide](https://github.com/castorini/pygaggle/blob/master/docs/experiments-dpr-reader.md) in our PyGaggle neural text ranking library. For more instructions, please see our [dense retrieval replication guide](https://github.com/castorini/pyserini/blob/master/docs/experiments-dpr.md).

## Summary

Here's how our results stack up against results reported in the paper using the BPR model (index 2.3GB + model 0.4GB):

| Dataset     | Method        | Top-20 (orig) | Top-20 (us)| Top-100 (orig) | Top-100 (us)|
|:------------|:--------------|--------------:|-----------:|---------------:|------------:|
| NQ          | BPR           | 77.9          |    77.9    | 85.7           | 85.7        | 
| NQ          | BPR w/o reranking          | 76.5          |    76.0    | 84.9           | 85.0        |

## Natural Questions (NQ) with BPR

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-bpr-nq-hash \
                             --encoded-queries bpr-nq-test \
                             --output runs/run.bpr.rerank.nq-test.nq.hash.trec \
                             --rerank \
                             --hits 100 --binary-hits 1000 \
                             --batch-size 36 --threads 12
```

The option `--encoded-queries` specifies the use of encoded queries (i.e., queries that have already been converted into dense vectors and cached).

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.bpr.rerank.nq-test.nq.hash.trec \
                                                                --output runs/run.bpr.rerank.nq-test.nq.hash.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.bpr.rerank.nq-test.nq.hash.json --topk 20 100
Top20  accuracy: 0.7947
Top100 accuracy: 0.8609
```

## Reproduction Log[*](reproducibility.md)

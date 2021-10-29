# Pyserini: Reproducing BPR Results

Binary passage retriever (BPR) is a two-stage ranking approach that represents the passages in both binary codes and dense vectors for memory efficiency and effectiveness.

> Ikuya Yamada, Akari Asai, Hannaneh Hajishirzi. [Efficient Passage Retrieval with Hashing for Open-domain Question Answering.](https://aclanthology.org/2021.acl-short.123/) _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)_, pages 979-986, 2021.

We have replicated BPR's results and incorporated the model into Pyserini.
To be clear, we started with model checkpoint and index releases in the official [BPR repo](https://github.com/studio-ousia/bpr) and did _not_ train the query and passage encoders from scratch.

This guide provides instructions to reproduce the BPR's results.

## Summary

Here's how our results stack up against results reported in the paper using the BPR model (index 2.3 GB + model 0.4 GB):

| Dataset     | Method        | Top-20 (orig) | Top-20 (us)| Top-100 (orig) | Top-100 (us)|
|:------------|:--------------|--------------:|-----------:|---------------:|------------:|
| NQ          | BPR           | 77.9          |    77.9    | 85.7           | 85.7        | 
| NQ          | BPR w/o reranking          | 76.5          |    76.0    | 84.9           | 85.0        |

## Natural Questions (NQ) with BPR

BPR with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-bpr-single-nq-hash \
                             --encoded-queries bpr_single_nq-nq-test \
                             --output runs/run.bpr.rerank.nq-test.nq.hash.trec \
                             --rerank \
                             --hits 100 --binary-hits 1000 \
                             --batch-size 36 --threads 12 \
                             --searcher bpr
```

The option `--encoded-queries` specifies the use of encoded queries (i.e., queries that have already been converted into dense vectors and cached).

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.bpr.rerank.nq-test.nq.hash.trec \
                                                                --output runs/run.bpr.rerank.nq-test.nq.hash.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.bpr.rerank.nq-test.nq.hash.json --topk 20 100
Top20  accuracy: 0.779
Top100 accuracy: 0.857
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-09-08 (commit [`d7a7be`](https://github.com/castorini/pyserini/commit/d7a7bededc650dfa87eb89ba92907fd97a10310b))

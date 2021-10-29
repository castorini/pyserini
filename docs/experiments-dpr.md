# Pyserini: Reproducing DPR Results

Dense passage retriever (DPR) is a dense retrieval method described in the following paper:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih. [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/). _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2020.

We have replicated DPR results and incorporated the technique into Pyserini.
Our own efforts are described in the following paper:

> Xueguang Ma, Kai Sun, Ronak Pradeep, and Jimmy Lin. [A Replication Study of Dense Passage Retriever](https://arxiv.org/abs/2104.05740). _arXiv:2104.05740_, April 2021. 

To be clear, we started with model checkpoint releases in the official [DPR repo](https://github.com/facebookresearch/DPR) and did _not_ retrain the query and passage encoders from scratch.
Our implementation does not share any code with the DPR repo, other than evaluation scripts to ensure that results are comparable.

This guide provides instructions to reproduce our replication study.
Our efforts include both retrieval as well as end-to-end answer extraction.
We cover only retrieval here; for end-to-end answer extraction, please see [this guide](https://github.com/castorini/pygaggle/blob/master/docs/experiments-dpr-reader.md) in our PyGaggle neural text ranking library.

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## Summary

Here's how our results stack up against results reported in the paper using the DPR-Multi model:

| Dataset     | Method        | Top-20 (orig) | Top-20 (us)| Top-100 (orig) | Top-100 (us)|
|:------------|:--------------|--------------:|-----------:|---------------:|------------:|
| NQ          | DPR           | 79.4          | 79.5       | 86.0           | 86.1        |
| NQ          | BM25          | 59.1          | 62.9       | 73.7           | 78.3        |
| NQ          | Hybrid        | 78.0          | 82.6       | 83.9           | 88.6        |
| TriviaQA    | DPR           | 78.8          | 78.9       | 84.7           | 84.8        |
| TriviaQA    | BM25          | 66.9          | 76.4       | 76.7           | 83.2        |
| TriviaQA    | Hybrid        | 79.9          | 82.6       | 84.4           | 86.5        |
| WQ          | DPR           | 75.0          | 75.0       | 82.9           | 83.0        |
| WQ          | BM25          | 55.0          | 62.4       | 71.1           | 75.5        |
| WQ          | Hybrid        | 74.7          | 77.1       | 82.3           | 84.4        |
| CuratedTREC | DPR           | 89.1          | 88.8       | 93.9           | 93.4        |
| CuratedTREC | BM25          | 70.9          | 80.7       | 84.1           | 89.9        |
| CuratedTREC | Hybrid        | 88.5          | 90.1       | 94.1           | 95.0        |
| SQuAD       | DPR           | 51.6          | 52.0       | 67.6           | 67.7        |
| SQuAD       | BM25          | 68.8          | 71.1       | 80.0           | 81.8        |
| SQuAD       | Hybrid        | 66.2          | 75.1       | 78.6           | 84.4        |

The hybrid results reported above for "us" capture what we call the "norm" condition (see paper for details).

## Natural Questions (NQ) with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoded-queries dpr_multi-nq-test \
                             --output runs/run.dpr.nq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

The option `--encoded-queries` specifies the use of encoded queries (i.e., queries that have already been converted into dense vectors and cached).
As an alternative, replace with `--encoder facebook/dpr-question_encoder-multiset-base` to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.nq-test.multi.bf.trec \
                                                                --output runs/run.dpr.nq-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.nq-test.multi.bf.json --topk 20 100
Top20  accuracy: 0.7947
Top100 accuracy: 0.8609
```

**BM25 retrieval**:

```bash
$ python -m pyserini.search --topics dpr-nq-test \
                            --index wikipedia-dpr \
                            --output runs/run.dpr.nq-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.nq-test.bm25.trec \
                                                                --output runs/run.dpr.nq-test.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.nq-test.bm25.json --topk 20 100
Top20  accuracy: 0.6294
Top100 accuracy: 0.7825
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoded-queries dpr_multi-nq-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-nq-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.nq-test.multi.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.nq-test.multi.bf.bm25.trec \
                                                                --output runs/run.dpr.nq-test.multi.bf.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.nq-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.8260
Top100 accuracy: 0.8859
```

## TriviaQA with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoded-queries dpr_multi-trivia-test \
                             --output runs/run.dpr.trivia-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.trivia-test.multi.bf.trec \
                                                                --output runs/run.dpr.trivia-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.trivia-test.multi.bf.json --topk 20 100
Top20  accuracy: 0.7887
Top100 accuracy: 0.8479
```

**BM25 retrieval**:

```bash
$ python -m pyserini.search --topics dpr-trivia-test \
                            --index wikipedia-dpr \
                            --output runs/run.dpr.trivia-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.trivia-test.bm25.trec \
                                                                --output runs/run.dpr.trivia-test.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.trivia-test.bm25.json --topk 20 100
Top20  accuracy: 0.7641
Top100 accuracy: 0.8315
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoded-queries dpr_multi-trivia-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-trivia-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.trivia-test.multi.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.trivia-test.multi.bf.bm25.trec \
                                                                --output runs/run.dpr.trivia-test.multi.bf.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.trivia-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.8264
Top100 accuracy: 0.8655
```

## WebQuestions (WQ) with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-wq-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoded-queries dpr_multi-wq-test \
                             --output runs/run.dpr.wq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.wq-test.multi.bf.trec \
                                                                --output runs/run.dpr.wq-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.wq-test.multi.bf.json --topk 20 100
Top20  accuracy: 0.7505
Top100 accuracy: 0.8297
```

**BM25 retrieval**:

```bash
$ python -m pyserini.search --topics dpr-wq-test \
                            --index wikipedia-dpr \
                            --output runs/run.dpr.wq-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.wq-test.bm25.trec \
                                                                --output runs/run.dpr.wq-test.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.wq-test.bm25.json --topk 20 100
Top20  accuracy: 0.6240
Top100 accuracy: 0.7549
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoded-queries dpr_multi-wq-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-wq-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.wq-test.multi.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.wq-test.multi.bf.bm25.trec \
                                                                --output runs/run.dpr.wq-test.multi.bf.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.wq-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.7712
Top100 accuracy: 0.8440
```

## CuratedTREC with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-curated-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoded-queries dpr_multi-curated-test \
                             --output runs/run.dpr.curated-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` with for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.curated-test.multi.bf.trec \
                                                                --output runs/run.dpr.curated-test.multi.bf.json \
                                                                --regex

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.curated-test.multi.bf.json --topk 20 100 --regex
Top20  accuracy: 0.8876
Top100 accuracy: 0.9337
```

**BM25 retrieval**:

```bash
$ python -m pyserini.search --topics dpr-curated-test \
                            --index wikipedia-dpr \
                            --output runs/run.dpr.curated-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.curated-test.bm25.trec \
                                                                --output runs/run.dpr.curated-test.bm25.json \
                                                                --regex

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.curated-test.bm25.json --topk 20 100 --regex
Top20  accuracy: 0.8069
Top100 accuracy: 0.8991
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoded-queries dpr_multi-curated-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.05 \
                             run    --topics dpr-curated-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.curated-test.multi.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.curated-test.multi.bf.bm25.trec \
                                                                --output runs/run.dpr.curated-test.multi.bf.bm25.json \
                                                                --regex

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.curated-test.multi.bf.bm25.json --topk 20 100 --regex
Top20  accuracy: 0.9006
Top100 accuracy: 0.9496
```

## SQuAD with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-squad-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoded-queries dpr_multi-squad-test \
                             --output runs/run.dpr.squad-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.squad-test.multi.bf.trec \
                                                                --output runs/run.dpr.squad-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.squad-test.multi.bf.json --topk 20 100
Top20  accuracy: 0.5199
Top100 accuracy: 0.6773
```

**BM25 retrieval**:

```bash
$ python -m pyserini.search --topics dpr-squad-test \
                            --index wikipedia-dpr \
                            --output runs/run.dpr.squad-test.bm25.trec
```


To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.squad-test.bm25.trec \
                                                                --output runs/run.dpr.squad-test.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.squad-test.bm25.json --topk 20 100
Top20  accuracy: 0.7109
Top100 accuracy: 0.8184
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoded-queries dpr_multi-squad-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 2.00 \
                             run    --topics dpr-squad-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.squad-test.multi.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.squad-test.multi.bf.bm25.trec \
                                                                --output runs/run.dpr.squad-test.multi.bf.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.squad-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.7511
Top100 accuracy: 0.8437
```

## Natural Questions (NQ) with DPR-Single

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-single-nq-bf \
                             --encoded-queries dpr_single_nq-nq-test \
                             --output runs/run.dpr.nq-test.single.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-single-nq-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.nq-test.single.bf.trec \
                                                                --output runs/run.dpr.nq-test.single.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.nq-test.single.bf.json --topk 20 100
Top20	accuracy: 0.8006
Top100	accuracy: 0.8610
```

**Hybrid dense-sparse retrieval**:

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-single-nq-bf \
                                    --encoded-queries dpr_single_nq-nq-test \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.2 \
                             run    --topics dpr-nq-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.nq-test.single.bf.bm25.trec 
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-single-nq-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.dpr.nq-test.single.bf.bm25.trec \
                                                                --output runs/run.dpr.nq-test.single.bf.bm25.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.dpr.nq-test.single.bf.bm25.json --topk 20 100
Top20	accuracy: 0.8288
Top100	accuracy: 0.8837
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-21 (commit [`2adbf1`](https://github.com/castorini/pyserini/commit/2adbf1bedcfbfbeb3a5fbad71fad95feaab2b641))
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-06-09 (commit [`5e8b917`](https://github.com/castorini/pyserini/commit/5e8b917dc806486da94a9bf1eb15b24e79c13479))
+ Results reproduced by [@mayankanand007](https://github.com/mayankanand007) on 2021-07-28 (commit [`b2b3538`](https://github.com/castorini/pyserini/commit/b2b3538d8d3ec5a8b2638457c16f02a8ced068b7))

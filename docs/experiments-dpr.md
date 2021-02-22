# Pyserini: Replicating Facbook's DPR Results

This guide provides replication instructions for the following dense retrieval work:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih, [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/), _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2929.

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.
These experiments were performed on a Linux machine running Ubuntu 18.04 with `faiss-cpu==1.6.5`,  `transformers==4.0.0`, `torch==1.7.1`, and `tensorflow==2.4.0`; results have also been replicated on macOS 10.14.6 with the same Python dependency versions.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a replicability perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## Summary

Here's how our results stack up against results reported in the paper:

| Dataset     | Method        | Top20 (paper) | Top20 (us) | Top100 (paper) | Top100 (us) |
|-------------|---------------|---------------|------------|----------------|-------------|
| NQ          | DPR           | 79.4          | 79.5       | 86.0           | 86.1        |
| NQ          | BM25          | 59.1          | 62.9       | 73.7           | 78.3        |
| NQ          | Hybrid (1.30) | 78.0          | 82.6       | 83.9           | 88.6        |
| TriviaQA    | DPR           | 78.8          | 78.9       | 84.7           | 84.8        |
| TriviaQA    | BM25          | 66.9          | 76.4       | 76.7           | 83.2        |
| TriviaQA    | Hybrid (0.95) | 79.9          | 82.6       | 84.4           | 86.5        |
| WQ          | DPR           | 75.0          | 75.0       | 82.9           | 83.0        |
| WQ          | BM25          | 55.0          | 62.4       | 71.1           | 75.5        |
| WQ          | Hybrid (0.95) | 74.7          | 77.1       | 82.3           | 84.4        |
| CuratedTREC | DPR           | 89.1          | 88.8       | 93.9           | 93.4        |
| CuratedTREC | BM25          | 70.9          | 80.7       | 84.1           | 89.9        |
| CuratedTREC | Hybrid (1.05) | 88.5          | 90.1       | 94.1           | 95.0        |
| SQuAD       | DPR           | 51.6          | 52.0       | 67.6           | 67.7        |
| SQuAD       | BM25          | 68.8          | 71.1       | 80.0           | 81.8        |
| SQuAD       | Hybrid (2.00) | 66.2          | 75.1       | 78.6           | 84.4        |

## Natural Questions (NQ)

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.nq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.nq-test.multi.bf.trec \
                                                           --output runs/run.dpr.nq-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.nq-test.multi.bf.json --topk 20 100
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
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.nq-test.bm25.trec \
                                                           --output runs/run.dpr.nq-test.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.nq-test.bm25.json --topk 20 100
Top20  accuracy: 0.6294
Top100 accuracy: 0.7825
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-nq-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.nq-test.multi.bf.bm25.trec 
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.nq-test.multi.bf.bm25.trec \
                                                           --output runs/run.dpr.nq-test.multi.bf.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.nq-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.8260
Top100 accuracy: 0.8859
```

## TriviaQA

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.trivia-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.trivia-test.multi.bf.trec \
                                                           --output runs/run.dpr.trivia-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.trivia-test.multi.bf.json --topk 20 100
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
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.trivia-test.bm25.trec \

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.trivia-test.bm25.json --topk 20 100
Top20  accuracy: 0.7641
Top100 accuracy: 0.8315
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-trivia-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.trivia-test.multi.bf.bm25.trec 
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.trivia-test.multi.bf.bm25.trec \
                                                           --output runs/run.dpr.trivia-test.multi.bf.bm25.json 

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.trivia-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.8264
Top100 accuracy: 0.8655
```

## WebQuestions (WQ)

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-wq-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.wq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-wq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.wq-test.multi.bf.trec \
                                                           --output runs/run.dpr.wq-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.wq-test.multi.bf.json --topk 20 100
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
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-wq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.wq-test.bm25.trec \
                                                           --output runs/run.dpr.wq-test.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.wq-test.bm25.json --topk 20 100
Top20  accuracy: 0.6240
Top100 accuracy: 0.7549
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-wq-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.wq-test.multi.bf.bm25.trec 
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-wq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.wq-test.multi.bf.bm25.trec \
                                                           --output runs/run.dpr.wq-test.multi.bf.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.wq-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.7712
Top100 accuracy: 0.8440
```

## CuratedTREC

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-curated-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.curated-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.curated-test.multi.bf.trec \
                                                           --output runs/run.dpr.curated-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.curated-test.multi.bf.json --topk 20 100 --regex
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
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.curated-test.bm25.trec \
                                                           --output runs/run.dpr.curated-test.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.curated-test.bm25.json --topk 20 100 --regex
Top20  accuracy: 0.8069
Top100 accuracy: 0.8991
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.05 \
                             run    --topics dpr-curated-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.curated-test.multi.bf.bm25.trec 
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.curated-test.multi.bf.bm25.trec \
                                                           --output runs/run.dpr.curated-test.multi.bf.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.curated-test.multi.bf.bm25.json --topk 20 100 --regex
Top20  accuracy: 0.9006
Top100 accuracy: 0.9496
```

## SQuAD

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-squad-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.squad-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-squad-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.squad-test.multi.bf.trec \
                                                           --output runs/run.dpr.squad-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.squad-test.multi.bf.json --topk 20 100
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
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-squad-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.squad-test.bm25.trec \
                                                           --output runs/run.dpr.squad-test.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.squad-test.bm25.json --topk 20 100
Top20  accuracy: 0.7109
Top100 accuracy: 0.8184
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
$ python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 2.00 \
                             run    --topics dpr-squad-test \
                                    --batch-size 36 --threads 12 \
                                    --output runs/run.dpr.squad-test.multi.bf.bm25.trec 
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-squad-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.squad-test.multi.bf.bm25.trec \
                                                           --output runs/run.dpr.squad-test.multi.bf.bm25.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.squad-test.multi.bf.bm25.json --topk 20 100
Top20  accuracy: 0.7511
Top100 accuracy: 0.8437
```

## Replication Log

+ Results replicated by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))

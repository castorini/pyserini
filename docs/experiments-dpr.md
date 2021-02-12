# Pyserini: Replicating Facbook's DPR Results

This guide provides replication instructions for the following dense retrieval work:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih, [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/), _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2929.

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.

## Summary

Here's how our results stack up against results reported in the paper:

| Dataset     | Method        | Top20 (paper) | Top20 (us) | Top100 (paper) | Top100 (us) |
|-------------|---------------|---------------|------------|----------------|-------------|
| NQ          | BM25          | 59.1          | 62.9       | 73.7           | 78.3        |
| NQ          | DPR           | 79.4          | 79.5       | 86.0           | 86.1        |
| NQ          | Hybrid (1.30) | 78.0          | 82.6       | 83.9           | 88.6        |
| TriviaQA    | BM25          | 66.0          | 76.4       | 76.7           | 83.2        |
| TriviaQA    | DPR           | 78.8          | 78.8       | 84.7           | 84.8        |
| TriviaQA    | Hybrid (0.95) | 79.9          | 82.6       | 84.4           | 86.5        |
| WQ          | BM25          | 55.0          | 62.4       | 71.1           | 75.5        |
| WQ          | DPR           | 75.0          | 75.0       | 82.9           | 83.0        |
| WQ          | Hybrid (0.95) | 74.7          | 77.1       | 82.3           | 84.4        |
| CuratedTREC | BM25          | 70.9          | 80.7       | 84.1           | 89.9        |
| CuratedTREC | DPR           | 89.1          | 88.8       | 93.9           | 93.4        |
| CuratedTREC | Hybrid (1.05) | 88.5          | 90.1       | 94.1           | 95.0        |
| SQuAD       | BM25          | 68.8          | 71.1       | 80.0           | 81.8        |
| SQuAD       | DPR           | 51.6          | 52.0       | 67.6           | 67.7        |
| SQuAD       | Hybrid (2.00) | 66.2          | 75.1       | 78.6           | 84.3        |

## Natural Questions (NQ)

**DPR retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.nq-test.multi.bf.trec \
                             --batch 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.nq-test.multi.bf.trec \
                                                           --output runs/run.dpr.nq-test.multi.bf.json

$ python tools/scripts/dpr/evaluate_retrieval.py --retrieval runs/run.dpr.nq-test.multi.bf.json --topk 20 100
Top20  accuracy: 0.7947368421052632
Top100 accuracy: 0.8609418282548477
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
Top20  accuracy: 0.6293628808864266
Top100 accuracy: 0.7825484764542936
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
Top20  accuracy: 0.8260387811634349
Top100 accuracy: 0.8858725761772853
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
Top20  accuracy: 0.7887386192875453
Top100 accuracy: 0.847874127110404
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
Top20  accuracy: 0.7640767258905684
Top100 accuracy: 0.8315212587288959
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
Top20  accuracy: 0.8263944135065854
Top100 accuracy: 0.8654645098559179
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
Top20  accuracy: 0.750492125984252
Top100 accuracy: 0.8297244094488189
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
Top20  accuracy: 0.6240157480314961
Top100 accuracy: 0.7549212598425197
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
Top20  accuracy: 0.7711614173228346
Top100 accuracy: 0.843996062992126
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
Top20  accuracy: 0.8876080691642652
Top100 accuracy: 0.9337175792507204
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
Top20  accuracy: 0.8069164265129684
Top100 accuracy: 0.899135446685879
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
Top20  accuracy: 0.9005763688760807
Top100 accuracy: 0.9495677233429395
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
Top20  accuracy: 0.5198675496688742
Top100 accuracy: 0.6772942289498581
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
Top20  accuracy: 0.710879848628193
Top100 accuracy: 0.8183538315988647
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
Top20  accuracy: 0.7510879848628192
Top100 accuracy: 0.8437086092715231
```

## Replication Log

+ Results replicated by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))

## DPR Retrieval

This guide provides replication instructions for the following dense retrieval work:

Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih, [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906), Preprint 2020.

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.


## Natural Questions
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics dpr_nq_test \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output runs/run.dpr.nq.multi.bf.trec \
                             --batch 36 --threads 12
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_nq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.nq.multi.bf.trec \
                                                           --output runs/run.dpr.nq.multi.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.nq.multi.bf.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.nq.multi.bf.json --topk 100
Top20  accuracy: 0.7947368421052632
Top100 accuracy: 0.8609418282548477
```

### BM25 retrieval

```bash
$ python -m pyserini.search --topics dpr_nq_test \
                             --index wikipedia-dpr \
                             --output runs/run.nq-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_nq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.nq-test.bm25.trec \
                                                           --output runs/run.nq-test.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-test.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-test.bm25.json --topk 100
Top20  accuracy: 0.6293628808864266
Top100 accuracy: 0.7825484764542936
```

In original paper, the corresponding results are:
```bash
Top20: 59.1
Top100: 73.7
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, brute force index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-multi-bf \
                                     --encoder facebook/dpr-question_encoder-multiset-base \
                                     --batch-size 72 --threads 72 \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics dpr_nq_test \
                                  --output runs/run.nq-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_nq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.nq-test.dpr.bf.bm25.trec  \
                                                           --output runs/run.nq-test.dpr.bf.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-test.dpr.bf.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-test.dpr.bf.bm25.json --topk 100
Top20  accuracy: 0.8088642659279779
Top100 accuracy: 0.8700831024930747
```

## TriviaQA
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics dpr_trivia_test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.trivia.multi.bf.trec \
                             --batch 72 --threads 72
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_trivia_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.trivia.multi.bf.trec \
                                                           --output runs/run.dpr.trivia.multi.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.trivia.multi.bf.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.trivia.multi.bf.json --topk 100
Top20  accuracy: 0.7887386192875453
Top100 accuracy: 0.847874127110404
```

### BM25 retrieval

```bash
$ python -m pyserini.search --topics dpr_trivia_test \
                             --index wikipedia-dpr \
                             --output runs/run.trivia-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_trivia_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.trivia-test.bm25.trec \
                                                           --output runs/run.trivia-test.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.trivia-test.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.trivia-test.bm25.json --topk 100
Top20  accuracy: 0.7640767258905684
Top100 accuracy: 0.8315212587288959
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, brute force index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-multi-bf \
                                     --batch-size 72 --threads 72 \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics dpr_trivia_test \
                                  --output runs/run.trivia-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_trivia_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.trivia-test.dpr.bf.bm25.trec  \
                                                           --output runs/run.trivia-test.dpr.bf.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.trivia-test.dpr.bf.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.trivia-test.dpr.bf.bm25.json --topk 100
Top20  accuracy: 0.8061522142667727
Top100 accuracy: 0.854680456112437
```

## Web Questions
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics dpr_wq_test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.wq.multi.bf.trec \
                             --batch 72 --threads 72
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_wq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.wq.multi.bf.trec \
                                                           --output runs/run.dpr.wq.multi.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.wq.multi.bf.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.wq.multi.bf.json --topk 100
Top20  accuracy: 0.750492125984252
Top100 accuracy: 0.8297244094488189
```

### BM25 retrieval

```bash
$ python -m pyserini.search --topics dpr_wq_test \
                             --index wikipedia-dpr \
                             --output runs/run.wq-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_wq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.wq-test.bm25.trec \
                                                           --output runs/run.wq-test.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.wq-test.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.wq-test.bm25.json --topk 100
Top20  accuracy: 0.6240157480314961
Top100 accuracy: 0.7549212598425197
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, brute force index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-multi-bf \
                                     --batch-size 72 --threads 72 \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics dpr_wq_test \
                                  --output runs/run.wq-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_wq_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.wq-test.dpr.bf.bm25.trec  \
                                                           --output runs/run.wq-test.dpr.bf.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.wq-test.dpr.bf.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.wq-test.dpr.bf.bm25.json --topk 100
Top20  accuracy: 0.7578740157480315
Top100 accuracy: 0.8321850393700787
```

## Curated TREC
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics dpr_curated_test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.curated.multi.bf.trec \
                             --batch 72 --threads 72
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_curated_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.curated.multi.bf.trec \
                                                           --output runs/run.dpr.curated.multi.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.curated.multi.bf.json --topk 20 --regex
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.curated.multi.bf.json --topk 100 --regex
Top20  accuracy: 0.8876080691642652
Top100 accuracy: 0.9337175792507204
```

### BM25 retrieval

```bash
$ python -m pyserini.search --topics dpr_curated_test \
                             --index wikipedia-dpr \
                             --output runs/run.curated-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_curated_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.curated-test.bm25.trec \
                                                           --output runs/run.curated-test.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.curated-test.bm25.json --topk 20 --regex
$ python scripts/dpr/evaluate.py --retrieval runs/run.curated-test.bm25.json --topk 100 --regex
Top20  accuracy: 0.8069164265129684
Top100 accuracy: 0.899135446685879
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, brute force index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-multi-bf \
                                     --batch-size 72 --threads 72 \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics dpr_curated_test \
                                  --output runs/run.curated-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_curated_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.curated-test.dpr.bf.bm25.trec  \
                                                           --output runs/run.curated-test.dpr.bf.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.curated-test.dpr.bf.bm25.json --topk 20 --regex
$ python scripts/dpr/evaluate.py --retrieval runs/run.curated-test.dpr.bf.bm25.json --topk 100 --regex
Top20  accuracy: 0.8933717579250721
Top100 accuracy: 0.9351585014409222
```

## SQUAD
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics dpr_squad_test \
                             --index wikipedia-dpr-multi-bf \
                             --output runs/run.dpr.squad.multi.bf.trec \
                             --batch 72 --threads 72
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_squad_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.squad.multi.bf.trec \
                                                           --output runs/run.dpr.squad.multi.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.squad.multi.bf.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.dpr.squad.multi.bf.json --topk 100
Top20  accuracy: 0.5198675496688742
Top100 accuracy: 0.6772942289498581
```

### BM25 retrieval

```bash
$ python -m pyserini.search --topics dpr_squad_test \
                             --index wikipedia-dpr \
                             --output runs/run.squad-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_squad_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.squad-test.bm25.trec \
                                                           --output runs/run.squad-test.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.squad-test.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.squad-test.bm25.json --topk 100
Top20  accuracy: 0.710879848628193
Top100 accuracy: 0.8183538315988647
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, brute force index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-multi-bf \
                                     --batch-size 72 --threads 72 \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics dpr_squad_test \
                                  --output runs/run.squad-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics dpr_squad_test \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.squad-test.dpr.bf.bm25.trec  \
                                                           --output runs/run.squad-test.dpr.bf.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.squad-test.dpr.bf.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.squad-test.dpr.bf.bm25.json --topk 100
Top20  accuracy: 0.5818353831598865
Top100 accuracy: 0.7264900662251655
```

## Summary
| Dataset     | Method | Top20 (paper) | Top20 (us) | Top100 (paper) | Top100 (us) |
|-------------|--------|---------------|------------|----------------|-------------|
| NQ          | BM25   | 59.1          | 62.9       | 73.7           | 78.3        |
| NQ          | DPR    | 79.4          | 79.5       | 86.0           | 86.1        |
| NQ          | Hybrid | 78.0          | 80.9       | 83.9           | 87.0        |
| TriviaQA    | BM25   | 66.0          | 76.4       | 76.7           | 83.2        |
| TriviaQA    | DPR    | 78.8          | 78.8       | 84.7           | 84.8        |
| TriviaQA    | Hybrid | 79.9          | 80.6       | 84.4           | 85.5        |
| WQ          | BM25   | 55.0          | 62.4       | 71.1           | 75.5        |
| WQ          | DPR    | 75.0          | 75.0       | 82.9           | 83.0        |
| WQ          | Hybrid | 74.7          | 75.8       | 82.3           | 83.2        |
| CuratedTREC | BM25   | 70.9          | 80.7       | 84.1           | 89.9        |
| CuratedTREC | DPR    | 89.1          | 88.8       | 93.9           | 93.4        |
| CuratedTREC | Hybrid | 88.5          | 89.3       | 94.1           | 93.5        |
| SQUAD       | BM25   | 68.8          | 71.1       | 80.0           | 81.8        |
| SQUAD       | DPR    | 51.6          | 52.0       | 67.6           | 67.7        |
| SQUAD       | Hybrid | 66.2          | 58.2       | 78.6           | 72.6        |


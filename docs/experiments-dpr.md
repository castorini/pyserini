## DPR Retrieval

This guide provides replication instructions for the following dense retrieval work:

Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih, [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906), Preprint 2020.

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.


## Natural Questions
### DPR retrieval
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics nq_test_dpr \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output runs/run.dpr.nq.multi.bf.trec \
                             --batch 36 --threads 12
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_test_dpr \
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
$ python -m pyserini.search --topics nq_test_dpr \
                             --index wikipedia-dpr \
                             --output runs/run.nq-test.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_test_dpr \
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
                             run  --topics nq_test_dpr \
                                  --output runs/run.nq-test.dpr.bf.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_test_dpr \
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

## DPR Retrieval

This guide provides replication instructions for the following dense retrieval work:

Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih, [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906), Preprint 2020.

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.

### Retrieval with HNSW index
```bash
$ python -m pyserini.dsearch --topics nq_dev_dpr \
                             --index wikipedia-dpr-hnsw \
                             --output runs/run.dpr.hnsw.trec 
```
The retrieval will use pre-encoded queries by default. To evaluate with on-the-fly query encoding with the pretrained encoder
on [Hugging Face](https://huggingface.co/facebook/dpr-question_encoder-single-nq-base/tree/main) add
`--encoder facebook/dpr-question_encoder-single-nq-base`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_dev_dpr \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.hnsw.trec \
                                                           --output runs/retrieval.dpr.hnsw.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/retrieval.dpr.hnsw.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/retrieval.dpr.hnsw.json --topk 100
Top20  accuracy: 0.7800616649537513
Top100 accuracy: 0.8480073084389631
```

### Retrieval with brute force index
Run DPR retrieval with Wikipedia brute force index

```bash
$ python -m pyserini.dsearch --topics nq_dev_dpr \
                             --index wikipedia-dpr-bf \
                             --output runs/run.dpr.bf.trec \
                             --batch 36 --threads 12
```
The retrieval will use pre-encoded queries by default. To evaluate with on-the-fly query encoding with the pretrained encoder
on [Hugging Face](https://huggingface.co/facebook/dpr-question_encoder-single-nq-base/tree/main) add
`--encoder facebook/dpr-question_encoder-single-nq-base`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_dev_dpr \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.dpr.bf.trec \
                                                           --output runs/retrieval.dpr.bf.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/retrieval.dpr.bf.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/retrieval.dpr.bf.json --topk 100
Top20  accuracy: 0.7813178029005368
Top100 accuracy: 0.8499486125385406
```

In original paper, the corresponding results are:
```bash
Top20  accuracy: 78.4
Top100 accuracy: 85.4
```
However, by running retrieval and evaluation from [DPR repo](https://github.com/facebookresearch/DPR),
via [this](https://github.com/efficientqa/retrieval-based-baselines/blob/master/run_inference.py).

we are getting:
```bash
Top20  accuracy: 0.7813178029005368
Top100 accuracy: 0.8498344181797419
```
which is closer to our implementation.

### BM25 retrieval

```bash
$ python -m pyserini.search --topics nq_dev_dpr \
                             --index wikipedia-dpr \
                             --output runs/run.nq-dev.bm25.trec
```


To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_dev_dpr \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.nq-dev.bm25.trec \
                                                           --output runs/run.nq-dev.bm25.json
```

Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-dev.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-dev.bm25.json --topk 100
Top20  accuracy: 0.6233870046819687
Top100 accuracy: 0.7601918465227818
```

In original paper, the corresponding results are:
```bash
Top20: 59.1
Top100: 73.7
```

### Hybrid Dense-Sparse Retrieval
Hybrid
- dense retrieval with DPR, HNSW index.
- sparse retrieval with BM25.

```bash
$ python -m pyserini.hsearch   dense --index wikipedia-dpr-hnsw \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.24 \
                             run  --topics nq_dev_dpr \
                                  --output runs/run.nq-dev.dpr.hnsw.bm25.trec 
```

To evaluate convert the TREC style run file to retrieval result file in `json` format
```bash
$ python -m scripts.dpr.convert_trec_run_to_retrieval_json --topics nq_dev_dpr \
                                                           --index wikipedia-dpr \
                                                           --input runs/run.nq-dev.dpr.hnsw.bm25.trec  \
                                                           --output runs/run.nq-dev.dpr.hnsw.bm25.json
```
Evaluate
```bash
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-dev.dpr.hnsw.bm25.json --topk 20
$ python scripts/dpr/evaluate.py --retrieval runs/run.nq-dev.dpr.hnsw.bm25.json --topk 100
Top20  accuracy: 0.7933082105743976
Top100 accuracy: 0.8563434966312664
```

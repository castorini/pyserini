# Pyserini: Aggretriever for MS MARCO (V1) Collections

This guide provides instructions to reproduce the Aggretriever dense retrieval model described in the following paper:

> Sheng-Chieh Lin, Minghan Li, and Jimmy Lin. [Aggretriever: A Simple Approach to Aggregate Textual Representation for Robust Dense Passage Retrieval.](https://arxiv.org/abs/2208.00511) arXiv:2208.00511, July 2022. 

Note that we often observe minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.
The models, indexes and encoded queries are now on orca so we use the local path temporarily.

## MS MARCO Passage Ranking

Summary of results:

| Condition                                              | MRR@10 |    MAP | Recall@1000 |
|:-------------------------------------------------------|-------:|-------:|------------:|
| Aggretriever-DistilBERT                                | 0.3412 | 0.3478 |      0.9604 |
| Aggretriever-coCondenser                               | 0.3619 | 0.3669 |      0.9735 |

### Aggretriever-DistilBERT Dense Retrieval

Dense retrieval with Aggretriever-DistilBERT, brute-force index:

```bash
python -m pyserini.search.faiss \
  --index msmarco-v1-passage.aggretriever-distilbert \
  --topics msmarco-passage-dev-subset \
  --encoded-queries aggretriever-distilbert-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.distilbert-agg.bf.tsv \
  --output-format trec \
  --batch-size 36 --threads 12
```

Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded. As an alternative, replace `--encoded-queries aggretriever-distilbert-msmarco-passage-dev-subset` with `--encoder castorini/aggretriever-distilbert` to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process.

To evaluate:

```bash
$ python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset \
    runs/run.msmarco-passage.distilbert-agg.bf.tsv

#####################
MRR @10: 0.3412
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.distilbert-agg.bf.tsv

map                     all     0.3478
recall_1000             all     0.9604
```

### Aggretriever-coCondenser Dense Retrieval

Dense retrieval with Aggretriever-coCondenser, brute-force index:

```bash
python -m pyserini.search.faiss \
  --index msmarco-v1-passage.aggretriever-distilbert \
  --topics msmarco-passage-dev-subset \
  --encoded-queries aggretriever-cocondenser-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.cocondenser-agg.bf.tsv \
  --output-format trec \
  --batch-size 36 --threads 12
```

Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded. As an alternative, replace `--encoded-queries aggretriever-cocondenser-msmarco-passage-dev-subset` with `--encoder castorini/aggretriever-cocondenser` to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process.

To evaluate:

```bash
$ python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset \
    runs/run.msmarco-passage.cocondenser-agg.bf.tsv

#####################
MRR @10: 0.3619
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.cocondenser-agg.bf.tsv

map                     all     0.3669
recall_1000             all     0.9735
```



## Reproduction Log[*](reproducibility.md)


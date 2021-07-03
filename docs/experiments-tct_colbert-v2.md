# Pyserini: Reproducing TCT-ColBERT-V2 Results

This guide provides instructions to reproduce the family of TCT-ColBERT-V2 dense retrieval models described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://cs.uwaterloo.ca/~jimmylin/publications/Lin_etal_2021_RepL4NLP.pdf) _RepL4NLP 2021_.

Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## MS MARCO Passage Ranking

Summary of results (figures from the paper are in parentheses):

| Condition | MRR@10 (paper) | MAP | Recall@1000 |
|:----------|-------:|----:|------------:|
| TCT_ColBERT-V2 (brute-force index) |  0.3440 (0.3435) | 0.3509 | 0.9670 |
| TCT_ColBERT-V2-HN (brute-force index) |  0.3543 (0.3540) | 0.3608 | 0.9708 |
| TCT_ColBERT-V2-HN+ (brute-force index) | 0.3585 (0.3586) | 0.3645 | 0.9695 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BoW BM25 | 0.3682 (0.3687)  | 0.3737 | 0.9707 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BM25 w/ doc2query-T5 | 0.3731 (0.3747) | 0.3789 | 0.9759 |

The slight differences can be attributed to TensorFlow implementations in the published paper and PyTorch implementations here in this reproduction guide.

## TCT_ColBERT-V2

Dense retrieval with TCT-ColBERT, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-bf \
                             --encoded-queries tct_colbert-v2-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2.bf.tsv \
                             --output-format msmarco
```
Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded.
As an alternative, to perform "on-the-fly" query encoding, see additional instructions below.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2.bf.tsv
#####################
MRR @10: 0.3440
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2.bf.trec
map                     all     0.3509
recall_1000             all     0.9670
```

## TCT_ColBERT-V2-HN

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hn-bf \
                             --encoded-queries tct_colbert-v2-hn-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv \
                             --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv
#####################
MRR @10: 0.3543
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec
map                     all     0.3608
recall_1000             all     0.9708
```

## TCT_ColBERT-V2-HN+

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hnp-bf \
                             --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv \
                             --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv
#####################
MRR @10: 0.3585
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec
map                     all     0.3645
recall_1000             all     0.9695
```

To perform on-the-fly query encoding with our [pretrained encoder model](https://huggingface.co/castorini/tct_colbert-v2-hnp-msmarco) use the option `--encoder castorini/tct_colbert-v2-hnp-msmarco`.
Query encoding will run on the CPU by default.
To perform query encoding on the GPU, use the option `--device cuda:0`.


### Hybrid Dense-Sparse Retrieval with TCT_ColBERT-V2-HN+

Hybrid retrieval with dense-sparse representations (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BM25 `msmarco-passage` (i.e., default bag-of-words) index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.06 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv
#####################
MRR @10: 0.3682
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec
map                   	all	0.3737
recall_1000           	all	0.9707
```

Follow the same instructions above to perform on-the-fly query encoding.

Hybrid retrieval with dense-sparse representations (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.1 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv
#####################
MRR @10: 0.3731
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec
map                   	all	0.3789
recall_1000           	all	0.9759
```

Follow the same instructions above to perform on-the-fly query encoding.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-01 (commit [`b1576a2`](https://github.com/castorini/pyserini/commit/b1576a2c3e899349be12e897f92f3ad75ec82d6f))

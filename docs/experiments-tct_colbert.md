# Pyserini: TCT-ColBERT for MS MARCO (V1) Collections

This guide provides instructions to reproduce the TCT-ColBERT dense retrieval model described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [Distilling Dense Representations for Ranking using Tightly-Coupled Teachers.](https://arxiv.org/abs/2010.11386) arXiv:2010.11386, October 2020. 

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## MS MARCO Passage Ranking

Summary of results:

| Condition | MRR@10 | MAP | Recall@1000 |
|:----------|-------:|----:|------------:|
| TCT-ColBERT (brute-force index) | 0.3350 | 0.3416 | 0.9640 |
| TCT-ColBERT (HNSW index) | 0.3345 | 0.3410 | 0.9618 |
| TCT-ColBERT (brute-force index) + BoW BM25 | 0.3529 | 0.3594 | 0.9698 |
| TCT-ColBERT (brute-force index) + BM25 w/ doc2query-T5 | 0.3647 | 0.3711 | 0.9751 |

### Dense Retrieval

Dense retrieval with TCT-ColBERT, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert.bf.tsv \
                             --output-format msmarco
```

Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded.
As an alternative, to perform "on-the-fly" query encoding, see additional instructions below.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.tsv
#####################
MRR @10: 0.3350
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert.bf.tsv --output runs/run.msmarco-passage.tct_colbert.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.trec
map                     all     0.3416
recall_1000             all     0.9640
```

To perform on-the-fly query encoding with our [pretrained encoder model](https://huggingface.co/castorini/tct_colbert-msmarco/tree/main) use the option `--encoder castorini/tct_colbert-msmarco`.
Query encoding will run on the CPU by default.
To perform query encoding on the GPU, use the option `--device cuda:0`.

Dense retrieval with TCT-ColBERT, HNSW index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-hnsw \
                             --output runs/run.msmarco-passage.tct_colbert.hnsw.tsv \
                             --output-format msmarco 
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.hnsw.tsv
#####################
MRR @10: 0.3345
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert.hnsw.tsv --output runs/run.msmarco-passage.tct_colbert.hnsw.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.hnsw.trec
map                     all     0.3411
recall_1000             all     0.9618
```

Follow the same instructions above to perform on-the-fly query encoding.
The caveat about minor differences in score applies here as well.

### Hybrid Dense-Sparse Retrieval

Hybrid retrieval with dense-sparse representations (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BM25 `msmarco-passage` (i.e., default bag-of-words) index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv
#####################
MRR @10: 0.3529
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv --output runs/run.msmarco-passage.tct_colbert.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.bm25.trec
map                   	all	0.3594
recall_1000           	all	0.9698
```

Follow the same instructions above to perform on-the-fly query encoding.
The caveat about minor differences in score applies here as well.

Hybrid retrieval with dense-sparse representations (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv
#####################
MRR @10: 0.3647
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
map                   	all	0.3711
recall_1000           	all	0.9751
```

Follow the same instructions above to perform on-the-fly query encoding.
The caveat about minor differences in score applies here as well.

## MS MARCO Document Ranking

Summary of results:

| Condition | MRR@100 | MAP | Recall@100 |
|:----------|-------:|----:|------------:|
| TCT-ColBERT (brute-force index) | 0.3323 | 0.3323 | 0.8664 |
| TCT-ColBERT (brute-force index) + BoW BM25 | 0.3701 | 0.3701 | 0.9020 |
| TCT-ColBERT (brute-force index) + BM25 w/ doc2query-T5 | 0.3784 | 0.3784 | 0.9081 |

Although this is not described in the paper, we have adapted TCT-ColBERT to the MS MARCO document ranking task in a zero-shot manner.
Documents in the MS MARCO document collection are first segmented, and each segment is then encoded with the TCT-ColBERT model trained on trained on MS MARCO passages.
The score of a document is the maximum score of all passages in that document.

Dense retrieval using a brute force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-tct_colbert-bf \
                             --encoded-queries tct_colbert-msmarco-doc-dev \
                             --output runs/run.msmarco-doc.passage.tct_colbert.txt \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --output-format msmarco \
                             --batch-size 36 \
                             --threads 12
```

Replace `--encoded-queries` by `--encoder castorini/tct_colbert-msmarco` for on-the-fly query encoding.

To compute the official metric MRR@100 using the official evaluation scripts:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.passage.tct_colbert.txt
#####################
MRR @100: 0.3323
#####################
```

To compute additional metrics using `trec_eval`, we first need to convert the run to TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc.passage.tct_colbert.txt --output runs/run.msmarco-doc.passage.tct_colbert.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.passage.tct_colbert.trec
map                   	all	0.3323
recall_100            	all	0.8664
```

Dense-sparse hybrid retrieval (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BoW BM25 index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-doc-dev \
                             sparse --index msmarco-doc-per-passage \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

Replace `--encoded-queries` by `--encoder castorini/tct_colbert-msmarco` for on-the-fly query encoding.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv
#####################
MRR @100: 0.3701
QueriesRanked: 5193
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv --output runs/run.msmarco-doc.tct_colbert.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.tct_colbert.bf.bm25.trec
map                   	all	0.3701
recall_100            	all	0.9020
```

Dense-sparse hybrid retrieval (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-doc-dev \
                             sparse --index msmarco-doc-expanded-per-passage \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

Replace `--encoded-queries` by `--encoder castorini/tct_colbert-msmarco` for on-the-fly query encoding.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv
#####################
MRR @100: 0.3784
QueriesRanked: 5193
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv --output runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.trec
map                   	all	0.3784
recall_100            	all	0.9081
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7f`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-25 (commit [`854c193`](https://github.com/castorini/pyserini/commit/854c1930ba00819245c0a9fbcf2090ce14db4db0))
+ Results reproduced by [@isoboroff](https://github.com/isoboroff) on 2021-05-14 (PyPI [`0.12.0`](https://pypi.org/project/pyserini/0.12.0/)
+ Results reproduced by [@jingtaozhan](https://github.com/jingtaozhan) on 2021-05-15 (commit [`53d8d3c`](https://github.com/castorini/pyserini/commit/53d8d3cbb78c88a23ce132a42b0396caad7d2e0f))
+ Results reproduced by [@jmmackenzie](https://github.com/jmmackenzie) on 2021-05-17 (PyPI [`0.12.0`](https://pypi.org/project/pyserini/0.12.0/))
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-06-12 (commit [`f614111`](https://github.com/castorini/pyserini/commit/f614111f014b7490f75e585e610f64f769164dd2))

# Pyserini: Replicating TCT-ColBERT Results

This guide provides replication instructions for the TCT-ColBERT dense retrieval model described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [Distilling Dense Representations for Ranking using Tightly-Coupled Teachers.](https://arxiv.org/abs/2010.11386) arXiv:2010.11386, October 2020. 

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.
These experiments were performed on a Linux machine running Ubuntu 18.04 with `faiss-cpu==1.6.5`, `transformers==4.0.0`, `torch==1.7.1`, and `tensorflow==2.4.0`; results have also been replicated on macOS 10.14.6 with the same Python dependency versions.

## MS MARCO Passage Ranking

Summary of results:

| Condition | MRR@10 | MAP | Recall@1000 |
|:----------|-------:|----:|------------:|
| TCT-ColBERT (brute-force index) | 0.3350 | 0.3416 | 0.9640 |
| TCT-ColBERT (HNSW index) | 0.3345 | 0.3410 | 0.9618 |
| TCT-ColBERT (brute-force index) + BoW BM25 | 0.3529 | 0.3594 | 0.9698 |
| TCT-ColBERT (brute-force index) + BM25 w/ doc2query-T5 | 0.3647 | 0.3711 | 0.9751 |

## Dense Retrieval

Dense retrieval with TCT-ColBERT, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert.bf.tsv \
                             --msmarco
```

Note that to ensure maximum replicability, by default Pyserini uses pre-computed query representations that are automatically downloaded.
As an alternative, to perform "on-the-fly" query encoding, see additional instructions below.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.tsv
#####################
MRR @10: 0.3350
QueriesRanked: 6980
#####################
```

Note that we have observed minor differences in MRR@10 depending on the source of the query representations (see below; pre-computed vs. on-the-fly encoding on the CPU vs. on-the-fly encoding on the GPU).
We have also noticed differences in MRR@10 between Linux and macOS.
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a replicability perspective.
Thus, while the MS MARCO scoring scripts provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.bf.tsv --output runs/run.msmarco-passage.tct_colbert.bf.trec
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
                             --msmarco 
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.hnsw.tsv
#####################
MRR @10: 0.3345
QueriesRanked: 6980
#####################

$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.hnsw.tsv --output runs/run.msmarco-passage.tct_colbert.hnsw.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.hnsw.trec
map                     all     0.3410
recall_1000             all     0.9618
```

Follow the same instructions above to perform on-the-fly query encoding.
The caveat about minor differences in score applies here as well.

## Hybrid Dense-Sparse Retrieval

Hybrid retrieval with dense-sparse representations (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BM25 `msmarco-passage` (i.e., default bag-of-words) index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv \
                                    --batch-size 36 --threads 12 \
                                    --msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv
#####################
MRR @10: 0.3529
QueriesRanked: 6980
#####################

$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.bf.bm25.tsv --output runs/run.msmarco-passage.tct_colbert.bf.bm25.trec
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
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv \
                                    --batch-size 36 --threads 12 \
                                    --msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv
#####################
MRR @10: 0.3647
QueriesRanked: 6980
#####################

$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
map                   	all	0.3711
recall_1000           	all	0.9751
```

Follow the same instructions above to perform on-the-fly query encoding.
The caveat about minor differences in score applies here as well.

## MS MARCO Document Ranking

Summary of results:

| Condition | MRR@10 | MAP | Recall@100 |
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
                             --encoder castorini/tct_colbert-msmarco \
                             --output runs/run.msmarco-doc.passage.tct_colbert.txt \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --msmarco \
                             --batch-size 36 \
                             --threads 12
```

To compute the official metric MRR@100 using the official evaluation scripts:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.passage.tct_colbert.txt
#####################
MRR @100: 0.3323
#####################
```

To compute additional metrics using `trec_eval`, we first need to convert the run to TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-doc.passage.tct_colbert.txt --output runs/run.msmarco-doc.passage.tct_colbert.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.passage.tct_colbert.trec
map                   	all	0.3323
recall_100            	all	0.8664
```

Dense-sparse hybrid retrieval (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BoW BM25 index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-per-passage \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv
#####################
MRR @100: 0.3701
QueriesRanked: 5193
#####################

$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-doc.tct_colbert.bf.bm25.tsv --output runs/run.msmarco-doc.tct_colbert.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.tct_colbert.bf.bm25.trec
map                   	all	0.3701
recall_100            	all	0.9020
```

Dense-sparse hybrid retrieval (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-expanded-per-passage \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --msmarco
```

To evaluate:

```bash
$ python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt --run runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv
#####################
MRR @100: 0.3784
QueriesRanked: 5193
#####################

$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv --output runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.tct_colbert.bf.doc2queryT5.trec
map                   	all	0.3784
recall_100            	all	0.9081
```

## Replication Log

+ Results replicated by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))

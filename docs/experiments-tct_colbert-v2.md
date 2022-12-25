# Pyserini: TCT-ColBERTv2 for MS MARCO (V1) Collections

This guide provides instructions to reproduce the family of TCT-ColBERT-V2 dense retrieval models described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://aclanthology.org/2021.repl4nlp-1.17/) _Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)_, pages 163-173, August 2021.

Note that we often observe minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## MS MARCO Passage Ranking

Summary of results (figures from the paper are in parentheses):

| Condition                                                     | MRR@10 (paper) |    MAP | Recall@1000 |
|:--------------------------------------------------------------|---------------:|-------:|------------:|
| TCT_ColBERT-V2 (brute-force index)                            | 0.3440 (0.344) | 0.3509 |      0.9670 |
| TCT_ColBERT-V2-HN (brute-force index)                         | 0.3543 (0.354) | 0.3608 |      0.9708 |
| TCT_ColBERT-V2-HN+ (brute-force index)                        | 0.3585 (0.359) | 0.3645 |      0.9695 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BoW BM25             | 0.3682 (0.369) | 0.3737 |      0.9707 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BM25 w/ doc2query-T5 | 0.3731 (0.375) | 0.3789 |      0.9759 |

The slight differences between the reproduced scores and those reported in the paper can be attributed to TensorFlow implementations in the published paper vs. PyTorch implementations here in this reproduction guide.

### TCT_ColBERT-V2

Dense retrieval with TCT-ColBERT, brute-force index:

```bash
python -m pyserini.search.faiss \
  --index msmarco-passage-tct_colbert-v2-bf \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2.bf.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12
```
Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded.
As an alternative, to perform "on-the-fly" query encoding, see additional instructions below.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2.bf.tsv

#####################
MRR @10: 0.3440
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-passage.tct_colbert-v2.bf.tsv \
    --output runs/run.msmarco-passage.tct_colbert-v2.bf.trec

$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2.bf.trec

map                     all     0.3509
recall_1000             all     0.9670
```

### TCT_ColBERT-V2-HN

```bash
python -m pyserini.search.faiss \
  --index msmarco-passage-tct_colbert-v2-hn-bf \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-hn-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv

#####################
MRR @10: 0.3543
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv \
    --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec

$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec

map                     all     0.3608
recall_1000             all     0.9708
```

### TCT_ColBERT-V2-HN+

```bash
python -m pyserini.search.faiss \
  --index msmarco-passage-tct_colbert-v2-hnp-bf \
  --topics msmarco-passage-dev-subset \
  --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv

#####################
MRR @10: 0.3585
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv \
    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec

$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec

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
python -m pyserini.search.hybrid \
  dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
         --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  sparse --index msmarco-passage \
  fusion --alpha 0.06 \
  run    --topics msmarco-passage-dev-subset \
         --output-format msmarco \
         --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv \
         --batch-size 36 --threads 12
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv

#####################
MRR @10: 0.3682
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv \
    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec

$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec

map                   	all	0.3737
recall_1000           	all	0.9707
```

Follow the same instructions above to perform on-the-fly query encoding.

Hybrid retrieval with dense-sparse representations (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
python -m pyserini.search.hybrid \
  dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
         --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
  sparse --index msmarco-passage-expanded \
  fusion --alpha 0.1 \
  run    --topics msmarco-passage-dev-subset \
         --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv \
         --output-format msmarco \
         --batch-size 36 --threads 12
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv

#####################
MRR @10: 0.3731
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv \
    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec

$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec

map                   	all	0.3789
recall_1000           	all	0.9759
```

Follow the same instructions above to perform on-the-fly query encoding.


## MS MARCO Document Ranking

We can also perform retrieval with the models trained on the MS MARCO passage corpus (above), but applied to the MS MARCO document corpus in a zero-shot manner.

```bash
# MS MARCO doc queries (dev set)
python -m pyserini.search.faiss \
  --index msmarco-doc-tct_colbert-v2-hnp-bf \
  --topics msmarco-doc-dev \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --output-format msmarco \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 36 --threads 12

# TREC 2019 DL queries
python -m pyserini.search.faiss \
  --index msmarco-doc-tct_colbert-v2-hnp-bf \
  --topics dl19-doc \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 36 --threads 12

# TREC 2020 DL queries
python -m pyserini.search.faiss \
  --index msmarco-doc-tct_colbert-v2-hnp-bf \
  --topics dl20 \
  --encoder castorini/tct_colbert-v2-hnp-msmarco \
  --output runs/run.dl20-doc.passage.tct_colbert-v2-hnp-maxp.txt \
  --hits 1000 \
  --max-passage \
  --max-passage-hits 100 \
  --batch-size 36 --threads 12
```

Evaluation on MS MARCO doc queries (dev set):

```bash
$ python -m pyserini.eval.msmarco_doc_eval \
    --judgments msmarco-doc-dev \
    --run runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt

#####################
MRR @100: 0.3509
QueriesRanked: 5193
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
   --output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.trec

$ python -m pyserini.eval.trec_eval -c -m recall.100 -m map -m ndcg_cut.10 \
    msmarco-doc-dev runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.trec

Results:
map                     all     0.3509
recall_100              all     0.8908
ndcg_cut_10             all     0.4123
```

Evaluation TREC 2019 DL queries:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 dl19-doc \
    runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt

Results:
map                     all     0.2684
recall_100              all     0.3854
ndcg_cut_10             all     0.6593
```

Evaluation TREC 2020 DL queries:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 dl20-doc \
    runs/run.dl20-doc.passage.tct_colbert-v2-hnp-maxp.txt

Results:
map                     all     0.3914
recall_100              all     0.5964
ndcg_cut_10             all     0.6094
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-01 (commit [`b1576a`](https://github.com/castorini/pyserini/commit/b1576a2c3e899349be12e897f92f3ad75ec82d6f))
+ Results reproduced by [@yuki617](https://github.com/yuki617) on 2021-06-30 (commit [`b3f3d9`](https://github.com/castorini/pyserini/commit/b3f3d94f2d2397e684094be7e997c9fe45c6fa76))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2022-12-25 (commit [`0c495c`](https://github.com/castorini/pyserini/commit/0c495cf2999dda980eb1f85efa30a4323cef5855))

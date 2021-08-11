# Pyserini: uniCOIL for the MS MARCO V2 Collections

This page describes how to reproduce retrieval experiments with the uniCOIL model on the MS MARCO V2 collections.
Details about our model can be found in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

At present, all indexes are referenced as absolute paths on our Waterloo machine `orca`, so these results are not broadly reproducible.
We are working on figuring out ways to distribute the indexes.

## Zero-Shot uniCOIL

For the TREC 2021 Deep Learning Track, we did not have time to train a new uniCOIL model and we did not have time to finish doc2query-T5 expansions.
Thus, we applied uniCOIL without expansions in a zero-shot manner using the model trained on the MS MARCO (V1) passage corpus, described [here](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage-unicoil.md).

Specifically, we applied inference over the MS MARCO V2 [passage corpus](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#passage-collection) and [segmented document corpus](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#document-collection-segmented) to obtain the term weights.

### Passage V2 Corpus

Sparse retrieval with uniCOIL:

```bash
python -m pyserini.search --topics collections/passv2_dev_queries.tsv \
                          --encoder castorini/unicoil-noexp-msmarco-passage \
                          --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-passage-v2  \
                          --output runs/run.msmarco-passage-v2.unicoil-noexp.0shot.txt \
                          --impact \
                          --hits 1000 \
                          --batch 144 \
                          --threads 36 \
                          --min-idf 1
```

To evaluate, using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2.unicoil-noexp.0shot.txt
Results:
map                   	all	0.1306
recip_rank            	all	0.1314

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2.unicoil-noexp.0shot.txt
Results:
recall_100            	all	0.4964
recall_1000           	all	0.7013
```

Note that we evaluate MAP and MRR at a cutoff of 100 hits to match the official evaluation metrics.
However, we measure recall at both 100 and 1000 hits; the latter is a common setting for reranking.

### Document V2 Corpus

Sparse retrieval with uniCOIL:

```bash
python -m pyserini.search --topics collections/docv2_dev_queries.tsv \
                          --encoder castorini/unicoil-noexp-msmarco-passage \
                          --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-doc-v2-segmented  \
                          --output runs/run.msmarco-document-v2-segmented.unicoil-noexp.0shot.txt \
                          --impact \
                          --hits 10000 \
                          --batch 144 \
                          --threads 36 \
                          --max-passage-hits 1000 \
                          --max-passage \
                          --min-idf 1
```

For the document corpus, since we are searching the segmented version, we retrieve the top 10k _segments_ and perform MaxP to obtain the top 1000 _documents_.

To evaluate, using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.unicoil-noexp.0shot.txt
Results:
map                   	all	0.2012
recip_rank            	all	0.2032

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.unicoil-noexp.0shot.txt
Results:
recall_100            	all	0.7190
recall_1000           	all	0.8813
```

Note that we evaluate MAP and MRR at a cutoff of 100 hits to match the official evaluation metrics.
However, we measure recall at both 100 and 1000 hits; the latter is a common setting for reranking.

## Zero-Shot uniCOIL + Dense Retrieval Hybrid

Note that there are duplicate passages in MS MARCO V2 collections, so score differences might be observed due to tie-breaking effects.
For example, if we output in MS MARCO format `--output-format msmarco` and then convert to TREC format with `pyserini.eval.convert_msmarco_run_to_trec_run`, the scores will be different.

### Passage V2 Corpus

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 zero-shot):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-passage-v2-augmented \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-passage-v2 \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.46 --normalization \
                             run    --topics collections/passv2_dev_queries.tsv \
                                    --output runs/run.msmarco-passage-v2.tct_v2+unicoil-noexp.0shot.top1k.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2.tct_v2+unicoil-noexp.0shot.top1k.dev1.trec
Results:
map                   	all	0.1823
recip_rank            	all	0.1835
recall_10             	all	0.3373
recall_100            	all	0.6375
recall_1000           	all	0.8620
```

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 trained):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/j587yang/project/trec_2021/indexes/dl2021/passage/title_headings_body/tct_colbert-v2-hnp-msmarco-hn-msmarcov2-full \
                                    --encoder /store/scratch/j587yang/project/trec_2021/checkpoints/torch_ckpt/tct_colbert-v2-hnp-msmarco-hn-msmarcov2 \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-passage-v2 \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.29 --normalization \
                             run    --topics collections/passv2_dev_queries.tsv \
                                    --output runs/run.msmarco-passage-v2.tct_v2-trained+unicoil-noexp-0shot.top1k.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2.tct_v2-trained+unicoil-noexp-0shot.top1k.dev1.trec
Results:
map                   	all	0.2265
recip_rank            	all	0.2283
recall_10             	all	0.3964
recall_100            	all	0.6701
recall_1000           	all	0.8748
```

### Document V2 Corpus

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 zero-shot):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-doc-v2-segmented \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-doc-v2-segmented \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.56 --normalization \
                             run    --topics collections/docv2_dev_queries.tsv \
                                    --output runs/run.msmarco-document-v2-segmented.tct_v2+unicoil_noexp.0shot.maxp.top100.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --max-passage \
                                    --max-passage-hits 100 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100 -mmap -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_v2+unicoil_noexp.0shot.maxp.top100.dev1.trec
Results:
map                   	all	0.2550
recip_rank            	all	0.2575
recall_10             	all	0.5051
recall_100            	all	0.8082
```

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 trained):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/j587yang/project/trec_2021/indexes/dl2021/document/title_headings_body/tct_colbert-v2-hnp-msmarco-hn-msmarcov2-full-maxp \
                                    --encoder /store/scratch/j587yang/project/trec_2021/checkpoints/torch_ckpt/tct_colbert-v2-hnp-msmarco-hn-msmarcov2 \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-doc-v2-segmented \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.54 --normalization \
                             run    --topics collections/docv2_dev_queries.tsv \
                                    --output runs/run.msmarco-document-v2-segmented.tct_v2-trained+unicoil-noexp-0shot.maxp.top100.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --max-passage \
                                    --max-passage-hits 100 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100 -mmap -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_v2-trained+unicoil-noexp-0shot.maxp.top100.dev1.trec
Results:
map                   	all	0.2945
recip_rank            	all	0.2970
recall_10             	all	0.5389
recall_100            	all	0.8128
```

## Reproduction Log[*](reproducibility.md)

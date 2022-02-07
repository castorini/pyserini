# Pyserini: uniCOIL + TCT-ColBERTv2 for MS MARCO V2

This document also describes hybrid combinations of uniCOIL with our TCT-ColBERTv2 dense retrieval mode.
At present, these indexes are referenced as absolute paths on our Waterloo machine `orca`, so these results are not broadly reproducible.
We are working on figuring out ways to distribute the indexes.

Because there are duplicate passages in MS MARCO V2 collections, score differences might be observed due to tie-breaking effects.
For example, if we output in MS MARCO format `--output-format msmarco` and then convert to TREC format with `pyserini.eval.convert_msmarco_run_to_trec_run`, the scores will be different.

## Passage Ranking

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 zero-shot):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-v2-passage-augmented \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-v2-passage \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.46 --normalization \
                             run    --topics collections/passv2_dev_queries.tsv \
                                    --output runs/run.msmarco-v2-passage.tct_v2+unicoil-noexp.0shot.top1k.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-v2-passage.tct_v2+unicoil-noexp.0shot.top1k.dev1.trec
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
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-v2-passage \
                                    --encoder castorini/unicoil-noexp-msmarco-passage \
                                    --impact \
                                    --min-idf 1 \
                             fusion --alpha 0.29 --normalization \
                             run    --topics collections/passv2_dev_queries.tsv \
                                    --output runs/run.msmarco-v2-passage.tct_v2-trained+unicoil-noexp-0shot.top1k.dev1.trec \
                                    --batch-size 72 --threads 72 \
                                    --output-format trec
```

Evaluation:

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-v2-passage.tct_v2-trained+unicoil-noexp-0shot.top1k.dev1.trec
Results:
map                   	all	0.2265
recip_rank            	all	0.2283
recall_10             	all	0.3964
recall_100            	all	0.6701
recall_1000           	all	0.8748
```

## Document Ranking

Dense-sparse hybrid retrieval (uniCOIL zero-shot + TCT_ColBERT_v2 zero-shot):

```bash
python -m pyserini.hsearch   dense  --index /store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-v2-doc-segmented \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-v2-doc-segmented \
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
                             sparse --index /store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-v2-doc-segmented \
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

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-08-13 (commit [`2b96b9`](https://github.com/castorini/pyserini/commit/2b96b99773302315e4d7dbe4a373b36b3eadeaa6))

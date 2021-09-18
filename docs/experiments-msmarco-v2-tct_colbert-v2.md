# Pyserini: TCT-ColBERTv2 for MS MARCO (V2) Collections

This guide provides instructions to reproduce experiments using TCT-ColBERTv2 dense retrieval models on the MS MARCO (V2) collections.
The model is described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://aclanthology.org/2021.repl4nlp-1.17/) _Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)_, pages 163-173, August 2021.

At present, all indexes are referenced as absolute paths on our Waterloo machine `orca`, so these results are not broadly reproducible.
We are working on figuring out ways to distribute the indexes.

For the TREC 2021 Deep Learning Track, we tried two different approaches:

1. We applied our TCT-ColBERTv2 model trained on MS MARCO (V1) in a zero-shot manner.
2. We started with the above TCT-ColBERTv2 model and further fine-tuned on the MS MARCO (V2) passage data.

In both cases, we applied inference over the MS MARCO V2 [passage corpus](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#passage-collection) and [segmented document corpus](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#document-collection-segmented) to obtain the dense vectors.

These are the indexes and the encoder for the zero-shot (V1) models:

```bash
export PASSAGE_INDEX0="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-passage-v2-augmented"
export DOC_INDEX0="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-doc-v2-segmented"
export ENCODER0="castorini/tct_colbert-v2-hnp-msmarco"
```

These are the indexes and the encoder for the fine-tuned (V2) models:

```bash
export PASSAGE_INDEX1="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.psg_v2_ft.msmarco-passage-v2-augmented"
export DOC_INDEX1="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.psg_v2_ft.msmarco-doc-v2-segmented"
export ENCODER1="castorini/tct_colbert-v2-hnp-msmarco-r2"
```

## Passage V2 (Zero Shot)

Dense retrieval with TCT-ColBERTv2 model trained on MS MARCO (V1), with FAISS brute-force index (i.e., zero shot):

```bash
$ python -m pyserini.dsearch --topics collections/passv2_dev_queries.tsv \
                             --index ${PASSAGE_INDEX0} \
                             --encoder ${ENCODER0} \
                             --batch-size 144 \
                             --threads 36 \
                             --output runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.0shot.dev1.trec \
                             --output-format trec
```

To evaluate using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.0shot.dev1.trec
Results:
map                   	all	0.1461
recip_rank            	all	0.1473

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.0shot.dev1.trec
Results:
recall_100            	all	0.5873
recall_1000           	all	0.8321
```

We evaluate MAP and MRR at a cutoff of 100 hits to match the official evaluation metrics.
However, we measure recall at both 100 and 1000 hits; the latter is a common setting for reranking.

Because there are duplicate passages in MS MARCO V2 collections, score differences might be observed due to tie-breaking effects.
For example, if we output in MS MARCO format `--output-format msmarco` and then convert to TREC format with `pyserini.eval.convert_msmarco_run_to_trec_run`, the scores will be different.

## Passage V2 (Fine Tuned)

Dense retrieval with TCT-ColBERTv2 model fine-tuned on MS MARCO (V2) passage data, with FAISS brute-force index:

```bash
$ python -m pyserini.dsearch --topics collections/passv2_dev_queries.tsv \
                             --index ${PASSAGE_INDEX1} \
                             --encoder ${ENCODER1} \
                             --batch-size 144 \
                             --threads 36 \
                             --output runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec \
                             --output-format trec
```

To evaluate using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec
Results:
map                   	all	0.1981
recip_rank            	all	0.2000

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec
Results:
recall_100            	all	0.6403
recall_1000           	all	0.8452
```

## Document V2 (Zero Shot)

Dense retrieval with TCT-ColBERT-V2, brute-force index:

```bash
$ python -m pyserini.dsearch --topics collections/docv2_dev_queries.tsv \
                             --index ${DOC_INDEX0} \
                             --encoder ${ENCODER0} \
                             --batch-size 144 \
                             --threads 36 \
                             --hits 10000 \
                             --max-passage-hits 1000 \
                             --max-passage \
                             --output runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.0shot.dev1.trec \
                             --output-format trec
```

To evaluate using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.0shot.dev1.trec
Results:
map                   	all	0.2440
recip_rank            	all	0.2464

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.0shot.dev1.trec
Results:
recall_100            	all	0.7873
recall_1000           	all	0.9161
```

We evaluate MAP and MRR at a cutoff of 100 hits to match the official evaluation metrics.
However, we measure recall at both 100 and 1000 hits; the latter is a common setting for reranking.

Same comment about duplicate passages and score ties applies here as well.

## Document V2 (Fine Tuned)

Dense retrieval with TCT-ColBERTv2 model fine-tuned on MS MARCO (V2) passage data, with FAISS brute-force index:

```bash
$ python -m pyserini.dsearch --topics collections/docv2_dev_queries.tsv \
                             --index ${DOC_INDEX1} \
                             --encoder ${ENCODER1} \
                             --batch-size 144 \
                             --threads 36 \
                             --hits 10000 \
                             --max-passage-hits 1000 \
                             --max-passage \
                             --output runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec \
                             --output-format trec
```

To evaluate using `trec_eval`:

```bash
$ python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec
Results:
map                   	all	0.2719
recip_rank            	all	0.2745

$ python -m pyserini.eval.trec_eval -c -m recall.100,1000 collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.psg_v2_ft.dev1.trec
Results:
recall_100            	all	0.7778
recall_1000           	all	0.8974
```

## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@crystina-z](https://github.com/crystina-z) on 2021-08-20 (commit [`45a2fb`](https://github.com/castorini/pyserini/commit/45a2fb4bacbbd92f54ff0f98463662cbc09d78bb))

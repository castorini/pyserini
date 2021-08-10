# Pyserini: Baseline for MS MARCO V2: TCT-ColBERT-V2

This guide provides instructions to reproduce the family of TCT-ColBERT-V2 dense retrieval models described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://cs.uwaterloo.ca/~jimmylin/publications/Lin_etal_2021_RepL4NLP.pdf) _RepL4NLP 2021_.


## Data Prep
<!-- # Anserini: Guide to Working with the MS MARCO V2 Collections -->

<!-- This guide presents information for working with V2 of the MS MARCO passage and document test collections. -->

If you're having issues downloading the collection via `wget`, try using [AzCopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10).


1. We use [augmented passage collection](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#passage-collection-augmented) and [segmented document collection](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#document-collection-segmented)
2. Currently, the prebuilt index is on our Waterloo machine `orca`.
3. We only encode `title`, `headings`, and `passage` (or `segment`) for passage (or document) collections.

Let's prepare our environment variables:

```bash
export PSG_INDEX="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-passage-v2-augmented"
export DOC_INDEX="/store/scratch/indexes/trec2021/faiss-flat.tct_colbert-v2-hnp.0shot.msmarco-doc-v2-segmented"
export ENCODER="castorini/tct_colbert-v2-hnp-msmarco"
```

## MS MARCO Passage V2

Dense retrieval with TCT-ColBERT-V2, brute-force index:

```bash
$ python -m pyserini.dsearch --topics collections/passv2_dev_queries.tsv \
                             --index ${PSG_INDEX} \
                             --encoder ${ENCODER} \
                             --batch-size 144 \
                             --threads 36 \
                             --output runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.0shot.top1k.dev1.trec \
                             --output-format trec
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics.
> Note: There are duplicated passages in msmarco v2, the following results will be different from using `--output-format msmarco` with `pyserini.eval.convert_msmarco_run_to_trec_run` because of tie breaking.

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m -m recip_rank collections/passv2_dev_qrels.uniq.tsv runs/run.msmarco-passage-v2-augmented.tct_colbert-v2-hnp.0shot.top1k.dev1.trec
Results:
map                     all     0.1472
recip_rank              all     0.1483
recall_10               all     0.2743
recall_100              all     0.5873
recall_1000             all     0.8321
```

## MS MARCO Document V2

Dense retrieval with TCT-ColBERT-V2, brute-force index:


```bash

$ python -m pyserini.dsearch --topics collections/docv2_dev_queries.tsv \
                             --index ${DOC_INDEX} \
                             --encoder ${ENCODER} \
                             --batch-size 144 \
                             --threads 36 \
                             --hits 1000 \
                             --max-passage-hits 100 \
                             --max-passage \
                             --output runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.0shot.maxp.top100.dev1.trec \
                             --output-format trec
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics. 

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100 -mmap -m -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.tct_colbert-v2-hnp.0shot.maxp.top100.dev1.trec
Results:
map                     all     0.2440
recip_rank              all     0.2464
recall_10               all     0.4784
recall_100              all     0.7873
```


## Reproduction Log[*](reproducibility.md)


# Pyserini: Baseline for MS MARCO V2: uniCOIL (zero-shot)

This page describes how to reproduce the uniCOIL experiments in the following paper:

> Jimmy Lin and Xueguang Ma. [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for Information Retrieval Techniques.](https://arxiv.org/abs/2106.14807) _arXiv:2106.14807_.

## Data Prep
<!-- # Anserini: Guide to Working with the MS MARCO V2 Collections -->

<!-- This guide presents information for working with V2 of the MS MARCO passage and document test collections. -->

If you're having issues downloading the collection via `wget`, try using [AzCopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10).


1. We use [passage collection](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#passage-collection) and [segmented document collection](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md#document-collection-segmented)
2. Currently, the prebuilt index is on our Waterloo machine `orca`.
3. We only encode `passage` (or `segment`) for passage (or document) collections.

Let's prepare our environment variables:

```bash
export PSG_INDEX="/store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-passage-v2"
export DOC_INDEX="/store/scratch/indexes/trec2021/lucene.unicoil-noexp.0shot.msmarco-doc-v2-segmented"
export ENCODER="castorini/unicoil-noexp-msmarco-passage"
```

## MS MARCO Passage V2

Sparse retrieval with uniCOIL:

```bash
python -m pyserini.search --topics collections/passv2_dev_queries.tsv \
                          --encoder ${ENCODER} \
                          --index ${PSG_INDEX}  \
                          --output runs/run.msmarco-passage-v2.unicoil-noexp.0shot.top1k.dev1.trec \
                          --impact \
                          --hits 1000 \
                          --batch 144 \
                          --threads 36 \
                          --min-idf 1
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics.
> Note: There are duplicated passages in msmarco v2, the following results will be different from using `--output-format msmarco` with `pyserini.eval.convert_msmarco_run_to_trec_run` because of tie breaking.

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m recip_rank collections/passv2_dev_qrels.tsv runs/run.msmarco-passage-v2.unicoil-noexp.0shot.top1k.dev1.trec
Results:
map                   	all	0.1314
recip_rank            	all	0.1322
recall_10             	all	0.2585
recall_100            	all	0.4964
recall_1000           	all	0.7013
```

## MS MARCO Document V2

Sparse retrieval with uniCOIL:
```bash
python -m pyserini.search --topics collections/docv2_dev_queries.tsv \
                          --encoder ${ENCODER} \
                          --index ${DOC_INDEX}  \
                          --output runs/run.msmarco-document-v2-segmented.unicoil-noexp.0shot.maxp.top100.dev1.trec \
                          --impact \
                          --hits 1000 \
                          --batch 144 \
                          --threads 36 \
                          --max-passage-hits 100 \
                          --max-passage \
                          --min-idf 1
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics. 

```bash
$ python -m pyserini.eval.trec_eval -c -m recall.10,100 -mmap -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-document-v2-segmented.unicoil-noexp.0shot.maxp.top100.dev1.trec
Results:
map                   	all	0.2012
recip_rank            	all	0.2032
recall_10             	all	0.3981
recall_100            	all	0.7200
```


## Reproduction Log[*](reproducibility.md)
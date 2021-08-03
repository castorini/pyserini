# Pyserini: Baseline for MS MARCO V2: TCT-ColBERT-V2

This guide provides instructions to reproduce the family of TCT-ColBERT-V2 dense retrieval models described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://cs.uwaterloo.ca/~jimmylin/publications/Lin_etal_2021_RepL4NLP.pdf) _RepL4NLP 2021_.


## Data Prep
<!-- # Anserini: Guide to Working with the MS MARCO V2 Collections -->

<!-- This guide presents information for working with V2 of the MS MARCO passage and document test collections. -->

If you're having issues downloading the collection via `wget`, try using [AzCopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10).


### Note1: we encode **title**, **headings**, **passage** here
### Note2: Currently, the prebuilt index is on our Waterloo machine `orca`

## MS MARCO Passage V2

Dense retrieval with TCT-ColBERT-V2, brute-force index:

```bash
export INDEX=/store/scratch/j587yang/project/trec_2021/indexes/dl2021/passage/title_headings_body/tct_colbert-v2-hnp-msmarco-full

$ python -m pyserini.dsearch --topics collections/passv2_dev_queries.tsv \
                             --index ${INDEX} \
                             --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             --batch-size 144 \
                             --threads 36 \
                             --output runs/run.msmarco-pass-v2.tct_colbert-v2-hnp.bf.tsv \
                             --output-format msmarco
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-pass-v2.tct_colbert-v2-hnp.bf.tsv --output runs/run.msmarco-pass-v2.tct_colbert-v2-hnp.bf.trec
$ python -m pyserini.eval.trec_eval -c -m recall.10,100,1000 -mmap -m -m recip_rank collections/passv2_dev_qrels.uniq.tsv runs/run.msmarco-pass-v2.tct_colbert-v2-hnp.bf.trec
map                     all     0.1502
recip_rank              all     0.1515
recall_10               all     0.2750
recall_100              all     0.5878
recall_1000             all     0.8321
```

## MS MARCO Document V2

Dense retrieval with TCT-ColBERT-V2, brute-force index:


```bash
export INDEX=/store/scratch/j587yang/project/trec_2021/indexes/dl2021/document/title_headings_body/tct_colbert-v2-hnp-msmarco-full-maxp

$ python -m pyserini.dsearch --topics collections/docv2_dev_queries.tsv \
                             --index ${INDEX} \
                             --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             --batch-size 144 \
                             --threads 36 \
                             --hits 1000 \
                             --max-passage-hits 100 \
                             --output runs/run.msmarco-doc-v2.tct_colbert-v2-hnp.maxp.bf.tsv \
                             --output-format msmarco
```

To evaluate:

We use the official TREC evaluation tool `trec_eval` to compute metrics. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc-v2.tct_colbert-v2-hnp.maxp.bf.tsv --output runs/run.msmarco-doc-v2.tct_colbert-v2-hnp.maxp.bf.trec
$ python -m pyserini.eval.trec_eval -c -m recall.10,100 -mmap -m -m recip_rank collections/docv2_dev_qrels.tsv runs/run.msmarco-doc-v2.tct_colbert-v2-hnp.maxp.bf.trec
map                     all     0.2485
recip_rank              all     0.2510
recall_10               all     0.4800
recall_100              all     0.7873
```


## Reproduction Log[*](reproducibility.md)


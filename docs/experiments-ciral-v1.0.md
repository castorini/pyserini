# Pyserini Regressions: BM25 Baselines for CIRAL Version 1.0

This page documents BM25 regression experiments for CIRAL (v1.0)

## Corpus Download

### 1. Manual Download

The CIRAL Corpus can be downloaded from the [Hugging Face Repo](https://huggingface.co/datasets/CIRAL/ciral-corpus)

We can now index the documents for each language as a `MrTyDiCollection`  using Anserini bindings from Pyserini

```bash
python -m pyserini.index.lucene --collection MrTyDiCollection \
    --input path/to/hausa_passages.jsonl --index lucene-index.ciral-v1.0-ha \
    --generator DefaultLuceneDocumentGenerator \
    --language ha --pretokenized \
    --threads 16 --storePositions --storeDocvectors --storeRaw \
    >& logs/log.ciral-v1.0-ha &

python -m pyserini.index.lucene --collection MrTyDiCollection \
    --input path/to/somali_passages.jsonl --index lucene-index.ciral-v1.0-so \
    --generator DefaultLuceneDocumentGenerator \
    --language so --pretokenized \
    --threads 16 --storePositions --storeDocvectors --storeRaw \
    >& logs/log.ciral-v1.0-so &

python -m pyserini.index.lucene --collection MrTyDiCollection \
    --input path/to/swahili_passages.jsonl --index lucene-index.ciral-v1.0-sw \
    --generator DefaultLuceneDocumentGenerator \
    --language sw --pretokenized \
    --threads 16 --storePositions --storeDocvectors --storeRaw \
    >& logs/log.ciral-v1.0-sw &

python -m pyserini.index.lucene --collection MrTyDiCollection \
    --input path/to/yoruba_passages.jsonl --index lucene-index.ciral-v1.0-yo \
    --generator DefaultLuceneDocumentGenerator \
    --language yo --pretokenized \
    --threads 16 --storePositions --storeDocvectors --storeRaw \
    >& logs/log.ciral-v1.0-yo &
```


### 2.  Download Pre-Built Sparse Indexes (for BM25)

[Hausa](https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-ha.20230721.e850ea.tar.gz)
[Somali](https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-so.20230721.e850ea.tar.gz)
[Swahili](https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-sw.20230721.e850ea.tar.gz)
[Yoruba](https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-yo.20230721.e850ea.tar.gz)


### Data Prep

We would need the topic and qrel files from the [Hugging Face repo](https://huggingface.co/datasets/CIRAL/ciral) to reproduce the baselines.  # TO-DO: To remove this section once queries and qrels are added to Anserini tools.

Clone the repo and copy the files to `tools/topics-and-qrels` in the cloned `Pyserini` repo. This requires the Pyserini [dev install](https://github.com/castorini/pyserini/blob/master/docs/installation.md#development-installation)

```bash
git clone https://huggingface.co/datasets/CIRAL/ciral
cp -r ciral/*/*/* $PYSERINI_PATH/tools/topics-and-qrels/
```



## Retrieval: Dev Topics

```bash
python -m pyserini.search.lucene --index ciral-v1.0-ha \
    --topics tools/topics-and-qrels/topics.ciral-v1.0-ha-train \
    --output runs/run.ciral-v1.0-ha.bm25.topics.ciral-v1.0-ha.train.txt \
    --pretokenized --language ha \
    --batch 128 --threads 16 --bm25 --hits 1000

python -m pyserini.search.lucene --index ciral-v1.0-so \
    --topics tools/topics-and-qrels/topics.ciral-v1.0-so-train \
    --output runs/run.ciral-v1.0-so.bm25.topics.ciral-v1.0-so.train.txt \
    --pretokenized --language so \
    --batch 128 --threads 16 --bm25 --hits 1000

python -m pyserini.search.lucene --index ciral-v1.0-sw \
    --topics tools/topics-and-qrels/topics.ciral-v1.0-sw-train \
    --output runs/run.ciral-v1.0-sw.bm25.topics.ciral-v1.0-sw.train.txt \
    --pretokenized --language sw \
    --batch 128 --threads 16 --bm25 --hits 1000

python -m pyserini.search.lucene --index ciral-v1.0-yo \
    --topics tools/topics-and-qrels/topics.ciral-v1.0-yo-train \
    --output runs/run.ciral-v1.0-yo.bm25.topics.ciral-v1.0-yo.train.txt \
    --pretokenized --language yo \
    --batch 128 --threads 16 --bm25 --hits 1000

```

## Evaluation: Dev Topics
python -m pyserini.eval.trec_eval -c -m recall.1000 tools/topics-and-qrels/qrels.ciral-v1.0-ha-train.tsv runs/run.ciral-v1.0-ha.bm25.topics.ciral-v1.0-ha.train.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 tools/topics-and-qrels/qrels.ciral-v1.0-so-train.tsv runs/run.ciral-v1.0-so.bm25.topics.ciral-v1.0-so.train.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 tools/topics-and-qrels/qrels.ciral-v1.0-sw-train.tsv runs/run.ciral-v1.0-sw.bm25.topics.ciral-v1.0-sw.train.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 tools/topics-and-qrels/qrels.ciral-v1.0-yo-train.tsv runs/run.ciral-v1.0-yo.bm25.topics.ciral-v1.0-yo.train.txt


## Effectiveness

### Yoruba

With the above commands, you should be able to reproduce the following results:
| **recall@1000**                                                                   | **BM2 (default)**| 
|:----------------------------------------------------------------------------------|-----------|
| [CIRAL (Yoruba): dev](https://github.com/ciralproject/ciral)                      | 0.6010    |



### Swahili

With the above commands, you should be able to reproduce the following results:
| **recall@1000**                                                                   | **BM2 (default)**| 
|:----------------------------------------------------------------------------------|-----------|
| [CIRAL (Swahili): dev](https://github.com/ciralproject/ciral)                     | 0.1333    |



### Somali

With the above commands, you should be able to reproduce the following results:
| **recall@1000**                                                                   | **BM2 (default)**| 
|:----------------------------------------------------------------------------------|-----------|
| [CIRAL (Somali): dev](https://github.com/ciralproject/ciral)                      | 0.1267    |



### Hausa

With the above commands, you should be able to reproduce the following results:
| **recall@1000**                                                                   | **BM2 (default)**| 
|:----------------------------------------------------------------------------------|-----------|
| [CIRAL (Hausa): dev](https://github.com/ciralproject/ciral)                       | 0.1050    |


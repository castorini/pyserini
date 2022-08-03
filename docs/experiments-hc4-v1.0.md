# Pyserini Regressions: BM25 Baseline for HC4 (v1.0)

This guide contains instructions for running BM25 baselines on [HC4 (v1.0)](https://arxiv.org/pdf/2201.09992.pdf).


## Corpus Download

### 1. Manual Download

The HC4 corpus can be downloaded following the instructions [here](https://github.com/hltcoe/HC4).
After download, verify that all and only specified documents have been downloaded by running the code 
[provided here](https://github.com/hltcoe/HC4#postprocessing-of-the-downloaded-documents).

With the corpus downloaded, we need to create 3 separate folders for the 3 languages (Persian, Chinese and  Russian) ,
and unpack the data into the respective folders for each language


```bash
mkdir collections/hc4-v1.0-fa collections/hc4-v1.0-zh collections/hc4-v1.0-ru
```

We can now index these docs as a `NeuClirCollection`  using Anserini bindings from Pyserini

```bash

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/hc4-v1.0-zh --index indexes/lucene-index.hc4-v1.0-zh \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language zh \
  >& logs/log.hc4-v1.0-zh &

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/hc4-v1.0-fa --index indexes/lucene-index.hc4-v1.0-fa \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language fa \
  >& logs/log.hc4-v1.0-fa &

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/hc4-v1.0-ru --index indexes/lucene-index.hc4-v1.0-ru \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language ru \
  >& logs/log.hc4-v1.0-ru &
```


### 2.  Download Pre-built sparse indexes (for BM25)

- [Chinese](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-zh.20220719.71c120.tar.gz)
- [Persian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-fa.20220719.71c120.tar.gz)
- [Russian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-ru.20220719.71c120.tar.gz)

## Retrieval Runs

### TEST SET

#### - Topic Title

```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --language ru

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --rocchio --language ru 
```

#### - Topic Description 


```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --language ru 

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --rocchio --language ru 
```

## Evaluate

#### -  Topic Title

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000  hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000  hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000  hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.title.txt
```

### Topic Description

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.txt
```

### DEV SET

#### - Topic Title

```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-title \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-title \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-title \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt \
    --bm25 --language ru 

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-title \
    --output runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.dev.title.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-title \
    --output runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.dev.title.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-title \
    --output runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.dev.title.txt \
    --bm25 --rm3 --language ru 

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-title \
    --output runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.dev.title.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-title \
    --output runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.dev.title.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-title \
    --output runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.dev.title.txt \
    --bm25 --rocchio --language ru 
```

#### - Topic Description 


```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-description \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.description.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-description \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.description.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-description \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.description.txt \
    --bm25 --language ru

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-description \
    --output runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.dev.description.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-description \
    --output runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.dev.description.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-description \
    --output runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.dev.description.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-description \
    --output runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.dev.description.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-description \
    --output runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.dev.description.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-description \
    --output runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.dev.description.txt \
    --bm25 --rocchio --language ru 
```


## Evaluate

#### -  Topic Title

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.dev.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.dev.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.dev.title.txt
```

### Topic Description

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25-default+rm3.topics.hc4-v1.0-zh.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25-default+rm3.topics.hc4-v1.0-fa.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25-default+rm3.topics.hc4-v1.0-ru.dev.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.dev.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.dev.description.txt
```

## Effectiveness

### - Chinese

With the above commands, you should be able to reproduce the following results:

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2969    | 0.3126    | 0.2641    |
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.2030    | 0.2239    | 0.2211    |
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.1801    | 0.1613    | 0.1671    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.1455    | 0.1051    | 0.1442    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.3908    | 0.4296    | 0.3474    |
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3023    | 0.3327    | 0.2963    |
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.2526    | 0.2132    | 0.2236    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.2048    | 0.1597    | 0.1916    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.4250    | 0.4200    | 0.4250    |
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3800    | 0.3250    | 0.3550    |
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.3000    | 0.2760    | 0.3070    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.2470    | 0.1960    | 0.2740    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.7964    | 0.7589    | 0.8365    |
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.7255    | 0.6730    | 0.7570    |
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.6963    | 0.6764    | 0.6652    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.6358    | 0.4933    | 0.6481    |

### - Russian

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2937    | 0.2390    | 0.3995    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.2374    | 0.0844    | 0.2817    |
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.2186    | 0.2369    | 0.2592    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.1880    | 0.1874    | 0.2252    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.3942    | 0.3376    | 0.4719    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.2580    | 0.1838    | 0.3168    |
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.2954    | 0.3200    | 0.3108    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.2446    | 0.2402    | 0.2759    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.4375    | 0.4500    | 0.5125    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.5125    | 0.3625    | 0.5500    |
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.3480    | 0.3620    | 0.3950    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.3180    | 0.2960    | 0.3510    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.8432    | 0.7598    | 0.8710    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.5942    | 0.3886    | 0.6171    |
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.7182    | 0.7223    | 0.7713    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.7355    | 0.6475    | 0.7669    |


### - Persian

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2971    | 0.2866    | 0.3030    |
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3243    | 0.3403    | 0.3721    |
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.2877    | 0.2962    | 0.2954    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.2928    | 0.2805    | 0.2928    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.3445    | 0.3450    | 0.3161    |
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3475    | 0.3862    | 0.3895    |
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.3846    | 0.3818    | 0.3861    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.4039    | 0.3732    | 0.3811    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.4100    | 0.3250    | 0.3950    |
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.4750    | 0.3500    | 0.5100    |
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.4010    | 0.3800    | 0.4350    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.3890    | 0.3590    | 0.4300    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.7794    | 0.7683    | 0.8039    |
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.8491    | 0.7737    | 0.8838    |
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.8223    | 0.7755    | 0.8560    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.8402    | 0.7487    | 0.8738    |
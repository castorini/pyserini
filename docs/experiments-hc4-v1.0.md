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

We can now index these docs as a `NeuClirCollection` using Anserini

```bash

python -m pyserini.index.lucene \
  --collection NeuClirCollection \
  --input collections/hc4-v1.0-zh \
  --index indexes/lucene-index.hc4-v1.0-zh/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language zh \
  >& logs/log.hc4-v1.0-zh &

python -m pyserini.index.lucene \
  --collection NeuClirCollection \
  --input collections/hc4-v1.0-fa \
  --index indexes/lucene-index.hc4-v1.0-fa/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language fa \
  >& logs/log.hc4-v1.0-fa &

  
python -m pyserini.index.lucene \
  --collection NeuClirCollection \
  --input collections/hc4-v1.0-ru \
  --index indexes/lucene-index.hc4-v1.0-ru/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language ru \
  >& logs/log.hc4-v1.0-ru &
```


### 2.  Download Pre-built sparse indexes (for BM25)

- [Chinese](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-chinese.20220714.cd2601.tar.gz)
- [Persian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-persian.20220714.cd2601.tar.gz)
- [Russian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.hc4-v1.0-russian.20220714.cd2601.tar.gz)

## Retrieval Runs

### TEST SET

#### - Topic Title

```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.title.txt \
    --hits 100 --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.title.txt \
    --hits 100 --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.title.txt \
    --hits 100 --bm25 --language ru 
```

#### - Topic Description 


```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.description.txt \
    --hits 100 --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.description.txt \
    --hits 100 --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.description.txt \
    --hits 100 --bm25 --language ru 
```

## Evaluate

#### -  Topic Title

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.title.txt
```

### Topic Description

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-zh-test runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-fa-test runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-ru-test runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.test.description.txt
```

### DEV SET

#### - Topic Title

```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-title \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt \
    --hits 100 --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-title \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt \
    --hits 100 --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-title \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt \
    --hits 100 --bm25 --language ru 
```

#### - Topic Description 


```bash
python -m pyserini.search.lucene  --index  hc4-v1.0-zh \
    --topics hc4-v1.0-zh-dev-description \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.description.txt \
    --hits 100 --bm25 --language zh

python -m pyserini.search.lucene  --index  hc4-v1.0-fa \
    --topics hc4-v1.0-fa-dev-description \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.description.txt \
    --hits 100 --bm25 --language fa 

python -m pyserini.search.lucene  --index  hc4-v1.0-ru \
    --topics hc4-v1.0-ru-dev-description \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.description.txt \
    --hits 100 --bm25 --language ru 
```


## Evaluate

#### -  Topic Title

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt
```

### Topic Description

```bash
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-zh-dev runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.description.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-fa-dev runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.description.txt
python -m pyserini.eval.trec_eval -c -M 100 -m map hc4-v1.0-ru-dev runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.description.txt
```

## Results

### TEST SET

With the above commands, you should be able to reproduce the following results:

| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                              | 0.1749   |
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                              | 0.2837   |
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                              | 0.2105   |


| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                        | 0.1404   |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                        | 0.2882   |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                        | 0.1779   |

### DEV SET

With the above commands, you should be able to reproduce the following results:

| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2914    |
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2919    |
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2767    |


| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.1983    |
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3188    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.2321    |
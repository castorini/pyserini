# Pyserini Regressions: BM25 Baseline for HC4 (v1.0) on NeuCLIR22 &mdash;

This page documents BM25 regression experiments for [HC4 (v1.0) Persian topics](https://github.com/hltcoe/HC4) on the [NeuCLIR22 Persian corpus](https://neuclir.github.io/).
The HC4 qrels have been filtered down to include only those in the intersection of the HC4 and NeuCLIR22 corpora.


## Corpus Download

### 1. Manual Download

The HC4 corpus can be downloaded following the instructions [here](https://github.com/NeuCLIR/download-collection.git).
After download, verify that all and only specified documents have been downloaded by running the code 
[provided here](https://github.com/NeuCLIR/download-collection#postprocessing-of-the-downloaded-documents).

With the corpus downloaded, we need to create 3 separate folders for the 3 languages (Persian, Chinese and  Russian) ,
and unpack the data into the respective folders for each language


```bash
mkdir collections/neuclir22-fa collections/neuclir22-zh collections/neuclir22-ru
```

We can now index these docs as a `NeuClirCollection` using Anserini bindings from Pyserini

```bash

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/neuclir22-zh --index indexes/lucene-index.neuclir22-zh \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language zh \
  >& logs/log.neuclir22-zh &

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/neuclir22-fa --index indexes/lucene-index.neuclir22-fa \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language fa \
  >& logs/log.neuclir22-fa &

python -m pyserini.index.lucene --collection NeuClirCollection \
  --input collections/neuclir22-ru --index indexes/lucene-index.neuclir22-ru \
  --generator DefaultLuceneDocumentGenerator --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language ru \
  >& logs/log.neuclir22-ru &
```


### 2.  Download Pre-built sparse indexes (for BM25)

- [Chinese](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.neuclir22-zh.20220719.71c120.tar.gz)
- [Persian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.neuclir22-fa.20220719.71c120.tar.gz)
- [Russian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.neuclir22-ru.20220719.71c120.tar.gz)

## Retrieval Runs

### TEST SET

#### - Topic Title

```bash
python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --language ru

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index neuclir22-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-title \
    --output runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.title.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics hc4-v1.0-fa-test-title \
    --output runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.title.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-title \
    --output runs/run.neuclir22-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.title.txt \
    --bm25 --rocchio --language ru 
```

#### - Topic Description 


```bash
python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --language ru 

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics hc4-v1.0-zh-test-description \
    --output runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics hc4-v1.0-fa-test-description \
    --output runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics hc4-v1.0-ru-test-description \
    --output runs/run.neuclir22-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.txt \
    --bm25 --rocchio --language ru 
```

#### - Topic Description+Title 



```bash
python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-zh.test.desc.title.tsv \
    --output runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.description.title.txt \
    --bm25 --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-fa.test.desc.title.tsv \
    --output runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.description.title.txt \
    --bm25 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-ru.test.desc.title.tsv \
    --output runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.description.title.txt \
    --bm25 --language ru 

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-zh.test.desc.title.tsv \
    --output runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.title.txt \
    --bm25 --rm3 --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-fa.test.desc.title.tsv \
    --output runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.title.txt \
    --bm25 --rm3 --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-ru.test.desc.title.tsv \
    --output runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.title.txt \
    --bm25 --rm3 --language ru

python -m pyserini.search.lucene  --index  neuclir22-zh \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-zh.test.desc.title.tsv \
    --output runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.title.txt \
    --bm25 --rocchio --language zh

python -m pyserini.search.lucene  --index  neuclir22-fa \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-fa.test.desc.title.tsv \
    --output runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.title.txt \
    --bm25 --rocchio --language fa 

python -m pyserini.search.lucene  --index  neuclir22-ru \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-ru.test.desc.title.tsv \
    --output runs/run.neuclir22-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.title.txt \
    --bm25 --rocchio --language ru 
```

## Evaluate


#### -  Topic Title

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.title.txt
```

### Topic Description

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.txt
```

### Topic Description+Title

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25.topics.hc4-v1.0-zh.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25.topics.hc4-v1.0-fa.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25.topics.hc4-v1.0-ru.test.description.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rm3.topics.hc4-v1.0-zh.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rm3.topics.hc4-v1.0-fa.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25-default+rm3.topics.hc4-v1.0-ru.test.description.title.txt

python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-zh.test.txt runs/run.neuclir22-zh.bm25-default+rocchio.topics.hc4-v1.0-zh.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-fa.test.txt runs/run.neuclir22-fa.bm25-default+rocchio.topics.hc4-v1.0-fa.test.description.title.txt
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.20 -m judged.20 -m recall.1000 tools/topics-and-qrels/qrels.hc4-neuclir22-ru.test.txt runs/run.neuclir22-ru.bm25-default+rocchio.topics.hc4-v1.0-ru.test.description.title.txt
```

## Effectiveness

### - Chinese

With the above commands, you should be able to reproduce the following results:

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.0561    | 0.0449    | 0.0488    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.0428    | 0.0262    | 0.0277    |
| [HC4 (Chinese): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.0597    | 0.0435    | 0.0462    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.0759    | 0.0622    | 0.0767    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.0687    | 0.0379    | 0.0529    |
| [HC4 (Chinese): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.0881    | 0.0640    | 0.0735    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.0620    | 0.0490    | 0.0760    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.0590    | 0.0360    | 0.0610    |
| [HC4 (Chinese): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.0710    | 0.0420    | 0.0740    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Chinese): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.4401    | 0.3909    | 0.4128    |
| [HC4 (Chinese): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.3565    | 0.2383    | 0.3858    |
| [HC4 (Chinese): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.4442    | 0.2673    | 0.4259    |
### - Russian

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.0964    | 0.0811    | 0.1245    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.0926    | 0.0605    | 0.1064    |
| [HC4 (Russian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.1113    | 0.0771    | 0.1341    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.1380    | 0.1257    | 0.1668    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.1459    | 0.0963    | 0.1643    |
| [HC4 (Russian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.1640    | 0.1318    | 0.1899    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.0860    | 0.0730    | 0.0940    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.0790    | 0.0610    | 0.0890    |
| [HC4 (Russian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.0900    | 0.0750    | 0.0980    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Russian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.6319    | 0.6154    | 0.6887    |
| [HC4 (Russian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.6640    | 0.5408    | 0.6407    |
| [HC4 (Russian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.6667    | 0.6221    | 0.6743    |

### - Persian

| **MAP**                                                                                                      | **BM25 (default)**| **+RM3**  | **+Rocchio**|
|:-------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.1198    | 0.1050    | 0.1221    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.1435    | 0.0845    | 0.1254    |
| [HC4 (Persian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.1438    | 0.1079    | 0.1351    |
| **nDCG@20**                                                                                                  | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.1806    | 0.1549    | 0.1794    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.2288    | 0.1323    | 0.1968    |
| [HC4 (Persian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.2233    | 0.1760    | 0.2001    |
| **J@20**                                                                                                     | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.1430    | 0.1220    | 0.1520    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.1480    | 0.1100    | 0.1480    |
| [HC4 (Persian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.1570    | 0.1210    | 0.1530    |
| **Recall@1000**                                                                                              | **BM25 (default)**| **+RM3**  | **+Rocchio**|
| [HC4 (Persian): test-topic title](https://github.com/hltcoe/HC4)                                             | 0.7234    | 0.6742    | 0.7929    |
| [HC4 (Persian): test-topic description](https://github.com/hltcoe/HC4)                                       | 0.7431    | 0.6107    | 0.7768    |
| [HC4 (Persian): test-topic description+title](https://github.com/hltcoe/HC4)                                 | 0.7652    | 0.6436    | 0.8058    |
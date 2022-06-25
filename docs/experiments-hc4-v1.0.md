# Pyserini Regressions: BM25 Baseline for HC4 (v1.0)

This guide contains instructions for running BM25 baselines on [HC4 (v1.0)](https://arxiv.org/pdf/2201.09992.pdf).


## Corpus Download

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
  --input collections/hc4-v1.0-fa \
  --index indexes/lucene-index.hc4-v1.0-persian/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language fa \
  >& logs/log.hc4-v1.0-fa &

python -m pyserini.index.lucene \
  --collection NeuClirCollection \
  --input collections/hc4-v1.0-zh \
  --index indexes/lucene-index.hc4-v1.0-chinese/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language zh \
  >& logs/log.hc4-v1.0-zh &
  
python -m pyserini.index.lucene \
  --collection NeuClirCollection \
  --input collections/hc4-v1.0-ru \
  --index indexes/lucene-index.hc4-v1.0-russian/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 \
  --storePositions --storeDocvectors --storeRaw -language ru \
  >& logs/log.hc4-v1.0-ru &
```

## Performing Retrieval on the Dev Queries

We will run retrieval for Topic title and descriptions for each language provided by HC4

### Topic Title

```bash

python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-persian/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-fa.dev.title.tsv.gz \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt \
    --hits 100 \
    --bm25 \
    --language fa

python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-chinese/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-zh.dev.title.tsv.gz \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt \
    --hits 100 \
    --bm25 \
    --language zh


python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-russian/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-ru.dev.title.tsv.gz \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt \
    --hits 100 \
    --bm25 \
    --language ru
```

### Topic Description

```bash

python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-persian/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-fa.dev.desc.tsv.gz \
    --output runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.desc.txt \
    --hits 100 \
    --bm25 \
    --language fa

python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-chinese/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-zh.dev.desc.tsv.gz \
    --output runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.desc.txt \
    --hits 100 \
    --bm25 \
    --language zh


python -m pyserini.search.lucene \
    --index indexes/lucene-index.hc4-v1.0-russian/ \
    --topics tools/topics-and-qrels/topics.hc4-v1.0-ru.dev.desc.tsv.gz \
    --output runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.desc.txt \
    --hits 100 \
    --bm25 \
    --language ru
```

## Evaluate

### Topic Title

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-fa.dev.txt runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.title.txt
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-zh.dev.txt runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.title.txt 
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-ru.dev.txt runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.title.txt 
```

### Topic Description

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-fa.dev.txt runs/run.hc4-v1.0-fa.bm25.topics.hc4-v1.0-fa.dev.desc.txt
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-zh.dev.txt runs/run.hc4-v1.0-zh.bm25.topics.hc4-v1.0-zh.dev.desc.txt 
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m map tools/topics-and-qrels/qrels.hc4-v1.0-ru.dev.txt runs/run.hc4-v1.0-ru.bm25.topics.hc4-v1.0-ru.dev.desc.txt 
```

## Results

With the above commands, you should be able to reproduce the following results:

| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Persian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2919    |
| [HC4 (Chinese): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2914    |
| [HC4 (Russian): dev-topic title](https://github.com/hltcoe/HC4)                                              | 0.2767    |

The Above results are reproduction of the BM25 title queries run in [table 7 of this paper](https://arxiv.org/pdf/2201.08471.pdf)

| MAP                                                                                                          | BM25      |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [HC4 (Persian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.3188    |
| [HC4 (Chinese): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.1983    |
| [HC4 (Russian): dev-topic description](https://github.com/hltcoe/HC4)                                        | 0.2321    |



# Pyserini Regressions: BM25 Baselines for MIRACL (v1.0)

This guide contains instructions for running BM25 baselines on [MIRACL (v1.0)](https://github.com/project-miracl/miracl).

## Corpus Download

### 1. Manual Download

The MIRACL corpus can be downloaded from [HuggingFace](https://huggingface.co/datasets/miracl/miracl-corpus).

We can now index the documents for each language as a `MrTyDiCollection`  using Anserini bindings from Pyserini

```bash
lang=ar

python -m pyserini.index.lucene --collection MrTyDiCollection \
  --input /path/to/miracl-v1.0-${lang} \
  --index indexes/lucene-index.miracl-v1.0-${lang} \
  --generator DefaultLuceneDocumentGenerator \
  --threads 8 --storePositions --storeDocvectors \
  --storeRaw -language ${lang} \
  >& logs/log.miracl-v1.0-${lang} &
```


### 2.  Download Pre-Built Sparse Indexes (for BM25)

- [Arabic](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-ar.20221004.2b2856.tar.gz)
- [Bengali](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-bn.20221004.2b2856.tar.gz)
- [English](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-en.20221004.2b2856.tar.gz)
- [Spanish](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-es.20221004.2b2856.tar.gz)
- [Persian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-fa.20221004.2b2856.tar.gz)
- [Finnish](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-fi.20221004.2b2856.tar.gz)
- [French](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-fr.20221004.2b2856.tar.gz)
- [Indonesian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-id.20221004.2b2856.tar.gz)
- [Hindi](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-hi.20221004.2b2856.tar.gz)
- [Japanese](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-ja.20221004.2b2856.tar.gz)
- [Korean](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-ko.20221004.2b2856.tar.gz)
- [Russian](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-ru.20221004.2b2856.tar.gz)
- [Swahili](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-sw.20221004.2b2856.tar.gz)
- [Telugu](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-te.20221004.2b2856.tar.gz)
- [Thai](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-th.20221004.2b2856.tar.gz)
- [Chinese](https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/lucene-index.miracl-v1.0-zh.20221004.2b2856.tar.gz)

## Retrieval: Dev Topics

```bash
python -m pyserini.search.lucene  --index  miracl-v1.0-ar \
    --topics miracl-v1.0-ar-dev \
    --output runs/run.miracl-v1.0-ar.bm25.topics.miracl-v1.0-ar.dev.txt \
    --bm25 --language ar
  
python -m pyserini.search.lucene  --index  miracl-v1.0-bn \
    --topics miracl-v1.0-bn-dev \
    --output runs/run.miracl-v1.0-bn.bm25.topics.miracl-v1.0-bn.dev.txt \
    --bm25 --language bn

python -m pyserini.search.lucene  --index  miracl-v1.0-en \
    --topics miracl-v1.0-en-dev \
[    --output runs/run.miracl-v1.0-en.bm25.topics.miracl-v1.0-en.dev.txt \
]()    --bm25 --language en

python -m pyserini.search.lucene  --index  miracl-v1.0-es \
    --topics miracl-v1.0-es-dev \
    --output runs/run.miracl-v1.0-es.bm25.topics.miracl-v1.0-es.dev.txt \
    --bm25 --language es

python -m pyserini.search.lucene  --index  miracl-v1.0-fa \
    --topics miracl-v1.0-fa-dev \
    --output runs/run.miracl-v1.0-fa.bm25.topics.miracl-v1.0-fa.dev.txt \
    --bm25 --language fa

python -m pyserini.search.lucene  --index  miracl-v1.0-fi \
    --topics miracl-v1.0-fi-dev \
    --output runs/run.miracl-v1.0-fi.bm25.topics.miracl-v1.0-fi.dev.txt \
    --bm25 --language fi

python -m pyserini.search.lucene  --index  miracl-v1.0-hi \
    --topics miracl-v1.0-hi-dev \
    --output runs/run.miracl-v1.0-hi.bm25.topics.miracl-v1.0-hi.dev.txt \
    --bm25 --language hi

python -m pyserini.search.lucene  --index  miracl-v1.0-id \
    --topics miracl-v1.0-id-dev \
    --output runs/run.miracl-v1.0-id.bm25.topics.miracl-v1.0-id.dev.txt \
    --bm25 --language id

python -m pyserini.search.lucene  --index  miracl-v1.0-ja \
    --topics miracl-v1.0-ja-dev \
    --output runs/run.miracl-v1.0-ja.bm25.topics.miracl-v1.0-ja.dev.txt \
    --bm25 --language ja

python -m pyserini.search.lucene  --index  miracl-v1.0-ko \
    --topics miracl-v1.0-ko-dev \
    --output runs/run.miracl-v1.0-ko.bm25.topics.miracl-v1.0-ko.dev.txt \
    --bm25 --language ko

python -m pyserini.search.lucene  --index  miracl-v1.0-ru \
    --topics miracl-v1.0-ru-dev \
    --output runs/run.miracl-v1.0-ru.bm25.topics.miracl-v1.0-ru.dev.txt \
    --bm25 --language ru

python -m pyserini.search.lucene  --index  miracl-v1.0-sw \
    --topics miracl-v1.0-sw-dev \
    --output runs/run.miracl-v1.0-sw.bm25.topics.miracl-v1.0-sw.dev.txt \
    --bm25 --language sw

python -m pyserini.search.lucene  --index  miracl-v1.0-te \
    --topics miracl-v1.0-te-dev \
    --output runs/run.miracl-v1.0-te.bm25.topics.miracl-v1.0-te.dev.txt \
    --bm25 --language te

python -m pyserini.search.lucene  --index  miracl-v1.0-th \
    --topics miracl-v1.0-th-dev \
    --output runs/run.miracl-v1.0-th.bm25.topics.miracl-v1.0-th.dev.txt \
    --bm25 --language th
    
python -m pyserini.search.lucene  --index  miracl-v1.0-zh \
    --topics miracl-v1.0-zh-dev \
    --output runs/run.miracl-v1.0-zh.bm25.topics.miracl-v1.0-zh.dev.txt \
    --bm25 --language zh
```


## Evaluation: Dev Topics

Condition: **Title**

```bash
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-ar-dev runs/run.miracl-v1.0-ar.bm25.topics.miracl-v1.0-ar.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-bn-dev runs/run.miracl-v1.0-bn.bm25.topics.miracl-v1.0-bn.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-en-dev runs/run.miracl-v1.0-en.bm25.topics.miracl-v1.0-en.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-es-dev runs/run.miracl-v1.0-es.bm25.topics.miracl-v1.0-es.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-fa-dev runs/run.miracl-v1.0-fa.bm25.topics.miracl-v1.0-fa.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-fi-dev runs/run.miracl-v1.0-fi.bm25.topics.miracl-v1.0-fi.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-fr-dev runs/run.miracl-v1.0-fr.bm25.topics.miracl-v1.0-fr.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-hi-dev runs/run.miracl-v1.0-hi.bm25.topics.miracl-v1.0-hi.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-id-dev runs/run.miracl-v1.0-id.bm25.topics.miracl-v1.0-id.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-ja-dev runs/run.miracl-v1.0-ja.bm25.topics.miracl-v1.0-ja.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-ko-dev runs/run.miracl-v1.0-ko.bm25.topics.miracl-v1.0-ko.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-ru-dev runs/run.miracl-v1.0-ru.bm25.topics.miracl-v1.0-ru.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-sw-dev runs/run.miracl-v1.0-sw.bm25.topics.miracl-v1.0-sw.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-te-dev runs/run.miracl-v1.0-te.bm25.topics.miracl-v1.0-te.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-th-dev runs/run.miracl-v1.0-th.bm25.topics.miracl-v1.0-th.dev.txt
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100  miracl-v1.0-zh-dev runs/run.miracl-v1.0-zh.bm25.topics.miracl-v1.0-zh.dev.txt

```


## Effectiveness

### Arabic

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Arabic): dev](https://github.com/project-miracl/miracl)                                              | 0.4809    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Arabic): dev](https://github.com/project-miracl/miracl)                                              | 0.8885    |

### Bengali

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Bengali): dev](https://github.com/project-miracl/miracl)                                              | 0.5079    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Bengali): dev](https://github.com/project-miracl/miracl)                                              | 0.9088    |

### English

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (English): dev](https://github.com/project-miracl/miracl)                                              | 0.3506    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (English): dev](https://github.com/project-miracl/miracl)                                              | 0.8190    |

### Spanish

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Spanish): dev](https://github.com/project-miracl/miracl)                                              | 0.3193    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Spanish): dev](https://github.com/project-miracl/miracl)                                              | 0.7018    |

### Persian

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Persian): dev](https://github.com/project-miracl/miracl)                                              | 0.3334    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Persian): dev](https://github.com/project-miracl/miracl)                                              | 0.7306    |

### Finnish

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Persian): dev](https://github.com/project-miracl/miracl)                                              | 0.5513    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Persian): dev](https://github.com/project-miracl/miracl)                                              | 0.8910    |

### French

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (French): dev](https://github.com/project-miracl/miracl)                                              | 0.1832    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (French): dev](https://github.com/project-miracl/miracl)                                              | 0.6528    |

### Hindi

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Hindi): dev](https://github.com/project-miracl/miracl)                                              | 0.4578    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Hindi): dev](https://github.com/project-miracl/miracl)                                              | 0.8679    |

### Indonesian

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Indonesian): dev](https://github.com/project-miracl/miracl)                                              | 0.4486    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Indonesian): dev](https://github.com/project-miracl/miracl)                                              | 0.9041    |

### Japanese

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Japanese): dev](https://github.com/project-miracl/miracl)                                              | 0.3689    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Japanese): dev](https://github.com/project-miracl/miracl)                                              | 0.8048    |

### Korean

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Korean): dev](https://github.com/project-miracl/miracl)                                              | 0.4190    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Korean): dev](https://github.com/project-miracl/miracl)                                              | 0.7831    |

### Russian

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Russian): dev](https://github.com/project-miracl/miracl)                                              | 0.3342    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Russian): dev](https://github.com/project-miracl/miracl)                                              | 0.6614    |

### Swahili

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Swahili): dev](https://github.com/project-miracl/miracl)                                              | 0.3826    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Swahili): dev](https://github.com/project-miracl/miracl)                                              | 0.7008    |

### Telugu

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Telugu): dev](https://github.com/project-miracl/miracl)                                              | 0.4942    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Telugu): dev](https://github.com/project-miracl/miracl)                                              | 0.8307    |

### Thai

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Thai): dev](https://github.com/project-miracl/miracl)                                              | 0.4838    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Thai): dev](https://github.com/project-miracl/miracl)                                              | 0.8874    |

### Chinese

With the above commands, you should be able to reproduce the following results:

| **nDCG@10**                                                                                                  | **BM25 (default)**| 
|:-------------------------------------------------------------------------------------------------------------|-----------|
| [MIRACL (Chinese): dev](https://github.com/project-miracl/miracl)                                              | 0.1801    |
| **Recall@100**                                                                                              | **BM25 (default)**|
| [MIRACL (Chinese): dev](https://github.com/project-miracl/miracl)                                              | 0.5599    |
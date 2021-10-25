# Pyserini: Learning-To-Rank Reranking Baseline for MS MARCO Document

This guide contains instructions for running learning-to-rank baseline on the [MS MARCO *document* reranking task](https://microsoft.github.io/msmarco/).
Learning-to-rank serves as a second stage reranker after BM25 retrieval.
Note, we use sliding window and maxP strategy here.

## Data Preprocessing

We're going to use the repository's root directory as the working directory. 

First, we need to download and extract the MS MARCO document dataset:

```bash
mkdir collections/msmarco-doc
wget https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-doc/msmarco-docs.tsv.gz -P collections/msmarco-doc
wget https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-doc/msmarco_doc_passage_ids.txt -P collections/msmarco-doc
```

We will need to generate collection of passage segments.
```bash
python scripts/ltr_msmarco-document/convert_msmarco_passage_doc_to_anserini.py \
  --original_docs_path collections/msmarco-doc/msmarco-docs.tsv.gz \
  --doc_ids_path collections/msmarco-doc/msmarco_doc_passage_ids.txt \
  --output_docs_path collections/msmarco-doc/msmarco_pass_doc.jsonl
```

```bash
python scripts/ltr_msmarco-passage/convert_collection_to_jsonl.py --collection-path collections/msmarco-doc/msmarco_pass_doc.jsonl --output-folder collections/msmarco-doc/msmarco_pass_doc/

python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
  -threads 21 -input collections/msmarco-doc/msmarco_pass_doc \
  -index indexes/lucene-index-msmarco-doc-passage -storePositions -storeDocvectors -storeRaw 

python -m pyserini.search --topics msmarco-doc-dev \
 --index indexes/lucene-index-msmarco-doc-passage \
 --output collections/msmarco-doc/run.msmarco-pass-doc.bm25.txt \
 --bm25 --output-format trec --hits 10000 
```

Now, we prepare queries:
```bash
mkdir collections/msmarco-ltr-document

python scripts/ltr_msmarco-passage/convert_queries.py \
  --input tools/topics-and-qrels/topics.msmarco-doc.dev.txt \
  --output collections/msmarco-ltr-document/queries.dev.small.json

python scripts/ltr_msmarco-passage/convert_queries.py \
  --input collections/msmarco-doc/msmarco-doctrain-queries.tsv \
  --output collections/msmarco-ltr-document/queries.train.json
```

```bash
python -m pyserini.ltr.search_msmarco_document --input collections/msmarco-doc/run.msmarco-pass-doc.bm25.txt --input-format tsv   --model runs/msmarco-passage-ltr-mrr-v1   --index indexes/lucene-index-msmarco-document-ltr/ --output runs/run.ltr.doc-pas.trec

python scripts/ltr_msmarco-document/generate_document_score_withmaxP.py --input runs/run.ltr.doc-pas.trec --output runs/run.ltr.doc_level.tsv
```

```bash
python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
--run runs/run.ltr.doc_level.tsv

```
```bash
#####################
MRR @100: 0.3105532197278601
QueriesRanked: 5193
#####################
```

## Building the Index From Scratch

Equivalently, we can preprocess collection and queries with our scripts:

```bash
python scripts/ltr_msmarco-document/convert_passage_doc.py \
  --input collections/msmarco-doc/msmarco_pass_doc.jsonl \
  --output collections/msmarco-ltr-document/ltr_msmarco_pass_doc.jsonl \
  --proc_qty 10
```

The above script will convert the collection and queries to json files with `text_unlemm`, `analyzed`, `text_bert_tok` and `raw` fields.
Next, we need to convert the MS MARCO json collection into Anserini's jsonl files (which have one json object per line):

```bash
python scripts/ltr_msmarco-passage/convert_collection_to_jsonl.py \
  --collection-path collections/msmarco-ltr-document/ltr_msmarco_pass_doc.jsonl \
  --output-folder collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  
```
The above script should generate 21 jsonl files in `collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl`, each with 1M lines (except for the last one, which should have 841,823 lines).

We can now index these docs as a `JsonCollection` using Anserini with pretokenized option:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 21 -input collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  \
 -index indexes/lucene-index-msmarco-document-ltr -storePositions -storeDocvectors -storeRaw -pretokenized
```

Note that pretokenized option let Anserini use whitespace analyzer so that do not break our preprocessed tokenization.

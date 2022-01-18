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

We will need to generate collection of passage segments. Here, we use segment size 3 and stride is 1.
```bash
python scripts/ltr_msmarco/convert_msmarco_passage_doc_to_anserini.py \
  --original_docs_path collections/msmarco-doc/msmarco-docs.tsv.gz \
  --doc_ids_path collections/msmarco-doc/msmarco_doc_passage_ids.txt \
  --output_docs_path collections/msmarco-doc/msmarco_pass_doc.jsonl
```

Let's first get bag-of-words 10000 hits for segments as our LTR reranking candidates.
```bash
python scripts/ltr_msmarco/convert_collection_to_jsonl.py --collection-path collections/msmarco-doc/msmarco_pass_doc.jsonl --output-folder collections/msmarco-doc/msmarco_pass_doc/

python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
  -threads 21 -input collections/msmarco-doc/msmarco_pass_doc \
  -index indexes/lucene-index-msmarco-doc-passage -storePositions -storeDocvectors -storeRaw 

python -m pyserini.search --topics msmarco-doc-dev \
 --index indexes/lucene-index-msmarco-doc-passage \
 --output collections/msmarco-doc/run.msmarco-pass-doc.bm25.txt \
 --bm25 --output-format trec --hits 10000 
```

Now, we prepare queries for LTR:
```bash
mkdir collections/msmarco-ltr-document

python scripts/ltr_msmarco/convert_queries.py \
  --input tools/topics-and-qrels/topics.msmarco-doc.dev.txt \
  --output collections/msmarco-ltr-document/queries.dev.small.json

```

Download pretrained IBM models:

```bash
wget https://www.dropbox.com/s/vlrfcz3vmr4nt0q/ibm_model.tar.gz -P collections/msmarco-ltr-document/
tar -xzvf collections/msmarco-ltr-document/ibm_model.tar.gz -C collections/msmarco-ltr-document/
```

Download our pretrained LTR model:

```bash
wget https://www.dropbox.com/s/ffl2bfw4cd5ngyz/msmarco-passage-ltr-mrr-v1.tar.gz -P runs/
tar -xzvf runs/msmarco-passage-ltr-mrr-v1.tar.gz -C runs
```

Get our prebuilt LTR document index:
```bash
python -c "from pyserini.search import SimpleSearcher; SimpleSearcher.from_prebuilt_index('msmarco-document-ltr')"
```

Now, we have all things ready and can run inference. The LTR outpus rankings on segments level. We will need to use another script to get doc level results using maxP strategy.
```bash
python scripts/ltr_msmarco/ltr_inference.py \
       --input collections/msmarco-doc/run.msmarco-pass-doc.bm25.txt \
       --input-format trec \
       --model runs/msmarco-passage-ltr-mrr-v1 \
       --data document \
       --ibm-model collections/msmarco-ltr-document/ibm_model/ \
       --queries collections/msmarco-ltr-document \
       --index ~/.cache/pyserini/indexes/index-msmarco-doc-per-passage-ltr-20211031-33e4151 --output runs/run.ltr.doc-pas.trec 

python scripts/ltr_msmarco/generate_document_score_withmaxP.py \
      --input runs/run.ltr.doc-pas.trec \
      --output runs/run.ltr.doc_level.tsv
```

```bash
python tools/scripts/msmarco/msmarco_doc_eval.py \
    --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
    --run runs/run.ltr.doc_level.tsv

```
The above evaluation should give your results as below.
```bash
#####################
MRR @100: 0.3090492928920076
QueriesRanked: 5193
#####################
```

## Building the Index From Scratch

```bash
python scripts/ltr_msmarco/convert_passage_doc.py \
  --input collections/msmarco-doc/msmarco_pass_doc.jsonl \
  --output collections/msmarco-ltr-document/ltr_msmarco_pass_doc.jsonl \
  --proc_qty 10
```

The above script will convert the collection and queries to json files with `text_unlemm`, `analyzed`, `text_bert_tok` and `raw` fields.
Next, we need to convert the MS MARCO json collection into Anserini's jsonl files (which have one json object per line):

```bash
python scripts/ltr_msmarco/convert_collection_to_jsonl.py \
  --collection-path collections/msmarco-ltr-document/ltr_msmarco_pass_doc.jsonl \
  --output-folder collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  
```
We can now index these docs as a `JsonCollection` using Anserini with pretokenized option:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 21 -input collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  \
 -index indexes/lucene-index-msmarco-doc-per-passage-ltr -storePositions -storeDocvectors -storeRaw -pretokenized
```

Note that pretokenized option let Anserini use whitespace analyzer so that do not break our preprocessed tokenization.

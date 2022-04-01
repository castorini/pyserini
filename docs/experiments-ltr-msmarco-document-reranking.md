# Pyserini: LTR Filtering for MS MARCO Document

This page describes how to reproduce the ltr experiments in the following paper

> Yue Zhang, Chengcheng Hu, Yuqi Liu, Hui Fang, and Jimmy Lin. [Learning to Rank in the Age of Muppets: Effectiveness–Efficiency Tradeoffs in Multi-Stage Ranking](https://aclanthology.org/2021.sustainlp-1.8) _Proceedings of the Second Workshop on Simple and Efficient Natural Language Processing_, pages 64–73, 2021.

This guide contains instructions for running learning-to-rank baseline on the [MS MARCO *document* reranking task](https://microsoft.github.io/msmarco/).
Learning-to-rank serves as a second stage-reranker after BM25 retrieval; we use a sliding window and MaxP strategy here.

## Performing Retrieval

We're going to use the repository's root directory as the working directory. 

```bash
mkdir collections/msmarco-ltr-document
```

Download our already trained IBM model:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-ibm.tar.gz -P collections/msmarco-ltr-document/
tar -xzvf collections/msmarco-ltr-document/model-ltr-ibm.tar.gz -C collections/msmarco-ltr-document/
```

Download our already trained LTR model:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-msmarco-passage-mrr-v1.tar.gz -P collections/msmarco-ltr-document/
tar -xzvf collections/msmarco-ltr-document/model-ltr-msmarco-passage-mrr-v1.tar.gz -C collections/msmarco-ltr-document/
```

Now, we have all things ready and can run inference:

```bash
python -m pyserini.search.lucene.ltr \
  --index msmarco-doc-per-passage-ltr \
  --model collections/msmarco-ltr-document/msmarco-passage-ltr-mrr-v1 \
  --ibm-model collections/msmarco-ltr-document/ibm_model/ \
  --topic tools/topics-and-qrels/topics.msmarco-doc.dev.txt \
  --qrel tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
  --output runs/run.ltr.msmarco-doc.tsv \
  --granularity document \
  --max-passage --hits 10000
```

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:

```bash
$ python tools/scripts/msmarco/msmarco_doc_eval.py \
    --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
    --run runs/run.ltr.msmarco-doc.tsv

#####################
MRR @100: 0.31088730804779396
QueriesRanked: 5193
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@10.
For that we first need to convert the run file into TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.ltr.msmarco-doc.tsv --output runs/run.ltr.msmarco-doc.trec

$ python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
    --input tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
    --output collections/msmarco-ltr-document/qrels.dev.small.trec
```

And then run the `trec_eval` tool:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
    collections/msmarco-ltr-document/qrels.dev.small.trec runs/run.ltr.msmarco-doc.trec

map                   	all	0.3109
recall_1000           	all	0.9268
```

## Building the Index from Scratch
First, we need to download collections.

```bash
mkdir collections/msmarco-doc
wget https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-doc/msmarco-docs.tsv.gz -P collections/msmarco-doc
wget https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-doc/msmarco_doc_passage_ids.txt -P collections/msmarco-doc
```

We will need to generate collection of passage segments. Here, we use segment size 3 and stride is 1 and then append fields for ltr pipeline.

```bash
python scripts/ltr_msmarco/convert_msmarco_passage_doc_to_anserini.py \
  --original_docs_path collections/msmarco-doc/msmarco-docs.tsv.gz \
  --doc_ids_path collections/msmarco-doc/msmarco_doc_passage_ids.txt \
  --output_docs_path collections/msmarco-doc/msmarco_pass_doc.jsonl

python scripts/ltr_msmarco/convert_passage_doc.py \
  --input collections/msmarco-doc/msmarco_pass_doc.jsonl \
  --output collections/msmarco-ltr-document/ltr_msmarco_pass_doc.json \
  --proc_qty 10
```

The above script will convert the collection and queries to json files with `text_unlemm`, `analyzed`, `text_bert_tok` and `raw` fields.
Note that the tokenization script depends on spaCy; our implementation currently depends on v3.2.1 (this is potentially important as tokenization might change from version to version).
Next, we need to convert the MS MARCO json collection into Anserini's jsonl files (which have one json object per line):

```bash
python scripts/ltr_msmarco/convert_collection_to_jsonl.py \
  --collection-path collections/msmarco-ltr-document/ltr_msmarco_pass_doc.json \
  --output-folder collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  
```

We can now index these docs as a `JsonCollection` using Anserini with pretokenized option:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 21 -input collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl  \
 -index indexes/lucene-index-msmarco-doc-per-passage-ltr -storePositions -storeDocvectors -storeRaw -pretokenized
```

Note that pretokenized option let Anserini use whitespace analyzer so that do not break our preprocessed tokenization.

## Reproduction Log[*](reproducibility.md)

# Pyserini: LTR Filtering for MS MARCO Passage

This page describes how to reproduce the ltr experiments in the following paper
> Yue Zhang and Chengcheng Hu and Yuqi Liu and Hui Fang and Jimmy Lin. [Learning to Rank in the Age of Muppets: Effectiveness–Efficiency Tradeoffs in Multi-Stage Ranking](https://aclanthology.org/2021.sustainlp-1.8) _2021.sustainlp-1.8_.

This guide contains instructions for running learning-to-rank baseline on the [MS MARCO *passage* reranking task](https://microsoft.github.io/msmarco/).
Learning-to-rank serves as a second stage reranker after BM25 retrieval.

## Data Preprocessing

Please first follow the [Pyserini BM25 retrieval guide](experiments-msmarco-passage.md) to obtain our reranking candidate.
Next, we're going to use `collections/msmarco-ltr-passage/` as the working directory to download pre processed data.

```bash
mkdir collections/msmarco-ltr-passage/

python scripts/ltr_msmarco/convert_queries.py \
  --input collections/msmarco-passage/queries.eval.small.tsv \
  --output collections/msmarco-ltr-passage/queries.eval.small.json 

python scripts/ltr_msmarco/convert_queries.py \
  --input collections/msmarco-passage/queries.dev.small.tsv \
  --output collections/msmarco-ltr-passage/queries.dev.small.json

python scripts/ltr_msmarco/convert_queries.py \
  --input collections/msmarco-passage/queries.train.tsv \
  --output collections/msmarco-ltr-passage/queries.train.json
```

The above scripts convert queries to json objects with `text`, `text_unlemm`, `raw`, and `text_bert_tok` fields.
The first two scripts take ~1 min and the third one is a bit longer (~1.5h).

## Performing Inference Using a Trained Model

Download pretrained IBM models:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-ibm.tar.gz -P collections/msmarco-ltr-passage/
tar -xzvf collections/msmarco-ltr-passage/model-ltr-ibm.tar.gz -C collections/msmarco-ltr-passage/
```

Download our trained LTR model:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-msmarco-passage-mrr-v1.tar.gz -P runs/
tar -xzvf runs/model-ltr-msmarco-passage-mrr-v1.tar.gz -C runs
```

The following command generates our reranking result:

```bash
python -m pyserini.search.lucene.ltr 
  --input runs/run.msmarco-passage.bm25tuned.txt \
  --input-format tsv \
  --model runs/msmarco-passage-ltr-mrr-v1 \
  --index msmarco-passage-ltr \
  --data passage \
  --ibm-model collections/msmarco-ltr-passage/ibm_model/ \
  --queries collections/msmarco-ltr-passage \
  --output runs/run.ltr.msmarco-passage.tsv 
```

Here, our model is trained to maximize MRR@10. 
Note that we can also train other models from scratch follow [training guide](experiments-ltr-msmarco-passage-training.md), and replace `--model` argument with your trained model dir.

Inference speed will vary, on orca, it takes ~0.25s/query.

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:

```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py \
   tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt runs/run.ltr.msmarco-passage.tsv
#####################
MRR @10: 0.24709612498294367
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@10.
For that we first need to convert the run file into TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
   --input runs/run.ltr.msmarco-passage.tsv --output runs/run.ltr.msmarco-passage.trec
$ python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
   --input tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt --output collections/msmarco-passage/qrels.dev.small.trec
```

And then run the `trec_eval` tool:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
   collections/msmarco-passage/qrels.dev.small.trec runs/run.ltr.msmarco-passage.trec
map                   	all	0.2551
recall_1000           	all	0.8573       	
```

Average precision or AP (also called mean average precision, MAP) and recall@1000 (recall at rank 1000) are the two metrics we care about the most.
AP captures aspects of both precision and recall in a single metric, and is the most common metric used by information retrieval researchers.
On the other hand, recall@1000 provides the upper bound effectiveness of downstream reranking modules (i.e., rerankers are useless if there isn't a relevant document in the results).

## Building the Index From Scratch

Equivalently, we can preprocess collection and queries with our scripts:

```bash
python scripts/ltr_msmarco/convert_passage.py \
  --input collections/msmarco-passage/collection.tsv \
  --output collections/msmarco-ltr-passage/ltr_collection.json 
```

The above script will convert the collection and queries to json files with `text_unlemm`, `analyzed`, `text_bert_tok` and `raw` fields.
Next, we need to convert the MS MARCO json collection into Anserini's jsonl files (which have one json object per line):

```bash
python scripts/ltr_msmarco/convert_collection_to_jsonl.py \
  --collection-path collections/msmarco-ltr-passage/ltr_collection.json \
  --output-folder collections/msmarco-ltr-passage/ltr_collection_jsonl 
```
The above script should generate 9 jsonl files in `collections/msmarco-ltr-passage/ltr_collection_jsonl`, each with 1M lines (except for the last one, which should have 841,823 lines).

We can now index these docs as a `JsonCollection` using Anserini with pretokenized option:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 9 -input collections/msmarco-ltr-passage/ltr_collection_jsonl  \
 -index indexes/lucene-index-msmarco-passage-ltr -storePositions -storeDocvectors -storeRaw -pretokenized
```

Note that pretokenized option let Anserini use whitespace analyzer so that do not break our preprocessed tokenization.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2021-07-17 (commit [`a6b6545`](https://github.com/castorini/pyserini/commit/a6b6545c0133c03d50d5c33fb2fea7c527de04bb))

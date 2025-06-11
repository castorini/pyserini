# Pyserini: LTR Filtering for MS MARCO Passage

❗ Code associated with these experiments was removed in commit [`a65b96`](https://github.com/castorini/pyserini/commit/a65b9687a91d1ba0f754445ab0e93dd7116c619f).
This page is preserved only for archival purposes.

This page describes how to reproduce the learning-to-rank (LTR) experiments in the following paper:

> Yue Zhang, Chengcheng Hu, Yuqi Liu, Hui Fang, and Jimmy Lin. [Learning to Rank in the Age of Muppets: Effectiveness–Efficiency Tradeoffs in Multi-Stage Ranking](https://aclanthology.org/2021.sustainlp-1.8) _Proceedings of the Second Workshop on Simple and Efficient Natural Language Processing_, pages 64–73, 2021.

This guide contains instructions for running the LTR baseline on the [MS MARCO *passage* reranking task](https://microsoft.github.io/msmarco/).
LTR serves as a second-stage reranker after BM25 retrieval.

## Performing Retrieval

We're going to use root as the working directory.

```bash
mkdir collections/msmarco-ltr-passage
```

Download our already trained IBM model:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-ibm.tar.gz -P collections/msmarco-ltr-passage/
tar -xzvf collections/msmarco-ltr-passage/model-ltr-ibm.tar.gz -C collections/msmarco-ltr-passage/
```

Download our already trained LTR model:

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-msmarco-passage-mrr-v1.tar.gz -P collections/msmarco-ltr-passage
tar -xzvf collections/msmarco-ltr-passage/model-ltr-msmarco-passage-mrr-v1.tar.gz -C collections/msmarco-ltr-passage/
```

The following command generates our reranking result with our prebuilt index:

```bash
python -m pyserini.search.lucene.ltr \
  --index msmarco-passage-ltr \
  --model collections/msmarco-ltr-passage/msmarco-passage-ltr-mrr-v1 \
  --ibm-model collections/msmarco-ltr-passage/ibm_model/ \
  --topic tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt \
  --qrel tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
  --output runs/run.ltr.msmarco-passage.tsv
```

Inference speed will vary; on our `orca` machine, the run takes about half an hour to complete.
Note that internally, retrieval depends on tokenization with spaCy; our implementation currently depends on v3.2.1 (this is potentially important as tokenization might change from version to version).

Here, our model was trained to maximize MRR@10.
We can also train other models from scratch, following the [training guide](experiments-ltr-msmarco-passage-training.md), and replace the `--model` argument with the newly trained model directory.

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset \
    runs/run.ltr.msmarco-passage.tsv

#####################
MRR @10: 0.24723580979669724
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@10.
For that we first need to convert the run file into TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input runs/run.ltr.msmarco-passage.tsv --output runs/run.ltr.msmarco-passage.trec
```

And then run the `trec_eval` tool:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap \
    msmarco-passage-dev-subset runs/run.ltr.msmarco-passage.trec

map                   	all	0.2552
recall_1000           	all	0.8573
```

Average precision or AP (also called mean average precision, MAP) and recall@1000 (recall at rank 1000) are the two metrics we care about the most.
AP captures aspects of both precision and recall in a single metric, and is the most common metric used by information retrieval researchers.
On the other hand, recall@1000 provides the upper bound effectiveness of downstream reranking modules (i.e., rerankers are useless if there isn't a relevant document in the results).

## Building the Index from Scratch

To build an index from scratch, we need to preprocess the collection:

First, download the MS MACRO passage dataset `collectionandqueries.tar.gz`, per instructions [here](experiments-msmarco-passage.md).

```bash
python scripts/ltr_msmarco/convert_passage.py \
  --input collections/msmarco-passage/collection.tsv \
  --output collections/msmarco-ltr-passage/ltr_collection.json
```

The above script will convert the collection to JSON files with `text_unlemm`, `analyzed`, `text_bert_tok` and `raw` fields.
Note that the tokenization script depends on spaCy; our implementation currently depends on v3.2.1 (this is potentially important as tokenization might change from version to version).
Next, we need to convert the MS MARCO JSON collection into Anserini's JSONL format:

```bash
python scripts/ltr_msmarco/convert_collection_to_jsonl.py \
  --collection-path collections/msmarco-ltr-passage/ltr_collection.json \
  --output-folder collections/msmarco-ltr-passage/ltr_collection_jsonl
```

The above script should generate nine JSONL files in `collections/msmarco-ltr-passage/ltr_collection_jsonl`, each with 1M lines (except for the last one, which should have 841,823 lines).

We can now index these docs as a `JsonCollection`:

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/msmarco-ltr-passage/ltr_collection_jsonl \
  --index indexes/lucene-index-msmarco-passage-ltr \
  --generator DefaultLuceneDocumentGenerator \
  --threads 9 \
  --storePositions --storeDocvectors --storeRaw --pretokenized
```

Note that the `--pretokenized` option pretokenized tells Pyserini to use the whitespace analyzer so preserve the existing tokenization.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2021-07-17 (commit [`a6b6545`](https://github.com/castorini/pyserini/commit/a6b6545c0133c03d50d5c33fb2fea7c527de04bb))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2022-04-02 (commit [`88e9a74`](https://github.com/castorini/pyserini/commit/88e9a74c17013217de714e50044a51513c46c87e))

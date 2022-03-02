# Pyserini: IRST on MS MARCO Passage and Document

This page describes how to reproduce IRST experiments with the IBM model on the MS MARCO collections.


## Passage Reranking 

### Data Preprocessing

For IRST, we make the corpus as well as the pre-built indexes available to download.

> You can skip the data prep and indexing steps if you use our pre-built indexes. 

Here, we start from MS MARCO [passage corpus](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md) that has already been processed.
As an alternative, we also make available pre-built indexes (in which case the indexing step can be skipped).


The below scripts convert queries to json objects with text, text_unlemm, raw, and text_bert_tok fields


```bash
mkdir irst_test
python scripts/ltr_msmarco/convert_queries.py --input path_to_topics --output irst_test/queries.irst_topics.dev.small.json
```
Here the path_to_topics represents the path to topics file saved in tools/topics-and-qrels/ folder, e.g., tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt

We can now perform retrieval to gain the baseline:

```
python -m pyserini.search.lucene \
  --index msmarco-passage-ltr \
  --topics topics \
  --output runs/run.topics.bm25tuned.txt \
  --output-format trec \
  --hits 1000 \
  --bm25 --k1 0.82 --b 0.68
```


### Performing Reranking Using Pretrained Model


Download pretrained IBM models:
```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz -P irst_test/
tar -xzvf irst_test/ibm_model_1_bert_tok_20211117.tar.gz -C irst_test
```

Next we can run our script to get our reranking results.

IRST (Sum) 
```bash
python -m pyserini.search.lucene.tprob \
  --base_path runs/run.topics.bm25tuned.txt \                    
  --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
  --query_path irst_test/queries.irst_topics.dev.small.json \
  --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ \
  --output irst_test/regression_test_sum.txt \
  --alpha 0.1
```

IRST (Max)
```bash
python -m pyserini.search.lucene.tprob \
  --base_path runs/run.topics.bm25tuned.txt \                    
  --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
  --query_path irst_test/queries.irst_topics.dev.small.json \
  --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ \
  --output irst_test/regression_test_sum.txt \
  --alpha 0.3 \
  --max_sim
```

For different topics, the `--input`,`--topics` and `--qrel` are different, since Pyserini has all these topics available, we can pass in
different values to run on different datasets.

`--input`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `tools/topics-and-qrels/topics.dl19-passage.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `tools/topics-and-qrels/topics.dl20.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt` <br />

`--topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `dl19-passage` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `dl20` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `msmarco-passage-dev-subset` <br />



After the run finishes, we can also evaluate the results using the official MS MARCO evaluation script:

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c -m ndcg_cut -m map -m recip_rank qrel_file irst_test/regression_test_sum.txt
```

`--qrel_file`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `tools/topics-and-qrels/qrels.dl19-passage.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `tools/topics-and-qrels/qrels.dl20-passage.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt` <br />


Note that we evaluate MRR and NDCG at a cutoff of 10 hits to match the official evaluation metrics.



## Document Reranking 


### Data Preprocessing

For MSMARCO DOC, each MS MARCO document is first segmented into passages, each passage is treated as a unit of indexing. 
We utilized the MaxP technique during the ranking, that is scoring documents based on one of its highest-scoring passage.

The below scripts convert queries to json objects with text, text_unlemm, raw, and text_bert_tok fields

```bash
mkdir irst_test
python scripts/ltr_msmarco/convert_queries.py --input path_to_topics --output irst_test/queries.irst_topics.dev.small.json
```

We can now perform retrieval in anserini to generate baseline:

```
python -m pyserini.search.lucene \
  --index msmarco-document-segment-ltr \
  --topics topics \
  --output runs/run.msmarco-doc-segmented.bm25-default.topics.dev.txt \
  --output-format trec \
  --hits 10000 \
  --bm25 
```

### Performing Reranking Using Pretrained Model


Download pretrained IBM models. Please note that we did not have time to train a new IBM model on MSMARCO DOC data, we used the trained MSMARCO Passage IBM Model1 instead.

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz -P ibm_test/
tar -xzvf ibm_test/ibm_model_1_bert_tok_20211117.tar.gz -C ibm_test
```

Next we can run our script to get our reranking results.

IRST (Sum) 
```bash
python -m pyserini.search.lucene.tprob 
  --base_path runs/run.msmarco-doc-segmented.bm25-default.topics.dev.txt \
  --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
  --query_path irst_test/queries.irst_topics.dev.small.json \
  --index ~/.cache/pyserini/indexes/index-msmarco-document-segment-ltr/ \
  --output irst_test/regression_test_sum.txt \
  --alpha 0.3
```

IRST (Max)
```bash
python -m pyserini.search.lucene.tprob
  --base_path runs/run.msmarco-doc-segmented.bm25-default.topics.dev.txt \
  --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
  --query_path irst_test/queries.irst_topics.dev.small.json \
  --index ~/.cache/pyserini/indexes/index-msmarco-document-segment-ltr/ \
  --output irst_test/regression_test_max.txt \
  --alpha 0.3 \
  --max_sim
```


For different topics, the `--input`,`--topics` and `--qrel` are different, since Pyserini has all these topics available, we can pass in
different values to run on different datasets.

`--input/topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `tools/topics-and-qrels/topics.dl19-doc.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `tools/topics-and-qrels/topics.dl20.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `tools/topics-and-qrels/topics.msmarco-doc.dev.txt` <br />

The reranked runfile contains top 10000 document segments, thus we need to use MaxP technique to get score for each document.

```bash
python scripts/ltr_msmarco/generate_document_score_withmaxP.py --input irst_test/regression_test_sum.txt --output irst_test/regression_test_sum_maxP.tsv
```

We can use the official TREC evaluation tool, trec_eval, to compute other metrics. For that we first need to convert the runs into TREC format:

```bash
python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input irst_test/regression_test_sum_maxP.tsv --output irst_test/regression_test_sum_maxP.trec
```

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c -M 100 -m ndcg_cut -m map -m recip_rank qrel_file irst_test/regression_test_sum.txt
```

`--qrel_file`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `tools/topics-and-qrels/qrels.dl19-doc.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `tools/topics-and-qrels/qrels.dl20-doc.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `tools/topics-and-qrels/qrels.msmarco-doc.dev.txt` <br />

## Results
### Passage Ranking Datasets

| Topics                | Method                        | MRR    | nDCG@10 | Map |
|:-------------------------|:------------------------|:------:|:--------:|:-----------:|
| DL19                | IRST(Sum)               | - | 0.542   | 0.331     |
| DL19                 | IRST(Max)              | - | 0.538   | 0.330      |
| DL20                | IRST(Sum)               | -| 0.551   | 0.334      |
| DL20                | IRST(Max)               | -| 0.541   | 0.325      |
| MS MARCO Dev                | IRST(Sum)               | 0.233| -   | -      |
| MS MARCO Dev                | IRST(Max)               | 0.227| -   | -      |


### Document Ranking Datasets

| Topics                | Method                  | MRR    | nDCG@10 | Map |
|:-------------------------|:------------------------|:------:|:--------:|:-----------:|
| DL19                | IRST(Sum)               | - | 0.573   | 0.354     |
| DL19                 | IRST(Max)              | - | 0.540   | 0.332      |
| DL20                | IRST(Sum)               | -| 0.561   | 0.397     |
| DL20                | IRST(Max)               | -| 0.531   | 0.374      |
| MS MARCO Dev                | IRST(Sum)               | 0.311| -   | -      |
| MS MARCO Dev                | IRST(Max)               | 0.276| -   | -      |

## Build Index from Scratch

Note that we have used our pre-built index in the above steps. You can also build index by yourself following instructions below.

### Passage Index
Please follow steps in [ltr experiment documentation](https://github.com/castorini/pyserini/blob/master/docs/experiments-ltr-msmarco-passage-reranking.md#building-the-index-from-scratch). 

### Document Index
We use the [script](https://github.com/castorini/docTTTTTquery/blob/master/convert_msmarco_passages_doc_to_anserini.py) in docTTTTTquery with default stride and window length to obtain segmented documents.

Then follow instructions in [ltr experiment](https://github.com/castorini/pyserini/blob/master/docs/experiments-ltr-msmarco-document-reranking.md#building-the-index-from-scratch).

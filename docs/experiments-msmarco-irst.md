# Pyserini: IRST on MS MARCO Passage and Document

This page describes how to reproduce IRST experiments with the IBM model on the MS MARCO collections.


## Passage Reranking 

### Data Preprocessing

For IRST, we make the corpus as well as the pre-built indexes available to download.

> You can skip the data prep and indexing steps if you use our pre-built indexes. 

Here, we start from MS MARCO [passage corpus](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md) that has already been processed.
As an alternative, we also make available pre-built indexes (in which case the indexing step can be skipped).

### Performing End-to-End Retrieval Using Already Trained Model

The IBM model we used in this experiment is referenced in the Boytsov et al. [paper](https://arxiv.org/pdf/2102.06815.pdf)
Note that there is a separate guide for training the IBM Model on [FlexNeuART](https://github.com/oaqa/FlexNeuART/tree/master/demo)

Download trained IBM model:
```bash
mkdir irst_test/

wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz -P irst_test/
tar -xzvf irst_test/ibm_model_1_bert_tok_20211117.tar.gz -C irst_test
```

Download term freq statistics for wp collection:
```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-passage.20220411.pickle -P irst_test/
```

Next we can run our script to get our end-to-end results.

IRST (Sum) 
```bash
python -m pyserini.search.lucene.irst \
  --topics topics \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --index msmarco-v1-passage \
  --output irst_test/regression_test_sum.irst_topics.txt \
  --alpha 0.1 \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle
```

IRST (Max)
```bash
python -m pyserini.search.lucene.irst \
  --topics topics \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --index msmarco-v1-passage \
  --output irst_test/regression_test_max.irst_topics.txt \
  --alpha 0.3 \
  --max-sim \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle
```

For different topics, the `--topics` and `--irst_topics` are different, since Pyserini has all these topics available, we can pass in
different values to run on different datasets.

`--topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `tools/topics-and-qrels/topics.dl19-passage.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `tools/topics-and-qrels/topics.dl20.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt` <br />

`--irst_topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Passage: `dl19-passage` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Passage: `dl20` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Passage V1: `msmarco-passage-dev-subset` <br />


After the run finishes, we can also evaluate the results using the official MS MARCO evaluation script:

For TREC DL 2019, use this command to evaluate your run file:

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -l 2 dl19-passage irst_test/regression_test_sum.dl19-passage.txt
```

Similarly for TREC DL 2020,
```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -l 2 dl20-passage irst_test/regression_test_sum.dl20.txt
```

For MS MARCO Passage V1, no need to use -l 2 option:
```bash
python -m pyserini.eval.trec_eval -c -M 10 -m ndcg_cut.10 -m map -m recip_rank msmarco-passage-dev-subset irst_test/regression_test_sum.msmarco-passage-dev-subset.txt
```

## Document Reranking 


### Data Preprocessing

Now, we perform experiment on full document.
### Performing End-to-End Retrieval Using Already Trained Model

Download trained IBM models. Please note that we did not have time to train a new IBM model on MS MARCO doc data, we used the trained MS MARCO passage IBM Model1 instead.

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz -P irst_test/
tar -xzvf irst_test/ibm_model_1_bert_tok_20211117.tar.gz -C irst_test
```

Download term freq statistics for wp collection:
```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc.20220411.pickle -P irst_test/
```

Next we can run our script to get our retrieval results.

IRST (Sum) 
```bash
python -m pyserini.search.lucene.irst \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --topics topics \
  --index msmarco-v1-doc \
  --output irst_test/regression_test_sum.irst_topics.txt \
  --alpha 0.3 \
  --hits 1000 \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle
```

IRST (Max)
```bash
python -m pyserini.search.lucene.irst \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --topics topics \
  --index msmarco-v1-doc \
  --output irst_test/regression_test_max.irst_topics.txt \
  --alpha 0.3 \
  --hits 1000 \
  --max-sim \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle
```


For different topics, the `--topics` and `--irst_topics` are different, since Pyserini has all these topics available, we can pass in
different values to run on different datasets.

`--topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Document: `tools/topics-and-qrels/topics.dl19-doc.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Document: `tools/topics-and-qrels/topics.dl20.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Document V1: `tools/topics-and-qrels/topics.msmarco-doc.dev.txt` <br />

`--irst_topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Document: `dl19-doc-full` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Document: `dl20-doc-full` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Document V1: `msmarco-doc-full` <br />

We can use the official TREC evaluation tool, trec_eval, to compute other metrics. For that we first need to convert the runs into TREC format:

For TREC DL 2019, use this command to evaluate your run file:

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -M 100 dl19-doc irst_test/regression_test_sum.dl19-doc-full.txt
```

Similarly for TREC DL 2020
```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -M 100 dl20-doc irst_test/regression_test_sum.dl20-doc-full.txt
```

For MS MARCO Doc V1
```bash
python -m pyserini.eval.trec_eval -c -M 100 -m ndcg_cut.10 -m map -m recip_rank msmarco-doc-dev irst_test/regression_test_sum.msmarco-doc-full.txt
```


## Document Segment Reranking 


### Data Preprocessing

For MS MARCO doc, each document is first segmented into passages, each passage is treated as a unit of indexing. 
We utilized the MaxP technique during the ranking, that is scoring documents based on one of its highest-scoring passage.

### Performing End-to-End Retrieval Using Already Trained Model


Download trained IBM models. Please note that we did not have time to train a new IBM model on MS MARCO doc data, we used the trained MS MARCO passage IBM Model1 instead.

```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz -P irst_test/
tar -xzvf irst_test/ibm_model_1_bert_tok_20211117.tar.gz -C irst_test
```

Download term freq statistics for wp collection:
```bash
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle -P irst_test/
```

Next we can run our script to get our retrieval results.

IRST (Sum) 
```bash
python -m pyserini.search.lucene.irst \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --topics topics \
  --index msmarco-v1-doc-segmented \
  --output irst_test/regression_test_sum.irst_topics.txt \
  --alpha 0.3 \
  --segments \
  --hits 10000 \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle
```

IRST (Max)
```bash
python -m pyserini.search.lucene.irst \
  --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
  --topics topics \
  --index msmarco-v1-doc-segmented \
  --output irst_test/regression_test_max.irst_topics.txt \
  --alpha 0.3 \
  --hits 10000 \
  --segments \
  --max-sim \
  --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle
```


For different topics, the `--topics` and `--irst_topics` are different, since Pyserini has all these topics available, we can pass in
different values to run on different datasets.

`--topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Document: `tools/topics-and-qrels/topics.dl19-doc.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Document: `tools/topics-and-qrels/topics.dl20.txt` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Document V1: `tools/topics-and-qrels/topics.msmarco-doc.dev.txt` <br />

`--irst_topics`: <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2019 Document: `dl19-doc-seg` <br />
&nbsp;&nbsp;&nbsp;&nbsp;TREC DL 2020 Document: `dl20-doc-seg` <br />
&nbsp;&nbsp;&nbsp;&nbsp;MS MARCO Document V1: `msmarco-doc-seg` <br />

We can use the official TREC evaluation tool, trec_eval, to compute other metrics. For that we first need to convert the runs into TREC format:

For TREC DL 2019, use this command to evaluate your run file:

```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -M 100 dl19-doc irst_test/regression_test_sum.dl19-doc-seg.txt
```

Similarly for TREC DL 2020,  no need to use -l 2 option:
```bash
python -m pyserini.eval.trec_eval -c -m map -m ndcg_cut.10 -M 100 dl20-doc irst_test/regression_test_max.dl20-doc-seg.txt
```

For MS MARCO Doc V1, no need to use -l 2 option:
```bash
python -m pyserini.eval.trec_eval -c -M 100 -m ndcg_cut.10 -m map -m recip_rank msmarco-doc-dev irst_test/regression_test_sum.msmarco-doc-seg.txt
```

## Results
### Passage Ranking Datasets

| Topics                | Method                        | MRR@10    | nDCG@10 | Map |
|:-------------------------|:------------------------|:------:|:--------:|:-----------:|
| DL19                | IRST(Sum)               | - | 0.526   | 0.328     |
| DL19                 | IRST(Max)              | - | 0.537   | 0.329      |
| DL20                | IRST(Sum)               | -| 0.558   | 0.352      |
| DL20                | IRST(Max)               | -| 0.547   | 0.336      |
| MS MARCO Dev                | IRST(Sum)               | 0.221| -   | -      |
| MS MARCO Dev                | IRST(Max)               | 0.215| -   | -      |


### Document Ranking Datasets

| Topics                | Method                  | MRR@100    | nDCG@10 | Map |
|:-------------------------|:------------------------|:------:|:--------:|:-----------:|
| DL19                | IRST(Sum)               | - | 0.549   | 0.252     |
| DL19                 | IRST(Max)              | - | 0.491   | 0.220     |
| DL20                | IRST(Sum)               | - | 0.556   | 0.383     |
| DL20                | IRST(Max)               | - | 0.502   | 0.337     |
| MS MARCO Dev                | IRST(Sum)               |0.303 | -   | -      |
| MS MARCO Dev                | IRST(Max)               |0.253 | -   | -      |

### Document Segment Ranking Datasets

| Topics                | Method                  | MRR@100    | nDCG@10 | Map |
|:-------------------------|:------------------------|:------:|:--------:|:-----------:|
| DL19                | IRST(Sum)               | - | 0.560   | 0.271      |
| DL19                 | IRST(Max)              | - | 0.520   | 0.243      |
| DL20                | IRST(Sum)               | - | 0.536   |  0.376     |
| DL20                | IRST(Max)               | - | 0.510   |   0.350    |
| MS MARCO Dev                | IRST(Sum)               |0.296 | -   | -      |
| MS MARCO Dev                | IRST(Max)               |0.260 | -   | -      |

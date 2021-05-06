# Pyserini: Learning-To-Rank Baseline for MS MARCO Passage Reranking

This guide contains instructions for running Learning-to-Rank baseline on the [MS MARCO *passage* reranking task](https://microsoft.github.io/msmarco/).
Learning-to-Rank serves as a second stage re-ranking after bm25 retrieval.

## Data Preprocess
Please first follow the [pyserini bm25 retrieval guide](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md) to obtain our reranking candidate.
Next, we're going to use `collections/msmarco-ltr-passage/` as the working directory to download pre processed data.

```bash
mkdir collections/msmarco-ltr-passage/

python scripts/ltr_msmarco-passage/convert_queries.py \
--input collections/msmarco-passage/queries.eval.small.tsv \
--output collections/msmarco-ltr-passage/queries.eval.small.json 

python scripts/ltr_msmarco-passage/convert_queries.py \
--input collections/msmarco-passage/queries.dev.small.tsv \
--output collections/msmarco-ltr-passage/queries.dev.small.json

python scripts/ltr_msmarco-passage/convert_queries.py \
--input collections/msmarco-passage/queries.train.tsv \
--output collections/msmarco-ltr-passage/queries.train.json

```
The above scripts convert queries to json objects with text, text_unlemm, raw, text_bert_tok fields.


```bash
wget https://www.dropbox.com/s/se5kokw1qqu8yxs/lucene-index-msmarco-passage-ltr.tar.gz?dl=0 -P indexes/ 
tar -xzvf indexes/lucene-index-msmarco-passage-ltr.tar.gz -C indexes/
```
We can download pre-built index by running the above command.
To confirm, `lucene-index-msmarco-passage-ltr.tar.gz` should have MD5 checksum of `89ffdd8feecfc13aa66e7a9dc1635624`.

Equivalently, we can preprocess collection and queries with our scripts:

```bash
python scripts/ltr_msmarco-passage/convert_passage.py \
--input collections/msmarco-passage/collection.tsv \
--output collections/msmarco-ltr-passage/ltr_collection.json 

```

The above script will convert the collection and queries to json files with text_unlemm, analyzed, text_bert_tok and raw fields.
Next, we need to convert the MS MARCO json collection into Anserini's jsonl files (which have one json object per line):

```bash
python scripts/ltr_msmarco-passage/convert_collection_to_jsonl.py \
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

Then we need to download pre-trained ibm models
```bash
wget https://www.dropbox.com/s/vo7h90j0wqzxvbq/ibm_model.tar.gz?dl=0 -P collections/msmarco-ltr-passage/
tar -xzvf collections/msmarco-ltr-passage/ibm_model.tar.gz -C collections/msmarco-ltr-passage/

```
## Performing Inference Using Pretrained Model
First we need to download the pretrained model.

```bash
wget https://www.dropbox.com/s/vusfjbvy9jl3144/ltr_model.tar.gz?dl=0 -P runs/
tar -xzvf runs/ltr_model.tar.gz -C runs/

```
Next we can run our inference script to get our reranking result.

```bash
python scripts/ltr_msmarco-passage/predict_passage.py \
--rank_list_path runs/run.msmarco-passage.bm25tuned.txt \
--rank_list_format tsv \
--ltr_model_path runs/ltr_model \
--ltr_output_path runs/run.ltr.msmarco-passage.tsv 
```

Here, our model is trained to maximize MRR@10.

Inference speed will vary, on orca, it takes ~0.25s/query.

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:


```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py \
   tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt runs/run.ltr.msmarco-passage.tsv
#####################
MRR @10: 0.24860445945331225
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
map                     all     0.2564
recall_1000             all     0.8573         	
```

Average precision or AP (also called mean average precision, MAP) and recall@1000 (recall at rank 1000) are the two metrics we care about the most.
AP captures aspects of both precision and recall in a single metric, and is the most common metric used by information retrieval researchers.
On the other hand, recall@1000 provides the upper bound effectiveness of downstream reranking modules (i.e., rerankers are useless if there isn't a relevant document in the results).

## Train a model by yourself
```bash
python scripts/ltr_msmarco-passage/train_passage.py   	
```
The above scripts will train a model at `runs/` with your running date in the file name. You can use this as the `--ltr_model_path` parameter for `predict_passage.py`.

## Reproduction Log[*](reproducibility.md)
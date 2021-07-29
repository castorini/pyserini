# Pyserini: Train Learning-To-Rank Reranking Models for MS MARCO Passage

## Data Preprocessing

Please first follow the [Pyserini BM25 retrieval guide](experiments-msmarco-passage.md) to obtain our reranking candidate.

```bash
wget https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.2.tsv.gz -P collections/msmarco-passage/	
gzip -d collections/msmarco-passage/qidpidtriples.train.full.2.tsv.gz
```
Then, download the file which has training triples and uncompress it.

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

The above scripts convert queries to json objects with `text`, `text_unlemm`, `raw`, and `text_bert_tok` fields.
The first two scripts take ~1 min and the third one is a bit longer (~1.5h).

```bash
python -c "from pyserini.search import SimpleSearcher; SimpleSearcher.from_prebuilt_index('msmarco-passage-ltr')"
```

We run the above commands to obtain pre-built index in cache. 

Note you can also build index from scratch follow [this guide](./experiments-ltr-msmarco-passage-reranking.md#L104).

```bash
wget https://www.dropbox.com/s/vlrfcz3vmr4nt0q/ibm_model.tar.gz -P collections/msmarco-ltr-passage/
tar -xzvf collections/msmarco-ltr-passage/ibm_model.tar.gz -C collections/msmarco-ltr-passage/
```
Download pretrained IBM models:

## Training the Model From Scratch
```bash
python scripts/ltr_msmarco-passage/train_ltr_model.py  \
 --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3 
```

Compare texts at the bottom of the output with texts below for a quick sanity check.
```
recall@10:0.48367956064947465
recall@20:0.5796442215854822
recall@50:0.683966093600764
recall@100:0.7545964660936009
recall@200:0.8033428844317098
recall@500:0.8454512893982808
recall@1000:0.8573424068767909
Total training time: XXXX s
Done!
```

Note that the number may vary due to the randomness of LambdaRank. As long as your outputs are around those values, your training is done correctly.

The training script will train a model at `runs/` with your running date in the file name. You can use this as the `--model` parameter for [reranking](experiments-ltr-msmarco-passage-reranking.md#L58).

Number of negative samples used in training can be changed by `--neg-sample`, by default is 10.

## Change the Optmization Goal of Your Trained Model
The script trains a model which optimizes MRR@10 by default. 

You can change the `mrr_at_10`  of [this function](../scripts/ltr_msmarco-passage/train_ltr_model.py#L621) and [here](../scripts/ltr_msmarco-passage/train_ltr_model.py#L358) to `recall_at_20` to train a model which optimizes recall@20.

You can also self defined a function format like [this](../scripts/ltr_msmarco-passage/train_ltr_model.py#L300) and change corresponding places mentioned above to have different optimization goal.

## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2021-07-18 (commit [`a6b6545`](https://github.com/castorini/pyserini/commit/a6b6545c0133c03d50d5c33fb2fea7c527de04bb))

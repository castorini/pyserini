# Pyserini: BM25 and RM3 Baselines for TREC 2022 Fair Ranking Track

This guide contains instructions for running BM25 and RM3 baselines on the [TREC 2022 Fair Ranking Track](https://fair-trec.github.io/)

# Data Prep

This guide requires the [development installation](https://github.com/castorini/pyserini/blob/master/docs/installation.md#development-installation) for additional resource not shipped with the Python module.

First, we need to download the Fair Ranking training dataset and the topics and queries.

TREC 2022 Fair Ranking provides three different formats: plain, text, html

In this example, only plain (7.1GB) will be used, but getting the baselines for the other formats is a nearly identical process.  
The text (16GB) and html (63GB) are significantly bigger than the plain collection so the following commands will also take longer for those collections.

```
mkdir collections/trec-fair-2022
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_plain.json.gz -P collections/trec-fair-2022

wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/2022/train_topics_meta.jsonl -P tools/topics-and-qrels
```

The other data formats can be downloaded optionally
```
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_html.json.gz -P collections/trec-fair-2022
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_text.json.gz -P collections/trec-fair-2022
```

Then, we need to extract the data.
```
gzip -d collections/trec-fair-2022/*.gz
```

Next, we need to convert the data to indexing format.
```
python scripts/trec-fair/convert_trec_fair_2022_data_to_jsonl.py \
  --input collections/trec-fair-2022/trec_corpus_20220301_plain.json \
  --output collections/trec-fair-2022-jsonl/plain/trec_corpus_plain.jsonl
```
This takes about 6 minutes.

We also need to convert the topics into tsv format
```
python scripts/trec-fair/convert_trec_fair_2022_queries_to_tsv.py \
  --input tools/topics-and-qrels/train_topics_meta.jsonl \
  --output tools/topics-and-qrels/trec_fair_2022_queries.tsv
```

We can index the documents with
```
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/trec-fair-2022-jsonl/plain \
  --index indexes/plain \
  --generator DefaultLuceneDocumentGenerator \
  --threads 9 \
  --storePositions --storeDocvectors --storeRaw
```
This takes about 1h. There should be 6,475,537 documents indexed.

# Performing Retrieval on Training Queries

Using BM25
```
python -m pyserini.search.lucene \
  --index indexes/plain \
  --topics tools/topics-and-qrels/trec_fair_2022_queries.tsv \
  --output runs/run.plain.bm25.txt \
  --bm25 \
  --hits 500
```

Using BM25+RM3
```
python -m pyserini.search.lucene \
  --index indexes/plain \
  --topics tools/topics-and-qrels/trec_fair_2022_queries.tsv \
  --output runs/run.plain.bm25.rm3.txt \
  --bm25 \
  --rm3 \
  --hits 500
```

# Evaluation

To evaluate, we first need to convert the given relevant documents into qrels format
```
python scripts/trec-fair/convert_trec_fair_2022_reldocs_to_qrels.py \
  --input tools/topics-and-qrels/train_topics_meta.jsonl \
  --output tools/topics-and-qrels/trec_fair_2022_qrels.txt
```

To evaluate BM25,
```
tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.500 -mP.10 -mndcg -mndcg_cut.10 tools/topics-and-qrels/trec_fair_2022_qrels.txt runs/run.plain.bm25.txt
```
The output should have the following results
```
P_10                  	all	0.6739
recall_500            	all	0.0138
ndcg                  	all	0.0241
ndcg_cut_10           	all	0.6827
```

To evaluate BM25 + RM3
```
tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.500 -mP.10 -mndcg -mndcg_cut.10 tools/topics-and-qrels/trec_fair_2022_qrels.txt runs/run.plain.bm25.rm3.txt
```

The output should have the following results
```
P_10                  	all	0.6717
recall_500            	all	0.0135
ndcg                  	all	0.0236
ndcg_cut_10           	all	0.6972
```

## Reproduction Log[*](reproducibility.md)

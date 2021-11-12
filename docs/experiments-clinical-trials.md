# Pyserini: BM25 and RM3 Baselines for TREC 2021 Clinical Trials

This guide contains instructions for running BM25 and RM3 baselines on the [TREC 2021 Clinical Trials Track](http://www.trec-cds.org/2021.html).

## Data Prep

The guide requires the [development installation](https://github.com/castorini/pyserini/#development-installation) for additional resource that are not shipped with the Python module; for the (more limited) runs that directly work from the Python module installed via `pip`, see [this guide](pypi-reproduction.md).

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the Clinical Trials documents and topics.

```
mkdir collections/trec-ct

wget http://www.trec-cds.org/2021_data/ClinicalTrials.2021-04-27.part1.zip -P collections/trec-ct
wget http://www.trec-cds.org/2021_data/ClinicalTrials.2021-04-27.part2.zip -P collections/trec-ct
wget http://www.trec-cds.org/2021_data/ClinicalTrials.2021-04-27.part3.zip -P collections/trec-ct
wget http://www.trec-cds.org/2021_data/ClinicalTrials.2021-04-27.part4.zip -P collections/trec-ct
wget http://www.trec-cds.org/2021_data/ClinicalTrials.2021-04-27.part5.zip -P collections/trec-ct

unzip 'collections/trec-ct/*.zip' -d collections/trec-ct

wget http://www.trec-cds.org/topics2021.xml -P tools/topics-and-qrels
```

Next we need to convert the documents into a json collection.

```
python scripts/trec-ct/convert_trec21_ct_to_json.py --input_dir collections/trec-ct --output_dir collections/trec-ct-json
```
The size of the output json file collections/trec-ct-json/trec21.json should be 2.4G.

Next we convert topics into tsv queries.

```
python scripts/trec-ct/convert_topic_xml_to_tsv.py --topics tools/topics-and-qrels/topics2021.xml \
                                                   --queries tools/topics-and-qrels/ctqueries2021.tsv
```

Build the index with the following command:

```
python -m pyserini.index --collection JsonCollection \
 --generator DefaultLuceneDocumentGenerator --threads 9 --input collections/trec-ct-json \
 --index indexes/lucene-index-ct --storePositions --storeDocvectors --storeRaw
```

On a modern desktop with an SSD, indexing takes around 5 minutes.
There should be a total of 375,580 documents indexed.

## Performing Retrieval on the Queries

Using bm25
```bash
python -m pyserini.search --topics tools/topics-and-qrels/ctqueries2021.tsv \
 --index indexes/lucene-index-ct \
 --output runs/run.msmarco-doc.bm25.txt \
 --hits 1000 \
 --bm25 --k1 0.9 --b 0.4
```

Using bm25+rm3
```bash
python -m pyserini.search --topics tools/topics-and-qrels/ctqueries2021.tsv \
 --index indexes/lucene-index-ct \
 --output runs/run.msmarco-doc.bm25.rm3.txt \
 --hits 1000 \
 --bm25 --rm3 --k1 0.9 --b 0.4
```

## Evaluation

After the run finishes, we can evaluate the results using the official TREC evaluation tool, `trec_eval`.

First download the qrels file.
```bash
$ wget --user <your_username> --password <your_password> https://trec.nist.gov/act_part/tracks/trials/2021-qrels.txt \
    -P tools/topics-and-qrels
```

For bm25, run this to get the RR and P@10 score:
```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -q -l 2 tools/topics-and-qrels/2021-qrels.txt runs/run.msmarco-doc.bm25.txt
```

You should find these two lines in the output
```
recip_rank            	all	0.3015
P_10                  	all	0.1680
```

In addition, run this to get nDCG@10 score:
```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -q -m ndcg_cut tools/topics-and-qrels/2021-qrels.txt runs/run.msmarco-doc.bm25.txt
```

You should see this line in the output
```
ndcg_cut_10           	all	0.2923
```

For bm25+rm3, run this to get the RR and P@10 score:
```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -q -l 2 tools/topics-and-qrels/2021-qrels.txt runs/run.msmarco-doc.bm25.rm3.txt
```

You should find these two lines in the output
```
recip_rank            	all	0.3659
P_10                  	all	0.2040
```

In addition, run this to get nDCG@10 score:
```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -q -m ndcg_cut tools/topics-and-qrels/2021-qrels.txt runs/run.msmarco-doc.bm25.rm3.txt
```

You should see this line in the output
```
ndcg_cut_10           	all	0.3539
```


## Reproduction Log[*](reproducibility.md)

# Pyserini: BM25 Baseline for the TripClick Dataset

This guide contains instructions for running BM25 baselines for Document Retrieval on the [TripClick benchmark collection](https://tripdatabase.github.io/tripclick/).

**Note:** If you're instantiating an Ubuntu VM on your system or on cloud (AWS and GCP), try to provision enough resources as the tasks such as building the index could take some time to finish such as RAM > 8GB and storage > 100 GB (SSD).
This will prevent going back and fixing machine configuration again and again. If you have a configuration which works for Anserini on this task, it will work with Pyserini as well.

## Data Preparation

The guide requires the [development installation](https://github.com/castorini/pyserini/#development-installation) for additional resources that are not shipped with the Python module;

We're going to use the repository's root directory as the working directory.
First, obtain the TripClick benchmark package, following instructions on the [TripClick benchmark collection web page](https://tripdatabase.github.io/tripclick/).

Uncompress the file: ```tar -xvfz benchmark.tar.gz```

Below we refer to the path to the uncompressed TripClick benchmark on your machine as ```~/../benchmark``` 

### Renaming Query Files
In the current version of TripClick benchmark query files have **.txt** file extensions. In order to be processed with Pyserini the extensions need to be changed
to **.trec**, as the files are written in TREC format. It is done with a simple console command. Move to ```~/../benchmark/qrels``` and ```~/../benchmark/topics``` and copy
the following to the command line for each of the two folders:
```bash
for f in *.txt; do 
    mv -- "$f" "${f%.txt}.trec"
done
```

### Indexing
The command below will create document index of the collection. The result file  will appear in ```indexes/``` folder of pyserini root named ```lucene-index-TRIP-doc```.
```bash
python -m pyserini.index
 -collection CleanTrecCollection \
 -generator DefaultLuceneDocumentGenerator \
 -threads 16 \
 -input ~/../benchmark/documents/ \
 -index indexes/lucene-index-TRIP-doc \
 -storePositions -storeDocvectors -storeRaw
```

Note that the indexing program simply dispatches command-line arguments to an underlying Java program, and so we use the Java single dash convention, e.g., `-index` and not `--index`.
The script will automatically go through all files in ```~/../benchmark/documents/``` and extract the documents.

On a modern desktop with an SSD, indexing of the whole TripClick collection (~1.5m documents) takes around 15 minutes.

## Performing Retrieval

The Train, Validation and Test queries are in ```~/../benchmark/documents/```. As an example we make a run for the file ```topics.head.val.trec```:

```bash
python -m pyserini.search \
 --topics ~/../benchmark/topics/topics.head.val.trec \
 --index indexes/lucene-index-TRIP-doc \
 --output runs/run.trip.head.val.bm25tuned.trec \
 --bm25 \
 --output-format trec
```
the result will be saved in ```runs``` folder of pyserini root named ```un.trip.head.val.bm25tuned.trec```

For the purpose of reproduction of the reults shown in the [TripClick paper](https://arxiv.org/abs/2103.07901) we run BM25 with default parameters.

The option `--output-format msmarco` says to generate output in the trec output format.

## Evaluation with the TREC Official Evaluation Tool
We can also use the official TREC evaluation tool, `trec_eval`, to compute a multitude of metrics on the result.
For that we first need to convert the run file into TREC format:

Run the `trec_eval` tool:

```bash
tools/eval/trec_eval.9.0.4/trec_eval -c \
   -mrecip_rank -mndcg_cut -mrecall  \
   ~/../benchmark/qrels/qrels.dctr.head.val.trec runs/run.trip.head.val.bm25tuned.trec
```
as a result we get:
```
recip_rank              all     0.3142
recall_5                all     0.0894
recall_10               all     0.1454
recall_15               all     0.1879
recall_20               all     0.2281
recall_30               all     0.2941
recall_100              all     0.5046
recall_200              all     0.6250
recall_500              all     0.7700
recall_1000             all     0.8426
ndcg_cut_5              all     0.1338
ndcg_cut_10             all     0.1490
ndcg_cut_15             all     0.1623
ndcg_cut_20             all     0.1764
ndcg_cut_30             all     0.2012
ndcg_cut_100            all     0.2732
ndcg_cut_200            all     0.3089
ndcg_cut_500            all     0.3458
ndcg_cut_1000           all     0.3627
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@yuki617](https://github.com/yuki617) on 2021-05-17 (commit [`e34c902`](https://github.com/castorini/pyserini/commit/e34c9028a6778171f18e4f166b5c79b343f40aab)) 

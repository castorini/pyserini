# Pyserini: Baseline for MS MARCO V2 Collections

This guide contains instructions for running baselines on the V2 of the MS MARCO passage and document test collection, 
which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-v2.md), except that everything is in Python here (no Java).
<!-- Note that there is a separate guide for the [MS MARCO *passage* ranking task](experiments-msmarco-passage.md). -->

**Setup Note:** If you're instantiating an Ubuntu VM on your system or on cloud (AWS and GCP), try to provision enough resources as the tasks such as building the index could take some time to finish such as RAM > 8GB and storage > 100 GB (SSD). This will prevent going back and fixing machine configuration again and again. If you get a configuration which works for Anserini on this task, it will work with Pyserini as well.


## Data Prep
<!-- # Anserini: Guide to Working with the MS MARCO V2 Collections -->

<!-- This guide presents information for working with V2 of the MS MARCO passage and document test collections. -->

If you're having issues downloading the collection via `wget`, try using [AzCopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10).


## MS MARCO Passage V2
Indexing the passage collection, which is 20 GB compressed:

```
python -m pyserini.index -collection MsMarcoPassageV2Collection \
 -generator DefaultLuceneDocumentGenerator -threads 18 \
 -input collections/msmarco_v2_passage \
 -index indexes/msmarco-passage-v2 \
 -storePositions -storeDocvectors -storeRaw
```

Adjust `-threads` as appropriate.
The above configuration, on a 2017 iMac Pro with SSD, takes around 30min.

The complete index occupies 72 GB (138,364,198 passages).
It's big because it includes postions (for phrase queries), document vectors (for relevance feedback), and a complete copy of the collection itself.
The index size can be reduced by removing the options `-storePositions`, `-storeDocvectors`, `-storeRaw` as appropriate.
For reference:

+ Without any of the three above option, index size reduces to 12 GB.
+ With just `-storeRaw`, index size reduces to 47 GB. This setting contains the raw JSON document, which makes it suitable for use as first-stage retrieval to support downstream rerankers. Bloat compared to compressed size of raw collection is due to support for per-document random access.


```
 python -m pyserini.search --index indexes/msmarco-passage-v2 \
        --topics collections/passv2_dev_queries.tsv \
        --output runs/run.msmarco-pass-v2.dev.txt \
        --bm25 --hits 1000 --batch-size 36 --threads 12
```

Evaluation:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -m map -m recall.100,1000 -m recip_rank collections/passv2_dev_qrels.uniq.tsv runs/run.msmarco-pass-v2.dev.txt
map                     all     0.0718
recip_rank              all     0.0728
recall_100            	all     0.3397
recall_1000             all     0.5733
```

## MS MARCO Doc V2
Indexing the document collection, which is 32 GB compressed:

```
python -m pyserini.index -collection MsMarcoDocV2Collection \
 -generator DefaultLuceneDocumentGenerator -threads 18 \
 -input collections/msmarco_v2_doc \
 -index indexes/msmarco-doc-v2 \
 -storePositions -storeDocvectors -storeRaw
```

Same instructions as above.
On the same machine, indexing takes around 40min.
Complete index occupies 134 GB (11,959,635 documents).
Index size can be reduced by removing the options `-storePositions`, `-storeDocvectors`, `-storeRaw` as appropriate.
For reference:

+ Without any of the three above option, index size reduces to 9.4 GB.
+ With just `-storeRaw`, index size reduces to 73 GB. This setting contains the raw JSON document, which makes it suitable for use as first-stage retrieval to support downstream rerankers. Bloat compared to compressed size of raw collection is due to support for per-document random access; evidently, the JSON docs don't compress well.

Perform a run on the dev queries:

```
 python -m pyserini.search --index indexes/msmarco-doc-v2 \
        --topics collections/docv2_dev_queries.tsv \
        --output runs/run.msmarco-doc-v2.dev.txt \
        --bm25 --hits 100 --batch-size 36 --threads 12
```

Evaluation:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -m map -m recall.100 -m recip_rank collections/docv2_dev_qrels.uniq.tsv runs/run.msmarco-doc-v2.dev.txt
map                   	all	0.1552
recip_rank            	all	0.1572
recall_100            	all	0.5956
```

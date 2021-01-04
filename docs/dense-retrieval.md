# Dense Retrieval Replication

Please follow the development installation [here](https://github.com/castorini/pyserini#development-installation) to setup `pyserini`
It's easy to replicate runs on dense retrieval experiments!

## MS MARCO Passage Ranking

MS MARCO passage ranking task, dense retrieval with TCT-ColBERT, HNSW index.
```bash
$ python -m pyserini.dsearch --topics msmarco_passage_dev_subset \
                             --index msmarco-passage-tct_colbert-hnsw \
                             --encoded-queries msmarco-passage-dev-subset-tct_colbert \
                             --output runs/run.msmarco-passage.tct_colbert.hnsw.tsv \
                             --msmarco 
```

To evaluate:

Using official MS MARCO evaluation script:
```bash
$ wget https://www.dropbox.com/s/khsplt2fhqwjs0v/qrels.dev.small.tsv -P collections/msmarco-passage/
$ python tools/scripts/msmarco/msmarco_eval.py qrels.dev.small.tsv runs/run.msmarco-passage.tct_colbert.hnsw.tsv
```
```
#####################
MRR @10: 0.33395142584254184
QueriesRanked: 6980
#####################
```
We can also use the official TREC evaluation tool, trec_eval, to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:
```
python tools/scripts/msmarco/convert_msmarco_to_trec_run.py \
       --input runs/run.msmarco-passage.tct_colbert.hnsw.tsv \
       --output runs/run.msmarco-passage.tct_colbert.hnsw.trec
                                                            
python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
       --input collections/msmarco-passage/qrels.dev.small.tsv \
       --output collections/msmarco-passage/qrels.dev.small.trec
```
And run the trec_eval tool:
```
tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
 collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.hnsw.trec
```
```
map                     all     0.3407
recall_1000             all     0.9618
```

MS MARCO passage ranking task, dense retrieval with TCT-ColBERT, brute force index.

```bash
$ python -m pyserini.dsearch --topics msmarco_passage_dev_subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --encoded-queries msmarco-passage-dev-subset-tct_colbert \
                             --batch 12  \
                             --output runs/run.msmarco-passage.tct_colbert.bf.tsv \
                             --msmarco
```

To evaluate:

Using official MS MARCO evaluation script:
```bash
$ wget https://www.dropbox.com/s/khsplt2fhqwjs0v/qrels.dev.small.tsv -P collections/msmarco-passage/
$ python tools/scripts/msmarco/msmarco_eval.py collections/msmarco-passage/qrels.dev.small.tsv runs/run.msmarco-passage.tct_colbert.bf.tsv
```
```
#####################
MRR @10: 0.3344603629417369
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool, trec_eval, to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:
```
python tools/scripts/msmarco/convert_msmarco_to_trec_run.py \
       --input runs/run.msmarco-passage.tct_colbert.bf.tsv \
       --output runs/run.msmarco-passage.tct_colbert.bf.trec
                                                            
python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
       --input collections/msmarco-passage/qrels.dev.small.tsv \
       --output collections/msmarco-passage/qrels.dev.small.trec
```
And run the trec_eval tool:
```
tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
 collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.bf.trec
```

```
map                   	all	0.3412
recall_1000           	all	0.9637
```
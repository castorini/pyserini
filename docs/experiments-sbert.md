# Pyserini: Replicating S-BERT MSMARCO Results

## Dense Retrieval

Dense retrieval with SBERT, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index dindex-msmarco-passage-sbert-bf-20210313-a0fbb3 \
                             --encoder sentence-transformers/msmarco-distilbert-base-v3 \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.sbert.bf.tsv \
                             --msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.tsv
#####################
MRR @10: 0.3313618842952645
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.sbert.bf.tsv --output runs/run.msmarco-passage.sbert.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.sbert.bf.trec
map                     all     0.3372
recall_1000             all     0.9558
```
# Pyserini: Replicating DistilBERT KD Results

## Dense Retrieval

Dense retrieval with distilbert-dot-margin_mse-T2, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
                             --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.tsv \
                             --msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.tsv
#####################
MRR @10: 0.32505867103288255
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.tsv --output runs/run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.trec
map                     all     0.3308
recall_1000             all     0.9553
```
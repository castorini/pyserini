# Pyserini: Replicating Microsoft's ANCE Results

This guide provides replication instructions for the following dense retrieval work:

> Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang, Jialin Liu, Paul Bennett, Junaid Ahmed, Arnold Overwijk. [Approximate Nearest Neighbor Negative Contrastive Learning for Dense Text Retrieval](https://arxiv.org/pdf/2007.00808.pdf)

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.


## MS MARCO Passage
Download the query encoder checkpoint:
```bash
$ wget https://www.dropbox.com/s/u02glpszk3jv6ws/ance-msmarco-passage-encoder.tar.gz
$ tar -xvf ance-msmarco-passage-encoder.tar.gz
```

**ANCE retrieval** with brute-force index:
```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-ance-bf \
                             --encoder ance-msmarco-passage-encoder \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.ance.bf.tsv \
                             --msmarco
```
To evaluate:
```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt runs/run.msmarco-passage.ance.bf.tsv
#####################
MRR @10: 0.3301838017919672
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.ance.bf.tsv --output runs/run.msmarco-passage.ance.bf.trec
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt runs/run.msmarco-passage.ance.bf.trec
map                   	all	0.3363
recall_1000           	all	0.9584
```

## Natural Questions (NQ)
Download the query encoder checkpoint:
```bash
$ https://www.dropbox.com/s/pps5rzzn4ynh3x3/ance-dpr-question_encoder-multi.tar.gz
$ tar -xvf ance-dpr-question_encoder-multi.tar.gz
```

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-ance-multi-bf \
                             --encoder ance-dpr-question_encoder-multi \
                             --output runs/run.ance.nq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.ance.nq-test.multi.bf.trec \
                                                                --output runs/run.ance.nq-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.ance.nq-test.multi.bf.json --topk 20 100
Top20	accuracy: 0.8224376731301939
Top100	accuracy: 0.8786703601108034
```

## Trivia QA
Download the query encoder checkpoint:
```bash
$ wget https://www.dropbox.com/s/pps5rzzn4ynh3x3/ance-dpr-question_encoder-multi.tar.gz
$ tar -xvf ance-dpr-question_encoder-multi.tar.gz
```

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-ance-multi-bf \
                             --encoder ance-dpr-question_encoder-multi \
                             --output runs/run.ance.trivia-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.ance.trivia-test.multi.bf.trec \
                                                                --output runs/run.ance.trivia-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.ance.trivia-test.multi.bf.json --topk 20 100
Top20	accuracy: 0.8010253690444621
Top100	accuracy: 0.852205427384425

```

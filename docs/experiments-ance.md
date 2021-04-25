# Pyserini: Reproducing ANCE Results

This guide provides instructions to reproduce the following dense retrieval work:

> Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang, Jialin Liu, Paul Bennett, Junaid Ahmed, Arnold Overwijk. [Approximate Nearest Neighbor Negative Contrastive Learning for Dense Text Retrieval](https://arxiv.org/pdf/2007.00808.pdf)

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.


## MS MARCO Passage

**ANCE retrieval** with brute-force index:
```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-ance-bf \
                             --encoded-queries ance-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.ance.bf.tsv \
                             --msmarco
```
> _Optional_: replace `--encoded-queries` by `--encoder castorini/ance-msmarco-passage`
> for on-the-fly query encoding.


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

## MS MARCO Document

**ANCE retrieval** with brute-force index:
```bash
$ python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-ance-maxp-bf \
                             --encoded-queries ance_maxp-msmarco-doc-dev \
                             --output runs/run.msmarco-doc.passage.ance-maxp.txt \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --msmarco \
                             --batch-size 36 \
                             --threads 12
```
> _Optional_: replace `--encoded-queries` by `--encoder castorini/ance-msmarco-doc-maxp`
> for on-the-fly query encoding.

To evaluate:
```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.passage.ance-maxp.txt
#####################
MRR @100: 0.37965620295359753
QueriesRanked: 5193
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@100. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc.passage.ance-maxp.txt --output runs/run.msmarco-doc.passage.ance-maxp.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap msmarco-doc-dev runs/run.msmarco-doc.passage.ance-maxp.trec
map                   	all	0.3797
recall_100            	all	0.9033
```

## Natural Questions (NQ)

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-ance-multi-bf \
                             --encoded-queires ance_multi-nq-test \
                             --output runs/run.ance.nq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```
> _Optional_: replace `--encoded-queries` by `--encoder castorini/ance-dpr-question-multi`
> for on-the-fly query encoding.

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

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-ance-multi-bf \
                             --encoded-queries ance_multi-trivia-test \
                             --output runs/run.ance.trivia-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```
> _Optional_: replace `--encoded-queries` by `--encoder castorini/ance-dpr-question-multi`
> for on-the-fly query encoding.

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

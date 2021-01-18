# Dense Retrieval Replication

This guide provides replication instructions for the following dense retrieval work:

+ Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [Distilling Dense Representations for Ranking using Tightly-Coupled Teachers.](https://arxiv.org/abs/2010.11386) arXiv:2010.11386, October 2020. 

You'll need a Pyserini [development installation](https://github.com/castorini/pyserini#development-installation) to get started.

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

```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
   runs/run.msmarco-passage.tct_colbert.hnsw.tsv
#####################
MRR @10: 0.3344676399690711
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10.
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.hnsw.tsv --output runs/run.msmarco-passage.tct_colbert.hnsw.trec
                                                            
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
   collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.hnsw.trec
map                     all     0.3410
recall_1000             all     0.9618
```

> To evaluate with on-the-fly query encoding, replace `--encoded-queries` with our pretrained encoder model
> on [Hugging Face](https://huggingface.co/castorini/tct_colbert-msmarco/tree/main) 
> `--encoder castorini/tct_colbert-msmarco`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.
> NOTE: Using GPU query encoding will give slightly different result. (E.g. MRR @10: 0.3349694137444839)


MS MARCO passage ranking task, dense retrieval with TCT-ColBERT, brute force index.

```bash
$ python -m pyserini.dsearch --topics msmarco_passage_dev_subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --encoded-queries msmarco-passage-dev-subset-tct_colbert \
                             --batch 36  \
                             --threads 12  \
                             --output runs/run.msmarco-passage.tct_colbert.bf.tsv \
                             --msmarco
```

To evaluate:

```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
   runs/run.msmarco-passage.tct_colbert.bf.tsv
#####################
MRR @10: 0.3349694137444839
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.bf.tsv --output runs/run.msmarco-passage.tct_colbert.bf.trec

$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
    collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.bf.trec
map                     all     0.3416
recall_1000             all     0.9640
```

You'll notice that hnsw index leads to a small loss in effectiveness.
> To evaluate with on-the-fly query encoding, replace `--encoded-queries` with our pretrained encoder model
> on [Hugging Face](https://huggingface.co/castorini/tct_colbert-msmarco/tree/main) 
> `--encoder castorini/tct_colbert-msmarco`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.
> NOTE: Using GPU query encoding will give slightly different result. (E.g. MRR @10: 0.3349479237731372)


### Hybrid Dense-Sparse Ranking
MS MARCO passage ranking task, 
Hybrid
- dense retrieval with TCT-ColBERT, HNSW index.
- sparse retrieval with doc2query-T5 expanded index.

```
python -m pyserini.hsearch   dense --index msmarco-passage-tct_colbert-hnsw \
                                   --encoded-queries msmarco-passage-dev-subset-tct_colbert  \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.24 \
                             run  --topics msmarco_passage_dev_subset \
                                  --output runs/run.msmarco-passage.tct_colbert.hnsw.doc2queryT5.tsv \
                                  --msmarco
```

To evaluate:
```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
   runs/run.msmarco-passage.tct_colbert.hnsw.doc2queryT5.tsv
#####################
MRR @10: 0.36371895893027617
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.hnsw.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert.hnsw.doc2queryT5.trec

$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
    collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.hnsw.doc2queryT5.trec
map                     all     0.3702
recall_1000             all     0.9734
```
> To evaluate with on-the-fly query encoding, replace `--encoded-queries` with our pretrained encoder model
> on [Hugging Face](https://huggingface.co/castorini/tct_colbert-msmarco/tree/main) 
> `--encoder castorini/tct_colbert-msmarco`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.

MS MARCO passage ranking task, 
Hybrid
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```
python -m pyserini.hsearch   dense --index msmarco-passage-tct_colbert-bf \
                                   --batch 36 --threads 12 \
                                   --encoded-queries msmarco-passage-dev-subset-tct_colbert  \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.24 \
                             run  --topics msmarco_passage_dev_subset \
                                  --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv \
                                  --msmarco
```

To evaluate:
```bash
$ python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
   runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv
#####################
MRR @10: 0.36410435712011574
QueriesRanked: 6980
#####################

```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python tools/scripts/msmarco/convert_msmarco_to_trec_run.py --input runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.1000 -mmap \
    collections/msmarco-passage/qrels.dev.small.trec runs/run.msmarco-passage.tct_colbert.bf.doc2queryT5.trec
map                     all     0.3706
recall_1000             all     0.9736
```

> To evaluate with on-the-fly query encoding, replace `--encoded-queries` with our pretrained encoder model
> on [Hugging Face](https://huggingface.co/castorini/tct_colbert-msmarco/tree/main) 
> `--encoder castorini/tct_colbert-msmarco`. The encoding will run on CPU by default. To enable GPU, add `--device cuda:0`.

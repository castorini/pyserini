# Pyserini: TCT-ColBERTv2 for MS MARCO (V1) Collections

This guide provides instructions to reproduce the family of TCT-ColBERT-V2 dense retrieval models described in the following paper:

> Sheng-Chieh Lin, Jheng-Hong Yang, and Jimmy Lin. [In-Batch Negatives for Knowledge Distillation with Tightly-CoupledTeachers for Dense Retrieval.](https://aclanthology.org/2021.repl4nlp-1.17/) _Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)_, pages 163-173, August 2021.

Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## MS MARCO Passage Ranking

Summary of results (figures from the paper are in parentheses):

| Condition | MRR@10 (paper) | MAP | Recall@1000 |
|:----------|-------:|----:|------------:|
| TCT_ColBERT-V2 (brute-force index) |  0.3440 (0.344) | 0.3509 | 0.9670 |
| TCT_ColBERT-V2-HN (brute-force index) |  0.3543 (0.354) | 0.3608 | 0.9708 |
| TCT_ColBERT-V2-HN+ (brute-force index) | 0.3585 (0.359) | 0.3645 | 0.9695 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BoW BM25 | 0.3682 (0.369)  | 0.3737 | 0.9707 |
| TCT_ColBERT-V2-HN+ (brute-force index) + BM25 w/ doc2query-T5 | 0.3731 (0.375) | 0.3789 | 0.9759 |

The slight differences between the reproduced scores and those reported in the paper can be attributed to TensorFlow implementations in the published paper vs. PyTorch implementations here in this reproduction guide.

### TCT_ColBERT-V2

Dense retrieval with TCT-ColBERT, brute-force index:

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-bf \
                             --encoded-queries tct_colbert-v2-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2.bf.tsv \
                             --output-format msmarco
```
Note that to ensure maximum reproducibility, by default Pyserini uses pre-computed query representations that are automatically downloaded.
As an alternative, to perform "on-the-fly" query encoding, see additional instructions below.

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2.bf.tsv
#####################
MRR @10: 0.3440
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool `trec_eval` to compute other metrics than MRR@10. 
For that we first need to convert runs and qrels files to the TREC format:

```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2.bf.trec
map                     all     0.3509
recall_1000             all     0.9670
```

### TCT_ColBERT-V2-HN

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hn-bf \
                             --encoded-queries tct_colbert-v2-hn-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv \
                             --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv
#####################
MRR @10: 0.3543
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hn.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hn.bf.trec
map                     all     0.3608
recall_1000             all     0.9708
```

### TCT_ColBERT-V2-HN+

```bash
$ python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hnp-bf \
                             --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             --batch-size 36 \
                             --threads 12 \
                             --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv \
                             --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv
#####################
MRR @10: 0.3585
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.trec
map                     all     0.3645
recall_1000             all     0.9695
```

To perform on-the-fly query encoding with our [pretrained encoder model](https://huggingface.co/castorini/tct_colbert-v2-hnp-msmarco) use the option `--encoder castorini/tct_colbert-v2-hnp-msmarco`.
Query encoding will run on the CPU by default.
To perform query encoding on the GPU, use the option `--device cuda:0`.

### Hybrid Dense-Sparse Retrieval with TCT_ColBERT-V2-HN+

Hybrid retrieval with dense-sparse representations (without document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with BM25 `msmarco-passage` (i.e., default bag-of-words) index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.06 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv
#####################
MRR @10: 0.3682
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.bm25.trec
map                   	all	0.3737
recall_1000           	all	0.9707
```

Follow the same instructions above to perform on-the-fly query encoding.

Hybrid retrieval with dense-sparse representations (with document expansion):
- dense retrieval with TCT-ColBERT, brute force index.
- sparse retrieval with doc2query-T5 expanded index.

```bash
$ python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoded-queries tct_colbert-v2-hnp-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.1 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv \
                                    --batch-size 36 --threads 12 \
                                    --output-format msmarco
```

To evaluate:

```bash
$ python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv
#####################
MRR @10: 0.3731
QueriesRanked: 6980
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.tsv --output runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset runs/run.msmarco-passage.tct_colbert-v2-hnp.bf.doc2queryT5.trec
map                   	all	0.3789
recall_1000           	all	0.9759
```

Follow the same instructions above to perform on-the-fly query encoding.


## MS MARCO Document Ranking with TCT-ColBERT-V2 (zero-shot)

Document retrieval with TCT-ColBERT, brute-force index:

Step0: prepare docs.json: split docs into segments of passages
Each line contains a json dict as follows:
{"id": "[doc_id]#[seg_id]", "contents": "[url]\n[title]\n[seg_text]"}


Step1: split documents for parallel encoding
```bash
$ split -a 2 -d -n l/50 docs.json collection.part
```

Step2-1: prepare encoder (on CC), you can download encoder using [git-lfs](https://git-lfs.github.com/)

Example (after you install git-lfs):
```bash
git clone https://huggingface.co/castorini/tct_colbert-v2-hnp-msmarco
```

Step2-2: run encoding
```bash
export TASK=msmarco
export ENCODER=tct_colbert-v2-msmarco-hnp
export WORKING_DIR=~/scratch

for i in $(seq -f "%02g" 0 49)
do
	srun --gres=gpu:v100:1 --mem=16G --cpus-per-task=2 --time=2:00:00 \
	python scripts/tct_colbert/encode_corpus_msmarco_doc.py \
		--corpus ${WORKING_DIR}/${TASK}/collection.part${i} \
		--encoder ${WORKING_DIR}/checkpoint/${ENCODER} \
		--index indexes/${TASK}-${ENCODER}-${i} \
		--index indexes/${TASK}-${ENCODER}-${i} \
		--batch 16 \
		--device cuda:0 &
done
```

Step3: merge / filter index, use --segment-num -1 for maxp (1 for firstp), or anyother interger you like
```bash
$ python scripts/tct_colbert/merge_indexes.py \
    --prefix <path_to_index> \
    --shard-num 50
    --segment-num -1
```

Step4: search (with on-the-fly query encoding)
```bash
$ python -m pyserini.dsearch --topics msmarco-doc-dev \
	--index <path_to_index>/msmarco-tct_colbert-v2-hnp-msmarco-full-maxp \
	--encoder castorini/tct_colbert-v2-hnp-msmarco \
	--output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
	--hits 1000 \
	--max-passage \
	--max-passage-hits 100 \
	--output-format msmarco \
	--batch-size 144 \
	--threads 36

$ python -m pyserini.dsearch --topics dl19-doc \
	--index <path_to_index>/msmarco-tct_colbert-v2-hnp-msmarco-full-maxp \
	--encoder castorini/tct_colbert-v2-hnp-msmarco \
	--output runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt \
	--hits 1000 \
	--max-passage \
	--max-passage-hits 100 \
	--output-format msmarco \
	--batch-size 144 \
	--threads 36
```

Step5: eval

For MSMARCO-Doc-dev
```bash
$ python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt

#####################
MRR @100: 0.3508557690776294
QueriesRanked: 5193
#####################

$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.txt \
 --output runs/run.msmarco-doc.passage.tct_colbert-v2-hnp-maxp.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 msmarco-doc-dev 

Results:
map                     all     0.3509
recall_100              all     0.8908
ndcg_cut_10             all     0.4123

```

For TREC-DL19
```bash
$ python -m pyserini.eval.convert_msmarco_run_to_trec_run --input runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.txt \
 --output runs/run.dl19-doc.passage.tct_colbert-v2-hnp-maxp.trec
$ python -m pyserini.eval.trec_eval -c -mrecall.100 -mmap -mndcg_cut.10 dl19-doc 

Results:
map                     all     0.2683
recall_100              all     0.3854
ndcg_cut_10             all     0.6592
```


## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-07-01 (commit [`b1576a2`](https://github.com/castorini/pyserini/commit/b1576a2c3e899349be12e897f92f3ad75ec82d6f))

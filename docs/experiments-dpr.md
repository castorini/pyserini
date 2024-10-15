# Pyserini: Reproducing DPR Results

Dense passage retriever (DPR) is a dense retrieval method described in the following paper:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih. [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/). _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2020.

We have replicated DPR results and incorporated the technique into Pyserini.
Our own efforts are described in the following paper:

> Xueguang Ma, Kai Sun, Ronak Pradeep, Minghan Li, and Jimmy Lin. [Another Look at DPR: Reproduction of Training and Replication of Retrieval](https://link.springer.com/chapter/10.1007/978-3-030-99736-6_41). Proceedings of the 44th European Conference on Information Retrieval (ECIR 2022), Part I, pages 613-626, April 2021, Stavanger, Norway.

Which evolved from a previous arXiv preprint:

> Xueguang Ma, Kai Sun, Ronak Pradeep, and Jimmy Lin. [A Replication Study of Dense Passage Retriever](https://arxiv.org/abs/2104.05740). _arXiv:2104.05740_, April 2021. 

To be clear, we started with model checkpoint releases in the official [DPR repo](https://github.com/facebookresearch/DPR) and did _not_ retrain the query and passage encoders from scratch.
Our implementation does not share any code with the DPR repo, other than evaluation scripts to ensure that results are comparable.

This guide provides instructions to reproduce our replication study.
Our efforts include both retrieval and end-to-end answer extraction, but we only cover retrieval here.

Note that we often observe minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## Summary

Here's how our results stack up against results reported in the paper using the DPR-Multi model:

| Dataset     | Method        | Top-20 (orig) | Top-20 (us) | Top-100 (orig) | Top-100 (us) |
|:------------|:--------------|--------------:|------------:|---------------:|-------------:|
| NQ          | DPR           |          79.4 |        79.5 |           86.0 |         86.1 |
| NQ          | BM25          |          59.1 |        63.0 |           73.7 |         78.2 |
| NQ          | Hybrid        |          78.0 |        82.6 |           83.9 |         88.6 |
| TriviaQA    | DPR           |          78.8 |        78.9 |           84.7 |         84.8 |
| TriviaQA    | BM25          |          66.9 |        76.4 |           76.7 |         83.1 |
| TriviaQA    | Hybrid        |          79.9 |        82.6 |           84.4 |         86.6 |
| WQ          | DPR           |          75.0 |        75.1 |           82.9 |         83.0 |
| WQ          | BM25          |          55.0 |        62.3 |           71.1 |         75.5 |
| WQ          | Hybrid        |          74.7 |        77.1 |           82.3 |         84.4 |
| CuratedTREC | DPR           |          89.1 |        88.8 |           93.9 |         93.4 |
| CuratedTREC | BM25          |          70.9 |        80.7 |           84.1 |         89.9 |
| CuratedTREC | Hybrid        |          88.5 |        90.1 |           94.1 |         95.0 |
| SQuAD       | DPR           |          51.6 |        52.0 |           67.6 |         67.7 |
| SQuAD       | BM25          |          68.8 |        71.1 |           80.0 |         81.8 |
| SQuAD       | Hybrid        |          66.2 |        75.1 |           78.6 |         84.4 |

The hybrid results reported above for "us" capture what we call the "norm" condition (see paper for details).
Note that the results below represent the current state of the code base, where there may be minor differences in effectiveness from what's reported in the paper.

## Natural Questions (NQ) with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-nq-test \
  --encoded-queries dpr_multi-nq-test \
  --output runs/run.encoded.dpr.nq-test.multi.trec \
  --batch-size 512 --threads 16
```

The option `--encoded-queries` specifies the use of encoded queries (i.e., queries that have already been converted into dense vectors and cached).
As an alternative, replace with `--encoder facebook/dpr-question_encoder-multiset-base` to perform "on-the-fly" query encoding, i.e., convert text queries into dense vectors as part of the dense retrieval process.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.encoded.dpr.nq-test.multi.trec \
  --output runs/run.encoded.dpr.nq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.nq-test.multi.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7947
Top100 accuracy: 0.8609
```

**BM25 retrieval**:

```bash
python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --output runs/run.encoded.dpr.nq-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.encoded.dpr.nq-test.bm25.trec \
  --output runs/run.encoded.dpr.nq-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.nq-test.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.6299
Top100 accuracy: 0.7823
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoded-queries dpr_multi-nq-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.3 \
  run    --topics dpr-nq-test \
         --output runs/run.encoded.dpr.nq-test.multi.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.encoded.dpr.nq-test.multi.bm25.trec \
  --output runs/run.encoded.dpr.nq-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.nq-test.multi.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.8260
Top100 accuracy: 0.8859
```

## TriviaQA with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-trivia-test \
  --encoded-queries dpr_multi-trivia-test \
  --output runs/run.encoded.dpr.trivia-test.multi.trec \
  --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.encoded.dpr.trivia-test.multi.trec \
  --output runs/run.encoded.dpr.trivia-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.trivia-test.multi.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7887
Top100 accuracy: 0.8479
```

**BM25 retrieval**:

```bash
python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --output runs/run.encoded.dpr.trivia-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.encoded.dpr.trivia-test.bm25.trec \
  --output runs/run.encoded.dpr.trivia-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.trivia-test.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7641
Top100 accuracy: 0.8314
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoded-queries dpr_multi-trivia-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 0.95 \
  run    --topics dpr-trivia-test \
         --output runs/run.encoded.dpr.trivia-test.multi.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-trivia-test \
  --input runs/run.encoded.dpr.trivia-test.multi.bm25.trec \
  --output runs/run.encoded.dpr.trivia-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.trivia-test.multi.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.8264
Top100 accuracy: 0.8655
```

## WebQuestions (WQ) with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-wq-test \
  --encoded-queries dpr_multi-wq-test \
  --output runs/run.encoded.dpr.wq-test.multi.trec \
  --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.encoded.dpr.wq-test.multi.trec \
  --output runs/run.encoded.dpr.wq-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.wq-test.multi.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7505
Top100 accuracy: 0.8297
```

**BM25 retrieval**:

```bash
python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --output runs/run.encoded.dpr.wq-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.encoded.dpr.wq-test.bm25.trec \
  --output runs/run.encoded.dpr.wq-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.wq-test.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.6230
Top100 accuracy: 0.7549
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoded-queries dpr_multi-wq-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 0.95 \
  run    --topics dpr-wq-test \
         --output runs/run.encoded.dpr.wq-test.multi.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` with `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-wq-test \
  --input runs/run.encoded.dpr.wq-test.multi.bm25.trec \
  --output runs/run.encoded.dpr.wq-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.wq-test.multi.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7712
Top100 accuracy: 0.8440
```

## CuratedTREC with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-curated-test \
  --encoded-queries dpr_multi-curated-test \
  --output runs/run.encoded.dpr.curated-test.multi.trec \
  --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` with for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.encoded.dpr.curated-test.multi.trec \
  --output runs/run.encoded.dpr.curated-test.multi.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.curated-test.multi.json \
  --topk 20 100 \
  --regex
```

And the expected results:

```
Top20  accuracy: 0.8876
Top100 accuracy: 0.9337
```

**BM25 retrieval**:

```bash
python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --output runs/run.encoded.dpr.curated-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.encoded.dpr.curated-test.bm25.trec \
  --output runs/run.encoded.dpr.curated-test.bm25.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.curated-test.bm25.json \
  --topk 20 100 \
  --regex
```

And the expected results:

```
Top20  accuracy: 0.8069
Top100 accuracy: 0.8991
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoded-queries dpr_multi-curated-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.05 \
  run    --topics dpr-curated-test \
         --output runs/run.encoded.dpr.curated-test.multi.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-curated-test \
  --input runs/run.encoded.dpr.curated-test.multi.bm25.trec \
  --output runs/run.encoded.dpr.curated-test.multi.bm25.json \
  --regex

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.curated-test.multi.bm25.json \
  --topk 20 100 \
  --regex
```

And the expected results:

```
Top20  accuracy: 0.9006
Top100 accuracy: 0.9496
```

## SQuAD with DPR-Multi

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-multi \
  --topics dpr-squad-test \
  --encoded-queries dpr_multi-squad-test \
  --output runs/run.encoded.dpr.squad-test.multi.trec \
  --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.encoded.dpr.squad-test.multi.trec \
  --output runs/run.encoded.dpr.squad-test.multi.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.squad-test.multi.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.5199
Top100 accuracy: 0.6773
```

**BM25 retrieval**:

```bash
python -m pyserini.search.lucene \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --output runs/run.encoded.dpr.squad-test.bm25.trec
```

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.encoded.dpr.squad-test.bm25.trec \
  --output runs/run.encoded.dpr.squad-test.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.squad-test.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7107
Top100 accuracy: 0.8183
```

**Hybrid dense-sparse retrieval** (combining above two approaches):

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-multi \
         --encoded-queries dpr_multi-squad-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 2.00 \
  run    --topics dpr-squad-test \
         --output runs/run.encoded.dpr.squad-test.multi.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-multiset-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-squad-test \
  --input runs/run.encoded.dpr.squad-test.multi.bm25.trec \
  --output runs/run.encoded.dpr.squad-test.multi.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.squad-test.multi.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20  accuracy: 0.7511
Top100 accuracy: 0.8437
```

## Natural Questions (NQ) with DPR-Single

**DPR retrieval** with brute-force index:

```bash
python -m pyserini.search.faiss \
  --index wikipedia-dpr-100w.dpr-single-nq \
  --topics dpr-nq-test \
  --encoded-queries dpr_single_nq-nq-test \
  --output runs/run.encoded.dpr.nq-test.single.trec \
  --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-single-nq-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index wikipedia-dpr-100w \
  --topics dpr-nq-test \
  --input runs/run.encoded.dpr.nq-test.single.trec \
  --output runs/run.encoded.dpr.nq-test.single.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.nq-test.single.json \
  --topk 20 100
```

And the expected results:

```
Top20	accuracy: 0.8006
Top100	accuracy: 0.8609
```

**Hybrid dense-sparse retrieval**:

```bash
python -m pyserini.search.hybrid \
  dense  --index wikipedia-dpr-100w.dpr-single-nq \
         --encoded-queries dpr_single_nq-nq-test \
  sparse --index wikipedia-dpr-100w \
  fusion --alpha 1.2 \
  run    --topics dpr-nq-test \
         --output runs/run.encoded.dpr.nq-test.single.bm25.trec \
         --batch-size 512 --threads 16
```

Same as above, replace `--encoded-queries` by `--encoder facebook/dpr-question_encoder-single-nq-base` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-nq-test \
  --index wikipedia-dpr-100w \
  --input runs/run.encoded.dpr.nq-test.single.bm25.trec \
  --output runs/run.encoded.dpr.nq-test.single.bm25.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.encoded.dpr.nq-test.single.bm25.json \
  --topk 20 100
```

And the expected results:

```
Top20	accuracy: 0.8288
Top100	accuracy: 0.8837
```

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-02-12 (commit [`52a1e7`](https://github.com/castorini/pyserini/commit/52a1e7f241b7b833a3ec1d739e629c08417a324c))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2021-04-21 (commit [`2adbf1`](https://github.com/castorini/pyserini/commit/2adbf1bedcfbfbeb3a5fbad71fad95feaab2b641))
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-06-09 (commit [`5e8b91`](https://github.com/castorini/pyserini/commit/5e8b917dc806486da94a9bf1eb15b24e79c13479))
+ Results reproduced by [@mayankanand007](https://github.com/mayankanand007) on 2021-07-28 (commit [`b2b353`](https://github.com/castorini/pyserini/commit/b2b3538d8d3ec5a8b2638457c16f02a8ced068b7))
+ Results reproduced by [@vivianliu0](https://github.com/vivianliu0) on 2022-01-20 (commit [`67d0a6`](https://github.com/castorini/pyserini/commit/c38c557faaa3b9ededf1e8504dd67a5be67d0a66))
+ Results reproduced by [@manveertamber](https://github.com/manveertamber) on 2022-01-22 (commit [`ef70c6`](https://github.com/castorini/pyserini/commit/ef70c63efd773e87afd9708338827342f4960540))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2022-12-25 (commit [`0c495c`](https://github.com/castorini/pyserini/commit/0c495cf2999dda980eb1f85efa30a4323cef5855))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2023-01-10 (commit [`7dafc4`](https://github.com/castorini/pyserini/commit/7dafc4f918bd44ada3771a5c81692ab19cc2cae9))
+ Results reproduced by [@lintool](https://github.com/lintool) on 2024-10-07 (commit [`3f7609`](https://github.com/castorini/pyserini/commit/3f76099a73820afee12496c0354d52ca6a6175c2))

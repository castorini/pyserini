# Pyserini: GAR-T5 enhanced retrieval for NQ and TriviaQA

This guide provides instructions to reproduce the search results of our GAR-T5 model which takes inspiration from the following paper:
> Mao, Y., He, P., Liu, X., Shen, Y., Gao, J., Han, J., & Chen, W. (2020). [Generation-augmented retrieval for open-domain question answering](https://arxiv.org/abs/2009.08553). arXiv preprint arXiv:2009.08553.

## GAR-T5 enhanced retrieval evaluation
### Method 1: Using prebuilt topics
```bash
python -m pyserini.search \
  --topics <dpr-trivia or nq>-test-gar-t5-<answers, titles, sentences, or all> \
  --index wikipedia-dpr \
  --output runs/gar-t5-run.trec \
  --batch-size 70 \
  --threads 70


python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics <nq-test, nq-dev, dpr-trivia-dev or dpr-trivia-test> \
  --index wikipedia-dpr \
  --input runs/gar-t5-run.trec \
  --output runs/gar-t5-run.json
```

### Method 2: Interacting with Gar-T5 Predictions
**Get the Dataset as tsv**  
With the command below, we download the GAR-T5 predictions and augment the topics ([TriviaQA](https://huggingface.co/datasets/castorini/triviaqa_gar-t5_expansions) and [NaturalQuestion](https://huggingface.co/datasets/castorini/nq_gar-t5_expansions))

```bash
export ANSERINI=<path to anserini>
python scripts/gar/query_augmentation_tsv.py \
  --dataset <nq or trivia> \
  --data_split <validation or test> \
  --output_path <default is augmented_topics.tsv> \
  --sentences <optional> \
  --titles <optional> \
  --answers <optional>
```

Running retrieval

```bash
python -m pyserini.search \
  --topics <path to your topic files> \
  --index wikipedia-dpr \
  --output runs/gar-t5-run.trec \
  --batch-size 70 \
  --threads 70


python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics <nq-test, nq-dev, dpr-trivia-dev or dpr-trivia-test> \
  --index wikipedia-dpr \
  --input runs/gar-t5-run.trec \
  --output runs/gar-t5-run.json
```
  
The rest of the section should be the same for both methods

---
To run fusion RRF, you will need all three (answers, titles, sentences) trec files
```bash
python -m pyserini.fusion \
  --runs <path to answers.trec> <path to sentences.trec> <path to titles.trec> \
  --output <output path fusion.trec>
```

To evaluate the run:
```
python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/gar-t5-run.json \
  --topk 1 5 10 20 50 100 200 300 500 1000
```

This should give you the topk scores as below

### Dev Scores from GAR-T5
|  Dataset | Features |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:--------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    |  answer  | 40.33 | 57.76 | 64.26 | 70.38 | 76.96 |  81.20 |  84.33 |  85.91 |  87.83 |  89.94  |
|    NQ    | sentence | 42.00 | 57.78 | 64.12 | 69.59 | 75.62 |  79.67 |  83.03 |  85.04 |  86.87 |  89.00  |
|    NQ    |   title  | 32.15 | 50.66 | 58.68 | 65.76 | 73.30 |  78.25 |  82.19 |  84.15 |  85.91 |  88.01  |
|    NQ    |  fusion  | 45.44 | 64.89 | 71.82 | 77.16 | 82.55 |  85.34 |  88.00 |  89.15 |  90.13 |  91.74  |
| TriviaQA |  answer  | 55.92 | 70.39 | 74.77 | 78.39 | 82.36 |  84.55 |  86.23 |  87.42 |  88.36 |  89.34  |
| TriviaQA | sentence | 49.17 | 63.30 | 68.42 | 72.57 | 77.55 |  80.67 |  83.33 |  84.93 |  86.22 |  87.78  |
| TriviaQA |   title  | 47.58 | 61.31 | 66.59 | 71.57 | 76.79 |  80.15 |  82.95 |  84.18 |  85.65 |  87.30  |
| TriviaQA |  fusion  | 59.48 | 73.43 | 77.29 | 80.43 | 83.80 |  85.60 |  87.11 |  87.81 |  88.70 |  89.68  |

### Test Scores from GAR-T5
|  Dataset | Features |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:--------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    |  answer  | 40.30 | 57.51 | 64.24 | 70.11 | 77.23 |  81.75 |  85.10 |  86.68 |  88.39 |  90.80  |
|    NQ    | sentence | 40.30 | 57.45 | 64.27 | 69.81 | 77.34 |  81.50 |  85.26 |  86.73 |  88.12 |  90.17  |
|    NQ    |   title  | 32.11 | 51.66 | 59.47 | 66.90 | 74.85 |  79.17 |  82.96 |  84.65 |  86.70 |  88.95  |
|    NQ    |  fusion  | 45.35 | 64.63 | 71.75 | 77.17 | 83.41 |  86.90 |  89.14 |  90.30 |  91.63 |  92.91  |
| TriviaQA |  answer  | 55.89 | 69.57 | 73.96 | 77.95 | 82.14 |  84.76 |  86.86 |  87.66 |  88.60 |  89.56  |
| TriviaQA | sentence | 48.96 | 62.68 | 68.05 | 72.47 | 77.51 |  80.84 |  83.54 |  85.01 |  86.23 |  87.93  |
| TriviaQA |   title  | 47.70 | 61.28 | 66.37 | 71.24 | 76.59 |  80.04 |  82.90 |  84.49 |  85.96 |  87.64  |
| TriviaQA |  fusion  | 59.00 | 72.82 | 76.93 | 80.66 | 84.10 |  85.95 |  87.39 |  88.15 |  89.07 |  90.06  |

## Hybrid sparse-dense retrieval with DKRR

To run hybrid sparse-dense retrieval with GAR-T5 and [DKRR](https://github.com/castorini/pyserini/blob/master/docs/experiments-dkrr.md):
```
python -m pyserini.fusion \
  --runs runs/gar-t5-run-fusion.trec runs/run.dpr-dkrr.trec \
  --output runs/run.dkrr.gar.hybrid.trec

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics  <nq-test, nq-dev, dpr-trivia-dev or dpr-trivia-test> \
  --index wikipedia-dpr \
  --input runs/run.dkrr.gar.hybrid.trec \
  --output runs/run.dkrr.gar.hybrid.json

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.dkrr.gar.hybrid.json \
  --topk 1 5 10 20 50 100 200 300 500 1000
```

The scores for this hybrid retrieval are as follows

### Dev Scores
|  Dataset |      Features      |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:------------------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    | hybrid (with DKRR) | 53.36 | 73.66 | 79.92 | 84.46 | 88.24 |  90.22 |  91.42 |  92.10 |  92.65 |  93.26  |
| TriviaQA | hybrid (with DKRR) | 65.81 | 79.40 | 82.34 | 84.69 | 86.87 |  88.05 |  88.99 |  89.52 |  90.05 |  90.61  |

### Test Scores
|  Dataset |      Features      |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:------------------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    | hybrid (with DKRR) | 53.07 | 74.60 | 80.25 | 84.90 | 88.89 |  90.86 |  91.99 |  92.66 |  93.35 |  94.18  |
| TriviaQA | hybrid (with DKRR) | 64.71 | 78.62 | 82.55 | 85.01 | 87.20 |  88.41 |  89.36 |  89.85 |  90.29 |  90.83  |

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@manveertamber](https://github.com/manveertamber) on 2022-05-04 (commit [`1facc72`](https://github.com/castorini/pyserini/commit/1facc72b3c8313149c763b76502f43352efaf974)) 
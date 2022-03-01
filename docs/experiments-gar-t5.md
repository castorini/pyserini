# Pyserini: GAR-T5 enhanced retrieval for NQ and TriviaQA

This guide provides instructions to reproduce the search results of our GAR-T5 model which takes inspiration from the following paper:
> Mao, Y., He, P., Liu, X., Shen, Y., Gao, J., Han, J., & Chen, W. (2020). [Generation-augmented retrieval for open-domain question answering](https://arxiv.org/abs/2009.08553). arXiv preprint arXiv:2009.08553.

We first need to download the test dataset for evaluation. For both NQ and TriviaQA, there are three types of query generation targets, answer, title and sentence.

## Get the Dataset as tsv
Download the dataset from HuggingFace and use script to process it to a .tsv file 
```bash
export ANSERINI=<path to anserini>

python scripts/gar/query_augmentation_tsv.py --dataset <nq or trivia> --data_split <validation or test> --output_path <default is augmented_topics.tsv> --sentences <optional> --titles <optional> --answers <optional>
```

## Evaluation
To evaluate the augmented queries, we need to concatenate and convert them into .tsv format for us to run BM25-search on Pyserini, which is then converted to .json format as required for evaluation.

Without specifying the output path, the default output will be an `augmented_topics.tsv` file in the working directory.

Once we have the tsv file, we can proceed to run search and evaluation

```bash
python -m pyserini.search --topics augmented_topics.tsv --index wikipedia-dpr --output runs/gar-bart-run.trec --batch-size 70 --threads 70

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics <nq-test or dpr-trivia-test> --index wikipedia-dpr --input runs/gar-bart-run.trec --output runs/gar-bart-run.json
```

To run fusion RRF, you will need all three (answers, titles, sentences) trec files
```bash
python -m $ANSERINI/src/main/python/fusion.py --runs <path to answers.trec> <path to sentences.trec> <path to titles.trec> --out <output path>
```

To evaluate the run:
```
python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/gar-bart-run.json --topk 1 5 10 20 50 100 200 300 500 1000
```

This should give you the topk scores as you wanted


### Dev Scores from Gar-T5
|  Dataset | Features |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:--------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    |  answer  | 40.33 | 57.76 | 64.26 | 70.38 | 76.96 |  81.20 |  84.33 |  85.91 |  87.83 |  89.94  |
|    NQ    | sentence | 42.00 | 57.78 | 64.12 | 69.59 | 75.62 |  79.67 |  83.03 |  85.04 |  86.87 |  89.00  |
|    NQ    |   title  | 32.15 | 50.66 | 58.68 | 65.76 | 73.30 |  78.25 |  82.19 |  84.45 |  85.91 |  88.01  |
|    NQ    |  fusion  | 45.44 | 64.89 | 71.82 | 77.16 | 82.55 |  85.34 |  88.00 |  89.15 |  90.13 |  91.74  |
| TriviaQA |  answer  | 55.92 | 70.39 | 74.77 | 78.39 | 82.36 |  84.55 |  86.23 |  87.42 |  88.36 |  89.34  |
| TriviaQA | sentence | 49.17 | 63.30 | 68.42 | 72.57 | 77.55 |  80.67 |  83.33 |  84.93 |  86.22 |  87.78  |
| TriviaQA |   title  | 47.58 | 61.31 | 66.59 | 71.57 | 76.79 |  80.15 |  82.95 |  84.18 |  85.65 |  87.30  |
| TriviaQA |  fusion  | 59.48 | 73.43 | 77.29 | 80.43 | 83.80 |  85.60 |  87.11 |  87.81 |  88.70 |  89.68  |

### Test Scores from Gar-T5
|  Dataset | Features |  Top1 |  Top5 | Top10 | Top20 | Top50 | Top100 | Top200 | Top300 | Top500 | Top1000 |
|:--------:|:--------:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:------:|:------:|:------:|:-------:|
|    NQ    |  answer  | 40.30 | 57.51 | 64.24 | 70.11 | 77.23 |  81.75 |  85.10 |  85.79 |  88.39 |  90.80  |
|    NQ    | sentence | 40.30 | 57.45 | 64.27 | 69.81 | 77.34 |  81.50 |  85.26 |  85.76 |  88.12 |  90.17  |
|    NQ    |   title  | 32.11 | 51.66 | 59.47 | 66.90 | 74.85 |  79.17 |  82.96 |  84.96 |  86.70 |  88.95  |
|    NQ    |  fusion  | 45.35 | 64.63 | 71.75 | 77.17 | 83.41 |  86.90 |  89.14 |  89.67 |  91.63 |  92.91  |
| TriviaQA |  answer  | 55.89 | 69.57 | 73.96 | 77.95 | 82.14 |  84.76 |  86.86 |  86.97 |  88.60 |  89.56  |
| TriviaQA | sentence | 48.96 | 62.68 | 68.05 | 72.47 | 77.51 |  80.84 |  83.54 |  84.47 |  86.23 |  87.93  |
| TriviaQA |   title  | 47.70 | 61.28 | 66.37 | 71.24 | 76.59 |  80.04 |  82.90 |  84.51 |  85.96 |  87.64  |
| TriviaQA |  fusion  | 59.00 | 72.82 | 76.93 | 80.66 | 84.10 |  85.95 |  87.39 |  87.62 |  89.07 |  90.06  |

## Reproduction Log[*](reproducibility.md)

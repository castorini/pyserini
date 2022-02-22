# Pyserini: Gar-BART for NQ and TriviaQA query expansions

This guide provides instructions to reproduce the GAR-T5 model described in the following paper:
> Mao, Y., He, P., Liu, X., Shen, Y., Gao, J., Han, J., & Chen, W. (2020). [Generation-augmented retrieval for open-domain question answering](https://arxiv.org/abs/2009.08553). arXiv preprint arXiv:2009.08553.

We first need to download the test dataset for evaluation. For both NQ and TriviaQA, there are three types of query generation targets, answer, title and sentence.

## Get the Dataset as tsv
Download the dataset from HuggingFace and use script to process it to a .tsv file 
```bash
python scripts/gar/query_augmentation_tsv.py --dataset <nq or trivia> --data_path <query datapath> --data_split <dev or test> --output_path <default is augmented_topics.tsv> --sentences <optional> --titles <optional> --answers <optional>
```

## Evaluation
To evaluate the augmented queries, we need to concatenate and convert them into .tsv format for Pyserini to convert to .trec and evaluate based on the generated .json file

without specifying the output path, the default output will be augmented_topics.tsv in the current folder

once we have the tsv file, we can proceed to search and evaluation

```bash
python -m pyserini.search --topics augmented_topics.tsv --index wikipedia-dpr --output runs/gar-bart-run.trec --batch-size 70 --threads 70

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics <nq-test or dpr-trivia-test> --index wikipedia-dpr --input runs/gar-bart-run.trec --output runs/gar-bart-run.json
```

To evaluate the run:
```
python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/gar-bart-run.json --topk 1 5 10 20 50 100 200 300 500 1000
```

This should give you the topk scores as you wanted
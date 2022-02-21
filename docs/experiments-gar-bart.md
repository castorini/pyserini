# Pyserini: Gar-BART for NQ and TriviaQA query expansions

This guide provides instructions to reproduce the GAR-BART model described in the following paper:
> Mao, Y., He, P., Liu, X., Shen, Y., Gao, J., Han, J., & Chen, W. (2020). [Generation-augmented retrieval for open-domain question answering](https://arxiv.org/abs/2009.08553). arXiv preprint arXiv:2009.08553.

For both NQ and TriviaQA, there are three types of query generation targets, answer, title and sentence. 


## Query Expansion
### Answer Generation

```bash
PT_DATA_DIR=<nq data root folder> PT_OUTPUT_DIR='answer' GEN_TARGET='answer' GEN_DATASET=<'nq' or 'trivia'> python test_generator.py --input_path nq-data/nq-answer/test.source.full --output_path output_path/ --model_ckpt <best checkpoint for answer>
```

### Title Generation

```bash
PT_DATA_DIR=<nq data root folder> PT_OUTPUT_DIR='title' GEN_TARGET='title' GEN_DATASET=<'nq' or 'trivia'> python test_generator.py --input_path nq-data/nq-title/test.source.full --output_path output_path/ --model_ckpt <best checkpoint for title>
```

### Sentence Generation


```bash
PT_DATA_DIR=<nq data root folder> PT_OUTPUT_DIR='sentence' GEN_TARGET='sentence' GEN_DATASET=<'nq' or 'trivia'> python test_generator.py --input_path nq-data/nq-answer/test.source.full --output_path output_path/ --model_ckpt <best checkpoint for sentence>
```

## Evaluation
To evaluate the augmented queries, we need to concatenate and convert them into .tsv format for Pyserini to convert to .trec and evaluate based on the generated .json file
  
  Todo that:

```bash
python to_tsv.py --query_path <path to the query file> --answer_path <optional>  --title_path <optional> --sentence_path <optional>
```

without specifying the output path, the default output will be out.tsv in the current folder

once we have the tsv file, we can proceed to search and evaluation

```
python -m pyserini.search --topics out.tsv --index wikipedia-dpr --output runs/gar-bart-run.trec --batch-size 70 --threads 70

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics <topic> --index wikipedia-dpr --input runs/gar-bart-run.trec --output runs/gar-bart-run.json
```

To evaluate the run:
```
python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/gar-bart-run.json --topk 1 5 10 20 50 100 200 300 500 1000
```

This should give you the topk scores as you wanted


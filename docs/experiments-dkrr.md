# Pyserini: Reproducing DKRR Results

DKRR (Distilling knowledge from reader to retriever) is a technique to learn retriever models described in the following paper:
> Izacard, G., & Grave, E. (2020). Distilling knowledge from reader to retriever for question answering. arXiv preprint arXiv:2012.04584.

We have incorporated this work into Pyserini. In particular, we have taken the pretrained nq_retriever and tqa_retriever models from the [DKRR repo](https://github.com/facebookresearch/FiD), and used them to index English Wikipedia to then allow for use for dense retrieval in Pyserini.

This guide provides instructions to reproduce our results.

## DKRR Retrieval on Natural Questions (NQ) and TriviaQA (TQA)

Running DKRR retrieval (here we are performing on-the-fly query encoding):

```bash
nohup python -m pyserini.dsearch \
    --topics nq-test \
    --index wikipedia-dpr-dkrr-nq \
    --encoder castorini/dkrr-dpr-nq-retriever \
    --output runs/nq.dkrr.ans.test.trec \
    --query-prefix question: \
    --batch-size 72 \
    --threads 72 &> logs/log.nq-test-dkrr

nohup python -m pyserini.dsearch \
    --topics dpr-trivia-test \
    --index wikipedia-dpr-dkrr-tqa \
    --encoder castorini/dkrr-dpr-tqa-retriever \
    --output runs/dpr-trivia.dkrr.ans.test.trec \
    --query-prefix question: \
    --batch-size 72 \
    --threads 72 &> logs/log.dpr-trivia-test-dkrr
```

To evaluate, convert the TREC output format to DPR's json format:

```bash
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
    --topics nq-test \
    --index wikipedia-dpr \
    --input runs/nq.dkrr.ans.test.trec \
    --output runs/nq.dkrr.ans.test.json

python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
    --topics dpr-trivia-test \
    --index wikipedia-dpr \
    --input runs/dpr-trivia.dkrr.ans.test.trec \
    --output runs/dpr-trivia.dkrr.ans.test.json
```

Evaluating on NQ:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
    --retrieval runs/nq.dkrr.ans.test.json \
    --topk 5 20 100 500 1000
```

After rounding the results, you should see:

| Top-5     | Top-20   | Top-100   | Top-500   | Top-1000  |
|----------:|---------:|----------:|----------:|----------:|
| 73.80     | 84.27    | 89.34     | 92.24     | 93.43     |

Evaluating on TriviaQA:

```bash
python -m pyserini.eval.evaluate_dpr_retrieval \
    --retrieval runs/dpr-trivia.dkrr.ans.test.json \
    --topk 5 20 100 500 1000
```


After rounding the results, you should see:

| Top-5     | Top-20   | Top-100   | Top-500   | Top-1000  |
|----------:|---------:|----------:|----------:|----------:|
| 77.23     | 83.74    | 87.78     | 89.87     | 90.63     |

## Reproduction Log[*](reproducibility.md)

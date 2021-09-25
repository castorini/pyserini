# Pyserini: Reproducing ANCE Results

This guide provides instructions to reproduce the Vector PRF in the following work:

> Hang Li, Ahmed Mourad, Shengyao Zhuang, Bevan Koopman, Guido Zuccon. [Pseudo Relevance Feedback with Deep Language Models and Dense Retrievers: Successes and Pitfalls](https://arxiv.org/pdf/2108.11044.pdf)

Starting with v0.12.0, you can reproduce these results directly from the [Pyserini PyPI package](https://pypi.org/project/pyserini/).
Since dense retrieval depends on neural networks, Pyserini requires a more complex set of dependencies to use this feature.
See [package installation notes](../README.md#package-installation) for more details.

Note that we have observed minor differences in scores between different computing environments (e.g., Linux vs. macOS).
However, the differences usually appear in the fifth digit after the decimal point, and do not appear to be a cause for concern from a reproducibility perspective.
Thus, while the scoring script provides results to much higher precision, we have intentionally rounded to four digits after the decimal point.

## TREC DL 2019

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**TCT-ColBERT V1 + Vector PRF** with Average approach:

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:

**TCT-ColBERT V2 + Vector PRF** with Average approach:

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:

## TREC DL 2020

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**TCT-ColBERT V1 + Vector PRF** with Average approach:

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:

**TCT-ColBERT V2 + Vector PRF** with Average approach:

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:

## MS MARCO Passage V1

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**TCT-ColBERT V1 + Vector PRF** with Average approach:

**TCT-ColBERT V1 + Vector PRF** with Rocchio approach:

**TCT-ColBERT V2 + Vector PRF** with Average approach:

**TCT-ColBERT V2 + Vector PRF** with Rocchio approach:

## Natural Questions (NQ)

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**DPR-Multi + Vector PRF** with Average approach:

**DPR-Multi + Vector PRF** with Rocchio approach:

**DPR-Single + Vector PRF** with Average approach:

**DPR-Single + Vector PRF** with Rocchio approach:

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-ance-multi-bf \
                             --encoded-queries ance_multi-nq-test \
                             --output runs/run.ance.nq-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` with `--encoder castorini/ance-dpr-question-multi` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.ance.nq-test.multi.bf.trec \
                                                                --output runs/run.ance.nq-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.ance.nq-test.multi.bf.json --topk 20 100
Top20	accuracy: 0.8224
Top100	accuracy: 0.8787
```

## Trivia QA

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**DPR-Multi + Vector PRF** with Average approach:

**DPR-Multi + Vector PRF** with Rocchio approach:

**ANCE retrieval** with brute-force index:

```bash
$ python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-ance-multi-bf \
                             --encoded-queries ance_multi-trivia-test \
                             --output runs/run.ance.trivia-test.multi.bf.trec \
                             --batch-size 36 --threads 12
```

Same as above, replace `--encoded-queries` with `--encoder castorini/ance-dpr-question-multi` for on-the-fly query encoding.

To evaluate, first convert the TREC output format to DPR's `json` format:

```bash
$ python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                                --index wikipedia-dpr \
                                                                --input runs/run.ance.trivia-test.multi.bf.trec \
                                                                --output runs/run.ance.trivia-test.multi.bf.json

$ python -m pyserini.eval.evaluate_dpr_retrieval --retrieval runs/run.ance.trivia-test.multi.bf.json --topk 20 100
Top20	accuracy: 0.8010
Top100	accuracy: 0.8522
```

## WebQuestions (WQ)

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**DPR-Multi + Vector PRF** with Average approach:

**DPR-Multi + Vector PRF** with Rocchio approach:

## CuratedTREC

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**DPR-Multi + Vector PRF** with Average approach:

**DPR-Multi + Vector PRF** with Rocchio approach:

## SQuAD

**ANCE + Vector PRF** with Average approach:

**ANCE + Vector PRF** with Rocchio approach:

**DPR-Multi + Vector PRF** with Average approach:

**DPR-Multi + Vector PRF** with Rocchio approach:

## Reproduction Log[*](reproducibility.md)

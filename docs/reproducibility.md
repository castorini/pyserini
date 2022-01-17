# Reproducibility: General Notes
 
## Reproducibility vs. Replicability

The terms "reproducibility" and "replicability" are often used in imprecise and confusing ways.
In the context of Pyserini, we use these terms as defined by ACM's [Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current) Policy.
Note that the policy itself is confusing in that a previous version of the policy had the meaning of "reproducibility" and "replicability" swapped.

To be precise, per the policy:

+ Repeatability = same team, same experimental setup
+ Reproducibility = different team, same experimental setup
+ Replicability = different team, different experimental setup

In this context, if you are able to run our code and get the same results, then you have successfully _reproduced_ our results.
For the most part, replicability is not applicable in the context of Pyserini, because the term implies a different (i.e., non-Pyserini) implementation.

At the bottom of many pages you'll find a "Reproduction Log", which keeps track of users who have successfully reproduced the results reported on that page.
Note that we stretch the meaning of "same team" a bit in these logs: we still consider it a successful reproduction if another member of our research group is able to obtain the same results,
as long as the person was not the primary author of the code in question.

## Non-Determinism of Neural Inference

In our implementations of sparse learned retrieval models (i.e., models that use transformers to assign term weights to bag-of-words representations), we distinguish between two modes of retrieval:

1. Pre-tokenized queries with pre-computed weights. The query encoder is not used at retrieval time.
2. "On-the-fly" query encoding, which means we run inference on the queries using the query encoder at retrieval time.

In the first case, the results should be deterministic (i.e., scores should be exactly reproducible).

In the second case, for broader access, we perform inference on the CPU by default.
This additional neural inference increases query latency, and furthermore may introduce minor differences in the final scores due to a number of issues, for example, GPU vs. CPU inference.
We have additionally found that the operating system makes a difference, e.g., Linux vs. macOS, even if inference is performed on the CPU in both cases.
Usually, these differences are in the third decimal point in retrieval metrics.
This roughly characterizes the limits of reproducibility for this class of retrieval models.

For learned sparse retrieval models, inference is performed on documents and the weights are quantized as part of the corpus preparation process.
This process also introduces some amount of non-determinism, for example, depending, for example, on which GPU we use.
This means that even if the model is exactly the same, if we ran inference on the documents again, the weights might be slightly different.
And if we index these new representations and performed retrieval experiments, we're likely to get slightly different results.
Once again, these differences characterize the limits of reproducibility.
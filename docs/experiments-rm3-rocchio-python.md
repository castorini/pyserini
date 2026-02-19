# Pyserini: Performance Comparison of Python versus Java  RM3 and Rocchio Implementations  

We fully re-implmented the RM3 and Rocchio implementations from Anserini in Python. Below is a comparison of the performance of RM3 and Rocchio in Python versus in Java. 

For example, to run RM3 in Python over TREC DL21, 

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage \
  --topics <topics_name> \
  --output run.msmarco-v2-passage.bm25-rm3-default.<dataset_name>.txt \
  --bm25 --rm3-py
```

Rocchio follows similar style:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage \
  --topics <topics_name> \
  --output run.msmarco-v2-passage.bm25-rm3-default.<dataset_name>.txt \
  --bm25 --rocchio-py
```

## Performance Comparison

For this experiment, these were the computer specs:

-  OS: Windows 11 (x64), WSL
- Machine: Intel NUC11PHi7
- CPU: 11th Gen Intel Core i7
- RAM: 16 GB

### Effectiveness Comparison: Python versus Java

| Implementation | RM3 MAP | RM3 nDCG@10 | RM3 Recall@1000 | Rocchio MAP | Rocchio nDCG@10 | Rocchio Recall@1000 |
|---------------|---------|-------------|-----------------|-------------|------------------|----------------------|
| **TREC DL19** |         |             |                 |             |                  |                      |
| Python        | 0.3420  | 0.5216      | 0.8136          | 0.3476      | 0.5275           | 0.8007               |
| Java          | 0.3416  | 0.5216      | 0.8136          | 0.3474      | 0.5275           | 0.8007               |
| **TREC DL20** |         |             |                 |             |                  |                      |
| Python        | 0.3010  | 0.4896      | 0.8236          | 0.3118      | 0.4887           | 0.8156               |
| Java          | 0.3006  | 0.4896      | 0.8236          | 0.3115      | 0.4910           | 0.8156               |
| **TREC DL21** |         |             |                 |             |                  |                      |
| Python        | 0.2115  | 0.4454      | 0.6618          | 0.2153      | 0.4550           | 0.6709               |
| Java          | 0.2115  | 0.4455      | 0.6616          | 0.2152      | 0.4546           | 0.6709               |
| **TREC DL22** |         |             |                 |             |                  |                      |
| Python        | 0.0446  | 0.2683      | 0.3559          | 0.0478      | 0.2755           | 0.3637               |
| Java          | 0.0446  | 0.2686      | 0.3559          | 0.0475      | 0.2743           | 0.3639               |
| **TREC DL23** |         |             |                 |             |                  |                      |
| Python        | 0.0968  | 0.2602      | 0.4745          | 0.0968      | 0.2626           | 0.4788               |
| Java          | 0.0969  | 0.2602      | 0.4748          | 0.0970      | 0.2653           | 0.4810               |



### Latency Differences: Python versus Java

| Implementation | RM3     | Rocchio |
|---------------|---------|----------|
| **TREC DL19** |         |          |
| Python        | 3.67    | 4.14     |
| Java          | 2.30    | 3.15     |
| Diff          | 1.37    | 0.99     |
| **TREC DL20** |         |          |
| Python        | 13.81   | 19.51    |
| Java          | 11.67   | 15.84    |
| Diff          | 2.14    | 3.67     |
| **TREC DL21** |         |          |
| Python        | 2338.80 | 4637.96  |
| Java          | 3293.97 | 4735.69  |
| Diff          | -955.17 | -97.73   |
| **TREC DL22** |         |          |
| Python        | 1282.89 | 1944.76  |
| Java          | 1503.62 | 2042.32  |
| Diff          | -220.73 | -97.56   |
| **TREC DL23** |         |          |
| Python        | 2112.62 | 4002.54  |
| Java          | 2758.77 | 3445.50  |
| Diff          | -646.15 | 557.04   |



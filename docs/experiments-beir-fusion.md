# Pyserini: Fusion on the BEIR Datasets

This page documents the results of running fusion retrieval on the BEIR datasets using Pyserini with BM25 and BGE indexes.

Currently, Pyserini provides support for the following fusion methods:

### **RRF** = Reciprocal Rank Fusion
Rank-based fusion using reciprocal ranks: `RRF_score(d) = Σ(1 / (k + rank_i(d)))` where `k=60`.  
### **Average** = Averaging scores on a list of runs
Simple arithmetic mean: `Average_score(d) = (1/n) × Σ(score_i(d))`
### **Interpolation** = Weighted sum of two runs
Weighted combination: `Interpolation_score(d) = α × score_1(d) + (1-α) × score_2(d)` where `α=0.5`

### **Normalize** = Average of scores normalized between [0, 1] (optimized implementation)
Min-max normalization then averaging: `Normalized_score_i(d) = (score_i(d) - min_i) / (max_i - min_i)`

## Results

For all experiments recorded here, the values k = 1000, depth = 1000, rrf_k = 60, and alpha = 0.5 were used.

The runs of two models were fused:
+ **BM25**: Sparse retrieval using flat BM25 index
+ **BGE**: Dense retrieval using bge-base-en-v1.5 with dense flat index

Since there were only two runs fused, the average and interpolation methods produced the same results.

Three metrics were used for evaluation: nDCG@10, R@100, and R@1000.

The table below reports the effectiveness of the methods with the nDCG@10 metric and the base runs fused for reference:

| Corpus                      | RRF    | Average | Interpolation | Normalize | BM25   | BGE    |
|-----------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `trec-covid`                | 0.8041 | 0.6567  | 0.6567        | 0.7956    | 0.5947 | 0.7815 |
| `bioasq`                    | 0.5278 | 0.5315  | 0.5315        | 0.5442    | 0.5225 | 0.4148 |
| `nfcorpus`                  | 0.3725 | 0.3414  | 0.3414        | 0.3789    | 0.3218 | 0.3735 |
| `nq`                        | 0.4831 | 0.3241  | 0.3241        | 0.5184    | 0.3055 | 0.5415 |
| `hotpotqa`                  | 0.7389 | 0.6497  | 0.6497        | 0.7658    | 0.6330 | 0.7259 |
| `fiqa`                      | 0.3671 | 0.2470  | 0.2470        | 0.3942    | 0.2361 | 0.4065 |
| `signal1m`                  | 0.3533 | 0.3463  | 0.3463        | 0.3622    | 0.3304 | 0.2886 |
| `trec-news`                 | 0.4855 | 0.4162  | 0.4162        | 0.5008    | 0.3952 | 0.4424 |
| `robust04`                  | 0.5070 | 0.4327  | 0.4327        | 0.5128    | 0.4070 | 0.4435 |
| `arguana`                   | 0.5586 | 0.3986  | 0.3986        | 0.5694    | 0.3970 | 0.6228 |
| `webis-touche2020`          | 0.3771 | 0.4509  | 0.4509        | 0.3755    | 0.4422 | 0.2571 |
| `cqadupstack-android`       | 0.4652 | 0.3872  | 0.3872        | 0.4868    | 0.3801 | 0.5076 |
| `cqadupstack-english`       | 0.4461 | 0.3601  | 0.3601        | 0.4678    | 0.3453 | 0.4857 |
| `cqadupstack-gaming`        | 0.5615 | 0.4886  | 0.4886        | 0.5818    | 0.4822 | 0.5967 |
| `cqadupstack-gis`           | 0.3679 | 0.2948  | 0.2948        | 0.3937    | 0.2901 | 0.4131 |
| `cqadupstack-mathematica`   | 0.2751 | 0.2084  | 0.2084        | 0.2951    | 0.2015 | 0.3163 |
| `cqadupstack-physics`       | 0.4143 | 0.3283  | 0.3283        | 0.4375    | 0.3214 | 0.4724 |
| `cqadupstack-programmers`   | 0.3715 | 0.2891  | 0.2891        | 0.4005    | 0.2802 | 0.4238 |
| `cqadupstack-stats`         | 0.3414 | 0.2796  | 0.2796        | 0.3534    | 0.2711 | 0.3728 |
| `cqadupstack-tex`           | 0.2931 | 0.2332  | 0.2332        | 0.3090    | 0.2244 | 0.3115 |
| `cqadupstack-unix`          | 0.3597 | 0.2829  | 0.2829        | 0.3853    | 0.2749 | 0.4220 |
| `cqadupstack-webmasters`    | 0.3711 | 0.3130  | 0.3130        | 0.3857    | 0.3059 | 0.4072 |
| `cqadupstack-wordpress`     | 0.3353 | 0.2625  | 0.2625        | 0.3546    | 0.2483 | 0.3547 |
| `quora`                     | 0.8682 | 0.8008  | 0.8008        | 0.8859    | 0.7886 | 0.8876 |
| `dbpedia-entity`            | 0.4190 | 0.3365  | 0.3365        | 0.4374    | 0.3180 | 0.4073 |
| `scidocs`                   | 0.1948 | 0.1527  | 0.1527        | 0.2019    | 0.1490 | 0.2172 |
| `fever`                     | 0.8108 | 0.6688  | 0.6688        | 0.8582    | 0.6513 | 0.8629 |
| `climate-fever`             | 0.2812 | 0.1742  | 0.1742        | 0.2946    | 0.1651 | 0.3117 |
| `scifact`                   | 0.7420 | 0.6806  | 0.6806        | 0.7472    | 0.6789 | 0.7408 |


The table below reports the effectiveness of the methods with the R@100 metric:

| Corpus                      | RRF    | Average | Interpolation | Normalize | BM25   | BGE    |
|-----------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `trec-covid`                | 0.1467 | 0.1255  | 0.1255        | 0.1518    | 0.1091 | 0.1406 |
| `bioasq`                    | 0.8128 | 0.7869  | 0.7869        | 0.8143    | 0.7687 | 0.6316 |
| `nfcorpus`                  | 0.3391 | 0.3003  | 0.3003        | 0.3382    | 0.2457 | 0.3368 |
| `nq`                        | 0.9415 | 0.7922  | 0.7922        | 0.9372    | 0.7513 | 0.9414 |
| `hotpotqa`                  | 0.8917 | 0.8184  | 0.8184        | 0.8919    | 0.7957 | 0.8726 |
| `fiqa`                      | 0.7160 | 0.5639  | 0.5639        | 0.7041    | 0.5395 | 0.7415 |
| `signal1m`                  | 0.4008 | 0.4077  | 0.4077        | 0.3947    | 0.3703 | 0.3112 |
| `trec-news`                 | 0.5547 | 0.4751  | 0.4751        | 0.5560    | 0.4469 | 0.4992 |
| `robust04`                  | 0.4465 | 0.3963  | 0.3963        | 0.4434    | 0.3746 | 0.3510 |
| `arguana`                   | 0.9879 | 0.9331  | 0.9331        | 0.9879    | 0.9324 | 0.9716 |
| `webis-touche2020`          | 0.6169 | 0.5878  | 0.5878        | 0.6039    | 0.5822 | 0.4867 |
| `cqadupstack-android`       | 0.8203 | 0.7076  | 0.7076        | 0.8155    | 0.6829 | 0.8454 |
| `cqadupstack-english`       | 0.7523 | 0.6022  | 0.6022        | 0.7436    | 0.5757 | 0.7586 |
| `cqadupstack-gaming`        | 0.8933 | 0.7956  | 0.7956        | 0.8906    | 0.7651 | 0.9036 |
| `cqadupstack-gis`           | 0.7621 | 0.6487  | 0.6487        | 0.7635    | 0.6119 | 0.7682 |
| `cqadupstack-mathematica`   | 0.6666 | 0.5173  | 0.5173        | 0.6725    | 0.4877 | 0.6922 |
| `cqadupstack-physics`       | 0.7921 | 0.6549  | 0.6549        | 0.7859    | 0.6326 | 0.8078 |
| `cqadupstack-programmers`   | 0.7530 | 0.5993  | 0.5993        | 0.7593    | 0.5588 | 0.7856 |
| `cqadupstack-stats`         | 0.6616 | 0.5650  | 0.5650        | 0.6644    | 0.5338 | 0.6719 |
| `cqadupstack-tex`           | 0.6332 | 0.5004  | 0.5004        | 0.6298    | 0.4686 | 0.6489 |
| `cqadupstack-unix`          | 0.7481 | 0.5798  | 0.5798        | 0.7363    | 0.5417 | 0.7797 |
| `cqadupstack-webmasters`    | 0.7543 | 0.6127  | 0.6127        | 0.7371    | 0.5820 | 0.7774 |
| `cqadupstack-wordpress`     | 0.6869 | 0.5488  | 0.5488        | 0.6794    | 0.5152 | 0.7047 |
| `quora`                     | 0.9966 | 0.9793  | 0.9793        | 0.9958    | 0.9733 | 0.9968 |
| `dbpedia-entity`            | 0.5985 | 0.5019  | 0.5019        | 0.5951    | 0.4682 | 0.5298 |
| `scidocs`                   | 0.4751 | 0.3735  | 0.3735        | 0.4830    | 0.3477 | 0.4959 |
| `fever`                     | 0.9731 | 0.9317  | 0.9317        | 0.9712    | 0.9185 | 0.9719 |
| `climate-fever`             | 0.6288 | 0.4590  | 0.4590        | 0.6324    | 0.4249 | 0.6354 |
| `scifact`                   | 0.9767 | 0.9327  | 0.9327        | 0.9700    | 0.9253 | 0.9667 |


The table below reports the effectiveness of the methods with the R@1000 metric:

| Corpus                      | RRF    | Average | Interpolation | Normalize | BM25   | BGE    |
|-----------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `trec-covid`                | 0.5029 | 0.3955  | 0.3955        | 0.5010    | 0.3955 | 0.4765 |
| `bioasq`                    | 0.9281 | 0.9030  | 0.9030        | 0.9281    | 0.9030 | 0.8062 |
| `nfcorpus`                  | 0.6540 | 0.6422  | 0.6422        | 0.6563    | 0.3704 | 0.6622 |
| `nq`                        | 0.9874 | 0.8958  | 0.8958        | 0.9870    | 0.8958 | 0.9859 |
| `hotpotqa`                  | 0.9473 | 0.8820  | 0.8820        | 0.9477    | 0.8820 | 0.9423 |
| `fiqa`                      | 0.8979 | 0.7402  | 0.7402        | 0.9011    | 0.7393 | 0.9083 |
| `signal1m`                  | 0.6139 | 0.5642  | 0.5642        | 0.6097    | 0.5642 | 0.5331 |
| `trec-news`                 | 0.8169 | 0.7051  | 0.7051        | 0.8158    | 0.7051 | 0.7875 |
| `robust04`                  | 0.7218 | 0.6345  | 0.6345        | 0.7200    | 0.6345 | 0.5961 |
| `arguana`                   | 0.9964 | 0.9893  | 0.9893        | 0.9964    | 0.9872 | 0.9929 |
| `webis-touche2020`          | 0.8912 | 0.8621  | 0.8621        | 0.8896    | 0.8621 | 0.8298 |
| `cqadupstack-android`       | 0.9537 | 0.8646  | 0.8646        | 0.9550    | 0.8632 | 0.9611 |
| `cqadupstack-english`       | 0.8751 | 0.7394  | 0.7394        | 0.8751    | 0.7323 | 0.8839 |
| `cqadupstack-gaming`        | 0.9661 | 0.8952  | 0.8952        | 0.9641    | 0.8945 | 0.9719 |
| `cqadupstack-gis`           | 0.9054 | 0.8174  | 0.8174        | 0.9064    | 0.8174 | 0.9117 |
| `cqadupstack-mathematica`   | 0.8781 | 0.7298  | 0.7298        | 0.8787    | 0.7221 | 0.8810 |
| `cqadupstack-physics`       | 0.9337 | 0.8375  | 0.8375        | 0.9340    | 0.8340 | 0.9415 |
| `cqadupstack-programmers`   | 0.9272 | 0.7745  | 0.7745        | 0.9275    | 0.7734 | 0.9353 |
| `cqadupstack-stats`         | 0.8363 | 0.7310  | 0.7310        | 0.8336    | 0.7310 | 0.8445 |
| `cqadupstack-tex`           | 0.8430 | 0.6907  | 0.6907        | 0.8430    | 0.6907 | 0.8538 |
| `cqadupstack-unix`          | 0.9097 | 0.7626  | 0.7626        | 0.9132    | 0.7616 | 0.9235 |
| `cqadupstack-webmasters`    | 0.9369 | 0.8088  | 0.8088        | 0.9334    | 0.8066 | 0.9380 |
| `cqadupstack-wordpress`     | 0.8761 | 0.7571  | 0.7571        | 0.8782    | 0.7552 | 0.8861 |
| `quora`                     | 0.9999 | 0.9950  | 0.9950        | 0.9999    | 0.9950 | 0.9999 |
| `dbpedia-entity`            | 0.8096 | 0.6773  | 0.6773        | 0.8089    | 0.6760 | 0.7833 |
| `scidocs`                   | 0.7477 | 0.5652  | 0.5652        | 0.7561    | 0.5638 | 0.7824 |
| `fever`                     | 0.9859 | 0.9591  | 0.9591        | 0.9859    | 0.9589 | 0.9855 |
| `climate-fever`             | 0.8220 | 0.6324  | 0.6324        | 0.8210    | 0.6324 | 0.8306 |
| `scifact`                   | 0.9967 | 0.9800  | 0.9800        | 0.9967    | 0.9767 | 0.9967 |


## Run and Evaluate

```bash
CORPORA=(trec-covid bioasq nfcorpus nq hotpotqa fiqa signal1m trec-news robust04 arguana webis-touche2020 cqadupstack-android cqadupstack-english cqadupstack-gaming cqadupstack-gis cqadupstack-mathematica cqadupstack-physics cqadupstack-programmers cqadupstack-stats cqadupstack-tex cqadupstack-unix cqadupstack-webmasters cqadupstack-wordpress quora dbpedia-entity scidocs fever climate-fever scifact)
for c in "${CORPORA[@]}"
do
    # bm25 search
    python -m pyserini.search.lucene \
        --index beir-v1.0.0-${c}.flat \
        --topics beir-v1.0.0-${c}-test \
        --output runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 \
        --bm25 \
        --remove-query \
        --hits 1000 \
        --threads 16 \
        --batch-size 128

    # bge search using Lucene ONNX
    python -m pyserini.search.lucene \
        --dense \
        --flat \
        --index beir-v1.0.0-${c}.bge-base-en-v1.5.flat \
        --topics beir-v1.0.0-${c}-test \
        --onnx-encoder BgeBaseEn15 \
        --output runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt \
        --hits 1000 \
        --remove-query \
        --threads 16 \
        --batch-size 128

    # rrf fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt \
        --output runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt \
        --method rrf \
        --k 1000 \
        --depth 1000 \
        --rrf.k 60

    # average fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt \
        --output runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt \
        --method average \
        --k 1000 \
        --depth 1000

    # interpolation fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt \
        --output runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt \
        --method interpolation \
        --k 1000 \
        --depth 1000 \
        --alpha 0.5

    # normalize fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt \
        --output runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt \
        --method normalize \
        --k 1000 \
        --depth 1000
done
```
The following snippet will generate the complete set of fusion results that corresponds to the above table:
```bash
CORPORA=(trec-covid bioasq nfcorpus nq hotpotqa fiqa signal1m trec-news robust04 arguana webis-touche2020 cqadupstack-android cqadupstack-english cqadupstack-gaming cqadupstack-gis cqadupstack-mathematica cqadupstack-physics cqadupstack-programmers cqadupstack-stats cqadupstack-tex cqadupstack-unix cqadupstack-webmasters cqadupstack-wordpress quora dbpedia-entity scidocs fever climate-fever scifact)

for c in "${CORPORA[@]}"
do
    echo "Evaluating: $c"
    # BM25
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25

    # BGE Lucene ONNX"
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/run.flat.beir-v1.0.0-${c}.bge-base-en-v1.5.test.bge-flat-onnx-lucene.txt

    # RRF Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt

    # Average Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt

    # Interpolation Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt

    # Normalize Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-lucene.test.txt
done
```


## Reproduction Log

These results can be reproduced using the provided scripts in this repository.


# Pyserini: Fusion on the BEIR Datasets with FAISS

This page documents the results of running fusion retrieval on the BEIR datasets using Pyserini with FAISS dense indexes.

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
+ **BGE-FAISS**: Dense retrieval using bge-base-en-v1.5 with FAISS index

Since there were only two runs fused, the average and interpolation methods produced the same results.

Three metrics were used for evaluation: nDCG@10, R@100, and R@1000.



The table below reports the effectiveness of the methods with the **nDCG@10** metric and the base runs fused for reference:

| Corpus                    |    RRF | Average | Interpolation | Normalize |   BM25 |    BGE |
|---------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `arguana                  ` | 0.5788 |  0.3994 |        0.3994 |    0.5905 | 0.3970 | 0.6232 |
| `bioasq                   ` | 0.5196 |  0.5337 |        0.5337 |    0.5366 | 0.5225 | 0.3906 |
| `climate-fever            ` | 0.2782 |  0.1739 |        0.1739 |    0.2872 | 0.1651 | 0.2871 |
| `cqadupstack-android      ` | 0.4654 |  0.3907 |        0.3907 |    0.4963 | 0.3801 | 0.5063 |
| `cqadupstack-english      ` | 0.4486 |  0.3635 |        0.3635 |    0.4668 | 0.3453 | 0.4567 |
| `cqadupstack-gaming       ` | 0.5663 |  0.4925 |        0.4925 |    0.5879 | 0.4822 | 0.5853 |
| `cqadupstack-gis          ` | 0.3721 |  0.2990 |        0.2990 |    0.3944 | 0.2901 | 0.4113 |
| `cqadupstack-mathematica  ` | 0.2788 |  0.2098 |        0.2098 |    0.3001 | 0.2015 | 0.3098 |
| `cqadupstack-physics      ` | 0.4173 |  0.3312 |        0.3312 |    0.4414 | 0.3214 | 0.4577 |
| `cqadupstack-programmers  ` | 0.3705 |  0.2924 |        0.2924 |    0.3984 | 0.2802 | 0.4002 |
| `cqadupstack-stats        ` | 0.3381 |  0.2819 |        0.2819 |    0.3542 | 0.2711 | 0.3535 |
| `cqadupstack-tex          ` | 0.2942 |  0.2349 |        0.2349 |    0.3101 | 0.2244 | 0.3036 |
| `cqadupstack-unix         ` | 0.3654 |  0.2869 |        0.2869 |    0.3902 | 0.2749 | 0.4053 |
| `cqadupstack-webmasters   ` | 0.3749 |  0.3134 |        0.3134 |    0.3938 | 0.3059 | 0.3989 |
| `cqadupstack-wordpress    ` | 0.3328 |  0.2637 |        0.2637 |    0.3556 | 0.2483 | 0.3456 |
| `dbpedia-entity           ` | 0.4139 |  0.3398 |        0.3398 |    0.4373 | 0.3180 | 0.4060 |
| `fiqa                     ` | 0.3696 |  0.2505 |        0.2505 |    0.3944 | 0.2361 | 0.3826 |
| `hotpotqa                 ` | 0.7388 |  0.6504 |        0.6504 |    0.7637 | 0.6330 | 0.7002 |
| `nfcorpus                 ` | 0.3759 |  0.3421 |        0.3421 |    0.3795 | 0.3218 | 0.3697 |
| `nq                       ` | 0.4759 |  0.3266 |        0.3266 |    0.5081 | 0.3055 | 0.5025 |
| `quora                    ` | 0.8722 |  0.8058 |        0.8058 |    0.8886 | 0.7886 | 0.8882 |
| `robust04                 ` | 0.5052 |  0.4294 |        0.4294 |    0.5096 | 0.4070 | 0.4226 |
| `scidocs                  ` | 0.2024 |  0.1539 |        0.1539 |    0.2077 | 0.1490 | 0.2200 |
| `scifact                  ` | 0.7483 |  0.6833 |        0.6833 |    0.7556 | 0.6789 | 0.7363 |
| `signal1m                 ` | 0.3489 |  0.3464 |        0.3464 |    0.3549 | 0.3304 | 0.2796 |
| `trec-covid               ` | 0.7989 |  0.6615 |        0.6615 |    0.7846 | 0.5947 | 0.6996 |
| `trec-news                ` | 0.4890 |  0.4175 |        0.4175 |    0.4938 | 0.3952 | 0.4094 |
| `webis-touche2020         ` | 0.3373 |  0.4542 |        0.4542 |    0.3547 | 0.4422 | 0.1899 |


The table below reports the effectiveness of the methods with the **R@100** metric:

| Corpus                    |    RRF | Average | Interpolation | Normalize |   BM25 |    BGE |
|---------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `arguana                  ` | 0.9879 |  0.9339 |        0.9339 |    0.9915 | 0.9324 | 0.9900 |
| `bioasq                   ` | 0.8061 |  0.7855 |        0.7855 |    0.8062 | 0.7687 | 0.6016 |
| `climate-fever            ` | 0.6204 |  0.4558 |        0.4558 |    0.6264 | 0.4249 | 0.6227 |
| `cqadupstack-android      ` | 0.8264 |  0.7105 |        0.7105 |    0.8218 | 0.6829 | 0.8519 |
| `cqadupstack-english      ` | 0.7462 |  0.6046 |        0.6046 |    0.7407 | 0.5757 | 0.7513 |
| `cqadupstack-gaming       ` | 0.8974 |  0.7957 |        0.7957 |    0.8975 | 0.7651 | 0.8907 |
| `cqadupstack-gis          ` | 0.7618 |  0.6516 |        0.6516 |    0.7711 | 0.6119 | 0.7591 |
| `cqadupstack-mathematica  ` | 0.6731 |  0.5184 |        0.5184 |    0.6749 | 0.4877 | 0.6871 |
| `cqadupstack-physics      ` | 0.7983 |  0.6595 |        0.6595 |    0.7912 | 0.6326 | 0.8028 |
| `cqadupstack-programmers  ` | 0.7473 |  0.5995 |        0.5995 |    0.7549 | 0.5588 | 0.7700 |
| `cqadupstack-stats        ` | 0.6661 |  0.5683 |        0.5683 |    0.6687 | 0.5338 | 0.6691 |
| `cqadupstack-tex          ` | 0.6381 |  0.5022 |        0.5022 |    0.6320 | 0.4686 | 0.6443 |
| `cqadupstack-unix         ` | 0.7475 |  0.5787 |        0.5787 |    0.7470 | 0.5417 | 0.7815 |
| `cqadupstack-webmasters   ` | 0.7560 |  0.6131 |        0.6131 |    0.7435 | 0.5820 | 0.7832 |
| `cqadupstack-wordpress    ` | 0.6863 |  0.5488 |        0.5488 |    0.6910 | 0.5152 | 0.7039 |
| `dbpedia-entity           ` | 0.6024 |  0.5011 |        0.5011 |    0.5959 | 0.4682 | 0.5308 |
| `fiqa                     ` | 0.7161 |  0.5644 |        0.5644 |    0.7084 | 0.5395 | 0.7206 |
| `hotpotqa                 ` | 0.8912 |  0.8153 |        0.8153 |    0.8928 | 0.7957 | 0.8671 |
| `nfcorpus                 ` | 0.3312 |  0.3018 |        0.3018 |    0.3333 | 0.2457 | 0.3279 |
| `nq                       ` | 0.9317 |  0.7896 |        0.7896 |    0.9313 | 0.7513 | 0.9218 |
| `quora                    ` | 0.9964 |  0.9804 |        0.9804 |    0.9962 | 0.9733 | 0.9966 |
| `robust04                 ` | 0.4328 |  0.3932 |        0.3932 |    0.4298 | 0.3746 | 0.3167 |
| `scidocs                  ` | 0.4941 |  0.3711 |        0.3711 |    0.5016 | 0.3477 | 0.5178 |
| `scifact                  ` | 0.9733 |  0.9327 |        0.9327 |    0.9767 | 0.9253 | 0.9700 |
| `signal1m                 ` | 0.3868 |  0.3976 |        0.3976 |    0.3783 | 0.3703 | 0.2675 |
| `trec-covid               ` | 0.1479 |  0.1252 |        0.1252 |    0.1508 | 0.1091 | 0.1382 |
| `trec-news                ` | 0.5483 |  0.4694 |        0.4694 |    0.5518 | 0.4469 | 0.4773 |
| `webis-touche2020         ` | 0.6131 |  0.5885 |        0.5885 |    0.5948 | 0.5822 | 0.4362 |


The table below reports the effectiveness of the methods with the **R@1000** metric:

| Corpus                    |    RRF | Average | Interpolation | Normalize |   BM25 |    BGE |
|---------------------------|-------:|--------:|--------------:|----------:|-------:|-------:|
| `arguana                  ` | 0.9964 |  0.9879 |        0.9879 |    0.9964 | 0.9872 | 0.9964 |
| `bioasq                   ` | 0.9237 |  0.9030 |        0.9030 |    0.9243 | 0.9030 | 0.7757 |
| `climate-fever            ` | 0.8118 |  0.6324 |        0.6324 |    0.8121 | 0.6324 | 0.8125 |
| `cqadupstack-android      ` | 0.9578 |  0.8646 |        0.8646 |    0.9568 | 0.8632 | 0.9687 |
| `cqadupstack-english      ` | 0.8684 |  0.7392 |        0.7392 |    0.8662 | 0.7323 | 0.8741 |
| `cqadupstack-gaming       ` | 0.9662 |  0.8945 |        0.8945 |    0.9661 | 0.8945 | 0.9693 |
| `cqadupstack-gis          ` | 0.9116 |  0.8174 |        0.8174 |    0.9115 | 0.8174 | 0.9189 |
| `cqadupstack-mathematica  ` | 0.8740 |  0.7286 |        0.7286 |    0.8780 | 0.7221 | 0.8940 |
| `cqadupstack-physics      ` | 0.9304 |  0.8375 |        0.8375 |    0.9309 | 0.8340 | 0.9429 |
| `cqadupstack-programmers  ` | 0.9283 |  0.7734 |        0.7734 |    0.9289 | 0.7734 | 0.9337 |
| `cqadupstack-stats        ` | 0.8287 |  0.7310 |        0.7310 |    0.8242 | 0.7310 | 0.8460 |
| `cqadupstack-tex          ` | 0.8485 |  0.6907 |        0.6907 |    0.8447 | 0.6907 | 0.8511 |
| `cqadupstack-unix         ` | 0.9122 |  0.7626 |        0.7626 |    0.9145 | 0.7616 | 0.9276 |
| `cqadupstack-webmasters   ` | 0.9319 |  0.8088 |        0.8088 |    0.9339 | 0.8066 | 0.9420 |
| `cqadupstack-wordpress    ` | 0.8789 |  0.7552 |        0.7552 |    0.8743 | 0.7552 | 0.8907 |
| `dbpedia-entity           ` | 0.8128 |  0.6773 |        0.6773 |    0.8128 | 0.6760 | 0.7856 |
| `fiqa                     ` | 0.8892 |  0.7399 |        0.7399 |    0.8902 | 0.7393 | 0.8966 |
| `hotpotqa                 ` | 0.9476 |  0.8820 |        0.8820 |    0.9482 | 0.8820 | 0.9421 |
| `nfcorpus                 ` | 0.6541 |  0.6348 |        0.6348 |    0.6574 | 0.3704 | 0.6596 |
| `nq                       ` | 0.9864 |  0.8958 |        0.8958 |    0.9852 | 0.8958 | 0.9809 |
| `quora                    ` | 0.9999 |  0.9950 |        0.9950 |    0.9999 | 0.9950 | 0.9998 |
| `robust04                 ` | 0.7072 |  0.6345 |        0.6345 |    0.7046 | 0.6345 | 0.5611 |
| `scidocs                  ` | 0.7736 |  0.5656 |        0.5656 |    0.7779 | 0.5638 | 0.8090 |
| `scifact                  ` | 0.9967 |  0.9767 |        0.9767 |    0.9967 | 0.9767 | 0.9967 |
| `signal1m                 ` | 0.5933 |  0.5642 |        0.5642 |    0.5869 | 0.5642 | 0.4614 |
| `trec-covid               ` | 0.5125 |  0.3955 |        0.3955 |    0.5109 | 0.3955 | 0.4749 |
| `trec-news                ` | 0.8178 |  0.7051 |        0.7051 |    0.8166 | 0.7051 | 0.7797 |
| `webis-touche2020         ` | 0.8734 |  0.8621 |        0.8621 |    0.8782 | 0.8621 | 0.7866 |


## Run and Evaluate

### Running Retrieval and Fusion with Pyserini

The following script will generate the complete set of fusion results using FAISS:

```bash
./pyserini_beir_retrieve_faiss.sh
```

This script performs:
1. BM25 sparse retrieval on all BEIR corpora
2. BGE-base-en-v1.5 dense retrieval using FAISS
3. Four fusion methods: RRF, Average, Interpolation, Normalize
4. Comprehensive timing for each operation (saved to `timing_results/`)

### Run and Evaluate

```bash
CORPORA=(trec-covid bioasq nfcorpus nq hotpotqa fiqa signal1m trec-news robust04 arguana webis-touche2020 cqadupstack-android cqadupstack-english cqadupstack-gaming cqadupstack-gis cqadupstack-mathematica cqadupstack-physics cqadupstack-programmers cqadupstack-stats cqadupstack-tex cqadupstack-unix cqadupstack-webmasters cqadupstack-wordpress quora dbpedia-entity scidocs fever climate-fever scifact)
for c in "${CORPORA[@]}"
do
    # BM25 search
    python -m pyserini.search.lucene \
        --index beir-v1.0.0-${c}.flat \
        --topics beir-v1.0.0-${c}-test \
        --output runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 \
        --bm25 \
        --remove-query \
        --hits 1000 \
        --threads 32 \
        --batch-size 256

    # BGE search using FAISS
    python -m pyserini.search.faiss \
        --encoder-class auto \
        --encoder BAAI/bge-base-en-v1.5 \
        --l2-norm \
        --pooling mean \
        --index beir-v1.0.0-${c}.bge-base-en-v1.5 \
        --topics beir-v1.0.0-${c}-test \
        --output runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt \
        --batch 256 \
        --threads 32 \
        --hits 1000 \
        --remove-query
    
    # RRF fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt \
        --output runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt \
        --method rrf \
        --k 1000 \
        --depth 1000 \
        --rrf.k 60

    # Average fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt \
        --output runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt \
        --method average \
        --k 1000 \
        --depth 1000

    # Interpolation fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt \
        --output runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt \
        --method interpolation \
        --k 1000 \
        --depth 1000 \
        --alpha 0.5

    # Normalize fusion
    python -m pyserini.fusion \
        --runs runs/run.inverted.beir-v1.0.0-${c}.flat.test.bm25 runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt \
        --output runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt \
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

    # BGE-FAISS
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/run.faiss.beir-v1.0.0-${c}.bge-base-en-v1.5.test.txt
    
    # RRF Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.rrf.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt

    # Average Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.avg.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    
    # Interpolation Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.interp.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt

    # Normalize Fusion
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.100 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
    python -m pyserini.eval.trec_eval -c -m recall.1000 beir-v1.0.0-${c}-test runs/runs.fuse.norm.beir-v1.0.0-${c}.flat.bm25.bge-faiss.test.txt
done
```


## Reproduction Log

These results can be reproduced using the provided scripts in this repository.


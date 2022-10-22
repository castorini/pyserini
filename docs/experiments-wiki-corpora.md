# Pyserini: Reproducing DPR Results With Improved Wikipedia Corpus Variants

Dense passage retriever (DPR) is a dense retrieval method described in the following paper:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih. [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/). _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2020.

We have replicated DPR results with our Wikipedia corpus variants and incorporated the technique into Pyserini.

Our own efforts are described in the paper entitled: "Pre-Processing Matters! Improved Wikipedia Corpora for Open-Domain Question Answering"

This guide provides instructions to reproduce some of the commands in our study. Note that you will need to change the parameters to the commands as necessary.
Our efforts include both retrieval as well as end-to-end answer generation.
We cover only retrieval here; for end-to-end answer generation, please see [this guide](https://github.com/manveertamber/pygaggle/blob/master/docs/experiments-wiki-corpora-fid.md) in our PyGaggle neural text ranking library.


## Generate Corpora
We start with downloading the full December 20, 2018 Wikipedia XML dump from the Internet Archive: https://archive.org/details/enwiki-20181220. This is then Pre-processed by WikiExtractor: https://github.com/attardi/wikiextractor (making sure to include lists if needed and replacing tables with the string "TABLETOREPLACE") and DrQA: https://github.com/facebookresearch/DrQA/tree/main/scripts/retriever (again making sure to not remove lists if needed). 

We then apply the pre-processing script we make available in this repository to generate the different corpus variants. Note that this is a time consuming process and uses a lot of memory if tables are included. 


```
cd pyserini/scripts/

python wiki_generate_tsv_no_tables_lists.py \
  -db_path plain.db \
  -output_path_6_3 wiki_6_3.tsv \
  -output_path_8_4 wiki_8_4.tsv \
  -output_path_100w wiki_100w.tsv 

python wiki_generate_tsv.py \
  -db_path tables_and_lists.db \
  -output_path_6_3 wiki_TL_6_3.tsv \
  -output_path_8_4 wiki_TL_8_4.tsv \
  -xml_path ../wiki/enwiki-20181220-pages-articles.xml
```

We take the .tsv files generated in the previous step and convert them to Pyserini and Anserini's JSONL format for indexing. 

For convenience we make the JSONL files available here: (You may use wget to download them)

[Wiki_our_100w_corpus](https://www.dropbox.com/s/o5qwqati0ccwkjo/wikipedia_100_word_splits.tar)  
[Wiki_6_3_corpus](https://www.dropbox.com/s/7o8y0ewuh8rkh9f/wikipedia_segment-6_stride-3.tar)  
[Wiki_6_3_TL_corpus](https://www.dropbox.com/s/9q7lqkc7duffmkl/wikipedia_segment-6_stride-3_tables_and_lists.tar)  
[Wiki_8_4_corpus](https://www.dropbox.com/s/fa099hfgb2a8660/wikipedia_segment-8_stride-4.tar)  
[Wiki_8_4_TL_corpus](https://www.dropbox.com/s/d5gfnvju7apvcsm/wikipedia_segment-8_stride-4_tables_and_lists.tar)

## Indexing

We index the jsonl file(s) using the following command.
```
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input path_to_jsonl_corpora \
  --index indexes/wiki_index \
  --generator DefaultLuceneDocumentGenerator \
  --threads 4 \
  --storeRaw
```

## BM25 Retrieval
With a chosen QA dataset (we use nq-test here as an example), we can perform BM25 retrieval using the following command
```
python -m pyserini.search.lucene \
  --index indexes/wiki_index \
  --topics nq-test \
  --batch-size 4 \
  --threads 4 \
  --hits 1000 \
  --output runs/run.trec
```

## DPR Retrieval

Retrieval with a DPR model is done in the Tevatron toolkit. Please follow the instructions from this document: https://github.com/texttron/tevatron/blob/main/examples/example_dpr.md. 

We make the DPR models available here: (You may use wget to download them)

[DPR-multi (1st Iteration) model for wiki_our_100w_corpus](https://www.dropbox.com/s/fewknoyo013tyhq/model_our_100w_multi.tar.gz)  
[DPR-multi (2nd Iteration) model for wiki_our_100w_corpus](https://www.dropbox.com/s/mk223441u1w8auh/model_our_100w_multi2.tar.gz)  
[DPR-nq (1st Iteration) model for wiki_our_100w_corpus](https://www.dropbox.com/s/3pwrfafuvuozwcs/model_our_100w_nq.tar.gz)  
[DPR-nq (2nd Iteration) model for wiki_our_100w_corpus](https://www.dropbox.com/s/clnuuzwuvrypsyh/model_our_100w_nq2.tar.gz)  
[DPR-multi (1st Iteration) model for wiki_6_3_corpus](https://www.dropbox.com/s/wtcqfwi2rqey1e2/model_6_3_multi.tar.gz)  
[DPR-multi (2nd Iteration) model for wiki_6_3_corpus](https://www.dropbox.com/s/5owlel8qpgcwgzx/model_6_3_multi2.tar.gz)  
[DPR-nq (1st Iteration) model for wiki_6_3_corpus](https://www.dropbox.com/s/bxr9s9ltsao2qn0/model_6_3_nq.tar.gz)  
[DPR-nq (2nd Iteration) model for wiki_6_3_corpus](https://www.dropbox.com/s/zw98i3p3eih3gdb/model_6_3_nq2.tar.gz)  
[DPR-multi (1st Iteration) model for wiki_6_3_TL_corpus](https://www.dropbox.com/s/npva0g3wpq67b9x/model_tables_6_3_multi.tar.gz)  
[DPR-multi (2nd Iteration) model for wiki_6_3_TL_corpus](https://www.dropbox.com/s/91k83kxkyswsrii/model_tables_6_3_multi2.tar.gz)  
[DPR-nq (1st Iteration) model for wiki_6_3_TL_corpus](https://www.dropbox.com/s/0t3naejxhqs1315/model_tables_6_3_nq.tar.gz)  
[DPR-nq (2nd Iteration) model for wiki_6_3_TL_corpus](https://www.dropbox.com/s/woj2zoobjqhdyyo/model_tables_6_3_nq2.tar.gz)  
[DPR-multi (1st Iteration) model for wiki_8_4_corpus](https://www.dropbox.com/s/4t040pcu2et5vvi/model_8_4_multi.tar.gz)  
[DPR-multi (2nd Iteration) model for wiki_8_4_corpus](https://www.dropbox.com/s/oh1ik9gdj7psysl/model_8_4_multi2.tar.gz)  
[DPR-nq (1st Iteration) model for wiki_8_4_corpus](https://www.dropbox.com/s/77ygo8uoehheqt5/model_8_4_nq.tar.gz)  
[DPR-nq (2nd Iteration) model for wiki_8_4_corpus](https://www.dropbox.com/s/xm0b9vex84v82ol/model_8_4_nq2.tar.gz)  
[DPR-multi (1st Iteration) model for wiki_8_4_TL_corpus](https://www.dropbox.com/s/1jeehwq0zwdiv2f/model_tables_8_4_multi.tar.gz)  
[DPR-multi (2nd Iteration) model for wiki_8_4_TL_corpus](https://www.dropbox.com/s/yp71q685qew7c9i/model_tables_8_4_multi2.tar.gz)  
[DPR-nq (1st Iteration) model for wiki_8_4_TL_corpus](https://www.dropbox.com/s/zg47epdj861869z/model_tables_8_4_nq.tar.gz)  
[DPR-nq (2nd Iteration) model for wiki_8_4_TL_corpus](https://www.dropbox.com/s/yty2gwtatan6kfw/model_tables_8_4_nq2.tar.gz)  




## Hybrid Retrieval
We can fuse the DPR and BM25 retrieval results using the following command. This uses reciprocal rank fusion.
```
python -m pyserini.fusion \
  --runs bm25_run.trec dpr_run.trec \
  --out hybrid.trec
```

## Evaluation
After retrieval is complete, we can evaluate results as follows. The final command should output 2 values, the top-20 accuracy and the top-100 accuracy.

```
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --index indexes/wiki_index \
  --topics nq-test \
  --input runs/run.trec \
  --output runs/run.json \
  --store-raw 

python -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.json \
  --topk 20 100
```

## Summary

Here's how our results stack up

### BM25 Results:

NQ Dev Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.6219                 | 0.6252                     | 0.6451                     | 0.6465                            | 0.6672                            |
| Top 100 Accuracy | 0.7603                 | 0.7635                     | 0.7807                     | 0.7987                            | 0.8080                            |

Trivia Dev Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.7632                 | 0.7751                     | 0.7839                     | 0.7814                            | 0.7895                            |
| Top 100 Accuracy | 0.8313                 | 0.8401                     | 0.8479                     | 0.8453                            | 0.8523                            |

NQ Test Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.6377                 | 0.6429                     | 0.6673                     | 0.6665                            | 0.6964                            |
| Top 100 Accuracy | 0.7812                 | 0.7892                     | 0.7964                     | 0.8166                            | 0.8291                            |

Trivia Test Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.7625                 | 0.7749                     | 0.7858                     | 0.7832                            | 0.7947                            |
| Top 100 Accuracy | 0.8328                 | 0.8420                     | 0.8471                     | 0.8482                            | 0.8546                            |

WQ Test Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.6063                 | 0.6284                     | 0.6521                     | 0.6403                            | 0.6609                            |
| Top 100 Accuracy | 0.7515                 | 0.7653                     | 0.7820                     | 0.7874                            | 0.8022                            |

Curated Test Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.7983                 | 0.8141                     | 0.8271                     | 0.8055                            | 0.8271                            |
| Top 100 Accuracy | 0.9049                 | 0.9121                     | 0.9222                     | 0.9135                            | 0.9207                            |

Squad Test Results

| Wikipedia Corpus | Ours (100 word splits) | Ours (Segment 6, Stride 3) | Ours (Segment 8, Stride 4) | With Tables and Lists (Segment 6, Stride 3) | With Tables and Lists (Segment 8, Stride 4) |
|------------------|------------------------|----------------------------|----------------------------|-----------------------------------|-----------------------------------|
| Top 20 Accuracy  | 0.7020                 | 0.7408                     | 0.7479                     | 0.7265                            | 0.7348                            |
| Top 100 Accuracy | 0.8134                 | 0.8443                     | 0.8500                     | 0.8325                            | 0.8410                            |

### DPR Results (1st and 2nd iteration models)

| Dpr-1 (MULTI)      | NQ-dev |         | NQ-test |         | Trivia-dev |         | Trivia-test |         | WQ-test |         | Curated-test |         | Squad-test |         |
|:----------------------:|:------:|:-------:|:-------:|:-------:|:----------:|:-------:|:-----------:|:-------:|:-------:|:-------:|:------------:|:-------:|:----------:|:-------:|
|         Corpus         | Top-20 | Top-100 |  Top-20 | Top-100 |   Top-20   | Top-100 |    Top-20   | Top-100 |  Top-20 | Top-100 |    Top-20    | Top-100 |   Top-20   | Top-100 |
| Wiki_6_3               | 0.7481 |  0.8448 |  0.7640 |  0.8579 |     0.7765 |  0.8478 |      0.7787 |  0.8499 |  0.7082 |  0.8125 |       0.8573 |  0.9294 |     0.5365 |  0.6956 |
| wiki_TL_6_3        | 0.7765 |  0.8786 |  0.7873 |  0.8895 |     0.7838 |  0.8495 |      0.7833 |  0.8564 |  0.7308 |  0.8199 |       0.8847 |  0.9438 |     0.5323 |  0.6855 |
| Wiki_8_4               | 0.7590 |  0.8481 |  0.7690 |  0.8634 |     0.7821 |  0.8493 |      0.7853 |  0.8542 |  0.7180 |  0.8130 |       0.8804 |  0.9467 |     0.5509 |  0.7066 |
| wiki_TL_8_4        | 0.7887 |  0.8847 |  0.8042 |  0.8978 |     0.7924 |  0.8540 |      0.7902 |  0.8571 |  0.7411 |  0.8307 |       0.8790 |  0.9395 |     0.5437 |  0.7017 |
| Wiki_our_100w          | 0.7464 |  0.8410 |  0.7537 |  0.8512 |     0.7825 |  0.8483 |      0.7804 |  0.8477 |  0.7008 |  0.8086 |       0.8818 |  0.9409 |     0.5047 |  0.6718 |


| Hybrid Dpr-1 (MULTI) | NQ-dev |         | NQ-test |         | Trivia-dev |         | Trivia-test |         | WQ-test |         | Curated-test |         | Squad-test |         |
|:--------------------:|:------:|:-------:|:-------:|:-------:|------------|---------|-------------|---------|---------|---------|--------------|---------|:----------:|:-------:|
|        Corpus        | Top-20 | Top-100 |  Top-20 | Top-100 |   Top-20   | Top-100 |    Top-20   | Top-100 |  Top-20 | Top-100 |    Top-20    | Top-100 |   Top-20   | Top-100 |
| Wiki_6_3             | 0.7925 |  0.8651 |  0.7956 |  0.8787 |     0.8287 |  0.8700 |      0.8289 |  0.8703 |  0.7608 |  0.8386 |       0.8948 |  0.9452 |     0.7677 |  0.8585 |
| wiki_TL_6_3      | 0.8224 |  0.8997 |  0.8332 |  0.9133 |     0.8342 |  0.8753 |      0.8379 |  0.8784 |  0.7707 |  0.8583 |       0.9222 |  0.9524 |     0.7563 |  0.8511 |
| Wiki_8_4             | 0.8027 |  0.8739 |  0.8119 |  0.8834 |     0.8322 |  0.8728 |      0.8348 |  0.8756 |  0.7559 |  0.8455 |       0.9107 |  0.9568 |     0.7711 |  0.8603 |
| wiki_TL_8_4      | 0.8365 |  0.9076 |  0.8465 |  0.9186 |     0.8394 |  0.8782 |      0.8423 |  0.8813 |  0.7874 |  0.8578 |       0.9150 |  0.9510 |     0.7604 |  0.8579 |
| Wiki_our_100w        | 0.7891 |  0.8646 |  0.7958 |  0.8781 |     0.8238 |  0.8673 |      0.8240 |  0.8701 |  0.7382 |  0.8346 |       0.9006 |  0.9467 |     0.7333 |  0.8309 |

| Dpr-1 (NQ)          | NQ-dev |         | NQ-test |         |
|:-------------------:|:------:|:-------:|:-------:|:-------:|
|        Corpus       | Top-20 | Top-100 |  Top-20 | Top-100 |
| Wiki_6_3            | 0.7593 |  0.8497 |  0.7698 |  0.8645 |
| wiki_TL_6_3     | 0.7805 |  0.8824 |  0.7928 |  0.8909 |
| Wiki_8_4            | 0.7578 |  0.8512 |  0.7762 |  0.8687 |
| wiki_TL_8_4     | 0.7972 |  0.8865 |  0.8114 |  0.8997 |
| Wiki_our_100w       | 0.7508 |  0.8450 |  0.7662 |  0.8540 |

| Hybrid Dpr-1 (NQ) | NQ-dev |         | NQ-test |         |
|:-----------------:|:------:|:-------:|:-------:|:-------:|
|       Corpus      | Top-20 | Top-100 |  Top-20 | Top-100 |
| Wiki_6_3          | 0.7922 |  0.8698 |  0.8053 |  0.8825 |
| wiki_TL_6_3   | 0.8238 |  0.9020 |  0.8299 |  0.9175 |
| Wiki_8_4          | 0.7996 |  0.8726 |  0.8122 |  0.8864 |
| wiki_TL_8_4   | 0.8350 |  0.9105 |  0.8446 |  0.9163 |
| Wiki_our_100w     | 0.7895 |  0.8656 |  0.8011 |  0.8734 |

| Dpr-2 (MULTI)     | NQ-dev |         | NQ-test |         | Trivia-dev |         | Trivia-test |         | WQ-test |         | Curated-test |         | Squad-test |         |
|:----------------------:|:------:|:-------:|:-------:|:-------:|:----------:|:-------:|:-----------:|:-------:|:-------:|:-------:|:------------:|:-------:|:----------:|:-------:|
|         Corpus         | Top-20 | Top-100 |  Top-20 | Top-100 |   Top-20   | Top-100 |    Top-20   | Top-100 |  Top-20 | Top-100 |    Top-20    | Top-100 |   Top-20   | Top-100 |
| Wiki_6_3               | 0.8010 |  0.8711 |  0.8111 |  0.8834 |     0.8085 |  0.8589 |      0.8120 |  0.8618 |  0.7653 |  0.8425 |       0.9035 |  0.9424 |     0.6062 |  0.7531 |
| wiki_TL_6_3        | 0.8376 |  0.9081 |  0.8543 |  0.9180 |     0.8188 |  0.8678 |      0.8195 |  0.8709 |  0.8007 |  0.8740 |       0.9179 |  0.9582 |     0.6079 |  0.7509 |
| Wiki_8_4               | 0.8092 |  0.8737 |  0.8219 |  0.8856 |     0.8134 |  0.8634 |      0.8112 |  0.8643 |  0.7776 |  0.8533 |       0.9164 |  0.9524 |     0.6032 |  0.7445 |
| wiki_TL_8_4        | 0.8490 |  0.9168 |  0.8587 |  0.9269 |     0.8201 |  0.8687 |      0.8239 |  0.8740 |  0.8017 |  0.8681 |       0.9063 |  0.9539 |     0.6108 |  0.7479 |
| Wiki_our_100w          | 0.7929 |  0.8694 |  0.8000 |  0.8812 |     0.8021 |  0.8565 |      0.8018 |  0.8580 |  0.7495 |  0.8396 |       0.9135 |  0.9510 |     0.5768 |  0.7266 |

| Hybrid Dpr-2 (MULTI) | NQ-dev |         | NQ-test |         | Trivia-dev |         | Trivia-test |         | WQ-test |         | Curated-test |         | Squad-test |         |
|:--------------------:|:------:|:-------:|:-------:|:-------:|------------|---------|-------------|---------|---------|---------|--------------|---------|:----------:|:-------:|
|        Corpus        | Top-20 | Top-100 |  Top-20 | Top-100 |   Top-20   | Top-100 |    Top-20   | Top-100 |  Top-20 | Top-100 |    Top-20    | Top-100 |   Top-20   | Top-100 |
| Wiki_6_3             | 0.8048 |  0.8778 |  0.8161 |  0.8917 |     0.8306 |  0.8716 |      0.8332 |  0.8737 |  0.7736 |  0.8465 |       0.9164 |  0.9539 |     0.7791 |  0.8651 |
| wiki_TL_6_3      | 0.8394 |  0.9141 |  0.8518 |  0.9302 |     0.8443 |  0.8772 |      0.8417 |  0.8800 |  0.8036 |  0.8745 |       0.9150 |  0.9640 |     0.7693 |  0.8589 |
| Wiki_8_4             | 0.8157 |  0.8830 |  0.8258 |  0.8922 |     0.8386 |  0.8764 |      0.8397 |  0.8774 |  0.7790 |  0.8524 |       0.9193 |  0.9510 |     0.7809 |  0.8669 |
| wiki_TL_8_4      | 0.8534 |  0.9220 |  0.8601 |  0.9319 |     0.8446 |  0.8807 |      0.8464 |  0.8850 |  0.8046 |  0.8755 |       0.9150 |  0.9582 |     0.7752 |  0.8640 |
| Wiki_our_100w        | 0.7950 |  0.8767 |  0.8125 |  0.8892 |     0.8240 |  0.8668 |      0.8250 |  0.8707 |  0.7598 |  0.8440 |       0.9121 |  0.9467 |     0.7441 |  0.8413 |

| Dpr-2 (NQ)          | NQ-dev |         | NQ-test |         |
|:-------------------:|:------:|:-------:|:-------:|:-------:|
|        Corpus       | Top-20 | Top-100 |  Top-20 | Top-100 |
| Wiki_6_3            | 0.8075 |  0.8728 |  0.8158 |  0.8850 |
| wiki_TL_6_3     | 0.8470 |  0.9091 |  0.8521 |  0.9227 |
| Wiki_8_4            | 0.8102 |  0.8734 |  0.8249 |  0.8920 |
| wiki_TL_8_4     | 0.8521 |  0.9120 |  0.8637 |  0.9238 |
| Wiki_our_100w       | 0.7963 |  0.8710 |  0.8122 |  0.8784 |

| Hybrid Dpr-2 (NQ) | NQ-dev |         | NQ-test |         |
|:-----------------:|:------:|:-------:|:-------:|:-------:|
|       Corpus      | Top-20 | Top-100 |  Top-20 | Top-100 |
| Wiki_6_3          | 0.8076 |  0.8784 |  0.8177 |  0.8934 |
| wiki_TL_6_3   | 0.8452 |  0.9174 |  0.8551 |  0.9283 |
| Wiki_8_4          | 0.8128 |  0.8818 |  0.8327 |  0.8975 |
| wiki_TL_8_4   | 0.8567 |  0.9225 |  0.8648 |  0.9291 |
| Wiki_our_100w     | 0.7959 |  0.8780 |  0.8089 |  0.8842 |



## Reproduction Log[*](reproducibility.md)


# Pyserini: Reproducing DPR Results With Improved Wikipedia Corpus Variants

Dense passage retriever (DPR) is a dense retrieval method described in the following paper:

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih. [Dense Passage Retrieval for Open-Domain Question Answering](https://www.aclweb.org/anthology/2020.emnlp-main.550/). _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages 6769-6781, 2020.

We have replicated DPR results with our Wikipedia corpus variants.

Our own efforts are described in the paper: 
> Manveer Singh Tamber, Ronak Pradeep, and Jimmy Lin. "Pre-Processing Matters! Improved Wikipedia Corpora for Open-Domain Question Answering". ECIR 2023.

This guide provides instructions to reproduce the pre-processing to generate the corpora and the retrieval on the ```wiki-all-6-3-tamber``` corpus variant.
For end-to-end answer generation, please see [this guide](https://github.com/castorini/pygaggle/blob/master/docs/experiments-wiki-corpora-fid.md) in our PyGaggle neural text ranking and question answering library.

## Generate Corpora
We start with downloading the full December 20, 2018 Wikipedia XML dump: ```enwiki-20181220-pages-articles.xml``` from the Internet Archive: https://archive.org/details/enwiki-20181220. This is then pre-processed by WikiExtractor: https://github.com/attardi/wikiextractor (making sure to modify the code to include lists as desired and replacing tables with the string "TABLETOREPLACE"). The following command is used for the corpora with no tables, infoboxes, or lists:
```
python -m wikiextractor.WikiExtractor \
  ../wiki/enwiki-20181220-pages-articles.xml  
  -o ../wiki_extractor_out/wiki-text/ \
  --json
```
and the same command (with modified code as described above) is used for the corpora with tables, infoboxes, and lists:
```
python -m wikiextractor.WikiExtractor \
  ../wiki/enwiki-20181220-pages-articles.xml  
  -o ../wiki_extractor_out/wiki-all/ \
  --json
```
The next step is using DrQA pre-processing: https://github.com/facebookresearch/DrQA/tree/main/scripts/retriever (again making sure to modify the code to not remove lists as desired) using the following commands:
```
python build_db.py \
  ../wiki_extractor_out/wiki-text/ \
  wiki-text.db \
  --preprocess prep_wikipedia.py
```
```
python build_db.py \
  ../wiki_extractor_out/wiki-all/ \
  wiki-all.db \
  --preprocess prep_wikipedia.py
```
We then apply the pre-processing script we make available in Pyserini to generate the different corpus variants. Note that this is a time consuming process and uses a lot of memory if tables are included. 

```
cd pyserini/scripts/

python wiki_generate_tsv_no_tables_lists.py \
  -db_path wiki-text.db \
  -output_path_6_3 wiki-text-6-3.tsv \
  -output_path_8_4 wiki-text-8-4.tsv \
  -output_path_100w wiki-text-100w.tsv 

python wiki_generate_tsv.py \
  -db_path wiki-all.db \
  -output_path_6_3 wiki-all-6-3.tsv \
  -output_path_8_4 wiki-all-8-4.tsv \
  -xml_path ../wiki/enwiki-20181220-pages-articles.xml
```

We take the .tsv files generated in the previous step and convert them to Pyserini and Anserini's JSONL format for indexing. 

## Download the Corpora

We make the different Wikipedia corpus variants available in [HuggingFace🤗](https://huggingface.co/datasets/castorini/odqa-wiki-corpora).

To download the corpora you may clone the repository. 
Make sure you have Git LFS set up by running 
```
git lfs install
```
Then to clone, run:
```
git clone https://huggingface.co/datasets/castorini/odqa-wiki-corpora
```

The following instructions will continue with the wiki-all-6-3-tamber corpus. We use the NaturalQuestions and TriviaQA datasets for evaluation.

## Indexing
We index the jsonl file(s) using the following command. You may skip this step as we provide the lucene index prebuilt in Pyserini. In the following steps, if you would like to use the index that you generate in this step then specify ```--index indexes/wiki-all-6-3-tamber``` instead of ```--index wiki-all-6-3-tamber```.
```
python3 -m pyserini.index.lucene \
  --collection MrTyDiCollection \
  --input odqa-wiki-corpora/wiki-all-6-3-tamber \
  --index indexes/wiki-all-6-3-tamber \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --storeRaw
```

## BM25 Retrieval
To run BM25 retrieval:

### Natural Questions
```
python3 -m pyserini.search.lucene \
  --index wiki-all-6-3-tamber \
  --topics nq-test \
  --batch-size 20 \
  --threads 10 \
  --hits 1000 \
  --output runs/run.wiki-all-6-3.nq-test.bm25.trec
```

After retrieval is complete, we can evaluate results as follows. The final command should output 2 values, the top-20 accuracy and the top-100 accuracy.

```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.nq-test.bm25.trec \
  --output runs/run.wiki-all-6-3.nq-test.bm25.json \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.nq-test.bm25.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.6665
Top100  accuracy: 0.8166
```
### TriviaQA
```
python3 -m pyserini.search.lucene \
  --index wiki-all-6-3-tamber \
  --topics dpr-trivia-test \
  --batch-size 20 \
  --threads 10 \
  --hits 1000 \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.bm25.trec
```

To get the results:
```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.dpr-trivia-test.bm25.trec \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.bm25.json \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.dpr-trivia-test.bm25.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.7832
Top100  accuracy: 0.8482
```

## DPR Retrieval

Retrieval with a DPR model can be done in the Tevatron toolkit. Please follow the instructions from [Tevatron](https://github.com/texttron/tevatron/blob/main/examples/example_dpr.md) to do this. 

We make the $2^{nd}$ iteration DPR models available in HuggingFace🤗 for all corpus variants. The links to the models for wiki-all-6-3-tamber are:

[wiki-all-6-3-multi-dpr2-passage-encoder](https://huggingface.co/manveertamber/wiki-all-6-3-multi-dpr2-passage-encoder)  
[wiki-all-6-3-multi-dpr2-query-encoder](https://huggingface.co/manveertamber/wiki-all-6-3-multi-dpr2-query-encoder)  
 
Alternatively, retrieval can be performed in Pyserini as we make the encoded-queries for NaturalQuestions and TriviaQA and the dense index available in the wiki-all-6-3-tamber setting:

### Natural Questions
```
python3 -m pyserini.search.faiss \
  --index wiki-6-3-all-dpr2-multi \
  --topics nq-test \
  --encoded-queries wiki-6-3-all-dpr2-multi-nq-test \
  --output runs/run.wiki-all-6-3.nq-test.dpr2.trec \
  --hits 1000 \
  --batch-size 72 --threads 36
```
To get the results:
```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.nq-test.dpr2.trec \
  --output runs/run.wiki-all-6-3.nq-test.dpr2.json \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.nq-test.dpr2.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.8546
Top100  accuracy: 0.9175
```

### TriviaQA
```
python3 -m pyserini.search.faiss \
  --index wiki-6-3-all-dpr2-multi \
  --topics dpr-trivia-test \
  --encoded-queries wiki-6-3-all-dpr2-multi-dpr-trivia-test \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.dpr2.trec \
  --hits 1000 \
  --batch-size 72 --threads 36
```
To get the results:
```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.dpr-trivia-test.dpr2.trec \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.dpr2.json \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.dpr-trivia-test.dpr2.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.8192
Top100  accuracy: 0.8709
```

## Hybrid Retrieval
In the hybrid setting, we perform reciprocal rank fusion (RRF) using the rankings from the DPR model and BM25.

Note we use the --store-raw option in pyserini.eval.convert_trec_run_to_dpr_retrieval_run because we will be using the .json files for [end-to-end answer generation in PyGaggle](https://github.com/castorini/pygaggle/blob/master/docs/experiments-wiki-corpora-fid.md)

### Natural Questions
```
python3 -m pyserini.fusion \
  --runs runs/run.wiki-all-6-3.nq-test.dpr2.trec \
         runs/run.wiki-all-6-3.nq-test.bm25.trec \
  --output runs/run.wiki-all-6-3.nq-test.hybrid.trec \
  --k 100
```
To get the results:
```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics nq-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.nq-test.hybrid.trec \
  --output runs/run.wiki-all-6-3.nq-test.hybrid.json \
  --store-raw \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.nq-test.hybrid.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.8526
Top100  accuracy: 0.9302
```

### TriviaQA
```
python3 -m pyserini.fusion \
  --runs runs/run.wiki-all-6-3.dpr-trivia-test.dpr2.trec \
         runs/run.wiki-all-6-3.dpr-trivia-test.bm25.trec \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.hybrid.trec \
  --k 100
```
To get the results:
```
python3 -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
  --topics dpr-trivia-test \
  --index wiki-all-6-3-tamber \
  --input runs/run.wiki-all-6-3.dpr-trivia-test.hybrid.trec \
  --output runs/run.wiki-all-6-3.dpr-trivia-test.hybrid.json \
  --store-raw \
  --combine-title-text

python3 -m pyserini.eval.evaluate_dpr_retrieval \
  --retrieval runs/run.wiki-all-6-3.dpr-trivia-test.hybrid.json \
  --topk 20 100
```
Expected Output:
```
Top20   accuracy: 0.8420
Top100  accuracy: 0.8803
```


## Reproduction Log[*](reproducibility.md)


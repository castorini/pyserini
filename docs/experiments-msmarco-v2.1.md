# Pyserini: BM25 Baselines for MS MARCO V2.1

The MS MARCO V2.1 document corpus was curated for the TREC 2004 RAG Track and comes in two flavors: the doc corpus and the segmented doc corpus.
This guide provides instructions for getting started with both variants using Pyserini: we provide prebuilt indexes that you can use "right out of the box".

❗ Beware, you need lots of space to run these experiments.
The `msmarco-v2.1-doc` prebuilt index is 63 GB uncompressed.
The `msmarco-v2.1-doc-segmented` prebuilt index is 84 GB uncompressed.
Both indexes will be downloaded automatically with the following commands.

For the TREC 2024 RAG Track, we have implemented BM25 baselines.
Current results are based existing qrels that have been "projected" over from MS MARCO V2.0 passage judgments.
The table below reports effectiveness (dev in terms of RR@10, DL21-DL23, RAGgy in terms of nDCG@10):

|                                                                            |    dev |   dev2 |   DL21 |   DL22 |   DL23 |  RAGgy |
|:---------------------------------------------------------------------------|-------:|-------:|-------:|-------:|-------:|-------:|
| BM25 doc (<i>k<sub><small>1</small></sub></i>=0.9, <i>b</i>=0.4)           | 0.1654 | 0.1732 | 0.5183 | 0.2991 | 0.2914 | 0.3631 |
| BM25 doc-segmented (<i>k<sub><small>1</small></sub></i>=0.9, <i>b</i>=0.4) | 0.1973 | 0.2000 | 0.5778 | 0.3576 | 0.3356 | 0.4227 |

The following commands show how to run Pyserini on the dev queries and evaluate effectiveness, on both the doc corpus and the segmented doc corpus:

```bash
python -m pyserini.search.lucene --threads 16 --batch-size 128 --index msmarco-v2.1-doc --topics rag24.raggy-dev --output runs/run.msmarco-v2.1-doc.dev.txt --bm25

python -m pyserini.eval.trec_eval -c -M 100 -m map rag24.raggy-dev runs/run.msmarco-v2.1-doc.dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 rag24.raggy-dev runs/run.msmarco-v2.1-doc.dev.txt
python -m pyserini.eval.trec_eval -c -m recall.100 rag24.raggy-dev runs/run.msmarco-v2.1-doc.dev.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 rag24.raggy-dev runs/run.msmarco-v2.1-doc.dev.txt

python -m pyserini.search.lucene --threads 16 --batch-size 128 --index msmarco-v2.1-doc-segmented --topics rag24.raggy-dev --output runs/run.msmarco-v2.1-doc-segmented.dev.txt --bm25 --hits 10000 --max-passage-hits 1000 --max-passage

python -m pyserini.eval.trec_eval -c -M 100 -m map rag24.raggy-dev runs/run.msmarco-v2.1-doc-segmented.dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 rag24.raggy-dev runs/run.msmarco-v2.1-doc-segmented.dev.txt
python -m pyserini.eval.trec_eval -c -m recall.100 rag24.raggy-dev runs/run.msmarco-v2.1-doc-segmented.dev.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 rag24.raggy-dev runs/run.msmarco-v2.1-doc-segmented.dev.txt
```

The following snippet will generate the complete set of results that corresponds to the above table:

```bash
export OUTPUT_DIR="runs"

# doc condition
TOPICS=(msmarco-v2-doc.dev msmarco-v2-doc.dev2 dl21-doc dl22-doc dl23-doc rag24.raggy-dev); for t in "${TOPICS[@]}"
do
    python -m pyserini.search.lucene --threads 16 --batch-size 128 --index msmarco-v2.1-doc --topics $t --output $OUTPUT_DIR/run.msmarco-v2.1.doc.${t}.txt --bm25
done

# doc-segmented condition
TOPICS=(msmarco-v2-doc.dev msmarco-v2-doc.dev2 dl21-doc dl22-doc dl23-doc rag24.raggy-dev); for t in "${TOPICS[@]}"
do
    python -m pyserini.search.lucene --threads 16 --batch-size 128 --index msmarco-v2.1-doc-segmented --topics $t --output $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.${t}.txt --bm25 --hits 10000 --max-passage-hits 1000 --max-passage
done
```

<details>
<summary>Manual evaluation</summary>

Here's the snippet of code to perform the evaluation of all runs above:

```bash
# doc condition
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank msmarco-v2.1-doc.dev $OUTPUT_DIR/run.msmarco-v2.1.doc.msmarco-v2-doc.dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank msmarco-v2.1-doc.dev2 $OUTPUT_DIR/run.msmarco-v2.1.doc.msmarco-v2-doc.dev2.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl21-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl22-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc.dl23-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -m recall.100 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc.rag24.raggy-dev.txt

# doc-segmented condition
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank msmarco-v2.1-doc.dev $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.msmarco-v2-doc.dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank msmarco-v2.1-doc.dev2 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.msmarco-v2-doc.dev2.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl21-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl21-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl21-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl22-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl22-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl22-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.100 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl23-doc.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 dl23-doc-msmarco-v2.1 $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.dl23-doc.txt
echo ''
python -m pyserini.eval.trec_eval -c -M 100 -m map rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m ndcg_cut.10 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -m recall.100 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.rag24.raggy-dev.txt
python -m pyserini.eval.trec_eval -c -m recall.1000 rag24.raggy-dev $OUTPUT_DIR/run.msmarco-v2.1.doc-segmented.rag24.raggy-dev.txt
```

And these are the complete set of expected scores:

```
# doc condition
recip_rank            	all	0.1654
recip_rank            	all	0.1732

map                   	all	0.2281
recip_rank            	all	0.8466
ndcg_cut_10           	all	0.5183
recall_100            	all	0.3502
recall_1000           	all	0.6915

map                   	all	0.0841
recip_rank            	all	0.6623
ndcg_cut_10           	all	0.2991
recall_100            	all	0.1866
recall_1000           	all	0.4254

map                   	all	0.1089
recip_rank            	all	0.5783
ndcg_cut_10           	all	0.2914
recall_100            	all	0.2604
recall_1000           	all	0.5383

map                   	all	0.1251
recip_rank            	all	0.7060
ndcg_cut_10           	all	0.3631
recall_100            	all	0.2433
recall_1000           	all	0.5317

# doc-segmented condition
recip_rank            	all	0.1973
recip_rank            	all	0.2000

map                   	all	0.2609
recip_rank            	all	0.9026
ndcg_cut_10           	all	0.5778
recall_100            	all	0.3811
recall_1000           	all	0.7115

map                   	all	0.1079
recip_rank            	all	0.7213
ndcg_cut_10           	all	0.3576
recall_100            	all	0.2330
recall_1000           	all	0.4790

map                   	all	0.1391
recip_rank            	all	0.6519
ndcg_cut_10           	all	0.3356
recall_100            	all	0.3049
recall_1000           	all	0.5852

map                   	all	0.1561
recip_rank            	all	0.7465
ndcg_cut_10           	all	0.4227
recall_100            	all	0.2807
recall_1000           	all	0.5745
```

</details>

In addition, Pyserini provides a REST API for programmatic access (in truth, it's just a wrapper around a Java application in Anserini):

```bash
python -m pyserini.server.AnseriniApplication --server.port=8082
```

Here's a specific example of using the REST API to issue the query "How does the process of digestion and metabolism of carbohydrates start" to `msmarco-v2.1-doc`:

```bash
curl -X GET "http://localhost:8082/api/collection/msmarco-v2.1-doc/search?query=How%20does%20the%20process%20of%20digestion%20and%20metabolism%20of%20carbohydrates%20start" 
```

And the output looks something like:

```bash
{
  "query": {
    "text": "How does the process of digestion and metabolism of carbohydrates start",
    "qid": ""
  },
  "candidates": [
    {
      "docid": "msmarco_v2.1_doc_15_390497775",
      "score": 14.3364,
      "doc": {
        "url": "https://diabetestalk.net/blood-sugar/conversion-of-carbohydrates-to-glucose",
        "title": "Conversion Of Carbohydrates To Glucose | DiabetesTalk.Net",
        "headings": "...",
        "body": "..."
      }
    },
    {
      "docid": "msmarco_v2.1_doc_15_416962410",
      "score": 14.2271,
      "doc": {
        "url": "https://diabetestalk.net/insulin/how-is-starch-converted-to-glucose-in-the-body",
        "title": "How Is Starch Converted To Glucose In The Body? | DiabetesTalk.Net",
        "headings": "...",
        "body": "..."
      }
    },
    ...
  ]
}
```

Here's the command to query the `msmarco-v2.1-doc-segmented` index for 1000 hits (i.e., `hits=1000`):

```bash
curl -X GET "http://localhost:8082/api/collection/msmarco-v2.1-doc-segmented/search?query=How%20does%20the%20process%20of%20digestion%20and%20metabolism%20of%20carbohydrates%20start&hits=1000" 
```

You get the idea...

The API also provides an interactive search interface.
To access it, navigate to [`http://localhost:8082/`](http://localhost:8082/) in your browser.

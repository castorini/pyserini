# Pyserini: BM25 Baseline for MS MARCO Document Ranking

This guide contains instructions for running BM25 baselines on the [MS MARCO *document* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-doc.md), except that everything is in Python here (no Java).
Note that there is a separate guide for the [MS MARCO *passage* ranking task](experiments-msmarco-passage.md).

As of July 2023, this exercise has been removed from the Waterloo students [onboarding path](https://github.com/lintool/guide/blob/master/ura.md), which [starts here](https://github.com/castorini/anserini/blob/master/docs/start-here.md).

## Data Prep

The guide requires the [development installation](https://github.com/castorini/pyserini/blob/master/docs/installation.md#development-installation) for additional resource that are not shipped with the Python module.

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the MS MARCO document dataset:

```bash
mkdir collections/msmarco-doc
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs.trec.gz -P collections/msmarco-doc

# Alternative mirror:
# wget https://www.dropbox.com/s/w6caao3sfx9nluo/msmarco-docs.trec.gz -P collections/msmarco-doc
```

To confirm, `msmarco-docs.trec.gz` should have MD5 checksum of `d4863e4f342982b51b9a8fc668b2d0c0`.

There's no need to uncompress the file, as Pyserini can directly index gzipped files.
Build the index with the following command:

```bash
python -m pyserini.index.lucene \
  --collection CleanTrecCollection \
  --input collections/msmarco-doc \
  --index indexes/lucene-index-msmarco-doc \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
```

On a modern desktop with an SSD, indexing takes around 40 minutes.
There should be a total of 3,213,835 documents indexed.

## Performing Retrieval on the Dev Queries

The 5193 queries in the development set are already stored in the repo.
Let's take a peek:

```bash
$ head tools/topics-and-qrels/topics.msmarco-doc.dev.txt
174249	does xpress bet charge to deposit money in your account
320792	how much is a cost to run disneyland
1090270	botulinum definition
1101279	do physicians pay for insurance from their salaries?
201376	here there be dragons comic
54544	blood diseases that are sexually transmitted
118457	define bona fides
178627	effects of detox juice cleanse
1101278	do prince harry and william have last names
68095	can hives be a sign of pregnancy

$ wc tools/topics-and-qrels/topics.msmarco-doc.dev.txt
    5193   35787  220304 tools/topics-and-qrels/topics.msmarco-doc.dev.txt
```

Each line contains a tab-delimited (query id, query) pair.
Conveniently, Pyserini already knows how to load and iterate through these pairs.
We can now perform retrieval using these queries:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index-msmarco-doc \
  --topics msmarco-doc-dev \
  --output runs/run.msmarco-doc.bm25tuned.txt \
  --output-format msmarco \
  --hits 100 \
  --bm25 --k1 4.46 --b 0.82
```

Here, we set the BM25 parameters to `k1=4.46`, `b=0.82` (tuned by grid search).
The option `--output-format msmarco` says to generate output in the MS MARCO output format.
The option `--hits` specifies the number of documents to return per query.
Note that for the [MS MARCO Document Ranking Leaderboard](https://microsoft.github.io/MSMARCO-Document-Ranking-Submissions/leaderboard/), the official metric is MRR@100, so submissions should only return 100 hits per query. 

Retrieval speed will vary by hardware:
On a reasonably modern CPU with an SSD, we might get around 18 qps (queries per second), and so the entire run should finish in under five minutes (using a single thread).
We can perform multi-threaded retrieval by using the `--threads` and `--batch-size` arguments.
For example, setting `--threads 16 --batch-size 64` on a CPU with sufficient cores, the entire run will finish in under a minute.

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script:

```bash
$ python tools/scripts/msmarco/msmarco_doc_eval.py \
    --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
    --run runs/run.msmarco-doc.bm25tuned.txt

#####################
MRR @100: 0.2770296928568702
QueriesRanked: 5193
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@100.
For that we first need to convert the run file into TREC format:

```bash
python -m pyserini.eval.convert_msmarco_run_to_trec_run \
  --input runs/run.msmarco-doc.bm25tuned.txt \
  --output runs/run.msmarco-doc.bm25tuned.trec
```

And then run the `trec_eval` tool:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.100 -mmap \
   tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/run.msmarco-doc.bm25tuned.trec

map                   	all	0.2770
recall_100            	all	0.8076
```

Let's compare to the baseline provided by Microsoft.
First, download:

```bash
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-top100.gz -P runs
gunzip runs/msmarco-docdev-top100.gz
```

Then, run `trec_eval` to compare:

```bash
$ tools/eval/trec_eval.9.0.4/trec_eval -c -mrecall.100 -mmap \
   tools/topics-and-qrels/qrels.msmarco-doc.dev.txt runs/msmarco-docdev-top100

map                   	all	0.2219
recall_100            	all	0.7564
```

We can see that Pyserini's (tuned) BM25 baseline is already much better than the baseline provided by the organizers.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@JeffreyCA](https://github.com/JeffreyCA) on 2020-09-14 (commit [`49fd7cb`](https://github.com/castorini/pyserini/commit/49fd7cb8fd802493dc34f5cb33767d2e72e19f13))
+ Results reproduced by [@jhuang265](https://github.com/jhuang265) on 2020-09-14 (commit [`2ed2acc`](https://github.com/castorini/pyserini/commit/2ed2acc62e445e3e887c6cf853ccc0b0b3b57534))
+ Results reproduced by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2020-11-12 (commit [`55c3dbc`](https://github.com/castorini/pyserini/commit/55c3dbc607d72b5318bff14ee4f89dc73e019386))
+ Results reproduced by [@rakeeb123](https://github.com/rakeeb123) on 2020-12-07 (commit [`3bcd4e5`](https://github.com/castorini/pyserini/commit/3bcd4e52beb327d55ae6d3c8f6bc94351a6d1449))
+ Results reproduced by [@jrzhang12](https://github.com/jrzhang12) on 2021-01-03 (commit [`7caedfc`](https://github.com/castorini/pyserini/commit/7caedfc150f916de302297406c45dead27b475ba))
+ Results reproduced by [@HEC2018](https://github.com/HEC2018) on 2021-01-04 (commit [`46a6d47`](https://github.com/castorini/pyserini/commit/46a6d472267a559152495d004c2a12f8e95e53f0))
+ Results reproduced by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-08 (commit [`aeec31f`](https://github.com/castorini/pyserini/commit/aeec31fbe17d39ecf3081597b4832f5af57ea549))
+ Results reproduced by [@yemiliey](https://github.com/yemiliey) on 2021-01-18 (commit [`98f3236`](https://github.com/castorini/pyserini/commit/98f323659c8a0a5d8ef26bb3f6768458a34e3eb9))
+ Results reproduced by [@larryli1999](https://github.com/larryli1999) on 2021-01-04 (commit [`74a87e4`](https://github.com/castorini/pyserini/commit/74a87e4951c98d7b066273140576d3cccd9ea0ed))
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-01-04 (commit [`7261223`](https://github.com/castorini/pyserini/commit/72612232bc886e71e8de9431a899a7c68f1d82c7))
+ Results reproduced by [@printfCalvin](https://github.com/printfCalvin) on 2021-04-12 (commit [`0801f7f`](https://github.com/castorini/pyserini/commit/0801f7fb15e249f2e67901a6523d6ce68c667207))
+ Results reproduced by [@saileshnankani](https://github.com/saileshnankani) on 2021-04-26 (commit [`6d48609`](https://github.com/castorini/pyserini/commit/6d486094137a26c8a0a57652a06ab4d42d5bce32))
+ Results reproduced by [@andrewyguo](https://github.com/andrewyguo) on 2021-04-30 (commit [`ecfed61`](https://github.com/castorini/pyserini/commit/ecfed61bfba065aa958848cff96ba9f22609aeb1))
+ Results reproduced by [@mayankanand007](https://github.com/mayankanand007) on 2021-05-04 (commit [`a9d6f66`](https://github.com/castorini/pyserini/commit/a9d6f66234b5dd2859a0dc116ef3e38a52d0f81d))
+ Results reproduced by [@rootofallevii](https://github.com/rootofallevii) on 2021-05-14 (commit [`e764797`](https://github.com/castorini/pyserini/commit/e764797081eebf487fa7e1fa34872a59ff97fdf7))
+ Results reproduced by [@jpark621](https://github.com/jpark621) on 2021-06-13 (commit [`f614111`](https://github.com/castorini/pyserini/commit/f614111f014b7490f75e585e610f64f769164dd2))
+ Results reproduced by [@nimasadri11](https://github.com/nimasadri11) on 2021-06-28 (commit [`d31e2e6`](https://github.com/castorini/pyserini/commit/d31e2e67984f3a8285589fb162080ac9570fcbe7))
+ Results reproduced by [@mzzchy](https://github.com/mzzchy) on 2021-07-05 (commit [`45083f5`](https://github.com/castorini/pyserini/commit/45083f5ecb986651301c1fe26d09981d0baee8ee))
+ Results reproduced by [@d1shs0ap](https://github.com/d1shs0ap) on 2021-07-16 (commit [`a6b6545`](https://github.com/castorini/pyserini/commit/a6b6545c0133c03d50d5c33fb2fea7c527de04bb))
+ Results reproduced by [@apokali](https://github.com/apokali) on 2021-08-19 (commit[`45a2fb4`](https://github.com/castorini/pyserini/commit/45a2fb4bacbbd92f54ff0f98463662cbc09d78bb))
+ Results reproduced by [@leungjch](https://github.com/leungjch) on 2021-09-12 (commit [`c71a69e`](https://github.com/castorini/pyserini/commit/c71a69e2dfad487e492b9b2b3c21b9b9c2e7cdb5))
+ Results reproduced by [@AlexWang000](https://github.com/AlexWang000) on 2021-10-10 (commit [`8599c81`](https://github.com/castorini/pyserini/commit/8599c81a0f0b1c09c32669c26c7e62dec6e4020d))
+ Results reproduced by [@manveertamber](https://github.com/manveertamber) on 2021-12-05 (commit [`c280dad`](https://github.com/castorini/pyserini/commit/c280dad1618c1f985f84fe35bb66aaadcf98131b))
+ Results reproduced by [@lingwei-gu](https://github.com/lingwei-gu) on 2021-12-15 (commit [`7249409`](https://github.com/castorini/pyserini/commit/7249409269095cd65259eb8a7c5131d3b9323068))
+ Results reproduced by [@tyao-t](https://github.com/tyao-t) on 2021-12-19 (commit [`fc54ed6`](https://github.com/castorini/pyserini/commit/fc54de6725ef1c973831f5c239facb8f03f32ad5))
+ Results reproduced by [@kevin-wangg](https://github.com/kevin-wangg) on 2022-01-05 (commit [`b9fcae7`](https://github.com/castorini/pyserini/commit/b9fcae7994fad0d1943f0f8054d84982c23a9954))
+ Results reproduced by [@vivianliu0](https://github.com/vivianliu0) on 2021-01-06 (commit [`937ec63`](https://github.com/castorini/pyserini/commit/937ec63deead4d6743a735d78d381792067469e7))
+ Results reproduced by [@mikhail-tsir](https://github.com/mikhail-tsir) on 2022-01-10 (commit [`f1084a0`](https://github.com/castorini/pyserini/commit/f1084a05a3bf955bdd27acd33f2b95c636b2e5b6))
+ Results reproduced by [@AceZhan](https://github.com/AceZhan) on 2022-01-14 (commit [`68be809`](https://github.com/castorini/pyserini/commit/68be8090b8553fc6eaf352ac690a6de9d3dc82dd))
+ Results reproduced by [@jh8liang](https://github.com/jh8liang) on 2022-02-06 (commit [`e03e068`](https://github.com/castorini/pyserini/commit/e03e06880ad4f6d67a1666c1dd45ce4250adc95d))
+ Results reproduced by [@HAKSOAT](https://github.com/HAKSOAT) on 2022-03-11 (commit [`7796685`](https://github.com/castorini/pyserini/commit/77966851755163e36489544fb08f73171e98103f))
+ Results reproduced by [@jasper-xian](https://github.com/jasper-xian) on 2022-03-27 (commit [`5668edd`](https://github.com/castorini/pyserini/commit/5668edd6f1e61e9c57d600d41d3d1f58b775d371))
+ Results reproduced by [@jx3yang](https://github.com/jx3yang) on 2022-04-25 (commit [`53333e0`](https://github.com/castorini/pyserini/commit/53333e0fb77371e049e24b10da3a20646c7b5af7))
+ Results reproduced by [@alvind1](https://github.com/alvind1) on 2022-05-05 (commit [`244828f`](https://github.com/castorini/pyserini/commit/244828f6d6d70a7405e0906a700a5ce8ef0def15))
+ Results reproduced by [@Pie31415](https://github.com/Pie31415) on 2022-06-20 (commit [`52db3a7`](https://github.com/castorini/pyserini/commit/52db3a7e8087ae351b69d00c9a3fe3450db4b328))
+ Results reproduced by [@aivan6842](https://github.com/aivan6842) on 2022-07-11 (commit [`f553d43`](https://github.com/castorini/pyserini/commit/f553d43e5bd0b5617a002f1ab7861a158d6e2e71))
+ Results reproduced by [@Jasonwu-0803](https://github.com/Jasonwu-0803) on 2022-09-27 (commit [`563e4e7`](https://github.com/castorini/pyserini/commit/563e4e7d0daa2869355952663ed3f68955cdefdc))
+ Results reproduced by [@limelody](https://github.com/limelody) on 2022-10-14 (commit [`40ecc7b`](https://github.com/castorini/pyserini/commit/40ecc7bedd8bf26ae9ac6f0cb0358213ce2182f7))
+ Results reproduced by [@minconszhang](https://github.com/minconszhang) on 2022-11-25 (commit [`a3b0631`](https://github.com/castorini/pyserini/commit/a3b06316594859bc56706b711a68a28b9880f49c))
+ Results reproduced by [@jingliu](https://github.com/ljatca) on 2022-12-08 (commit [`f5a73f0`](https://github.com/castorini/pyserini/commit/f5a73f013d8da6bde8e56e146b1e09ef2c708c29))
+ Results reproduced by [@farazkh80](https://github.com/farazkh80) on 2022-12-18 (commit [`3d8c473`](https://github.com/castorini/pyserini/commit/3d8c4731507c3f30e6a88243e26443c681a5c826))
+ Results reproduced by [@Cath](https://github.com/Cathrineee) on 2023-01-14 (commit [`ec37c5e`](https://github.com/castorini/pyserini/commit/ec37c5e1d02868e7ed73d6293155a6f16f0d9a12))
+ Results reproduced by [@dlrudwo1269](https://github.com/dlrudwo1269) on 2023-03-08 (commit [`dfae4bb5`](https://github.com/castorini/pyserini/commit/dfae4bb5128225e81606acbb17d1d92e254d609f))
+ Results reproduced by [@aryamancodes](https://github.com/aryamancodes) on 2023-04-11 (commit [`1aea2b0`](https://github.com/castorini/pyserini/commit/1aea2b02ccb48e7f9bfe8065657ba57462eb1a47))
+ Results reproduced by [@Jocn2020](https://github.com/Jocn2020) on 2023-05-01 (commit [`ca5a2be`](https://github.com/castorini/pyserini/commit/ca5a2beb7164013e787e0124c7d79b5c751a2d60))
+ Results reproduced by [@zoehahaha](https://github.com/zoehahaha) on 2023-05-12 (commit [`b429218`](https://github.com/castorini/anserini/commit/b429218e52a385eabf3fd81979e221111fbc4a19))
+ Results reproduced by [@Richard5678](https://github.com/richard5678) on 2023-06-14 (commit [`b713dea`](https://github.com/castorini/pyserini/commit/b713dea93e6c52bb372f482afde296cb45483084))
+ Results reproduced by [@pratyushpal](https://github.com/pratyushpal) on 2023-07-14 (commit [`760c22a`](https://github.com/castorini/pyserini/commit/760c22a3300a4fc3bfc83991140cdc1d6d7a35f9))
+ Results reproduced by [@br0mabs](https://github.com/br0mabs) on 2023-07-25 (commit [`44889de`](https://github.com/castorini/pyserini/commit/44889de3d151b2e1317934b405b3ad6badd81308))

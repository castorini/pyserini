# Pyserini: BM25 Baseline for MS MARCO Passage Ranking

This guide contains instructions for running a BM25 baseline on the [MS MARCO *passage* ranking task](https://microsoft.github.io/msmarco/), which is nearly identical to a [similar guide in Anserini](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md), except that everything is in Python here (no Java).
Note that there is a separate guide for the [MS MARCO *document* ranking task](experiments-msmarco-doc.md).
This exercise will require a machine with >8 GB RAM and >15 GB free disk space.

If you're a Waterloo student traversing the [onboarding path](https://github.com/lintool/guide/blob/master/ura.md) (which [starts here](https://github.com/castorini/anserini/blob/master/docs/start-here.md)),
make sure you've already done the [BM25 Baselines for MS MARCO Passage Ranking **in Anserini**](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md).
In general, don't try to rush through this guide by just blindly copying and pasting commands into a shell;
that's what I call [cargo culting](https://en.wikipedia.org/wiki/Cargo_cult_programming).
Instead, really try to understand what's going on.

**Learning outcomes** for this guide, building on previous steps in the onboarding path:

+ Be able to use Pyserini to build a Lucene inverted index on the MS MARCO passage collection.
+ Be able to use Pyserini to perform a batch retrieval run on the MS MARCO passage collection with the dev queries.
+ Be able to evaluate the retrieved results above.
+ Be able to generate the retrieved results above _interactively_ by directly manipulating Pyserini Python classes.

In short, you'll do everything you did with Anserini (in Java) on the MS MARCO passage ranking test collection, but now with Pyserini (in Python).

What's Pyserini?
Well, it's the repo that you're in right now.
Pyserini is a Python toolkit for reproducible information retrieval research with sparse and dense representations.
The toolkit provides Python bindings for our group's [Anserini IR toolkit](http://anserini.io/), which is built on Lucene (in Java).
Pyserini provides entrée into the broader deep learning ecosystem, which is heavily Python-centric.

## Data Prep

The guide requires the [development installation](https://github.com/castorini/pyserini/blob/master/docs/installation.md#development-installation).
So get your Python environment set up.

Once you've done that: congratulations, you've passed the most difficult part!
Everything else below mirrors what you did in Anserini (in Java), so it should be easy.

We're going to use `collections/msmarco-passage/` as the working directory.
First, we need to download and extract the MS MARCO passage dataset:

```bash
mkdir collections/msmarco-passage

wget https://msmarco.blob.core.windows.net/msmarcoranking/collectionandqueries.tar.gz -P collections/msmarco-passage

# Alternative mirror:
# wget https://www.dropbox.com/s/9f54jg2f71ray3b/collectionandqueries.tar.gz -P collections/msmarco-passage

tar xvfz collections/msmarco-passage/collectionandqueries.tar.gz -C collections/msmarco-passage
```

To confirm, `collectionandqueries.tar.gz` should have MD5 checksum of `31644046b18952c1386cd4564ba2ae69`.

Next, we need to convert the MS MARCO tsv collection into Pyserini's jsonl files (which have one json object per line):

```bash
python tools/scripts/msmarco/convert_collection_to_jsonl.py \
 --collection-path collections/msmarco-passage/collection.tsv \
 --output-folder collections/msmarco-passage/collection_jsonl
```

The above script should generate 9 jsonl files in `collections/msmarco-passage/collection_jsonl`, each with 1M lines (except for the last one, which should have 841,823 lines).

## Indexing

We can now index these documents as a `JsonCollection` using Pyserini:

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/msmarco-passage/collection_jsonl \
  --index indexes/lucene-index-msmarco-passage \
  --generator DefaultLuceneDocumentGenerator \
  --threads 9 \
  --storePositions --storeDocvectors --storeRaw
```

The command-line invocation should look familiar: it essentially mirrors the command with Anserini (in Java).
If you can't make sense of what's going on here, back up and make sure you've first done the [BM25 Baselines for MS MARCO Passage Ranking **in Anserini**](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md).

Upon completion, you should have an index with 8,841,823 documents.
The indexing speed may vary; on a modern desktop with an SSD, indexing takes a couple of minutes.

## Retrieval

The 6980 queries in the development set are already stored in the repo.
Let's take a peek:

```bash
$ head tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt
1048585	what is paula deen's brother
2	 Androgen receptor define
524332	treating tension headaches without medication
1048642	what is paranoid sc
524447	treatment of varicose veins in legs
786674	what is prime rate in canada
1048876	who plays young dr mallard on ncis
1048917	what is operating system misconfiguration
786786	what is priority pass
524699	tricare service number

$ wc tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt
    6980   48335  290193 tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt
```

Each line contains a tab-delimited (query id, query) pair.
Conveniently, Pyserini already knows how to load and iterate through these pairs.
We can now perform retrieval using these queries:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index-msmarco-passage \
  --topics msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.bm25tuned.txt \
  --output-format msmarco \
  --hits 1000 \
  --bm25 --k1 0.82 --b 0.68 \
  --threads 4 --batch-size 16
```

Here, we set the BM25 parameters to `k1=0.82`, `b=0.68` (tuned by grid search).
The option `--output-format msmarco` says to generate output in the MS MARCO output format.
The option `--hits` specifies the number of documents to return per query.
Thus, the output file should have approximately 6980 × 1000 = 6.9M lines.

Once again, if you can't make sense of what's going on here, back up and make sure you've first done the [BM25 Baselines for MS MARCO Passage Ranking **in Anserini**](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md).

Retrieval speed will vary by hardware:
On a reasonably modern CPU with an SSD, we might get around 13 qps (queries per second), and so the entire run should finish in under ten minutes (using a single thread).
We can perform multi-threaded retrieval by using the `--threads` and `--batch-size` arguments.
For example, setting `--threads 16 --batch-size 64` on a CPU with sufficient cores, the entire run will finish in a couple of minutes.

## Evaluation

After the run finishes, we can evaluate the results using the official MS MARCO evaluation script, which has been incorporated into Pyserini:

```bash
$ python -m pyserini.eval.msmarco_passage_eval \
   tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
   runs/run.msmarco-passage.bm25tuned.txt

#####################
MRR @10: 0.18741227770955546
QueriesRanked: 6980
#####################
```

We can also use the official TREC evaluation tool, `trec_eval`, to compute metrics other than MRR@10.

The tool needs a different run format, so it's easier to just run retrieval again:

```bash
python -m pyserini.search.lucene \
  --index indexes/lucene-index-msmarco-passage \
  --topics msmarco-passage-dev-subset \
  --output runs/run.msmarco-passage.bm25tuned.trec \
  --hits 1000 \
  --bm25 --k1 0.82 --b 0.68 \
  --threads 4 --batch-size 16
```

The only difference here is that we've removed `--output-format msmarco`.

Then, convert qrels files to the TREC format:

```bash
python tools/scripts/msmarco/convert_msmarco_to_trec_qrels.py \
  --input collections/msmarco-passage/qrels.dev.small.tsv \
  --output collections/msmarco-passage/qrels.dev.small.trec
```

Finally, run the `trec_eval` tool, which has been incorporated into Pyserini:

```bash
$ python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap \
   collections/msmarco-passage/qrels.dev.small.trec \
   runs/run.msmarco-passage.bm25tuned.trec

map                   	all	0.1957
recall_1000           	all	0.8573
```

If you want to examine the MRR@10 for `qid` 1048585:

```bash
$ python -m pyserini.eval.trec_eval -q -c -M 10 -m recip_rank \
    collections/msmarco-passage/qrels.dev.small.trec \
    runs/run.msmarco-passage.bm25tuned.trec | grep 1048585

recip_rank            	1048585	1.0000
```

Once again, if you can't make sense of what's going on here, back up and make sure you've first done the [BM25 Baselines for MS MARCO Passage Ranking **in Anserini**](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md).

Otherwise, congratulations!
You've done everything that you did in Anserini (in Java), but now in Pyserini (in Python).

## Interactive Retrieval

There's one final thing we should go over.
Because we're in Python now, we get the benefit of having an interactive shell.
Thus, we can run Pyserini interactively.

Try the following:

```python
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/lucene-index-msmarco-passage')
searcher.set_bm25(0.82, 0.68)
hits = searcher.search('what is paula deen\'s brother')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')
```

The `LuceneSearcher` class provides search capabilities for BM25.
In the code snippet above, we're issuing the query about Paula Deen's brother (from above).
Note that we're explicitly setting the BM25 parameters, which are not the default parameters.
We get back a list of results (`hits`), which we then iterate through and print out:

```
 1 7187158 18.811600
 2 7187157 18.333401
 3 7187163 17.878799
 4 7546327 16.962099
 5 7187160 16.564699
 6 8227279 16.432501
 7 7617404 16.239901
 8 7187156 16.024900
 9 2298838 15.701500
10 7187155 15.513300
```

You can confirm that the output is the same as `pyserini.search.lucene` from above.

```bash
$ grep 1048585 runs/run.msmarco-passage.bm25tuned.trec | head -10
1048585 Q0 7187158 1 18.811600 Anserini
1048585 Q0 7187157 2 18.333401 Anserini
1048585 Q0 7187163 3 17.878799 Anserini
1048585 Q0 7546327 4 16.962099 Anserini
1048585 Q0 7187160 5 16.564699 Anserini
1048585 Q0 8227279 6 16.432501 Anserini
1048585 Q0 7617404 7 16.239901 Anserini
1048585 Q0 7187156 8 16.024900 Anserini
1048585 Q0 2298838 9 15.701500 Anserini
1048585 Q0 7187155 10 15.513300 Anserini
```

To pull up the actual contents of a hit:

```python
hits[0].lucene_document.get('raw')
```

And you should get:

```
'{\n  "id" : "7187158",\n  "contents" : "Paula Deen and her brother Earl W. Bubba Hiers are being sued by a former general manager at Uncle Bubba\'sâ\x80¦ Paula Deen and her brother Earl W. Bubba Hiers are being sued by a former general manager at Uncle Bubba\'sâ\x80¦"\n}'
```

Everything make sense?
If so, now you're truly done with this guide and are ready to move on and [learn about the relationship between sparse and dense retrieval](conceptual-framework.md)!

Before you move on, however, add an entry in the "Reproduction Log" at the bottom of this page, following the same format: use `yyyy-mm-dd`, make sure you're using a commit id that's on the main trunk of Pyserini, and use its 7-hexadecimal prefix for the link anchor text.

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@JeffreyCA](https://github.com/JeffreyCA) on 2020-09-14 (commit [`49fd7cb`](https://github.com/castorini/pyserini/commit/49fd7cb8fd802493dc34f5cb33767d2e72e19f13))
+ Results reproduced by [@jhuang265](https://github.com/jhuang265) on 2020-09-14 (commit [`2ed2acc`](https://github.com/castorini/pyserini/commit/2ed2acc62e445e3e887c6cf853ccc0b0b3b57534))
+ Results reproduced by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2020-11-11 (commit [`8172015`](https://github.com/Dahlia-Chehata/pyserini/commit/817201553d790c8b53a3aef17ed87721a9d35595))
+ Results reproduced by [@rakeeb123](https://github.com/rakeeb123) on 2020-12-07 (commit [`3bcd4e5`](https://github.com/castorini/pyserini/commit/3bcd4e52beb327d55ae6d3c8f6bc94351a6d1449))
+ Results reproduced by [@jrzhang12](https://github.com/jrzhang12) on 2021-01-03 (commit [`7caedfc`](https://github.com/castorini/pyserini/commit/7caedfc150f916de302297406c45dead27b475ba))
+ Results reproduced by [@HEC2018](https://github.com/HEC2018) on 2021-01-04 (commit [`46a6d47`](https://github.com/castorini/pyserini/commit/46a6d472267a559152495d004c2a12f8e95e53f0))
+ Results reproduced by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-08 (commit [`aeec31f`](https://github.com/castorini/pyserini/commit/aeec31fbe17d39ecf3081597b4832f5af57ea549))
+ Results reproduced by [@yemiliey](https://github.com/yemiliey) on 2021-01-18 (commit [`98f3236`](https://github.com/castorini/pyserini/commit/98f323659c8a0a5d8ef26bb3f6768458a34e3eb9))
+ Results reproduced by [@larryli1999](https://github.com/larryli1999) on 2021-01-22 (commit [`74a87e4`](https://github.com/castorini/pyserini/commit/74a87e4951c98d7b066273140576d3cccd9ea0ed))
+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-04-08 (commit [`7261223`](https://github.com/castorini/pyserini/commit/72612232bc886e71e8de9431a899a7c68f1d82c7))
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
+ Results reproduced by [@HAKSOAT](https://github.com/HAKSOAT) on 2022-03-10 (commit [`7796685`](https://github.com/castorini/pyserini/commit/77966851755163e36489544fb08f73171e98103f))
+ Results reproduced by [@jasper-xian](https://github.com/jasper-xian) on 2022-03-27 (commit [`5668edd`](https://github.com/castorini/pyserini/commit/5668edd6f1e61e9c57d600d41d3d1f58b775d371))
+ Results reproduced by [@jx3yang](https://github.com/jx3yang) on 2022-04-25 (commit [`53333e0`](https://github.com/castorini/pyserini/commit/53333e0fb77371e049e24b10da3a20646c7b5af7))
+ Results reproduced by [@alvind1](https://github.com/alvind1) on 2022-05-04 (commit [`244828f`](https://github.com/castorini/pyserini/commit/244828f6d6d70a7405e0906a700a5ce8ef0def15))
+ Results reproduced by [@Pie31415](https://github.com/Pie31415) on 2022-06-20 (commit [`52db3a7`](https://github.com/castorini/pyserini/commit/52db3a7e8087ae351b69d00c9a3fe3450db4b328))
+ Results reproduced by [@aivan6842](https://github.com/aivan6842) on 2022-07-11 (commit [`f553d43`](https://github.com/castorini/pyserini/commit/f553d43e5bd0b5617a002f1ab7861a158d6e2e71))
+ Results reproduced by [@Jasonwu-0803](https://github.com/Jasonwu-0803) on 2022-09-27 (commit [`563e4e7`](https://github.com/castorini/pyserini/commit/563e4e7d0daa2869355952663ed3f68955cdefdc))
+ Results reproduced by [@limelody](https://github.com/limelody) on 2022-09-27 (commit [`7b53918`](https://github.com/castorini/pyserini/commit/7b5391864897df4523b34a4943ce08d7e373dbe7))
+ Results reproduced by [@minconszhang](https://github.com/minconszhang) on 2022-11-25 (commit [`a3b0631`](https://github.com/castorini/pyserini/commit/a3b06316594859bc56706b711a68a28b9880f49c))
+ Results reproduced by [@jingliu](https://github.com/ljatca) on 2022-12-08 (commit [`f5a73f0`](https://github.com/castorini/pyserini/commit/f5a73f013d8da6bde8e56e146b1e09ef2c708c29))
+ Results reproduced by [@farazkh80](https://github.com/farazkh80) on 2022-12-18 (commit [`3d8c473`](https://github.com/castorini/pyserini/commit/3d8c4731507c3f30e6a88243e26443c681a5c826))
+ Results reproduced by [@Cath](https://github.com/Cathrineee) on 2023-01-14 (commit [`ec37c5e`](https://github.com/castorini/pyserini/commit/ec37c5e1d02868e7ed73d6293155a6f16f0d9a12))
+ Results reproduced by [@dlrudwo1269](https://github.com/dlrudwo1269) on 2023-03-08 (commit [`dfae4bb5`](https://github.com/castorini/pyserini/commit/dfae4bb5128225e81606acbb17d1d92e254d609f))
+ Results reproduced by [@aryamancodes](https://github.com/aryamancodes) on 2023-04-11 (commit [`1aea2b0`](https://github.com/castorini/pyserini/commit/1aea2b02ccb48e7f9bfe8065657ba57462eb1a47))
+ Results reproduced by [@Jocn2020](https://github.com/Jocn2020) on 2023-05-01 (commit [`ca5a2be`](https://github.com/castorini/pyserini/commit/ca5a2beb7164013e787e0124c7d79b5c751a2d60))
+ Results reproduced by [@zoehahaha](https://github.com/zoehahaha) on 2023-05-12 (commit [`68be809`](https://github.com/castorini/pyserini/commit/68be8090b8553fc6eaf352ac690a6de9d3dc82dd))
+ Results reproduced by [@Richard5678](https://github.com/richard5678) on 2023-06-13 (commit [`ccb6df5`](https://github.com/castorini/pyserini/commit/ccb6df50f37590b861e960989d98450b6de43850))
+ Results reproduced by [@pratyushpal](https://github.com/pratyushpal) on 2023-07-14 (commit [`760c22a`](https://github.com/castorini/pyserini/commit/760c22a3300a4fc3bfc83991140cdc1d6d7a35f9))
+ Results reproduced by [@sahel-sh](https://github.com/sahel-sh) on 2023-07-22 (commit [`863ff361`](https://github.com/castorini/pyserini/commit/863ff361fd671bb79b07f8f89a4b8121b7b46e8e))
+ Results reproduced by [@yilinjz](https://github.com/yilinjz) on 2023-08-25 (commit [`b57b583`](https://github.com/castorini/pyserini/commit/b57b5838bcb48ecbc478302d364eace787cc1b6f))
+ Results reproduced by [@Andrwyl](https://github.com/Andrwyl) on 2023-08-26 (commit [`0b3ec90`](https://github.com/castorini/pyserini/commit/0b3ec904376d207a36f809944108720c49ff8ce1))
+ Results reproduced by [@UShivani3](https://github.com/UShivani3) on 2023-08-29 (commit [`d9da49e`](https://github.com/castorini/pyserini/commit/d9da49eb3a23fb9daa26399a2e27a5efc73beb71))
+ Results reproduced by [@Edward-J-Xu](https://github.com/Edward-J-Xu) on 2023-09-04 (commit [`8063322`](https://github.com/castorini/pyserini/commit/806332286d6eacea23061c04205a71698e6a6208))
+ Results reproduced by [@mchlp](https://github.com/mchlp) on 2023-09-07 (commit [`d8dc5b3`](https://github.com/castorini/pyserini/commit/d8dc5b3a1f32fd5d0cebeb711ba148ea967fadbe))
+ Results reproduced by [@lucedes27](https://github.com/lucedes27) on 2023-09-10 (commit [`54014af`](https://github.com/castorini/pyserini/commit/54014af8fe4bf4ba75daba9119acac94c7191cdb))
+ Results reproduced by [@MojTabaa4](https://github.com/MojTabaa4) on 2023-09-14 (commit [`d4a829d`](https://github.com/castorini/pyserini/commit/d4a829d18043783ef3dec2a8adce50e4061ba99a))
+ Results reproduced by [@Kshama](https://github.com/Kshama33) on 2023-09-24 (commit [`7d18f4b`](https://github.com/castorini/pyserini/commit/7d18f4bd3f98d4f901dc061ffd93a1c656e32d0d))
+ Results reproduced by [@MelvinMo](https://github.com/MelvinMo) on 2023-09-24 (commit [`7d18f4b`](https://github.com/castorini/pyserini/commit/7d18f4bd3f98d4f901dc061ffd93a1c656e32d0d))
+ Results reproduced by [@ksunisth](https://github.com/ksunisth) on 2023-09-27 (commit [`142c774`](https://github.com/castorini/pyserini/commit/142c774a303c906ee245913bc7e714b165074b77))
+ Results reproduced by [@maizerrr](https://github.com/maizerrr) on 2023-10-01 (commit [`bdb9504`](https://github.com/castorini/pyserini/commit/bdb9504b1757ab88247924b55a8fde3e5c1a3d20))
+ Results reproduced by [@Stefan824](https://github.com/stefan824) on 2023-10-04 (commit [`4f3da10`](https://github.com/castorini/pyserini/commit/4f3da10b99341d0bc2729590c23d9f1654d8ee37))
+ Results reproduced by [@shayanbali](https://github.com/shayanbali) on 2023-10-13 (commit [`f889bc4`](https://github.com/castorini/pyserini/commit/f889bc40665952f1698f4bd131bc0093276e279c))
+ Results reproduced by [@gituserbs](https://github.com/gituserbs) on 2023-10-18 (commit [`f1d623c`](https://github.com/castorini/pyserini/commit/f1d623cdcb12c3083ff1db8aed4b84e81951a18c))
+ Results reproduced by [@shakibaam](https://github.com/shakibaam) on 2023-11-04 (commit [`01889cc`](https://github.com/castorini/pyserini/commit/01889ccb40c5dcc2c6baf629f58db4e6004eeddf))
+ Results reproduced by [@gitHubAndyLee2020](https://github.com/gitHubAndyLee2020) on 2023-11-05 (commit [`01889cc`](https://github.com/castorini/pyserini/commit/01889ccb40c5dcc2c6baf629f58db4e6004eeddf))
+ Results reproduced by [@Melissa1412](https://github.com/Melissa1412) on 2023-11-05 (commit [`acd969f`](https://github.com/castorini/pyserini/commit/acd969f8f234126c272d70d55d047a3804b52ff8))
+ Results reproduced by [@aliranjbari](https://github.com/aliranjbari) on 2023-11-08 (commit [`12cbb11`](https://github.com/castorini/pyserini/commit/12cbb11efbf1d82c2be84bc376e1aceffcaced31))
+ Results reproduced by [@salinaria](https://github.com/salinaria) on 2023-11-11 (commit [`086e16b`](https://github.com/castorini/pyserini/commit/086e16be28b7dc6022f8582dbd803824dc2c1ad2))
+ Results reproduced by [@oscarbelda86](https://github.com/oscarbelda86) on 2023-11-13 (commit [`086e16b`](https://github.com/castorini/pyserini/commit/086e16be28b7dc6022f8582dbd803824dc2c1ad2))
+ Results reproduced by [@Seun-Ajayi](https://github.com/Seun-Ajayi) on 2023-11-13 (commit [`086e16b`](https://github.com/castorini/pyserini/commit/086e16be28b7dc6022f8582dbd803824dc2c1ad2))
+ Results reproduced by [@AndreSlavescu](https://github.com/AndreSlavescu) on 2023-11-28 (commit [`1219cdb`](https://github.com/castorini/pyserini/commit/1219cdbca780e869ba77658c29e1aaa972585d09))
+ Results reproduced by [@tudou0002](https://github.com/tudou0002) on 2023-11-28 (commit [`723e06c`](https://github.com/castorini/pyserini/commit/723e06c3b04e6c6fcd56fcf5bce4386c72503e5a))
+ Results reproduced by [@golnooshasefi](https://github.com/golnooshasefi) on 2023-11-28 (commit [`1219cdb`](https://github.com/castorini/pyserini/commit/1219cdbca780e869ba77658c29e1aaa972585d09))
+ Results reproduced by [@alimt1992](https://github.com/alimt1992) on 2023-11-29 (commit [`e6700f6`](https://github.com/castorini/pyserini/commit/e6700f6a1bca7d2bea81fb40d9c3ae63c1be142a))
+ Results reproduced by [@sueszli](https://github.com/sueszli) on 2023-12-01 (commit [`170e271`](https://github.com/castorini/pyserini/commit/170e271bb8c863b7a45499190bcb8b6b8cfa27f0))
+ Results reproduced by [@kdricci](https://github.com/kdricci) on 2023-12-01 (commit [`a2049c4`](https://github.com/castorini/pyserini/commit/a2049c49124228fe41192a848ec49fbaf391ebee))
+ Results reproduced by [@ljk423](https://github.com/ljk423) on 2023-12-04 (commit [`35002ad`](https://github.com/castorini/pyserini/commit/35002ad21ecb408ced2a96eb09f3a85fc02475ce))
+ Results reproduced by [@saharsamr](https://github.com/saharsamr) on 2023-12-14 (commit [`039c137`](https://github.com/castorini/pyserini/commit/039c137055c429d662544303546d8e225d159be8))
+ Results reproduced by [@Panizghi](https://github.com/Panizghi) on 2023-12-17 (commit [`0f5db95`](https://github.com/castorini/pyserini/commit/0f5db95dbd5ed6b983ac4f638b486a70bc5ea99a))
+ Results reproduced by [@AreelKhan](https://github.com/AreelKhan) on 2023-12-22 (commit [`f75adca`](https://github.com/castorini/pyserini/commit/f75adca8c410e64b3ff1375e181a0ea3af1ddb28))
+ Results reproduced by [@wu-ming233](https://github.com/wu-ming233) on 2023-12-31 (commit [`38a571f`](https://github.com/castorini/pyserini/commit/38a571fb2a61d61d9245997b5d0f8cd64550912c))
+ Results reproduced by [@Yuan-Hou](https://github.com/Yuan-Hou) on 2024-01-02 (commit [`38a571f`](https://github.com/castorini/pyserini/commit/38a571fb2a61d61d9245997b5d0f8cd64550912c))
+ Results reproduced by [@himasheth](https://github.com/himasheth) on 2024-01-10 (commit [`a6ed27e`](https://github.com/castorini/pyserini/commit/a6ed27ec5c9138ea2686d9079909ca7b2fed9d90))
+ Results reproduced by [@Tanngent](https://github.com/Tanngent) on 2024-01-13 (commit [`57a00cf`](https://github.com/castorini/pyserini/commit/57a00cfa6c1201a57eeda13512fee37d72afa348))
+ Results reproduced by [@BeginningGradeMaker](https://github.com/BeginningGradeMaker) on 2024-01-15 (commit [`d4ea011`](https://github.com/castorini/pyserini/commit/d4ea01125ed5d744abc276e70c337e3be1ace260))


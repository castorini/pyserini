# Direct PyPI Package Replication

It's easy to replicate runs on many "standard" IR test collections directly from the PyPI package (i.e., with only `pip install`)!

## Robust04

BM25 baseline from the [TREC 2004 Robust Track](https://github.com/castorini/anserini/blob/master/docs/regressions-robust04.md) on TREC Disks 4 &amp; 5: 

```bash
$ python -m pyserini.search --topics robust04 --index robust04 --output run.robust04.txt --bm25
```

That's it!

A dependency-free way to evaluate the run:

```
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.robust04.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -m P.30 qrels.robust04.txt run.robust04.txt
map                   	all	0.2531
P_30                  	all	0.3102
```

## MS MARCO Passage Ranking

MS MARCO passage ranking task, BM25 baseline:

```bash
$ python -m pyserini.search --topics msmarco_passage_dev_subset --index ms-marco-passage --output run.msmarco-passage.txt --bm25
```

To evaluate:

```bash
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -c -m recall.1000 -c qrels.msmarco-passage.dev-subset.txt run.msmarco-passage.txt
map                   	all	0.1926
recall_1000           	all	0.8526
```

MS MARCO passage ranking task, BM25 baseline with [docTTTTTquery expansions](http://doc2query.ai/):

```bash
$ python -m pyserini.search --topics msmarco_passage_dev_subset --index ms-marco-passage-expanded --output run.msmarco-passage.expanded.txt --bm25
```

To evaluate:

```bash
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -c -m recall.1000 -c qrels.msmarco-passage.dev-subset.txt run.msmarco-passage.expanded.txt
map                   	all	0.2805
recall_1000           	all	0.9470
```

## MS MARCO Document Ranking

MS MARCO document ranking task, BM25 baseline:

```bash
$ python -m pyserini.search --topics msmarco_doc_dev --index ms-marco-doc --output run.msmarco-doc.txt --bm25
```

To evaluate:

```bash
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.msmarco-doc.dev.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -m recall.1000 qrels.msmarco-doc.dev.txt run.msmarco-doc.txt
map                   	all	0.2310
recall_1000           	all	0.8856
```

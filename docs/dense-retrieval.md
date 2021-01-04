# Direct PyPI Package Replication on Dense Retrieval

It's easy to replicate runs on many "standard" IR test collections directly from the PyPI package (i.e., with only `pip install`)!

## MS MARCO Passage Ranking

MS MARCO passage ranking task, dense retrieval with TCT-ColBERT, HNSW index.
```bash
$ python -m pyserini.dsearch --topics msmarco_passage_dev_subset --index msmarco-passage-tct_colbert-hnsw --query_emb msmarco-passage-dev-subset-tct_colbert --output run.msmarco-passage.tct_colbert.hnsw.txt
```

To evaluate:

```bash
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -c -m recall.1000 -c qrels.msmarco-passage.dev-subset.txt run.msmarco-passage.tct_colbert.hnsw.txt
map                   	all	0.3408
recall_1000           	all	0.9618
```

MS MARCO passage ranking task, dense retrieval with TCT-ColBERT, brute force index.
```bash
$ python -m pyserini.dsearch --topics msmarco_passage_dev_subset --index msmarco-passage-tct_colbert-bf --query_emb msmarco-passage-dev-subset-tct_colbert --batch 48  --output run.msmarco-passage.tct_colbert.bf.txt
```

To evaluate:

```bash
$ wget -O jtreceval-0.0.5-jar-with-dependencies.jar https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar
$ wget https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt
$ java -jar jtreceval-0.0.5-jar-with-dependencies.jar -m map -c -m recall.1000 -c qrels.msmarco-passage.dev-subset.txt run.msmarco-passage.tct_colbert.bf.txt
map                   	all	0.3412
recall_1000           	all	0.9637
```
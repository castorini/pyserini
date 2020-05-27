# Pyserini Release Notes (v0.9.3.0)

**Release date: May 27, 2020**

+ Implemented pseudo-relevance classifier reranking technique.
+ Added `TfidfVectorizer` to obtain vector representations of arbitrary documents from index. Verified that class works as expected by replicating [classification demo on 20 Newsgroups with scikit-learn](https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html).
+ Added bindings to TREC COVID round 3 topics.
+ Added script for CORD-19 length outlier detection.
+ Added `__main__` to `pyserini.search` to perform TREC runs from the command line.
+ Fixed issues with computing BM25 term weights and query-document scores.
+ Exposed access to basic index statistics in `IndexReaderUtils`.

## Contributors (This Release)

Sorted by number of commits:

+ Johnson Han ([x65han](https://github.com/x65han))
+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Tim Hatch ([thatch](https://github.com/thatch))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))

## All Contributors

Sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Tommaso Teofili ([tteofili](https://github.com/tteofili))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Tim Hatch ([thatch](https://github.com/thatch))
+ Rodrigo Nogueira ([rodrigonogueira4](https://github.com/rodrigonogueira4))
+ Alireza Mirzaeiyan ([amirzaeiyan](https://github.com/amirzaeiyan))

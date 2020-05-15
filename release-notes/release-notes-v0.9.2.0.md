# Pyserini Release Notes (v0.9.2.0)

**Release date: May 15, 2020**

+ Refactored `SimpleSearcher` to keep up with underlying changes in Anserini.
+ Exposed `num_docs` in `SimpleSearcher`.
+ Exposed Lucene query building blocks in `pyquerybuilder`.
+ Exposed options for setting BM25 parameters when computing BM25 term weights in `IndexReaderUtils`.
+ Added `Cord19Article` to provide support for manipulating CORD-19 articles in `pycollection`.
+ Added documentation for reading CORD-19 via the Collection API; supports data drop of 2020/05/12.
+ Known issue: new methods for computing query-document scores have not be properly "wired up" in Pyserini yet.

## Contributors (This Release)

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))

## All Contributors

Sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Tommaso Teofili ([tteofili](https://github.com/tteofili))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Rodrigo Nogueira ([rodrigonogueira4](https://github.com/rodrigonogueira4))
+ Alireza Mirzaeiyan ([amirzaeiyan](https://github.com/amirzaeiyan))

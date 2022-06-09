# Pyserini Release Notes (v0.17.0)

**Release date: May 28, 2022**

+ Released "two-click reproductions" to match experiments in SIGIR 2022 paper.
+ Refactored computation of judged@k in `trec_eval`, use `-m judged.10,100,1000`.
+ Installed pre-built indexes for MS MARCO V1/V2 doc2query-T5 with docvectors to support relevance feedback.
+ Cleaned up package reorganization of `pyserini.search`.
+ Added support for quantizing term vectors weights (e.g., BM25).
+ Added integration tests based on pre-built baselines for Robust04, MS MARCO V1 doc/passage.
+ Added integration tests for Mr.TyDi, untied mDPR based on NQ.

## Contributors (This Release)

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))

## All Contributors

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))

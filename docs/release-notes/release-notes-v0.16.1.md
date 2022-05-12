# Pyserini Release Notes (v0.16.1)

**Release date: May 12, 2022**

+ Installed pre-built indexes:
  + BEIR (v1.0.0): "flat" baseline, "multfield" baseline, and SPLADE-distill CoCodenser-medium.
  + MS MARCO V1/V2 segmented doc condition (updated indexes).
  + MS MARCO V1 doc/passage uniCOIL noexp.
+ Created initial repro-matrix for MS MARCO V1/V2 doc/passage.
+ Improved indexing util for encoding a corpus.
+ Added util to dump out BM25 document vectors from a corpus.
+ Added bindings to new Anserini feature: multi-threaded method to fetch raw documents from index in batch.
+ Added option in `trec_eval` to compute metrics with unjudged docs removed and to computed judged@k.
+ Added IRST retrieval model, with integration tests.
+ Added `SimpleGeoSearcher`.
+ Refactored LTR pipeline, improved documentation.
+ Refactored `IndexReader`, moved from `pyserini.index` to `pyserini.index.lucene`.
+ Refactored Vector-PRF implementation and added negative PRF passages for Rocchio.
+ Refactored code for loading topics and qrels.
+ Updated documentation for dense encoding.

## Contributors (This Release)

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Nandan Thakur ([NThakur20](https://github.com/NThakur20))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ Yuqing Xie ([amyxie361](https://github.com/amyxie361))
+ Matt Yang ([d1shs0ap](https://github.com/d1shs0ap))
+ Ji Xi Yang ([jx3yang](https://github.com/jx3yang))
+ Vivian Liu ([vivianliu0](https://github.com/vivianliu0))
+ vjeronymo2 ([vjeronymo2](https://github.com/vjeronymo2))
+ xiaoyu ([XY2323819551](https://github.com/XY2323819551))

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
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))

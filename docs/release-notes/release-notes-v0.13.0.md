# Pyserini Release Notes (v0.13.0)

**Release date: July 3, 2021**

+ Added dense retrieval support for DistilBERT TAS-B, TCT-ColBERTv2, and BPR.
+ Added integration tests for DistilBERT TAS-B and TCT-ColBERTv2.
+ Added bindings for `nmslib` in `pyserini.vsearch`.
+ Added reproduction guide for TripClick collection.
+ Added integration tests for TREC-COVID rounds 3, 4, and 5.
+ Added interactive demo.
+ Added script to rerank MS MARCO doc Indri baseline with BM25 MaxP and ANCE MaxP.
+ Improved support for non-English languages.
+ Refactored LTR reranking pipeline for MS MARCO passage.
+ Refactored JVM initialization to allow other jars to be loaded.
+ Harmonized underlying dependencies.
+ Moved sparse and dense index hosting away from Dropbox, to UWaterloo GitLab and UWaterloo CSCF services.
+ Exposed option to use ASCII term filtering in RM3.
+ Changed Japanese analyzer to kuromoji.

## Contributors (This Release)

Sorted by number of commits:

+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Joel Mackenzie ([JMMackenzie](https://github.com/JMMackenzie))
+ Jingtao Zhan ([jingtaozhan](https://github.com/jingtaozhan))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Cash Costello ([cash](https://github.com/cash))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ David Duan ([RootofalleviI](https://github.com/RootofalleviI))
+ Ian Soboroff ([isoboroff](https://github.com/isoboroff))
+ Jin Park ([jpark621](https://github.com/jpark621)) 
+ Kelechi Ogueji ([keleog](https://github.com/keleog))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Xinyan (Velocity) Yu ([velocityCavalry](https://github.com/velocityCavalry))
+ Yu Nakano ([nak6](https://github.com/nak6))
+ Oleg Lesota ([olesota](https://github.com/olesota))
   
## All Contributors

All contributors with more than one commit, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Qing Guo ([qguo96](https://github.com/qguo96))
+ Tommaso Teofili ([tteofili](https://github.com/tteofili))
+ Kai Sun ([KaiSun314](https://github.com/KaiSun314))
+ Hang Cui ([HangCui0510](https://github.com/HangCui0510))
+ Jingtao Zhan ([jingtaozhan](https://github.com/jingtaozhan))
+ Marko Arezina ([mrkarezina](https://github.com/mrkarezina))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Dahlia Chehata ([Dahlia-Chehata](https://github.com/Dahlia-Chehata))
+ Rodrigo Nogueira ([rodrigonogueira4](https://github.com/rodrigonogueira4))
+ David Duan ([RootofalleviI](https://github.com/RootofalleviI))
+ Larry Li ([larryli1999](https://github.com/larryli1999))
+ Jiarui Zhang ([jrzhang12](https://github.com/jrzhang12))
+ Joel Mackenzie ([JMMackenzie](https://github.com/JMMackenzie))
+ Cash Costello ([cash](https://github.com/cash))
+ Oleg Lesota ([olesota](https://github.com/olesota))
+ Yuxuan Ji ([yuxuan-ji](https://github.com/yuxuan-ji))

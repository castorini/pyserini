# Pyserini Release Notes (v0.40.0)

+ **Release date:** October 28, 2024
+ **Anserini dependency:** v0.38.0
+ **Lucene dependency:** v9.9.1

## Summary of Changes

+ Refactored package to reconcile duplicate code in `pyserini.encode` and `pyserini.search.faiss`.
+ Refactored package to clean up warnings.
+ Refactored documentation for various dense models.
+ Started untangling "core" dependencies from "optional" dependencies.
  + "Core" dependencies: `tests/`, `integrations/`
  + "Optional" dependencies: `tests-optional/`, `integrations-optional/`
  + Noteworthy "optional" dependencies include `faiss`, `nmslib`, and `lightgbm`.
+ Added initial bindings for Snowflake's Arctic model.

## Contributors

### This Release

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Ahmed Essam ([AhmedEssam19](https://github.com/AhmedEssam19))
+ Jie Min ([Stefan824](https://github.com/Stefan824))
+ Luke Gallagher ([lgrz](https://github.com/lgrz))
+ Raghav Vasudeva ([Raghav0005](https://github.com/Raghav0005))
+ alirezaJavaheri ([alirezaJvh](https://github.com/alirezaJvh))
+ pxlin-09 ([pxlin-09](https://github.com/pxlin-09))
+ sisixili ([sisixili](https://github.com/sisixili))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Sahel Sharifymoghaddam ([sahel-sh](https://github.com/sahel-sh))
+ Jheng-Hong Yang ([justram](https://github.com/justram))
+ Mofe Adeyemi ([Mofetoluwa](https://github.com/Mofetoluwa))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Ogundepo Odunayo ([ToluClassics](https://github.com/ToluClassics))
+ Catherine Zhou ([Cathrineee](https://github.com/Cathrineee))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Ehsan ([ehsk](https://github.com/ehsk))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))

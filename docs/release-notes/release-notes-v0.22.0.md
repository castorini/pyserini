# Pyserini Release Notes (v0.22.0)

+ **Release date:** August 31, 2023
+ **Anserini dependency:** v0.22.0
+ **Lucene dependency:** v9.5.0

## Summary of Changes

+ Improved `LuceneImpactSearcher`:
  + Ability to parse raw text "on-the-fly" to enable relevance feedback in `SimpleImpactSearcher` in Anserini.
  + Misalignment in code paths between `SearchCollection` and `SimpleImpactSearcher` in Anserini.
+ Improved two-click reproductions:
  + OpenAI `ada` embeddings (new)
  + Aggretriever (new)
  + SLIM (new)
  + SPLADE++ ED/SD (new)
  + Mr.TyDi and MIRACL (updated)
+ Improved documentation and onboarding path.
+ Added hooks to take advantage of "on-the-fly" raw text parsing for base models.
+ Added CIRACL BM25 indexes.
+ Exposed ONNX hooks from Anserini.
+ Refactored prebuilt index info (better organization) and index names (better consistency).

## Contributors

### This Release

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Sahel Sharify ([sahel-sh](https://github.com/sahel-sh))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Aileen Lin ([AileenLin](https://github.com/AileenLin))
+ Bill Cui ([billcui57](https://github.com/billcui57))
+ Mofe Adeyemi ([Mofetoluwa](https://github.com/Mofetoluwa))
+ Zoe Zou ([zoehahaha](https://github.com/zoehahaha))
+ Andrew Drozdov ([mrdrozdov](https://github.com/mrdrozdov))
+ Aryaman Gupta ([aryamancodes](https://github.com/aryamancodes))
+ Ehsan Kamalloo ([ehsk](https://github.com/ehsk))
+ Hannibal046 ([Hannibal046](https://github.com/Hannibal046))
+ Jason Zhang ([yilinjz](https://github.com/yilinjz))
+ Jocn2020 ([Jocn2020](https://github.com/Jocn2020))
+ Jonathan Hilgart ([jonhilgart22](https://github.com/jonhilgart22))
+ Kyung Jae (Jack) Lee ([dlrudwo1269](https://github.com/dlrudwo1269))
+ Morteza Behbooei ([mobehbooei](https://github.com/mobehbooei))
+ Richard Fan ([Richard5678](https://github.com/Richard5678))
+ pratyushpal ([pratyushpal](https://github.com/pratyushpal))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Catherine Zhou ([Cathrineee](https://github.com/Cathrineee))
+ Ogundepo Odunayo ([ToluClassics](https://github.com/ToluClassics))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Matt J. H. Yang ([justram](https://github.com/justram))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))

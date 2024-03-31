# Pyserini Release Notes (v0.25.0)

+ **Release date:** March 31, 2024
+ **Anserini dependency:** v0.25.0
+ **Lucene dependency:** v9.9.1

## Summary of Changes

+ Added `cohere-embed-english-v3.0` 2CRs for MS MARCO v1 passage.
+ Added `BGE-base-en-v1.5` 2CRs for MS MARCO v1 passage and BEIR.
+ Added support for DL22 doc and DL23 doc and passages from MS MARCO v2 and added thier 2CRs.
+ Added initial support for CLIP dense encoder and multimodal retrieval.
+ Added option for users to specify different distance metrics when building Faiss indexes.
+ Refactored and recalibrated 2CR scores, increased tolerance as needed.
+ Refactored method to get topics.
+ Replaced deprecated `pkg_resources` with `importlib.resources` and other deprecation fixes.
+ Updated CIRAL 2CRs.
+ Updated SPLADE 2CRs for BEIR.

## Contributors

### This Release

Sorted by number of commits:

+ Sahel Sharifymoghaddam ([sahel-sh](https://github.com/sahel-sh))
+ Jheng-Hong Yang ([justram](https://github.com/justram))
+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Mofe Adeyemi ([Mofetoluwa](https://github.com/Mofetoluwa))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Ryan Nguyen ([xpbowler](https://github.com/xpbowler))
+ ASChampOmega ([ASChampOmega](https://github.com/ASChampOmega))
+ Alexandru Stan ([AlexStan0](https://github.com/AlexStan0))
+ Amin Haeri ([haeriamin](https://github.com/haeriamin))
+ Danny ([dannychn11](https://github.com/dannychn11))
+ Devesh Marwah ([devesh-002](https://github.com/devesh-002))
+ Ehsan ([ehsk](https://github.com/ehsk))
+ Eric Zhang ([16BitNarwhal](https://github.com/16BitNarwhal))
+ Gavin Wang ([BeginningGradeMaker](https://github.com/BeginningGradeMaker))
+ Ibrahim Ahmed ([ia03](https://github.com/ia03))
+ Jody Zhou ([JodyZ0203](https://github.com/JodyZ0203))
+ Jonathan Hilgart ([jonhilgart22](https://github.com/jonhilgart22))
+ Kevin Tan ([kxwtan](https://github.com/kxwtan))
+ Max Tang ([Tanngent](https://github.com/Tanngent))
+ Melissa Meng ([17Melissa](https://github.com/17Melissa))
+ Nour Oulad Moussa ([NourOM02](https://github.com/NourOM02))
+ Syed Mahbubul Huq ([SyedHuq28](https://github.com/SyedHuq28))
+ charlie-liuu ([charlie-liuu](https://github.com/charlie-liuu))
+ chloeqxq ([chloeqxq](https://github.com/chloeqxq))
+ hima sheth ([himasheth](https://github.com/himasheth))
+ khufia ([khufia](https://github.com/khufia))
+ ru5h16h ([ru5h16h](https://github.com/ru5h16h))
+ wu-ming233 ([wu-ming233](https://github.com/wu-ming233))
+ yvonne90190 ([yvonne90190](https://github.com/yvonne90190))
+ Yuan-Hou ([Yuan-Hou](https://github.com/Yuan-Hou))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Jheng-Hong Yang ([justram](https://github.com/justram))
+ Sahel Sharifymoghaddam ([sahel-sh](https://github.com/sahel-sh))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Mofe Adeyemi ([Mofetoluwa](https://github.com/Mofetoluwa))
+ Catherine Zhou ([Cathrineee](https://github.com/Cathrineee))
+ Ogundepo Odunayo ([ToluClassics](https://github.com/ToluClassics))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Ehsan ([ehsk](https://github.com/ehsk))

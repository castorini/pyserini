# Pyserini Release Notes (v2.2.0)

+ **Release date:** June 2, 2026
+ **Anserini dependency:** v2.1.1
+ **Lucene dependency:** v10.4.0

## Summary of Changes

+ Known issues are [enumerated separately](./known-issues-v2.2.0.md).
+ Added BM25 `k1` and `b` configuration support to the REST API and MCP server.
+ Added document truncation support to REST search results and document fetches.
+ Fixed DPR and CosDPR encoder compatibility with Transformers 5.
+ Combined and reorganized ODQA 2CR topic runs.
+ Removed deprecated CS Vault metadata URLs from prebuilt index and encoded corpus metadata.
+ Moved non-Faiss encoding tests from `tests/core` to `tests/base` and cleaned up warnings.
+ Fixed null handling for `bottom_fb_docs` in Python rerankers.

## Contributors

### This Release

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Lily Ge ([lilyjge](https://github.com/lilyjge))
+ Md. Masud Mazumder ([masud70](https://github.com/masud70))
+ amulyabenarji777 ([amulyabenarji777](https://github.com/amulyabenarji777))
+ grf932 ([grf932](https://github.com/grf932))
+ Kevin Wang ([k464wang](https://github.com/k464wang))
+ Tobiloba Komolafe ([ibot1](https://github.com/ibot1))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors?all=1):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Daniel Guo ([clides](https://github.com/clides))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Lily Ge ([lilyjge](https://github.com/lilyjge))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Sahel Sharifymoghaddam ([sahel-sh](https://github.com/sahel-sh))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Jasper Xian ([jasper-xian](https://github.com/jasper-xian))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Manveer Tamber ([manveertamber](https://github.com/manveertamber))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Jheng-Hong Yang ([justram](https://github.com/justram))
+ FarmersWrap ([FarmersWrap](https://github.com/FarmersWrap))
+ Minghan Li ([alexlimh](https://github.com/alexlimh))
+ Mofe Adeyemi ([Mofetoluwa](https://github.com/Mofetoluwa))
+ Catherine Zhou ([Cathrineee](https://github.com/Cathrineee))
+ Ogundepo Odunayo ([ToluClassics](https://github.com/ToluClassics))
+ sisixili ([sisixili](https://github.com/sisixili))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Habeeb Shopeju ([HAKSOAT](https://github.com/HAKSOAT))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Ehsan ([ehsk](https://github.com/ehsk))
+ Shivani Upadhyay ([UShivani3](https://github.com/UShivani3))
+ Daniel Zhang ([zdann15](https://github.com/zdann15))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))

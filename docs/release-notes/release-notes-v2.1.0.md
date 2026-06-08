# Pyserini Release Notes (v2.1.0)

+ **Release date:** May 19, 2026
+ **Anserini dependency:** v2.1.1
+ **Lucene dependency:** v10.4.0

## Summary of Changes

+ Known issues are [enumerated separately](./known-issues-v2.1.0.md).
+ Updated to the Anserini v2.1.1 fatjar.
+ Upgraded to Transformers 5.
+ Added Python implementations of RM3 and Rocchio PRF.
+ Added installation skills.
+ Refactored JVM setup.
+ Refactored and reorganized test cases.
  + Reorganized unit test cases into `base`, `core`, and `optional` under `tests/`.
  + Reorganized integration test cases into `integrations/core`.
+ Refactored and improved the REST and MCP APIs around a shared backend.
+ Improved REST API:
  + Aligned with Anserini REST API.
  + Added authentication, logging, backpressure, and caching support.
+ Refreshed prebuilt index metadata, added support for plain tar prebuilt indexes, and updated BEIR 2CR coverage.

## Contributors

### This Release

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Lily Ge ([lilyjge](https://github.com/lilyjge))
+ Alex Wang ([alex-wang101](https://github.com/alex-wang101))
+ Ayomide Adebara ([Adebara123](https://github.com/Adebara123))
+ David Dong ([david23131](https://github.com/david23131))
+ DHRUV DUBEY ([zatchbell1311-wq](https://github.com/zatchbell1311-wq))
+ h79yan ([h79yan](https://github.com/h79yan))
+ Kevin Wang ([k464wang](https://github.com/k464wang))
+ kwamearhinPORTFL ([kwamearhinPORTFL](https://github.com/kwamearhinPORTFL))
+ Mazharul Islam Leon ([mazleon](https://github.com/mazleon))
+ mohamedshakir3 ([mohamedshakir3](https://github.com/mohamedshakir3))
+ Na'ad ([namatvir](https://github.com/namatvir))
+ Nas ([nasazzam](https://github.com/nasazzam))
+ Nour Jedidi ([nourj98](https://github.com/nourj98))
+ Oluwaseun Ajayi ([Seun-Ajayi](https://github.com/Seun-Ajayi))
+ Tahseen Rasheed Chowdhury ([TahseenSust](https://github.com/TahseenSust))
+ Uchenna Uchechukwu-Njoku ([blissuche90](https://github.com/blissuche90))
+ Vansh Jain ([VanshJain4](https://github.com/VanshJain4))
+ Xianda Du ([XiandaDu](https://github.com/XiandaDu))
+ Zixi Tang ([Zixi-Sam-Tang](https://github.com/Zixi-Sam-Tang))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors?all=1):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Daniel Guo ([clides](https://github.com/clides))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Lily Ge ([lilyjge](https://github.com/lilyjge))
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

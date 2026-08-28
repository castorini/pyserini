# Pyserini Release Notes (v2.4.0)

+ **Release date:** August 27, 2026
+ **Anserini dependency:** v2.3.0
+ **Lucene dependency:** v10.5.0

## Summary of Changes

+ Updated to the Anserini v2.3.0 fatjar and Lucene v10.5.0.
+ Moved metadata for prebuilt indexes, topics, and qrels to external catalogs.
+ Refactored query encoding code and loading of encoded queries.
+ Removed obsolete cached queries.
+ Removed the `tools/` submodule.
+ Fixed BPR reproductions and added support for encoding BPR queries from Hugging Face models.
+ Centralized Pyserini cache directory resolution, archive downloads, and the FAISS OpenMP workaround.
+ Added unified JSONL request logging to the REST server.
+ Updated handling of MIRACL training data.
+ Refreshed and reran dense retrieval commands in documentation.

## Contributors

### This Release

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Caden Sun ([Quaden2307](https://github.com/Quaden2307))
+ Yash Singh ([yashs33244](https://github.com/yashs33244))
+ abduldattijo ([abduldattijo](https://github.com/abduldattijo))
+ Abu Bin Fahd ([abubinfahd](https://github.com/abubinfahd))
+ Ahmad Tamer ([AhmadT198](https://github.com/AhmadT198))
+ Akpoyibo Fortune ([Rex-fortune](https://github.com/Rex-fortune))
+ akshaldhal ([akshaldhal](https://github.com/akshaldhal))
+ Ananto Nayan Bala ([nayanananto](https://github.com/nayanananto))
+ Arnaud Thery ([St4r4x](https://github.com/St4r4x))
+ ayesha12321 ([ayesha12321](https://github.com/ayesha12321))
+ Bakary Gibba ([BakaryGibba](https://github.com/BakaryGibba))
+ Bashir486 ([Bashir486](https://github.com/Bashir486))
+ Carlos Pineda ([carlosp2001](https://github.com/carlosp2001))
+ Crystina Xinyu Zhang ([crystina-z](https://github.com/crystina-z))
+ Derek Lin ([kenoi1](https://github.com/kenoi1))
+ Evan-Lowry ([Evan-Lowry](https://github.com/Evan-Lowry))
+ farhadmoradi66 ([farhadmoradi66](https://github.com/farhadmoradi66))
+ Foad Rashidi ([mfrashidi](https://github.com/mfrashidi))
+ Hamza Nadif ([Hamza-Nadif](https://github.com/Hamza-Nadif))
+ Hayanaanaa ([Hayanaanaa](https://github.com/Hayanaanaa))
+ Ian Chang ([Fustigate8933](https://github.com/Fustigate8933))
+ Jon Holman ([JonHolman](https://github.com/JonHolman))
+ Khush Mittal ([k22mitta](https://github.com/k22mitta))
+ Leonoaix ([Leonoaix](https://github.com/Leonoaix))
+ Lily Ge ([lilyjge](https://github.com/lilyjge))
+ MasrurAjhor ([MasrurAjhor](https://github.com/MasrurAjhor))
+ mehra-es ([mehra-es](https://github.com/mehra-es))
+ Mihit Nanda ([mihiit](https://github.com/mihiit))
+ Mohamed Anis Nedjem ([NMA19](https://github.com/NMA19))
+ MUHAMMAD ALI ARSHAD ([muhammad-ali-arshad](https://github.com/muhammad-ali-arshad))
+ Muhammad Dawood Khan ([dawoodkhandev](https://github.com/dawoodkhandev))
+ Navid Ebadi ([Navid-Ebadi-2003](https://github.com/Navid-Ebadi-2003))
+ Niloy Biswas ([niloy-biswas](https://github.com/niloy-biswas))
+ Nomso ([nomsou](https://github.com/nomsou))
+ PRAVEENA SATTI ([sattipraveena3-sudo](https://github.com/sattipraveena3-sudo))
+ sadia213 ([sadia213](https://github.com/sadia213))
+ sean aba ([seangebob](https://github.com/seangebob))
+ Sepideh Forouzi ([sepidfs](https://github.com/sepidfs))
+ Sparsh Shah ([sparshshah19](https://github.com/sparshshah19))

### All Time

All contributors with five or more commits, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors?all=1):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Daniel Guo ([clides](https://github.com/clides))
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
+ Shivani Upadhyay ([UShivani3](https://github.com/UShivani3))
+ Daniel Zhang ([zdann15](https://github.com/zdann15))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Ehsan ([ehsk](https://github.com/ehsk))

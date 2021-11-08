# Pyserini Release Notes (v0.14.0)

**Release date: November 8, 2021**

+ Added support for impact indexes and sparse learned retrieval models (DeepImpact, uniCOIL + doc2query-T5, uniCOIL + TILDE, SPLADE v2) .
+ Added support for MS MARCO V2 collections.
+ Added support for Vector-PRF.
+ Added various pre-built indexes.
+ Added integration tests for sparse learned retrieval models and Vector-PRF; improved testing overall.
+ Added convenience scripts for generating info about pre-built indexes and for validating pre-built indexes.
+ Fixed encoding issues by dropping `JString` wrapping and letting Pyjnius handle Python/Java string conversion directly.
+ Updated MS MARCO passage LTR code/documentation and added MS MARCO doc LTR code/documentation.

## Contributors (This Release)

Sorted by number of commits:

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Matt Yang ([justram](https://github.com/justram))
+ Xuntian Lin ([apokali](https://github.com/apokali))
+ Dahlia Chehata ([Dahlia-Chehata](https://github.com/Dahlia-Chehata))
+ Mayank Anand ([mayankanand007](https://github.com/mayankanand007))
+ Nima Sadri ([nimasadri11](https://github.com/nimasadri11))
+ Rodrigo Nogueira ([rodrigonogueira4](https://github.com/rodrigonogueira4))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ stekiri ([stekiri](https://github.com/stekiri))
+ Carlos Eduardo Rosar Kós Lassance ([cadurosar](https://github.com/cadurosar))
+ David Duan ([RootofalleviI](https://github.com/RootofalleviI))
+ Justin Leung ([leungjch](https://github.com/leungjch))
+ Larry Li ([larryli1999](https://github.com/larryli1999))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Wei Zhong ([t-k-](https://github.com/t-k-))
+ Yifan Qiao ([Qiaoyf96](https://github.com/Qiaoyf96))
+ Yuetong Wang ([AlexWang000](https://github.com/AlexWang000))
+ Matt Yang ([d1shs0ap](https://github.com/d1shs0ap))
+ Zizeng Meng ([mzzchy](https://github.com/mzzchy))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))

## All Contributors

All contributors with more than one commit, sorted by number of commits, [according to GitHub](https://github.com/castorini/pyserini/graphs/contributors):

+ Jimmy Lin ([lintool](https://github.com/lintool))
+ Xueguang Ma ([MXueguang](https://github.com/MXueguang))
+ Johnson Han ([x65han](https://github.com/x65han))
+ Yuqi Liu ([yuki617](https://github.com/yuki617))
+ Stephanie Hu ([stephaniewhoo](https://github.com/stephaniewhoo))
+ Jack Lin ([jacklin64](https://github.com/jacklin64))
+ Arthur Chen ([ArthurChen189](https://github.com/ArthurChen189))
+ Ronak Pradeep ([ronakice](https://github.com/ronakice))
+ Hang Li ([hanglics](https://github.com/hanglics))
+ Chris Kamphuis ([Chriskamphuis](https://github.com/Chriskamphuis))
+ Zeynep Akkalyoncu Yilmaz ([zeynepakkalyoncu](https://github.com/zeynepakkalyoncu))
+ Xinyu Mavis Liu ([x389liu](https://github.com/x389liu))
+ Sailesh Nankani ([saileshnankani](https://github.com/saileshnankani))
+ Pepijn Boers ([PepijnBoers](https://github.com/PepijnBoers))
+ Dahlia Chehata ([Dahlia-Chehata](https://github.com/Dahlia-Chehata))
+ Jingtao Zhan ([jingtaozhan](https://github.com/jingtaozhan))
+ Qing Guo ([qguo96](https://github.com/qguo96))
+ Marko Arezina ([mrkarezina](https://github.com/mrkarezina))
+ Rodrigo Nogueira ([rodrigonogueira4](https://github.com/rodrigonogueira4))
+ Tommaso Teofili ([tteofili](https://github.com/tteofili))
+ Hang Cui ([HangCui0510](https://github.com/HangCui0510))
+ Kai Sun ([KaiSun314](https://github.com/KaiSun314))
+ Xinyu (Crystina) Zhang ([crystina-z](https://github.com/crystina-z))
+ Larry Li ([larryli1999](https://github.com/larryli1999))
+ Matt Yang ([justram](https://github.com/justram))
+ Xuntian Lin ([apokali](https://github.com/apokali))
+ Shengyao Zhuang ([ArvinZhuang](https://github.com/ArvinZhuang))
+ David Duan ([RootofalleviI](https://github.com/RootofalleviI))
+ Mayank Anand ([mayankanand007](https://github.com/mayankanand007))
+ Nima Sadri ([nimasadri11](https://github.com/nimasadri11))
+ Cash Costello ([cash](https://github.com/cash))
+ Yuxuan Ji ([yuxuan-ji](https://github.com/yuxuan-ji))
+ stekiri ([stekiri](https://github.com/stekiri))
+ Jiarui Zhang ([jrzhang12](https://github.com/jiarui-z))
+ Joel Mackenzie ([JMMackenzie](https://github.com/JMMackenzie))
+ Oleg Lesota ([olesota](https://github.com/olesota))

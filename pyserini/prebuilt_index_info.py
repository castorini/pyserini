#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from prebuilt_index_tf_msmarco import TF_INDEX_INFO_MSMARCO
from prebuilt_index_tf_beir import TF_INDEX_INFO_BEIR
from prebuilt_index_tf_miracl import TF_INDEX_INFO_MIRACL
from prebuilt_index_tf_mrtydi import TF_INDEX_INFO_MRTYDI

TF_INDEX_INFO_CURRENT = {
    "cacm": {
        "description": "Lucene index of the CACM corpus. (Lucene 9)",
        "filename": "lucene-index.cacm.tar.gz",
        "urls": [
            "https://github.com/castorini/anserini-data/raw/master/CACM/lucene-index.cacm.20221005.252b5e.tar.gz",
        ],
        "md5": "cfe14d543c6a27f4d742fb2d0099b8e0",
        "size compressed (bytes)": 2347197,
        "total_terms": 320968,
        "documents": 3204,
        "unique_terms": 14363,
    },
    "robust04": {
        "description": "Lucene index of TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track. (Lucene 9)",
        "filename": "lucene-index.robust04.20221005.252b5e.tar.gz",
        "readme": "lucene-index.robust04.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.robust04.20221005.252b5e.tar.gz",
        ],
        "md5": "a1abd5437394956b7ec8bea4699b5e46",
        "size compressed (bytes)": 1806776535,
        "total_terms": 174540872,
        "documents": 528030,
        "unique_terms": 923436,
    },

    "enwiki-paragraphs": {
        "description": "Lucene index of English Wikipedia for BERTserini",
        "filename": "lucene-index.enwiki-20180701-paragraphs.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.enwiki-20180701-paragraphs.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/WHKMSCbwQfDXyHt/download"
        ],
        "md5": "77d1cd530579905dad2ee3c2bda1b73d",
        "size compressed (bytes)": 17725958785,
        "total_terms": 1498980668,
        "documents": 39880064,
        "unique_terms": -1,
        "downloaded": False
    },
    "zhwiki-paragraphs": {
        "description": "Lucene index of Chinese Wikipedia for BERTserini",
        "filename": "lucene-index.zhwiki-20181201-paragraphs.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.zhwiki-20181201-paragraphs.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/6kEjQZaRYtnb8A6/download"
        ],
        "md5": "c005af4036296972831288c894918a92",
        "size compressed (bytes)": 3284531213,
        "total_terms": 320776789,
        "documents": 4170312,
        "unique_terms": -1,
        "downloaded": False
    },
    "trec-covid-r5-abstract": {
        "description": "Lucene index for TREC-COVID Round 5: abstract index",
        "filename": "lucene-index-cord19-abstract-2020-07-16.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-07-16/lucene-index-cord19-abstract-2020-07-16.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/c37JxKYQ7Hogs72/download"
        ],
        "md5": "c883571ccc78b4c2ce05b41eb07f5405",
        "size compressed (bytes)": 2796524,
        "total_terms": 22100404,
        "documents": 192459,
        "unique_terms": 195875,
        "downloaded": False
    },
    "trec-covid-r5-full-text": {
        "description": "Lucene index for TREC-COVID Round 5: full-text index",
        "filename": "lucene-index-cord19-full-text-2020-07-16.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-07-16/lucene-index-cord19-full-text-2020-07-16.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/c7CcxRbFWfiFnFq/download"
        ],
        "md5": "23cfad89b4c206d66125f5736f60248f",
        "size compressed (bytes)": 5351744,
        "total_terms": 275238847,
        "documents": 192460,
        "unique_terms": 1843368,
        "downloaded": False
    },
    "trec-covid-r5-paragraph": {
        "description": "Lucene index for TREC-COVID Round 5: paragraph index",
        "filename": "lucene-index-cord19-paragraph-2020-07-16.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-07-16/lucene-index-cord19-paragraph-2020-07-16.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/HXigraF5KJL3xS8/download"
        ],
        "md5": "c2c6ac832f8a1fcb767d2356d2b1e1df",
        "size compressed (bytes)": 11352968,
        "total_terms": 627083574,
        "documents": 3010497,
        "unique_terms": 1843368,
        "downloaded": False
    },
    "trec-covid-r4-abstract": {
        "description": "Lucene index for TREC-COVID Round 4: abstract index",
        "filename": "lucene-index-cord19-abstract-2020-06-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-06-19/lucene-index-cord19-abstract-2020-06-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/fBta6sAt4MdaHQX/download"
        ],
        "md5": "029bd55daba8800fbae2be9e5fcd7b33",
        "size compressed (bytes)": 2584264,
        "total_terms": 18724353,
        "documents": 158226,
        "unique_terms": 179937,
        "downloaded": False
    },
    "trec-covid-r4-full-text": {
        "description": "Lucene index for TREC-COVID Round 4: full-text index",
        "filename": "lucene-index-cord19-full-text-2020-06-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-06-19/lucene-index-cord19-full-text-2020-06-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/yErSHZHD38jcDSY/download"
        ],
        "md5": "3d0eb12094a24cff9bcacd1f17c3ea1c",
        "size compressed (bytes)": 4983900,
        "total_terms": 254810123,
        "documents": 158227,
        "unique_terms": 1783089,
        "downloaded": False
    },
    "trec-covid-r4-paragraph": {
        "description": "Lucene index for TREC-COVID Round 4: paragraph index",
        "filename": "lucene-index-cord19-paragraph-2020-06-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-06-19/lucene-index-cord19-paragraph-2020-06-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/7md4kwNNgy3oxiH/download"
        ],
        "md5": "5cd8cd6998177bed7a3e0057ef8b3595",
        "size compressed (bytes)": 10382704,
        "total_terms": 567579834,
        "documents": 2781172,
        "unique_terms": 1783089,
        "downloaded": False
    },
    "trec-covid-r3-abstract": {
        "description": "Lucene index for TREC-COVID Round 3: abstract index",
        "filename": "lucene-index-cord19-abstract-2020-05-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-19/lucene-index-cord19-abstract-2020-05-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Zg9p2D5tJgiTGx2/download"
        ],
        "md5": "37bb97d0c41d650ba8e135fd75ae8fd8",
        "size compressed (bytes)": 2190328,
        "total_terms": 16278419,
        "documents": 128465,
        "unique_terms": 168291,
        "downloaded": False
    },
    "trec-covid-r3-full-text": {
        "description": "Lucene index for TREC-COVID Round 3: full-text index",
        "filename": "lucene-index-cord19-full-text-2020-05-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-19/lucene-index-cord19-full-text-2020-05-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/BTzaQgZ55898dXM/download"
        ],
        "md5": "f5711915a66cd2b511e0fb8d03e4c325",
        "size compressed (bytes)": 4233300,
        "total_terms": 215806519,
        "documents": 128465,
        "unique_terms": 1620335,
        "downloaded": False
    },
    "trec-covid-r3-paragraph": {
        "description": "Lucene index for TREC-COVID Round 3: paragraph index",
        "filename": "lucene-index-cord19-paragraph-2020-05-19.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-19/lucene-index-cord19-paragraph-2020-05-19.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/nPyMYTys6NkmEdN/download"
        ],
        "md5": "012ab1f804382b2275c433a74d7d31f2",
        "size compressed (bytes)": 9053524,
        "total_terms": 485309568,
        "documents": 2297201,
        "unique_terms": 1620335,
        "downloaded": False
    },
    "trec-covid-r2-abstract": {
        "description": "Lucene index for TREC-COVID Round 2: abstract index",
        "filename": "lucene-index-cord19-abstract-2020-05-01.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-abstract-2020-05-01.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/3YZE65FSypwfnQQ/download"
        ],
        "md5": "a06e71a98a68d31148cb0e97e70a2ee1",
        "size compressed (bytes)": 1575804,
        "total_terms": 7651125,
        "documents": 59873,
        "unique_terms": 109750,
        "downloaded": False
    },
    "trec-covid-r2-full-text": {
        "description": "Lucene index for TREC-COVID Round 2: full-text index",
        "filename": "lucene-index-cord19-full-text-2020-05-01.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-full-text-2020-05-01.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/NdPEB7swXeZnq3o/download"
        ],
        "md5": "e7eca1b976cdf2cd80e908c9ac2263cb",
        "size compressed (bytes)": 3088540,
        "total_terms": 154736295,
        "documents": 59876,
        "unique_terms": 1214374,
        "downloaded": False
    },
    "trec-covid-r2-paragraph": {
        "description": "Lucene index for TREC-COVID Round 2: paragraph index",
        "filename": "lucene-index-cord19-paragraph-2020-05-01.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-paragraph-2020-05-01.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Mz7n5FAt7rmnYCY/download"
        ],
        "md5": "8f9321757a03985ac1c1952b2fff2c7d",
        "size compressed (bytes)": 6881696,
        "total_terms": 360119048,
        "documents": 1758168,
        "unique_terms": 1214374,
        "downloaded": False
    },
    "trec-covid-r1-abstract": {
        "description": "Lucene index for TREC-COVID Round 1: abstract index",
        "filename": "lucene-index-covid-2020-04-10.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-04-10/lucene-index-covid-2020-04-10.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Rz8AEmsFo9NWGP6/download"
        ],
        "md5": "ec239d56498c0e7b74e3b41e1ce5d42a",
        "size compressed (bytes)": 1621440,
        "total_terms": 6672525,
        "documents": 51069,
        "unique_terms": 104595,
        "downloaded": False
    },
    "trec-covid-r1-full-text": {
        "description": "Lucene index for TREC-COVID Round 1: full-text index",
        "filename": "lucene-index-covid-full-text-2020-04-10.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-04-10/lucene-index-covid-full-text-2020-04-10.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/oQzSoxrT3grGmBe/download"
        ],
        "md5": "401a6f5583b0f05340c73fbbeb3279c8",
        "size compressed (bytes)": 4471820,
        "total_terms": 315624154,
        "documents": 51071,
        "unique_terms": 1812522,
        "downloaded": False
    },
    "trec-covid-r1-paragraph": {
        "description": "Lucene index for TREC-COVID Round 1: paragraph index",
        "filename": "lucene-index-covid-paragraph-2020-04-10.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-04-10/lucene-index-covid-paragraph-2020-04-10.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/HDtb5Ys7MYBkePC/download"
        ],
        "md5": "8b87a2c55bc0a15b87f11e796860216a",
        "size compressed (bytes)": 5994192,
        "total_terms": 330715243,
        "documents": 1412648,
        "unique_terms": 944574,
        "downloaded": False
    },
    "cast2019": {
        "description": "Lucene index for TREC 2019 CaST",
        "filename": "index-cast2019.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-cast2019.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/56LcDcRPopdQc4d/download"
        ],
        "md5": "36e604d7f5a4e08ade54e446be2f6345",
        "size compressed (bytes)": 21266884884,
        "total_terms": 1593628213,
        "documents": 38429835,
        "unique_terms": -1,
        "downloaded": False
    },
    "wikipedia-dpr": {
        "description": "Lucene index of Wikipedia with DPR 100-word splits",
        "filename": "index-wikipedia-dpr-20210120-d1b9e6.tar.gz",
        "readme": "index-wikipedia-dpr-20210120-d1b9e6-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-wikipedia-dpr-20210120-d1b9e6.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/t6tDJmpoxPw9tH8/download"
        ],
        "md5": "c28f3a56b2dfcef25bf3bf755c264d04",
        "size compressed (bytes)": 9177942656,
        "total_terms": 1512973270,
        "documents": 21015324,
        "unique_terms": 5345463,
        "downloaded": False
    },
    "wikipedia-dpr-slim": {
        "description": "Lucene index of Wikipedia with DPR 100-word splits (slim version, document text not stored)",
        "filename": "index-wikipedia-dpr-slim-20210120-d1b9e6.tar.gz",
        "readme": "index-wikipedia-dpr-slim-20210120-d1b9e6-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-wikipedia-dpr-slim-20210120-d1b9e6.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Gk2sfTyJCyaTrYH/download"
        ],
        "md5": "7d40604a824b5df37a1ae9d25ea38071",
        "size compressed (bytes)": 1810342390,
        "total_terms": 1512973270,
        "documents": 21015324,
        "unique_terms": 5345463,
        "downloaded": False
    },
    "wikipedia-kilt-doc": {
        "description": "Lucene index of Wikipedia snapshot used as KILT's knowledge source.",
        "filename": "index-wikipedia-kilt-doc-20210421-f29307.tar.gz",
        "readme": "index-wikipedia-kilt-doc-20210421-f29307-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-wikipedia-kilt-doc-20210421-f29307.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/RqtLg3CZT38k32c/download"
        ],
        "md5": "b8ec8feb654f7aaa86f9901dc6c804a8",
        "size compressed (bytes)": 10901127209,
        "total_terms": 1915061164,
        "documents": 5903530,
        "unique_terms": 8722502,
        "downloaded": False
    },
    "wiki-all-6-3-tamber": {
        "description": "Lucene index of wiki-all-6-3-tamber from castorini/odqa-wiki-corpora",
        "filename": "lucene-index.wiki-all-6-3-tamber.20230111.40277a.tar.gz",
        "readme": "lucene-index-wiki-all-6-3-tamber-20230111-40277a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.wiki-all-6-3-tamber.20230111.40277a.tar.gz",
        ],
        "md5": "018b45ee8c6278a879caa3145b2dc05d",
        "size compressed (bytes)": 26240661946,
        "total_terms": 5064706668,
        "documents": 76680040,
        "unique_terms": 14604922,
        "downloaded": False
    },

    # Mr.TyDi indexes
    "mrtydi-v1.1-arabic": {
        "description": "Lucene index for Mr.TyDi v1.1 (Arabic).",
        "filename": "lucene-index.mrtydi-v1.1-arabic.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-arabic.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-arabic.20220928.b5ecc5.tar.gz",
        ],
        "md5": "efff40a2548f759eb8b0e47e0622685b",
        "size compressed (bytes)": 1420441600,
        "total_terms": 92529032,
        "documents": 2106586,
        "unique_terms": 1284748,
        "downloaded": False
    },
    "mrtydi-v1.1-bengali": {
        "description": "Lucene index for Mr.TyDi v1.1 (Bengali).",
        "filename": "lucene-index.mrtydi-v1.1-bengali.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-bengali.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-bengali.20220928.b5ecc5.tar.gz"
        ],
        "md5": "6ed844c8f17b2f041fba7c5676d3fb42",
        "size compressed (bytes)": 294942720,
        "total_terms": 15236599,
        "documents": 304059,
        "unique_terms": 520699,
        "downloaded": False
    },
    "mrtydi-v1.1-english": {
        "description": "Lucene index for Mr.TyDi v1.1 (English).",
        "filename": "lucene-index.mrtydi-v1.1-english.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-english.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-english.20220928.b5ecc5.tar.gz"
        ],
        "md5": "e6b0a2531d958c3d1a65634dc315b0ab",
        "size compressed (bytes)": 20566118400,
        "total_terms": 1507060932,
        "documents": 32907100,
        "unique_terms": -1,
        "downloaded": False
    },
    "mrtydi-v1.1-finnish": {
        "description": "Lucene index for Mr.TyDi v1.1 (Finnish).",
        "filename": "lucene-index.mrtydi-v1.1-finnish.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-finnish.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-finnish.20220928.b5ecc5.tar.gz"
        ],
        "md5": "0f464c022447eed5431157f0b2feb0b3",
        "size compressed (bytes)": 1116272640,
        "total_terms": 69416543,
        "documents": 1908757,
        "unique_terms": 1715076,
        "downloaded": False
    },
    "mrtydi-v1.1-indonesian": {
        "description": "Lucene index for Mr.TyDi v1.1 (Indonesian).",
        "filename": "lucene-index.mrtydi-v1.1-indonesian.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-indonesian.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-indonesian.20220928.b5ecc5.tar.gz"
        ],
        "md5": "345d43a2443786a3394a93a6f7ef77b7",
        "size compressed (bytes)": 698388480,
        "total_terms": 52493134,
        "documents": 1469399,
        "unique_terms": 942552,
        "downloaded": False
    },
    "mrtydi-v1.1-japanese": {
        "description": "Lucene index for Mr.TyDi v1.1 (Japanese).",
        "filename": "lucene-index.mrtydi-v1.1-japanese.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-japanese.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-japanese.20220928.b5ecc5.tar.gz"
        ],
        "md5": "5f0802c1257c325a3e25c58523dba841",
        "size compressed (bytes)": 4333844480,
        "total_terms": 300761975,
        "documents": 7000027,
        "unique_terms": 1588879,
        "downloaded": False
    },
    "mrtydi-v1.1-korean": {
        "description": "Lucene index for Mr.TyDi v1.1 (Korean).",
        "filename": "lucene-index.mrtydi-v1.1-korean.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-korean.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-korean.20220928.b5ecc5.tar.gz"
        ],
        "md5": "4277f406b138c46edf7c17e4248f3b2e",
        "size compressed (bytes)": 1349109760,
        "total_terms": 122217295,
        "documents": 1496126,
        "unique_terms": 1517179,
        "downloaded": False
    },
    "mrtydi-v1.1-russian": {
        "description": "Lucene index for Mr.TyDi v1.1 (Russian).",
        "filename": "lucene-index.mrtydi-v1.1-russian.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-russian.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-russian.20220928.b5ecc5.tar.gz"
        ],
        "md5": "d5837fee29c60c7a3a24cfd598056038",
        "size compressed (bytes)": 6864660480,
        "total_terms": 346329117,
        "documents": 9597504,
        "unique_terms": 3034240,
        "downloaded": False
    },
    "mrtydi-v1.1-swahili": {
        "description": "Lucene index for Mr.TyDi v1.1 (Swahili).",
        "filename": "lucene-index.mrtydi-v1.1-swahili.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-swahili.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-swahili.20220928.b5ecc5.tar.gz"
        ],
        "md5": "bebff76ec6dfe76c904604f8ed1bcd3e",
        "size compressed (bytes)": 59607040,
        "total_terms": 4937051,
        "documents": 136689,
        "unique_terms": 385711,
        "downloaded": False
    },
    "mrtydi-v1.1-telugu": {
        "description": "Lucene index for Mr.TyDi v1.1 (Telugu).",
        "filename": "lucene-index.mrtydi-v1.1-telugu.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-telugu.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-telugu.20220928.b5ecc5.tar.gz"
        ],
        "md5": "89f8b280cacbdc27e90bb1ea40029c21",
        "size compressed (bytes)": 519157760,
        "total_terms": 26812052,
        "documents": 548224,
        "unique_terms": 1157217,
        "downloaded": False
    },
    "mrtydi-v1.1-thai": {
        "description": "Lucene index for Mr.TyDi v1.1 (Thai).",
        "filename": "lucene-index.mrtydi-v1.1-thai.20220928.b5ecc5.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-thai.20220928.b5ecc5.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-thai.20220928.b5ecc5.tar.gz"
        ],
        "md5": "047152fc6bc1b5c5d945f38b23de971e",
        "size compressed (bytes)": 546201600,
        "total_terms": 31550936,
        "documents": 568855,
        "unique_terms": 663628,
        "downloaded": False
    },

    "hc4-v1.0-fa": {
        "description": "Lucene index for HC4 v1.0 (Persian). (Lucene 9)",
        "filename": "lucene-index.hc4-v1.0-fa.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.hc4-v1.0.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-fa.20221025.c4a8d0.tar.gz"
        ],
        "md5": "80735c01b2f2cf82288381370adf1d66",
        "size compressed (bytes)": 1652960750,
        "total_terms": 112225896,
        "documents": 486486,
        "unique_terms": 617109,
        "downloaded": False
    },
    "hc4-v1.0-ru": {
        "description": "Lucene index for HC4 v1.0 (Russian). (Lucene 9)",
        "filename": "lucene-index.hc4-v1.0-ru.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.hc4-v1.0.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-ru.20221025.c4a8d0.tar.gz"
        ],
        "md5": "40259ba9ca993f850c960a172debe33e",
        "size compressed (bytes)": 13292705599,
        "total_terms": 764996714,
        "documents": 4721064,
        "unique_terms": 2625222,
        "downloaded": False
    },
    "hc4-v1.0-zh": {
        "description": "Lucene index for HC4 v1.0 (Chinese). (Lucene 9)",
        "filename": "lucene-index.hc4-v1.0-zh.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.hc4-v1.0.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-zh.20221025.c4a8d0.tar.gz"
        ],
        "md5": "2ea8885b8ec6c637971c8df0706b623e",
        "size compressed (bytes)": 2899033342,
        "total_terms": 304468580,
        "documents": 646302,
        "unique_terms": 4380932,
        "downloaded": False
    },
    "neuclir22-fa": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Persian). (Lucene 9)",
        "filename": "lucene-index.neuclir22-fa.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-fa.20221025.c4a8d0.tar.gz"
        ],
        "md5": "d423fb72bcd5bf2dea6e4a19743dcb95",
        "size compressed (bytes)": 7565790180,
        "total_terms": 514262091,
        "documents": 2232016,
        "unique_terms": 1479443,
        "downloaded": False
    },
    "neuclir22-ru": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Russian). (Lucene 9)",
        "filename": "lucene-index.neuclir22-ru.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-ru.20221025.c4a8d0.tar.gz"
        ],
        "md5": "2d04bbc880d535c1c4ab172c2c2d8ffe",
        "size compressed (bytes)": 14202967387,
        "total_terms": 830006658,
        "documents": 4627541,
        "unique_terms": 3396095,
        "downloaded": False
    },
    "neuclir22-zh": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Chinese). (Lucene 9)",
        "filename": "lucene-index.neuclir22-zh.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-zh.20221025.c4a8d0.tar.gz"
        ],
        "md5": "46fe989676ff510b997af24f6398199f",
        "size compressed (bytes)": 15733809682,
        "total_terms": 1654090507,
        "documents": 3179206,
        "unique_terms": 8213058,
        "downloaded": False
    },
    "neuclir22-fa-en": {
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Persian). (Lucene 9)",
        "filename": "lucene-index.neuclir22-fa-en.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22-en.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-fa-en.20221025.c4a8d0.tar.gz"
        ],
        "md5": "35363339b7f0527f27403b848fe01b04",
        "size compressed (bytes)": 6172239242,
        "total_terms": 554848215,
        "documents": 2232016,
        "unique_terms": 1033260,
        "downloaded": False
    },
    "neuclir22-ru-en": {
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Russian). (Lucene 9)",
        "filename": "lucene-index.neuclir22-ru-en.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22-en.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-ru-en.20221025.c4a8d0.tar.gz"
        ],
        "md5": "b0b98803260665eeae97163d2361838e",
        "size compressed (bytes)": 10513242212,
        "total_terms": 911886830,
        "documents": 4627541,
        "unique_terms": 2794257,
        "downloaded": False
    },
    "neuclir22-zh-en": {
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Chinese). (Lucene 9)",
        "filename": "lucene-index.neuclir22-zh-en.20221025.c4a8d0.tar.gz",
        "readme": "lucene-index.neuclir22-en.20221025.c4a8d0.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-zh-en.20221025.c4a8d0.tar.gz"
        ],
        "md5": "d44ca9c7b634cf56e8cfd5892a3d3427",
        "size compressed (bytes)": 8470981318,
        "total_terms": 803227160,
        "documents": 3179206,
        "unique_terms": 1616532,
        "downloaded": False
    },

    "miracl-v1.0-ar": {
        "description": "Lucene index for MIRACL v1.0 (Arabic).",
        "filename": "lucene-index.miracl-v1.0-ar.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-ar.20221004.2b2856.tar.gz"
        ],
        "md5": "503d3b49a557222d8074ac831a2f047a",
        "size compressed (bytes)": 1193292491,
        "total_terms": 90223450,
        "documents": 2061414,
        "unique_terms": 1246254,
        "downloaded": False
    },
    "miracl-v1.0-bn": {
        "description": "Lucene index for MIRACL v1.0 (Bengali).",
        "filename": "lucene-index.miracl-v1.0-bn.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-bn.20221004.2b2856.tar.gz"
        ],
        "md5": "7a20210328f0b83f44e041f0c94d30e2",
        "size compressed (bytes)": 236113202,
        "total_terms": 14963235,
        "documents": 297265,
        "unique_terms": 506812,
        "downloaded": False
    },
    "miracl-v1.0-en": {
        "description": "Lucene index for MIRACL v1.0 (English).",
        "filename": "lucene-index.miracl-v1.0-en.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-en.20221004.2b2856.tar.gz"
        ],
        "md5": "4fbd652deb76bcc05daa35392d4aa9f3",
        "size compressed (bytes)": 17823436054,
        "total_terms": 1505029955,
        "documents": 32893221,
        "unique_terms": 6152316,
        "downloaded": False
    },
    "miracl-v1.0-es": {
        "description": "Lucene index for MIRACL v1.0 (Spanish).",
        "filename": "lucene-index.miracl-v1.0-es.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-es.20221004.2b2856.tar.gz"
        ],
        "md5": "b4c9993ee3a131871d4f07dd96e80531",
        "size compressed (bytes)": 5474245249,
        "total_terms": 389319806,
        "documents": 10373953,
        "unique_terms": 2907509,
        "downloaded": False
    },
    "miracl-v1.0-fa": {
        "description": "Lucene index for MIRACL v1.0 (Persian).",
        "filename": "lucene-index.miracl-v1.0-fa.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-fa.20221004.2b2856.tar.gz"
        ],
        "md5": "bfc824aa37633e3d45bcfd5c5e0e1701",
        "size compressed (bytes)": 1023090577,
        "total_terms": 67968038,
        "documents": 2207172,
        "unique_terms": 1208930,
        "downloaded": False
    },
    "miracl-v1.0-fi": {
        "description": "Lucene index for MIRACL v1.0 (Finnish).",
        "filename": "lucene-index.miracl-v1.0-fi.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-fi.20221004.2b2856.tar.gz"
        ],
        "md5": "4197c90efd781c6153acaf15452c5479",
        "size compressed (bytes)": 925422988,
        "total_terms": 68295087,
        "documents": 1883509,
        "unique_terms": 1669817,
        "downloaded": False
    },
    "miracl-v1.0-fr": {
        "description": "Lucene index for MIRACL v1.0 (French).",
        "filename": "lucene-index.miracl-v1.0-fr.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-fr.20221004.2b2856.tar.gz"
        ],
        "md5": "e68b10d90be71b702888a3d00a8aa39c",
        "size compressed (bytes)": 6747612709,
        "total_terms": 508723988,
        "documents": 14636953,
        "unique_terms": 2811342,
        "downloaded": False
    },
    "miracl-v1.0-hi": {
        "description": "Lucene index for MIRACL v1.0 (Hindi).",
        "filename": "lucene-index.miracl-v1.0-hi.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-hi.20221004.2b2856.tar.gz"
        ],
        "md5": "d81f4e2b7ec5df8f9741168c23c977e2",
        "size compressed (bytes)": 340997734,
        "total_terms": 21080143,
        "documents": 506264,
        "unique_terms": 597558,
        "downloaded": False
    },
    "miracl-v1.0-id": {
        "description": "Lucene index for MIRACL v1.0 (Indonesian).",
        "filename": "lucene-index.miracl-v1.0-id.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-id.20221004.2b2856.tar.gz"
        ],
        "md5": "b1092e732991029fae7c542e5e129255",
        "size compressed (bytes)": 577263718,
        "total_terms": 51469219,
        "documents": 1446315,
        "unique_terms": 911944,
        "downloaded": False
    },
    "miracl-v1.0-ja": {
        "description": "Lucene index for MIRACL v1.0 (Japanese).",
        "filename": "lucene-index.miracl-v1.0-ja.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-ja.20221004.2b2856.tar.gz"
        ],
        "md5": "4db9550d0af63736a0fd2b486b3b7273",
        "size compressed (bytes)": 3745158372,
        "total_terms": 296659169,
        "documents": 6953614,
        "unique_terms": 1558643,
        "downloaded": False
    },
    "miracl-v1.0-ko": {
        "description": "Lucene index for MIRACL v1.0 (Korean).",
        "filename": "lucene-index.miracl-v1.0-ko.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-ko.20221004.2b2856.tar.gz"
        ],
        "md5": "c82f5c7641fd78b8dadfcb279a1c0340",
        "size compressed (bytes)": 1150899287,
        "total_terms": 121464424,
        "documents": 1486752,
        "unique_terms": 1504782,
        "downloaded": False
    },
    "miracl-v1.0-ru": {
        "description": "Lucene index for MIRACL v1.0 (Russian).",
        "filename": "lucene-index.miracl-v1.0-ru.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-ru.20221004.2b2856.tar.gz"
        ],
        "md5": "c1b974e298d9e1deeccae8b84a5bcd64",
        "size compressed (bytes)": 6003987738,
        "total_terms": 343106870,
        "documents": 9543918,
        "unique_terms": 2955627,
        "downloaded": False
    },
    "miracl-v1.0-sw": {
        "description": "Lucene index for MIRACL v1.0 (Swahili).",
        "filename": "lucene-index.miracl-v1.0-sw.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-sw.20221004.2b2856.tar.gz"
        ],
        "md5": "64b77bcc11e04575d0723ad81ac7c135",
        "size compressed (bytes)": 45410264,
        "total_terms": 4752278,
        "documents": 131924,
        "unique_terms": 361306,
        "downloaded": False
    },
    "miracl-v1.0-te": {
        "description": "Lucene index for MIRACL v1.0 (Telugu).",
        "filename": "lucene-index.miracl-v1.0-te.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-te.20221004.2b2856.tar.gz"
        ],
        "md5": "1f78c68678f439a3143a6fb0d25bfe27",
        "size compressed (bytes)": 402045711,
        "total_terms": 26105595,
        "documents": 518079,
        "unique_terms": 1120047,
        "downloaded": False
    },
    "miracl-v1.0-th": {
        "description": "Lucene index for MIRACL v1.0 (Thai).",
        "filename": "lucene-index.miracl-v1.0-th.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-th.20221004.2b2856.tar.gz"
        ],
        "md5": "eeef93c23b76fdc66b9e1ee01576765e",
        "size compressed (bytes)": 431498349,
        "total_terms": 29922100,
        "documents": 542166,
        "unique_terms": 626084,
        "downloaded": False
    },
    "miracl-v1.0-zh": {
        "description": "Lucene index for MIRACL v1.0 (Chinese).",
        "filename": "lucene-index.miracl-v1.0-zh.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-zh.20221004.2b2856.tar.gz"
        ],
        "md5": "dc7880da333b7c56d3a4ff0bf018febd",
        "size compressed (bytes)": 4212198217,
        "total_terms": 423635495,
        "documents": 4934368,
        "unique_terms": 6517412,
        "downloaded": False
    },
    "miracl-v1.0-de": {
        "description": "Lucene index for MIRACL v1.0 (German).",
        "filename": "lucene-index.miracl-v1.0-de.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-de.20221004.2b2856.tar.gz"
        ],
        "md5": "a40d1b9429c450b2e476d1e4ba22784d",
        "size compressed (bytes)": 8708219012,
        "total_terms": 581583743,
        "documents": 15866222,
        "unique_terms": 6288858,
        "downloaded": False
    },
    "miracl-v1.0-yo": {
        "description": "Lucene index for MIRACL v1.0 (Yoruba).",
        "filename": "lucene-index.miracl-v1.0-yo.20221004.2b2856.tar.gz",
        "readme": "lucene-index.miracl-v1.0.20221004.2b2856.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.miracl-v1.0-yo.20221004.2b2856.tar.gz"
        ],
        "md5": "7fa283d1af4a7c4ea8791eab9e386807",
        "size compressed (bytes)": 13211664,
        "total_terms": 1387088,
        "documents": 49043,
        "unique_terms": 174539,
        "downloaded": False
    }
}

TF_INDEX_INFO = {**TF_INDEX_INFO_CURRENT,
                 **TF_INDEX_INFO_MSMARCO,
                 **TF_INDEX_INFO_BEIR,
                 **TF_INDEX_INFO_MRTYDI,
                 **TF_INDEX_INFO_MIRACL}

IMPACT_INDEX_INFO_CURRENT = {
    "msmarco-v1-passage-slimr": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with BM25 negatives. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-slimr.20230220.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-slimr.20230220.md",
        "urls": [
            "https://vault.cs.uwaterloo.ca/s/EptAojzmCxz7mYM/download",
        ],
        "md5": "79e566fee4f376096e12a33cf67c8012",
        "size compressed (bytes)": 1942207690,
        "total_terms": 100694232684,
        "documents": 8841823,
        "unique_terms": 28121,
        "downloaded": False
    },
    "msmarco-v1-passage-slimr-pp": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with cross-encoder distillation and hardnegative mining. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-slimr-pp.20230220.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-slimr-pp.20230220.md",
        "urls": [
            "https://vault.cs.uwaterloo.ca/s/22Gjmnp5EP2HpqR/download",
        ],
        "md5": "17b2edd909bcda4980a93fb0ab87e72b",
        "size compressed (bytes)": 2164253966,
        "total_terms": 104421954301,
        "documents": 8841823,
        "unique_terms": 27766,
        "downloaded": False
    },
    "msmarco-v1-passage-unicoil": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-unicoil.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-unicoil.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-unicoil.20221005.252b5e.tar.gz",
        ],
        "md5": "29521fa94165e87caaaddcb5b0d37b13",
        "size compressed (bytes)": 1161034003,
        "total_terms": 44495093768,
        "documents": 8841823,
        "unique_terms": 27678,
        "downloaded": False
    },
    "msmarco-v1-passage-unicoil-noexp": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL (noexp). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-unicoil-noexp.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-unicoil-noexp.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-unicoil-noexp.20221005.252b5e.tar.gz",
        ],
        "md5": "dcb6506e0b8bb1d41863ea9cbaa057cf",
        "size compressed (bytes)": 873512626,
        "total_terms": 26468530021,
        "documents": 8841823,
        "unique_terms": 27647,
        "downloaded": False
    },
    "msmarco-v1-passage-deepimpact": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by DeepImpact. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-deepimpact.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-deepimpact.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-deepimpact.20221005.252b5e.tar.gz",
        ],
        "md5": "e1cd5bd86ae5b35912991a6c8c448bb0",
        "size compressed (bytes)": 1242661484,
        "total_terms": 35455908214,
        "documents": 8841823,
        "unique_terms": 3514102,
        "downloaded": False
    },
    "msmarco-v1-passage-unicoil-tilde": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-TILDE. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-unicoil-tilde.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-unicoil-tilde.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-unicoil-tilde.20221005.252b5e.tar.gz",
        ],
        "md5": "b732c58113ec39b197083dee3e702932",
        "size compressed (bytes)": 1871922326,
        "total_terms": 73040108576,
        "documents": 8841823,
        "unique_terms": 27646,
        "downloaded": False
    },
    "msmarco-v1-passage-distill-splade-max": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by distill-splade-max. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-distill-splade-max.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-distill-splade-max.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-distill-splade-max.20221005.252b5e.tar.gz"
        ],
        "md5": "7d8b56b348685b9c3e29e306803c61eb",
        "size compressed (bytes)": 3822892457,
        "total_terms": 95445422483,
        "documents": 8841823,
        "unique_terms": 28131,
        "downloaded": False
    },

    "msmarco-v1-doc-segmented-unicoil": {
        "description": "Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL, with title/segment encoding. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-unicoil.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-unicoil.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-unicoil.20221005.252b5e.tar.gz",
        ],
        "md5": "06e087b8575f3d49177abfcfaf4bba1c",
        "size compressed (bytes)": 5765257637,
        "total_terms": 214505277898,
        "documents": 20545677,
        "unique_terms": 29142,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-unicoil-noexp": {
        "description": "Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp), with title/segment encoding. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-unicoil-noexp.20221005.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-unicoil-noexp.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-unicoil-noexp.20221005.252b5e.tar.gz",
        ],
        "md5": "f2bb0e6e9e0ea4baa6072f6f842623d8",
        "size compressed (bytes)": 5323380960,
        "total_terms": 152323732876,
        "documents": 20545677,
        "unique_terms": 29142,
        "downloaded": False
    },

    "msmarco-v2-passage-unicoil-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-unicoil-0shot.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-unicoil-0shot.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-unicoil-0shot.20220808.4d6d2a.tar.gz",
        ],
        "md5": "9da229088995a3abfea57dd8681d16d5",
        "size compressed (bytes)": 21736933361,
        "total_terms": 775253560148,
        "documents": 138364198,
        "unique_terms": 29149,
        "downloaded": False
    },
    "msmarco-v2-passage-unicoil-noexp-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL (noexp). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220808.4d6d2a.tar.gz",
        ],
        "md5": "dda9de84072d2162e8649a040153942e",
        "size compressed (bytes)": 14347302774,
        "total_terms": 411330032512,
        "documents": 138364198,
        "unique_terms": 29148,
        "downloaded": False
    },

    "msmarco-v2-doc-segmented-unicoil-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL, with title prepended. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220808.4d6d2a.tar.gz"
        ],
        "md5": "cc98b13869c78ad3ef069d3a1c4ebaf4",
        "size compressed (bytes)": 33573641204,
        "total_terms": 1204542769110,
        "documents": 124131414,
        "unique_terms": 29168,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-unicoil-noexp-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220808.4d6d2a.tar.gz"
        ],
        "md5": "e70c3bf0016407bf20cfe35fb0d277e0",
        "size compressed (bytes)": 29059155839,
        "total_terms": 820664704261,
        "documents": 124131404,
        "unique_terms": 29172,
        "downloaded": False
    },

    # BEIR (v1.0.0) impact indexes encoded by SPLADE-distill CoCodenser-medium
    "beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-COVID encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "0f91fb01fec4b1c590fe683ad2383339",
        "size compressed (bytes)": 55889585,
        "total_terms": 1697942549,
        "documents": 171332,
        "unique_terms": 26611,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): BioASQ encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "a0317f26b1fab3bca71b46e0a4eff816",
        "size compressed (bytes)": 5396189427,
        "total_terms": 181960155708,
        "documents": 14914603,
        "unique_terms": 27703,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): NFCorpus encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "9c6f3ecfa6186c3ab5125f5c3d4eb962",
        "size compressed (bytes)": 1439110,
        "total_terms": 41582222,
        "documents": 3633,
        "unique_terms": 16295,
        "downloaded": False
    },
    "beir-v1.0.0-nq-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): NQ encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "9d418f806b8304a075945afa80bfcc22",
        "size compressed (bytes)": 833470407,
        "total_terms": 21901570532,
        "documents": 2681468,
        "unique_terms": 28747,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): HotpotQA encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "e96767f3d97cba5104dfd76eafdb35b7",
        "size compressed (bytes)": 1173403732,
        "total_terms": 32565190895,
        "documents": 5233329,
        "unique_terms": 28724,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): FiQA-2018 encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "937f0112a77a81879d6e42431d7fd522",
        "size compressed (bytes)": 19624314,
        "total_terms": 487502241,
        "documents": 57638,
        "unique_terms": 26244,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): Signal-1M encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "ac79812f60bcd597d351174a58fb085c",
        "size compressed (bytes)": 602427178,
        "total_terms": 13103073741,
        "documents": 2866316,
        "unique_terms": 28130,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-NEWS encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "d24ca30cb52510d193f9361e7f6996b7",
        "size compressed (bytes)": 270800660,
        "total_terms": 7519025445,
        "documents": 594977,
        "unique_terms": 27745,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): Robust04 encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "24e6310cd04a73604a8b467e582d153f",
        "size compressed (bytes)": 213476457,
        "total_terms": 6718533167,
        "documents": 528155,
        "unique_terms": 27623,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): ArguAna encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "d008e420e5be96ab7e9d40bafc3183ce",
        "size compressed (bytes)": 3816904,
        "total_terms": 96421121,
        "documents": 8674,
        "unique_terms": 22536,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): Webis-Touche2020 encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "e05433f5cd3113b50b5fe166e18975d4",
        "size compressed (bytes)": 124322238,
        "total_terms": 3229042324,
        "documents": 382545,
        "unique_terms": 27742,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-android encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "753c02411a6391e5d45ba39fdc30a535",
        "size compressed (bytes)": 5995405,
        "total_terms": 157949889,
        "documents": 22998,
        "unique_terms": 18891,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-english encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "f377274f93d9f6426034fdd78457f5ee",
        "size compressed (bytes)": 9857825,
        "total_terms": 218761119,
        "documents": 40221,
        "unique_terms": 26613,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gaming encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "a8549ec6b7af25fe4a60fd7f4827afbd",
        "size compressed (bytes)": 12976249,
        "total_terms": 296073202,
        "documents": 45301,
        "unique_terms": 24564,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gis encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "26341f18a352668986bc8cf82006dc38",
        "size compressed (bytes)": 10250646,
        "total_terms": 296967034,
        "documents": 37637,
        "unique_terms": 22034,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-mathematica encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "799a7c044cc774b29e55de4a8c0a813b",
        "size compressed (bytes)": 4771584,
        "total_terms": 132796971,
        "documents": 16705,
        "unique_terms": 19765,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-physics encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "75ed5bb0217ba4f1c957bc25109f2823",
        "size compressed (bytes)": 10887180,
        "total_terms": 284896455,
        "documents": 38316,
        "unique_terms": 22985,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-programmers encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "42e2da2036a3e1d5780c90cda8c2193e",
        "size compressed (bytes)": 10036425,
        "total_terms": 258856106,
        "documents": 32176,
        "unique_terms": 22560,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-stats encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "50043a036497ea6533fd2ce62f151370",
        "size compressed (bytes)": 11867711,
        "total_terms": 333590386,
        "documents": 42269,
        "unique_terms": 23322,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-tex encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "83026f984c1007c656f15d7c01cf5da0",
        "size compressed (bytes)": 19613041,
        "total_terms": 604604076,
        "documents": 68184,
        "unique_terms": 24669,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-unix encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "5bb2b4999e8769aca00c7dff2baaf297",
        "size compressed (bytes)": 12705584,
        "total_terms": 369576280,
        "documents": 47382,
        "unique_terms": 21712,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-webmasters encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "bb2b4227659f8f32e1fcd4d7dee6065c",
        "size compressed (bytes)": 4987493,
        "total_terms": 127823828,
        "documents": 17405,
        "unique_terms": 20286,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-wordpress encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "2acbaa7b2a0f8699e54fdee2efb2d376",
        "size compressed (bytes)": 12583602,
        "total_terms": 362488001,
        "documents": 48605,
        "unique_terms": 21867,
        "downloaded": False
    },
    "beir-v1.0.0-quora-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): Quora encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "6358d683527284ecf4c1dbb6ad008a0f",
        "size compressed (bytes)": 51880975,
        "total_terms": 1322737004,
        "documents": 522931,
        "unique_terms": 27042,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): DBPedia encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "9cb05766611bea863a96818219657c78",
        "size compressed (bytes)": 1225612002,
        "total_terms": 30490098411,
        "documents": 4635922,
        "unique_terms": 28709,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): SCIDOCS encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "38d2a4bbabf9b6b1cd627ce81660e07d",
        "size compressed (bytes)": 11252695,
        "total_terms": 273175826,
        "documents": 25657,
        "unique_terms": 24241,
        "downloaded": False
    },
    "beir-v1.0.0-fever-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): FEVER encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "cc71baa5838edd4e7cd288ca26488532",
        "size compressed (bytes)": 1497554696,
        "total_terms": 38844967407,
        "documents": 5416568,
        "unique_terms": 28670,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): Climate-FEVER encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "1479d75cd9496a7d57064b86f6ee67ef",
        "size compressed (bytes)": 1497450545,
        "total_terms": 38845226073,
        "documents": 5416593,
        "unique_terms": 28670,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-splade_distil_cocodenser_medium": {
        "description": "Lucene impact index of BEIR (v1.0.0): SciFact encoded by SPLADE-distill CoCodenser-medium",
        "filename": "lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-splade_distil_cocodenser_medium.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20221116.505594.tar.gz"
        ],
        "md5": "367db6c4a466d442ba089a38dad9fc6e",
        "size compressed (bytes)": 2173167,
        "total_terms": 65836037,
        "documents": 5183,
        "unique_terms": 17486,
        "downloaded": False
    },
}

IMPACT_INDEX_INFO_DEPRECATED = {

    # Deprecated: Lucene 8 indexes
    "msmarco-v2-passage-unicoil-0shot-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL. (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-passage-unicoil-0shot.20220219.6a7080.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-unicoil-0shot.20220219.6a7080.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-unicoil-0shot.20220219.6a7080.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/SCskjTJLX4CExkF/download"
        ],
        "md5": "ea024b0dd43a574deb65942e14d32630",
        "size compressed (bytes)": 22212154603,
        "total_terms": 775253560148,
        "documents": 138364198,
        "unique_terms": 29149,
        "downloaded": False
    },
    "msmarco-v2-passage-unicoil-noexp-0shot-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL (noexp). (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220219.6a7080.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220219.6a7080.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-unicoil-noexp-0shot.20220219.6a7080.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/FmW6N5FpMCyjMCE/download"
        ],
        "md5": "fb356e7614afc07e330b0559ae5cef18",
        "size compressed (bytes)": 14615689637,
        "total_terms": 411330032512,
        "documents": 138364198,
        "unique_terms": 29148,
        "downloaded": False
    },
    "msmarco-v2-passage-unicoil-tilde-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL-TILDE. (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-passage.unicoil-tilde.20211012.58d286.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.unicoil-tilde.20211012.58d286.readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage.unicoil-tilde.20211012.58d286.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/oGQ8tWifozPaHLK/download"
        ],
        "md5": "562f9534eefe04ab8c07beb304074d41",
        "size compressed (bytes)": 31168302160,
        "total_terms": 1155211154985,
        "documents": 138364198,
        "unique_terms": 29149,
        "downloaded": False
    },

    "msmarco-v2-doc-segmented-unicoil-0shot-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL. (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220219.6a7080.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220219.6a7080.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-0shot.20220219.6a7080.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/7PTnyEGwNGoJjXm/download"
        ],
        "md5": "94fc8af0d08682f7c79ffb16d82dcfab",
        "size compressed (bytes)": 32787358081,
        "total_terms": 1185840285417,
        "documents": 124131414,
        "unique_terms": 29169,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-unicoil-0shot-v2-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL, with title prepended. (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot-v2.20220419.c47993.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-0shot-v2.20220419.c47993.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-0shot-v2.20220419.c47993.tar.gz"
        ],
        "md5": "109572d65098021642b33e0feecde057",
        "size compressed (bytes)": 33967003367,
        "total_terms": 1204542769110,
        "documents": 124131414,
        "unique_terms": 29168,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-unicoil-noexp-0shot-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp). (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220219.6a7080.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220219.6a7080.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot.20220219.6a7080.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/PoWYJzGJYx6nCik/download"
        ],
        "md5": "d7807b60087b630010e9c31b59d30b69",
        "size compressed (bytes)": 28640356748,
        "total_terms": 805830282591,
        "documents": 124131404,
        "unique_terms": 29172,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2-lucene8": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended. (Lucene 8)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2.20220419.c47993.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2.20220419.c47993.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2.20220419.c47993.tar.gz"
        ],
        "md5": "8a48373934ad45052b5267ba73cdcad0",
        "size compressed (bytes)": 29662349942,
        "total_terms": 820664704261,
        "documents": 124131404,
        "unique_terms": 29172,
        "downloaded": False
    },

    # These MS MARCO uniCOIL models are deprecated, but keeping around for archival reasons
    "msmarco-passage-unicoil-d2q": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by uniCOIL-d2q (deprecated; use msmarco-v1-passage-unicoil instead).",
        "filename": "lucene-index.msmarco-passage.unicoil-d2q.20211012.58d286.tar.gz",
        "readme": "lucene-index.msmarco-passage.unicoil-d2q.20211012.58d286.readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-passage.unicoil-d2q.20211012.58d286.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/LGoAAXM7ZEbyQ7y/download"
        ],
        "md5": "4a8cb3b86a0d9085a0860c7f7bb7fe99",
        "size compressed (bytes)": 1205104390,
        "total_terms": 44495093768,
        "documents": 8841823,
        "unique_terms": 27678,
        "downloaded": False
    },
    "msmarco-doc-per-passage-unicoil-d2q": {
        "description": "Lucene impact index of the MS MARCO doc corpus per passage expansion encoded by uniCOIL-d2q (deprecated; use msmarco-v1-doc-segmented-unicoil instead).",
        "filename": "lucene-index.msmarco-doc-per-passage-expansion.unicoil-d2q.20211012.58d286.tar.gz",
        "readme": "lucene-index.msmarco-doc-per-passage-expansion.unicoil-d2q.20211012.58d286.readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-doc-per-passage-expansion.unicoil-d2q.20211012.58d286.tar.gz",
        ],
        "md5": "44bfc848f9a77302b10a59c5b136eb95",
        "size compressed (bytes)": 5945466106,
        "total_terms": 214505277898,
        "documents": 20545677,
        "unique_terms": 29142,
        "downloaded": False
    },
    "msmarco-v2-passage-unicoil-noexp-0shot-deprecated": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus encoded by uniCOIL (zero-shot, no expansions) (deprecated; use msmarco-v2-passage-unicoil-noexp-0shot instead).",
        "filename": "lucene-index.msmarco-v2-passage.unicoil-noexp-0shot.20211012.58d286.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage.unicoil-noexp-0shot.20211012.58d286.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eXA2BHF8WQjdY8R/download"
        ],
        "md5": "8886a8d9599838bc6d8d61464da61086",
        "size compressed (bytes)": 14801476783,
        "total_terms": 411330032512,
        "documents": 138364198,
        "unique_terms": 29148,
        "downloaded": False
    },
    "msmarco-v2-doc-per-passage-unicoil-noexp-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 document corpus per passage encoded by uniCOIL (zero-shot, no expansions) (deprecated; msmarco-v2-doc-segmented-unicoil-noexp-0shot).",
        "filename": "lucene-index.msmarco-v2-doc-per-passage.unicoil-noexp-0shot.20211012.58d286.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-per-passage.unicoil-noexp-0shot.20211012.58d286.readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-per-passage.unicoil-noexp-0shot.20211012.58d286.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/BSrJmAFJywsRYXo/download"
        ],
        "md5": "1980db886d969c3393e4da20190eaa8f",
        "size compressed (bytes)": 29229949764,
        "total_terms": 805830282591,
        "documents": 124131404,
        "unique_terms": 29172,
        "downloaded": False
    },

    # BEIR (v1.0.0) impact indexes encoded by SPLADE-distill CoCodenser-medium (Lucene 8; deprecated)
    "beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-COVID encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "b9c3837f2421667ba48adb84fcb599aa",
        "size compressed (bytes)": 57011989,
        "total_terms": 1697942549,
        "documents": 171332,
        "unique_terms": 26611,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): BioASQ encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "96ebb0b9016d9894e9784fa71ad7595d",
        "size compressed (bytes)": 5474720263,
        "total_terms": 181960155708,
        "documents": 14914603,
        "unique_terms": 27703,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): NFCorpus encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "7f5ec129305d630a18d63f188e08aa22",
        "size compressed (bytes)": 1445273,
        "total_terms": 41582222,
        "documents": 3633,
        "unique_terms": 16295,
        "downloaded": False
    },
    "beir-v1.0.0-nq-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): NQ encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "026dc3c2ed7292e7549ce4ff9ae2c318",
        "size compressed (bytes)": 859416460,
        "total_terms": 21901570532,
        "documents": 2681468,
        "unique_terms": 28747,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): HotpotQA encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "3edf537dfed5a9274ba56ef58ab090f6",
        "size compressed (bytes)": 1197602761,
        "total_terms": 32565190895,
        "documents": 5233329,
        "unique_terms": 28724,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): FiQA-2018 encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "a6ff07fe2a75f30838c3faf7c133efc1",
        "size compressed (bytes)": 19858617,
        "total_terms": 487502241,
        "documents": 57638,
        "unique_terms": 26244,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): Signal-1M encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "6d1fedefd3cb3a08820edc9552dd44b6",
        "size compressed (bytes)": 611827346,
        "total_terms": 13103073741,
        "documents": 2866316,
        "unique_terms": 28130,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-NEWS encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "05faf28e84259629aceb4d39d52471db",
        "size compressed (bytes)": 278203568,
        "total_terms": 7519025445,
        "documents": 594977,
        "unique_terms": 27745,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): Robust04 encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "c2c7f69edf7bc0edf2ede9d88f4d0402",
        "size compressed (bytes)": 217727819,
        "total_terms": 6718533167,
        "documents": 528155,
        "unique_terms": 27623,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): ArguAna encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "2dbb3cdd8412697cc336197912783eb2",
        "size compressed (bytes)": 3866879,
        "total_terms": 96421121,
        "documents": 8674,
        "unique_terms": 22536,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): Webis-Touche2020 encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "ff5cb006fac08086c575109e0ac80a1c",
        "size compressed (bytes)": 126819142,
        "total_terms": 3229042324,
        "documents": 382545,
        "unique_terms": 27742,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-android encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "1fb9462d93a21293a0c7aedd26653158",
        "size compressed (bytes)": 6068305,
        "total_terms": 157949889,
        "documents": 22998,
        "unique_terms": 18891,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-english encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "12f4581a96b775166210b462a78f72e3",
        "size compressed (bytes)": 9955691,
        "total_terms": 218761119,
        "documents": 40221,
        "unique_terms": 26613,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gaming encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "310750f0cbe930fd521d875b6df7a61f",
        "size compressed (bytes)": 13104645,
        "total_terms": 296073202,
        "documents": 45301,
        "unique_terms": 24564,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gis encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "3b42c73ccc278cc0bb823829867c6fce",
        "size compressed (bytes)": 10380891,
        "total_terms": 296967034,
        "documents": 37637,
        "unique_terms": 22034,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-mathematica encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "5b9d594270ff7417aabf1e9ca0a5bdf5",
        "size compressed (bytes)": 4823160,
        "total_terms": 132796971,
        "documents": 16705,
        "unique_terms": 19765,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-physics encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "a520cde380062b58f52c90e15d05e445",
        "size compressed (bytes)": 11011175,
        "total_terms": 284896455,
        "documents": 38316,
        "unique_terms": 22985,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-programmers encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "a90bd4f1185184881cbeaae095eb9e6f",
        "size compressed (bytes)": 10146685,
        "total_terms": 258856106,
        "documents": 32176,
        "unique_terms": 22560,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-stats encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "33f8e2025e89fd637806fe3083b61e86",
        "size compressed (bytes)": 12016946,
        "total_terms": 333590386,
        "documents": 42269,
        "unique_terms": 23322,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-tex encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "c20a0543a3ed90cf0ac8a2f4f52a8f7a",
        "size compressed (bytes)": 19883333,
        "total_terms": 604604076,
        "documents": 68184,
        "unique_terms": 24669,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-unix encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "7fdc9d04b7a3ced70bdef10e1bf92a09",
        "size compressed (bytes)": 12857043,
        "total_terms": 369576280,
        "documents": 47382,
        "unique_terms": 21712,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-webmasters encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "71a8d47e53a7befd43d4e29827699bfd",
        "size compressed (bytes)": 5044024,
        "total_terms": 127823828,
        "documents": 17405,
        "unique_terms": 20286,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-wordpress encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "370d0a704300987447a884bce28b0057",
        "size compressed (bytes)": 12737602,
        "total_terms": 362488001,
        "documents": 48605,
        "unique_terms": 21867,
        "downloaded": False
    },
    "beir-v1.0.0-quora-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): Quora encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "0fc0e726e877bfcc65f00d11e62d014a",
        "size compressed (bytes)": 52687112,
        "total_terms": 1322737004,
        "documents": 522931,
        "unique_terms": 27042,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): DBPedia encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "3e0979e02c97ee76ae30b1bf135ac2c8",
        "size compressed (bytes)": 1230929506,
        "total_terms": 30490098411,
        "documents": 4635922,
        "unique_terms": 28709,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): SCIDOCS encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "ac689f1bcf15d858fdbec70e692f9642",
        "size compressed (bytes)": 11401355,
        "total_terms": 273175826,
        "documents": 25657,
        "unique_terms": 24241,
        "downloaded": False
    },
    "beir-v1.0.0-fever-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): FEVER encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "99ac85688f3bee09a14334a02e0bc06c",
        "size compressed (bytes)": 1504352314,
        "total_terms": 38844967407,
        "documents": 5416568,
        "unique_terms": 28670,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): Climate-FEVER encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "60956badd9028ad18adfaf0a87e2c2d7",
        "size compressed (bytes)": 1504855696,
        "total_terms": 38845226073,
        "documents": 5416593,
        "unique_terms": 28670,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-splade_distil_cocodenser_medium-lucene8": {
        "description": "Lucene impact index of BEIR (v1.0.0): SciFact encoded by SPLADE-distill CoCodenser-medium. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20220501.1842ee.tar.gz"
        ],
        "md5": "bb0f30dad94daa06766da55ae615091d",
        "size compressed (bytes)": 2184301,
        "total_terms": 65836037,
        "documents": 5183,
        "unique_terms": 17486,
        "downloaded": False
    }

}

IMPACT_INDEX_INFO = {**IMPACT_INDEX_INFO_CURRENT, **IMPACT_INDEX_INFO_DEPRECATED}

FAISS_INDEX_INFO = {
    # BEIR (v1.0.0) contriever indexes
    "beir-v1.0.0-trec-covid.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-COVID) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz"
        ],
        "md5": "5b5baf557979e30e943180627fe31340",
        "size compressed (bytes)": 488100317,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (BioASQ) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-bioasq.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-bioasq.contriever.20230124.tar.gz"
        ],
        "md5": "c0cbca535d38c1f1f78ff1bd6d91af5d",
        "size compressed (bytes)": 42417202460,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (NFCorpus) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz"
        ],
        "md5": "5eff0107f7953ebe7658c3a6400e7027",
        "size compressed (bytes)": 10322409,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (NQ) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-nq.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-nq.contriever.20230124.tar.gz"
        ],
        "md5": "e1825fe0ce5c8000b63b1499374adb0e",
        "size compressed (bytes)": 7617697503,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (HotpotQA) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz"
        ],
        "md5": "51445960e00a18264ae3947b3af2bc80",
        "size compressed (bytes)": 14874721901,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (FiQA-2018) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-fiqa.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-fiqa.contriever.20230124.tar.gz"
        ],
        "md5": "a03cc30459b1a1928b93ad1aa51a7849",
        "size compressed (bytes)": 164024764,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (Signal-1M) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-signal1m.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-signal1m.contriever.20230124.tar.gz"
        ],
        "md5": "19e3e324b7b87e55fb9f6b6b1e72c464",
        "size compressed (bytes)": 8142533760,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-NEWS) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-trec-news.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-trec-news.contriever.20230124.tar.gz"
        ],
        "md5": "20db6299b57b3e78ea2f8b7a2b649770",
        "size compressed (bytes)": 1629958623,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (Robust04) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-robust04.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-robust04.contriever.20230124.tar.gz"
        ],
        "md5": "81c730b68e066baf18d5b46918b8c830",
        "size compressed (bytes)": 1501110333,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (ArguAna) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-arguana.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-arguana.contriever.20230124.tar.gz"
        ],
        "md5": "03f701916d49dd86b9c8989796d2dcc4",
        "size compressed (bytes)": 24710561,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (Webis-Touche2020) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz"
        ],
        "md5": "dfff9bc58521f09542f0affa3069f9a7",
        "size compressed (bytes)": 1091320704,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-android) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz"
        ],
        "md5": "4f03c0238f0e8f77e6365b61108042ed",
        "size compressed (bytes)": 65447231,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-english) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz"
        ],
        "md5": "319e3cba8f5f5d5175aad92c99c4b0fd",
        "size compressed (bytes)": 114460495,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gaming) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz"
        ],
        "md5": "049f2cb22adfb5803a5f7f762f578bce",
        "size compressed (bytes)": 128906099,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gis) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz"
        ],
        "md5": "13fdfa5a13634c10c1e7e6179bb4c376",
        "size compressed (bytes)": 107128974,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-mathematica) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz"
        ],
        "md5": "e4f756eede3ae5f9228d32096c1bd5b4",
        "size compressed (bytes)": 47544559,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-physics) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz"
        ],
        "md5": "b92ec0c233a1112d6f8782fb0f2bc9c1",
        "size compressed (bytes)": 109048286,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-programmers) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz"
        ],
        "md5": "f180240f35e2a3c27d39361a20533205",
        "size compressed (bytes)": 91583135,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-stats) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz"
        ],
        "md5": "64737df62b4e03b93356ba234cefe0e6",
        "size compressed (bytes)": 120288620,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-tex) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz"
        ],
        "md5": "ef087faff49e5bae0799e8576e387c0d",
        "size compressed (bytes)": 194080724,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-unix) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz"
        ],
        "md5": "9279884bfc3a14c2896276b679a58dbf",
        "size compressed (bytes)": 134860159,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-webmasters) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz"
        ],
        "md5": "f1a46fc6f6586c716d2a6239753c9573",
        "size compressed (bytes)": 49531545,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-wordpress) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz"
        ],
        "md5": "27480c7a4c8d437af30618bf98b10969",
        "size compressed (bytes)": 138348184,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (Quora) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-quora.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-quora.contriever.20230124.tar.gz"
        ],
        "md5": "4876145908b7af946593df6dbb8af600",
        "size compressed (bytes)": 1485866217,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (DBPedia) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz"
        ],
        "md5": "ee88a23de31d3faf403673c08ea0c844",
        "size compressed (bytes)": 13214316305,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (SCIDOCS) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-scidocs.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-scidocs.contriever.20230124.tar.gz"
        ],
        "md5": "dd1555b714c482a22cbb74d8c72599c9",
        "size compressed (bytes)": 73532556,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (FEVER) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-fever.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-fever.contriever.20230124.tar.gz"
        ],
        "md5": "d5b738dc38e56857a987bdb1eb4ce5c1",
        "size compressed (bytes)": 15437918827,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (Climate-FEVER) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz"
        ],
        "md5": "1e169cf6a8baaa4909f6823e3c23a80f",
        "size compressed (bytes)": 15437988868,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.contriever": {
        "description": "Faiss index for BEIR v1.0.0 (SciFact) corpus encoded by Contriever encoder.",
        "filename": "faiss.beir-v1.0.0-scifact.contriever.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-scifact.contriever.20230124.tar.gz"
        ],
        "md5": "61eb253aa08c9c97fa2f82ef2a96ca7b",
        "size compressed (bytes)": 14753553,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },

    # BEIR (v1.0.0) contriever ft MSMARCO indexes
    "beir-v1.0.0-trec-covid.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-COVID) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "7dd33fbd77deba89174b6d1b2c34866c",
        "size compressed (bytes)": 487986935,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat",
    },
    "beir-v1.0.0-bioasq.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (BioASQ) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "e51924bb78555942f0a9465959a6f6f2",
        "size compressed (bytes)": 42438279267,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat",
    },
    "beir-v1.0.0-nfcorpus.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (NFCorpus) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "657649d19fafd06cb031c6b11868d7f9",
        "size compressed (bytes)": 10327231,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat",
    },
    "beir-v1.0.0-nq.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (NQ) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "8d7ff2e5e285b1549bb8af27a7cf6e30",
        "size compressed (bytes)": 7619790303,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat",
    },
    "beir-v1.0.0-hotpotqa.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (HotpotQA) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "bef5b2fba77859c778f121ae2f17c9f1",
        "size compressed (bytes)": 14889518902,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat",
    },
    "beir-v1.0.0-fiqa.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (FiQA-2018) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "3dd16db861dbef4da545ccbea127198a",
        "size compressed (bytes)": 163998627,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat",
    },
    "beir-v1.0.0-signal1m.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (Signal-1M) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c4e25dc99c27a9d1931ad129d4091da0",
        "size compressed (bytes)": 8146484698,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat",
    },
    "beir-v1.0.0-trec-news.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-NEWS) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "22272011f0e0dea7f66b624de196b6b3",
        "size compressed (bytes)": 1629437319,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat",
    },
    "beir-v1.0.0-robust04.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (Robust04) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a2a0603fae866e1e92abcdfc46de6fe5",
        "size compressed (bytes)": 1501089289,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat",
    },
    "beir-v1.0.0-arguana.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (ArguAna) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "dcc0408ab033433d47363f5902fbde3d",
        "size compressed (bytes)": 24705859,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat",
    },
    "beir-v1.0.0-webis-touche2020.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (Webis-Touche2020) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "60072a3b32855067fea0f8e21ce0d905",
        "size compressed (bytes)": 1090748271,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat",
    },
    "beir-v1.0.0-cqadupstack-android.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-android) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "f9b02c2410fc8ddf63e96ea6ebbd8447",
        "size compressed (bytes)": 65438882,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat",
    },
    "beir-v1.0.0-cqadupstack-english.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-english) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "7c50f04a61a08f16dfb1d28010b4e222",
        "size compressed (bytes)": 114462161,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat",
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gaming) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "d97fafe933ae40fc12a9df0afc6a8e78",
        "size compressed (bytes)": 128896840,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat",
    },
    "beir-v1.0.0-cqadupstack-gis.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gis) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "f536d8feda0069a1769ad71010fab0e3",
        "size compressed (bytes)": 107086862,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat",
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-mathematica) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "987fb7ac275baf344828cdda0013703d",
        "size compressed (bytes)": 47526982,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat",
    },
    "beir-v1.0.0-cqadupstack-physics.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-physics) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "e252b1c4dcb06d2183109dc4bc820176",
        "size compressed (bytes)": 109024692,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat",
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-programmers) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "09bd10b2b06c7b0c7611e7811958f4b3",
        "size compressed (bytes)": 91567840,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat",
    },
    "beir-v1.0.0-cqadupstack-stats.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-stats) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c4586c11a2bc90f9ea5a3355fc6e6c53",
        "size compressed (bytes)": 120271253,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat",
    },
    "beir-v1.0.0-cqadupstack-tex.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-tex) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c3c5ec87aeb33a7320c0d61146c03fc0",
        "size compressed (bytes)": 194009234,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat",
    },
    "beir-v1.0.0-cqadupstack-unix.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-unix) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "3220f3eb0e9f0095cf13dcc8eb3ae1e0",
        "size compressed (bytes)": 134821535,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat",
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-webmasters) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "f696855c02090833a6ca695f8efa3006",
        "size compressed (bytes)": 49530869,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat",
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-wordpress) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "e92063c046803a76010b57e0ef1ace9e",
        "size compressed (bytes)": 138328541,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat",
    },
    "beir-v1.0.0-quora.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (Quora) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "82481f11087ebf63156da1f3dda00d5e",
        "size compressed (bytes)": 1487402659,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat",
    },
    "beir-v1.0.0-dbpedia-entity.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (DBPedia) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "5b9249745aa548776a8f22269bd55dbe",
        "size compressed (bytes)": 13226846024,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat",
    },
    "beir-v1.0.0-scidocs.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (SCIDOCS) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "091d751629ae22d843ce741f05f00b81",
        "size compressed (bytes)": 73530332,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat",
    },
    "beir-v1.0.0-fever.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (FEVER) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c1e9851e23c9f46e7210aedd613e4a1b",
        "size compressed (bytes)": 15444001312,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat",
    },
    "beir-v1.0.0-climate-fever.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (Climate-FEVER) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "1ec289569b80edb25d885100feba83aa",
        "size compressed (bytes)": 15444073223,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat",
    },
    "beir-v1.0.0-scifact.contriever-msmarco": {
        "description": "Faiss index for BEIR v1.0.0 (SciFact) corpus encoded by Contriever encoder that has been fine-tuned with MS MARCO passage.",
        "filename": "faiss.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "e560d5de0ccb65f66853540cb6917369",
        "size compressed (bytes)": 14758747,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat",
    },

    "msmarco-passage-tct_colbert-hnsw": {
        "description": "Faiss HNSW index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "dindex-msmarco-passage-tct_colbert-hnsw-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-tct_colbert-hnsw-20210112-be7119.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/F6MjyjmCi6yHFTa/download"
        ],
        "md5": "7e12ae728ea5f2ae6d1cfb88a8775ba8",
        "size compressed (bytes)": 33359100887,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-tct_colbert-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "dindex-msmarco-passage-tct_colbert-bf-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-tct_colbert-bf-20210112-be7119.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/mHxezzSAkrWbXZC/download"
        ],
        "md5": "7312e0e7acec2a686e994902ca064fc5",
        "size compressed (bytes)": 25204514289,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-doc-tct_colbert-bf": {
        "description": "Faiss FlatIP index of the MS MARCO document corpus encoded by TCT-ColBERT",
        "filename": "dindex-msmarco-doc-tct_colbert-bf-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-doc-tct_colbert-bf-20210112-be7119.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Ti5JxdCgjdw3noq/download"
        ],
        "md5": "f0b4c3bff3bb685be5c475511004c3b0",
        "size compressed (bytes)": 58514325936,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-doc-tct_colbert-v2-hnp-bf": {
        "description": "Faiss FlatIP index of the MS MARCO document corpus encoded by TCT-ColBERT-V2-HNP",
        "filename": "faiss-flat.msmarco-doc-per-passage.tct_colbert-v2-hnp.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss-flat.msmarco-doc-per-passage.tct_colbert-v2-hnp.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/XjkKAWMz2fwSeJB/download",
        ],
        "md5": "c6a7d295cfe711ef84dffe9ba6a702e5",
        "size compressed (bytes)": 58586765624,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "wikipedia-dpr-multi-bf": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on multiple QA datasets",
        "filename": "dindex-wikipedia-dpr_multi-bf-20200127-f403c3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-wikipedia-dpr_multi-bf-20200127-f403c3.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/xN44ZSC9tFFtp3F/download"
        ],
        "md5": "29eb39fe0b00a03c36c0eeae4c24f775",
        "size compressed (bytes)": 59836766981,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "wikipedia-dpr-single-nq-bf": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on NQ",
        "filename": "dindex-wikipedia-dpr_single_nq-bf-20200115-cd5034.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-wikipedia-dpr_single_nq-bf-20200115-cd5034.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/W4k44aLZWcbcJXe/download"
        ],
        "md5": "d1ef9286ddb38633cd052171963c62cb",
        "size compressed (bytes)": 59836863670,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "wikipedia-bpr-single-nq-hash": {
        "description": "Faiss binary index of Wikipedia encoded by the BPR doc encoder trained on NQ",
        "filename": "dindex-wikipedia_bpr_single_nq-hash-20210827-8a8f75.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-wikipedia_bpr_single_nq-hash-20210827-8a8f75.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/qKFrptGP4pSp987/download"
        ],
        "md5": "e60e5ed1d7fab924bfa9149ed169d082",
        "size compressed (bytes)": 1887382350,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "msmarco-passage-ance-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the ANCE MS MARCO passage encoder",
        "filename": "dindex-msmarco-passage-ance-bf-20210224-060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-ance-bf-20210224-060cef.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/mntwDQtXc9WbZSM/download"
        ],
        "md5": "f6332edb8f06ba796850388cf975b414",
        "size compressed (bytes)": 25102344985,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-doc-ance-maxp-bf": {
        "description": "Faiss FlatIP index of the MS MARCO document corpus encoded by the ANCE MaxP encoder",
        "filename": "dindex-msmarco-doc-ance_maxp-bf-20210304-b2a1b0.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-doc-ance_maxp-bf-20210304-b2a1b0.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/ifXbHmgTz27SYCC/download"
        ],
        "md5": "a9f8d77ea0cef7c6acdba881c45b7d99",
        "size compressed (bytes)": 58312805496,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc"
    },
    "wikipedia-ance-multi-bf": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the ANCE-multi encoder",
        "filename": "dindex-wikipedia-ance_multi-bf-20210224-060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-wikipedia-ance_multi-bf-20210224-060cef.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/XRGYFBN6d6WZRNw/download"
        ],
        "md5": "715605b56dc393b8f939e12682dfd467",
        "size compressed (bytes)": 59890492088,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "msmarco-passage-sbert-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the SBERT MS MARCO passage encoder",
        "filename": "dindex-msmarco-passage-sbert-bf-20210313-a0fbb3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-sbert-bf-20210313-a0fbb3.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/8xiZK5cx4ffExoz/download"
        ],
        "md5": "3f98b9564cd3a33e45bfeca4d4fec623",
        "size compressed (bytes)": 25214193901,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-distilbert-dot-margin_mse-T2-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the distilbert-dot-margin_mse-T2-msmarco passage encoder",
        "filename": "dindex-msmarco-passage-distilbert-dot-margin_mse-T2-20210316-d44c3a.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-distilbert-dot-margin_mse-T2-20210316-d44c3a.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/DSHYNJJRZLqckLA/download"
        ],
        "md5": "83a8081d6020910058164978b095615f",
        "size compressed (bytes)": 25162770962,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-distilbert-dot-tas_b-b256-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by msmarco-passage-distilbert-dot-tas_b-b256 passage encoder",
        "filename": "dindex-msmarco-passage-distilbert-dot-tas_b-b256-bf-20210527-63276f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-distilbert-dot-tas_b-b256-bf-20210527-63276f.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/89fr56FNeGFbyrG/download",
        ],
        "md5": "cc947bf66d9552a2a7c6fe060466e490",
        "size compressed (bytes)": 25162328596,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-tct_colbert-v2-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-tct_colbert-v2-bf-20210608-5f341b.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/2EZ2feACyL8cnw5/download",
        ],
        "md5": "479591e265347ceff954ae05f6d3462b",
        "size compressed (bytes)": 25211079381,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-tct_colbert-v2-hn-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hn passage encoder",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-hn-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-tct_colbert-v2-hn-bf-20210608-5f341b.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/2dP6EJz7QgywM4b/download",
        ],
        "md5": "61d38e4935b3ca36c99e0cda2b27fba2",
        "size compressed (bytes)": 25205729786,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-passage-tct_colbert-v2-hnp-bf": {
        "description": "Faiss FlatIP index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hnp passage encoder",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-hnp-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/dindex-msmarco-passage-tct_colbert-v2-hnp-bf-20210608-5f341b.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/od63ZXNadCZymwj/download",
        ],
        "md5": "c3c3fc3a288bcdf61708d4bba4bc79ff",
        "size compressed (bytes)": 25225528775,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "cast2019-tct_colbert-v2-hnsw": {
        "description": "Faiss HNSW index of the CAsT2019 passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "faiss-hnsw.cast2019.tct_colbert-v2.tar.gz",
        "readme": "faiss-hnsw.cast2019.tct_colbert-v2-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss-hnsw.cast2019.tct_colbert-v2.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/ncrZdE67BCKxPwc/download"
        ],
        "md5": "fa7673509b34d978e1b931d5705369ee",
        "size compressed (bytes)": 112121366773,
        "documents": 38429835,
        "downloaded": False,
        "texts": "cast2019"
    },
    "mrtydi-v1.1-arabic-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-arabic.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Jgj3rYjbyRrmJs8/download"  # Note, this is Crystina's account.
        ],
        "md5": "de86c1ce43854bbeea4e3af5d95d6ffb",
        "size compressed (bytes)": 5997943791,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-bengali.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/4PpkzXAQtXFFJHR/download"  # Note, this is Crystina's account.
        ],
        "md5": "e60cb6f1f7139cf0551f0ba4e4e83bf6",
        "size compressed (bytes)": 865716848,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-english.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/A7pjbwYeoT4Krnj/download"  # Note, this is Crystina's account.
        ],
        "md5": "a0a8cc39e8af782ec82188a18c4c97c3",
        "size compressed (bytes)": 93585951488,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-finnish.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/erNYkrYzRZxpecz/download"  # Note, this is Crystina's account.
        ],
        "md5": "3e4e18aacf07ca551b474315f267ead6",
        "size compressed (bytes)": 5435516778,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-indonesian.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/BpR3MzT7KJ6edx7/download"  # Note, this is Crystina's account.
        ],
        "md5": "0bf693e4046d9a565ae18b9f5939d193",
        "size compressed (bytes)": 865716848,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-japanese.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/k7bptHT8GwMJpnF/download"  # Note, this is Crystina's account.
        ],
        "md5": "4ba566e27bc0158108259b18a153e2fc",
        "size compressed (bytes)": 19920816424,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-korean.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/TigfYMde94YWAoE/download"  # Note, this is Crystina's account.
        ],
        "md5": "44212e5722632d5bcb14f0680741638c",
        "size compressed (bytes)": 4257414237,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-russian.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eN7demnmnspqxjk/download"  # Note, this is Crystina's account.
        ],
        "md5": "e7634093f2a3362928e9699441ce8a3b",
        "size compressed (bytes)": 27317759143,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-swahili.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/JgiX8PRftnqcPwy/download"  # Note, this is Crystina's account.
        ],
        "md5": "5061bdd1d81bc32490bbb3682096acdd",
        "size compressed (bytes)": 389658394,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-telugu.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/dkm6RGdgRbnwiX2/download"  # Note, this is Crystina's account.
        ],
        "md5": "4952dacaeae89185d3757f9f26af4e88",
        "size compressed (bytes)": 1561173721,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-thai.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220207.5df364.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/fFrRYefd3nWFR3J/download"  # Note, this is Crystina's account.
        ],
        "md5": "2458f704b277fa8ffe2509b6296892a0",
        "size compressed (bytes)": 1616059846,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },
    "wikipedia-dpr-dkrr-nq": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on NQ",
        "filename": "faiss-flat.wikipedia.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss-flat.wikipedia.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "e58886fd5485b84f2c44963ce644561b",
        "size compressed (bytes)": 37812137819,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "wikipedia-dpr-dkrr-tqa": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on TriviaQA",
        "filename": "faiss-flat.wikipedia.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss-flat.wikipedia.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "a6b02d33c9c0376ad1bf6550212ecdcb",
        "size compressed (bytes)": 37802648060,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "bafb6fb2c530567dec26aa4597c6ee25",
        "size compressed (bytes)": 5997943791,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic",
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "d04bb6e634fb4f7df23dbff7481a8f9b",
        "size compressed (bytes)": 865733058,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali",
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-english.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "4a93a2211199f7359cc99486a9f93d02",
        "size compressed (bytes)": 93594561391,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "6cbe2d52225fb15a494857b9df593113",
        "size compressed (bytes)": 5436419399,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "26108a7ee1fc5ac15e0b7fcecf4d39ad",
        "size compressed (bytes)": 4178791300,
        "documents": 1469399,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "2ef2b5e3f5778d99e65aafc48450508a",
        "size compressed (bytes)": 19918319452,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-korean.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "26ed9be031603019304b66f985ce154c",
        "size compressed (bytes)": 4256863335,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-russian.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "b1be7a45a702be4021f38425c0001f39",
        "size compressed (bytes)": 27318555548,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "14edb5f677820b5a5a3858555e900591",
        "size compressed (bytes)": 389600527,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "25b37f5d7a035a17b447f1732e241b85",
        "size compressed (bytes)": 1561419958,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-thai.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "0544ce677fa31b633a29a079c0cdfc82",
        "size compressed (bytes)": 1616716166,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },
    "mrtydi-v1.1-arabic-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220523.7b099d5.tar.gz",
        ],
        "md5": "3d764e7936bb6beb5308ccfd6717b38e",
        "size compressed (bytes)": 5988743258,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220523.7b099d5.tar.gz",
        ],
        "md5": "2ee8e550245f7eb5184c27fe3369d818",
        "size compressed (bytes)": 864358280,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220523.7b099d5.tar.gz",
        ],
        "md5": "a1be61486c209bf2545d63f950274a99",
        "size compressed (bytes)": 93435965796,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220523.7b099d5.tar.gz",
        ],
        "md5": "0dbd873fa8bf8c87052940bdf4097ba2",
        "size compressed (bytes)": 5427976705,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220523.7b099d5.tar.gz",
        ],
        "md5": "937f7c03e2386166e34ef81b25d7959f",
        "size compressed (bytes)": 4172976570,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220523.7b099d5.tar.gz",
        ],
        "md5": "21a64d1a012a854d4bf42fa24c8712fd",
        "size compressed (bytes)": 19890571158,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220523.7b099d5.tar.gz",
        ],
        "md5": "ed3216fb5bc431ac52931b58cc4c4d0f",
        "size compressed (bytes)": 4250320804,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220523.7b099d5.tar.gz",
        ],
        "md5": "c3c4db1397c7125f8e411cf637054148",
        "size compressed (bytes)": 27278520787,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220523.7b099d5.tar.gz",
        ],
        "md5": "20235115c0a877e11c91cb662d5a6fdb",
        "size compressed (bytes)": 389244265,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220523.7b099d5.tar.gz",
        ],
        "md5": "86cae6fe8f8c08489e49b6e6c28a09b0",
        "size compressed (bytes)": 1558691592,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220523.7b099d5.tar.gz",
        ],
        "md5": "3ba9c64a9f7479bd2e3a84a816ee0f6f",
        "size compressed (bytes)": 1613563144,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },
    "mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220524.7b099d5.tar.gz",
        ],
        "md5": "9ea47ae7425fd3376f015ca7c6ba5134",
        "size compressed (bytes)": 5988743258,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220524.7b099d5.tar.gz",
        ],
        "md5": "d1e75f4960a723b068bb778a972ffb54",
        "size compressed (bytes)": 864358280,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220524.7b099d5.tar.gz",
        ],
        "md5": "1fce43e549ff57bbac432a579961f34b",
        "size compressed (bytes)": 93435965796,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220524.7b099d5.tar.gz",
        ],
        "md5": "6faa7b2fe8ad4b9ca284bd7e8f69b727",
        "size compressed (bytes)": 5427976705,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220524.7b099d5.tar.gz",
        ],
        "md5": "659b1e0a1bea46f62a842b55385085b7",
        "size compressed (bytes)": 4172976570,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220524.7b099d5.tar.gz",
        ],
        "md5": "126c82da9e0e0e1fd290cf62d7fe4dfa",
        "size compressed (bytes)": 19890571158,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220524.7b099d5.tar.gz",
        ],
        "md5": "cf07b71aaefba58bbe150265f6696503",
        "size compressed (bytes)": 4250320804,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220524.7b099d5.tar.gz",
        ],
        "md5": "c0a53fa6428cb9b1399a90e3a9a805d5",
        "size compressed (bytes)": 27278520787,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220524.7b099d5.tar.gz",
        ],
        "md5": "93dc3f3453815c92f3bccf4f41c5f2d4",
        "size compressed (bytes)": 389244265,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220524.7b099d5.tar.gz",
        ],
        "md5": "7aba1b7ee36e572bd982b3f62f41c380",
        "size compressed (bytes)": 1558691592,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220524.7b099d5.tar.gz",
        ],
        "md5": "57151073a4c0d90b64242e4536a3af75",
        "size compressed (bytes)": 1613563144,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },

    "miracl-v1.0-ar-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "177d47e9a802c87abca52380ad1ce83b",
        "size compressed (bytes)": 5997943791,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "156e8ba8cd369b1c4a606e28ea025b2e",
        "size compressed (bytes)": 846825710,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "ce00518f54b130a157112c2a1b2d0980",
        "size compressed (bytes)": 93554329467,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "d7a9627bb60e901386f455ba6c9063ac",
        "size compressed (bytes)": 29553300598,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "e8b59e3eb2e08f61f81569c6d4c85350",
        "size compressed (bytes)": 6286832343,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a82d6e6cf964d2e4cfac99cf14cbcc35",
        "size compressed (bytes)": 5366190875,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a952d944aa63dcee604c8357f1be18db",
        "size compressed (bytes)": 41648462587,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "9d1dc4b948edf3df263977d82c9fcc3f",
        "size compressed (bytes)": 1440625097,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "19815233f5cc3a198b88cdb990459637",
        "size compressed (bytes)": 4115281873,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "6e9b6e304b2b1a192a3d81e55880f971",
        "size compressed (bytes)": 19791965448,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "ea1fa34341fc5d5ea88e5b633025d2d5",
        "size compressed (bytes)": 4231563116,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-korean"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "4325e716ee6af5ea2b73d4b25f1ad76c",
        "size compressed (bytes)": 27173379698,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2b879dac6823077ae497ba8ebfce523b",
        "size compressed (bytes)": 376181791,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a3dfb8ba31f316c93d1fd147f88fbbfd",
        "size compressed (bytes)": 1476021181,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "cb0c9b84a80ff338372b32857c58368d",
        "size compressed (bytes)": 1541590044,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2743dfaa794b7abbef1d3c912c5cc4b5",
        "size compressed (bytes)": 14046912361,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (German) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "1abcf3aac78e30ebe7a75163412f1c84",
        "size compressed (bytes)": 45154018897,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2ad15ea0576ae3284082ae661e001faa",
        "size compressed (bytes)": 139412730,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    },

    "miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "428fbde84d2c18e48f0821298947a9d1",
        "size compressed (bytes)": 5866199790,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "4394a09e043be9be5b820814a82fc8ac",
        "size compressed (bytes)": 846476050,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "5bd57f5e4daf93294fd2cbd969c05bb3",
        "size compressed (bytes)": 93527497283,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b6db16c1ab0ae95fec0465299c660d2a",
        "size compressed (bytes)": 29544413180,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "2a2825706211eb96bd3dbb616463c661",
        "size compressed (bytes)": 6283957262,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "65719de730cda3fa5f6a8a75611db6eb",
        "size compressed (bytes)": 5363289277,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "24eb2f63f78aa1e39b1ea61e20661424",
        "size compressed (bytes)": 41635104326,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "d08aad08a8592aa40355fb7d50afd170",
        "size compressed (bytes)": 1439798033,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b02c20d4fc27e390ec5b1e9ca732dc5a",
        "size compressed (bytes)": 4113737773,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5f219c7f46a36c5c7a2555fbdaa0479",
        "size compressed (bytes)": 19790154560,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "67b2a803eab3491a057d4ac6b81974f1",
        "size compressed (bytes)": 4230830690,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-korean"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "edad6d5cb508de61ba84173d0ad2aa31",
        "size compressed (bytes)": 27169921407,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "0b039d766b55f678102a59a6e050d0bc",
        "size compressed (bytes)": 375865677,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "ea21915c69f70f41acadee4b6b83d129",
        "size compressed (bytes)": 1474866678,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5875b473109310789710e2f3df91b0f",
        "size compressed (bytes)": 1540180247,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a2d233e792d46c20c912d10afff033f5",
        "size compressed (bytes)": 14043150097,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "d53da12ae6119ed54ef968e968f8520a",
        "size compressed (bytes)": 45139752128,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "0a1b0f48108508724a3892dfc04eb756",
        "size compressed (bytes)": 139286213,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    },

    "wiki-all-6-3-dpr2-multi": {
        "description": "Faiss FlatIP index of wiki-all-6-3-tamber encoded by a 2nd iteration DPR model trained on multiple QA datasets",
        "filename": "faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        "readme": "faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        ],
        "md5": "b77b8e296c339b6d76988ee5c2d3e96a",
        "size compressed (bytes)": 218257913793,
        "documents": 76680040,
        "downloaded": False,
        "texts": "wiki-all-6-3-tamber"
    },
    "miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-miracl-ar": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-miracl-ar.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-miracl-ar.20230329.e40d4a.tar.gz",
        ],
        "md5": "29cdb7fa7cc52cabc32791d57be3bd42",
        "size compressed (bytes)": 5871030506,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar"
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-miracl-bn": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-miracl-bn.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-miracl-bn.20230329.e40d4a.tar.gz",
        ],
        "md5": "8972166564a9c13e102ae83ea062c166",
        "size compressed (bytes)": 846236944,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn"
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-miracl-en": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-miracl-en.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-miracl-en.20230329.e40d4a.tar.gz",
        ],
        "md5": "cd43e6c93879a107b94396a42aa7c987",
        "size compressed (bytes)": 93502848095,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-miracl-es": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-miracl-es.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-miracl-es.20230329.e40d4a.tar.gz",
        ],
        "md5": "4f45c3171690dd691afcfc9e45b89494",
        "size compressed (bytes)": 29552466540,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-miracl-fa": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-miracl-fa.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-miracl-fa.20230329.e40d4a.tar.gz",
        ],
        "md5": "ae262fea849f6903c93e1f3269e07804",
        "size compressed (bytes)": 6287728719,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-miracl-fi": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-miracl-fi.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-miracl-fi.20230329.e40d4a.tar.gz",
        ],
        "md5": "12c5c5c4dd8df37ad8ae90039851fbec",
        "size compressed (bytes)": 5367069541,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-miracl-fr": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-miracl-fr.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-miracl-fr.20230329.e40d4a.tar.gz",
        ],
        "md5": "8cf28f8df0805a848cb5c54d5f5d8bfb",
        "size compressed (bytes)": 41654288474,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-miracl-hi": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-miracl-hi.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-miracl-hi.20230329.e40d4a.tar.gz",
        ],
        "md5": "f579dfa45a5f14c48f97ba9980f7dec8",
        "size compressed (bytes)": 1440859085,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-miracl-id": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-miracl-id.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-miracl-id.20230329.e40d4a.tar.gz",
        ],
        "md5": "d5b540fb82fe21c1fd2b56e248184af6",
        "size compressed (bytes)": 4111428848,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-miracl-ja": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-miracl-ja.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-miracl-ja.20230329.e40d4a.tar.gz",
        ],
        "md5": "e7ad21b12a7d5e937c55d49184d68814",
        "size compressed (bytes)": 19790420501,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-miracl-ko": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-miracl-ko.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-miracl-ko.20230329.e40d4a.tar.gz",
        ],
        "md5": "c31290dfae5429549500759279af3a8d",
        "size compressed (bytes)": 4230154713,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-ko"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-miracl-ru": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-miracl-ru.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-miracl-ru.20230329.e40d4a.tar.gz",
        ],
        "md5": "b9460efd096292a1012ab1d27082498e",
        "size compressed (bytes)": 27177739148,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-miracl-sw": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-miracl-sw.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-miracl-sw.20230329.e40d4a.tar.gz",
        ],
        "md5": "526a930a27353462e11cc7e1b794dcc7",
        "size compressed (bytes)": 375865597,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-miracl-te": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-miracl-te.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-miracl-te.20230329.e40d4a.tar.gz",
        ],
        "md5": "f64b28542afdd15b2fe3831972bcd91e",
        "size compressed (bytes)": 1475895517,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-miracl-th": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-miracl-th.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-miracl-th.20230329.e40d4a.tar.gz",
        ],
        "md5": "b6ba6d5363bf07a5dc8e1cd35fe11e93",
        "size compressed (bytes)": 1540581013,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-miracl-zh": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-miracl-zh.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-miracl-zh.20230329.e40d4a.tar.gz",
        ],
        "md5": "feba34e41cb8234988f7fb99bd8998f3",
        "size compressed (bytes)": 14049243202,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh"
    },
}

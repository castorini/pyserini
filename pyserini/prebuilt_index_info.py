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

INDEX_INFO = {
    "cacm": {
        "description": "CACM corpus",
        "filename": "lucene-index.cacm.tar.gz",
        "urls": [
            "https://github.com/castorini/anserini-data/raw/master/CACM/lucene-index.cacm.tar.gz",
        ],
        "md5": "e47164fbd18aab72cdc18aecc0744bb1",
        "size compressed (bytes)": 2372903,
        "total_terms": 320968,
        "documents": 3204,
        "unique_terms": 14363,
    },
    "robust04": {
        "description": "TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track",
        "filename": "index-robust04-20191213.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eqFacNeSGc4pLLH/download"
        ],
        "md5": "15f3d001489c97849a010b0a4734d018",
        "size compressed (bytes)": 1821814915,
        "total_terms": 174540872,
        "documents": 528030,
        "unique_terms": 923436,
    },
    "msmarco-passage": {
        "description": "MS MARCO passage corpus",
        "filename": "index-msmarco-passage-20201117-f87c94.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-passage-20201117-f87c94.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/QQsZMFG8MpF4P8M/download"
        ],
        "md5": "1efad4f1ae6a77e235042eff4be1612d",
        "size compressed (bytes)": 2218470796,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-passage-slim": {
        "description": "MS MARCO passage corpus (slim version, no documents)",
        "filename": "index-msmarco-passage-slim-20201202-ab6e28.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-passage-slim-20201202-ab6e28.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Kx6K9NJFmwnaAP8/download"
        ],
        "md5": "5e11da4cebd2e8dda2e73c589ffb0b4c",
        "size compressed (bytes)": 513566686,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-passage-expanded": {
        "description": "MS MARCO passage corpus (+ docTTTTTquery expansion)",
        "filename": "index-msmarco-passage-expanded-20201121-e127fb.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-passage-expanded-20201121-e127fb.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/pm7cisJtRxiAMHd/download"
        ],
        "md5": "e5762e9e065b6fe5000f9c18da778565",
        "size compressed (bytes)": 816438546,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },
    "msmarco-passage-ltr": {
        "description": "MS MARCO passage corpus (4 extra preprocessed fields) used for LTR pipeline",
        "filename": "index-msmarco-passage-ltr-20210519-e25e33f.tar.gz",
        "urls": [
            "https://vault.cs.uwaterloo.ca/s/8qFCaCtwabRfYQD/download" # too big for UWaterloo GitLab
        ],
        "md5": "a5de642c268ac1ed5892c069bdc29ae3",
        "size compressed (bytes)": 14073966046,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-doc": {
        "description": "MS MARCO document corpus",
        "filename": "index-msmarco-doc-20201117-f87c94.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-20201117-f87c94.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/5NC7A2wAL7opJKH/download"
        ],
        "md5": "ac747860e7a37aed37cc30ed3990f273",
        "size compressed (bytes)": 13642330935,
        "total_terms": 2748636047,
        "documents": 3213835,
        "unique_terms": 29823078,
        "downloaded": False
    },
    "msmarco-doc-slim": {
        "description": "MS MARCO document corpus (slim version, no documents)",
        "filename": "index-msmarco-doc-slim-20201202-ab6e28.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-slim-20201202-ab6e28.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/BMZ6oYBoEPgTFqs/download"
        ],
        "md5": "c56e752f7992bf6149761097641d515a",
        "size compressed (bytes)": 1874471867,
        "total_terms": 2748636047,
        "documents": 3213835,
        "unique_terms": 29823078,
        "downloaded": False
    },
    "msmarco-doc-per-passage": {
        "description": "MS MARCO document corpus, segmented into passages",
        "filename": "index-msmarco-doc-per-passage-20201204-f50dcc.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-per-passage-20201204-f50dcc.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/q6sAxE6q57q2TBo/download"
        ],
        "md5": "797367406a7542b649cefa6b41cf4c33",
        "size compressed (bytes)": 11602951258,
        "total_terms": 3197886407,
        "documents": 20544550,
        "unique_terms": 21173582,
        "downloaded": False
    },
    "msmarco-doc-per-passage-slim": {
        "description": "MS MARCO document corpus, segmented into passages (slim version, no documents)",
        "filename": "index-msmarco-doc-per-passage-slim-20201204-f50dcc.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-per-passage-slim-20201204-f50dcc.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/mKTjbTKMwWF9kY3/download"
        ],
        "md5": "77c2409943a8c9faffabf57cb6adca69",
        "size compressed (bytes)": 2834865200,
        "total_terms": 3197886407,
        "documents": 20544550,
        "unique_terms": 21173582,
        "downloaded": False
    },
    "msmarco-doc-expanded-per-doc": {
        "description": "MS MARCO document corpus, with per-doc docTTTTTquery expansion",
        "filename": "index-msmarco-doc-expanded-per-doc-20201126-1b4d0a.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-expanded-per-doc-20201126-1b4d0a.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/3BQz6ZAXAxtfne8/download"
        ],
        "md5": "f7056191842ab77a01829cff68004782",
        "size compressed (bytes)": 1978837253,
        "total_terms": 3748333319,
        "documents": 3213835,
        "unique_terms": 30627687,
        "downloaded": False
    },
    "msmarco-doc-expanded-per-passage": {
        "description": "MS MARCO document corpus, with per-passage docTTTTTquery expansion",
        "filename": "index-msmarco-doc-expanded-per-passage-20201126-1b4d0a.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-msmarco-doc-expanded-per-passage-20201126-1b4d0a.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eZLbPWcnB7LzKnQ/download"
        ],
        "md5": "54ea30c64515edf3c3741291b785be53",
        "size compressed (bytes)": 3069280946,
        "total_terms": 4203956960,
        "documents": 20544550,
        "unique_terms": 22037213,
        "downloaded": False
    },
    "enwiki-paragraphs": {
        "description": "English Wikipedia (for BERTserini)",
        "filename": "lucene-index.enwiki-20180701-paragraphs.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/lucene-index.enwiki-20180701-paragraphs.tar.gz",
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
        "description": "Chinese Wikipedia (for BERTserini)",
        "filename": "lucene-index.zhwiki-20181201-paragraphs.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/lucene-index.zhwiki-20181201-paragraphs.tar.gz",
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
        "description": "TREC-COVID Round 5: abstract index",
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
        "description": "TREC-COVID Round 5: full-text index",
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
        "description": "TREC-COVID Round 5: paragraph index",
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
        "description": "TREC-COVID Round 4: abstract index",
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
        "description": "TREC-COVID Round 4: full-text index",
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
        "description": "TREC-COVID Round 4: paragraph index",
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
        "description": "TREC-COVID Round 3: abstract index",
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
        "description": "TREC-COVID Round 3: full-text index",
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
        "description": "TREC-COVID Round 3: paragraph index",
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
        "description": "TREC-COVID Round 2: abstract index",
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
        "description": "TREC-COVID Round 2: full-text index",
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
        "description": "TREC-COVID Round 2: paragraph index",
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
        "description": "TREC-COVID Round 1: abstract index",
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
        "description": "TREC-COVID Round 1: full-text index",
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
        "description": "TREC-COVID Round 1: paragraph index",
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
        "description": "TREC 2019 CaST",
        "filename": "index-cast2019.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-cast2019.tar.gz",
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
        "description": "Wikipedia (DPR 100 word splits) Anserini index",
        "filename": "index-wikipedia-dpr-20210120-d1b9e6.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-wikipedia-dpr-20210120-d1b9e6.tar.gz",
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
        "description": "Wikipedia (DPR 100 word splits) Anserini index, without raw texts stored",
        "filename": "index-wikipedia-dpr-slim-20210120-d1b9e6.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-wikipedia-dpr-slim-20210120-d1b9e6.tar.gz",
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
        "description": "Wikipedia snapshot used as KILT's knowledge source. Indexed by documents.",
        "filename": "index-wikipedia-kilt-doc-20210421-f29307.tar.gz",
        "urls": [
            "https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-wikipedia-kilt-doc-20210421-f29307.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/RqtLg3CZT38k32c/download"
        ],
        "md5": "b8ec8feb654f7aaa86f9901dc6c804a8",
        "size compressed (bytes)": 10901127209,
        "total_terms": 1915061164,
        "documents": 5903530,
        "unique_terms": 8722502,
        "downloaded": False
    },
}

DINDEX_INFO = {
    "msmarco-passage-tct_colbert-hnsw": {
        "description": "MS MARCO passage corpus encoded by TCT-ColBERT and indexed as HNSW index",
        "filename": "dindex-msmarco-passage-tct_colbert-hnsw-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-tct_colbert-hnsw-20210112-be7119.tar.gz",
            "https://www.dropbox.com/s/xrsjn38lk3axfdd/dindex-msmarco-passage-tct_colbert-hnsw-20210112-be7119.tar.gz?dl=1"
        ],
        "md5": "7e12ae728ea5f2ae6d1cfb88a8775ba8",
        "size compressed (bytes)": 33359100887,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-tct_colbert-bf": {
        "description": "MS MARCO passage corpus encoded by TCT-ColBERT and indexed as brute force index",
        "filename": "dindex-msmarco-passage-tct_colbert-bf-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-tct_colbert-bf-20210112-be7119.tar.gz",
            "https://www.dropbox.com/s/sgmugleqwwirx3n/dindex-msmarco-passage-tct_colbert-bf-20210112-be7119.tar.gz?dl=1"
        ],
        "md5": "7312e0e7acec2a686e994902ca064fc5",
        "size compressed (bytes)": 25204514289,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-doc-tct_colbert-bf": {
        "description": "MS MARCO document corpus encoded by TCT-ColBERT and indexed as brute force index",
        "filename": "dindex-msmarco-doc-tct_colbert-bf-20210112-be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-doc-tct_colbert-bf-20210112-be7119.tar.gz",
            "https://www.dropbox.com/s/jse0j82l4ouqdna/dindex-msmarco-doc-tct_colbert-bf-20210112-be7119.tar.gz?dl=1"
        ],
        "md5": "f0b4c3bff3bb685be5c475511004c3b0",
        "size compressed (bytes)": 58514325936,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "wikipedia-dpr-multi-bf": {
        "description": "Wikipedia corpus encoded by DPR doc encoder trained on multiset, indexed as brute force index",
        "filename": "dindex-wikipedia-dpr_multi-bf-20200127-f403c3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-wikipedia-dpr_multi-bf-20200127-f403c3.tar.gz",
            "https://www.dropbox.com/s/9g4e2ps73lf4ysl/dindex-wikipedia-dpr_multi-bf-20200127-f403c3.tar.gz?dl=1"
        ],
        "md5": "29eb39fe0b00a03c36c0eeae4c24f775",
        "size compressed (bytes)": 59836766981,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "wikipedia-dpr-single-nq-bf": {
        "description": "Wikipedia corpus encoded by DPR doc encoder trained on NQ, indexed as brute force index",
        "filename": "dindex-wikipedia-dpr_single_nq-bf-20200115-cd5034.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-wikipedia-dpr_single_nq-bf-20200115-cd5034.tar.gz",
            "https://www.dropbox.com/s/negktsxze5sy7e2/dindex-wikipedia-dpr_single_nq-bf-20200115-cd5034.tar.gz?dl=1",
        ],
        "md5": "d1ef9286ddb38633cd052171963c62cb",
        "size compressed (bytes)": 59836863670,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "wikipedia-bpr-single-nq-hash": {
        "description": "Wikipedia corpus encoded by BPR doc encoder trained on NQ, indexed as faiss binary index",
        "filename": "dindex-wikipedia_bpr_single_nq-hash-20210827-8a8f75.tar.gz",
        "urls": [
            "https://www.dropbox.com/s/obz5q1td4f6o1l1/dindex-wikipedia_bpr_single_nq-hash-20210827-8a8f75.tar.gz?dl=1",
        ],
        "md5": "e60e5ed1d7fab924bfa9149ed169d082",
        "size compressed (bytes)": 1887382350,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "msmarco-passage-ance-bf": {
        "description": "MS MARCO passage corpus encoded by ANCE msmarco passage encoder and indexed as brute force index",
        "filename": "dindex-msmarco-passage-ance-bf-20210224-060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-ance-bf-20210224-060cef.tar.gz",
            "https://www.dropbox.com/s/ahpxwtgh56o6j2f/dindex-msmarco-passage-ance-bf-20210224-060cef.tar.gz?dl=1"
        ],
        "md5": "f6332edb8f06ba796850388cf975b414",
        "size compressed (bytes)": 25102344985,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-doc-ance-maxp-bf": {
        "description": "MS MARCO document corpus encoded by ANCE maxp encoder and indexed as brute force index",
        "filename": "dindex-msmarco-doc-ance_maxp-bf-20210304-b2a1b0.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-doc-ance_maxp-bf-20210304-b2a1b0.tar.gz",
            "https://www.dropbox.com/s/bddpw1nwcka7pdf/dindex-msmarco-doc-ance_maxp-bf-20210304-b2a1b0.tar.gz?dl=1"
        ],
        "md5": "a9f8d77ea0cef7c6acdba881c45b7d99",
        "size compressed (bytes)": 58312805496,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-doc"
    },
    "wikipedia-ance-multi-bf": {
        "description": "Wikipedia corpus encoded by ANCE-multi doc encoder and indexed as brute force index",
        "filename": "dindex-wikipedia-ance_multi-bf-20210224-060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-wikipedia-ance_multi-bf-20210224-060cef.tar.gz",
            "https://www.dropbox.com/s/j89z1vnhe12cva4/dindex-wikipedia-ance_multi-bf-20210224-060cef.tar.gz?dl=1"
        ],
        "md5": "715605b56dc393b8f939e12682dfd467",
        "size compressed (bytes)": 59890492088,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr"
    },
    "msmarco-passage-sbert-bf": {
        "description": "MS MARCO passage corpus encoded by SBERT msmarco passage encoder and indexed as brute force index",
        "filename": "dindex-msmarco-passage-sbert-bf-20210313-a0fbb3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-sbert-bf-20210313-a0fbb3.tar.gz",
            "https://www.dropbox.com/s/puj3lqxt661a3c0/dindex-msmarco-passage-sbert-bf-20210313-a0fbb3.tar.gz?dl=1"
        ],
        "md5": "3f98b9564cd3a33e45bfeca4d4fec623",
        "size compressed (bytes)": 25214193901,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-distilbert-dot-margin_mse-T2-bf": {
        "description": "MS MARCO passage corpus encoded by distilbert-dot-margin_mse-T2-msmarco passage encoder and "
                       "indexed as brute force index",
        "filename": "dindex-msmarco-passage-distilbert-dot-margin_mse-T2-20210316-d44c3a.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-distilbert-dot-margin_mse-T2-20210316-d44c3a.tar.gz",
            "https://www.dropbox.com/s/sn06dukchscnyxf/dindex-msmarco-passage-distilbert-dot-margin_mse-T2-20210316-d44c3a.tar.gz?dl=1"
        ],
        "md5": "83a8081d6020910058164978b095615f",
        "size compressed (bytes)": 25162770962,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-distilbert-dot-tas_b-b256-bf": {
        "description": "MS MARCO passage corpus encoded by msmarco-passage-distilbert-dot-tas_b-b256 passage encoder and "
                       "indexed as brute force index",
        "filename": "dindex-msmarco-passage-distilbert-dot-tas_b-b256-bf-20210527-63276f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-distilbert-dot-tas_b-b256-bf-20210527-63276f.tar.gz",
            "https://www.dropbox.com/s/1iu2wo2da1ai7ca/dindex-msmarco-passage-distilbert-dot-tas_b-b256-bf-20210527-63276f.tar.gz?dl=1",
        ],
        "md5": "cc947bf66d9552a2a7c6fe060466e490",
        "size compressed (bytes)": 25162328596,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-tct_colbert-v2-bf": {
        "description": "MS MARCO passage corpus encoded by tct_colbert-v2 passage encoder and "
                       "indexed as brute force index",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-tct_colbert-v2-bf-20210608-5f341b.tar.gz", 
            "https://www.dropbox.com/s/89mjp90z37dvt85/dindex-msmarco-passage-tct_colbert-v2-bf-20210608-5f341b.tar.gz?dl=1",
        ],
        "md5": "479591e265347ceff954ae05f6d3462b",
        "size compressed (bytes)": 25211079381,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-tct_colbert-v2-hn-bf": {
        "description": "MS MARCO passage corpus encoded by tct_colbert-v2-hn passage encoder and "
                       "indexed as brute force index",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-hn-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-tct_colbert-v2-hn-bf-20210608-5f341b.tar.gz",
            "https://www.dropbox.com/s/9ekxqhya475lkjw/dindex-msmarco-passage-tct_colbert-v2-hn-bf-20210608-5f341b.tar.gz?dl=1",
        ],
        "md5": "61d38e4935b3ca36c99e0cda2b27fba2",
        "size compressed (bytes)": 25205729786,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    },
    "msmarco-passage-tct_colbert-v2-hnp-bf": {
        "description": "MS MARCO passage corpus encoded by tct_colbert-v2-hnp passage encoder and "
                       "indexed as brute force index",
        "filename": "dindex-msmarco-passage-tct_colbert-v2-hnp-bf-20210608-5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/dindex-msmarco-passage-tct_colbert-v2-hnp-bf-20210608-5f341b.tar.gz",
            "https://www.dropbox.com/s/5q0siztt9dhwbxy/dindex-msmarco-passage-tct_colbert-v2-hnp-bf-20210608-5f341b.tar.gz?dl=1",
        ],
        "md5": "c3c3fc3a288bcdf61708d4bba4bc79ff",
        "size compressed (bytes)": 25225528775,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-passage"
    }
}

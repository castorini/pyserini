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

    # MS MARCO V1 document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-doc": {
        "description": "Lucene index of the MS MARCO V1 document corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc.20221004.252b5e.tar.gz",
        ],
        "md5": "b2b1841c93255f9902150128d5e27e41",
        "size compressed (bytes)": 13736982438,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },
    "msmarco-v1-doc-slim": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "400fe94ec97a20cf775596085c5ad79d",
        "size compressed (bytes)": 1791498133,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },
    "msmarco-v1-doc-full": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-full.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-full.20221004.252b5e.tar.gz",
        ],
        "md5": "75735da0dd35e3631d22bf682ebed8a0",
        "size compressed (bytes)": 25525615599,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },

    # MS MARCO V1 document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc-d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "87530b64e55080fcfb90ec9e598be23e",
        "size compressed (bytes)": 1885596544,
        "total_terms": 3748343494,
        "documents": 3213835,
        "unique_terms": 30631009,
        "downloaded": False
    },
    "msmarco-v1-doc-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "a081b866b78e0f604ddb9e3103ee6cc5",
        "size compressed (bytes)": 11152231182,
        "total_terms": 3748343494,
        "documents": 3213835,
        "unique_terms": 30631009,
        "downloaded": False
    },

    # MS MARCO V1 segmented document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-doc-segmented": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented.20221004.252b5e.tar.gz",
        ],
        "md5": "59fdf88f360d0a72d1b94b9729c2198e",
        "size compressed (bytes)": 15924438098,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-slim": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "c277161780d501ab832e16e6396f9cae",
        "size compressed (bytes)": 3306727108,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-full": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-full.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-full.20221004.252b5e.tar.gz",
        ],
        "md5": "c1af97d16c552a99a23382639c4a668c",
        "size compressed (bytes)": 29470600011,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },

    # MS MARCO V1 segmented document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc-segmented-d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "b242fd9cb0982e87d0c667439cb6d59c",
        "size compressed (bytes)": 3554554620,
        "total_terms": 4206646183,
        "documents": 20545677,
        "unique_terms": 22055268,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "40341fc2cf151b8c447a8e77f5e9f100",
        "size compressed (bytes)": 16349673687,
        "total_terms": 4206646183,
        "documents": 20545677,
        "unique_terms": 22055268,
        "downloaded": False
    },

    # MS MARCO V1 passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-passage": {
        "description": "Lucene index of the MS MARCO V1 passage corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage.20221004.252b5e.tar.gz",
        ],
        "md5": "c697b18c9a0686ca760583e615dbe450",
        "size compressed (bytes)": 2170758938,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-slim": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "9f952db731ed7c3f2ec14010664ddcec",
        "size compressed (bytes)": 491451085,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-full": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-full.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-full.20221004.252b5e.tar.gz",
        ],
        "md5": "0ff5ceaae32333d3580ae594d460385c",
        "size compressed (bytes)": 3720616158,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },

    # MS MARCO V1 passage corpus, doc2query-T5 expansions.
    "msmarco-v1-passage-d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "0a62959d300634aa0eb37e910aa4f4a7",
        "size compressed (bytes)": 807866125,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },
    "msmarco-v1-passage-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "2530b20771c6f441073ff49a56ea9004",
        "size compressed (bytes)": 4409861543,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },

    # MS MARCO V1 indexes for LTR experiments.
    "msmarco-passage-ltr": {
        "description": "Lucene index of the MS MARCO passage corpus with four extra preprocessed fields for LTR. (Lucene 8)",
        "filename": "index-msmarco-passage-ltr-20210519-e25e33f.tar.gz",
        "readme": "index-msmarco-passage-ltr-20210519-e25e33f-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/8qFCaCtwabRfYQD/download"
        ],
        "md5": "a5de642c268ac1ed5892c069bdc29ae3",
        "size compressed (bytes)": 14073966046,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-doc-per-passage-ltr": {
        "description": "Lucene index of the MS MARCO document per-passage corpus with four extra preprocessed fields for LTR. (Lucene 8)",
        "filename": "index-msmarco-doc-per-passage-ltr-20211031-33e4151.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-per-passage-ltr-20211031-33e4151.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/kNdXMWXEsTt3fT8/download"
        ],
        "md5": "bd60e89041b4ebbabc4bf0cfac608a87",
        "size compressed (bytes)": 45835520960,
        "total_terms": 1232004740,
        "documents": 20545628,
        "unique_terms": 10123678,
        "downloaded": False
    },
    "msmarco-document-segment-ltr": {
        "description": "Lucene index of the MS MARCO document segmented corpus with four extra preprocessed fields for LTR. (Lucene 8)",
        "filename": "lucene-index.msmarco-doc-segmented.ibm.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-doc-segmented.ibm.tar.gz"
        ],
        "md5": "13064bdaf8e8a79222634d67ecd3ddb5",
        "size compressed (bytes)": 98984853515,
        "total_terms": 3197500226,
        "documents": 20532330,
        "unique_terms": -1,
        "downloaded": False
    },

    # MS MARCO V2 document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-doc": {
        "description": "Lucene index of the MS MARCO V2 document corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc.20220808.4d6d2a.tar.gz",
        ],
        "md5": "0599bd6ed5ee28390b279eb398ef0267",
        "size compressed (bytes)": 63431299815,
        "total_terms": 14165667143,
        "documents": 11959635,
        "unique_terms": 44860768,
        "downloaded": False
    },
    "msmarco-v2-doc-slim": {
        "description": "Lucene index of the MS MARCO V2 document corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-slim.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-slim.20220808.4d6d2a.tar.gz",
        ],
        "md5": "4dfc5549e3c15abec4b9694542a376d1",
        "size compressed (bytes)": 7172175394,
        "total_terms": 14165667143,
        "documents": 11959635,
        "unique_terms": 44860768,
        "downloaded": False
    },
    "msmarco-v2-doc-full": {
        "description": "Lucene index of the MS MARCO V2 document corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-full.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-full.20220808.4d6d2a.tar.gz",
        ],
        "md5": "fc6f546898725617eb5ca7a144bef531",
        "size compressed (bytes)": 119537276117,
        "total_terms": 14165667143,
        "documents": 11959635,
        "unique_terms": 44860768,
        "downloaded": False
    },

    # MS MARCO V2 document corpus, doc2query-T5 expansions.
    "msmarco-v2-doc-d2q-t5": {
        "description": "Lucene index of the MS MARCO V2 document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-d2q-t5.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-d2q-t5.20220808.4d6d2a.tar.gz",
        ],
        "md5": "25514f77600a6be87aeb1c66c9107b89",
        "size compressed (bytes)": 8155218407,
        "total_terms": 19760783236,
        "documents": 11959635,
        "unique_terms": 54148271,
        "downloaded": False
    },
    "msmarco-v2-doc-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        ],
        "md5": "a3ce9b1146857a332825825623ab89e7",
        "size compressed (bytes)": 54415612794,
        "total_terms": 19760783236,
        "documents": 11959635,
        "unique_terms": 54148271,
        "downloaded": False
    },

    # MS MARCO V2 segmented document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-doc-segmented": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented.20220808.4d6d2a.tar.gz"
        ],
        "md5": "8a5f444fa5a63cc5d4ddc3e6dd15faa0",
        "size compressed (bytes)": 109269078191,
        "total_terms": 24780918039,
        "documents": 124131414,
        "unique_terms": 29265408,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-slim": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-slim.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-slim.20220808.4d6d2a.tar.gz"
        ],
        "md5": "f50c591aa9a0a0126ebc4dc53c6306d7",
        "size compressed (bytes)": 20852487058,
        "total_terms": 24780918039,
        "documents": 124131414,
        "unique_terms": 29265408,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-full": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-full.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-full.20220808.4d6d2a.tar.gz"
        ],
        "md5": "259b936d3591e48770da9dde153d1617",
        "size compressed (bytes)": 201358944352,
        "total_terms": 24780918039,
        "documents": 124131414,
        "unique_terms": 29265408,
        "downloaded": False
    },

    # MS MARCO V2 segmented document corpus, doc2query-T5 expansions.
    "msmarco-v2-doc-segmented-d2q-t5": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220808.4d6d2a.tar.gz"
        ],
        "md5": "1e9fa18f082aaadfef02ba9eea32fcc2",
        "size compressed (bytes)": 24242738999,
        "total_terms": 30376034132,
        "documents": 124131414,
        "unique_terms": 38932296,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        ],
        "md5": "eff6fe5b61936491c8985ad7efa46b20",
        "size compressed (bytes)": 114315186555,
        "total_terms": 30376034132,
        "documents": 124131414,
        "unique_terms": 38932296,
        "downloaded": False
    },

    # MS MARCO V2 passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-passage": {
        "description": "Lucene index of the MS MARCO V2 passage corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage.20220808.4d6d2a.tar.gz"
        ],
        "md5": "eacd8556dd416ccad517b5e7dc97bceb",
        "size compressed (bytes)": 38808092190,
        "total_terms": 4673266800,
        "documents": 138364198,
        "unique_terms": 11885838,
        "downloaded": False
    },
    "msmarco-v2-passage-slim": {
        "description": "Lucene index of the MS MARCO V2 passage corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-slim.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-slim.20220808.4d6d2a.tar.gz"
        ],
        "md5": "d7e644c048669aa72314dd358b475765",
        "size compressed (bytes)": 8170344330,
        "total_terms": 4673266800,
        "documents": 138364198,
        "unique_terms": 11885838,
        "downloaded": False
    },
    "msmarco-v2-passage-full": {
        "description": "Lucene index of the MS MARCO V2 passage corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-full.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-full.20220808.4d6d2a.tar.gz"
        ],
        "md5": "ef5c22c865094c386b9ec600165bb061",
        "size compressed (bytes)": 60413585958,
        "total_terms": 4673266800,
        "documents": 138364198,
        "unique_terms": 11885838,
        "downloaded": False
    },

    # MS MARCO V2 passage corpus, doc2query-T5 expansions.
    "msmarco-v2-passage-d2q-t5": {
        "description": "Lucene index of the MS MARCO V2 passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-d2q-t5.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-d2q-t5.20220808.4d6d2a.tar.gz",
        ],
        "md5": "3c357f9c219e4c3d980bc663e1f5a5f4",
        "size compressed (bytes)": 14404903785,
        "total_terms": 16961479264,
        "documents": 138364198,
        "unique_terms": 36651533,
        "downloaded": False
    },
    "msmarco-v2-passage-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        ],
        "md5": "01e369b644e5a8b7413e04140780cf94",
        "size compressed (bytes)": 59206472740,
        "total_terms": 16961479264,
        "documents": 138364198,
        "unique_terms": 36651533,
        "downloaded": False
    },

    # MS MARCO V2 augmented passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-passage-augmented": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-augmented.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented.20220808.4d6d2a.tar.gz"
        ],
        "md5": "69675971a0172eb5e37668ea42761d43",
        "size compressed (bytes)": 75036026507,
        "total_terms": 15272965252,
        "documents": 138364198,
        "unique_terms": 16579899,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-slim": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('slim' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-slim.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-slim.20220808.4d6d2a.tar.gz"
        ],
        "md5": "3524b5b28117ac1a5365cd664c6871f1",
        "size compressed (bytes)": 14757394934,
        "total_terms": 15272965252,
        "documents": 138364198,
        "unique_terms": 16579899,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-full": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('full' version). (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-full.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-full.20220808.4d6d2a.tar.gz"
        ],
        "md5": "c3e18c02e749c0416e1acc653899c6b0",
        "size compressed (bytes)": 130622740320,
        "total_terms": 15272965252,
        "documents": 138364198,
        "unique_terms": 16579899,
        "downloaded": False
    },

    # MS MARCO V2 augmented passage corpus, doc2query-T5 expansions.
    "msmarco-v2-passage-augmented-d2q-t5": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220808.4d6d2a.tar.gz"
        ],
        "md5": "2b683a3a64692b95375ddbdcb9590f25",
        "size compressed (bytes)": 14404903785,
        "total_terms": 27561177716,
        "documents": 138364198,
        "unique_terms": 41177061,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions. (Lucene 9)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220808.4d6d2a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220808.4d6d2a.tar.gz",
        ],
        "md5": "fe6eaeceabaa06cb09fdf8432f65f9d8",
        "size compressed (bytes)": 59206472740,
        "total_terms": 27561177716,
        "documents": 138364198,
        "unique_terms": 41177061,
        "downloaded": False
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

    # BEIR (v1.0.0) flat indexes
    "beir-v1.0.0-trec-covid-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-COVID",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-flat.20221116.505594.tar.gz"
        ],
        "md5": "9ae06c30a7c352f18a5a8e75b88b9106",
        "size compressed (bytes)": 226268661,
        "total_terms": 20822821,
        "documents": 171331,
        "unique_terms": 202648,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): BioASQ",
        "filename": "lucene-index.beir-v1.0.0-bioasq-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-flat.20221116.505594.tar.gz"
        ],
        "md5": "d9b098a7e127a79f390285290a7c0ba8",
        "size compressed (bytes)": 24821933182,
        "total_terms": 2257541758,
        "documents": 14914603,
        "unique_terms": 4960004,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): NFCorpus",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-flat.20221116.505594.tar.gz"
        ],
        "md5": "12ad00c0f58393b9a6c473183b4ff55a",
        "size compressed (bytes)": 6509693,
        "total_terms": 637485,
        "documents": 3633,
        "unique_terms": 22111,
        "downloaded": False
    },
    "beir-v1.0.0-nq-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): NQ",
        "filename": "lucene-index.beir-v1.0.0-nq-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-flat.20221116.505594.tar.gz"
        ],
        "md5": "fefe2c93019b2eb899d875a90861b9f4",
        "size compressed (bytes)": 1645453710,
        "total_terms": 151249294,
        "documents": 2681468,
        "unique_terms": 997027,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): HotpotQA",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-flat.20221116.505594.tar.gz"
        ],
        "md5": "29723f2d1ea53880720765dd558fb264",
        "size compressed (bytes)": 2019085858,
        "total_terms": 172477066,
        "documents": 5233329,
        "unique_terms": 2644892,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): FiQA-2018",
        "filename": "lucene-index.beir-v1.0.0-fiqa-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-flat.20221116.505594.tar.gz"
        ],
        "md5": "7ead89ae57ca09a0f6f39f0c621feba8",
        "size compressed (bytes)": 55982529,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Signal-1M",
        "filename": "lucene-index.beir-v1.0.0-signal1m-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-flat.20221116.505594.tar.gz"
        ],
        "md5": "a1c952e55f7dd3383c9140c7b446e044",
        "size compressed (bytes)": 496596590,
        "total_terms": 32240069,
        "documents": 2866315,
        "unique_terms": 796647,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-NEWS",
        "filename": "lucene-index.beir-v1.0.0-trec-news-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-flat.20221116.505594.tar.gz"
        ],
        "md5": "599aca58ee57e9593d40953b12a1bd69",
        "size compressed (bytes)": 2623577554,
        "total_terms": 275651967,
        "documents": 594589,
        "unique_terms": 729872,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Robust04",
        "filename": "lucene-index.beir-v1.0.0-robust04-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-flat.20221116.505594.tar.gz"
        ],
        "md5": "717325e5c282f45d2a8e189e9ef89388",
        "size compressed (bytes)": 1728446672,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): ArguAna",
        "filename": "lucene-index.beir-v1.0.0-arguana-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-flat.20221116.505594.tar.gz"
        ],
        "md5": "5989163bb5c7e0a29f8241f3fae95c02",
        "size compressed (bytes)": 10563484,
        "total_terms": 969528,
        "documents": 8674,
        "unique_terms": 23895,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Webis-Touche2020",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-flat.20221116.505594.tar.gz"
        ],
        "md5": "5f54ca552b6075b8dff6d9ae9cd138e6",
        "size compressed (bytes)": 750400909,
        "total_terms": 76082209,
        "documents": 382545,
        "unique_terms": 525540,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-android",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-flat.20221116.505594.tar.gz"
        ],
        "md5": "14451ca82955bc7ce3b1df73091d5f0e",
        "size compressed (bytes)": 17423304,
        "total_terms": 1760762,
        "documents": 22998,
        "unique_terms": 41456,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-english",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-flat.20221116.505594.tar.gz"
        ],
        "md5": "0b66a52f9f67b4ddd163590bb968efee",
        "size compressed (bytes)": 24949592,
        "total_terms": 2236655,
        "documents": 40221,
        "unique_terms": 62517,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gaming",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20221116.505594.tar.gz"
        ],
        "md5": "a369444e1296c54beb6d7eae19f30f3b",
        "size compressed (bytes)": 29156968,
        "total_terms": 2827717,
        "documents": 45301,
        "unique_terms": 60070,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gis",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20221116.505594.tar.gz"
        ],
        "md5": "85ad4715eb06b2a2079385c74504da15",
        "size compressed (bytes)": 43396160,
        "total_terms": 4048584,
        "documents": 37637,
        "unique_terms": 184133,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-mathematica",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20221116.505594.tar.gz"
        ],
        "md5": "5b8bd6d8f8f37d449856e0bc14eb16fc",
        "size compressed (bytes)": 21589911,
        "total_terms": 2332642,
        "documents": 16705,
        "unique_terms": 111611,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-physics",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20221116.505594.tar.gz"
        ],
        "md5": "e4a1dda9c0940277d8bbc2d5e9278eb7",
        "size compressed (bytes)": 37956223,
        "total_terms": 3785483,
        "documents": 38316,
        "unique_terms": 55950,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-programmers",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20221116.505594.tar.gz"
        ],
        "md5": "f8b124fb052d2f14e908f20c47792cc3",
        "size compressed (bytes)": 40297081,
        "total_terms": 3905694,
        "documents": 32176,
        "unique_terms": 74195,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-stats",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20221116.505594.tar.gz"
        ],
        "md5": "a622bd3c4d6b413c50c1855b6fa85e64",
        "size compressed (bytes)": 52212616,
        "total_terms": 5356042,
        "documents": 42269,
        "unique_terms": 183358,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-tex",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20221116.505594.tar.gz"
        ],
        "md5": "939c69cdf1ab563729697bc936f45e6a",
        "size compressed (bytes)": 91818976,
        "total_terms": 9556423,
        "documents": 68184,
        "unique_terms": 288088,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-unix",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20221116.505594.tar.gz"
        ],
        "md5": "34913c5e811c0399c6ee3c03c68861d1",
        "size compressed (bytes)": 53802802,
        "total_terms": 5767374,
        "documents": 47382,
        "unique_terms": 206323,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-webmasters",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20221116.505594.tar.gz"
        ],
        "md5": "41f91e1dc4c4d7ee4da89ef2e7210dfb",
        "size compressed (bytes)": 15174810,
        "total_terms": 1482585,
        "documents": 17405,
        "unique_terms": 40547,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-wordpress",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20221116.505594.tar.gz"
        ],
        "md5": "c10a130177b7ca65ae47640cffc4a5ec",
        "size compressed (bytes)": 54807600,
        "total_terms": 5463472,
        "documents": 48605,
        "unique_terms": 125727,
        "downloaded": False
    },
    "beir-v1.0.0-quora-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Quora",
        "filename": "lucene-index.beir-v1.0.0-quora-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-flat.20221116.505594.tar.gz"
        ],
        "md5": "20cc429516848d0f314ac593c94bf226",
        "size compressed (bytes)": 52698681,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): DBPedia",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-flat.20221116.505594.tar.gz"
        ],
        "md5": "8aabf2456b0cccc1a1d013059125b6ef",
        "size compressed (bytes)": 2085472968,
        "total_terms": 164794982,
        "documents": 4635922,
        "unique_terms": 3351459,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): SCIDOCS",
        "filename": "lucene-index.beir-v1.0.0-scidocs-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-flat.20221116.505594.tar.gz"
        ],
        "md5": "a25663e4bce0d588814efb3091a3a53f",
        "size compressed (bytes)": 186572828,
        "total_terms": 3266767,
        "documents": 25657,
        "unique_terms": 63604,
        "downloaded": False
    },
    "beir-v1.0.0-fever-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): FEVER",
        "filename": "lucene-index.beir-v1.0.0-fever-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-flat.20221116.505594.tar.gz"
        ],
        "md5": "ce620e8c11b44528a498360912d5fe46",
        "size compressed (bytes)": 3880155518,
        "total_terms": 325179165,
        "documents": 5416568,
        "unique_terms": 3293639,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Climate-FEVER",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-flat.20221116.505594.tar.gz"
        ],
        "md5": "50adaaac662f7fadaf5494808e50f9d6",
        "size compressed (bytes)": 3880208210,
        "total_terms": 325185072,
        "documents": 5416593,
        "unique_terms": 3293621,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): SciFact",
        "filename": "lucene-index.beir-v1.0.0-scifact-flat.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-flat.20221116.505594.tar.gz"
        ],
        "md5": "5fee55eb99327b38a5ca623e68e25edf",
        "size compressed (bytes)": 8851172,
        "total_terms": 838128,
        "documents": 5183,
        "unique_terms": 28865,
        "downloaded": False
    },

    # BEIR (v1.0.0) multifield indexes
    "beir-v1.0.0-trec-covid-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-COVID",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-multifield.20221116.505594.tar.gz"
        ],
        "md5": "ec260e10c9897e736820c22476c3574f",
        "size compressed (bytes)": 222831948,
        "total_terms": 19060122,
        "documents": 129192,
        "unique_terms": 193851,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): BioASQ",
        "filename": "lucene-index.beir-v1.0.0-bioasq-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-multifield.20221116.505594.tar.gz"
        ],
        "md5": "d754a05c01fd1c3e34d883e4fa912d63",
        "size compressed (bytes)": 25346354708,
        "total_terms": 2099554307,
        "documents": 14914602,
        "unique_terms": 4889053,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NFCorpus",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-multifield.20221116.505594.tar.gz"
        ],
        "md5": "6e5fc4f35cc1fa8dc98b86b2385c4a0b",
        "size compressed (bytes)": 6645574,
        "total_terms": 601950,
        "documents": 3633,
        "unique_terms": 21819,
        "downloaded": False
    },
    "beir-v1.0.0-nq-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NQ",
        "filename": "lucene-index.beir-v1.0.0-nq-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-multifield.20221116.505594.tar.gz"
        ],
        "md5": "db80e0851c81c082688add60b57bd9f1",
        "size compressed (bytes)": 1642708222,
        "total_terms": 144050891,
        "documents": 2680961,
        "unique_terms": 996653,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): HotpotQA",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-multifield.20221116.505594.tar.gz"
        ],
        "md5": "95c657338468ddacfae5874cbd09d7eb",
        "size compressed (bytes)": 2083441352,
        "total_terms": 158180692,
        "documents": 5233235,
        "unique_terms": 2627639,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FiQA-2018",
        "filename": "lucene-index.beir-v1.0.0-fiqa-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-multifield.20221116.505594.tar.gz"
        ],
        "md5": "ba7f197331d1a84582c5485536b0d2aa",
        "size compressed (bytes)": 55984431,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Signal-1M",
        "filename": "lucene-index.beir-v1.0.0-signal1m-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-multifield.20221116.505594.tar.gz"
        ],
        "md5": "6f5c151ade6efc6567d2b98016a97041",
        "size compressed (bytes)": 496603097,
        "total_terms": 32240069,
        "documents": 2866315,
        "unique_terms": 796647,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-NEWS",
        "filename": "lucene-index.beir-v1.0.0-trec-news-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-multifield.20221116.505594.tar.gz"
        ],
        "md5": "b9e935edb604edb04524970c40ca107a",
        "size compressed (bytes)": 2633899051,
        "total_terms": 270886723,
        "documents": 578605,
        "unique_terms": 727856,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Robust04",
        "filename": "lucene-index.beir-v1.0.0-robust04-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-multifield.20221116.505594.tar.gz"
        ],
        "md5": "bb2939df4ca76dec5d6e5f366d08fe00",
        "size compressed (bytes)": 1728446264,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): ArguAna",
        "filename": "lucene-index.beir-v1.0.0-arguana-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-multifield.20221116.505594.tar.gz"
        ],
        "md5": "3b548e373d85835f478199cdcebd7b0b",
        "size compressed (bytes)": 10524119,
        "total_terms": 944123,
        "documents": 8674,
        "unique_terms": 23867,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Webis-Touche2020",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-multifield.20221116.505594.tar.gz"
        ],
        "md5": "2a1549bc27a34a140914e42b709f1a19",
        "size compressed (bytes)": 750724431,
        "total_terms": 74066724,
        "documents": 382545,
        "unique_terms": 524665,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-android",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20221116.505594.tar.gz"
        ],
        "md5": "858ed389f7a924cd90a8c9c8882954ed",
        "size compressed (bytes)": 17887744,
        "total_terms": 1591285,
        "documents": 22998,
        "unique_terms": 40824,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-english",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20221116.505594.tar.gz"
        ],
        "md5": "40e87436b956a78ba312751d90116c27",
        "size compressed (bytes)": 25558892,
        "total_terms": 2006983,
        "documents": 40221,
        "unique_terms": 61530,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gaming",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20221116.505594.tar.gz"
        ],
        "md5": "eed5e2778ed6e22fca99eec8dae8f77f",
        "size compressed (bytes)": 29992461,
        "total_terms": 2510477,
        "documents": 45300,
        "unique_terms": 59113,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gis",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20221116.505594.tar.gz"
        ],
        "md5": "add51b3adeb981dfb7749b01edc9b4e5",
        "size compressed (bytes)": 44188649,
        "total_terms": 3789161,
        "documents": 37637,
        "unique_terms": 183298,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-mathematica",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20221116.505594.tar.gz"
        ],
        "md5": "90e592f86ab093bbc1d77b8de65dc9ba",
        "size compressed (bytes)": 21911907,
        "total_terms": 2234369,
        "documents": 16705,
        "unique_terms": 111306,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-physics",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20221116.505594.tar.gz"
        ],
        "md5": "a8abde1bced888a706d0a6311c3e13ad",
        "size compressed (bytes)": 38736490,
        "total_terms": 3542078,
        "documents": 38316,
        "unique_terms": 55229,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-programmers",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20221116.505594.tar.gz"
        ],
        "md5": "2f99a6e167475ecdb2265846381e7171",
        "size compressed (bytes)": 40982054,
        "total_terms": 3682227,
        "documents": 32176,
        "unique_terms": 73765,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-stats",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20221116.505594.tar.gz"
        ],
        "md5": "4b4a103decd723566f1935134434c9a9",
        "size compressed (bytes)": 53094503,
        "total_terms": 5073873,
        "documents": 42269,
        "unique_terms": 182933,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-tex",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20221116.505594.tar.gz"
        ],
        "md5": "93e0cb6018cc7fcf042a2119e3b73d5d",
        "size compressed (bytes)": 93081213,
        "total_terms": 9155405,
        "documents": 68184,
        "unique_terms": 287393,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-unix",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20221116.505594.tar.gz"
        ],
        "md5": "c7d4cebf819aa19c6a0da6df7aed93fe",
        "size compressed (bytes)": 54758840,
        "total_terms": 5449726,
        "documents": 47382,
        "unique_terms": 205471,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-webmasters",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20221116.505594.tar.gz"
        ],
        "md5": "1ff00797eb6fb43bef05b054281ca016",
        "size compressed (bytes)": 15524401,
        "total_terms": 1358292,
        "documents": 17405,
        "unique_terms": 40073,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-wordpress",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20221116.505594.tar.gz"
        ],
        "md5": "5e571c3ca3d28cb53e2b280fd05dfaec",
        "size compressed (bytes)": 55738645,
        "total_terms": 5151575,
        "documents": 48605,
        "unique_terms": 125110,
        "downloaded": False
    },
    "beir-v1.0.0-quora-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Quora",
        "filename": "lucene-index.beir-v1.0.0-quora-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-multifield.20221116.505594.tar.gz"
        ],
        "md5": "1e033c875d3fdda2f096928003d6f977",
        "size compressed (bytes)": 52703125,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): DBPedia",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20221116.505594.tar.gz"
        ],
        "md5": "107ac2e15140ae889315920148e73ce6",
        "size compressed (bytes)": 2144410442,
        "total_terms": 152205479,
        "documents": 4635922,
        "unique_terms": 3338476,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SCIDOCS",
        "filename": "lucene-index.beir-v1.0.0-scidocs-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-multifield.20221116.505594.tar.gz"
        ],
        "md5": "e97467dff3cf15b20471421c4ef7e106",
        "size compressed (bytes)": 175887258,
        "total_terms": 3065828,
        "documents": 25313,
        "unique_terms": 62562,
        "downloaded": False
    },
    "beir-v1.0.0-fever-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FEVER",
        "filename": "lucene-index.beir-v1.0.0-fever-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-multifield.20221116.505594.tar.gz"
        ],
        "md5": "7a10971ad193dddaf604240e54965305",
        "size compressed (bytes)": 3947213520,
        "total_terms": 310655699,
        "documents": 5396138,
        "unique_terms": 3275057,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Climate-FEVER",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-multifield.20221116.505594.tar.gz"
        ],
        "md5": "a940bc3477e67f3231e891863ebfe393",
        "size compressed (bytes)": 3947277760,
        "total_terms": 310661477,
        "documents": 5396163,
        "unique_terms": 3275068,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SciFact",
        "filename": "lucene-index.beir-v1.0.0-scifact-multifield.20221116.505594.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-multifield.20221116.505594.tar.gz"
        ],
        "md5": "1a918170d342b0e208b28c9f02d626b3",
        "size compressed (bytes)": 9078031,
        "total_terms": 784591,
        "documents": 5183,
        "unique_terms": 28581,
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
    },
}

TF_INDEX_INFO_DEPRECATED = {
    "hc4-v1.0-zh-lucene8": {
        "description": "Lucene index for HC4 v1.0 (Chinese). (Lucene 8; deprecated)",
        "filename": "lucene-index.hc4-v1.0-zh.20220719.71c120.tar.gz",
        "readme": "lucene-index.hc4-v1.0-zh.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-zh.20220719.71c120.tar.gz"
        ],
        "md5": "7351794f4b570c387a12527cf46a7956",
        "size compressed (bytes)": 2904147388,
        "total_terms": 304468573,
        "documents": 646302,
        "unique_terms": 4380931,
        "downloaded": False
    },
    "hc4-v1.0-fa-lucene8": {
        "description": "Lucene index for HC4 v1.0 (Persian). (Lucene 8; deprecated)",
        "filename": "lucene-index.hc4-v1.0-fa.20220719.71c120.tar.gz",
        "readme": "lucene-index.hc4-v1.0-fa.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-fa.20220719.71c120.tar.gz"
        ],
        "md5": "fd838abb94864f22cb4d94cd33660b24",
        "size compressed (bytes)": 1656366266,
        "total_terms": 112225895,
        "documents": 486486,
        "unique_terms": 617107,
        "downloaded": False
    },
    "hc4-v1.0-ru-lucene8": {
        "description": "Lucene index for HC4 v1.0 (Russian). (Lucene 8; deprecated)",
        "filename": "lucene-index.hc4-v1.0-ru.20220719.71c120.tar.gz",
        "readme": "lucene-index.hc4-v1.0-ru.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.hc4-v1.0-ru.20220719.71c120.tar.gz"
        ],
        "md5": "3f15b30d1238d2d0a6f720f06c7c442c",
        "size compressed (bytes)": 13323791981,
        "total_terms": 764996697,
        "documents": 4721064,
        "unique_terms": 2640439,
        "downloaded": False
    },
    "neuclir22-zh-lucene8": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Chinese). (Lucene 8; deprecated)",
        "filename": "lucene-index.neuclir22-zh.20220719.71c120.tar.gz",
        "readme": "lucene-index.neuclir22-zh.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-zh.20220719.71c120.tar.gz"
        ],
        "md5": "edca109c2f39464f73cf9d12af776b73",
        "size compressed (bytes)": 15744742868,
        "total_terms": 1654090468,
        "documents": 3179206,
        "unique_terms": 8213049,
        "downloaded": False
    },
    "neuclir22-fa-lucene8": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Persian). (Lucene 8; deprecated)",
        "filename": "lucene-index.neuclir22-fa.20220719.71c120.tar.gz",
        "readme": "lucene-index.neuclir22-fa.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-fa.20220719.71c120.tar.gz"
        ],
        "md5": "ff3a6ac9a4c428d3aa42e1ae3c007147",
        "size compressed (bytes)": 7577718950,
        "total_terms": 514262091,
        "documents": 2232016,
        "unique_terms": 1479422,
        "downloaded": False
    },
    "neuclir22-ru-lucene8": {
        "description": "Lucene index for NeuCLIR 2022 corpus (Russian). (Lucene 8; deprecated)",
        "filename": "lucene-index.neuclir22-ru.20220719.71c120.tar.gz",
        "readme": "lucene-index.neuclir22-ru.20220719.71c120.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.neuclir22-ru.20220719.71c120.tar.gz"
        ],
        "md5": "dd483e258fddde98cd059fd5f4f0fe1e",
        "size compressed (bytes)": 14237631658,
        "total_terms": 830006488,
        "documents": 4627541,
        "unique_terms": 3412268,
        "downloaded": False
    },

    "mrtydi-v1.1-arabic-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Arabic). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-arabic.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-arabic.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-arabic.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/7oDFnq8FmTazf2a/download"
        ],
        "md5": "0129b01cc88524e13a9ff3e398e988a5",
        "size compressed (bytes)": 1172153418,
        "total_terms": 92529014,
        "documents": 2106586,
        "unique_terms": 1284712,
        "downloaded": False
    },
    "mrtydi-v1.1-bengali-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Bengali). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-bengali.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-bengali.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-bengali.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/HaPaz2wFbRMP2LK/download"
        ],
        "md5": "756a686cc5723791eb5ab5357271be10",
        "size compressed (bytes)": 240371052,
        "total_terms": 15236598,
        "documents": 304059,
        "unique_terms": 520694,
        "downloaded": False
    },
    "mrtydi-v1.1-english-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (English). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-english.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-english.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-english.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/w4ccMwH5BLnXQ3j/download"
        ],
        "md5": "804c7626b5a36f06f75e0a04c6ec4fe1",
        "size compressed (bytes)": 16772744114,
        "total_terms": 1507060955,
        "documents": 32907100,
        "unique_terms": 6189349,
        "downloaded": False
    },
    "mrtydi-v1.1-finnish-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Finnish). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-finnish.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-finnish.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-finnish.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Pgd3mqjy77a6FR8/download"
        ],
        "md5": "65361258d1a318447f364ccae90c293a",
        "size compressed (bytes)": 908904453,
        "total_terms": 69431615,
        "documents": 1908757,
        "unique_terms": 1709590,
        "downloaded": False
    },
    "mrtydi-v1.1-indonesian-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Indonesian). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-indonesian.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-indonesian.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-indonesian.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/tF8NE7pWZ2xGix7/download"
        ],
        "md5": "ca62d690401b84a493c70693ee2626c3",
        "size compressed (bytes)": 564741230,
        "total_terms": 52493134,
        "documents": 1469399,
        "unique_terms": 942550,
        "downloaded": False
    },
    "mrtydi-v1.1-japanese-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Japanese). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-japanese.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-japanese.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-japanese.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/ema8i83zqJr7n48/download"
        ],
        "md5": "d05aefed5f79bfc151a9f4815d3693d8",
        "size compressed (bytes)": 3670762373,
        "total_terms": 303640353,
        "documents": 7000027,
        "unique_terms": 1708155,
        "downloaded": False
    },
    "mrtydi-v1.1-korean-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Korean). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-korean.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-korean.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-korean.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/igmEHCTjTwNi3de/download"
        ],
        "md5": "4ecc408de4c749f25865859ea97278bd",
        "size compressed (bytes)": 1141503582,
        "total_terms": 122217290,
        "documents": 1496126,
        "unique_terms": 1517175,
        "downloaded": False
    },
    "mrtydi-v1.1-russian-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Russian). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-russian.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-russian.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-russian.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Pbi9xrD7jSYaxnX/download"
        ],
        "md5": "9e229b33f4ddea411477d2f00c25be72",
        "size compressed (bytes)": 5672456411,
        "total_terms": 346329152,
        "documents": 9597504,
        "unique_terms": 3059773,
        "downloaded": False
    },
    "mrtydi-v1.1-swahili-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Swahili). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-swahili.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-swahili.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-swahili.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/SWqajDQgq8wppf6/download"
        ],
        "md5": "ec88a5b39c2506b8cd61e6e47b8044e7",
        "size compressed (bytes)": 47689785,
        "total_terms": 4937051,
        "documents": 136689,
        "unique_terms": 385711,
        "downloaded": False
    },
    "mrtydi-v1.1-telugu-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Telugu). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-telugu.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-telugu.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-telugu.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/DAB6ba5ZF98awH6/download"
        ],
        "md5": "2704b725c0418905037a45b6301e8666",
        "size compressed (bytes)": 452906283,
        "total_terms": 27173644,
        "documents": 548224,
        "unique_terms": 1892900,
        "downloaded": False
    },
    "mrtydi-v1.1-thai-lucene8": {
        "description": "Lucene index for Mr.TyDi v1.1 (Thai). (Lucene 8; deprecated)",
        "filename": "lucene-index.mrtydi-v1.1-thai.20220108.6fcb89.tar.gz",
        "readme": "lucene-index.mrtydi-v1.1-thai.20220108.6fcb89.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.mrtydi-v1.1-thai.20220108.6fcb89.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/2Ady6AwBwNbYLpg/download"
        ],
        "md5": "9756502f1aeeee035c37975202787538",
        "size compressed (bytes)": 452244053,
        "total_terms": 31550936,
        "documents": 568855,
        "unique_terms": 663628,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-doc-lucene8": {
        "description": "Lucene index of the MS MARCO V1 document corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/aDRAfyZytQsQ9T3/download"
        ],
        "md5": "43b60b3fc75324c648a02375772e7fe8",
        "size compressed (bytes)": 13757573401,
        "total_terms": 2742209690,
        "documents": 3213835,
        "unique_terms": 29820456,
        "downloaded": False
    },
    "msmarco-v1-doc-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-slim.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-slim.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-slim.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/iCnysqnaG9SL9pA/download"
        ],
        "md5": "17a7b079e9d527492904c7697a9cae59",
        "size compressed (bytes)": 1811599007,
        "total_terms": 2742209690,
        "documents": 3213835,
        "unique_terms": 29820456,
        "downloaded": False
    },
    "msmarco-v1-doc-full-lucene8": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-full.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-full.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-full.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/KsqZ2AwkSrTM8yS/download"
        ],
        "md5": "ef60d7f8afa3919cdeedc6fea89aa3f7",
        "size compressed (bytes)": 25548064269,
        "total_terms": 2742209690,
        "documents": 3213835,
        "unique_terms": 29820456,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V1 document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/jWb3La4NYorwSCp/download"
        ],
        "md5": "37c639c9c26a34d2612ea6549fb866df",
        "size compressed (bytes)": 1904879520,
        "total_terms": 3748333319,
        "documents": 3213835,
        "unique_terms": 30627687,
        "downloaded": False
    },
    "msmarco-v1-doc-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "987088270d4df2d51bcdffb1588f6915",
        "size compressed (bytes)": 11169880136,
        "total_terms": 3748333319,
        "documents": 3213835,
        "unique_terms": 30627687,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 segmented document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-doc-segmented-lucene8": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-segmented.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/FKniAWGJjZHy3TF/download"
        ],
        "md5": "611bb83e043c0d6febe0fa3508d1d7f9",
        "size compressed (bytes)": 17091132803,
        "total_terms": 3200515914,
        "documents": 20545677,
        "unique_terms": 21190687,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-slim.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-slim.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-slim.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/QNYpaAcLXERr74y/download"
        ],
        "md5": "d42113cfeeea862b51765329795948ad",
        "size compressed (bytes)": 3408754542,
        "total_terms": 3200515914,
        "documents": 20545677,
        "unique_terms": 21190687,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-full-lucene8": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-full.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-full.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-full.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/RzRBC6xkmaTsmX9/download"
        ],
        "md5": "2ed7457c8804d2d6370a1a7f604eb360",
        "size compressed (bytes)": 30771630666,
        "total_terms": 3200515914,
        "documents": 20545677,
        "unique_terms": 21190687,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 segmented document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc-segmented-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/gJmL8iiWWztnYmH/download"
        ],
        "md5": "6c1f86ee4f7175eed4d3a7acc3d567b8",
        "size compressed (bytes)": 3638703522,
        "total_terms": 4206639543,
        "documents": 20545677,
        "unique_terms": 22054207,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-doc-segmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "a67e6854187f084a8a3eee11dd30bc31",
        "size compressed (bytes)": 16627681594,
        "total_terms": 4206639543,
        "documents": 20545677,
        "unique_terms": 22054207,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-passage-lucene8": {
        "description": "Lucene index of the MS MARCO V1 passage corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-passage.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/L7yNfCXpqK5yf8e/download"
        ],
        "md5": "4d8fdbdcd119c1f47a4cc5d01a45dad3",
        "size compressed (bytes)": 2178557129,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-passage-slim.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-slim.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-slim.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/swtPDQAGg6oHD8m/download"
        ],
        "md5": "2f1e50d60a0df32a50111a986159de51",
        "size compressed (bytes)": 498355616,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-full-lucene8": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-passage-full.20220131.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-full.20220131.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-full.20220131.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/wzGLFMQyKAc2TTC/download"
        ],
        "md5": "3283069c6e8451659c8ea83e2140d739",
        "size compressed (bytes)": 3781721749,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },

    # Deprecated: MS MARCO V1 passage corpus, doc2query-T5 expansions.
    "msmarco-v1-passage-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V1 passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-passage-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/P7Lt234kyZP87nB/download"
        ],
        "md5": "136205f35bd895077c0874eaa063376c",
        "size compressed (bytes)": 819441969,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },
    "msmarco-v1-passage-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "5eb8178e48a4a9b85714be156d85b2d1",
        "size compressed (bytes)": 4433982542,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },

    # These MS MARCO V1 indexes are deprecated, but keeping around for archival reasons
    "msmarco-passage": {
        "description": "Lucene index of the MS MARCO passage corpus (deprecated; use msmarco-v1-passage instead). (Lucene 8)",
        "filename": "index-msmarco-passage-20201117-f87c94.tar.gz",
        "readme": "index-msmarco-passage-20201117-f87c94-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-passage-20201117-f87c94.tar.gz",
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
        "description": "Lucene index of the MS MARCO passage corpus (slim version, document text not stored) (deprecated; use msmarco-v1-passage-slim instead). (Lucene 8)",
        "filename": "index-msmarco-passage-slim-20201202-ab6e28.tar.gz",
        "readme": "index-msmarco-passage-slim-20201202-ab6e28-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-passage-slim-20201202-ab6e28.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/Kx6K9NJFmwnaAP8/download"
        ],
        "md5": "5e11da4cebd2e8dda2e73c589ffb0b4c",
        "size compressed (bytes)": 513566686,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-doc": {
        "description": "Lucene index of the MS MARCO document corpus (deprecated; use msmarco-v1-doc instead). (Lucene 8)",
        "filename": "index-msmarco-doc-20201117-f87c94.tar.gz",
        "readme": "index-msmarco-doc-20201117-f87c94-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-20201117-f87c94.tar.gz",
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
        "description": "Lucene index of the MS MARCO document corpus (slim version, document text not stored) (deprecated; use msmarco-v1-doc-slim instead). (Lucene 8)",
        "filename": "index-msmarco-doc-slim-20201202-ab6e28.tar.gz",
        "readme": "index-msmarco-doc-slim-20201202-ab6e28-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-slim-20201202-ab6e28.tar.gz",
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
        "description": "Lucene index of the MS MARCO document corpus segmented into passages (deprecated; use msmarco-v1-doc-segmented instead). (Lucene 8)",
        "filename": "index-msmarco-doc-per-passage-20201204-f50dcc.tar.gz",
        "readme": "index-msmarco-doc-per-passage-20201204-f50dcc-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-per-passage-20201204-f50dcc.tar.gz",
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
        "description": "Lucene index of the MS MARCO document corpus segmented into passages (slim version, document text not stored) (deprecated; use msmarco-v1-doc-segmented-slim instead). (Lucene 8)",
        "filename": "index-msmarco-doc-per-passage-slim-20201204-f50dcc.tar.gz",
        "readme": "index-msmarco-doc-per-passage-slim-20201204-f50dcc-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-per-passage-slim-20201204-f50dcc.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/mKTjbTKMwWF9kY3/download"
        ],
        "md5": "77c2409943a8c9faffabf57cb6adca69",
        "size compressed (bytes)": 2834865200,
        "total_terms": 3197886407,
        "documents": 20544550,
        "unique_terms": 21173582,
        "downloaded": False
    },

    # These MS MARCO V1 doc2query expansion indexes are deprecated, but keeping around for archival reasons
    "msmarco-passage-expanded": {
        "description": "Lucene index of the MS MARCO passage corpus with docTTTTTquery expansions (deprecated; use msmarco-v1-passage-d2q-t5 instead). (Lucene 8)",
        "filename": "index-msmarco-passage-expanded-20201121-e127fb.tar.gz",
        "readme": "index-msmarco-passage-expanded-20201121-e127fb-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-passage-expanded-20201121-e127fb.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/pm7cisJtRxiAMHd/download"
        ],
        "md5": "e5762e9e065b6fe5000f9c18da778565",
        "size compressed (bytes)": 816438546,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },
    "msmarco-doc-expanded-per-doc": {
        "description": "Lucene index of the MS MARCO document corpus with per-doc docTTTTTquery expansions (deprecated; use msmarco-v1-doc-d2q-t5 instead). (Lucene 8)",
        "filename": "index-msmarco-doc-expanded-per-doc-20201126-1b4d0a.tar.gz",
        "readme": "index-msmarco-doc-expanded-per-doc-20201126-1b4d0a-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-expanded-per-doc-20201126-1b4d0a.tar.gz",
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
        "description": "Lucene index of the MS MARCO document corpus with per-passage docTTTTTquery expansions (deprecated; use msmarco-v1-doc-segmented-d2q-t5 instead). (Lucene 8)",
        "filename": "index-msmarco-doc-expanded-per-passage-20201126-1b4d0a.tar.gz",
        "readme": "index-msmarco-doc-expanded-per-passage-20201126-1b4d0a-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/index-msmarco-doc-expanded-per-passage-20201126-1b4d0a.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eZLbPWcnB7LzKnQ/download"
        ],
        "md5": "54ea30c64515edf3c3741291b785be53",
        "size compressed (bytes)": 3069280946,
        "total_terms": 4203956960,
        "documents": 20544550,
        "unique_terms": 22037213,
        "downloaded": False
    },

    # MS MARCO V2 document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-doc-lucene8": {
        "description": "Lucene index of the MS MARCO V2 document corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc.20220111.06fb4f.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/BC7CXiRrTfg9FbD/download"
        ],
        "md5": "3ca8b924f00f11e51e337c5421e55d96",
        "size compressed (bytes)": 63719115316,
        "total_terms": 14165661202,
        "documents": 11959635,
        "unique_terms": 44855557,
        "downloaded": False
    },
    "msmarco-v2-doc-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V2 document corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-slim.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-slim.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-slim.20220111.06fb4f.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/eAjtprNt2fwjQ7F/download"
        ],
        "md5": "502c4c96ecd95e4113a7a26a06065ecf",
        "size compressed (bytes)": 7306072104,
        "total_terms": 14165661202,
        "documents": 11959635,
        "unique_terms": 44855557,
        "downloaded": False
    },
    "msmarco-v2-doc-full-lucene8": {
        "description": "Lucene index of the MS MARCO V2 document corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-full.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-full.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-full.20220111.06fb4f.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/ZqEx5bbznxc9ekd/download"
        ],
        "md5": "cdb600adceccd327cb97c4277f910150",
        "size compressed (bytes)": 119577632837,
        "total_terms": 14165661202,
        "documents": 11959635,
        "unique_terms": 44855557,
        "downloaded": False
    },

    # MS MARCO V2 document corpus, doc2query-T5 expansions.
    "msmarco-v2-doc-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V2 document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/MeTFfBnwffS7gLd/download"
        ],
        "md5": "431391554854c51f347ba38c5e07ef94",
        "size compressed (bytes)": 8254297093,
        "total_terms": 19760777295,
        "documents": 11959635,
        "unique_terms": 54143053,
        "downloaded": False
    },
    "msmarco-v2-doc-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "200176909cd31d750919f38410f20b8a",
        "size compressed (bytes)": 54511069668,
        "total_terms": 19760777295,
        "documents": 11959635,
        "unique_terms": 54143053,
        "downloaded": False
    },

    # MS MARCO V2 segmented document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-doc-segmented-lucene8": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-segmented.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented.20220111.06fb4f.tar.gz"
        ],
        "md5": "cb37211851bd0053227b8db1dd0a3853",
        "size compressed (bytes)": 105646039864,
        "total_terms": 24780915974,
        "documents": 124131414,
        "unique_terms": 29263590,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-slim.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-slim.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-slim.20220111.06fb4f.tar.gz"
        ],
        "md5": "448c1e0e49c38364abbc4d880e865ee5",
        "size compressed (bytes)": 21004046043,
        "total_terms": 24780915974,
        "documents": 124131414,
        "unique_terms": 29263590,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-full-lucene8": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-full.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-full.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-full.20220111.06fb4f.tar.gz"
        ],
        "md5": "bb597b3d03eba00653387ffab8c01998",
        "size compressed (bytes)": 186377654091,
        "total_terms": 24780915974,
        "documents": 124131414,
        "unique_terms": 29263590,
        "downloaded": False
    },

    # MS MARCO V2 segmented document corpus, doc2query-T5 expansions.
    "msmarco-v2-doc-segmented-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/m4DRWpeGW9Dawd7/download"
        ],
        "md5": "3ce9eaca885e1e8a79466bee5e6a4084",
        "size compressed (bytes)": 24125355549,
        "total_terms": 30376032067,
        "documents": 124131414,
        "unique_terms": 38930475,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-doc-segmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "d7fd3d9fbca6ca0b5ffeb8b824db0cd7",
        "size compressed (bytes)": 114312032964,
        "total_terms": 30376032067,
        "documents": 124131414,
        "unique_terms": 38930475,
        "downloaded": False
    },

    # MS MARCO V2 passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-passage-lucene8": {
        "description": "Lucene index of the MS MARCO V2 passage corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage.20220111.06fb4f.tar.gz"
        ],
        "md5": "5990b4938dfdd092888ce9c9dfb6a90c",
        "size compressed (bytes)": 38013278576,
        "total_terms": 4673266762,
        "documents": 138364198,
        "unique_terms": 11885026,
        "downloaded": False
    },
    "msmarco-v2-passage-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V2 passage corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-slim.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-slim.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-slim.20220111.06fb4f.tar.gz"
        ],
        "md5": "b9a6fdf88775b0b546907d4cd84c4a58",
        "size compressed (bytes)": 8174630082,
        "total_terms": 4673266762,
        "documents": 138364198,
        "unique_terms": 11885026,
        "downloaded": False
    },
    "msmarco-v2-passage-full-lucene8": {
        "description": "Lucene index of the MS MARCO V2 passage corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-full.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-full.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-full.20220111.06fb4f.tar.gz"
        ],
        "md5": "a233873bef304dd87adef35f54c7a436",
        "size compressed (bytes)": 59658189636,
        "total_terms": 4673266762,
        "documents": 138364198,
        "unique_terms": 11885026,
        "downloaded": False
    },

    # MS MARCO V2 passage corpus, doc2query-T5 expansions.
    "msmarco-v2-passage-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V2 passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/EiPESdXiikAcbFF/download"
        ],
        "md5": "72f3f0f56b9c7a1bdff836419f2f30bd",
        "size compressed (bytes)": 14431987438,
        "total_terms": 16961479226,
        "documents": 138364198,
        "unique_terms": 36650715,
        "downloaded": False
    },
    "msmarco-v2-passage-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "e0ed749284f67db1f0890cb709ecb690",
        "size compressed (bytes)": 59320157969,
        "total_terms": 16961479226,
        "documents": 138364198,
        "unique_terms": 36650715,
        "downloaded": False
    },

    # MS MARCO V2 augmented passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v2-passage-augmented-lucene8": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-augmented.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented.20220111.06fb4f.tar.gz"
        ],
        "md5": "975f6be8d49238fe1d47e2895d26f99e",
        "size compressed (bytes)": 65574361728,
        "total_terms": 15272964956,
        "documents": 138364198,
        "unique_terms": 16579071,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-slim-lucene8": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('slim' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-slim.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-slim.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-slim.20220111.06fb4f.tar.gz"
        ],
        "md5": "af893e56d050a98b6646ce2ca063d3f4",
        "size compressed (bytes)": 117322378611,
        "total_terms": 15272964956,
        "documents": 138364198,
        "unique_terms": 16579071,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-full-lucene8": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('full' version). (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-full.20220111.06fb4f.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-full.20220111.06fb4f.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-full.20220111.06fb4f.tar.gz"
        ],
        "md5": "e99f99503b9e030424546d59239f0cb5",
        "size compressed (bytes)": 14819003760,
        "total_terms": 15272964956,
        "documents": 138364198,
        "unique_terms": 16579071,
        "downloaded": False
    },

    # MS MARCO V2 augmented passage corpus, doc2query-T5 expansions.
    "msmarco-v2-passage-augmented-d2q-t5-lucene8": {
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220201.9ea315.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220201.9ea315.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-d2q-t5.20220201.9ea315.tar.gz",
            "https://vault.cs.uwaterloo.ca/s/44EDc5a9aCbHZNW/download"
        ],
        "md5": "f248becbe3ef3fffc39680cff417791d",
        "size compressed (bytes)": 20940452572,
        "total_terms": 27561177420,
        "documents": 138364198,
        "unique_terms": 41176227,
        "downloaded": False
    },
    "msmarco-v2-passage-augmented-d2q-t5-docvectors-lucene8": {
        "description": "Lucene index (+docvectors) of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions. (Lucene 8; deprecated)",
        "filename": "lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220525.30c997.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-augmented-d2q-t5-docvectors.20220525.30c997.tar.gz",
        ],
        "md5": "8fc1cc2b71331772ff7b306cd62794f6",
        "size compressed (bytes)": 96122355388,
        "total_terms": 27561177420,
        "documents": 138364198,
        "unique_terms": 41176227,
        "downloaded": False
    },

    # BEIR (v1.0.0) flat indexes (Lucene 8; deprecated)
    "beir-v1.0.0-trec-covid-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-COVID. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-covid-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "d8574b8263df5dc337b443c4c35d384f",
        "size compressed (bytes)": 226745226,
        "total_terms": 20822810,
        "documents": 171331,
        "unique_terms": 202643,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): BioASQ. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-bioasq-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-bioasq-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "ab4823b0b59dbb59ae72c2689b73133c",
        "size compressed (bytes)": 24861183683,
        "total_terms": 2257541768,
        "documents": 14914603,
        "unique_terms": 4959999,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): NFCorpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nfcorpus-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "b52e0f918eb3a5517289980850dec55c",
        "size compressed (bytes)": 6508815,
        "total_terms": 637485,
        "documents": 3633,
        "unique_terms": 22111,
        "downloaded": False
    },
    "beir-v1.0.0-nq-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): NQ. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nq-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nq-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "71c35db0343ba9800c6b34510acbfb4f",
        "size compressed (bytes)": 1650195223,
        "total_terms": 151249287,
        "documents": 2681468,
        "unique_terms": 997009,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): HotpotQA. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-hotpotqa-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "431995b33471f183272bb84d9499d8f6",
        "size compressed (bytes)": 2027634934,
        "total_terms": 172477063,
        "documents": 5233329,
        "unique_terms": 2644887,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): FiQA-2018. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fiqa-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fiqa-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "332ec18504778b03e330847a006541d4",
        "size compressed (bytes)": 56101137,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): Signal-1M. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-signal1m-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-signal1m-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "95b279bbd4533b631967540647f18476",
        "size compressed (bytes)": 499183897,
        "total_terms": 32240067,
        "documents": 2866315,
        "unique_terms": 796646,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-NEWS. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-news-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-news-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "9f78f049ffdcac5f6f55cd118e008bdb",
        "size compressed (bytes)": 2630489172,
        "total_terms": 275651967,
        "documents": 594589,
        "unique_terms": 729872,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): Robust04. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-robust04-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-robust04-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "a9340eeedb444a303afbf974ba1872d5",
        "size compressed (bytes)": 1731243578,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): ArguAna. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-arguana-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-arguana-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "62ba65fa619e7f1c9e48850974ab242d",
        "size compressed (bytes)": 10563170,
        "total_terms": 969528,
        "documents": 8674,
        "unique_terms": 23895,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): Webis-Touche2020. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-webis-touche2020-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "9e43abfd1de98da6671df90bba8486a1",
        "size compressed (bytes)": 751902399,
        "total_terms": 76082209,
        "documents": 382545,
        "unique_terms": 525540,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-android. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-android-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "870b2ddfd59abb96a74c00515122b9e1",
        "size compressed (bytes)": 17466940,
        "total_terms": 1760761,
        "documents": 22998,
        "unique_terms": 41455,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-english. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-english-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "bdcfe2cb5798b79405cba1185ad4ad38",
        "size compressed (bytes)": 24992357,
        "total_terms": 2236655,
        "documents": 40221,
        "unique_terms": 62517,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gaming. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "92fc7435b1ee64783c4a97eea9d2c4a4",
        "size compressed (bytes)": 29224430,
        "total_terms": 2827717,
        "documents": 45301,
        "unique_terms": 60070,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gis. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "80c3dcc4b3fd39a1125537b587f27436",
        "size compressed (bytes)": 43466795,
        "total_terms": 4048584,
        "documents": 37637,
        "unique_terms": 184133,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-mathematica. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "359c577e5a4f9a48e7b61fbd70447121",
        "size compressed (bytes)": 21621544,
        "total_terms": 2332642,
        "documents": 16705,
        "unique_terms": 111611,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-physics. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "3f4a0c885463a50038893c5169374e56",
        "size compressed (bytes)": 38016173,
        "total_terms": 3785483,
        "documents": 38316,
        "unique_terms": 55950,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-programmers. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "2b0be6fc6d9623201540cbcb2f4881ab",
        "size compressed (bytes)": 40373220,
        "total_terms": 3905694,
        "documents": 32176,
        "unique_terms": 74195,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-stats. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "ce64d853969bde0fecea2228c1258944",
        "size compressed (bytes)": 52283784,
        "total_terms": 5356042,
        "documents": 42269,
        "unique_terms": 183358,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-tex. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "558efcfba599b0e8e7a95a41df4dc5f2",
        "size compressed (bytes)": 91968319,
        "total_terms": 9556422,
        "documents": 68184,
        "unique_terms": 288087,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-unix. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "a3c6cbfc1e81d98abc6cc4380a8f19d2",
        "size compressed (bytes)": 53892386,
        "total_terms": 5767374,
        "documents": 47382,
        "unique_terms": 206323,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-webmasters. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "fa35ece230cb4d85a5e4ad5de0fd9240",
        "size compressed (bytes)": 15204463,
        "total_terms": 1482585,
        "documents": 17405,
        "unique_terms": 40547,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-wordpress. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "5a3591b6ff9ce5a97d1600f8a8cd63e8",
        "size compressed (bytes)": 54895441,
        "total_terms": 5463472,
        "documents": 48605,
        "unique_terms": 125727,
        "downloaded": False
    },
    "beir-v1.0.0-quora-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): Quora. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-quora-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-quora-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "dde92b4610b08282d11e7a4465b29181",
        "size compressed (bytes)": 52750359,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): DBPedia. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-dbpedia-entity-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "0d38ea1abf89644bb7d39e74cc4dd2d9",
        "size compressed (bytes)": 2079898414,
        "total_terms": 164794987,
        "documents": 4635922,
        "unique_terms": 3351449,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): SCIDOCS. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scidocs-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scidocs-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "09a0ea1853445be14da2afb0bc47335e",
        "size compressed (bytes)": 186605163,
        "total_terms": 3266767,
        "documents": 25657,
        "unique_terms": 63604,
        "downloaded": False
    },
    "beir-v1.0.0-fever-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): FEVER. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fever-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fever-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "63cd5f369b5952386f138efe45571d41",
        "size compressed (bytes)": 3878535207,
        "total_terms": 325179170,
        "documents": 5416568,
        "unique_terms": 3293639,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): Climate-FEVER. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-climate-fever-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "9af959cf58139d086d52121917913a02",
        "size compressed (bytes)": 3878606250,
        "total_terms": 325185077,
        "documents": 5416593,
        "unique_terms": 3293621,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-flat-lucene8": {
        "description": "Lucene flat index of BEIR (v1.0.0): SciFact. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scifact-flat.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scifact-flat.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-flat.20220501.1842ee.tar.gz"
        ],
        "md5": "8c79300afd78acb95f127c58682fc881",
        "size compressed (bytes)": 8851845,
        "total_terms": 838128,
        "documents": 5183,
        "unique_terms": 28865,
        "downloaded": False
    },

    # BEIR (v1.0.0) multifield indexes (Lucene 8; deprecated)
    "beir-v1.0.0-trec-covid-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-COVID. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-covid-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-covid-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-covid-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "2dabcca159c157215ae59b1899c495a8",
        "size compressed (bytes)": 223251753,
        "total_terms": 19060111,
        "documents": 129192,
        "unique_terms": 193846,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): BioASQ. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-bioasq-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-bioasq-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-bioasq-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "723dcc48c961a9faef23e41cc0f372b0",
        "size compressed (bytes)": 25390117017,
        "total_terms": 2099554317,
        "documents": 14914602,
        "unique_terms": 4889048,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NFCorpus. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nfcorpus-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nfcorpus-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nfcorpus-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "7c6a63153cca484bd85510d9ffc7c62e",
        "size compressed (bytes)": 6644821,
        "total_terms": 601950,
        "documents": 3633,
        "unique_terms": 21819,
        "downloaded": False
    },
    "beir-v1.0.0-nq-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NQ. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-nq-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-nq-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-nq-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "3642ab8879de1c37993347d164694885",
        "size compressed (bytes)": 1647410313,
        "total_terms": 144050884,
        "documents": 2680961,
        "unique_terms": 996635,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): HotpotQA. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-hotpotqa-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-hotpotqa-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-hotpotqa-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "fa80379866ff06ad905d70ba1d4d55e3",
        "size compressed (bytes)": 2092477199,
        "total_terms": 158180689,
        "documents": 5233235,
        "unique_terms": 2627634,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FiQA-2018. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fiqa-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fiqa-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fiqa-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "2cc96d72349f5f864235a88303af5da9",
        "size compressed (bytes)": 56101140,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Signal-1M. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-signal1m-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-signal1m-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-signal1m-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "16a8c34363c69afc820af20ec6ec0848",
        "size compressed (bytes)": 499183933,
        "total_terms": 32240067,
        "documents": 2866315,
        "unique_terms": 796646,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-NEWS. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-trec-news-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-trec-news-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-trec-news-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "91390f9e059ba04479f3550cca166a65",
        "size compressed (bytes)": 2640469722,
        "total_terms": 270886723,
        "documents": 578605,
        "unique_terms": 727856,
        "downloaded": False
    },
    "beir-v1.0.0-robust04-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Robust04. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-robust04-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-robust04-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-robust04-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "f9821cef4dc903772dec283cc8c9e0f5",
        "size compressed (bytes)": 1731243641,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): ArguAna. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-arguana-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-arguana-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-arguana-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "d22aa6b4247535dedb78b3f876d958e7",
        "size compressed (bytes)": 10523627,
        "total_terms": 944123,
        "documents": 8674,
        "unique_terms": 23867,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Webis-Touche2020. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-webis-touche2020-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-webis-touche2020-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-webis-touche2020-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "f9d1601b76bdbafef6bfa335bf1d1595",
        "size compressed (bytes)": 752116420,
        "total_terms": 74066724,
        "documents": 382545,
        "unique_terms": 524665,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-android. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "05801b35a25af7c16172255512b4ce36",
        "size compressed (bytes)": 17931810,
        "total_terms": 1591284,
        "documents": 22998,
        "unique_terms": 40823,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-english. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "bf9eef1c5fd10b66b6816f272e7872e1",
        "size compressed (bytes)": 25605309,
        "total_terms": 2006983,
        "documents": 40221,
        "unique_terms": 61530,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gaming. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "3393426ddc796ce263ffb318a6d2bfed",
        "size compressed (bytes)": 30065920,
        "total_terms": 2510477,
        "documents": 45300,
        "unique_terms": 59113,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gis. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "f69c20cdd61ca7d59ba13e46d8119f5c",
        "size compressed (bytes)": 44265052,
        "total_terms": 3789161,
        "documents": 37637,
        "unique_terms": 183298,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-mathematica. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "74ef57dcbca928d6ac77b79bb9e6c9ad",
        "size compressed (bytes)": 21944398,
        "total_terms": 2234369,
        "documents": 16705,
        "unique_terms": 111306,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-physics. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "be67a3ae1f91fbe3fb26262e695871f3",
        "size compressed (bytes)": 38801084,
        "total_terms": 3542078,
        "documents": 38316,
        "unique_terms": 55229,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-programmers. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "8d40c0e813171a68ea27da42e1943ebe",
        "size compressed (bytes)": 41061263,
        "total_terms": 3682227,
        "documents": 32176,
        "unique_terms": 73765,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-stats. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "d00eec70ebfba38d32e5d588be7e0d74",
        "size compressed (bytes)": 53164818,
        "total_terms": 5073873,
        "documents": 42269,
        "unique_terms": 182933,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-tex. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "6952954b17ebe87987c08d1994bcb801",
        "size compressed (bytes)": 93231672,
        "total_terms": 9155404,
        "documents": 68184,
        "unique_terms": 287392,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-unix. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "858632caf3b93fd0ce6f2c4cdc95503b",
        "size compressed (bytes)": 54854147,
        "total_terms": 5449726,
        "documents": 47382,
        "unique_terms": 205471,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-webmasters. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "d40fbb1d750a8d4bfcb77edd3d74e758",
        "size compressed (bytes)": 15560909,
        "total_terms": 1358292,
        "documents": 17405,
        "unique_terms": 40073,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-wordpress. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "938abf49a6835006e1b29b1bcd28602f",
        "size compressed (bytes)": 55833972,
        "total_terms": 5151575,
        "documents": 48605,
        "unique_terms": 125110,
        "downloaded": False
    },
    "beir-v1.0.0-quora-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Quora. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-quora-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-quora-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-quora-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "0812beec31e051515524c746323e0ee2",
        "size compressed (bytes)": 52750399,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): DBPedia. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "0834295cdc4e955cb9052b24a56f074b",
        "size compressed (bytes)": 2139032416,
        "total_terms": 152205484,
        "documents": 4635922,
        "unique_terms": 3338466,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SCIDOCS. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scidocs-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scidocs-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scidocs-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "0944c45ccf3ab5bb3cee5f1863725114",
        "size compressed (bytes)": 175925466,
        "total_terms": 3065828,
        "documents": 25313,
        "unique_terms": 62562,
        "downloaded": False
    },
    "beir-v1.0.0-fever-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FEVER. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-fever-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-fever-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-fever-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "3ba53efbdbeed974a641c7dc5860dbc8",
        "size compressed (bytes)": 3946159718,
        "total_terms": 310655704,
        "documents": 5396138,
        "unique_terms": 3275057,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Climate-FEVER. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-climate-fever-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-climate-fever-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-climate-fever-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "998e9e9aa3d91c8022e1f8cae3f75a5f",
        "size compressed (bytes)": 3946246078,
        "total_terms": 310661482,
        "documents": 5396163,
        "unique_terms": 3275068,
        "downloaded": False
    },
    "beir-v1.0.0-scifact-multifield-lucene8": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SciFact. (Lucene 8; deprecated)",
        "filename": "lucene-index.beir-v1.0.0-scifact-multifield.20220501.1842ee.tar.gz",
        "readme": "lucene-index.beir-v1.0.0-scifact-multifield.20220501.1842ee.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.beir-v1.0.0-scifact-multifield.20220501.1842ee.tar.gz"
        ],
        "md5": "a72d8c62859a2434fba2e0034268dbe4",
        "size compressed (bytes)": 9078043,
        "total_terms": 784591,
        "documents": 5183,
        "unique_terms": 28581,
        "downloaded": False
    }

}

TF_INDEX_INFO = {**TF_INDEX_INFO_CURRENT, **TF_INDEX_INFO_DEPRECATED}

IMPACT_INDEX_INFO_CURRENT = {
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
        "filename": "faiss.miracl-v1.0-ar.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-bn.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-en.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-es.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-fa.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-fi.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-fr.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-hi.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-id.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-ja.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-ko.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-ru.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-sw.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-te.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-th.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-zh.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-de.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-yo.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-arabic.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "428fbde84d2c18e48f0821298947a9d1",
        "size compressed (bytes)": 5866199790,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "4394a09e043be9be5b820814a82fc8ac",
        "size compressed (bytes)": 846476050,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "5bd57f5e4daf93294fd2cbd969c05bb3",
        "size compressed (bytes)": 93527497283,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b6db16c1ab0ae95fec0465299c660d2a",
        "size compressed (bytes)": 29544413180,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "2a2825706211eb96bd3dbb616463c661",
        "size compressed (bytes)": 6283957262,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "65719de730cda3fa5f6a8a75611db6eb",
        "size compressed (bytes)": 5363289277,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "24eb2f63f78aa1e39b1ea61e20661424",
        "size compressed (bytes)": 41635104326,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "d08aad08a8592aa40355fb7d50afd170",
        "size compressed (bytes)": 1439798033,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b02c20d4fc27e390ec5b1e9ca732dc5a",
        "size compressed (bytes)": 4113737773,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5f219c7f46a36c5c7a2555fbdaa0479",
        "size compressed (bytes)": 19790154560,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "67b2a803eab3491a057d4ac6b81974f1",
        "size compressed (bytes)": 4230830690,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-korean"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "edad6d5cb508de61ba84173d0ad2aa31",
        "size compressed (bytes)": 27169921407,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "0b039d766b55f678102a59a6e050d0bc",
        "size compressed (bytes)": 375865677,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "ea21915c69f70f41acadee4b6b83d129",
        "size compressed (bytes)": 1474866678,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5875b473109310789710e2f3df91b0f",
        "size compressed (bytes)": 1540180247,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a2d233e792d46c20c912d10afff033f5",
        "size compressed (bytes)": 14043150097,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.20221004.2b2856.tar.gz",
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
        "filename": "faiss.miracl-v1.0-yo.20221004.2b2856.tar.gz",
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
}

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


TF_INDEX_INFO_MSMARCO = {
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
    }
}

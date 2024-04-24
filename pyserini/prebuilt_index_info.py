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
        "description": "Lucene index of the MS MARCO V1 document corpus.",
        "filename": "lucene-inverted.msmarco-v1-doc.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc.20221004.252b5e.tar.gz",
        ],
        "md5": "f66020a923df6430007bd5718e53de86",
        "size compressed (bytes)": 13736982339,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },
    "msmarco-v1-doc-slim": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('slim' version).",
        "filename": "lucene-inverted.msmarco-v1-doc-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "1ac67c1150d5e6c9ec2b70b3ce1fb5e0",
        "size compressed (bytes)": 1791498091,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },
    "msmarco-v1-doc-full": {
        "description": "Lucene index of the MS MARCO V1 document corpus ('full' version).",
        "filename": "lucene-inverted.msmarco-v1-doc-full.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-full.20221004.252b5e.tar.gz",
        ],
        "md5": "4975ca1b175343705b899c1e609234f9",
        "size compressed (bytes)": 25525613395,
        "total_terms": 2742219865,
        "documents": 3213835,
        "unique_terms": 29823777,
        "downloaded": False
    },

    # MS MARCO V1 document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc.d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 document corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "c0b0a25c329c1bdd7df3189400ec2f38",
        "size compressed (bytes)": 1885596445,
        "total_terms": 3748343494,
        "documents": 3213835,
        "unique_terms": 30631009,
        "downloaded": False
    },
    "msmarco-v1-doc.d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 document corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-doc.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "3c7c47c5cb718081da91d36b81d0d820",
        "size compressed (bytes)": 11152231392,
        "total_terms": 3748343494,
        "documents": 3213835,
        "unique_terms": 30631009,
        "downloaded": False
    },

    # MS MARCO V1 segmented document corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-doc-segmented": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus.",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.tar.gz",
        ],
        "md5": "dbf968dbf6e9d64119b4e320334524aa",
        "size compressed (bytes)": 15924437950,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-slim": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('slim' version).",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "8ab6f2a49e8a6f3157615c2f0d746e3a",
        "size compressed (bytes)": 3306727065,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented-full": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus ('full' version).",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented-full.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented-full.20221004.252b5e.tar.gz",
        ],
        "md5": "3571ca047669b1e6dee5bcd8a640ef18",
        "size compressed (bytes)": 29470600225,
        "total_terms": 3200522554,
        "documents": 20545677,
        "unique_terms": 21191748,
        "downloaded": False
    },

    # MS MARCO V1 segmented document corpus, doc2query-T5 expansions.
    "msmarco-v1-doc-segmented.d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "c76e514df930721401c215b90f9f5d14",
        "size compressed (bytes)": 3554554591,
        "total_terms": 4206646183,
        "documents": 20545677,
        "unique_terms": 22055268,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented.d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 segmented document corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "38e364692cd9c892ebb6f05b3255f0fb",
        "size compressed (bytes)": 16349673467,
        "total_terms": 4206646183,
        "documents": 20545677,
        "unique_terms": 22055268,
        "downloaded": False
    },

    # MS MARCO V1 passage corpus, three indexes with different amounts of information (and sizes).
    "msmarco-v1-passage": {
        "description": "Lucene index of the MS MARCO V1 passage corpus.",
        "filename": "lucene-inverted.msmarco-v1-passage.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.20221004.252b5e.tar.gz",
        ],
        "md5": "678876e8c99a89933d553609a0fd8793",
        "size compressed (bytes)": 2170758745,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-slim": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('slim' version).",
        "filename": "lucene-inverted.msmarco-v1-passage-slim.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage-slim.20221004.252b5e.tar.gz",
        ],
        "md5": "229c750cc39eaa25f0c37bf69c2c708f",
        "size compressed (bytes)": 491451223,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },
    "msmarco-v1-passage-full": {
        "description": "Lucene index of the MS MARCO V1 passage corpus ('full' version).",
        "filename": "lucene-inverted.msmarco-v1-passage-full.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage-full.20221004.252b5e.tar.gz",
        ],
        "md5": "4d2e2e1fdb7ffc7c9758c4c2234261a1",
        "size compressed (bytes)": 3720616156,
        "total_terms": 352316036,
        "documents": 8841823,
        "unique_terms": 2660824,
        "downloaded": False
    },

    # MS MARCO V1 passage corpus, doc2query-T5 expansions.
    "msmarco-v1-passage.d2q-t5": {
        "description": "Lucene index of the MS MARCO V1 passage corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.tar.gz",
        ],
        "md5": "cfd6acef0912647603457b1e98ca5bc0",
        "size compressed (bytes)": 807866520,
        "total_terms": 1986612263,
        "documents": 8841823,
        "unique_terms": 3929111,
        "downloaded": False
    },
    "msmarco-v1-passage.d2q-t5-docvectors": {
        "description": "Lucene index (+docvectors) of the MS MARCO V1 passage corpus with doc2query-T5 expansions.",
        "filename": "lucene-inverted.msmarco-v1-passage.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.d2q-t5.20221004.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.d2q-t5-docvectors.20221004.252b5e.tar.gz",
        ],
        "md5": "3be8131464c2d1db23c8d6151c55740e",
        "size compressed (bytes)": 4409861674,
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
        "description": "Lucene index of the MS MARCO V2 document corpus.",
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
        "description": "Lucene index of the MS MARCO V2 document corpus ('slim' version).",
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
        "description": "Lucene index of the MS MARCO V2 document corpus ('full' version).",
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
        "description": "Lucene index of the MS MARCO V2 document corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index (+docvectors) of the MS MARCO V2 document corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index of the MS MARCO V2 segmented document corpus.",
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
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('slim' version).",
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
        "description": "Lucene index of the MS MARCO V2 segmented document corpus ('full' version).",
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
        "description": "Lucene index of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index (+docvectors) of the MS MARCO V2 segmented document corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index of the MS MARCO V2 passage corpus.",
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
        "description": "Lucene index of the MS MARCO V2 passage corpus ('slim' version).",
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
        "description": "Lucene index of the MS MARCO V2 passage corpus ('full' version).",
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
        "description": "Lucene index of the MS MARCO V2 passage corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index (+docvectors) of the MS MARCO V2 passage corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus.",
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
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('slim' version).",
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
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus ('full' version).",
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
        "description": "Lucene index of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.",
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
        "description": "Lucene index (+docvectors) of the MS MARCO V2 augmented passage corpus with doc2query-T5 expansions.",
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

TF_INDEX_INFO_MSMARCO_ALIASES = {
    # To preserve working commands in published papers: integrations/papers/test_sigir2021.py testcase test_section3_3
    "msmarco-passage": TF_INDEX_INFO_MSMARCO["msmarco-v1-passage"],
    # To preserve working commands in published papers: integrations/papers/test_sigir2022.py testcase test_Ma_etal_section4_1a
    "msmarco-v1-passage-d2q-t5": TF_INDEX_INFO_MSMARCO["msmarco-v1-passage.d2q-t5"],
}

TF_INDEX_INFO_BEIR = {
    # BEIR (v1.0.0) flat indexes
    "beir-v1.0.0-trec-covid.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-COVID.",
        "filename": "lucene-inverted.beir-v1.0.0-trec-covid.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-covid.flat.20221116.505594.tar.gz"
        ],
        "md5": "1aaf107b0787aa349deac92cb67d4230",
        "size compressed (bytes)": 226271040,
        "total_terms": 20822821,
        "documents": 171331,
        "unique_terms": 202648,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): BioASQ.",
        "filename": "lucene-inverted.beir-v1.0.0-bioasq.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-bioasq.flat.20221116.505594.tar.gz"
        ],
        "md5": "12728b3629817d352322f18b0cb6199b",
        "size compressed (bytes)": 24821943492,
        "total_terms": 2257541758,
        "documents": 14914603,
        "unique_terms": 4960004,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): NFCorpus.",
        "filename": "lucene-inverted.beir-v1.0.0-nfcorpus.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nfcorpus.flat.20221116.505594.tar.gz"
        ],
        "md5": "eb7a6f1bb15071c2940bc50752d86626",
        "size compressed (bytes)": 6510365,
        "total_terms": 637485,
        "documents": 3633,
        "unique_terms": 22111,
        "downloaded": False
    },
    "beir-v1.0.0-nq.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): NQ.",
        "filename": "lucene-inverted.beir-v1.0.0-nq.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nq.flat.20221116.505594.tar.gz"
        ],
        "md5": "0ba1ef0412d8a0fb56b4a04ecb13ef0b",
        "size compressed (bytes)": 1645445055,
        "total_terms": 151249294,
        "documents": 2681468,
        "unique_terms": 997027,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): HotpotQA.",
        "filename": "lucene-inverted.beir-v1.0.0-hotpotqa.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-hotpotqa.flat.20221116.505594.tar.gz"
        ],
        "md5": "3f41d640a8ebbcad4f598140750c24f8",
        "size compressed (bytes)": 2019088696,
        "total_terms": 172477066,
        "documents": 5233329,
        "unique_terms": 2644892,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): FiQA-2018.",
        "filename": "lucene-inverted.beir-v1.0.0-fiqa.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fiqa.flat.20221116.505594.tar.gz"
        ],
        "md5": "d98ee6ebfc234657ecbd04226e8a7849",
        "size compressed (bytes)": 55983760,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Signal-1M.",
        "filename": "lucene-inverted.beir-v1.0.0-signal1m.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-signal1m.flat.20221116.505594.tar.gz"
        ],
        "md5": "93d901916b473351fbc04fdf12c5ba4f",
        "size compressed (bytes)": 496598928,
        "total_terms": 32240069,
        "documents": 2866315,
        "unique_terms": 796647,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): TREC-NEWS.",
        "filename": "lucene-inverted.beir-v1.0.0-trec-news.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-news.flat.20221116.505594.tar.gz"
        ],
        "md5": "22e7752c3d0122c28013b33e5e2134ae",
        "size compressed (bytes)": 2623562099,
        "total_terms": 275651967,
        "documents": 594589,
        "unique_terms": 729872,
        "downloaded": False
    },
    "beir-v1.0.0-robust04.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Robust04.",
        "filename": "lucene-inverted.beir-v1.0.0-robust04.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-robust04.flat.20221116.505594.tar.gz"
        ],
        "md5": "d508fc770002a99a5dc3da3d0fa001b7",
        "size compressed (bytes)": 1728445005,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): ArguAna.",
        "filename": "lucene-inverted.beir-v1.0.0-arguana.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-arguana.flat.20221116.505594.tar.gz"
        ],
        "md5": "db59ef0cb74e9cfeac0ac735827381df",
        "size compressed (bytes)": 10562079,
        "total_terms": 969528,
        "documents": 8674,
        "unique_terms": 23895,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Webis-Touche2020.",
        "filename": "lucene-inverted.beir-v1.0.0-webis-touche2020.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-webis-touche2020.flat.20221116.505594.tar.gz"
        ],
        "md5": "f6419ddfd53c0bf1d76ea132b1c0c352",
        "size compressed (bytes)": 750402985,
        "total_terms": 76082209,
        "documents": 382545,
        "unique_terms": 525540,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-android.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-android.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-android.flat.20221116.505594.tar.gz"
        ],
        "md5": "443e413b49c39de43a6cece96a7513c0",
        "size compressed (bytes)": 17426545,
        "total_terms": 1760762,
        "documents": 22998,
        "unique_terms": 41456,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-english.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-english.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-english.flat.20221116.505594.tar.gz"
        ],
        "md5": "f7db543f5bb56fa98c3c14224c6b96f2",
        "size compressed (bytes)": 24945030,
        "total_terms": 2236655,
        "documents": 40221,
        "unique_terms": 62517,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gaming.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gaming.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gaming.flat.20221116.505594.tar.gz"
        ],
        "md5": "775169fd863d3e91076e1905799456ea",
        "size compressed (bytes)": 29159238,
        "total_terms": 2827717,
        "documents": 45301,
        "unique_terms": 60070,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-gis.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gis.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gis.flat.20221116.505594.tar.gz"
        ],
        "md5": "4c5be1c7026a61ca7866b4f28cac91fe",
        "size compressed (bytes)": 43393675,
        "total_terms": 4048584,
        "documents": 37637,
        "unique_terms": 184133,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-mathematica.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.flat.20221116.505594.tar.gz"
        ],
        "md5": "43e2b33db7ecadc041165005aa5d4b6f",
        "size compressed (bytes)": 21593600,
        "total_terms": 2332642,
        "documents": 16705,
        "unique_terms": 111611,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-physics.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-physics.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-physics.flat.20221116.505594.tar.gz"
        ],
        "md5": "765b8013595962e01600f4f851e8f16d",
        "size compressed (bytes)": 37955556,
        "total_terms": 3785483,
        "documents": 38316,
        "unique_terms": 55950,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-programmers.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-programmers.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-programmers.flat.20221116.505594.tar.gz"
        ],
        "md5": "aa4fc9f29a0436a6e0942656274ceaf5",
        "size compressed (bytes)": 40301156,
        "total_terms": 3905694,
        "documents": 32176,
        "unique_terms": 74195,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-stats.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-stats.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-stats.flat.20221116.505594.tar.gz"
        ],
        "md5": "d56538f56d982ce09961d4b680bd4dc5",
        "size compressed (bytes)": 52213800,
        "total_terms": 5356042,
        "documents": 42269,
        "unique_terms": 183358,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-tex.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-tex.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-tex.flat.20221116.505594.tar.gz"
        ],
        "md5": "36825b8428aa34fdaad7e420e120c101",
        "size compressed (bytes)": 91817321,
        "total_terms": 9556423,
        "documents": 68184,
        "unique_terms": 288088,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-unix.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-unix.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-unix.flat.20221116.505594.tar.gz"
        ],
        "md5": "961e386016c7eb7afa2bc26feb96902c",
        "size compressed (bytes)": 53798364,
        "total_terms": 5767374,
        "documents": 47382,
        "unique_terms": 206323,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-webmasters.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.flat.20221116.505594.tar.gz"
        ],
        "md5": "f31625436dc6efc24b9c2ae1b0f2364e",
        "size compressed (bytes)": 15171145,
        "total_terms": 1482585,
        "documents": 17405,
        "unique_terms": 40547,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): CQADupStack-wordpress.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.flat.20221116.505594.tar.gz"
        ],
        "md5": "5a0035fbb6ccabd20fe0eed742dce0d0",
        "size compressed (bytes)": 54809846,
        "total_terms": 5463472,
        "documents": 48605,
        "unique_terms": 125727,
        "downloaded": False
    },
    "beir-v1.0.0-quora.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Quora.",
        "filename": "lucene-inverted.beir-v1.0.0-quora.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-quora.flat.20221116.505594.tar.gz"
        ],
        "md5": "48c95c2da43e24cc603695d3e6bfd779",
        "size compressed (bytes)": 52699889,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): DBPedia.",
        "filename": "lucene-inverted.beir-v1.0.0-dbpedia-entity.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-dbpedia-entity.flat.20221116.505594.tar.gz"
        ],
        "md5": "8ac66272fde08ff10491dc0ec52f17e2",
        "size compressed (bytes)": 2085481920,
        "total_terms": 164794982,
        "documents": 4635922,
        "unique_terms": 3351459,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): SCIDOCS.",
        "filename": "lucene-inverted.beir-v1.0.0-scidocs.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scidocs.flat.20221116.505594.tar.gz"
        ],
        "md5": "9555ecc5da399a73956d9302a98420fc",
        "size compressed (bytes)": 186568206,
        "total_terms": 3266767,
        "documents": 25657,
        "unique_terms": 63604,
        "downloaded": False
    },
    "beir-v1.0.0-fever.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): FEVER.",
        "filename": "lucene-inverted.beir-v1.0.0-fever.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fever.flat.20221116.505594.tar.gz"
        ],
        "md5": "30b5a338f9f16669ed3dae3bae4e7b32",
        "size compressed (bytes)": 3880157241,
        "total_terms": 325179165,
        "documents": 5416568,
        "unique_terms": 3293639,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): Climate-FEVER.",
        "filename": "lucene-inverted.beir-v1.0.0-climate-fever.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-climate-fever.flat.20221116.505594.tar.gz"
        ],
        "md5": "6e7101f4a5c241ba263bb6a826049826",
        "size compressed (bytes)": 3880210072,
        "total_terms": 325185072,
        "documents": 5416593,
        "unique_terms": 3293621,
        "downloaded": False
    },
    "beir-v1.0.0-scifact.flat": {
        "description": "Lucene flat index of BEIR (v1.0.0): SciFact.",
        "filename": "lucene-inverted.beir-v1.0.0-scifact.flat.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-flat.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scifact.flat.20221116.505594.tar.gz"
        ],
        "md5": "59777038fe0539e600658591e322ea57",
        "size compressed (bytes)": 8849995,
        "total_terms": 838128,
        "documents": 5183,
        "unique_terms": 28865,
        "downloaded": False
    },

    # BEIR (v1.0.0) multifield indexes
    "beir-v1.0.0-trec-covid.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-COVID.",
        "filename": "lucene-inverted.beir-v1.0.0-trec-covid.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-covid.multifield.20221116.505594.tar.gz"
        ],
        "md5": "0439617a927a33727c7b592bd436d8d6",
        "size compressed (bytes)": 222842016,
        "total_terms": 19060122,
        "documents": 129192,
        "unique_terms": 193851,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): BioASQ.",
        "filename": "lucene-inverted.beir-v1.0.0-bioasq.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-bioasq.multifield.20221116.505594.tar.gz"
        ],
        "md5": "b2f4fed18b04414193f8368b6891e19c",
        "size compressed (bytes)": 25346387550,
        "total_terms": 2099554307,
        "documents": 14914602,
        "unique_terms": 4889053,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NFCorpus.",
        "filename": "lucene-inverted.beir-v1.0.0-nfcorpus.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nfcorpus.multifield.20221116.505594.tar.gz"
        ],
        "md5": "85cdcceaf06c482ab6a60c34c06c0448",
        "size compressed (bytes)": 6648624,
        "total_terms": 601950,
        "documents": 3633,
        "unique_terms": 21819,
        "downloaded": False
    },
    "beir-v1.0.0-nq.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): NQ.",
        "filename": "lucene-inverted.beir-v1.0.0-nq.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nq.multifield.20221116.505594.tar.gz"
        ],
        "md5": "73b3e3c49c2d79a2851c1ba85f8fbbdf",
        "size compressed (bytes)": 1642710572,
        "total_terms": 144050891,
        "documents": 2680961,
        "unique_terms": 996653,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): HotpotQA.",
        "filename": "lucene-inverted.beir-v1.0.0-hotpotqa.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-hotpotqa.multifield.20221116.505594.tar.gz"
        ],
        "md5": "1d9f75122d4b50cb33cccaa125640a38",
        "size compressed (bytes)": 2083442675,
        "total_terms": 158180692,
        "documents": 5233235,
        "unique_terms": 2627639,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FiQA-2018.",
        "filename": "lucene-inverted.beir-v1.0.0-fiqa.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fiqa.multifield.20221116.505594.tar.gz"
        ],
        "md5": "1c9330baf3d9004ae46778d4d9e039f6",
        "size compressed (bytes)": 55983827,
        "total_terms": 5288635,
        "documents": 57600,
        "unique_terms": 66977,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Signal-1M.",
        "filename": "lucene-inverted.beir-v1.0.0-signal1m.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-signal1m.multifield.20221116.505594.tar.gz"
        ],
        "md5": "0735de4f103330975d206285ea85aaf5",
        "size compressed (bytes)": 496598936,
        "total_terms": 32240069,
        "documents": 2866315,
        "unique_terms": 796647,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): TREC-NEWS.",
        "filename": "lucene-inverted.beir-v1.0.0-trec-news.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-news.multifield.20221116.505594.tar.gz"
        ],
        "md5": "a7b5bd79d22d3631dffcad2ffa8afd0a",
        "size compressed (bytes)": 2633899391,
        "total_terms": 270886723,
        "documents": 578605,
        "unique_terms": 727856,
        "downloaded": False
    },
    "beir-v1.0.0-robust04.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Robust04.",
        "filename": "lucene-inverted.beir-v1.0.0-robust04.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-robust04.multifield.20221116.505594.tar.gz"
        ],
        "md5": "49db6bf123b6224d0e0973a16ff9c243",
        "size compressed (bytes)": 1728445191,
        "total_terms": 174384263,
        "documents": 528036,
        "unique_terms": 923466,
        "downloaded": False
    },
    "beir-v1.0.0-arguana.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): ArguAna.",
        "filename": "lucene-inverted.beir-v1.0.0-arguana.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-arguana.multifield.20221116.505594.tar.gz"
        ],
        "md5": "895b0d78a1cc40222aaebcff10b6b929",
        "size compressed (bytes)": 10523045,
        "total_terms": 944123,
        "documents": 8674,
        "unique_terms": 23867,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Webis-Touche2020.",
        "filename": "lucene-inverted.beir-v1.0.0-webis-touche2020.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-webis-touche2020.multifield.20221116.505594.tar.gz"
        ],
        "md5": "390552c8b93dc95bf2f58808d1c8a37d",
        "size compressed (bytes)": 750734533,
        "total_terms": 74066724,
        "documents": 382545,
        "unique_terms": 524665,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-android.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-android.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-android.multifield.20221116.505594.tar.gz"
        ],
        "md5": "299fc8b542dabc241320db571b8f8ff0",
        "size compressed (bytes)": 17886622,
        "total_terms": 1591285,
        "documents": 22998,
        "unique_terms": 40824,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-english.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-english.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-english.multifield.20221116.505594.tar.gz"
        ],
        "md5": "5bb26ad0ba9184592b5ed935e65b5f17",
        "size compressed (bytes)": 25562248,
        "total_terms": 2006983,
        "documents": 40221,
        "unique_terms": 61530,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gaming.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gaming.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gaming.multifield.20221116.505594.tar.gz"
        ],
        "md5": "90d1ae9a1862b8b96871b9b94cc46b4e",
        "size compressed (bytes)": 29996620,
        "total_terms": 2510477,
        "documents": 45300,
        "unique_terms": 59113,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-gis.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gis.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gis.multifield.20221116.505594.tar.gz"
        ],
        "md5": "62869b2b6cf569424fed659adf1e5ea7",
        "size compressed (bytes)": 44187762,
        "total_terms": 3789161,
        "documents": 37637,
        "unique_terms": 183298,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-mathematica.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.multifield.20221116.505594.tar.gz"
        ],
        "md5": "a78c9d2e29a4b727fbeb38e825629df5",
        "size compressed (bytes)": 21914072,
        "total_terms": 2234369,
        "documents": 16705,
        "unique_terms": 111306,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-physics.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-physics.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-physics.multifield.20221116.505594.tar.gz"
        ],
        "md5": "d6e60e2665c1b6f2bac021dc6c767393",
        "size compressed (bytes)": 38738718,
        "total_terms": 3542078,
        "documents": 38316,
        "unique_terms": 55229,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-programmers.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-programmers.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-programmers.multifield.20221116.505594.tar.gz"
        ],
        "md5": "77b54cd7613b555d80998b9744eef85c",
        "size compressed (bytes)": 40986350,
        "total_terms": 3682227,
        "documents": 32176,
        "unique_terms": 73765,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-stats.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-stats.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-stats.multifield.20221116.505594.tar.gz"
        ],
        "md5": "8469917c70c767ea398ec2b93aaf04ca",
        "size compressed (bytes)": 53094510,
        "total_terms": 5073873,
        "documents": 42269,
        "unique_terms": 182933,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-tex.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-tex.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-tex.multifield.20221116.505594.tar.gz"
        ],
        "md5": "4d0b0efb2579e0fd73b9156921580a00",
        "size compressed (bytes)": 93088212,
        "total_terms": 9155405,
        "documents": 68184,
        "unique_terms": 287393,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-unix.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-unix.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-unix.multifield.20221116.505594.tar.gz"
        ],
        "md5": "33e2510bb1414ca106766ae787e28670",
        "size compressed (bytes)": 54757808,
        "total_terms": 5449726,
        "documents": 47382,
        "unique_terms": 205471,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-webmasters.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.multifield.20221116.505594.tar.gz"
        ],
        "md5": "cb16d3da34b6705747ec07ce89913457",
        "size compressed (bytes)": 15528521,
        "total_terms": 1358292,
        "documents": 17405,
        "unique_terms": 40073,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): CQADupStack-wordpress.",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.multifield.20221116.505594.tar.gz"
        ],
        "md5": "f619c003e2d0cf84794cc672e18e0437",
        "size compressed (bytes)": 55737065,
        "total_terms": 5151575,
        "documents": 48605,
        "unique_terms": 125110,
        "downloaded": False
    },
    "beir-v1.0.0-quora.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Quora.",
        "filename": "lucene-inverted.beir-v1.0.0-quora.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-quora.multifield.20221116.505594.tar.gz"
        ],
        "md5": "9248de265c88afc105231659d8c8be09",
        "size compressed (bytes)": 52699891,
        "total_terms": 4390852,
        "documents": 522931,
        "unique_terms": 69597,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): DBPedia.",
        "filename": "lucene-inverted.beir-v1.0.0-dbpedia-entity.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-dbpedia-entity.multifield.20221116.505594.tar.gz"
        ],
        "md5": "b7f0ae30f045188a608cc87553cade37",
        "size compressed (bytes)": 2144410641,
        "total_terms": 152205479,
        "documents": 4635922,
        "unique_terms": 3338476,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SCIDOCS.",
        "filename": "lucene-inverted.beir-v1.0.0-scidocs.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scidocs.multifield.20221116.505594.tar.gz"
        ],
        "md5": "6409f5ec569530fc3240590dab59bc4c",
        "size compressed (bytes)": 175890028,
        "total_terms": 3065828,
        "documents": 25313,
        "unique_terms": 62562,
        "downloaded": False
    },
    "beir-v1.0.0-fever.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): FEVER.",
        "filename": "lucene-inverted.beir-v1.0.0-fever.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fever.multifield.20221116.505594.tar.gz"
        ],
        "md5": "841908da91e7e5eaa0d122faf1a486d8",
        "size compressed (bytes)": 3947210591,
        "total_terms": 310655699,
        "documents": 5396138,
        "unique_terms": 3275057,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): Climate-FEVER.",
        "filename": "lucene-inverted.beir-v1.0.0-climate-fever.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-climate-fever.multifield.20221116.505594.tar.gz"
        ],
        "md5": "2901ac443ca4f0df424a35d068905829",
        "size compressed (bytes)": 3947289128,
        "total_terms": 310661477,
        "documents": 5396163,
        "unique_terms": 3275068,
        "downloaded": False
    },
    "beir-v1.0.0-scifact.multifield": {
        "description": "Lucene multifield index of BEIR (v1.0.0): SciFact.",
        "filename": "lucene-inverted.beir-v1.0.0-scifact.multifield.20221116.505594.tar.gz",
        "readme": "lucene-inverted.beir-v1.0.0-multifield.20221116.505594.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scifact.multifield.20221116.505594.tar.gz"
        ],
        "md5": "b40b26f44f68ab9aa4b573aafea27e2e",
        "size compressed (bytes)": 9076714,
        "total_terms": 784591,
        "documents": 5183,
        "unique_terms": 28581,
        "downloaded": False
    }
}

TF_INDEX_INFO_MRTYDI = {
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
    }
}

TF_INDEX_INFO_MIRACL = {
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

TF_INDEX_INFO_CIRAL = {
    "ciral-v1.0-ha": {
        "description": "Lucene index for CIRAL v1.0 (Hausa).",
        "filename": "lucene-index.ciral-v1.0-ha.20230721.e850ea.tar.gz",
        "readme": "lucene-index.ciral-v1.0.20230721.e850ea.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-ha.20230721.e850ea.tar.gz"
        ],
        "md5": "9bef13f2b528d3a5712ce412c3c264f7",
        "size compressed (bytes)": 671653035,
        'total_terms': 93696543,
        'documents': 715355,
        'unique_terms': 817967,
        "downloaded": False
    },

    "ciral-v1.0-so": {
        "description": "Lucene index for CIRAL v1.0 (Somali).",
        "filename": "lucene-index.ciral-v1.0-so.20230721.e850ea.tar.gz",
        "readme": "lucene-index.ciral-v1.0.20230721.e850ea.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-so.20230721.e850ea.tar.gz"
        ],
        "md5": "4bb9d3ae1a6d65fbb2a4e7e57a71397d",
        "size compressed (bytes)": 916229181,
        "total_terms": 103736362,
        "documents": 827552,
        "unique_terms": 1636109,
        "downloaded": False
    },

    "ciral-v1.0-sw": {
        "description": "Lucene index for CIRAL v1.0 (Swahili).",
        "filename": "lucene-index.ciral-v1.0-sw.20230721.e850ea.tar.gz",
        "readme": "lucene-index.ciral-v1.0.20230721.e850ea.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-sw.20230721.e850ea.tar.gz"
        ],
        "md5": "1236a1a4c87268d98ec6534cd99aaada",
        "size compressed (bytes)": 896921754,
        "total_terms": 115140711,
        "documents": 949013,
        "unique_terms": 1655554,
        "downloaded": False
    },

    "ciral-v1.0-yo": {
        "description": "Lucene index for CIRAL v1.0 (Yoruba).",
        "filename": "lucene-index.ciral-v1.0-yo.20230721.e850ea.tar.gz",
        "readme": "lucene-index.ciral-v1.0.20230721.e850ea.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-yo.20230721.e850ea.tar.gz"
        ],
        "md5": "655e571314ed85cbfe637246c3d18110",
        "size compressed (bytes)": 94610259,
        "total_terms": 13693080,
        "documents": 82095,
        "unique_terms": 236638,
        "downloaded": False
    },

    "ciral-v1.0-ha-en": {
        "description": "Lucene index for CIRAL v1.0 English Translations (Hausa).",
        "filename": "lucene-index.ciral-v1.0-ha-en.20240212.2154e7.tar.gz",
        "readme": "lucene-index.ciral-v1.0-en.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-ha-en.20240212.2154e7.tar.gz"
        ],
        "md5": "40af043730fe0fb31c32551ae615bfb0",
        "size compressed (bytes)": 485237964,
        "total_terms": 55768945,
        "documents": 715355,
        "unique_terms": 222612,
        "downloaded": False
    },

    "ciral-v1.0-so-en": {
        "description": "Lucene index for CIRAL v1.0 English Translations (Somali).",
        "filename": "lucene-index.ciral-v1.0-so-en.20240212.2154e7.tar.gz",
        "readme": "lucene-index.ciral-v1.0-en.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-so-en.20240212.2154e7.tar.gz"
        ],
        "md5": "ceff839268ebb1f41ac5398d613cbf32",
        "size compressed (bytes)": 611464833,
        "total_terms": 63835022,
        "documents": 827552,
        "unique_terms": 214501,
        "downloaded": False
    },

    "ciral-v1.0-sw-en": {
        "description": "Lucene index for CIRAL v1.0 English Translations (Swahili).",
        "filename": "lucene-index.ciral-v1.0-sw-en.20240212.2154e7.tar.gz",
        "readme": "lucene-index.ciral-v1.0-en.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-sw-en.20240212.2154e7.tar.gz"
        ],
        "md5": "60a57a128cda8c4a1460f1e3a0df002a",
        "size compressed (bytes)": 683277315,
        "total_terms": 83817100,
        "documents": 949013,
        "unique_terms": 265867,
        "downloaded": False
    },

    "ciral-v1.0-yo-en": {
        "description": "Lucene index for CIRAL v1.0 English Translations (Yoruba).",
        "filename": "lucene-index.ciral-v1.0-yo-en.20240212.2154e7.tar.gz",
        "readme": "lucene-index.ciral-v1.0-en.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.ciral-v1.0-yo-en.20240212.2154e7.tar.gz"
        ],
        "md5": "84f29864973de98f2d93fe03a2908703",
        "size compressed (bytes)": 60936367,
        "total_terms": 7245155,
        "documents": 82095,
        "unique_terms": 68394,
        "downloaded": False
    }

}

TF_INDEX_INFO_OTHER = {
    "cacm": {
        "description": "Lucene index of the CACM corpus.",
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
        "description": "Lucene index of TREC Disks 4 & 5 (minus Congressional Records), used in the TREC 2004 Robust Track.",
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

    "wikipedia-dpr-100w": {
        "description": "Lucene index of Wikipedia with DPR 100-word splits",
        "filename": "lucene-index.wikipedia-dpr-100w.20210120.d1b9e6.tar.gz",
        "readme": "index-wikipedia-dpr-20210120-d1b9e6-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.wikipedia-dpr-100w.20210120.d1b9e6.tar.gz"
        ],
        "md5": "7b58c08da992b2ea7e96667f0b176651",
        "size compressed (bytes)": 9177917732,
        "total_terms": 1512973270,
        "documents": 21015324,
        "unique_terms": 5345463,
        "downloaded": False
    },
    "wikipedia-dpr-100w-slim": {
        "description": "Lucene index of Wikipedia with DPR 100-word splits (slim version, document text not stored)",
        "filename": "lucene-index.wikipedia-dpr-100w-slim.20210120.d1b9e6.tar.gz",
        "readme": "index-wikipedia-dpr-slim-20210120-d1b9e6-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.wikipedia-dpr-100w-slim.20210120.d1b9e6.tar.gz"
        ],
        "md5": "5d24352f0de6ae75b60e11a9cf622251",
        "size compressed (bytes)": 1810337190,
        "total_terms": 1512973270,
        "documents": 21015324,
        "unique_terms": 5345463,
        "downloaded": False
    },
    "wikipedia-kilt-doc": {
        "description": "Lucene index of Wikipedia snapshot used as KILT's knowledge source.",
        "filename": "lucene-index.wikipedia-kilt-doc.20210421.f29307.tar.gz",
        "readme": "index-wikipedia-kilt-doc-20210421-f29307-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.wikipedia-kilt-doc.20210421.f29307.tar.gz"
        ],
        "md5": "d4a1e7628f6f68c51dd2d764e62b7f8d",
        "size compressed (bytes)": 10901145611,
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

    "hc4-v1.0-fa": {
        "description": "Lucene index for HC4 v1.0 (Persian).",
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
        "description": "Lucene index for HC4 v1.0 (Russian).",
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
        "description": "Lucene index for HC4 v1.0 (Chinese).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (Persian).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (Russian).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (Chinese).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Persian).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Russian).",
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
        "description": "Lucene index for NeuCLIR 2022 corpus (official English translation from Chinese).",
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
    "atomic_text_v0.2.1_small_validation": {
        "description": "Lucene index for AToMiC Text v0.2.1 small setting on validation set",
        "filename": "lucene-index.atomic.image.flat.small.validation.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.text.flat.small.validation.tar.gz"
        ],
        "md5": "fe0ae1286dde8a4969f16134c47682ae",
        "size compressed (bytes)": 32902223,
        "total_terms": 2999824,
        "documents": 17173,
        "unique_terms": 118071,
        "downloaded": False
    },
    "atomic_text_v0.2.1_base": {
        "description": "Lucene index for AToMiC Text v0.2.1 base setting on validation set",
        "filename": "lucene-index.atomic.image.flat.base.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.text.flat.base.tar.gz"
        ],
        "md5": "fe2f0beb617f5ade4ffce6d05adfbc7a",
        "size compressed (bytes)": 5532187295,
        "total_terms": 520954965,
        "documents": 3029504,
        "unique_terms": -1,
        "downloaded": False
    },
    "atomic_text_v0.2.1_large": {
        "description": "Lucene index for AToMiC Text v0.2.1 large setting on validation set",
        "filename": "lucene-index.atomic.image.flat.large.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.text.flat.large.tar.gz"
        ],
        "md5": "0f4639ba8b6ecff1d26da02790f78add",
        "size compressed (bytes)": 18194155242,
        "total_terms": 1727597393,
        "documents": 10134744,
        "unique_terms": -1,
        "downloaded": False
    },
    "atomic_image_v0.2_small_validation": {
        "description": "Lucene index for AToMiC Images v0.2 small setting on validation set",
        "filename": "lucene-index.atomic.image.flat.small.validation.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.image.flat.small.validation.tar.gz"
        ],
        "md5": "7afd990df79462040f175b990545ad40",
        "size compressed (bytes)": 5454742,
        "total_terms": 308646,
        "documents": 16126,
        "unique_terms": 48666,
        "downloaded": False
    },
    "atomic_image_v0.2_base": {
        "description": "Lucene index for AToMiC Images v0.2 base setting on validation set",
        "filename": "lucene-index.atomic.image.flat.base.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.image.flat.base.tar.gz"
        ],
        "md5": "d8a4e8ce05305406004cceff60147592",
        "size compressed (bytes)": 1309435624,
        "total_terms": 100743397,
        "documents": 3410779,
        "unique_terms": -1,
        "downloaded": False
    },
    "atomic_image_v0.2_large": {
        "description": "Lucene index for AToMiC Images v0.2 large setting on validation set",
        "filename": "lucene-index.atomic.image.flat.large.tar.gz",
        "readme": "lucene-index.atomic.20231018.ae6ff6.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/lucene-index.atomic.image.flat.large.tar.gz"
        ],
        "md5": "3e4a0c976a2c50daeee7a276b9b2c379",
        "size compressed (bytes)": 1448435404,
        "total_terms": 108550562,
        "documents": 3803656,
        "unique_terms": -1,
        "downloaded": False
    },
}

TF_INDEX_INFO_OTHER_ALIASES = {
    # To preserve working commands in published papers: integrations/papers/test_sigir2021.py
    "wikipedia-dpr": TF_INDEX_INFO_OTHER["wikipedia-dpr-100w"],
}

TF_INDEX_INFO = {**TF_INDEX_INFO_MSMARCO,
                 **TF_INDEX_INFO_MSMARCO_ALIASES,
                 **TF_INDEX_INFO_BEIR,
                 **TF_INDEX_INFO_MRTYDI,
                 **TF_INDEX_INFO_MIRACL,
                 **TF_INDEX_INFO_CIRAL,
                 **TF_INDEX_INFO_OTHER,
                 **TF_INDEX_INFO_OTHER_ALIASES}

IMPACT_INDEX_INFO_MSMARCO = {
    "msmarco-v1-passage.slimr": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with BM25 negatives.",
        "filename": "lucene-inverted.msmarco-v1-passage.slimr.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.slimr.20230925.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.slimr.tar.gz",
        ],
        "md5": "2871da5fec6991b65032c7a159cfc9ec",
        "size compressed (bytes)": 1902711709,
        "total_terms": 100694232684,
        "documents": 8841823,
        "unique_terms": 28121,
        "downloaded": False
    },
    "msmarco-v1-passage.slimr-pp": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus enoded by SLIM trained with cross-encoder distillation and hard-negative mining.",
        "filename": "lucene-inverted.msmarco-v1-passage.slimr-pp.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.slimr-pp.20230925.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.slimr-pp.tar.gz",
        ],
        "md5": "af85ff00a264e5288bac9e745cc4bb62",
        "size compressed (bytes)": 2135050221,
        "total_terms": 104421954301,
        "documents": 8841823,
        "unique_terms": 27766,
        "downloaded": False
    },
    "msmarco-v1-passage.unicoil": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL.",
        "filename": "lucene-inverted.msmarco-v1-passage.unicoil.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.unicoil.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.unicoil.20221005.252b5e.tar.gz",
        ],
        "md5": "f926bd3e17d210ff041f880d27bdcd6f",
        "size compressed (bytes)": 1161033793,
        "total_terms": 44495093768,
        "documents": 8841823,
        "unique_terms": 27678,
        "downloaded": False
    },
    "msmarco-v1-passage.unicoil-noexp": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL (noexp).",
        "filename": "lucene-inverted.msmarco-v1-passage.unicoil-noexp.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.unicoil-noexp.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.unicoil-noexp.20221005.252b5e.tar.gz",
        ],
        "md5": "8a2527e582c343374b8270b1db8d1a06",
        "size compressed (bytes)": 873513687,
        "total_terms": 26468530021,
        "documents": 8841823,
        "unique_terms": 27647,
        "downloaded": False
    },
    "msmarco-v1-passage.unicoil-tilde": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus encoded by uniCOIL-TILDE.",
        "filename": "lucene-inverted.msmarco-v1-passage.unicoil-tilde.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.unicoil-tilde.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.unicoil-tilde.20221005.252b5e.tar.gz",
        ],
        "md5": "2d192adb9e0bfc6024d399dca9f36b50",
        "size compressed (bytes)": 1871923442,
        "total_terms": 73040108576,
        "documents": 8841823,
        "unique_terms": 27646,
        "downloaded": False
    },
    "msmarco-v1-passage.deepimpact": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus encoded by DeepImpact.",
        "filename": "lucene-inverted.msmarco-v1-passage.deepimpact.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.deepimpact.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.deepimpact.20221005.252b5e.tar.gz",
        ],
        "md5": "b4f1d0886cdfca43230dfb6d4866ff14",
        "size compressed (bytes)": 1242661399,
        "total_terms": 35455908214,
        "documents": 8841823,
        "unique_terms": 3514102,
        "downloaded": False
    },
    "msmarco-v1-passage.distill-splade-max": {
        "description": "Lucene impact index of the MS MARCO V1 passage corpus encoded by distill-splade-max.",
        "filename": "lucene-inverted.msmarco-v1-passage.distill-splade-max.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.distill-splade-max.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.distill-splade-max.20221005.252b5e.tar.gz",
        ],
        "md5": "145e283e9f44235ae132f86fca07f083",
        "size compressed (bytes)": 3822890791,
        "total_terms": 95445422483,
        "documents": 8841823,
        "unique_terms": 28131,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-ed": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-ed.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-ed.20230524.a59610.tar.gz",
        ],
        "md5": "2c008fc36131e27966a72292932358e6",
        "size compressed (bytes)": 2102230097,
        "total_terms": 52376261130,
        "documents": 8841823,
        "unique_terms": 28679,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-ed-docvectors": {
        "description": "Lucene impact index (with docvectors) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-ed-docvectors.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-ed-docvectors.20230524.a59610.tar.gz",
        ],
        "md5": "98d6bb5eaf7b0c704d200843115ef827",
        "size compressed (bytes)": 13052698276,
        "total_terms": 52376261130,
        "documents": 8841823,
        "unique_terms": 28679,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-ed-text": {
        "description": "Lucene impact index (with text) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-EnsembleDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-ed-text.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-ed-text.20230524.a59610.tar.gz",
        ],
        "md5": "738f7a79c69075044da92127889fd191",
        "size compressed (bytes)": 9983469326,
        "total_terms": 52376261130,
        "documents": 8841823,
        "unique_terms": 28679,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-sd": {
        "description": "Lucene impact index of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-sd.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-sd.20230524.a59610.tar.gz",
        ],
        "md5": "b92bbe960186d2b7c752856b07b0e889",
        "size compressed (bytes)": 2367260823,
        "total_terms": 55456660129,
        "documents": 8841823,
        "unique_terms": 28662,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-sd-docvectors": {
        "description": "Lucene impact index (with docvectors) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-sd-docvectors.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-sd-docvectors.20230524.a59610.tar.gz",
        ],
        "md5": "32eab153ab5c67faf9c0411a421e2ac5",
        "size compressed (bytes)": 14829233252,
        "total_terms": 55456660129,
        "documents": 8841823,
        "unique_terms": 28662,
        "downloaded": False
    },
    "msmarco-v1-passage.splade-pp-sd-text": {
        "description": "Lucene impact index (with text) of the MS MARCO passage corpus encoded by SPLADE++ CoCondenser-SelfDistil.",
        "filename": "lucene-inverted.msmarco-v1-passage.splade-pp-sd-text.20230524.a59610.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-passage.splade-pp.20230524.a59610.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-passage.splade-pp-sd-text.20230524.a59610.tar.gz",
        ],
        "md5": "5483ec81dc4f4057468a3df21c22f236",
        "size compressed (bytes)": 11473064932,
        "total_terms": 55456660129,
        "documents": 8841823,
        "unique_terms": 28662,
        "downloaded": False
    },

    "msmarco-v1-doc-segmented.unicoil": {
        "description": "Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL, with title/segment encoding.",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented.unicoil.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.unicoil.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented.unicoil.20221005.252b5e.tar.gz",
        ],
        "md5": "7dc32ad22876fbbe0f24f21fd1ea50c0",
        "size compressed (bytes)": 5765257801,
        "total_terms": 214505277898,
        "documents": 20545677,
        "unique_terms": 29142,
        "downloaded": False
    },
    "msmarco-v1-doc-segmented.unicoil-noexp": {
        "description": "Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp), with title/segment encoding.",
        "filename": "lucene-inverted.msmarco-v1-doc-segmented.unicoil-noexp.20221005.252b5e.tar.gz",
        "readme": "lucene-inverted.msmarco-v1-doc-segmented.unicoil-noexp.20221005.252b5e.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.msmarco-v1-doc-segmented.unicoil-noexp.20221005.252b5e.tar.gz",
        ],
        "md5": "f92d5a2ba22274993b34f69e59427379",
        "size compressed (bytes)": 5323380902,
        "total_terms": 152323732876,
        "documents": 20545677,
        "unique_terms": 29142,
        "downloaded": False
    },

    "msmarco-v2-passage-unicoil-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL.",
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
        "description": "Lucene impact index of the MS MARCO V2 passage corpus for uniCOIL (noexp).",
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
    "msmarco-v2-passage-slimr-pp-norefine-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 passage corpus encoded by SLIM (norefine) trained with cross-encoder distillation and hard-negative mining.",
        "filename": "lucene-index.msmarco-v2-passage-slimr-pp.20230614.tar.gz",
        "readme": "lucene-index.msmarco-v2-passage-slimr-pp.20230614.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene-index.msmarco-v2-passage-slimr-pp.20230614.tar.gz",
        ],
        "md5": "0251a882369dd9c27f6a629198123a40",
        "size compressed (bytes)": 35297323293,
        "total_terms": 1668035574958,
        "documents": 138364197,
        "unique_terms": -1,
        "downloaded": False
    },
    "msmarco-v2-doc-segmented-unicoil-0shot": {
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL, with title prepended.",
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
        "description": "Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended.",
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
    }
}

IMPACT_INDEX_INFO_MSMARCO_ALIASES = {
    # To preserve working commands in published papers: integrations/papers/test_sigir2022.py testcase test_Trotman_etal
    "msmarco-passage-unicoil-d2q": IMPACT_INDEX_INFO_MSMARCO["msmarco-v1-passage.unicoil"]
}

IMPACT_INDEX_INFO_BEIR = {
    # SPLADE++ (CoCondenser-EnsembleDistil)
    "beir-v1.0.0-trec-covid.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-COVID, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-trec-covid.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-covid.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "e808ff9d4a1f45de9f0bc292900302b4",
        "size compressed (bytes)": 52144690,
        "total_terms": 1206882333,
        "documents": 171332,
        "unique_terms": 26030,
        "downloaded": False
    },
    "beir-v1.0.0-bioasq.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): BioASQ, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-bioasq.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-bioasq.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "fc661b2c2fa59e24f37c6dfa6de8e682",
        "size compressed (bytes)": 4866347210,
        "total_terms": 127381306317,
        "documents": 14914603,
        "unique_terms": 27606,
        "downloaded": False
    },
    "beir-v1.0.0-nfcorpus.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): NFCorpus, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-nfcorpus.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nfcorpus.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "7d6e66cca9d2db8bb7caa3bdf330cdd8",
        "size compressed (bytes)": 1352017,
        "total_terms": 30711150,
        "documents": 3633,
        "unique_terms": 15307,
        "downloaded": False
    },
    "beir-v1.0.0-nq.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): NQ, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-nq.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-nq.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "a785d6636df60c861829507c3d806ee6",
        "size compressed (bytes)": 737526054,
        "total_terms": 15061905296,
        "documents": 2681468,
        "unique_terms": 28714,
        "downloaded": False
    },
    "beir-v1.0.0-hotpotqa.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): HotpotQA, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-hotpotqa.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-hotpotqa.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "b280ed3f7b12034c0cc4b302f92801b9",
        "size compressed (bytes)": 1168143910,
        "total_terms": 23736328387,
        "documents": 5233329,
        "unique_terms": 28654,
        "downloaded": False
    },
    "beir-v1.0.0-fiqa.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): FiQA-2018, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-fiqa.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fiqa.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "ea53103c695c0da6cea5b1c8353371b0",
        "size compressed (bytes)": 16919422,
        "total_terms": 342348959,
        "documents": 57638,
        "unique_terms": 25136,
        "downloaded": False
    },
    "beir-v1.0.0-signal1m.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): Signal-1M, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-signal1m.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-signal1m.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "0b46d71c97eabe9ca424f3ab9b2ddc64",
        "size compressed (bytes)": 496739597,
        "total_terms": 8237410263,
        "documents": 2866316,
        "unique_terms": 28020,
        "downloaded": False
    },
    "beir-v1.0.0-trec-news.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): TREC-NEWS, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-trec-news.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-trec-news.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "ef4fb032b632b80355db46549f08a026",
        "size compressed (bytes)": 250744439,
        "total_terms": 5190619991,
        "documents": 594977,
        "unique_terms": 27774,
        "downloaded": False
    },
    "beir-v1.0.0-robust04.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): Robust04, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-robust04.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-robust04.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "c1a6fd094bb9e34e69e10040d9b0ad2a",
        "size compressed (bytes)": 193499509,
        "total_terms": 4818025575,
        "documents": 528155,
        "unique_terms": 27545,
        "downloaded": False
    },
    "beir-v1.0.0-arguana.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): ArguAna, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-arguana.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-arguana.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "c2725b375ca53ff031ee8b4ba8501eb6",
        "size compressed (bytes)": 3559009,
        "total_terms": 71992355,
        "documents": 8674,
        "unique_terms": 21501,
        "downloaded": False
    },
    "beir-v1.0.0-webis-touche2020.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): Webis-Touche2020, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-webis-touche2020.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-webis-touche2020.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "1abec77feeb741edfb3c9b7565b42964",
        "size compressed (bytes)": 119213878,
        "total_terms": 2275005818,
        "documents": 382545,
        "unique_terms": 27611,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-android.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-android, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-android.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-android.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "0b6b36417df9095e9ed32e4127bdd2fd",
        "size compressed (bytes)": 4789380,
        "total_terms": 108476959,
        "documents": 22998,
        "unique_terms": 16844,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-english.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-english, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-english.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-english.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "f2a5f68523117638f957bcc353c956c1",
        "size compressed (bytes)": 8868099,
        "total_terms": 158861979,
        "documents": 40221,
        "unique_terms": 25618,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gaming.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gaming, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gaming.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gaming.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "804851ed2ca5c38464f28263fb664615",
        "size compressed (bytes)": 10471910,
        "total_terms": 197713644,
        "documents": 45301,
        "unique_terms": 22854,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-gis.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-gis, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-gis.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-gis.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "ee53ba7f26e678f39c3db8997785169a",
        "size compressed (bytes)": 8652361,
        "total_terms": 214744014,
        "documents": 37637,
        "unique_terms": 20225,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-mathematica.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-mathematica, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-mathematica.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "c3dd33ddfd364a0665450691963f9036",
        "size compressed (bytes)": 3845630,
        "total_terms": 90452420,
        "documents": 16705,
        "unique_terms": 17697,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-physics.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-physics, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-physics.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-physics.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "155a130b556072ec0b84788417361228",
        "size compressed (bytes)": 9342353,
        "total_terms": 199892911,
        "documents": 38316,
        "unique_terms": 21505,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-programmers.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-programmers, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-programmers.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-programmers.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "f0923dd88b7d4f050d54ff6f6efcc7f5",
        "size compressed (bytes)": 8566346,
        "total_terms": 182133939,
        "documents": 32176,
        "unique_terms": 20985,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-stats.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-stats, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-stats.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-stats.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "78e62040ed6d44e232e9381e96a56cc7",
        "size compressed (bytes)": 10153907,
        "total_terms": 236361350,
        "documents": 42269,
        "unique_terms": 21654,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-tex.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-tex, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-tex.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-tex.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "402088c62cbffeba3d710fec408226ed",
        "size compressed (bytes)": 16238354,
        "total_terms": 433864313,
        "documents": 68184,
        "unique_terms": 23064,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-unix.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-unix, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-unix.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-unix.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "66e884e446ff183e07973c65ccf32625",
        "size compressed (bytes)": 10586092,
        "total_terms": 260688145,
        "documents": 47382,
        "unique_terms": 19773,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-webmasters.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-webmasters, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-webmasters.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "17be129cbe65b4e4e64a181f95a56972",
        "size compressed (bytes)": 4077803,
        "total_terms": 89755810,
        "documents": 17405,
        "unique_terms": 18246,
        "downloaded": False
    },
    "beir-v1.0.0-cqadupstack-wordpress.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): CQADupStack-wordpress, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-cqadupstack-wordpress.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "f20bacfe92f21bc75360a9978278e690",
        "size compressed (bytes)": 9973318,
        "total_terms": 257594340,
        "documents": 48605,
        "unique_terms": 19864,
        "downloaded": False
    },
    "beir-v1.0.0-quora.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): Quora, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-quora.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-quora.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "ce6dbaacf3b7b0e8282020565d324ea5",
        "size compressed (bytes)": 62673280,
        "total_terms": 1064938611,
        "documents": 522931,
        "unique_terms": 26583,
        "downloaded": False
    },
    "beir-v1.0.0-dbpedia-entity.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): DBPedia, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-dbpedia-entity.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-dbpedia-entity.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "fc9ac8329b6e2c054290791e68e0a0e4",
        "size compressed (bytes)": 1224474004,
        "total_terms": 22302972729,
        "documents": 4635922,
        "unique_terms": 28628,
        "downloaded": False
    },
    "beir-v1.0.0-scidocs.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): SCIDOCS, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-scidocs.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scidocs.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "3285b17da7cd88d2e6e62a3bfc465039",
        "size compressed (bytes)": 10386053,
        "total_terms": 192911913,
        "documents": 25657,
        "unique_terms": 23225,
        "downloaded": False
    },
    "beir-v1.0.0-fever.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): FEVER, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-fever.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-fever.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "22e67800879422840f20c7d0008795a9",
        "size compressed (bytes)": 1499855743,
        "total_terms": 28498465299,
        "documents": 5416593,
        "unique_terms": 28578,
        "downloaded": False
    },
    "beir-v1.0.0-climate-fever.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): Climate-FEVER, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-climate-fever.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-climate-fever.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "bd5f3c804874ca18f99590037873a1bc",
        "size compressed (bytes)": 1500344997,
        "total_terms": 28498465299,
        "documents": 5416593,
        "unique_terms": 28578,
        "downloaded": False
    },
    "beir-v1.0.0-scifact.splade-pp-ed": {
        "description": "Lucene impact index of BEIR (v1.0.0): SciFact, encoded by SPLADE++ (CoCondenser-EnsembleDistil).",
        "filename": "lucene-inverted.beir-v1.0.0-scifact.splade-pp-ed.20231124.a66f86f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-scifact.splade-pp-ed.20231124.a66f86f.tar.gz"
        ],
        "md5": "3abe52209fcd04f411da438a37254e3a",
        "size compressed (bytes)": 1985785,
        "total_terms": 47317323,
        "documents": 5183,
        "unique_terms": 16385,
        "downloaded": False
    }
}

IMPACT_INDEX_INFO = {**IMPACT_INDEX_INFO_MSMARCO,
                     **IMPACT_INDEX_INFO_MSMARCO_ALIASES,
                     **IMPACT_INDEX_INFO_BEIR}

FAISS_INDEX_INFO_MSMARCO = {
    "msmarco-v1-passage.cosdpr-distil": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by cosDPR-distil.",
        "filename": "faiss-flat.msmarco-v1-passage.cosdpr-distil.20221023.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.cosdpr-distil.20221023.tar.gz"
        ],
        "md5": "83565019175c79fcc5f8d99fb1bd43ca",
        "size compressed (bytes)": 23843194320,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.aggretriever-cocondenser": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-cocondenser.",
        "filename": "faiss-flat.msmarco-v1-passage.aggretriever-cocondenser.20230407.f627ef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.aggretriever-cocondenser.20230407.f627ef.tar.gz"
        ],
        "md5": "c55472025808eeca736c7123f0033726",
        "size compressed (bytes)": 26053474818,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.aggretriever-distilbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-distilbert.",
        "filename": "faiss-flat.msmarco-v1-passage.aggretriever-distilbert.20230407.f627ef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.aggretriever-distilbert.20230407.f627ef.tar.gz"
        ],
        "md5": "d8fd51bfe974752cf770856623e39668",
        "size compressed (bytes)": 25963140631,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },

    "msmarco-v1-passage.ance": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the ANCE MS MARCO passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.ance.20210224.060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.ance.20210224.060cef.tar.gz"
        ],
        "md5": "e6cf0c1011200af81fd53aa7c5ce9414",
        "size compressed (bytes)": 25102344926,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.distilbert-dot-margin-mse-t2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the distilbert-dot-margin_mse-T2-msmarco encoder",
        "filename": "faiss-flat.msmarco-v1-passage.distilbert-dot-margin_mse-t2.20210316.d44c3a.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.distilbert-dot-margin_mse-t2.20210316.d44c3a.tar.gz"
        ],
        "md5": "bb8a3c3cf48fcd8c2e66f974fb449336",
        "size compressed (bytes)": 25162771335,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.distilbert-dot-tas_b-b256": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by distilbert-dot-tas_b-b256-msmarco encoder",
        "filename": "faiss-flat.msmarco-v1-passage.distilbert-dot-tas_b-b256.20210527.63276f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.distilbert-dot-tas_b-b256.20210527.63276f.tar.gz"
        ],
        "md5": "538546d5818527a51d87ce482e7a197e",
        "size compressed (bytes)": 25162329450,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.sbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the SBERT MS MARCO passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.sbert.20210313.a0fbb3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.sbert.20210313.a0fbb3.tar.gz"
        ],
        "md5": "b1649ea89b48cc89b3027399d09873dd",
        "size compressed (bytes)": 25214193348,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.bge-base-en-v1.5": {
        "description": "Faiss index of the MS MARCO passage corpus encoded by BGE-base-en-v1.5 encoder",
        "filename": "faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b21fb6abee3be6da3b6f39c9f6d9f280",
        "size compressed (bytes)": 25217210007,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "6c544e9dcd87b3b6acac0f8a69d741dd",
        "size compressed (bytes)": 25204502424,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert.hnsw": {
        "description": "Faiss HNSW index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "faiss-hnsw.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-hnsw.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "6b7285a7f0163d1a547214396be20488",
        "size compressed (bytes)": 33359120779,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2.20210608.5f341b.tar.gz"
        ],
        "md5": "768b897ec4ac62f5cea05ece12e5b284",
        "size compressed (bytes)": 25211079424,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2-hn": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hn passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2-hn.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2-hn.20210608.5f341b.tar.gz"
        ],
        "md5": "583210e5e8c8cddd4f34dbdf75bb4c21",
        "size compressed (bytes)": 25205730186,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2-hnp": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hnp passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2-hnp.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2-hnp.20210608.5f341b.tar.gz"
        ],
        "md5": "d22d0b6b32f156088a10b0d54ecc1da2",
        "size compressed (bytes)": 25225526400,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.openai-ada2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by OpenAI ada2",
        "filename": "faiss-flat.msmarco-v1-passage.openai-ada2.20230530.e3a58f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.openai-ada2.20230530.e3a58f.tar.gz"
        ],
        "md5": "5bad28d6ab7e28b834c3b3dd7be0fbc7",
        "size compressed (bytes)": 45649935995,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.cohere-embed-english-v3.0": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by Cohere Embed English v3.0",
        "filename": "faiss-flat.msmarco-v1-passage.cohere-embed-english-v3.0.20240216.2154e79.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.cohere-embed-english-v3.0.20240216.2154e79.tar.gz"
        ],
        "md5": "be2b8975161e1327fc852e01287dff48",
        "size compressed (bytes)": 21341576860,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.openai-text-embedding-3-large": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by OpenAI text-embedding-3-large",
        "filename": "faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.tar.gz",
        "readme": "faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.tar.gz"
        ],
        "md5": "e52f046b1decc9bf3a55ac0ff70780d0",
        "size compressed (bytes)": 87658796879,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },

    "msmarco-v1-doc.ance-maxp": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by the ANCE MaxP encoder",
        "filename": "faiss-flat.msmarco-v1-doc.ance_maxp.20210304.b2a1b0.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc.ance_maxp.20210304.b2a1b0.tar.gz"
        ],
        "md5": "f956d8c718c77717fa9611c471e336da",
        "size compressed (bytes)": 58312804630,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc"
    },
    "msmarco-v1-doc.tct_colbert": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT",
        "filename": "faiss-flat.msmarco-v1-doc.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "be7ff45b369803c10cc90fbab8642e60",
        "size compressed (bytes)": 58514326319,
        "documents": 20544550,
        "downloaded": False,
        "texts": "smarco-v1-doc"
    },
    "msmarco-v1-doc-segmented.tct_colbert-v2-hnp": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT-V2-HNP",
        "filename": "faiss-flat.msmarco-v1-doc-segmented.tct_colbert-v2-hnp.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc-segmented.tct_colbert-v2-hnp.tar.gz"
        ],
        "md5": "51b1309a0afac090aafbf96f84002ec0",
        "size compressed (bytes)": 58586765630,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc-segmented"
    }
}

FAISS_INDEX_INFO_BEIR = {
    # BEIR (v1.0.0) contriever indexes
    "beir-v1.0.0-trec-covid.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz"
        ],
        "md5": "3f178cadc4a2d31bb1087e344f99ab4c",
        "size compressed (bytes)": 488100337,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.contriever.20230124.tar.gz"
        ],
        "md5": "a29261de8d5d3e473f66ed255b65ba96",
        "size compressed (bytes)": 42417202575,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz"
        ],
        "md5": "30008d78302ee205f704bae116523efa",
        "size compressed (bytes)": 10322413,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-nq.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.contriever.20230124.tar.gz"
        ],
        "md5": "0bcfc534e6ef614e0f1b9ab6da57e481",
        "size compressed (bytes)": 7617697773,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz"
        ],
        "md5": "b0813bc6c07b972419385e5f7f9aefe4",
        "size compressed (bytes)": 14874722012,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.contriever.20230124.tar.gz"
        ],
        "md5": "dd7812b413b2bb6d1168937402b2ac6c",
        "size compressed (bytes)": 164024743,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.contriever.20230124.tar.gz"
        ],
        "md5": "cb7e12e441584094a996139f16831b71",
        "size compressed (bytes)": 8142534260,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.contriever.20230124.tar.gz"
        ],
        "md5": "d3c5d0b7c3611805bec59b382f373857",
        "size compressed (bytes)": 1629958666,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.contriever.20230124.tar.gz"
        ],
        "md5": "cbc30e163097ec1269e2b355d40ef373",
        "size compressed (bytes)": 1501110513,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.contriever.20230124.tar.gz"
        ],
        "md5": "d75510f440ba12c645de1a1aa1d2cbc9",
        "size compressed (bytes)": 24710574,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz"
        ],
        "md5": "d26a488863f44023580deefc309f4d13",
        "size compressed (bytes)": 1091320687,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz"
        ],
        "md5": "e360f313228e914808bc90721bd39784",
        "size compressed (bytes)": 65447253,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz"
        ],
        "md5": "edb867d9bc0744fefc3024ecd38f83ee",
        "size compressed (bytes)": 114460503,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz"
        ],
        "md5": "8778ea1b56d506449eea05a510935500",
        "size compressed (bytes)": 128906101,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz"
        ],
        "md5": "0b6224dc15c8c5211f8d16189e3c7fac",
        "size compressed (bytes)": 107128998,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz"
        ],
        "md5": "7db3aa811104f7b34464cadcd3084176",
        "size compressed (bytes)": 47544599,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz"
        ],
        "md5": "26126f4e8896d054cec11d8f4b840c1a",
        "size compressed (bytes)": 109048292,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz"
        ],
        "md5": "bb5fec14f14caf08d7338b7d1ff86d6b",
        "size compressed (bytes)": 91583163,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz"
        ],
        "md5": "249b0a88775ab130e30efd3b6e07ebb8",
        "size compressed (bytes)": 120288678,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz"
        ],
        "md5": "47d87a4dba07dc2cd651582b0388ccf1",
        "size compressed (bytes)": 194080722,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz"
        ],
        "md5": "e8e09adcd207653792b5f5c430f355db",
        "size compressed (bytes)": 134860136,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz"
        ],
        "md5": "9c0d468e18b137d8c7123c7ece5deafd",
        "size compressed (bytes)": 49531606,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz"
        ],
        "md5": "c4100815492270db1519f644260a3b5a",
        "size compressed (bytes)": 138348174,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-quora.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.contriever.20230124.tar.gz"
        ],
        "md5": "65cebdab871e2065fdacf0977f32a2bd",
        "size compressed (bytes)": 1485866155,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz"
        ],
        "md5": "6098fd3dc9b2cae202d56f20b961291f",
        "size compressed (bytes)": 13214316276,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.contriever.20230124.tar.gz"
        ],
        "md5": "c565903e4eacf637173df096c6306e45",
        "size compressed (bytes)": 73532582,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-fever.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.contriever.20230124.tar.gz"
        ],
        "md5": "01808e4f7ddcd31b391091c441de4bac",
        "size compressed (bytes)": 15437918697,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz"
        ],
        "md5": "b6ed4fe268281cd6cde8a2e0be361485",
        "size compressed (bytes)": 15437988872,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.contriever.20230124.tar.gz"
        ],
        "md5": "b0fe70f77488b3f296ccc98ffce65b49",
        "size compressed (bytes)": 14753571,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },

    # BEIR (v1.0.0) contriever ft MSMARCO indexes
    "beir-v1.0.0-trec-covid.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "607174fdc964760a1d491af294fb1b91",
        "size compressed (bytes)": 487986914,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat",
    },
    "beir-v1.0.0-bioasq.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "280c03564ea10a2bf1dcc01f9107b11c",
        "size compressed (bytes)": 42438279824,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat",
    },
    "beir-v1.0.0-nfcorpus.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "bfbec2a543a719e4085b2f67911ce965",
        "size compressed (bytes)": 10327251,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat",
    },
    "beir-v1.0.0-nq.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "5eb685f5c2de1978de5b43604560fb01",
        "size compressed (bytes)": 7619790062,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat",
    },
    "beir-v1.0.0-hotpotqa.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "38c37708f9927501ca2f7563aa43f407",
        "size compressed (bytes)": 14889518959,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat",
    },
    "beir-v1.0.0-fiqa.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "540216665f5611df5ef968c66a068150",
        "size compressed (bytes)": 163998686,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat",
    },
    "beir-v1.0.0-signal1m.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a71e5a2ada31a540817acdc1a2f7b2de",
        "size compressed (bytes)": 8146484810,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat",
    },
    "beir-v1.0.0-trec-news.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "fe560c02030bf212e4a4f3c1f205560d",
        "size compressed (bytes)": 1629437390,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat",
    },
    "beir-v1.0.0-robust04.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "de5531902df243521e006fbaa82ca1f9",
        "size compressed (bytes)": 1501089090,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat",
    },
    "beir-v1.0.0-arguana.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "2e32725a55a0db47953f481de393f1e4",
        "size compressed (bytes)": 24705839,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat",
    },
    "beir-v1.0.0-webis-touche2020.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c33ec5918c1afc435c5fa5ca2bfe61f1",
        "size compressed (bytes)": 1090748336,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat",
    },
    "beir-v1.0.0-cqadupstack-android.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "797b950b084d394f491fd84a0e7b8ef1",
        "size compressed (bytes)": 65438909,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat",
    },
    "beir-v1.0.0-cqadupstack-english.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "47f1408415a30ef448e516331d8c6131",
        "size compressed (bytes)": 114462176,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat",
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c293a3bca328183609c09d910094862a",
        "size compressed (bytes)": 128896849,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat",
    },
    "beir-v1.0.0-cqadupstack-gis.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "524162e606cc785a9f5e30b369d6334d",
        "size compressed (bytes)": 107086866,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat",
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a224440d580614ec8dc5d00f052aaa41",
        "size compressed (bytes)": 47527017,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat",
    },
    "beir-v1.0.0-cqadupstack-physics.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "ed92c35d50f462cf29b09369a15c0b94",
        "size compressed (bytes)": 109024718,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat",
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "b0f925036d7a7b1b7529fbee840befa1",
        "size compressed (bytes)": 91567849,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat",
    },
    "beir-v1.0.0-cqadupstack-stats.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a9db7f37526ee392ba762bf52e29f981",
        "size compressed (bytes)": 120271278,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat",
    },
    "beir-v1.0.0-cqadupstack-tex.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "f7e4f9da65d21bfc471e72c155791326",
        "size compressed (bytes)": 194009281,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat",
    },
    "beir-v1.0.0-cqadupstack-unix.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "d866f3c8d21ccfffecd400bda40dd823",
        "size compressed (bytes)": 134821507,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat",
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "84631850c0a127382e10ebb871b056a6",
        "size compressed (bytes)": 49530843,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat",
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "2e171633d09f3ac069fbafd7c1b81af3",
        "size compressed (bytes)": 138328538,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat",
    },
    "beir-v1.0.0-quora.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "1a58388eca4591390c439c7bf3a10dcc",
        "size compressed (bytes)": 1487402618,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat",
    },
    "beir-v1.0.0-dbpedia-entity.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c9dd2022c77ce99a381346b5e550f438",
        "size compressed (bytes)": 13226845554,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat",
    },
    "beir-v1.0.0-scidocs.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "11181c5fa0c75521cbac1417236a0a95",
        "size compressed (bytes)": 73530345,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat",
    },
    "beir-v1.0.0-fever.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "736b179578fe3798111bda2b2e00aced",
        "size compressed (bytes)": 15444001345,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat",
    },
    "beir-v1.0.0-climate-fever.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "fd1bfde8fd2bccc0be98edec8eb3bf20",
        "size compressed (bytes)": 15444073241,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat",
    },
    "beir-v1.0.0-scifact.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "0caa1724d9e6e3324bfd2a875b7218df",
        "size compressed (bytes)": 14758752,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat",
    },

    # BEIR (v1.0.0) bge-base-en-v1.5 indexes
    "beir-v1.0.0-trec-covid.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "da2d227d8ddbb97109b469f8e1473b3b",
        "size compressed (bytes)": 489619642,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "13261d776f4f27aec1abf4431eedcb42",
        "size compressed (bytes)": 42566761620,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "40da814f50fadf5f5ac1feb06ed3903b",
        "size compressed (bytes)": 10355291,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-nq.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b738bbbe7ca36532f25189b776d4e153",
        "size compressed (bytes)": 7630355859,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "d2c08665e8cd750bd06ceb7d23897c94",
        "size compressed (bytes)": 14932298529,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b57027c48f0b31c53fca034a1f773541",
        "size compressed (bytes)": 164430948,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "3286c1fa5496e3d5de97eee1e621ad3b",
        "size compressed (bytes)": 8162604163,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "2032399345f13ea0d1f15d7ae22427d1",
        "size compressed (bytes)": 1580911769,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "e136ef8528027b9085161b5a4f3dc046",
        "size compressed (bytes)": 1503712018,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "269047a536f856117a6a34048f49c030",
        "size compressed (bytes)": 24759653,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "00b68d1ef1c677715ca1ac10c676f99d",
        "size compressed (bytes)": 1090354182,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "f77217f345ec8e26e8f4b45c1a81dba2",
        "size compressed (bytes)": 65620193,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "0c57a49936831e31f8aec4d893dc2e36",
        "size compressed (bytes)": 114768549,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "51d5a6a8157a27b2a919890d7760fb01",
        "size compressed (bytes)": 129249921,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "0d4a65cecf8fb51be5f3fc89bbc0910d",
        "size compressed (bytes)": 107394286,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "bbae6dfe9ad38215143bf04c1d70e210",
        "size compressed (bytes)": 47672368,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "8a28f699c6c93cf3847b2c7c0e38916d",
        "size compressed (bytes)": 109354431,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "87786e84825276f2edddf282dbed87c5",
        "size compressed (bytes)": 91818236,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "44d178e9780083dc5eb6dafdc7871e69",
        "size compressed (bytes)": 120632552,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "94eae392bef6c8d78a3e8a086f867478",
        "size compressed (bytes)": 194551985,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cc0c4ec48266f3064661f7e2cfd3aa97",
        "size compressed (bytes)": 135195477,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "6e9ccef54902fa6740e0ff37cf187215",
        "size compressed (bytes)": 49670415,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b0d124624680cc3c833f348b4f9a1396",
        "size compressed (bytes)": 138678474,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-quora.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cab4a6c847331986cf62490238aec4a5",
        "size compressed (bytes)": 1491755601,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "d3ba32cc2c185ef9585a91b6083ad78e",
        "size compressed (bytes)": 13265129127,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cb41d6930f699514c70b23e99506954c",
        "size compressed (bytes)": 73776098,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-fever.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b9ccc330c46645e7819b73315dab8d29",
        "size compressed (bytes)": 15489138892,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "13515703cfa4032a0ae3a94ac2a3b76f",
        "size compressed (bytes)": 15489213928,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "248b6db6e61d18f17674219aecd8b41d",
        "size compressed (bytes)": 14807082,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },
    # BEIR (v1.0.0) cohere-embed-english-v3.0 indexes
    "beir-v1.0.0-trec-covid.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-COVID) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "fc8d3ea638e6392e42f532d9a9b2473b",
        "size compressed (bytes)": 414024898,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (BioASQ) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "057997ebe1bd0a2a461f48a6fa891e36",
        "size compressed (bytes)": 36008753142,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (NFCorpus) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "d837ad82575de15d99c3e7d617c9c5b7",
        "size compressed (bytes)": 8769679,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (NQ) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-nq.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "7317fe3a0f8185c5df0a6531b4c203df",
        "size compressed (bytes)": 6456624840,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (HotpotQA) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "42da497387358389a6868cc2b96b1e29",
        "size compressed (bytes)": 12618101496,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (FiQA-2018) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "1a8daeb75d6d90b462c3e08b7ddc518e",
        "size compressed (bytes)": 139105470,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Signal-1M) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "4007841cd6341d088ba8cb479a178223",
        "size compressed (bytes)": 6910589037,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-NEWS) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "185fc5cc07d49592701ca371964b23b0",
        "size compressed (bytes)": 1292117526,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Robust04) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "4f5bf3bf1d171601192d6282a2100d5a",
        "size compressed (bytes)": 1271873159,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (ArguAna) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "aa41dc0b9dcb7800db9d0da28c92f7ab",
        "size compressed (bytes)": 20943565,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Webis-Touche2020) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "029a2f90dba4b43ebf1c08fa1391d669",
        "size compressed (bytes)": 920313935,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-android) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "df22925505b2a849183392c2f5e77de7",
        "size compressed (bytes)": 55520457,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-english) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "baeca7a93d78717134e47d9a68d47d93",
        "size compressed (bytes)": 97094650,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gaming) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "454bdab58c4913879e72c0a1ec0d151d",
        "size compressed (bytes)": 109357956,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gis) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "13feaa47f324e82160b64006f4c8ab02",
        "size compressed (bytes)": 90814190,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-mathematica) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "dd9f2997c53b3096c928a31cd401e33d",
        "size compressed (bytes)": 40290632,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-physics) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "3ce9d4a450068355a0e525c655352788",
        "size compressed (bytes)": 92506339,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-programmers) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "f0ab46150ca322ed958a1deea2a81942",
        "size compressed (bytes)": 77659528,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-stats) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "8a9be5f3292b1f537dd8b769754a2fc6",
        "size compressed (bytes)": 101984479,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-tex) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "bb7658fe0aed83cdab108c3c30d2070a",
        "size compressed (bytes)": 164385190,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-unix) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "86c6c0f4810119b49dad7e938b69432d",
        "size compressed (bytes)": 114349232,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-webmasters) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "11336ee9dc0fc1751e4504ef02968722",
        "size compressed (bytes)": 42021677,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-wordpress) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "6009da48e8ca9d7c5a6d1b40e5682d66",
        "size compressed (bytes)": 117283207,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Quora) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-quora.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "02c7b4b04f9068a1d40e4105cb227ce8",
        "size compressed (bytes)": 1261685670,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (DBPedia) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "7f82e6710435dd98cd1bdaa2176a50d3",
        "size compressed (bytes)": 11215257899,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (SCIDOCS) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "5bf026b2d00721da37e3fef94d8a7c1f",
        "size compressed (bytes)": 62465918,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-fever.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "115c8015033b06f54e2bffdcf9135d4b",
        "size compressed (bytes)": 13095399646,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Climate-FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "6437ab39a758e38d2a5aa07c1a00e7ae",
        "size compressed (bytes)": 13095456722,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (SciFact) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "0c5cc4e57a2494a4336d599869527835",
        "size compressed (bytes)": 12522417,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    }
}

FAISS_INDEX_INFO_MRTYDI = {
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
    }
}

FAISS_INDEX_INFO_MIRACL = {
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

    "miracl-v1.0-ar-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "80c18ac84922ae27bfbee881485816c6",
        "size compressed (bytes)": 5861079368,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "08191b7749151a7bc70e54b92988dd25",
        "size compressed (bytes)": 845828394, 
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "a460d0eb95cf8a278686531e13141d00",
        "size compressed (bytes)": 93426889457, 
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "936e9188c4dcf57f8f116b9e25790372",
        "size compressed (bytes)": 29499200527,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "58f83135ecafae6993e49f5f08e471ff",
        "size compressed (bytes)": 6278766617,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "b10bc504213199fe0c0972678ab4fdd6",
        "size compressed (bytes)": 5358004166,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "b0d5543824b456d9008d05d7dcef5272",
        "size compressed (bytes)": 41578767020, 
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "ba66e98169b22244c7a7a89ae9bfe549", 
        "size compressed (bytes)": 1439122724, 
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "700466ab62bfd4b0ceddff7aa9b7a5f8",
        "size compressed (bytes)": 4113610061,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "f0358ae58b32456c3cef5f71e83a0143",
        "size compressed (bytes)": 19772957772,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "fa00afb61fa4332c408069cb6eb2e8f2",
        "size compressed (bytes)": 4229330667,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-korean"
    },
    "miracl-v1.0-ru-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "118835c214f7b24997ab9f1744b3f5ee",
        "size compressed (bytes)": 27155045095, 
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "ae45812eadb685c672f7b19c084ae3bc",
        "size compressed (bytes)": 375416284,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "8cbea3c141002dd477a15b387350ea37",
        "size compressed (bytes)": 1474250608,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "58cd7d862f202ece45dbd4cb6b6d12f4",
        "size compressed (bytes)": 1540980581,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "d8800abe1ac22b4161704f2b6d4fe575",
        "size compressed (bytes)": 14034991692,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (German) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "218cb42441af355285fbf219e9d2d7c7",
        "size compressed (bytes)": 45085913144,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "f8aee10055a31914c4c214819a7c1890",
        "size compressed (bytes)": 139276690,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    }

}

FAISS_INDEX_INFO_CIRAL = {
    "ciral-v1.0-ha-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Hausa) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-ha.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-ha.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "1feb2fb70d16117bd588f7d2168758c8",
        "size compressed (bytes)": 2023010322,
        "documents": 715355,
        "downloaded": False,
        "texts": "ciral-v1.0-ha"
    },

    "ciral-v1.0-so-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Somali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-so.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-so.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "eb5a9ab2c0aea0939768980f93bd28a2",
        "size compressed (bytes)": 2356035617,
        "documents": 827552,
        "downloaded": False,
        "texts": "ciral-v1.0-so"
    },

    "ciral-v1.0-sw-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-sw.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-sw.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "0a0412eadf7fb8895bbc6d7090019352",
        "size compressed (bytes)": 2689039681,
        "documents": 949013,
        "downloaded": False,
        "texts": "ciral-v1.0-sw"
    },

    "ciral-v1.0-yo-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-yo.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-yo.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "0f84c7f8594b6352aa26970565877668",
        "size compressed (bytes)": 233478865,
        "documents": 82095,
        "downloaded": False,
        "texts": "ciral-v1.0-yo"
    },

    "ciral-v1.0-ha-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Hausa) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-ha.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-ha.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "809f7c3c211c019a345e7bc8a716ff7b",
        "size compressed (bytes)": 2023992537,
        "documents": 715355,
        "downloaded": False,
        "texts": "ciral-v1.0-ha"
    },

    "ciral-v1.0-so-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Somali) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-so.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-so.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "0ef7404ef10f3135f6a11addcf723504",
        "size compressed (bytes)": 2356542056,
        "documents": 827552,
        "downloaded": False,
        "texts": "ciral-v1.0-so"
    },

    "ciral-v1.0-sw-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Swahili) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-sw.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-sw.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "1951d3f61eef760407c66c426e5047c6",
        "size compressed (bytes)": 2688836963,
        "documents": 949013,
        "downloaded": False,
        "texts": "ciral-v1.0-sw"
    },

    "ciral-v1.0-yo-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-yo.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-yo.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "f433299809c659cfc4dede6c42d4a3fd",
        "size compressed (bytes)": 233490972,
        "documents": 82095,
        "downloaded": False,
        "texts": "ciral-v1.0-yo"
    },
}

FAISS_INDEX_INFO_WIKIPEDIA = {
    "wikipedia-dpr-100w.dpr-multi": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on multiple QA datasets",
        "filename": "faiss.wikipedia-dpr-100w.dpr_multi.20200127.f403c3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dpr_multi.20200127.f403c3.tar.gz"
        ],
        "md5": "fe307ef2e60ab6e6f3ad66e24a4144ae",
        "size compressed (bytes)": 59836766732,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dpr-single-nq": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.dpr_single-nq.20200115.cd5034.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dpr_single-nq.20200115.cd5034.tar.gz"
        ],
        "md5": "01fb6bcaa047df254663d0a3d854b7cc",
        "size compressed (bytes)": 59836863979,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.bpr-single-nq": {
        "description": "Faiss binary index of Wikipedia encoded by the BPR doc encoder trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.bpr_single-nq.20210827.8a8f75.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.bpr_single-nq.20210827.8a8f75.tar.gz"
        ],
        "md5": "b022580ab2fc66f6eaa54af241dba690",
        "size compressed (bytes)": 1886380629,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.ance-multi": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the ANCE-multi encoder",
        "filename": "faiss.wikipedia-dpr-100w.ance_multi.20210224.060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.ance_multi.20210224.060cef.tar.gz"
        ],
        "md5": "eb00e096460c8e6296a39732f1676dd7",
        "size compressed (bytes)": 59890491335,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dkrr-nq": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "36a658e08dafb3e3313b05f88e001557",
        "size compressed (bytes)": 37812137732,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dkrr-tqa": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on TriviaQA",
        "filename": "faiss.wikipedia-dpr-100w.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "072a514ca3ff7717339038d024019e3d",
        "size compressed (bytes)": 37802648577,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wiki-all-6-3.dpr2-multi-retriever": {
        "description": "Faiss FlatIP index of wiki-all-6-3-tamber encoded by a 2nd iteration DPR model trained on multiple QA datasets",
        "filename": "faiss.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        "readme": "faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        ],
        "md5": "823b6297d6fd8011598e7618742ac7f8",
        "size compressed (bytes)": 218257913366,
        "documents": 76680040,
        "downloaded": False,
        "texts": "wiki-all-6-3-tamber"
    }
}

FAISS_INDEX_INFO_OTHER = {
    "cast2019-tct_colbert-v2.hnsw": {
        "description": "Faiss HNSW index of the CAsT2019 passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "faiss-hnsw.cast2019.tct_colbert-v2.tar.gz",
        "readme": "faiss-hnsw.cast2019.tct_colbert-v2-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/hnsw-faiss.cast2019.tct_colbert-v2.tar.gz"
        ],
        "md5": "2ce7ce8064ed235a9b6aad08571340d4",
        "size compressed (bytes)": 112121368296,
        "documents": 38429835,
        "downloaded": False,
        "texts": "cast2019"
    },
    # TODO: update urls to rgw.cs.uwaterloo.ca/....
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base": {
        "description": "Faiss index for AToMiC Images v0.2 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.base.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.base.faiss.flat.tar.gz"
        ],
        "md5": "7e7abf80e99b81c444281405db19c579",
        "size compressed (bytes)": 9284282630,
        "documents": 3410779,
        "downloaded": False,
        "texts": "atomic_image_v0.2_base"
    },
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.faiss.flat.tar.gz"
        ],
        "md5": "501b7477a8e1eea9e10904a2ea307906",
        "size compressed (bytes)": 29984366146,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation": {
        "description": "Faiss index for AToMiC Images v0.2 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.small.validation.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.small.validation.faiss.flat.tar.gz"
        ],
        "md5": "798d601cfc505a4b290bb708290a38fc",
        "size compressed (bytes)": 43875634,
        "documents": 16126,
        "downloaded": False,
        "texts": "atomic_image_v0.2_small_validation"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.base.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.base.faiss.flat.tar.gz"
        ],
        "md5": "1d90ecfb703b96f003a9d6dc054c057b",
        "size compressed (bytes)": 8187618352,
        "documents": 3029504,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_base"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.faiss.flat.tar.gz"
        ],
        "md5": "9f5962e0b29bb341cba88041107b693e",
        "size compressed (bytes)": 27373277238,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.small.validation.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.small.validation.faiss.flat.tar.gz"
        ],
        "md5": "2dd9d0c805bbef6a6a23ece3c2b221a3",
        "size compressed (bytes)": 46421016,
        "documents": 17173,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_small_validation"
    },
    "atomic-v0.2.ViT-H-14.laion2b_s32b_b79k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k",
        "filename": "ViT-H-14.laion2b_s32b_b79k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-H-14.laion2b_s32b_b79k.image.faiss.flat.tar.gz"
        ],
        "md5": "3cacbc8af251dd59177140b83de61024",
        "size compressed (bytes)": 39192329951,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-H-14.laion2b_s32b_b79k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k",
        "filename": "ViT-H-14.laion2b_s32b_b79k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-H-14.laion2b_s32b_b79k.text.faiss.flat.tar.gz"
        ],
        "md5": "7866b6b2c38cd46eea5fc28254cf17bc",
        "size compressed (bytes)": 35824621106,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-bigG-14.laion2b_s39b_b160k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k",
        "filename": "ViT-bigG-14.laion2b_s39b_b160k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-bigG-14.laion2b_s39b_b160k.image.faiss.flat.tar.gz"
        ],
        "md5": "1837c886187bb6ecc60fdc02c6056a21",
        "size compressed (bytes)": 48274458058,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-bigG-14.laion2b_s39b_b160k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k",
        "filename": "ViT-bigG-14.laion2b_s39b_b160k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-bigG-14.laion2b_s39b_b160k.text.faiss.flat.tar.gz"
        ],
        "md5": "5cc288862b73772b466916a79ec311b0",
        "size compressed (bytes)": 44195349889,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-B-32.laion2b_e16.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16",
        "filename": "ViT-B-32.laion2b_e16.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion2b_e16.image.faiss.flat.tar.gz"
        ],
        "md5": "1b35007a5b066179180edd2fb2d56448",
        "size compressed (bytes)": 20408227482,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-B-32.laion2b_e16.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16",
        "filename": "ViT-B-32.laion2b_e16.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion2b_e16.text.faiss.flat.tar.gz"
        ],
        "md5": "6182fc18d112dea4dcfd91546ddf0747",
        "size compressed (bytes)": 18574571493,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-B-32.laion400m_e32.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32",
        "filename": "ViT-B-32.laion400m_e32.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion400m_e32.image.faiss.flat.tar.gz"
        ],
        "md5": "c08ea30351953b6c91c9b15ad87749e4",
        "size compressed (bytes)": 20402486061,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-B-32.laion400m_e32.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32",
        "filename": "ViT-B-32.laion400m_e32.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion400m_e32.text.faiss.flat.tar.gz"
        ],
        "md5": "a68e71ed301870a9be82003f0246183b",
        "size compressed (bytes)": 18566367182,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.openai.clip-vit-large-patch14.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14",
        "filename": "openai.clip-vit-large-patch14.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-large-patch14.image.faiss.flat.tar.gz"
        ],
        "md5": "6bb4b5169ca864328ab03ecdd484437d",
        "size compressed (bytes)": 29989412901,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.openai.clip-vit-large-patch14.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14",
        "filename": "openai.clip-vit-large-patch14.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-large-patch14.text.faiss.flat.tar.gz"
        ],
        "md5": "c6303d01cac83be6902df2967782d2cb",
        "size compressed (bytes)": 27399921354,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.openai.clip-vit-base-patch32.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32",
        "filename": "openai.clip-vit-base-patch32.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-base-patch32.image.faiss.flat.tar.gz"
        ],
        "md5": "2af24862dd2a37b92cc03edc465d3705",
        "size compressed (bytes)": 20434283763,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.openai.clip-vit-base-patch32.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32",
        "filename": "openai.clip-vit-base-patch32.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-base-patch32.text.faiss.flat.tar.gz"
        ],
        "md5": "15c643b65b990aaf5fe3ec1012a710e0",
        "size compressed (bytes)": 18586684424,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.facebook.flava-full.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-facebook.flava-full",
        "filename": "facebook.flava-full.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/facebook.flava-full.image.faiss.flat.tar.gz"
        ],
        "md5": "0c5d4e938627dc902cbde9a47a179d41",
        "size compressed (bytes)": 29963221412,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.facebook.flava-full.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-facebook.flava-full",
        "filename": "facebook.flava-full.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/facebook.flava-full.text.faiss.flat.tar.gz"
        ],
        "md5": "763e574a749a16b6bf56d7b622131c12",
        "size compressed (bytes)": 27414008560,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.Salesforce.blip-itm-base-coco.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco",
        "filename": "Salesforce.blip-itm-base-coco.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-base-coco.image.faiss.flat.tar.gz"
        ],
        "md5": "9d924b64860ae26857e57591c621b811",
        "size compressed (bytes)": 10466804855,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.Salesforce.blip-itm-base-coco.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco",
        "filename": "Salesforce.blip-itm-base-coco.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-base-coco.text.faiss.flat.tar.gz"
        ],
        "md5": "a52770a28ce877e271544de3298b1e53",
        "size compressed (bytes)": 9439317784,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.Salesforce.blip-itm-large-coco.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco",
        "filename": "Salesforce.blip-itm-large-coco.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-large-coco.image.faiss.flat.tar.gz"
        ],
        "md5": "550b318e53f18604b2b919a3c22cfa39",
        "size compressed (bytes)": 10463191370,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.Salesforce.blip-itm-large-coco.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco",
        "filename": "Salesforce.blip-itm-large-coco.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-large-coco.text.faiss.flat.tar.gz"
        ],
        "md5": "a09bb2b0b2ae3eb5099061a7cddfe949",
        "size compressed (bytes)": 9440231672,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
}

FAISS_INDEX_INFO = {**FAISS_INDEX_INFO_MSMARCO,
                    **FAISS_INDEX_INFO_BEIR,
                    **FAISS_INDEX_INFO_MRTYDI,
                    **FAISS_INDEX_INFO_MIRACL,
                    **FAISS_INDEX_INFO_WIKIPEDIA,
                    **FAISS_INDEX_INFO_CIRAL,
                    **FAISS_INDEX_INFO_OTHER}

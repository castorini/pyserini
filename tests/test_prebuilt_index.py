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

import unittest

import requests

from pyserini.prebuilt_index_info import TF_INDEX_INFO, IMPACT_INDEX_INFO, \
    LUCENE_HNSW_INDEX_INFO, LUCENE_FLAT_INDEX_INFO, FAISS_INDEX_INFO
from pyserini.pyclass import autoclass


class TestPrebuiltIndexes(unittest.TestCase):
    def test_index_inf(self):
        # Test the accessibility of IndexInfo on the Anserini end to make sure everything is "connected together"
        JIndexInfo = autoclass('io.anserini.index.IndexInfo')

        self.assertEqual(JIndexInfo.BEIR_V1_0_0_ARGUANA_BGE_BASE_EN_15_FLAT.indexName,
                         'beir-v1.0.0-arguana.bge-base-en-v1.5.flat')
        self.assertEqual(JIndexInfo.BEIR_V1_0_0_ARGUANA_BGE_BASE_EN_15_FLAT.filename,
                         'lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240618.6cf601.tar.gz')
        self.assertEqual(JIndexInfo.BEIR_V1_0_0_ARGUANA_BGE_BASE_EN_15_FLAT.readme,
                         'lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20240618.6cf601.README.md')
        self.assertEqual(JIndexInfo.BEIR_V1_0_0_ARGUANA_BGE_BASE_EN_15_FLAT.urls[0],
                         'https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240618.6cf601.tar.gz')

    def test_lucene_tf_beir(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'beir' in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # 29 each for flat and multifield
        self.assertEqual(cnt, 58)
        self._test_urls(urls)

    def test_lucene_tf_mrtydi(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'mrtydi' in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # 11 languages, but two entries for each language from aliases (e.g., arabic and ar)
        self.assertEqual(cnt, 22)
        self._test_urls(urls)

    def test_lucene_tf_miracl(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'miracl' in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # 18 languages including surprise
        self.assertEqual(cnt, 18)
        self._test_urls(urls)

    def test_lucene_tf_ciral(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'ciral' in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # each 4: african languages, english translations
        self.assertEqual(cnt, 8)
        self._test_urls(urls)

    def test_lucene_impact_beir(self):
        urls = []
        cnt = 0
        for key in IMPACT_INDEX_INFO:
            if 'beir' in key:
                cnt += 1
                for url in IMPACT_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # 29 from SPLADE-distill CoCodenser-medium
        self.assertEqual(cnt, 29)
        self._test_urls(urls)

    def test_lucene_impact_mrtydi(self):
        urls = []
        cnt = 0
        for key in IMPACT_INDEX_INFO:
            if 'miracl' in key:
                cnt += 1
                for url in IMPACT_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # currently, none
        self.assertEqual(cnt, 0)

    def test_lucene_impact_miracl(self):
        urls = []
        cnt = 0
        for key in IMPACT_INDEX_INFO:
            if 'miracl' in key:
                cnt += 1
                for url in IMPACT_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # currently, none
        self.assertEqual(cnt, 0)

    def test_lucene_hnsw_beir(self):
        urls = []
        cnt = 0
        for key in LUCENE_HNSW_INDEX_INFO:
            if 'beir' in key:
                cnt += 1
                for url in LUCENE_HNSW_INDEX_INFO[key]['urls']:
                    urls.append(url)

        self.assertEqual(cnt, 29)
        self._test_urls(urls)

    def test_lucene_flat_beir(self):
        urls = []
        cnt = 0
        for key in LUCENE_FLAT_INDEX_INFO:
            if 'beir' in key:
                cnt += 1
                for url in LUCENE_FLAT_INDEX_INFO[key]['urls']:
                    urls.append(url)

        self.assertEqual(cnt, 29)
        self._test_urls(urls)

    def test_faiss_beir(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'beir' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # each 29: contriever, contriever-msmarco, bge, cohere-embed-english-v3.0
        self.assertEqual(cnt, 116)
        self._test_urls(urls)

    def test_faiss_mrtydi(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'mrtydi-' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # each 11: mdpr-nq, mdpr-tied-pft-msmarco, mdpr-tied-pft-nq, mdpr-tied-pft-msmarco-ft-all
        self.assertEqual(cnt, 44)
        self._test_urls(urls)

    def test_faiss_miracl(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'miracl' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # 18 pFT MS MARCO, 18 pFT MS MARCO all, 16 pFT MS MARCO + per lang (no de, yo), 18 mContriever pFT MS MARCO
        self.assertEqual(cnt, 70)
        self._test_urls(urls)

    def test_faiss_msmarco(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'msmarco-v' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        self.assertEqual(cnt, 19)
        self._test_urls(urls)

    def test_faiss_ciral(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'ciral' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        # each 4: mdpr-tied-pft-msmarco, afriberta-dpr-ptf-msmarco-ft-latin-mrtydi
        self.assertEqual(cnt, 8)
        self._test_urls(urls)

    def test_faiss_wikipedia(self):
        urls = []
        cnt = 0
        for key in FAISS_INDEX_INFO:
            if 'wiki' in key:
                cnt += 1
                for url in FAISS_INDEX_INFO[key]['urls']:
                    urls.append(url)

        self.assertEqual(cnt, 7)
        self._test_urls(urls)

    def _test_urls(self, urls):
        cnt = 0
        for url in urls:
            cnt += 1
            response = requests.head(url)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(cnt, len(urls))

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

from pyserini.prebuilt_index_info import (
    FAISS_INDEX_INFO,
    IMPACT_INDEX_INFO,
    LUCENE_FLAT_INDEX_INFO,
    LUCENE_HNSW_INDEX_INFO,
    TF_INDEX_INFO,
)
from pyserini.pyclass import autoclass


class TestPrebuiltIndexes(unittest.TestCase):
    def test_index_inf(self):
        # Test the accessibility of IndexInfo on the Anserini end to make sure everything is "connected together"
        JPrebuiltFlatIndex = autoclass('io.anserini.index.prebuilt.PrebuiltFlatIndex')

        self.assertEqual(JPrebuiltFlatIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.flat').name,
            'beir-v1.0.0-arguana.bge-base-en-v1.5.flat')
        self.assertEqual(JPrebuiltFlatIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.flat').filename,
            'lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20260425.bb3d65.tar')
        self.assertEqual(JPrebuiltFlatIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.flat').readme,
            'https://huggingface.co/datasets/castorini/prebuilt-indexes-beir/blob/main/lucene-flat/bge-base-en-v1.5/lucene-flat.beir-v1.0.0.bge-base-en-v1.5.20260425.bb3d65.README.md')
        self.assertEqual(JPrebuiltFlatIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.flat').urls[0],
            'https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20260425.bb3d65.tar')

    TF_CASES = (
        ('msmarco-v1', 16),    # 10 for doc, 5 for passage, 1 alias
        ('beir-v1.0.0-', 58),  # 29 each for flat and multifield
        ('bright-', 12),
        ('mrtydi-v1.1-', 22),  # 11 languages, but two entries for each language from aliases (e.g., arabic and ar)
        ('miracl-v1.0-', 18),  # 18 languages including surprise
        ('ciral-v1.0-', 8)     # each 4: african languages, english translations
    )

    # TF Cases
    def test_lucene_tf_indexes(self):
        for prefix, expected in self.TF_CASES:
            with self.subTest(prefix=prefix):
                urls = []
                cnt = 0
                for key in TF_INDEX_INFO:
                    if key.startswith(prefix):
                        cnt += 1
                        urls.extend(TF_INDEX_INFO[key]['urls'])
                self.assertEqual(cnt, expected)
                self._test_urls(urls)

    IMPACT_CASES = (
        ('msmarco-', 26),
        ('beir-v1.0.0-', 58),  # 29 each from SPLADE++ (CoCondenser-EnsembleDistil) and SPLADEv3
        ('bright-', 12),
        ('mrtydi-', 0),        # currently, none
        ('miracl-', 0)         # currently, none
    )

    # Impact Cases
    def test_lucene_impact_indexes(self):
        for prefix, expected in self.IMPACT_CASES:
            with self.subTest(prefix=prefix):
                urls = []
                cnt = 0
                for key in IMPACT_INDEX_INFO:
                    if key.startswith(prefix):
                        cnt += 1
                        urls.extend(IMPACT_INDEX_INFO[key]['urls'])
                self.assertEqual(cnt, expected)
                self._test_urls(urls)

    HNSW_CASES = (('beir-v1.0.0-', 29),
                  ('msmarco-v1-passage', 6),
                  ('msmarco-v2.1-doc-segmented', 10))

    # Lucene HNSW Cases
    def test_lucene_hnsw_indexes(self):
        for prefix, expected in self.HNSW_CASES:
            with self.subTest(prefix=prefix):
                urls = []
                cnt = 0
                for key in LUCENE_HNSW_INDEX_INFO:
                    if key.startswith(prefix):
                        cnt += 1
                        urls.extend(LUCENE_HNSW_INDEX_INFO[key]['urls'])
                self.assertEqual(cnt, expected)
                self._test_urls(urls)

    FLAT_CASES = (('beir-v1.0.0-', 29),
                  ('bright-', 12))

    # Lucene Flat Cases
    def test_lucene_flat_indexes(self):
        for prefix, expected in self.FLAT_CASES:
            with self.subTest(prefix=prefix):
                urls = []
                cnt = 0
                for key in LUCENE_FLAT_INDEX_INFO:
                    if key.startswith(prefix):
                        cnt += 1
                        urls.extend(LUCENE_FLAT_INDEX_INFO[key]['urls'])
                self.assertEqual(cnt, expected)
                self._test_urls(urls)

    FAISS_CASES = (
        # name, match, expected, dedupe
        ('beir', lambda k: 'beir' in k and 'm-beir' not in k, 116, False),  # each 29: contriever, contriever-msmarco, bge, cohere-embed-english-v3.0
        ('bright', lambda k: 'bright' in k, 36, False),
        ('mrtydi', lambda k: 'mrtydi-' in k, 44, False),                    # each 11: mdpr-nq, mdpr-tied-pft-msmarco, mdpr-tied-pft-nq, mdpr-tied-pft-msmarco-ft-all
        ('miracl', lambda k: 'miracl' in k, 70, False),                     # 18 pFT MS MARCO, 18 pFT MS MARCO all, 16 pFT MS MARCO + per lang (no de, yo), 18 mContriever pFT MS MARCO
        ('msmarco', lambda k: 'msmarco-v' in k, 23, False),
        ('ciral', lambda k: 'ciral' in k, 8, False),                        # each 4: mdpr-tied-pft-msmarco, afriberta-dpr-ptf-msmarco-ft-latin-mrtydi
        ('wikipedia', lambda k: 'wikipedia' in k or 'wiki-all' in k, 7, False),
        ('mmeb', lambda k: 'mmeb' in k, 44, True),
        ('m-beir', lambda k: 'm-beir' in k, 34, True),
        ('dse', lambda k: 'dse' in k, 2, False)
    )

    # Faiss Cases
    def test_faiss_indexes(self):
        for name, match, expected, dedupe in self.FAISS_CASES:
            with self.subTest(name=name):
                urls = set() if dedupe else []
                cnt = 0
                for key in FAISS_INDEX_INFO:
                    if match(key):
                        cnt += 1
                        if dedupe:
                            urls.update(FAISS_INDEX_INFO[key]['urls'])
                        else:
                            urls.extend(FAISS_INDEX_INFO[key]['urls'])
                self.assertEqual(cnt, expected)
                self._test_urls(urls)

    def _test_urls(self, urls):
        cnt = 0
        for url in urls:
            cnt += 1
            self._assert_url_accessible(url)

        self.assertEqual(cnt, len(urls))

    def _assert_url_accessible(self, url):
        transient_status_codes = {408, 429, 500, 502, 503, 504}
        attempts = []

        for _ in range(3):
            for method in ['HEAD', 'GET']:
                try:
                    kwargs = {'allow_redirects': True, 'timeout': (5, 30)}
                    if method == 'GET':
                        kwargs['headers'] = {'Range': 'bytes=0-0'}
                        kwargs['stream'] = True

                    response = requests.request(method, url, **kwargs)
                    try:
                        attempts.append(f'{method} {response.status_code} {response.url}')

                        if response.status_code == 200 or (method == 'GET' and response.status_code == 206):
                            return

                        if response.status_code not in transient_status_codes and method == 'GET':
                            self.fail(f'Error checking {url}; attempts: {"; ".join(attempts)}')
                    finally:
                        response.close()
                except requests.RequestException as e:
                    attempts.append(f'{method} {type(e).__name__}: {e}')

        self.fail(f'Error checking {url}; attempts: {"; ".join(attempts)}')


if __name__ == '__main__':
    unittest.main()

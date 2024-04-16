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

import os
import shutil
import unittest
from typing import List, Dict

from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder
from pyserini.search.hybrid import HybridSearcher


class TestHybridSearch(unittest.TestCase):
    tarball_name = None
    collection_url = None
    searcher = None
    searcher_index_dir = None
    no_vec_searcher = None
    no_vec_searcher_index_dir = None

    @classmethod
    def setUpClass(cls):
        cls.s_index_name = 'beir-v1.0.0-arguana.flat'
        cls.d_searcher_name = 'facebook/contriever-msmarco'
        cls.d_index_name = 'beir-v1.0.0-arguana.contriever-msmarco'
        
        cls.s_searcher = LuceneSearcher.from_prebuilt_index(f'{cls.s_index_name}')
        cls.d_encoder = AutoQueryEncoder(cls.d_searcher_name, pooling='mean', l2_norm=False)
        cls.d_searcher = FaissSearcher.from_prebuilt_index(f'{cls.d_index_name}', cls.d_encoder)
        cls.searcher = HybridSearcher(cls.d_searcher, cls.s_searcher)

    def test_hybrid_searcher(self):
        hits = self.searcher.search('information retrieval')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, 'test-digital-freedoms-aihbiahr-con03b')
        self.assertAlmostEqual(hits[0].score, 1.440788245201111, places=5)
    
    def test_hybrid_searcher_batch(self):
        hits = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)
        self.assertTrue(isinstance(hits, Dict))
        
        self.assertTrue(isinstance(hits['q1'], List))
        self.assertEqual(hits['q1'][0].docid, 'test-digital-freedoms-aihbiahr-con03b')
        self.assertAlmostEqual(hits['q1'][0].score, 1.440788245201111, places=5)

        self.assertTrue(isinstance(hits['q2'], List))
        self.assertEqual(hits['q2'][0].docid, 'test-digital-freedoms-piidfaihbg-pro01a')
        self.assertAlmostEqual(hits['q2'][0].score, 1.4042499542236329, places=5)


if __name__ == '__main__':
    unittest.main()

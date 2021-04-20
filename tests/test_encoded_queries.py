#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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
import os
import shutil
from pyserini.search import get_topics
from pyserini.dsearch import QueryEncoder


class TestEncodedQueries(unittest.TestCase):

    def setUp(self):
        os.environ['PYSERINI_CACHE'] = 'temp_dir'

    def test_tct_colbert_msmarco_passage_dev_subset(self):
        encoder = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_msmarco_passage_dev_subset(self):
        encoder = QueryEncoder.load_encoded_queries('ance-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_tct_colbert_msmarco_doc_dev(self):
        encoder = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-doc-dev')
        topics = get_topics('msmarco-doc-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_maxp_msmarco_doc_dev(self):
        encoder = QueryEncoder.load_encoded_queries('ance_maxp-msmarco-doc-dev')
        topics = get_topics('maxp-msmarco-doc-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_sbert_msmarco_passage_dev_subset(self):
        encoder = QueryEncoder.load_encoded_queries('sbert-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_distilbert_kd_msmarco_passage_dev_subset(self):
        encoder = QueryEncoder.load_encoded_queries('distilbert_kd-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_nq_dev(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-nq-dev')
        topics = get_topics('dpr-nq-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_nq_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_multi_nq_dev(self):
        encoder = QueryEncoder.load_encoded_queries('ance_multi-nq-dev')
        topics = get_topics('dpr-nq-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_multi_nq_test(self):
        encoder = QueryEncoder.load_encoded_queries('ance_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_trivia_dev(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-trivia-dev')
        topics = get_topics('dpr-trivia-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_trivia_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-trivia-test')
        topics = get_topics('dpr-trivia-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_multi_trivia_dev(self):
        encoder = QueryEncoder.load_encoded_queries('ance_multi-trivia-dev')
        topics = get_topics('dpr-trivia-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_ance_multi_trivia_test(self):
        encoder = QueryEncoder.load_encoded_queries('ance_multi-trivia-test')
        topics = get_topics('dpr-trivia-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_wq_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-wq-test')
        topics = get_topics('dpr-wq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_squad_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-squad-test')
        topics = get_topics('dpr-squad-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_multi_curated_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-curated-test')
        topics = get_topics('dpr-curated-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_single_nq_dev(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_single_nq-nq-dev')
        topics = get_topics('dpr-nq-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_single_nq_test(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_single_nq-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def tearDown(self):
        if os.path.exists('temp_dir'):
            shutil.rmtree('temp_dir')

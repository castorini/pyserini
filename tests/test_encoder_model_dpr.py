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

import json
import unittest
from itertools import islice

import numpy as np

from pyserini.encode import DprDocumentEncoder, DprQueryEncoder
from pyserini.search import get_topics


class TestEncodeDpr(unittest.TestCase):
    def test_dpr_doc_encoder(self):
        texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = DprDocumentEncoder('facebook/dpr-ctx_encoder-multiset-base', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.59793323, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.13036962, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.3044764, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.1516793, places=4)

    def test_dpr_encoded_queries(self):
        encoded = DprQueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_dpr_query_encoder(self):
        encoder = DprQueryEncoder('facebook/dpr-question_encoder-multiset-base')

        cached_encoder = DprQueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        # Just test the first 10 topics
        for t in dict(islice(topics.items(), 10)):
            cached_vector = np.array(cached_encoder.encode(topics[t]['title']))
            encoded_vector = np.array(encoder.encode(topics[t]['title']))

            l1 = np.sum(np.abs(cached_vector - encoded_vector))
            self.assertTrue(l1 < 0.0005)


if __name__ == '__main__':
    unittest.main()

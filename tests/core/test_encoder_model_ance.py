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
from itertools import islice

import numpy as np

from pyserini.encode import QueryEncoder, AnceQueryEncoder
from pyserini.search import get_topics


class TestEncodeAnce(unittest.TestCase):
    def test_ance_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('ance-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('ance-dl19-passage')
        topics = get_topics('dl19-passage')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('ance-dl20')
        topics = get_topics('dl20')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_ance_encoder(self):
        encoder = AnceQueryEncoder('castorini/ance-msmarco-passage')

        cached_encoder = QueryEncoder.load_encoded_queries('ance-dl20')
        topics = get_topics('dl20')
        # Just test the first 10 topics
        for t in dict(islice(topics.items(), 10)):
            cached_vector = np.array(cached_encoder.encode(topics[t]['title']))
            encoded_vector = np.array(encoder.encode(topics[t]['title']))

            l1 = np.sum(np.abs(cached_vector - encoded_vector))
            self.assertTrue(l1 < 0.0005)

    def test_ance_weights_loaded(self):
        encoder = AnceQueryEncoder('castorini/ance-msmarco-passage')
        norm_weights = encoder.model.norm.weight.detach().cpu().numpy()
        norm_bias = encoder.model.norm.bias.detach().cpu().numpy()
        self.assertFalse(np.allclose(norm_weights, np.ones_like(norm_weights)),
            "norm weights appear to be default initialized, not loaded from checkpoint")
        self.assertFalse(np.allclose(norm_bias, np.zeros_like(norm_bias)),
            "norm bias appear to be default initialized, not loaded from checkpoint")


if __name__ == '__main__':
    unittest.main()

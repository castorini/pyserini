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

from pyserini.encode import TctColBertDocumentEncoder, DprDocumentEncoder, UniCoilDocumentEncoder


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                self.texts.append(json.loads(line)['contents'])

    def test_dpr_encoder(self):
        encoder = DprDocumentEncoder('facebook/dpr-ctx_encoder-multiset-base', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.59793323, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.13036962, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.3044764, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.1516793, places=4)

    def test_tct_colbert_encoder(self):
        encoder = TctColBertDocumentEncoder('castorini/tct_colbert-msmarco', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.01649557, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.05648308, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.10293338, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.05549275, places=4)

    def test_unicoil_encoder(self):
        encoder = UniCoilDocumentEncoder('castorini/unicoil-d2q-msmarco-passage', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0]['generation'], 2.2441017627716064, places=4)
        self.assertAlmostEqual(vectors[0]['normal'], 2.4618067741394043, places=4)
        self.assertAlmostEqual(vectors[2]['rounding'], 3.9474332332611084, places=4)
        self.assertAlmostEqual(vectors[2]['commercial'], 3.288801670074463, places=4)


if __name__ == '__main__':
    unittest.main()

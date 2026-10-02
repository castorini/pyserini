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

import numpy as np

from pyserini.encode import AutoQueryEncoder

MODEL = 'sentence-transformers/msmarco-distilbert-base-v3'
# Deliberately different lengths so batching pads the shorter queries; the
# padding mask is what makes mean pooling match the per-query result.
QUERIES = [
    'what is information retrieval',
    'dense retrieval',
    'how do transformer models encode text for semantic search',
]


class TestBatchQueryEncode(unittest.TestCase):
    def _assert_batch_matches_single(self, encoder):
        batch = encoder.encode_batch(QUERIES)
        self.assertEqual(batch.shape[0], len(QUERIES))
        for i, query in enumerate(QUERIES):
            single = encoder.encode(query)
            self.assertEqual(batch[i].shape, single.shape)
            self.assertTrue(
                np.allclose(batch[i], single, atol=1e-5),
                f'batch row {i} differs from encode({query!r})',
            )

    def test_cls_pooling(self):
        encoder = AutoQueryEncoder(MODEL, device='cpu', pooling='cls')
        self._assert_batch_matches_single(encoder)

    def test_mean_pooling_l2(self):
        encoder = AutoQueryEncoder(MODEL, device='cpu', pooling='mean', l2_norm=True)
        self._assert_batch_matches_single(encoder)


if __name__ == '__main__':
    unittest.main()

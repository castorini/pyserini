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
import torch

from pyserini.encode import CosDprQueryEncoder


class TestEncodeCosDpr(unittest.TestCase):
    def test_cosdpr_query_encoder(self):
        torch.manual_seed(12345)
        encoder = CosDprQueryEncoder('castorini/cosdpr-distil', device='cpu')
        encoder.model.eval()
        vector = encoder.encode('what is information retrieval?')

        self.assertEqual(vector.shape, (768,))
        self.assertAlmostEqual(np.linalg.norm(vector), 1.0, places=4)
        self.assertAlmostEqual(vector[0], 0.04074, places=5)
        self.assertAlmostEqual(vector[-1], 0.01294, places=5)


if __name__ == '__main__':
    unittest.main()

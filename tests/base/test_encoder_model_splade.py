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

from pyserini.encode import SpladeQueryEncoder


class TestEncodeSplade(unittest.TestCase):
    def test_splade_encoder(self):
        encoder = SpladeQueryEncoder('naver/splade-v3')
        weights = encoder.encode('information retrieval')

        self.assertEqual(weights['retrieval'], 151)
        self.assertEqual(weights['information'], 139)
        self.assertEqual(weights['retrieve'], 107)
        self.assertEqual(weights['retrieved'], 92)
        self.assertEqual(weights['archive'], 53)


if __name__ == '__main__':
    unittest.main()

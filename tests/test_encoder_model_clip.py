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

from pyserini.encode import ClipDocumentEncoder


class TestEncodeClip(unittest.TestCase):
    def test_clip_encoder(self):
        texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = ClipDocumentEncoder('openai/clip-vit-base-patch32', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], 0.1933609, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.21501173, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.06461975, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.35396004, places=4)


if __name__ == '__main__':
    unittest.main()

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
import os
import unittest

from pyserini.encode import ArcticDocumentEncoder


class TestEncodeArctic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('core'):
            cls.resource_dir = '../resources'
        else:
            cls.resource_dir = 'tests/resources'

    def test_arctic_doc_encoder(self):
        texts = []
        with open(os.path.join(self.resource_dir, 'simple_cacm_corpus.json')) as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = ArcticDocumentEncoder('Snowflake/snowflake-arctic-embed-m-v1.5', device='cpu', truncate_to_256=True)
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], 0.05097485, places=4)
        self.assertAlmostEqual(vectors[0][-1], 0.04520516, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.027567765, places=4)
        self.assertAlmostEqual(vectors[2][-1], 4.9405815e-05, places=4)
    
    def test_arctic_query_encoder(self):
        pass
        #TODO: Implement test_arctic_query_encoder after beir regression incorporated


if __name__ == '__main__':
    unittest.main()

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
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

from pyserini.encode import AutoQueryEncoder
from pyserini.query_iterator import DefaultQueryIterator


EXPECTED_VALUES = [(0.18463, -0.08488), (-0.28631, 0.20652)]


class TestEncodeDistilBertTasB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    def test_distilbert_tas_b_encode_query_cli(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
            subprocess.run(
                [
                    sys.executable, '-m', 'pyserini.encode.query',
                    '--topics', 'msmarco-passage-dev-subset',
                    '--encoder', 'sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco',
                    '--output', output_path,
                    '--device', 'cpu',
                    '--max-queries', '2',
                ],
                cwd=self.repo_dir,
                check=True,
            )

            encoded = pd.read_pickle(output_path)
            self.assertEqual(encoded.shape, (2, 3))
            self.assertEqual(encoded.columns.tolist(), ['id', 'text', 'embedding'])
            self.assertEqual(len(encoded.iloc[0]['embedding']), 768)
            for i, (first_value, last_value) in enumerate(EXPECTED_VALUES):
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][0], first_value, places=5)
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][-1], last_value, places=5)

    def test_distilbert_tas_b_query_encoder_direct(self):
        encoder = AutoQueryEncoder('sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco', device='cpu')
        query_iterator = DefaultQueryIterator.from_topics('msmarco-passage-dev-subset')
        for i, (_, text) in enumerate(query_iterator):
            if i == 2:
                break
            embedding = encoder.encode(text)
            self.assertEqual(len(embedding), 768)
            self.assertAlmostEqual(embedding[0], EXPECTED_VALUES[i][0], places=5)
            self.assertAlmostEqual(embedding[-1], EXPECTED_VALUES[i][1], places=5)


if __name__ == '__main__':
    unittest.main()

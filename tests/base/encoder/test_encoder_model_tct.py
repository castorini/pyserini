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
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

from pyserini.encode import TctColBertDocumentEncoder, TctColBertQueryEncoder
from pyserini.query_iterator import DefaultQueryIterator


class TestEncodeTctColBert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))
        cls.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    def _assert_encode_query_cli_output(self, topics, encoder, expected_values):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
            subprocess.run(
                [
                    sys.executable, '-m', 'pyserini.encode.query',
                    '--topics', topics,
                    '--encoder', encoder,
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
            self.assertAlmostEqual(encoded.iloc[0]['embedding'][0], expected_values[0][0], places=5)
            self.assertAlmostEqual(encoded.iloc[0]['embedding'][-1], expected_values[0][1], places=5)
            self.assertAlmostEqual(encoded.iloc[1]['embedding'][0], expected_values[1][0], places=5)
            self.assertAlmostEqual(encoded.iloc[1]['embedding'][-1], expected_values[1][1], places=5)

    def _assert_query_encoder_output(self, topics, encoder, expected_values):
        encoder = TctColBertQueryEncoder(encoder, device='cpu')
        query_iterator = DefaultQueryIterator.from_topics(topics)
        for i, (_, text) in enumerate(query_iterator):
            if i == 2:
                break
            embedding = encoder.encode(text)
            self.assertEqual(len(embedding), 768)
            self.assertAlmostEqual(embedding[0], expected_values[i][0], places=5)
            self.assertAlmostEqual(embedding[-1], expected_values[i][1], places=5)

    def test_tct_colbert_encoder(self):
        texts = []
        with open(os.path.join(self.resource_dir, 'simple_cacm_corpus.json')) as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = TctColBertDocumentEncoder('castorini/tct_colbert-msmarco', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.01650, places=5)
        self.assertAlmostEqual(vectors[0][-1], -0.05648, places=5)
        self.assertAlmostEqual(vectors[2][0], -0.10293, places=5)
        self.assertAlmostEqual(vectors[2][-1], 0.05549, places=5)

    def test_msmarco_doc_tct_colbert_encode_query_cli(self):
        self._assert_encode_query_cli_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-msmarco',
            [(0.14085, -0.15662), (-0.14778, 0.10030)]
        )

    def test_msmarco_doc_tct_colbert_query_encoder(self):
        self._assert_query_encoder_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-msmarco',
            [(0.14085, -0.15662), (-0.14778, 0.10030)]
        )

    def test_msmarco_passage_tct_colbert_v2_encode_query_cli(self):
        self._assert_encode_query_cli_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-msmarco',
            [(0.18285, -0.10137), (-0.03068, 0.08468)]
        )

    def test_msmarco_passage_tct_colbert_v2_query_encoder(self):
        self._assert_query_encoder_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-msmarco',
            [(0.18285, -0.10137), (-0.03068, 0.08468)]
        )

    def test_msmarco_passage_tct_colbert_v2_hn_encode_query_cli(self):
        self._assert_encode_query_cli_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-hn-msmarco',
            [(0.15629, -0.09900), (-0.04446, 0.07603)]
        )

    def test_msmarco_passage_tct_colbert_v2_hn_query_encoder(self):
        self._assert_query_encoder_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-hn-msmarco',
            [(0.15629, -0.09900), (-0.04446, 0.07603)]
        )

    def test_msmarco_passage_tct_colbert_v2_hnp_encode_query_cli(self):
        self._assert_encode_query_cli_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-hnp-msmarco',
            [(0.15061, -0.08704), (-0.05862, 0.10783)]
        )

    def test_msmarco_passage_tct_colbert_v2_hnp_query_encoder(self):
        self._assert_query_encoder_output(
            'msmarco-passage-dev-subset',
            'castorini/tct_colbert-v2-hnp-msmarco',
            [(0.15061, -0.08704), (-0.05862, 0.10783)]
        )


if __name__ == '__main__':
    unittest.main()

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

from pyserini.encode import BprQueryEncoder
from pyserini.query_iterator import DefaultQueryIterator


EXPECTED_VALUES = [(-0.25418, 0.13869, -1.0, 1.0), (0.15668, -0.28884, 1.0, -1.0)]
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def assert_bpr_encode_query_cli_output(testcase, topics, encoder, expected_values, embedding_dim=768):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
        subprocess.run(
            [
                sys.executable, '-m', 'pyserini.encode.query',
                '--topics', topics,
                '--encoder', encoder,
                '--bpr',
                '--output', output_path,
                '--device', 'cpu',
                '--max-queries', str(len(expected_values)),
            ],
            cwd=REPO_DIR,
            check=True,
        )

        encoded = pd.read_pickle(output_path)
        testcase.assertEqual(encoded.shape, (len(expected_values), 4))
        testcase.assertEqual(encoded.columns.tolist(), ['id', 'text', 'dense_embedding', 'sparse_embedding'])
        testcase.assertEqual(len(encoded.iloc[0]['dense_embedding']), embedding_dim)
        testcase.assertEqual(len(encoded.iloc[0]['sparse_embedding']), embedding_dim)
        for i, (dense_first, dense_last, sparse_first, sparse_last) in enumerate(expected_values):
            testcase.assertAlmostEqual(encoded.iloc[i]['dense_embedding'][0], dense_first, places=5)
            testcase.assertAlmostEqual(encoded.iloc[i]['dense_embedding'][-1], dense_last, places=5)
            testcase.assertAlmostEqual(encoded.iloc[i]['sparse_embedding'][0], sparse_first, places=5)
            testcase.assertAlmostEqual(encoded.iloc[i]['sparse_embedding'][-1], sparse_last, places=5)


def assert_bpr_query_encoder_output(testcase, topics, encoder, expected_values, embedding_dim=768):
    query_iterator = DefaultQueryIterator.from_topics(topics)
    for i, (_, text) in enumerate(query_iterator):
        if i == len(expected_values):
            break
        embedding = encoder.encode(text)
        testcase.assertEqual(embedding.keys(), {'dense', 'sparse'})
        testcase.assertEqual(len(embedding['dense']), embedding_dim)
        testcase.assertEqual(len(embedding['sparse']), embedding_dim)
        testcase.assertAlmostEqual(embedding['dense'][0], expected_values[i][0], places=5)
        testcase.assertAlmostEqual(embedding['dense'][-1], expected_values[i][1], places=5)
        testcase.assertAlmostEqual(embedding['sparse'][0], expected_values[i][2], places=5)
        testcase.assertAlmostEqual(embedding['sparse'][-1], expected_values[i][3], places=5)


class TestEncodeBpr(unittest.TestCase):
    def test_bpr_encode_query_cli(self):
        assert_bpr_encode_query_cli_output(self, 'dpr-nq-test', 'castorini/bpr-nq-question-encoder', EXPECTED_VALUES)

    def test_bpr_query_encoder_direct(self):
        encoder = BprQueryEncoder('castorini/bpr-nq-question-encoder', device='cpu')
        assert_bpr_query_encoder_output(self, 'dpr-nq-test', encoder, EXPECTED_VALUES)


if __name__ == '__main__':
    unittest.main()

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

import pandas as pd

from pyserini.query_iterator import DefaultQueryIterator


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def assert_encode_query_cli_output(testcase, topics, encoder, expected_values, embedding_dim=768):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
        subprocess.run(
            [
                sys.executable, '-m', 'pyserini.encode.query',
                '--topics', topics,
                '--encoder', encoder,
                '--output', output_path,
                '--device', 'cpu',
                '--max-queries', str(len(expected_values)),
            ],
            cwd=REPO_DIR,
            check=True,
        )

        encoded = pd.read_pickle(output_path)
        testcase.assertEqual(encoded.shape, (len(expected_values), 3))
        testcase.assertEqual(encoded.columns.tolist(), ['id', 'text', 'embedding'])
        testcase.assertEqual(len(encoded.iloc[0]['embedding']), embedding_dim)
        for i, (first_value, last_value, places) in enumerate(expected_values):
            testcase.assertAlmostEqual(encoded.iloc[i]['embedding'][0], first_value, places=places)
            testcase.assertAlmostEqual(encoded.iloc[i]['embedding'][-1], last_value, places=places)


def assert_query_encoder_output(testcase, topics, encoder, expected_values, embedding_dim=768):
    query_iterator = DefaultQueryIterator.from_topics(topics)
    for i, (_, text) in enumerate(query_iterator):
        if i == len(expected_values):
            break
        embedding = encoder.encode(text)
        testcase.assertEqual(len(embedding), embedding_dim)
        first_value, last_value, places = expected_values[i]
        testcase.assertAlmostEqual(embedding[0], first_value, places=places)
        testcase.assertAlmostEqual(embedding[-1], last_value, places=places)

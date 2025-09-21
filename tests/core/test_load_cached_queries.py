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

from pyserini.encode import QueryEncoder


class TestLoadCachedQueries(unittest.TestCase):

    def test_msmarco_v1_and_dl(self):
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-ada2-msmarco-passage-dev-subset'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-ada2-dl19-passage'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-ada2-dl20'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('msmarco-v1-passage.dev.openai-ada2'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl19-passage.openai-ada2'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl20-passage.openai-ada2'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-ada2-dl19-passage-hyde'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-ada2-dl20-hyde'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl19-passage.openai-ada2-hyde'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl20-passage.openai-ada2-hyde'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-text-embedding-3-large-msmarco-passage-dev-subset'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-text-embedding-3-large-dl19-passage'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('openai-text-embedding-3-large-dl20'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('msmarco-v1-passage.dev.openai-text-embedding-3-large'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl19-passage.openai-text-embedding-3-large'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl20-passage.openai-text-embedding-3-large'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('cohere-embed-english-v3.0-msmarco-passage-dev-subset'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('cohere-embed-english-v3.0-dl19-passage'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('cohere-embed-english-v3.0-dl20'))

        self.assertIsNotNone(QueryEncoder.load_encoded_queries('msmarco-v1-passage.dev.cohere-embed-english-v3.0'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl19-passage.cohere-embed-english-v3.0'))
        self.assertIsNotNone(QueryEncoder.load_encoded_queries('dl20-passage.cohere-embed-english-v3.0'))

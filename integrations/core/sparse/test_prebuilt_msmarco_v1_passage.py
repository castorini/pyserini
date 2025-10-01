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

"""Integration tests for MS MARCO V1 passage corpus using prebuilt indexes."""

import unittest

from integrations.core.utils import run_retrieval_and_return_scores


class TestPrebuiltMsMarcoV1Passage(unittest.TestCase):
    def setUp(self):
        self.threads = 16
        self.batch_size = 128

    def test_passage_trec_output(self):
        """Test case for MS MARCO V1 passage, dev queries, TREC output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-passage', 'msmarco-v1-passage-slim', 'msmarco-v1-passage-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-passage.trec.txt',
                f'python -m pyserini.search.lucene \
                    --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-passage-dev-subset --bm25',
                'msmarco-passage-dev-subset',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.1958, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.8573, delta=0.0001)

    def test_passage_msmarco_output(self):
        """Test case for MS MARCO V1 passage, dev queries, MS MARCO output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-passage', 'msmarco-v1-passage-slim', 'msmarco-v1-passage-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-passage.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-passage-dev-subset --bm25 --output-format msmarco',
                'msmarco-passage-dev-subset',
                'msmarco_passage_string', [])

            self.assertTrue('MRR@10' in scores)
            self.assertEqual(scores['MRR@10'], '0.18741227770955546')

    def test_passage_expanded_trec_output(self):
        """Test case for MS MARCO V1 passage w/ doc2query-T5 expansions, dev queries, TREC output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-passage.d2q-t5', 'msmarco-v1-passage.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-passage.expanded.trec.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-passage-dev-subset --bm25',
                'msmarco-passage-dev-subset',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.2893, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9506, delta=0.0001)

    def test_passage_expanded_msmarco_output(self):
        """Test case for MS MARCO V1 passage w/ doc2query-T5 expansions, dev queries, MS MARCO output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-passage.d2q-t5', 'msmarco-v1-passage.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-passage.expanded.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-passage-dev-subset --bm25 --output-format msmarco',
                'msmarco-passage-dev-subset',
                'msmarco_passage_string', [])

            self.assertTrue('MRR@10' in scores)
            self.assertEqual(scores['MRR@10'], '0.281560751807885')


if __name__ == '__main__':
    unittest.main()

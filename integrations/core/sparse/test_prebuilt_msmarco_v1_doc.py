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

"""Integration tests for MS MARCO V1 doc corpora (full and segmented) using pre-built indexes."""

import unittest

from integrations.core.utils import run_retrieval_and_return_scores


class TestPrebuiltMsMarcoV1Doc(unittest.TestCase):
    def setUp(self):
        self.threads = 16
        self.batch_size = 128

    #
    # doc "full" conditions
    #

    def test_doc_full_trec_output(self):
        """Test case for MS MARCO V1 doc (full), dev queries, TREC output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-doc', 'msmarco-v1-doc-slim', 'msmarco-v1-doc-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.trec.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev --bm25 --hits 1000',
                'msmarco-doc-dev',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.2774, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9357, delta=0.0001)

    def test_doc_full_msmarco_output(self):
        """Test case for MS MARCO V1 doc (full), dev queries, MS MARCO output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-doc', 'msmarco-v1-doc-slim', 'msmarco-v1-doc-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev --bm25 --hits 100 --output-format msmarco',
                'msmarco-doc-dev',
                'msmarco_doc_string', [])

            self.assertTrue('MRR@100' in scores)
            self.assertEqual(scores['MRR@100'], '0.2766351807440808')

    #
    # doc segmented conditions
    #

    def test_doc_segmented_trec_output(self):
        """Test case for MS MARCO V1 doc segmented, dev queries, TREC output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-doc-segmented', 'msmarco-v1-doc-segmented-slim', 'msmarco-v1-doc-segmented-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc-segmented.trec.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev --bm25 --hits 10000 --max-passage --max-passage-hits 1000',
                'msmarco-doc-dev',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.2762, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9311, delta=0.0001)

    def test_doc_segmented_msmarco_output(self):
        """Test case for MS MARCO V1 doc segmented, dev queries, MS MARCO output
           on all three prebuilt indexes (base, slim, full)."""

        # Loop over all three prebuilt indexes.
        for index in ['msmarco-v1-doc-segmented', 'msmarco-v1-doc-segmented-slim', 'msmarco-v1-doc-segmented-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc-segmented.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev \
                    --bm25 --hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco',
                'msmarco-doc-dev',
                'msmarco_doc_string', [])

            self.assertTrue('MRR@100' in scores)
            self.assertEqual(scores['MRR@100'], '0.2755196341768384')

    #
    # doc2query conditions
    #

    def test_doc_full_expanded_trec_output(self):
        """Test case for MS MARCO V1 doc (full) + doc2query-T5 expansions, dev queries, TREC output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-doc.d2q-t5', 'msmarco-v1-doc.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.expanded.trec.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev --bm25 --hits 1000',
                'msmarco-doc-dev',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.3273, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9553, delta=0.0001)

    def test_doc_full_expanded_msmarco_output(self):
        """Test case for MS MARCO V1 doc (full) + doc2query-T5 expansions, dev queries, MS MARCO output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-doc.d2q-t5', 'msmarco-v1-doc.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.expanded.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev --bm25 --hits 100 --output-format msmarco',
                'msmarco-doc-dev',
                'msmarco_doc_string', [])

            self.assertTrue('MRR@100' in scores)
            self.assertEqual(scores['MRR@100'], '0.3268656233100833')

    def test_doc_segmented_expanded_trec_output(self):
        """Test case for MS MARCO V1 doc segmented + doc2query-T5 expansions, dev queries, TREC output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-doc-segmented.d2q-t5', 'msmarco-v1-doc-segmented.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc-segmented.expanded.trec.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev \
                    --bm25 --hits 10000 --max-passage --max-passage-hits 1000',
                'msmarco-doc-dev',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'], 0.3213, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9530, delta=0.0001)

    def test_doc_segmented_expanded_msmarco_output(self):
        """Test case for MS MARCO V1 doc segmented + doc2query-T5 expansions, dev queries, MS MARCO output."""

        # Loop over both prebuilt indexes.
        for index in ['msmarco-v1-doc-segmented.d2q-t5', 'msmarco-v1-doc-segmented.d2q-t5-docvectors']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc-segmented.expanded.msmarco.txt',
                f'python -m pyserini.search.lucene --threads {self.threads} --batch-size {self.batch_size} \
                    --index {index} --topics msmarco-doc-dev \
                    --bm25 --hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco',
                'msmarco-doc-dev',
                'msmarco_doc_string', [])

            self.assertTrue('MRR@100' in scores)
            self.assertEqual(scores['MRR@100'], '0.320918438140918')


if __name__ == '__main__':
    unittest.main()

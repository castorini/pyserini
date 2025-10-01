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

"""Integration tests for various newswire collections using prebuilt indexes."""

import unittest

from integrations.core.utils import run_retrieval_and_return_scores


class TestPrebuiltNewswire(unittest.TestCase):

    def test_disk45(self):
        """Test case for disk45 (alias for robust04)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.disk45.bm25.txt',
            'python -m pyserini.search.lucene --topics robust04 --index disk45 --bm25',
            'robust04',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2531, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3102, delta=1e-10)

    def test_robust04(self):
        """Test case for robust04 (alias for disk45)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.robust04.bm25.txt',
            'python -m pyserini.search.lucene --topics robust04 --index robust04 --bm25',
            'robust04',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2531, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3102, delta=1e-10)

    def test_aquaint(self):
        """Test case for aquaint (alias for robust05)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.aquaint.bm25.txt',
            'python -m pyserini.search.lucene --topics robust05 --index aquaint --bm25',
            'robust05',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2032, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3693, delta=1e-10)

    def test_robust05(self):
        """Test case for robust05 (alias for aquaint)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.robust05.bm25.txt',
            'python -m pyserini.search.lucene --topics robust05 --index robust05 --bm25',
            'robust05',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2032, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3693, delta=1e-10)

    def test_nyt(self):
        """Test case for nyt (alias for core17)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.nyt.bm25.txt',
            'python -m pyserini.search.lucene --topics core17 --index nyt --bm25',
            'core17',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2087, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.4293, delta=1e-10)

    def test_core17(self):
        """Test case for core17 (alias for nyt)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.core17.bm25.txt',
            'python -m pyserini.search.lucene --topics core17 --index core17 --bm25',
            'core17',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2087, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.4293, delta=1e-10)

    def test_wapo_v2(self):
        """Test case for wapo.v2 (alias for core18)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.wapo.v2.bm25.txt',
            'python -m pyserini.search.lucene --topics core18 --index wapo.v2 --bm25',
            'core18',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2496, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3573, delta=1e-10)

    def test_core18(self):
        """Test case for core18 (alias for wapo.v2)."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.core18.bm25.txt',
            'python -m pyserini.search.lucene --topics core18 --index core18 --bm25',
            'core18',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2496, delta=1e-10)
        self.assertAlmostEqual(scores['P.30'], 0.3573, delta=1e-10)


if __name__ == '__main__':
    unittest.main()

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

"""Integration tests for Robust04 using pre-built indexes."""

import unittest

from integrations.utils import run_retrieval_and_return_scores


class TestPrebuiltRobust04(unittest.TestCase):
    def test_robust04(self):
        """Test case for Robust04."""

        scores = run_retrieval_and_return_scores(
            'runs/test_run.robust04.bm25.txt',
            'python -m pyserini.search.lucene --topics robust04 --index robust04 --bm25',
            'robust04',
            'trec_eval',
            [['map', 'map'], ['P.30', 'P_30']])

        self.assertTrue('map' in scores)
        self.assertTrue('P.30' in scores)
        self.assertAlmostEqual(scores['map'], 0.2531, delta=0.0001)
        self.assertAlmostEqual(scores['P.30'], 0.3102, delta=0.0001)


if __name__ == '__main__':
    unittest.main()

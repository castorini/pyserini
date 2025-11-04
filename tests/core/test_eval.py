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
import unittest

from pyserini.eval.trec_eval import trec_eval


class TestTrecEval(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith("core"):
            self.root = "../../"
        else:
            self.root = "."

        self.qrels_path = os.path.join(
            self.root, "tools/topics-and-qrels/qrels.covid-round1.txt"
        )
        self.run_path = os.path.join(
            self.root, "tests/resources/simple_trec_run_filter.txt"
        )

    def test_aggeregated_scores(self):
        args = [
            "-c",
            "-m",
            "ndcg_cut.10",
            self.qrels_path,
            self.run_path,
        ]
        self.assertEqual(trec_eval(args), 0.055)

    def test_single_query_score(self):
        args = [
            "-c",
            "-q",
            "-m",
            "ndcg_cut.10",
            self.qrels_path,
            self.run_path,
        ]
        self.assertEqual(trec_eval(args, query_id="1"), 0.2201)

    def test_per_query_unaggeregated_scores(self):
        args = [
            "-c",
            "-q",
            "-m",
            "ndcg_cut.10",
            self.qrels_path,
            self.run_path,
        ]
        expected = {"1": 0.2201, "2": 0.0, "3": 0.0, "4": 0.0, "all": 0.055}
        self.assertDictEqual(trec_eval(args, return_per_query_results=True), expected)

    def test_judged_at_k_scores(self):
        args = [
            "-c",
            "-q",
            "-m",
            "judged.20",
            self.qrels_path,
            self.run_path,
        ]
        self.assertEqual(trec_eval(args), 0.5)

if __name__ == "__main__":
    unittest.main()

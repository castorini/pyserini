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

"""Integration tests for commands in Ma et al. resource paper and Trotman et al. demo paper at SIGIR 2022."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score, parse_score_msmarco


class TestSIGIR2022(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_Ma_etal_section4_1a(self):
        """Sample code in Section 4.1. in Ma et al. resource paper."""

        output_file = 'run.msmarco-passage.expanded.txt'
        self.temp_files.append(output_file)
        run_cmd = f'python -m pyserini.search.lucene \
                      --index msmarco-v1-passage-d2q-t5 \
                      --topics msmarco-passage-dev-subset \
                      --output {output_file} \
                      --output-format msmarco \
                      --bm25'
        status = os.system(run_cmd)
        self.assertEqual(status, 0)

        eval_cmd = f'python -m pyserini.eval.msmarco_passage_eval \
                       msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(eval_cmd)
        score = parse_score_msmarco(stdout, "MRR @10")
        self.assertAlmostEqual(score, 0.2816, delta=0.0001)
        # Note that this is the score with (k1=2.18, b=0.86); score is 0.2723 with default (k1=0.9, b=0.4) parameters.

    def test_Ma_etal_section4_1b(self):
        """Sample code in Section 4.1. in Ma et al. resource paper."""

        output_file = 'run.msmarco-v2-passage.unicoil.txt'
        self.temp_files.append(output_file)
        run_cmd = f'python -m pyserini.search.lucene \
                      --index msmarco-v2-passage-unicoil-0shot \
                      --topics msmarco-v2-passage-dev \
                      --encoder castorini/unicoil-msmarco-passage \
                      --output {output_file} \
                      --batch 144 --threads 36 \
                      --hits 1000 \
                      --impact'
        status = os.system(run_cmd)
        self.assertEqual(status, 0)

        eval_cmd = f'python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-passage-dev {output_file}'
        stdout, stderr = run_command(eval_cmd)
        score = parse_score(stdout, "recip_rank")
        self.assertAlmostEqual(score, 0.1499, delta=0.0001)

    def test_Trotman_etal(self):
        """Sample code in Trotman et al. demo paper."""

        output_file = 'run.msmarco-passage.unicoil.tsv'
        self.temp_files.append(output_file)
        run_cmd = f'python -m pyserini.search.lucene \
                      --index msmarco-passage-unicoil-d2q \
                      --topics msmarco-passage-dev-subset-unicoil \
                      --output {output_file} \
                      --output-format msmarco \
                      --batch 36 --threads 12 \
                      --hits 1000 \
                      --impact'
        status = os.system(run_cmd)
        self.assertEqual(status, 0)

        eval_cmd = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(eval_cmd)
        score = parse_score_msmarco(stdout, "MRR @10", digits=3)
        self.assertAlmostEqual(score, 0.352, delta=0.0005)

        # TODO: There's corresponding test code with JASS that's also in the demo paper. We should also add.

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()

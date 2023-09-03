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

"""Integration tests for commands in Pradeep et al. resource paper at ECIR 2023."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score_qa


class TestECIR2023(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_section5_sub2_first(self):
        """Sample code of the first command in Section 5.2."""
        metrics = ["Top5", "Top20", "Top100"]
        ground_truth = [73.8, 84.27, 89.34]

        output_file = 'runs/run.nq-test.dkrr.trec'
        json_file = 'runs/run.nq-test.dkrr.json'
        self.temp_files.append(output_file)
        self.temp_files.append(json_file)

        # retrieval
        run_cmd = f'python -m pyserini.search.faiss \
                      --index wikipedia-dpr-dkrr-nq \
                      --topics nq-test \
                      --encoder castorini/dkrr-dpr-nq-retriever \
                      --output {output_file} --query-prefix question: \
                      --threads 72 --batch-size 72 \
                      --hits 100'
        status = os.system(run_cmd)
        self.assertEqual(status, 0)

        # conversion
        convert_cmd = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run \
                        --topics nq-test \
                        --index wikipedia-dpr \
                        --input {output_file} \
                        --output {json_file}'
        status = os.system(convert_cmd)
        self.assertEqual(status, 0)

        # evaluation
        eval_cmd = f'python -m pyserini.eval.evaluate_dpr_retrieval \
                       --retrieval {json_file} \
                       --topk 5 20 100'
        stdout, stderr = run_command(eval_cmd)
        
        scores = [] 
        for mt in metrics: 
            scores.append(parse_score_qa(stdout, mt, 4) * 100)

        for score in zip(scores, ground_truth):
            self.assertAlmostEqual(score[0], score[1], delta=0.02)

    def test_section5_sub2_second(self):
        """Sample code of the second command in Section 5.2."""

        cmd_nq = 'python scripts/repro_matrix/run_all_odqa.py --topics nq'
        cmd_tqa = 'python scripts/repro_matrix/run_all_odqa.py --topics nq'

        # run both commands, check if all tests passed (i.e., returned OK)
        stdout_nq, stderr_nq = run_command(cmd_nq)
        self.assertEqual(stdout_nq.count('[OK]'), 21)

        stdout_tqa, stderr_tqa = run_command(cmd_tqa)
        self.assertEqual(stdout_tqa.count('[OK]'), 21)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()


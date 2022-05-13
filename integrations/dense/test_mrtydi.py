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

"""Integration tests for Mr TyDi results using pre-encoded queries."""

import os
import socket
import unittest

from integrations.utils import clean_files, run_command, parse_score, parse_score_qa
from pyserini.search import QueryEncoder
from pyserini.search import get_topics


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 12
        self.batch_size = 36
        self.languages = ['arabic', 'bengali', 'english', 'finnish', 'indonesian', 'japanese', 'korean', 'russian', 'swahili', 'telugu', 'thai']

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_mrtydi_untied_nq(self):
        expected_mrr = [0.291, 0.291, 0.291, 0.205, 0.271, 0.213, 0.235, 0.283, 0.189, 0.111, 0.172]
        assert len(self.languages) == len(expected_mrr), f"Expect same number of languages and scores"

        for lang, expected_score in zip(self.languages, expected_mrr):
            output_file = f'test_run.mrtydi.untied-nq-test.{lang}.trec'
            retrieval_file = f'test_run.mrtydi.untied-nq-test.{lang}.json'
            self.temp_files.extend([output_file, retrieval_file])

            topics = f'mrtydi-v1.1-{lang}-test'
            index = f'mrtydi-v1.1-{lang}-mdpr-nq'
            
            cmd1 = f'python -m pyserini.search.faiss \
                                --topics {topics} \
                                --index {index} \
                                --output {output_file} \
                                --batch-size {self.batch_size} \
                                --threads {self.threads} \
                                --encoder castorini/mdpr-question-nq'
            cmd2 = f'python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m recall.100 mrtydi-v1.1-{lang}-test {output_file}'
 
            status1 = os.system(cmd1)
            stdout, stderr = run_command(cmd2)
            score = parse_score(stdout, 'recip_rank')
 
            self.assertEqual(status1, 0)
            self.assertAlmostEqual(score, expected_score, delta=0.01)

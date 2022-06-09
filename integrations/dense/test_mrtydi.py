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
from posixpath import basename
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

    def test_mrtydi_untied_pft_nq(self):
        expected_mrr = [0.291, 0.291, 0.291, 0.205, 0.271, 0.213, 0.235, 0.283, 0.189, 0.111, 0.172]
        get_index_fn = lambda lang: f'mrtydi-v1.1-{lang}-mdpr-nq'
        self._run_search(expected_mrr, get_index_fn, encoder_name="castorini/mdpr-question-nq")

    def test_mrtydi_tied_pft_nq(self):
        expected_mrr = [0.221, 0.254, 0.243, 0.244, 0.282, 0.206, 0.223, 0.250, 0.262, 0.097, 0.158]
        get_index_fn = lambda lang: f'mrtydi-v1.1-{lang}-mdpr-tied-pft-nq'
        self._run_search(expected_mrr, get_index_fn, encoder_name="castorini/mdpr-tied-pft-nq", encoder_class='auto')

    def test_mrtydi_tied_pft_msmarco(self):
        expected_mrr = [0.441, 0.398, 0.327, 0.275, 0.352, 0.311, 0.282, 0.356, 0.342, 0.310, 0.270]
        get_index_fn = lambda lang: f'mrtydi-v1.1-{lang}-mdpr-tied-pft-msmarco'
        self._run_search(expected_mrr, get_index_fn, encoder_name="castorini/mdpr-tied-pft-msmarco", encoder_class='auto')

    def test_mrtydi_tied_pft_msmarco_ft_all(self):
        expected_mrr = [0.695, 0.623, 0.492, 0.560, 0.579, 0.501, 0.487, 0.517, 0.644, 0.891, 0.617]
        get_index_fn = lambda lang: f'mrtydi-v1.1-{lang}-mdpr-tied-pft-msmarco-ft-all'
        self._run_search(expected_mrr, get_index_fn, encoder_name="castorini/mdpr-tied-pft-msmarco-ft-all", encoder_class='auto')

    def _run_search(self, expected_mrr, get_index_fn, encoder_name, encoder_class=None):
        assert len(self.languages) == len(expected_mrr), f"Expect same number of languages and scores"
        basename = encoder_name.split("/")[-1]

        for lang, expected_score in zip(self.languages, expected_mrr):
            output_file = f'test_run.mrtydi.{basename}.{lang}.trec'
            retrieval_file = f'test_run.mrtydi.{basename}.{lang}.json'
            self.temp_files.extend([output_file, retrieval_file])

            topics = f'mrtydi-v1.1-{lang}-test'
            index = get_index_fn(lang)

            encoder_class_args = f'--encoder-class {encoder_class}' if encoder_class is not None else ''
            cmd1 = f'python -m pyserini.search.faiss {encoder_class_args} \
                                --topics {topics} \
                                --index {index} \
                                --output {output_file} \
                                --batch-size {self.batch_size} \
                                --threads {self.threads} \
                                --encoder {encoder_name}'

            cmd2 = f'python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank -c -m recall.100 mrtydi-v1.1-{lang}-test {output_file}'
 
            status1 = os.system(cmd1)
            stdout, stderr = run_command(cmd2)
            score = parse_score(stdout, 'recip_rank')
 
            self.assertEqual(status1, 0)
            self.assertAlmostEqual(score, expected_score, delta=0.0012)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
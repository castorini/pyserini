#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

"""Integration tests for KILT integration."""

import os
import socket
import unittest
from integrations.utils import clean_files, run_command, parse_score
from pyserini.search import get_topics
from pyserini.dsearch import QueryEncoder


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 12
        self.batch_size = 36

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_kilt_search(self):
        output_file = 'test_run.nq-dev-kilt.jsonl'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics integrations/resources/sample_kilt_topics/nq-dev-kilt.jsonl \
                             --topics-format kilt \
                             --index wikipedia-kilt-doc \
                             --output {output_file} \
                             --output-format kilt'
        status = os.system(cmd1)
        self.assertEqual(status, 0)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()

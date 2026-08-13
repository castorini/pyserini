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
import shlex
import shutil
import sys
import tempfile
import unittest

from integrations.core.lucenesearcher import LuceneSearcherScoreChecker
from integrations.utils import run_command
from pyserini.util import download_url


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        # We assume running in the base directory from the command line.
        # Testcase will *not* run from inside the IDE.
        self.pyserini_root = '.'
        self.tmp = tempfile.mkdtemp(prefix='search-pretokenized-', dir='integrations')
        self.addCleanup(shutil.rmtree, self.tmp, True)

        self.cacm_jsonl_path = os.path.join(self.tmp, 'cacm_jsonl')
        self.cacm_bert_jsonl_path = os.path.join(self.tmp, 'cacm_bert_jsonl')
        os.mkdir(self.cacm_jsonl_path)

        download_url('https://raw.githubusercontent.com/castorini/anserini-data/master/CACM/corpus/jsonl/cacm.json', self.cacm_jsonl_path)

        result = run_command([
            sys.executable, '-m', 'pyserini.tokenize_json_collection',
            '--input', self.cacm_jsonl_path,
            '--output', self.cacm_bert_jsonl_path,
            '--tokenizer', 'bert-base-uncased',
        ])
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        self.pyserini_trec_eval_cmd = shlex.join([sys.executable, '-m', 'pyserini.eval.trec_eval'])

        self.cacm_index_path = os.path.join(self.tmp, 'cacm_index')
        self.cacm_bert_index_path = os.path.join(self.tmp, 'cacm_bert_index')

        index_cmd = [
            sys.executable, '-m', 'pyserini.index',
            '-collection', 'JsonCollection',
            '-generator', 'DefaultLuceneDocumentGenerator',
            '-threads', '9',
            '-input', self.cacm_jsonl_path,
            '-index', self.cacm_index_path,
            '-storePositions', '-storeDocvectors', '-storeRaw',
        ]
        result = run_command(index_cmd)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        pretokenized_index_cmd = [
            sys.executable, '-m', 'pyserini.index',
            '-collection', 'JsonCollection',
            '-generator', 'DefaultLuceneDocumentGenerator',
            '-threads', '9',
            '-input', self.cacm_bert_jsonl_path,
            '-index', self.cacm_bert_index_path,
            '-storePositions', '-storeDocvectors', '-storeRaw', '-pretokenized',
        ]
        result = run_command(pretokenized_index_cmd)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        
        self.cacm_checker = LuceneSearcherScoreChecker(
            index=self.cacm_index_path,
            topics='cacm',
            qrels='cacm',
            eval=f'{self.pyserini_trec_eval_cmd} -m map -m P.30')

        self.cacm_bert_checker = LuceneSearcherScoreChecker(
            index=self.cacm_bert_index_path,
            topics='cacm',
            qrels='cacm',
            eval=f'{self.pyserini_trec_eval_cmd} -m map -m P.30')

    def test_without_pretokenized(self):
        self.assertTrue(self.cacm_checker.run('cacm', '--bm25', 0.3114))

    def test_with_pretokenized(self):
        self.assertTrue(self.cacm_bert_checker.run('cacm_bert', '--bm25', 0.2750, 'bert-base-uncased'))

if __name__ == '__main__':
    unittest.main()

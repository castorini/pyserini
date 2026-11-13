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

import importlib
import shlex
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import yaml

msmarco = importlib.import_module('pyserini.2cr.msmarco')


class TestMsmarco(unittest.TestCase):
    @staticmethod
    def config():
        return yaml.safe_dump({'conditions': [{
            'name': 'bm25',
            'display': 'BM25',
            'command': 'python -m pyserini.search.lucene --topics $topics --output $output',
            'topics': [{
                'display': label,
                'topic_key': 'rag24.test',
                'eval_key': qrels,
                'metric_definitions': {'nDCG@20': '-c -m ndcg_cut.20'},
                'scores': [{'nDCG@20': 0.5}],
            } for label, qrels in (('NIST', 'rag24.test'), ('Umbrela', 'rag24.test-umbrela-all'))],
        }]})

    @staticmethod
    def args(**kwargs):
        values = dict(collection='msmarco-v2.1-doc-segmented', all=True, condition=None,
                      directory='', display_commands=False, dry_run=False, skip_eval=False)
        values.update(kwargs)
        return Namespace(**values)

    def test_cli_accepts_slim_condition(self):
        result = subprocess.run(
            [sys.executable, '-m', 'pyserini.2cr.msmarco', '--collection', 'v2.1-doc',
             '--condition', 'bm25-doc-slim', '--dry-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('bm25-doc-slim', result.stdout)

    def test_shared_run_is_retrieved_once_and_evaluated_against_both_qrels(self):
        def write_run(command, **kwargs):
            tokens = shlex.split(command)
            Path(tokens[tokens.index('--output') + 1]).touch()

        with tempfile.TemporaryDirectory() as directory, redirect_stdout(StringIO()), \
                patch.object(msmarco, 'read_file', return_value=self.config()), \
                patch.object(msmarco, 'run_command', side_effect=write_run) as retrieve, \
                patch.object(msmarco, 'run_eval_and_return_metric', return_value=0.5) as evaluate:
            msmarco.run_conditions(self.args(directory=directory))
        retrieve.assert_called_once()
        calls = evaluate.call_args_list
        self.assertEqual([call.args[1] for call in calls], ['rag24.test', 'rag24.test-umbrela-all'])
        self.assertEqual(calls[0].args[3], calls[1].args[3])

    def test_dry_run_and_skip_eval_control_execution(self):
        for dry_run, skip_eval in ((True, False), (True, True), (False, True)):
            for existing_run in (False, True):
                with self.subTest(dry_run=dry_run, skip_eval=skip_eval, existing_run=existing_run):
                    # One evaluation is sufficient to check execution flags.
                    config = yaml.safe_load(self.config())
                    config['conditions'][0]['topics'] = config['conditions'][0]['topics'][:1]
                    output = StringIO()
                    with tempfile.TemporaryDirectory() as directory, redirect_stdout(output), \
                            patch.object(msmarco, 'read_file', return_value=yaml.safe_dump(config)), \
                            patch.object(msmarco.os.path, 'exists', return_value=existing_run), \
                            patch.object(msmarco, 'run_command') as retrieve, \
                            patch.object(msmarco, 'run_eval_and_return_metric') as evaluate:
                        msmarco.run_conditions(self.args(directory=directory, dry_run=dry_run, skip_eval=skip_eval))
                    evaluate.assert_not_called()
                    if dry_run or existing_run:
                        retrieve.assert_not_called()
                    else:
                        retrieve.assert_called_once()
                    if dry_run:
                        self.assertIn('0.5000', output.getvalue())


if __name__ == '__main__':
    unittest.main()

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

import argparse
import contextlib
import html
import importlib
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from pyserini.util import run_command

bright = importlib.import_module('pyserini.2cr.bright')
base = importlib.import_module('pyserini.2cr._base')


class TestBrightCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conditions = yaml.safe_load(bright.read_file('bright.yaml'))['conditions']

    def capture_shell_args(self, command):
        # Execute only an argv-printing stub, never the retrieval command.
        stub = shlex.join([sys.executable, '-c', 'import json, sys; print(json.dumps(sys.argv[1:]))'])
        return json.loads(subprocess.run(
            ['/bin/sh', '-c', stub + ' ' + command], check=True,
            capture_output=True, text=True
        ).stdout)

    def test_prefixes_and_paths_reach_subprocess_unchanged(self):
        for condition in self.conditions:
            for dataset in condition['datasets']:
                with self.subTest(condition=condition['name'], dataset=dataset['dataset']):
                    output = '/tmp/bright results/it\'s "$output"; run.txt'
                    argv = bright.build_run_command(condition, dataset, output)
                    self.assertEqual(argv[argv.index('--output') + 1], output)
                    if condition['name'] == 'diver-retriever-4b':
                        expected = ('Instruct: Given a web search query, retrieve relevant passages '
                                    'that answer the query\nQuery:')
                    elif condition['name'] == 'reason-embed-qwen3-4b-0928':
                        expected = f"Instruct: {dataset['query_prefix']}\nQuery: "
                    else:
                        self.assertNotIn('--query-prefix', argv)
                        continue
                    self.assertEqual(argv.count('--query-prefix'), 1)
                    self.assertEqual(argv[argv.index('--query-prefix') + 1], expected)
                    result = run_command([
                        sys.executable, '-c', 'import json, sys; print(json.dumps(sys.argv[1:]))', *argv
                    ], check=True)
                    self.assertEqual(json.loads(result.stdout), argv)

    def test_rendered_commands_preserve_arguments(self):
        for condition in self.conditions:
            with self.subTest(condition=condition['name']):
                dataset = dict(condition['datasets'][0], query_prefix='A "quote", $value, \'apostrophe\', --topics <tag>')
                argv = bright.build_run_command(condition, dataset, '/tmp/a b/--index <run>.txt')
                self.assertEqual(self.capture_shell_args(bright.format_run_command(argv)), argv)

    def test_report_commands_match_builder_and_preserve_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'report.html'
            run_directory = '/tmp/bright results/it\'s <a&b>'
            bright.generate_report(argparse.Namespace(directory=run_directory, output=output))
            report = output.read_text()
            commands = [html.unescape(cmd).strip() for cmd in re.findall(
                r'<pre><code>(.*?)</code></pre>', report, re.DOTALL
            )]
            for condition in self.conditions:
                dataset = condition['datasets'][0]
                runfile = os.path.join(run_directory, f"run.bright.{condition['name']}.{dataset['dataset']}.txt")
                argv = bright.build_run_command(condition, dataset, runfile)
                self.assertIn(bright.format_run_command(argv), commands)
                self.assertIn(html.escape(bright.format_run_command(argv)), report)
            evaluation = next(cmd for cmd in commands if cmd.startswith('python -m pyserini.eval.trec_eval'))
            for command in evaluation.split('\n\n'):
                self.assertTrue(self.capture_shell_args(command)[-1].startswith(run_directory + '/'))

    def test_dry_run_and_execution(self):
        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run), tempfile.TemporaryDirectory() as directory:
                args = argparse.Namespace(
                    all=False, condition='diver-retriever-4b', dataset='biology',
                    directory=directory, display_commands=True, dry_run=dry_run, skip_eval=True
                )
                with patch.object(bright, 'run_command') as runner, contextlib.redirect_stdout(io.StringIO()):
                    bright.run_conditions(args)
                if dry_run:
                    runner.assert_not_called()
                else:
                    condition = next(c for c in self.conditions if c['name'] == args.condition)
                    dataset = next(d for d in condition['datasets'] if d['dataset'] == args.dataset)
                    runfile = os.path.join(directory, f'run.bright.{args.condition}.{args.dataset}.txt')
                    runner.assert_called_once_with(
                        bright.build_run_command(condition, dataset, runfile), capture_output=False
                    )

    def test_shared_eval_formatter_supports_strings_and_argv(self):
        command = 'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 bright-biology run.txt'
        self.assertEqual(
            self.capture_shell_args(base.format_eval_command(command)), shlex.split(command)
        )
        argv = shlex.split(command)
        argv[-1] = "/tmp/bright results/it's <run>.txt"
        self.assertEqual(self.capture_shell_args(base.format_eval_command(argv)), argv)
        self.assertIs(bright.format_eval_command, base.format_eval_command)
        self.assertIs(bright.read_file, base.read_file)

    def test_evaluation_preserves_runfile_argument(self):
        runfile = '/tmp/bright results/it\'s <run>.txt'
        stdout = io.StringIO()
        with patch.object(base, 'run_command') as runner, contextlib.redirect_stdout(stdout):
            runner.return_value.stdout = 'ndcg_cut_10\tall\t0.4247\n'
            score = base.run_eval_and_return_metric(
                'nDCG@10', 'bright-biology', '-c -m ndcg_cut.10', runfile, display_command=True
            )
        expected = ['python', '-m', 'pyserini.eval.trec_eval', '-c', '-m', 'ndcg_cut.10', 'bright-biology', runfile]
        runner.assert_called_once_with(expected)
        self.assertEqual(score, 0.4247)
        self.assertIn(shlex.join(expected), stdout.getvalue())


if __name__ == '__main__':
    unittest.main()

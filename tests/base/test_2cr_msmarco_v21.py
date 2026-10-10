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
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from html import unescape
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import yaml

msmarco = importlib.import_module('pyserini.2cr.msmarco')


class TestMsmarcoV21(unittest.TestCase):
    collections = ('msmarco-v2.1-doc', 'msmarco-v2.1-doc-segmented')

    @staticmethod
    def config(collection):
        return yaml.safe_load(msmarco.read_file(f'{collection}.yaml'))['conditions']

    @staticmethod
    def args(collection, **kwargs):
        values = dict(collection=collection, all=True, condition=None, directory='',
                      display_commands=False, dry_run=False, skip_eval=False)
        values.update(kwargs)
        return Namespace(**values)

    def test_complete_condition_and_evaluation_coverage(self):
        for collection, condition_count, pairing_count, metric_count in zip(
                self.collections, (4, 13), (24, 52), (88, 156)):
            conditions = self.config(collection)
            self.assertEqual(len(conditions), condition_count)
            self.assertEqual([c['name'] for c in conditions], msmarco.models[collection])
            self.assertEqual(sum(len(c['topics']) for c in conditions), pairing_count)
            self.assertEqual(sum(len(s) for c in conditions for t in c['topics'] for s in t['scores']),
                             metric_count)
            for condition in conditions:
                for topic in condition['topics']:
                    self.assertEqual(set(topic['metric_definitions']), set(topic['scores'][0]))

    def test_document_aggregation_and_dense_search_settings(self):
        for collection in self.collections:
            for condition in self.config(collection):
                _, command = msmarco.get_run_command(collection, condition, condition['topics'][0])
                tokens = shlex.split(command)
                name = condition['name']
                aggregate = collection == 'msmarco-v2.1-doc' and 'segmented' in name
                self.assertEqual('--max-passage' in tokens, aggregate)
                if aggregate:
                    self.assertEqual(tokens[tokens.index('--hits') + 1], '10000')
                    self.assertEqual(tokens[tokens.index('--max-passage-hits') + 1], '1000')
                    self.assertEqual(tokens[tokens.index('--max-passage-delimiter') + 1], '#')
                if name.startswith('shard'):
                    self.assertIn('--dense', tokens)
                    self.assertIn('--hnsw', tokens)
                    self.assertEqual(tokens[tokens.index('--onnx-encoder') + 1], 'ArcticEmbedL')
                    self.assertEqual(tokens[tokens.index('--ef-search') + 1], '1000')
                    self.assertEqual(tokens[tokens.index('--hits') + 1], '250')
                elif name == 'splade-v3.onnx':
                    self.assertIn('--impact', tokens)
                    self.assertIn('--pretokenized', tokens)
                    self.assertIn('--remove-query', tokens)
                    self.assertEqual(tokens[tokens.index('--onnx-encoder') + 1], 'SpladeV3')

    def test_all_scores_are_evaluated_and_shared_runs_are_reused(self):
        for collection, run_count, metric_count in zip(self.collections, (24, 26), (88, 156)):
            with self.subTest(collection=collection), tempfile.TemporaryDirectory(prefix='2cr runs ') as directory:
                expected_calls = []
                for condition in self.config(collection):
                    for topic in condition['topics']:
                        runfile, _ = msmarco.get_run_command(collection, condition, topic, directory)
                        for scores in topic['scores']:
                            expected_calls.extend((metric, topic['eval_key'], topic['metric_definitions'][metric],
                                                   shlex.quote(runfile)) for metric in scores)

                def write_run(command, **kwargs):
                    tokens = shlex.split(command)
                    Path(tokens[tokens.index('--output') + 1]).touch()

                output = StringIO()
                with redirect_stdout(output), patch.object(msmarco, 'run_command', side_effect=write_run) as run, \
                        patch.object(msmarco, 'run_eval_and_return_metric', return_value=0.5) as evaluate:
                    msmarco.run_conditions(self.args(collection, directory=directory))
                self.assertEqual(run.call_count, run_count)
                self.assertEqual(evaluate.call_count, metric_count)
                self.assertEqual([call.args for call in evaluate.call_args_list], expected_calls)
                if collection.endswith('-segmented'):
                    for key in ('rag24.test-umbrela-all', 'rag24.test', 'rag25.test-umbrela2', 'rag25.test'):
                        self.assertIn(f'/ {key}:', output.getvalue())

    def test_dry_run_does_not_search_or_evaluate_existing_runs(self):
        for collection, metric_count in zip(self.collections, (88, 156)):
            output = StringIO()
            with redirect_stdout(output), patch.object(msmarco.os.path, 'exists', return_value=True), \
                    patch.object(msmarco, 'run_command') as run, \
                    patch.object(msmarco, 'run_eval_and_return_metric') as evaluate:
                msmarco.run_conditions(self.args(collection, dry_run=True, display_commands=True))
            run.assert_not_called()
            evaluate.assert_not_called()
            self.assertEqual(output.getvalue().count('python -m pyserini.eval.trec_eval'), metric_count)
            self.assertNotIn('Observed scores:', output.getvalue())

    def test_single_condition_and_skip_eval(self):
        output = StringIO()
        collection = self.collections[1]
        with redirect_stdout(output), patch.object(msmarco.os.path, 'exists', return_value=True), \
                patch.object(msmarco, 'run_eval_and_return_metric') as evaluate:
            msmarco.run_conditions(self.args(collection, all=False, condition='splade-v3.onnx',
                                             dry_run=True, skip_eval=True))
        evaluate.assert_not_called()
        self.assertEqual(output.getvalue().count('# Running condition'), 1)
        self.assertIn('Reference scores (evaluation skipped):', output.getvalue())
        self.assertIn('nDCG@20: 0.5167', output.getvalue())
        self.assertIn('nDCG@20: 0.4642', output.getvalue())

    def test_reports_include_all_metrics_and_commands(self):
        for collection, metric_count in zip(self.collections, (88, 156)):
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'report.html'
                msmarco.generate_report(self.args(collection, output=output))
                report = unescape(output.read_text())
            self.assertEqual(report.count('python -m pyserini.eval.trec_eval'), metric_count)
            self.assertNotIn('${', report)
            for condition in self.config(collection):
                self.assertIn(condition['name'], report)
                for topic in condition['topics']:
                    runfile, _ = msmarco.get_run_command(collection, condition, topic)
                    for scores in topic['scores']:
                        for metric, expected in scores.items():
                            self.assertIn(f'<td>{expected:.4f}</td>', report)
                            self.assertIn(f"{topic['metric_definitions'][metric]} {topic['eval_key']} {runfile}", report)


if __name__ == '__main__':
    unittest.main()

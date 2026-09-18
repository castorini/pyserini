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
import math
import unittest
from argparse import Namespace
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from unittest.mock import patch

import yaml

base = importlib.import_module('pyserini.2cr._base')
ReproductionStatus = base.ReproductionStatus


class TestScoreClassification(unittest.TestCase):
    def test_equality_and_floating_point_differences(self):
        for observed, expected in [(0.0, 0.0), (1.0, 1.0), (0.3, 0.1 + 0.2), (0.5 + 5e-10, 0.5), (0.5 - 5e-10, 0.5)]:
            with self.subTest(observed=observed, expected=expected):
                self.assertIs(base.compare_reproduction_score(observed, expected), ReproductionStatus.OK)

    def test_inclusive_numerical_boundary(self):
        # Subtraction from zero isolates the exact boundary from cancellation.
        for delta, status in [
            (math.nextafter(1e-9, 0.0), ReproductionStatus.OK),
            (1e-9, ReproductionStatus.OK),
            (math.nextafter(1e-9, math.inf), ReproductionStatus.OKISH),
        ]:
            with self.subTest(delta=delta):
                self.assertIs(base.compare_reproduction_score(0.0, delta), status)
                self.assertIs(base.compare_reproduction_score(delta, 0.0), status)

    def test_improvements_and_regressions(self):
        for observed, expected, status in [
            (0.5001, 0.5, ReproductionStatus.OKISH),
            (0.9, 0.5, ReproductionStatus.OKISH),
            (0.4999, 0.5, ReproductionStatus.OKISH),
            (0.4997, 0.5, ReproductionStatus.FAIL),
            (0.1, 0.5, ReproductionStatus.FAIL),
        ]:
            with self.subTest(observed=observed, expected=expected):
                self.assertIs(base.compare_reproduction_score(observed, expected), status)

    def test_strict_okish_boundary(self):
        for delta, status in [
            (math.nextafter(0.0002, 0.0), ReproductionStatus.OKISH),
            (0.0002, ReproductionStatus.FAIL),
            (math.nextafter(0.0002, math.inf), ReproductionStatus.FAIL),
        ]:
            with self.subTest(delta=delta):
                self.assertIs(base.compare_reproduction_score(0.0, delta), status)
                # Improvements remain OKish even at or above the threshold.
                self.assertIs(base.compare_reproduction_score(delta, 0.0), ReproductionStatus.OKISH)

    def test_normalized_percentage_scores(self):
        for observed, expected, status in [
            (50.0, 50.0, ReproductionStatus.OK),
            (0.0, 1e-7, ReproductionStatus.OK),
            (0.0, 1.1e-7, ReproductionStatus.OKISH),
            (0.0, 0.0199, ReproductionStatus.OKISH),
            (0.0, 0.02, ReproductionStatus.FAIL),
            (0.0, 0.0201, ReproductionStatus.FAIL),
            (50.0, 50.01, ReproductionStatus.OKISH),
            (50.0, 50.03, ReproductionStatus.FAIL),
            (60.0, 50.0, ReproductionStatus.OKISH),
        ]:
            with self.subTest(observed=observed, expected=expected):
                self.assertIs(base.compare_reproduction_score(observed / 100, expected / 100), status)


class TestRunnerScoreClassification(unittest.TestCase):
    def test_all_runners_classify_and_display_scores(self):
        runners = ['atomic', 'beir', 'bright', 'ciral', 'dse', 'm_beir', 'miracl', 'mmeb', 'mrtydi', 'msmarco', 'odqa']
        args = Namespace(all=True, condition=None, directory='unused', display_commands=False,
                         dry_run=False, skip_eval=False, full_topk=False, collection='msmarco-v1-passage',
                         language=None, dataset=None, model=None)
        for name in runners:
            runner = importlib.import_module(f'pyserini.2cr.{name}')
            percentage = name in ('dse', 'odqa')
            filename = {'msmarco': 'msmarco-v1-passage', 'odqa': 'odqa_nq'}.get(name, name)
            config = yaml.safe_load(base.read_file(f'{filename}.yaml'))
            cases = [(0.5, base.ok_str), (0.5001, base.okish_str), (0.5003, base.fail_str), (0.4, base.okish_str)]
            for expected, label in cases:
                with self.subTest(runner=name, expected=expected):
                    self.set_scores(config, expected * 100 if percentage else expected)
                    output = StringIO()
                    with ExitStack() as stack:
                        stack.enter_context(redirect_stdout(output))
                        stack.enter_context(patch.object(runner.yaml, 'safe_load', return_value=config))
                        stack.enter_context(patch.object(runner.os.path, 'exists', return_value=True))
                        command = stack.enter_context(patch.object(runner.os, 'system') if name == 'bright'
                                                      else patch.object(runner, 'run_command'))
                        command.return_value.stdout = 'Top-k Accuracy: 0.5\n'
                        comparison = stack.enter_context(
                            patch.object(runner, 'compare_reproduction_score', wraps=base.compare_reproduction_score)
                        )
                        if name == 'odqa':
                            stack.enter_context(patch.object(
                                runner, 'run_dpr_retrieval_eval_and_return_metric',
                                return_value={f'Top{k}': 50.0 for k in (5, 20, 100, 500, 1000)}
                            ))
                            runner.run_topic_conditions(args, *runner.topic_configs()[1])
                        else:
                            stack.enter_context(patch.object(runner, 'run_eval_and_return_metric', return_value=0.5))
                            runner.run_conditions(args)
                    self.assertGreater(comparison.call_count, 0)
                    self.assertEqual(output.getvalue().count(label), comparison.call_count)
                    for call in comparison.call_args_list:
                        self.assertEqual(len(call.args), 2)
                        self.assertEqual(call.args[0], 0.5)
                        self.assertAlmostEqual(call.args[1], expected)
                        self.assertEqual(call.kwargs, {})
                    if name != 'dse':
                        command.assert_not_called()
                    displayed = '50.00' if percentage else '0.5000'
                    self.assertIn(f'{displayed} {label}', output.getvalue())
                    if label == base.ok_str:
                        self.assertNotIn(' expected ', output.getvalue())
                    else:
                        precision = 1 if name == 'dse' else 4
                        expected_display = expected * 100 if percentage else expected
                        self.assertIn(f'{label} expected {expected_display:.{precision}f}', output.getvalue())

    @classmethod
    def set_scores(cls, node, value):
        if isinstance(node, dict):
            for key, child in node.items():
                if key == 'scores':
                    for scores in child:
                        for metric in scores:
                            scores[metric] = value
                else:
                    cls.set_scores(child, value)
        elif isinstance(node, list):
            for child in node:
                cls.set_scores(child, value)


if __name__ == '__main__':
    unittest.main()

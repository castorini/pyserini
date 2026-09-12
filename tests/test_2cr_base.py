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


base = importlib.import_module('pyserini.2cr._base')


class TestScoreClassification(unittest.TestCase):
    def test_equality_and_floating_point_noise_are_ok(self):
        self.assertEqual(base.ScoreStatus.OK, base.classify_score(0.3123, 0.3123))
        self.assertEqual(base.ScoreStatus.OK, base.classify_score(0.1 + 0.2, 0.3))
        self.assertEqual(
            base.ScoreStatus.OK,
            base.classify_score(base.NUMERICAL_TOLERANCE, 0.0)
        )

    def test_improvement_is_okish(self):
        self.assertEqual(base.ScoreStatus.OKISH, base.classify_score(0.6, 0.5))

    def test_small_regression_and_strict_boundary(self):
        self.assertEqual(
            base.ScoreStatus.OKISH,
            base.classify_score(0.0, math.nextafter(base.OKISH_TOLERANCE, 0.0))
        )
        self.assertEqual(
            base.ScoreStatus.FAIL,
            base.classify_score(0.0, base.OKISH_TOLERANCE)
        )
        self.assertEqual(
            base.ScoreStatus.FAIL,
            base.classify_score(0.0, math.nextafter(base.OKISH_TOLERANCE, math.inf))
        )

    def test_fractional_and_percentage_inputs_are_equivalent(self):
        cases = [
            (0.5, 0.5),
            (0.6, 0.5),
            (0.4999, 0.5),
            (0.4997, 0.5),
        ]
        for observed, expected in cases:
            with self.subTest(observed=observed, expected=expected):
                fractional = base.classify_score(observed, expected)
                percentage = base.classify_score(
                    observed * 100,
                    expected * 100,
                    percentage=True
                )
                self.assertEqual(fractional, percentage)


if __name__ == '__main__':
    unittest.main()

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

import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from pyserini.server.admission import GlobalRequestLimiter


class TestGlobalRequestLimiter(unittest.TestCase):
    def test_rolling_window_and_exact_boundary(self):
        limiter = GlobalRequestLimiter(2)
        with patch('pyserini.server.admission.monotonic') as clock:
            clock.return_value = 100.0
            self.assertEqual(limiter.retry_after(), 0)
            clock.return_value = 100.75
            self.assertEqual(limiter.retry_after(), 0)
            clock.return_value = 100.999
            self.assertEqual(limiter.retry_after(), 1)
            clock.return_value = 101.0
            self.assertEqual(limiter.retry_after(), 0)
            self.assertEqual(limiter.retry_after(), 1)
            clock.return_value = 101.75
            self.assertEqual(limiter.retry_after(), 0)

    def test_wall_clock_second_boundary_does_not_reset_window(self):
        limiter = GlobalRequestLimiter(1)
        with patch('pyserini.server.admission.monotonic', side_effect=[100.9, 101.1, 101.9]):
            self.assertEqual([limiter.retry_after() for _ in range(3)], [0, 1, 0])

    def test_rejected_requests_do_not_extend_window_or_grow_state(self):
        limiter = GlobalRequestLimiter(1)
        with patch('pyserini.server.admission.monotonic') as clock:
            clock.return_value = 100.0
            self.assertEqual(limiter.retry_after(), 0)
            for i in range(1, 1000):
                clock.return_value = 100.0 + i / 1000
                self.assertEqual(limiter.retry_after(), 1)
            self.assertEqual(len(limiter._admitted), 1)
            clock.return_value = 101.0
            self.assertEqual(limiter.retry_after(), 0)

    def test_idle_window_expires_all_slots(self):
        limiter = GlobalRequestLimiter(3)
        with patch('pyserini.server.admission.monotonic') as clock:
            clock.return_value = 10.0
            self.assertEqual([limiter.retry_after() for _ in range(4)], [0, 0, 0, 1])
            clock.return_value = 10000.0
            self.assertEqual([limiter.retry_after() for _ in range(4)], [0, 0, 0, 1])

    def test_concurrent_requests_cannot_exceed_limit(self):
        limiter = GlobalRequestLimiter(30)
        with patch('pyserini.server.admission.monotonic', return_value=100.0):
            with ThreadPoolExecutor(max_workers=32) as executor:
                outcomes = list(executor.map(lambda _: limiter.retry_after(), range(200)))
        self.assertEqual(outcomes.count(0), 30)
        self.assertEqual(outcomes.count(1), 170)
        self.assertEqual(len(limiter._admitted), 30)

    def test_instances_have_independent_budgets(self):
        with patch('pyserini.server.admission.monotonic', return_value=100.0):
            first, second = GlobalRequestLimiter(1), GlobalRequestLimiter(1)
            self.assertEqual([first.retry_after(), first.retry_after(), second.retry_after()], [0, 1, 0])

    def test_clock_is_sampled_while_holding_lock(self):
        limiter = GlobalRequestLimiter(1)

        def clock():
            self.assertTrue(limiter._lock.locked())
            return 100.0

        with patch('pyserini.server.admission.monotonic', side_effect=clock):
            self.assertEqual(limiter.retry_after(), 0)
            self.assertEqual(limiter.retry_after(), 1)

    def test_invalid_limits(self):
        for limit in (None, 0, -1, 1.5, float('inf'), '3', True, False):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, 'positive integer'):
                GlobalRequestLimiter(limit)


if __name__ == '__main__':
    unittest.main()

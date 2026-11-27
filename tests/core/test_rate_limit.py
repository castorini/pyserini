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

from pyserini.server.rate_limit import TokenRequestLimiter


class TestTokenRequestLimiter(unittest.TestCase):
    def test_hard_cap_and_independent_tokens(self):
        limiter = TokenRequestLimiter(3)
        self.assertEqual([limiter.retry_after('one', 100) for _ in range(3)], [0, 0, 0])
        self.assertEqual(limiter.retry_after('one', 100), 60)
        self.assertEqual(limiter.retry_after('two', 100), 0)

    def test_rolling_window_and_retry_after(self):
        limiter = TokenRequestLimiter(2)
        self.assertEqual(limiter.retry_after('key', 100), 0)
        self.assertEqual(limiter.retry_after('key', 110), 0)
        self.assertEqual(limiter.retry_after('key', 159.5), 1)
        self.assertEqual(limiter.retry_after('key', 160), 0)
        self.assertEqual(limiter.retry_after('key', 160), 10)

    def test_wall_clock_minute_boundary_does_not_reset_quota(self):
        limiter = TokenRequestLimiter(1)
        self.assertEqual(limiter.retry_after('key', 59.9), 0)
        self.assertEqual(limiter.retry_after('key', 60.1), 60)

    def test_rejected_requests_do_not_extend_block(self):
        limiter = TokenRequestLimiter(1)
        limiter.retry_after('key', 100)
        for now in range(101, 160):
            self.assertGreater(limiter.retry_after('key', now), 0)
        self.assertEqual(limiter.retry_after('key', 160), 0)

    def test_expired_tokens_are_removed(self):
        limiter = TokenRequestLimiter(1)
        limiter.retry_after('old', 100)
        limiter.retry_after('new', 160)
        self.assertNotIn('old', limiter._by_key)

    def test_concurrent_requests_cannot_exceed_limit(self):
        limiter = TokenRequestLimiter(30)
        with ThreadPoolExecutor(max_workers=32) as executor:
            outcomes = list(executor.map(lambda _: limiter.retry_after('key', 100), range(200)))
        self.assertEqual(outcomes.count(0), 30)
        self.assertEqual(outcomes.count(60), 170)

    def test_invalid_limits(self):
        for limit in (0, -1, 2.5, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                TokenRequestLimiter(limit)


if __name__ == '__main__':
    unittest.main()

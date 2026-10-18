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

"""Thread-safe request quotas shared by all routes for an API token."""

from __future__ import annotations

import math
import threading
from collections import deque

DEFAULT_REQUESTS_PER_MINUTE = 30
REQUEST_WINDOW_SECONDS = 60


class TokenRequestLimiter:
    """Admit at most the configured number of requests in any rolling minute."""

    def __init__(self, requests_per_minute: int = DEFAULT_REQUESTS_PER_MINUTE) -> None:
        if isinstance(requests_per_minute, bool) or not isinstance(requests_per_minute, int) or requests_per_minute <= 0:
            raise ValueError('requests_per_minute must be a positive integer')
        self.requests_per_minute = requests_per_minute
        self._lock = threading.Lock()
        self._requests: deque[tuple[float, str]] = deque()
        self._by_key: dict[str, deque[float]] = {}

    def retry_after(self, key_id: str, now: float) -> int:
        """Reserve a request, or return seconds until this token may try again."""
        with self._lock:
            cutoff = now - REQUEST_WINDOW_SECONDS
            while self._requests and self._requests[0][0] <= cutoff:
                _, expired_key = self._requests.popleft()
                timestamps = self._by_key[expired_key]
                timestamps.popleft()
                if not timestamps:
                    del self._by_key[expired_key]

            timestamps = self._by_key.get(key_id)
            if timestamps is not None and len(timestamps) >= self.requests_per_minute:
                return max(1, math.ceil(timestamps[0] + REQUEST_WINDOW_SECONDS - now))
            if timestamps is None:
                timestamps = self._by_key[key_id] = deque()
            timestamps.append(now)
            self._requests.append((now, key_id))
            return 0

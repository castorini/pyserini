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

"""Process-local admission budget shared by all authenticated REST clients."""

import math
import threading
from collections import deque
from time import monotonic


class GlobalRequestLimiter:
    """Admit at most ``requests_per_second`` requests in any rolling second.

    An admitted request consumes a slot regardless of its eventual response.
    Rejected requests do not extend the window. State is bounded by the limit,
    independent of the number of API keys; it is not shared across processes.
    """

    def __init__(self, requests_per_second: int) -> None:
        if type(requests_per_second) is not int or requests_per_second <= 0:
            raise ValueError('global_requests_per_second must be a positive integer')
        self._limit = requests_per_second
        self._admitted: deque[float] = deque()
        self._lock = threading.Lock()

    def retry_after(self) -> int:
        """Reserve one slot, or return seconds to wait without reserving one."""
        with self._lock:
            # Read the clock inside the lock so concurrent callers cannot append
            # timestamps out of order. Wall-clock corrections must not reset quotas.
            now = monotonic()
            while self._admitted and self._admitted[0] <= now - 1.0:
                self._admitted.popleft()
            if len(self._admitted) >= self._limit:
                return max(1, math.ceil(self._admitted[0] + 1.0 - now))
            self._admitted.append(now)
            return 0

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

"""Deprecated. The package ``pyserini.hsearch` has been renamed `pyserini.search.hybrid`. Stubs are retained here for
redirection purpose to ensure that code in existing published papers remain function (with warnings)."""

import os
import sys

from pyserini.search.hybrid import HybridSearcher as NewHybridSearcher

__all__ = ['HybridSearcher']


class HybridSearcher(NewHybridSearcher):
    def __new__(cls, *args, **kwargs):
        print('pyserini.hsearch.HybridSearcher class has been deprecated, '
              'please use HybridSearcher from pyserini.search.hybrid instead')
        return super().__new__(cls)


if __name__ == "__main__":
    print('WARNING: pyserini.hsearch is deprecated, please use pyserini.search.hybrid instead')
    args = " ".join(sys.argv[1:])
    os.system(f'python -m pyserini.search.hybrid {args}')

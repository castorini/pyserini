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

import logging
from typing import List

from jnius import cast

from pyserini.pyclass import autoclass

logger = logging.getLogger(__name__)

# Wrappers around Anserini classes
JHnswDenseSearcher = autoclass('io.anserini.search.HnswDenseSearcher')
JHnswDenseSearcherArgs = autoclass('io.anserini.search.HnswDenseSearcher$Args')
JScoredDoc = autoclass('io.anserini.search.ScoredDoc')


class LuceneHnswDenseSearcher:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir

        args = JHnswDenseSearcherArgs()
        args.index = index_dir
        self.searcher = JHnswDenseSearcher(args)

    @staticmethod
    def _string_to_comparable(string: str):
        return cast('java.lang.Comparable', autoclass('java.lang.String')(string))

    def search(self, q: str, k: int = 10) -> List[JScoredDoc]:
        return self.searcher.search(self._string_to_comparable('dummy'), q, k)

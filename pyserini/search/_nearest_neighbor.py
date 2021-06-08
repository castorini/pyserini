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

"""
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import List

from ..pyclass import autoclass, JString

logger = logging.getLogger(__name__)


# Wrappers around Anserini classes
JSimpleNearestNeighborSearcher = autoclass('io.anserini.search.SimpleNearestNeighborSearcher')
JSimpleNearestNeighborSearcherResult = autoclass('io.anserini.search.SimpleNearestNeighborSearcher$Result')


class SimpleNearestNeighborSearcher:

    def __init__(self, index_dir: str):
        self.object = JSimpleNearestNeighborSearcher(JString(index_dir))

    def search(self, q: str, k=10) -> List[JSimpleNearestNeighborSearcherResult]:
        """Searches nearest neighbor of an embedding identified by its id.

        Parameters
        ----------
        q : id
            The input embedding id.
        k : int
            The number of nearest neighbors to return.

        Returns
        -------
        List(JSimpleNearestNeighborSearcherResult]
            List of (nearest neighbor) search results.
        """
        return self.object.search(JString(q), k)

    def multisearch(self, q: str, k=10) -> List[List[JSimpleNearestNeighborSearcherResult]]:
        """Searches nearest neighbors of all the embeddings having the specified id.

        Parameters
        ----------
        q : id
            The input embedding id.
        k : int
            The number of nearest neighbors to return for each found embedding.

        Returns
        -------
        List(List[JSimpleNearestNeighborSearcherResult])
            List of List of (nearest neighbor) search results (one for each matching id).
        """
        return self.object.multisearch(JString(q), k)



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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``LuceneGeoSearcher``
class, which wraps the Java class ``SimpleGeoSearcher`` in Anserini.
"""

import logging
from typing import List

from pyserini.pyclass import autoclass
from pyserini.search import JQuery


logger = logging.getLogger(__name__)


# Wrappers around Lucene classes
JSort = autoclass('org.apache.lucene.search.Sort')
JLatLonDocValuesField = autoclass('org.apache.lucene.document.LatLonDocValuesField')
JLatLonShape = autoclass('org.apache.lucene.document.LatLonShape')
JQueryRelation = autoclass('org.apache.lucene.document.ShapeField$QueryRelation')
JLongPoint = autoclass('org.apache.lucene.document.LongPoint')

# Wrappers around Anserini classes
JGeoSearcher = autoclass('io.anserini.search.SimpleGeoSearcher')
JGeoSearcherResult = autoclass('io.anserini.search.SimpleSearcher$Result')


class LuceneGeoSearcher:
    """Wrapper class for ``SimpleGeoSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        self.object = JGeoSearcher(index_dir)

    def search(self, q: JQuery, k: int = 10, sort: JSort = None) -> List[JGeoSearcherResult]:
        """Search the collection.

        Parameters
        ----------
        q : JQuery
            Lucene query.
        k : int
            Number of hits to return.
        sort : JSort
            Optional distance sort that allows searcher to return results based on distance to a point.

        Returns
        -------
        List[JGeoSearcherResult]
            List of search results.
        """
        if sort:
            hits = self.object.searchGeo(q, k, sort)
        else:
            hits = self.object.searchGeo(q, k)
        return hits

    def close(self):
        """Close the searcher."""
        self.object.close()

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
from typing import List, Dict

from jnius import cast

from pyserini.pyclass import autoclass
from pyserini.util import download_prebuilt_index

logger = logging.getLogger(__name__)

# Wrappers around Anserini classes
JHnswDenseSearcher = autoclass('io.anserini.search.HnswDenseSearcher')
JHnswDenseSearcherArgs = autoclass('io.anserini.search.HnswDenseSearcher$Args')

JFlatDenseSearcher = autoclass('io.anserini.search.FlatDenseSearcher')

JScoredDoc = autoclass('io.anserini.search.ScoredDoc')


class LuceneHnswDenseSearcherOld:
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


class LuceneHnswDenseSearcher:
    """Wrapper class for ``HnswDenseSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str, encoder=None, prebuilt_index_name=None):
        self.index_dir = index_dir

        args = JHnswDenseSearcherArgs()
        args.index = index_dir
        if encoder:
            args.encoder = encoder
        self.searcher = JHnswDenseSearcher(args)

        # Keep track if self is a known pre-built index.
        self.prebuilt_index_name = prebuilt_index_name

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, encoder=None, verbose=False):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.
        verbose : bool
            Print status information.

        Returns
        -------
        LuceneSearcher
            Searcher built from the prebuilt index.
        """
        if verbose:
            print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')

        try:
            index_dir = download_prebuilt_index(prebuilt_index_name, verbose=verbose)
        except ValueError as e:
            print(str(e))
            return None

        if verbose:
            print(f'Initializing {prebuilt_index_name}...')

        return cls(index_dir, encoder=encoder, prebuilt_index_name=prebuilt_index_name)

    def search(self, q: str, k: int = 10) -> List[JScoredDoc]:
        """Search the collection.

        Parameters
        ----------
        q : Union[str, JQuery]
            Query string or the ``JQuery`` objected.
        k : int
            Number of hits to return.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.
        strip_segment_id : bool
            Remove the .XXXXX suffix used to denote different segments from an document.
        remove_dups : bool
            Remove duplicate docids when writing final run output.

        Returns
        -------
        List[JLuceneSearcherResult]
            List of search results.
        """

        return self.searcher.search(q, k)


    def batch_search(self, queries: List[str], qids: List[str], k: int = 10, threads: int = 1) -> Dict[str, List[JScoredDoc]]:
        """Search the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            List of query strings.
        qids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.
        query_generator : JQueryGenerator
            Generator to build queries. Set to ``None`` by default to use Anserini default.
        fields : dict
            Optional map of fields to search with associated boosts.

        Returns
        -------
        Dict[str, List[JScoredDoc]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        pass

    def close(self):
        """Close the searcher."""
        self.object.close()

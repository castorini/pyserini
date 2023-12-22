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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``LuceneSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import Dict, List, Optional, Union

from pyserini.fusion import FusionMethod, reciprocal_rank_fusion
from pyserini.index import Document, IndexReader
from pyserini.pyclass import autoclass, JFloat, JArrayList, JHashMap
from pyserini.search import JQuery, JQueryGenerator
from pyserini.trectools import TrecRun
from pyserini.util import download_prebuilt_index, get_sparse_indexes_info

logger = logging.getLogger(__name__)

# Wrappers around Anserini classes
JHnswDenseSearcher = autoclass('io.anserini.search.HnswDenseSearcher')
JHnswDenseSearcher = autoclass('io.anserini.search.HnswDenseSearcher$Args')
JScoredDoc = autoclass('io.anserini.search.JScoredDoc')


class LuceneHnswDenseSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str, prebuilt_index_name=None):
        self.index_dir = index_dir
        self.object = JLuceneSearcher(index_dir)
        self.num_docs = self.object.get_total_num_docs()
        # Keep track if self is a known pre-built index.
        self.prebuilt_index_name = prebuilt_index_name
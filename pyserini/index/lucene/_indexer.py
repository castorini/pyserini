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

from pyserini.pyclass import autoclass

logger = logging.getLogger(__name__)

JLuceneIndexer = autoclass('io.anserini.index.SimpleIndexer')


class LuceneIndexer:
    """Wrapper class for ``SimpleIndexer`` in Anserini. Provides basic functionality of on-the-fly indexing via a
    programmatic API, i.e., indexing in-process objects as opposed to on-file documents.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    args : List[str]
        List of arguments to pass to ``SimpleIndexer``.
    """

    def __init__(self, index_dir: str = None, args: List[str] = None):
        self.index_dir = index_dir
        self.args = args
        if args:
            default_args = ["-input", "", "-collection", "JsonCollection"]
            if not "-threads" in args:
                default_args.extend(["-threads", "1"])
            
            args.extend(default_args)
            self.object = JLuceneIndexer(args)
        else:
            self.object = JLuceneIndexer(index_dir)

    def add(self, doc: str):
        """Add a document to the index.

        Parameters
        ----------
        doc : str
            Document to add.
        """
        self.object.addDocument(doc)

    def close(self):
        """Close this indexer, committing all in-memory data to disk."""
        self.object.close()

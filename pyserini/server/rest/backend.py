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

"""Lucene search backend for Anserini-compatible REST (``SimpleSearcher`` / ``LuceneSearcher``)."""

from __future__ import annotations

import threading
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from pyserini.search.lucene import LuceneSearcher
from pyserini.server.rest.document_format import format_lucene_document
from pyserini.server.rest.index_config import load_index_aliases
from pyserini.util import download_prebuilt_index


class LuceneSearcherRestBackend:
    """Resolve indexes, cache ``LuceneSearcher`` instances, run search and doc lookup."""

    def __init__(self, index_config_path: str | None = None):
        self._aliases = dict(load_index_aliases(index_config_path))
        self._searchers: dict[str, LuceneSearcher] = {}
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)

    def close_all(self) -> None:
        for searcher in self._searchers.values():
            try:
                searcher.close()
            except Exception:
                pass
        self._searchers.clear()

    def decode_path_segment(self, value: str) -> str:
        return unquote(value)

    def resolve_index_dir(self, index_key: str) -> str | None:
        if index_key in self._aliases:
            return self._aliases[index_key]

        p = Path(index_key).expanduser()
        if p.is_dir():
            return str(p.resolve())

        try:
            return download_prebuilt_index(index_key, verbose=False)
        except (ValueError, OSError):
            return None

    def _get_searcher(self, index_token: str) -> LuceneSearcher | None:
        if index_token not in self._searchers:
            path = self.resolve_index_dir(index_token)
            if path is None:
                return None
            try:
                self._searchers[index_token] = LuceneSearcher(path)
            except Exception:
                return None
        return self._searchers[index_token]

    def search(self, index_token: str, query: str, hits: int, parse: bool) -> dict[str, Any] | None:
        """Return Anserini-shaped search JSON or None if the index cannot be opened."""
        with self._locks[index_token]:
            searcher = self._get_searcher(index_token)
            if searcher is None:
                return None
            scored = searcher.search(query, hits)
            candidates = []
            for rank, hit in enumerate(scored, start=1):
                doc = searcher.doc(hit.docid)
                candidates.append({
                    'docid': hit.docid,
                    'score': round(float(hit.score), 6),
                    'rank': rank,
                    'doc': format_lucene_document(doc, parse),
                })
            return {
                'api': 'v1',
                'index': index_token,
                'query': {'text': query},
                'candidates': candidates,
            }

    def get_document(self, index_token: str, docid: str, parse: bool) -> tuple[dict[str, Any] | None, bool]:
        """
        Returns (response_body, index_open_ok).

        If the index cannot be opened, returns (None, False).
        If the index is open but the doc is missing, returns (None, True).
        """
        with self._locks[index_token]:
            searcher = self._get_searcher(index_token)
            if searcher is None:
                return None, False
            doc = searcher.doc(docid)
            if doc is None:
                return None, True
            return {
                'api': 'v1',
                'index': index_token,
                'docid': docid,
                'doc': format_lucene_document(doc, parse),
            }, True

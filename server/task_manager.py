"""
Task manager for Pyserini capabilities.

Initialized with prebuilt index msmarco-v1-passage.
"""

from pathlib import Path
import json
from typing import Dict, List, Optional, Any

from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader
from pyserini.prebuilt_index_info import TF_INDEX_INFO
from pyserini.util import check_downloaded

from models import IndexConfig, IndexType


class TaskManager:
    """Core functionality manager."""

    def __init__(self):
        self.indexes: Dict[str, IndexConfig] = {}

    def initialize_default_index(self, default_index: Optional[str]) -> None:
        """Initialize default prebuilt index."""

        if default_index and default_index in TF_INDEX_INFO.keys():
            self.add_index(
                IndexConfig(
                    name=default_index,
                    type=IndexType.PREBUILT,
                    path=default_index,
                    description=TF_INDEX_INFO[default_index].get("description", ""),
                )
            )

    def add_index(self, config: IndexConfig) -> None:
        """Add a new index to the manager."""
        if config.type == IndexType.LOCAL:
            if not Path(config.path).exists():
                raise FileNotFoundError(f"Index path does not exist: {config.path}")
            config.searcher = LuceneSearcher(config.path)
            config.reader = LuceneIndexReader(config.path)
        else:
            config.searcher = LuceneSearcher.from_prebuilt_index(config.path)
            config.reader = LuceneIndexReader.from_prebuilt_index(config.reader)

        self.indexes[config.name] = config

    def get_indexes(self) -> Dict[str, Dict[str, Any]]:
        """Get all indexes (only prebuilt for now)"""
        return TF_INDEX_INFO

    def search(
        self,
        query: str,
        index_name: str,
        k: int = 10,
        qid: str = "",
        ef_search: Optional[int] = None,
        encoder: Optional[str] = None,
        query_generator: Optional[str] = None,
        shard: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform search on specified index."""
        index_config = self.indexes.get(index_name)
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        if not index_config.searcher or not not index_config.reader:
            index_config.searcher = LuceneSearcher.from_prebuilt_index(
                index_config.path
            )
            index_config.reader = LuceneIndexReader.from_prebuilt_index(
                index_config.reader
            )

        # TODO: actually use other params

        hits = index_config.searcher.search(query, k)
        results: Dict[str, Any] = {"query": {"qid": qid, "text": query}}
        candidates: List[Dict[str, Any]] = []

        for hit in hits:
            raw = json.loads(hit.lucene_document.get("raw"))
            candidates.append(
                {
                    "docid": hit.docid,
                    "score": hit.score,
                    "doc": {"contents": raw["contents"]},
                }
            )
        results["candidates"] = candidates

        return results

    def get_document(self, docid: str, index_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve full document by document ID."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        if not index_config.searcher or not not index_config.reader:
            index_config.searcher = LuceneSearcher.from_prebuilt_index(
                index_config.path
            )
            index_config.reader = LuceneIndexReader.from_prebuilt_index(
                index_config.reader
            )

        doc = index_config.searcher.doc(docid)
        if doc is None:
            raise ValueError(f"Document '{docid}' not found in index '{index_name}'")

        return {
            "docid": docid,
            "text": json.loads(doc.raw())["contents"],
        }

    def get_status(self, index_name: str):
        return check_downloaded(index_name)

    def update_settings(
        self,
        index_name: str,
        ef_search: Optional[str] = None,
        encoder: Optional[str] = None,
        query_generator: Optional[str] = None,
    ) -> None:
        """Update index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        if ef_search is not None:
            index_config.ef_search_override = int(ef_search)
        if encoder is not None:
            index_config.encoder_override = encoder
        if query_generator is not None:
            index_config.query_generator_override = query_generator

    def get_settings(self, index_name: str) -> Dict[str, Any]:
        """Get current index settings."""
        index_config = self.indexes[index_name]
        if not index_config:
            raise ValueError(f"Index '{index_name}' not available")

        settings = {}
        if index_config.ef_search_override is not None:
            settings["efSearch"] = index_config.ef_search_override
        if index_config.encoder_override is not None:
            settings["encoder"] = index_config.encoder_override
        if index_config.query_generator_override is not None:
            settings["queryGenerator"] = index_config.query_generator_override
        return settings


manager = TaskManager()
manager.initialize_default_index("msmarco-v1-passage")

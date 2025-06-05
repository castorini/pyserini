from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader


class IndexType(Enum):
    """Supported index types."""

    PREBUILT = "prebuilt"
    LOCAL = "local"


@dataclass
class IndexConfig:
    """Configuration for a search index."""

    name: str
    type: IndexType
    path: str
    description: Optional[str] = None
    searcher: Optional[LuceneSearcher] = None
    reader: Optional[LuceneIndexReader] = None
    ef_search_override: Optional[int] = None
    encoder_override: Optional[str] = None
    query_generator_override: Optional[str] = None
    shard: Optional[str] = None

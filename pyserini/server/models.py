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
Models and configuration classes for Pyserini FastAPI and MCP server.

"""

from dataclasses import dataclass
from typing import List, Optional

from pyserini.search.lucene import LuceneSearcher, LuceneHnswDenseSearcher


@dataclass
class IndexConfig:
    """Configuration for a search index."""
    name: str
    searcher: LuceneSearcher | LuceneHnswDenseSearcher | None = None
    ef_search: int | None = None
    encoder: str | None = None
    query_generator: str | None = None

@dataclass
class QueryInfo:
    qid: str
    text: str

@dataclass
class DocContents:
    contents: str

@dataclass
class Candidate:
    docid: str
    score: float
    doc: DocContents

@dataclass
class Hits: 
    query: QueryInfo
    candidates: List[Candidate]

@dataclass
class ShardHit:
    docid: str
    score: float

@dataclass 
class Document:
    docid: str
    text: str

@dataclass
class IndexStatus:
    downloaded: bool
    size_bytes: str

@dataclass
class IndexSetting:
    efSearch: Optional[str] = None
    encoder: Optional[str] = None
    queryGenerator: Optional[str] = None
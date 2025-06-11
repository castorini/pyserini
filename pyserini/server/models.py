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
from enum import Enum
from typing import Optional

from pyserini.search.lucene import LuceneSearcher


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
    ef_search_override: Optional[int] = None
    encoder_override: Optional[str] = None
    query_generator_override: Optional[str] = None
    shard: Optional[str] = None

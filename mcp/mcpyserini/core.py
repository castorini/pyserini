import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


from enum import Enum
from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    
class MCPyserini:
    """Main server class that manages Pyserini indexes and search operations."""
    
    def __init__(self):
        self.indexes: Dict[str, IndexConfig] = {}
        self.default_index: str = None
        self.logger = logging.getLogger(__name__)
        self._initialize_default_indexes()
        self.logger.info("Created Pyserini MCP Server")
    
    def _initialize_default_indexes(self) -> None:
        """Initialize default prebuilt indexes."""
        default_configs = [
            IndexConfig(
                name="msmarco-v1-passage",
                type=IndexType.PREBUILT,
                path="msmarco-v1-passage",
                description="MS MARCO V1 passage ranking dataset"
            ),
        ]
        
        for config in default_configs:
            try:
                self.add_index(config)
                if self.default_index is None:
                    self.default_index = config.name
                self.logger.info(f"Successfully loaded prebuilt index: {config.name}")
            except Exception as e:
                self.logger.warning(f"Failed to load prebuilt index {config.name}: {e}")
                
    def add_index(self, config: IndexConfig) -> bool:
        """Add a new index to the server."""
        try:
            if config.type == IndexType.PREBUILT:
                searcher = LuceneSearcher.from_prebuilt_index(config.path)
                reader = LuceneIndexReader.from_prebuilt_index(config.path)
            else:
                if not Path(config.path).exists():
                    raise FileNotFoundError(f"Index path does not exist: {config.path}")
                searcher = LuceneSearcher(config.path)
                reader = LuceneIndexReader(config.path)
            
            config.searcher = searcher
            config.reader = reader
            self.indexes[config.name] = config
            
            self.logger.info(f"Added index '{config.name}' with {reader.stats()['documents']} documents")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add index {config.name}: {e}")
            return False
        
    def get_index(self, index_name: Optional[str] = None) -> Optional[IndexConfig]:
        """Get index configuration by name, or default if none specified."""
        if index_name is None:
            index_name = self.default_index
        return self.indexes.get(index_name)
        
    def get_document(self, docid: str, index_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieve full document by document ID."""
        index_config = self.get_index(index_name)
        if not index_config or not index_config.searcher:
            raise ValueError(f"Index '{index_name or self.default_index}' not available")
        
        try:
            doc = index_config.searcher.doc(docid)
            if doc is None:
                return None
                
            return {
                "docid": docid,
                "text": doc.raw(),
                "index": index_config.name
            }
            
        except Exception as e:
            self.logger.error(f"Document retrieval failed for {docid}: {e}")
            raise RuntimeError(f"Failed to retrieve document {docid}: {e}")  
        
    def search(self, query: str, k: int = 10, index_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Perform BM25 search on specified index."""
        
        print("SEARCHING", self.get_index(index_name), query)
        index_config = self.get_index(index_name)
        if not index_config or not index_config.searcher:
            raise ValueError(f"Index '{index_name or self.default_index}' not available")
        
        try:
            hits = index_config.searcher.search(query, k)
            results = []
            
            for hit in hits:
                doc = index_config.searcher.doc(hit.docid)
                if doc:
                    text = doc.raw()
                    results.append({
                        "docid": hit.docid,
                        "score": round(hit.score, 5),
                        "text": text[:200] + "…" if len(text) > 200 else text,
                        "index": index_config.name
                    })
            
            self.logger.info(f"Search query '{query}' returned {len(results)} results from {index_config.name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            raise RuntimeError(f"Search operation failed: {e}")    
# Copyright (c) Microsoft. All rights reserved.

import json
import logging
from dataclasses import dataclass

import aiohttp
import requests

from semantic_kernel.orchestration.sk_context import SKContext
from typing import Callable, Optional, Tuple, Union
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from pyserini.search import LuceneSearcher, FaissSearcher, AutoQueryEncoder

@dataclass
class PyseriniConfig:
    k1: Optional[float]=None
    b: Optional[float]=None
    hits: Optional[int]=1

class PyseriniSkill:
    """
    A skill that uses Pyserini to search a corpus of documents.

    Usage:
        kernel.import_skill(PyseriniSkill(), "http")

    Examples:

        {{pyserini.search $query}}
    """

    def __init__(self,pyserini_config:PyseriniConfig):
        self.lang = 'en'
        self.searcher = LuceneSearcher('indexes/lucene-index-acl-paragraph')
        self.searcher.set_language(self.lang)
        if pyserini_config.k1 is not None and pyserini_config.b is not None:
            self.searcher.set_bm25(pyserini_config.k1, pyserini_config.b)
            self.retriever_name = f'BM25 (k1={pyserini_config.k1}, b={pyserini_config.b})'
        else:
            self.retriever_name = 'BM25'
        self.hits = pyserini_config.hits

    @sk_function(description="Searches a corpus of documents using Pyserini using the specified query.", name="search")
    @sk_function_context_parameter(name="url", description="The url of the request")
    async def search(self, query: str, context: SKContext) -> str:
        """
        Searches a corpus of documents using Pyserini using the specified query.
        Return the response body as a string.

        params:
            query: The query to search for.
            context: The SKContext containing the url of the request.
        returns:
            The response body as a string.
        """
        _, url = context.variables.get("url")
        if not url:
            raise ValueError("url cannot be `None` or empty")

        if not query:
            search_results = []
        else:
            hits = self.searcher.search(query, k=self.hits)
            docs = [self.searcher.doc(hit.docid) for hit in hits]
            search_results = [
                {
                    'rank': r + 1,
                    'docid': hit.docid,
                    'doc': docs[r].contents(),
                }
                for r, hit in enumerate(hits)
            ]
        return "docid:" + search_results[0]["docid"] + ",doc:" + search_results[0]["doc"]


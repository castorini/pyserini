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
Retrieval-Augmented Generation (RAG) pipeline for Pyserini.

Combines any Pyserini searcher (LuceneSearcher, FaissSearcher, …) with an
LLMClient to implement the classic retrieve-then-read RAG pattern:

    from pyserini.llm import LLMClient, RAGSearcher
    from pyserini.search.lucene import LuceneSearcher

    searcher = LuceneSearcher.from_prebuilt_index("msmarco-v1-passage")
    client   = LLMClient("meta-llama/Llama-3.1-8B-Instruct", backend="vllm")
    rag      = RAGSearcher(searcher, client)

    result = rag.search_and_generate("What is the boiling point of water?")
    print(result["answer"])
"""

import json
from typing import Any, Dict, List, Optional

from pyserini.llm._client import LLMClient

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer the user's question using only the "
    "information found in the provided context documents. If the context does "
    "not contain enough information to answer the question, say so clearly."
)

DEFAULT_RAG_TEMPLATE = """\
Context documents:
{context}

Question: {query}

Answer the question based on the context above."""


class RAGSearcher:
    """Retrieve-then-read RAG pipeline combining a Pyserini searcher and an LLM.

    Parameters
    ----------
    searcher :
        Any initialised Pyserini searcher (``LuceneSearcher``, ``FaissSearcher``,
        ``LuceneHnswDenseSearcher``, etc.). The only requirement is that it
        exposes a ``search(query, k)`` method returning a list of hit objects.
    llm_client : LLMClient
        Initialised :class:`LLMClient` instance.
    system_prompt : str, optional
        System-role message sent to the LLM before the RAG prompt.
    rag_template : str, optional
        Prompt template used to format retrieved passages and the user query.
        Must contain the ``{context}`` and ``{query}`` placeholders.
    """

    def __init__(
        self,
        searcher: Any,
        llm_client: LLMClient,
        system_prompt: Optional[str] = None,
        rag_template: Optional[str] = None,
    ):
        self.searcher = searcher
        self.llm_client = llm_client
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.rag_template = rag_template or DEFAULT_RAG_TEMPLATE

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the top-*k* documents for *query*.

        Parameters
        ----------
        query : str
            The search query string.
        k : int
            Number of documents to retrieve.

        Returns
        -------
        list of dict
            Each dict has the following keys:

            - ``docid`` (str) – document identifier
            - ``score`` (float) – retrieval score
            - ``text``  (str) – raw passage / document text
            - ``rank``  (int) – 1-based rank position
        """
        hits = self.searcher.search(query, k)
        results: List[Dict[str, Any]] = []
        for rank, hit in enumerate(hits, start=1):
            text = self._extract_text(hit)
            results.append(
                {
                    'docid': hit.docid,
                    'score': float(hit.score),
                    'text': text,
                    'rank': rank,
                }
            )
        return results

    def generate(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> str:
        """Generate an answer given *query* and pre-retrieved documents.

        Parameters
        ----------
        query : str
            The user's question.
        retrieved_docs : list of dict
            Documents returned by :meth:`retrieve`.
        **kwargs
            Extra keyword arguments forwarded to :meth:`LLMClient.generate`
            (e.g., ``max_tokens``, ``temperature``).

        Returns
        -------
        str
            Generated answer text.
        """
        context = self._format_context(retrieved_docs)
        prompt = self.rag_template.format(context=context, query=query)
        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': prompt},
        ]
        return self.llm_client.generate(messages, **kwargs)

    def search_and_generate(
        self,
        query: str,
        k: int = 5,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Retrieve documents and generate an answer in one call.

        Parameters
        ----------
        query : str
            The user's question.
        k : int
            Number of documents to retrieve (passed to :meth:`retrieve`).
        **kwargs
            Extra keyword arguments forwarded to :meth:`LLMClient.generate`.

        Returns
        -------
        dict
            A dict with three keys:

            - ``query`` (str) – the original query
            - ``retrieved_docs`` (list of dict) – ranked retrieved documents
            - ``answer`` (str) – LLM-generated answer
        """
        retrieved_docs = self.retrieve(query, k)
        answer = self.generate(query, retrieved_docs, **kwargs)
        return {
            'query': query,
            'retrieved_docs': retrieved_docs,
            'answer': answer,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_text(hit: Any) -> str:
        """Pull plain text from a Pyserini search hit.

        Handles both Lucene hits (which carry a ``lucene_document`` with a
        ``raw`` JSON field) and dense hits (which carry a ``contents`` attribute
        directly).
        """
        # Lucene / sparse hits store the document as a JSON blob in 'raw'
        if hasattr(hit, 'lucene_document') and hit.lucene_document is not None:
            raw = hit.lucene_document.get('raw')
            if raw:
                try:
                    doc = json.loads(raw)
                    return (
                        doc.get('contents')
                        or doc.get('text')
                        or doc.get('passage')
                        or doc.get('segment')
                        or ''
                    )
                except (json.JSONDecodeError, AttributeError):
                    return str(raw)

        # Dense hits (FaissSearcher) sometimes carry text directly
        for attr in ('contents', 'text', 'passage'):
            if hasattr(hit, attr):
                val = getattr(hit, attr)
                if val:
                    return str(val)

        return ''

    @staticmethod
    def _format_context(docs: List[Dict[str, Any]]) -> str:
        """Render retrieved documents as a numbered list for the LLM prompt."""
        parts = []
        for doc in docs:
            header = f"[{doc['rank']}] docid={doc['docid']}  score={doc['score']:.4f}"
            parts.append(f"{header}\n{doc['text']}")
        return '\n\n'.join(parts)

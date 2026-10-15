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
Tests for pyserini.llm (LLMClient and RAGSearcher).

All external API calls are mocked so the tests run without a live OpenAI key
or a running vLLM server.  A small integration smoke-test is also included
and skipped automatically unless a vLLM server is reachable on localhost.
"""

import json
import socket
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from pyserini.llm import LLMClient, RAGSearcher


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_completion(content: str) -> MagicMock:
    """Build a minimal mock that looks like an openai ChatCompletion object."""
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    completion = MagicMock()
    completion.choices = [choice]
    return completion


def _vllm_reachable(port: int = 8000) -> bool:
    """Return True if something is listening on localhost:{port}."""
    try:
        with socket.create_connection(('localhost', port), timeout=1):
            return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# LLMClient tests
# ---------------------------------------------------------------------------

class TestLLMClientInit(unittest.TestCase):
    """Test that LLMClient initialises with the correct OpenAI client settings."""

    def test_openai_backend_default_base_url(self):
        """OpenAI backend should use the standard api.openai.com endpoint."""
        with patch('pyserini.llm._client.OpenAI') as mock_openai:
            LLMClient('gpt-4o', backend='openai', api_key='sk-test')
            # base_url should NOT be passed (stays as None → api.openai.com)
            call_kwargs = mock_openai.call_args[1]
            self.assertNotIn('base_url', call_kwargs)
            self.assertEqual(call_kwargs['api_key'], 'sk-test')

    def test_vllm_backend_default_url(self):
        """vLLM backend should point to http://localhost:8000/v1 by default."""
        with patch('pyserini.llm._client.OpenAI') as mock_openai:
            LLMClient('meta-llama/Llama-3.1-8B-Instruct', backend='vllm')
            call_kwargs = mock_openai.call_args[1]
            self.assertEqual(call_kwargs['base_url'], 'http://localhost:8000/v1')
            self.assertEqual(call_kwargs['api_key'], 'EMPTY')

    def test_vllm_backend_custom_port(self):
        """Custom vllm_port should be reflected in the base_url."""
        with patch('pyserini.llm._client.OpenAI') as mock_openai:
            LLMClient('some-model', backend='vllm', vllm_port=9000)
            call_kwargs = mock_openai.call_args[1]
            self.assertEqual(call_kwargs['base_url'], 'http://localhost:9000/v1')

    def test_vllm_backend_custom_base_url(self):
        """An explicit base_url overrides the vllm_port default."""
        with patch('pyserini.llm._client.OpenAI') as mock_openai:
            LLMClient('some-model', backend='vllm', base_url='http://gpu-server:8080/v1')
            call_kwargs = mock_openai.call_args[1]
            self.assertEqual(call_kwargs['base_url'], 'http://gpu-server:8080/v1')

    def test_openai_compatible_backend(self):
        """openai_compatible backend passes through base_url unchanged."""
        with patch('pyserini.llm._client.OpenAI') as mock_openai:
            LLMClient(
                'some-model',
                backend='openai_compatible',
                api_key='my-key',
                base_url='https://my-proxy.example.com/v1',
            )
            call_kwargs = mock_openai.call_args[1]
            self.assertEqual(call_kwargs['base_url'], 'https://my-proxy.example.com/v1')
            self.assertEqual(call_kwargs['api_key'], 'my-key')

    def test_unknown_backend_raises(self):
        """An unrecognised backend name should raise ValueError immediately."""
        with self.assertRaises(ValueError):
            LLMClient('gpt-4o', backend='unknown_backend')

    def test_attributes_stored(self):
        """Constructor params should be stored as instance attributes."""
        with patch('pyserini.llm._client.OpenAI'):
            client = LLMClient(
                'gpt-4o',
                backend='openai',
                api_key='sk-test',
                max_tokens=512,
                temperature=0.7,
                timeout=30.0,
            )
        self.assertEqual(client.model, 'gpt-4o')
        self.assertEqual(client.backend, 'openai')
        self.assertEqual(client.max_tokens, 512)
        self.assertAlmostEqual(client.temperature, 0.7)
        self.assertAlmostEqual(client.timeout, 30.0)


class TestLLMClientGenerate(unittest.TestCase):
    """Test the generate() method with mocked API responses."""

    def _make_client(self, **kwargs) -> LLMClient:
        with patch('pyserini.llm._client.OpenAI'):
            client = LLMClient('gpt-4o', backend='openai', api_key='sk-test', **kwargs)
        return client

    def test_generate_returns_content(self):
        """generate() should return the message content from the completion."""
        client = self._make_client()
        client.client = MagicMock()
        client.client.chat.completions.create.return_value = _make_completion(
            'Paris is the capital of France.'
        )

        messages = [{'role': 'user', 'content': 'What is the capital of France?'}]
        result = client.generate(messages)
        self.assertEqual(result, 'Paris is the capital of France.')

    def test_generate_none_content_returns_empty_string(self):
        """If the API returns None as content, generate() should return ''."""
        client = self._make_client()
        client.client = MagicMock()
        client.client.chat.completions.create.return_value = _make_completion(None)

        result = client.generate([{'role': 'user', 'content': 'Hi'}])
        self.assertEqual(result, '')

    def test_generate_passes_correct_params(self):
        """generate() must forward model, messages, max_tokens, temperature to the API."""
        client = self._make_client(max_tokens=256, temperature=0.5)
        client.client = MagicMock()
        client.client.chat.completions.create.return_value = _make_completion('ok')

        messages = [{'role': 'user', 'content': 'Test'}]
        client.generate(messages)

        call_kwargs = client.client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['model'], 'gpt-4o')
        self.assertEqual(call_kwargs['messages'], messages)
        self.assertEqual(call_kwargs['max_tokens'], 256)
        self.assertAlmostEqual(call_kwargs['temperature'], 0.5)

    def test_generate_per_call_overrides(self):
        """max_tokens and temperature kwargs in generate() should override instance defaults."""
        client = self._make_client(max_tokens=1024, temperature=0.0)
        client.client = MagicMock()
        client.client.chat.completions.create.return_value = _make_completion('ok')

        client.generate([{'role': 'user', 'content': 'Test'}], max_tokens=64, temperature=1.0)

        call_kwargs = client.client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['max_tokens'], 64)
        self.assertAlmostEqual(call_kwargs['temperature'], 1.0)

    def test_generate_retries_on_error(self):
        """generate() should retry up to MAX_RETRIES times before raising."""
        from pyserini.llm._client import MAX_RETRIES

        client = self._make_client()
        client.client = MagicMock()
        client.client.chat.completions.create.side_effect = RuntimeError('server error')

        with patch('pyserini.llm._client.time.sleep'):  # don't actually sleep in tests
            with self.assertRaises(RuntimeError):
                client.generate([{'role': 'user', 'content': 'Test'}])

        self.assertEqual(
            client.client.chat.completions.create.call_count,
            MAX_RETRIES,
        )

    def test_generate_succeeds_after_transient_error(self):
        """generate() should succeed if a later attempt works after a transient failure."""
        client = self._make_client()
        client.client = MagicMock()
        client.client.chat.completions.create.side_effect = [
            RuntimeError('transient'),
            _make_completion('recovered'),
        ]

        with patch('pyserini.llm._client.time.sleep'):
            result = client.generate([{'role': 'user', 'content': 'Test'}])

        self.assertEqual(result, 'recovered')


# ---------------------------------------------------------------------------
# RAGSearcher tests
# ---------------------------------------------------------------------------

class TestRAGSearcherRetrieve(unittest.TestCase):
    """Test the retrieve() helper that wraps the pyserini searcher."""

    def _make_lucene_hit(self, docid: str, score: float, text: str) -> MagicMock:
        """Simulate a LuceneSearcher hit (has a lucene_document with raw JSON)."""
        raw = json.dumps({'contents': text})
        doc = MagicMock()
        doc.get.return_value = raw
        hit = MagicMock()
        hit.docid = docid
        hit.score = score
        hit.lucene_document = doc
        return hit

    def _make_dense_hit(self, docid: str, score: float, contents: str) -> SimpleNamespace:
        """Simulate a FaissSearcher dense hit (has a contents attribute)."""
        hit = SimpleNamespace(docid=docid, score=score, contents=contents)
        # Dense hits don't have lucene_document
        return hit

    def test_retrieve_lucene_hits(self):
        mock_searcher = MagicMock()
        mock_searcher.search.return_value = [
            self._make_lucene_hit('doc1', 0.9, 'Water boils at 100 °C.'),
            self._make_lucene_hit('doc2', 0.7, 'Ice melts at 0 °C.'),
        ]
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        rag = RAGSearcher(mock_searcher, llm)

        docs = rag.retrieve('boiling point of water', k=2)

        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]['docid'], 'doc1')
        self.assertAlmostEqual(docs[0]['score'], 0.9)
        self.assertEqual(docs[0]['text'], 'Water boils at 100 °C.')
        self.assertEqual(docs[0]['rank'], 1)
        self.assertEqual(docs[1]['rank'], 2)

    def test_retrieve_passes_k_to_searcher(self):
        mock_searcher = MagicMock()
        mock_searcher.search.return_value = []
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        rag = RAGSearcher(mock_searcher, llm)

        rag.retrieve('some query', k=7)
        mock_searcher.search.assert_called_once_with('some query', 7)

    def test_retrieve_dense_hits(self):
        """retrieve() should also work with dense hits that have a contents attribute."""
        mock_searcher = MagicMock()
        mock_searcher.search.return_value = [
            self._make_dense_hit('d1', 0.95, 'Dense passage text.'),
        ]
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        rag = RAGSearcher(mock_searcher, llm)

        docs = rag.retrieve('query', k=1)
        self.assertEqual(docs[0]['text'], 'Dense passage text.')

    def test_retrieve_empty_results(self):
        mock_searcher = MagicMock()
        mock_searcher.search.return_value = []
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        rag = RAGSearcher(mock_searcher, llm)

        docs = rag.retrieve('query', k=5)
        self.assertEqual(docs, [])


class TestRAGSearcherGenerate(unittest.TestCase):
    """Test RAGSearcher.generate() prompt construction and LLM invocation."""

    def _make_rag(self, mock_response: str = 'Mock answer.') -> tuple:
        mock_searcher = MagicMock()
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        llm.client = MagicMock()
        llm.client.chat.completions.create.return_value = _make_completion(mock_response)
        rag = RAGSearcher(mock_searcher, llm)
        return rag, llm

    def test_generate_includes_query_in_prompt(self):
        rag, llm = self._make_rag()
        docs = [{'rank': 1, 'docid': 'doc1', 'score': 0.9, 'text': 'Passage text.'}]
        rag.generate('What is X?', docs)

        call_args = llm.client.chat.completions.create.call_args[1]
        messages = call_args['messages']
        user_content = next(m['content'] for m in messages if m['role'] == 'user')
        self.assertIn('What is X?', user_content)
        self.assertIn('Passage text.', user_content)

    def test_generate_system_prompt_present(self):
        rag, llm = self._make_rag()
        docs = [{'rank': 1, 'docid': 'doc1', 'score': 0.9, 'text': 'Some text.'}]
        rag.generate('Q?', docs)

        call_args = llm.client.chat.completions.create.call_args[1]
        messages = call_args['messages']
        system_msgs = [m for m in messages if m['role'] == 'system']
        self.assertTrue(len(system_msgs) > 0)

    def test_generate_custom_system_prompt(self):
        mock_searcher = MagicMock()
        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        llm.client = MagicMock()
        llm.client.chat.completions.create.return_value = _make_completion('ans')
        rag = RAGSearcher(mock_searcher, llm, system_prompt='Custom system prompt.')

        docs = [{'rank': 1, 'docid': 'doc1', 'score': 0.5, 'text': 'text'}]
        rag.generate('Q?', docs)

        call_args = llm.client.chat.completions.create.call_args[1]
        messages = call_args['messages']
        system_content = next(m['content'] for m in messages if m['role'] == 'system')
        self.assertEqual(system_content, 'Custom system prompt.')

    def test_generate_returns_llm_answer(self):
        rag, _ = self._make_rag('The answer is 42.')
        docs = [{'rank': 1, 'docid': 'doc1', 'score': 0.9, 'text': 'Context.'}]
        result = rag.generate('What is the answer?', docs)
        self.assertEqual(result, 'The answer is 42.')


class TestRAGSearcherSearchAndGenerate(unittest.TestCase):
    """Integration-style test for the full search_and_generate() pipeline."""

    def test_search_and_generate_result_structure(self):
        raw = json.dumps({'contents': 'Water boils at 100 °C at standard pressure.'})
        doc_mock = MagicMock()
        doc_mock.get.return_value = raw
        hit = MagicMock()
        hit.docid = 'doc42'
        hit.score = 0.88
        hit.lucene_document = doc_mock

        mock_searcher = MagicMock()
        mock_searcher.search.return_value = [hit]

        with patch('pyserini.llm._client.OpenAI'):
            llm = LLMClient('gpt-4o', backend='openai', api_key='sk-test')
        llm.client = MagicMock()
        llm.client.chat.completions.create.return_value = _make_completion(
            'Water boils at 100 °C.'
        )

        rag = RAGSearcher(mock_searcher, llm)
        result = rag.search_and_generate('What is the boiling point of water?', k=1)

        self.assertEqual(result['query'], 'What is the boiling point of water?')
        self.assertEqual(len(result['retrieved_docs']), 1)
        self.assertEqual(result['retrieved_docs'][0]['docid'], 'doc42')
        self.assertEqual(result['answer'], 'Water boils at 100 °C.')

    def test_vllm_backend_used_in_rag(self):
        """Ensure RAGSearcher works end-to-end with a vLLM-configured LLMClient."""
        mock_searcher = MagicMock()
        mock_searcher.search.return_value = []

        with patch('pyserini.llm._client.OpenAI') as mock_openai_cls:
            llm = LLMClient(
                'meta-llama/Llama-3.1-8B-Instruct',
                backend='vllm',
                vllm_port=8000,
            )
            # Verify vLLM endpoint was configured
            call_kwargs = mock_openai_cls.call_args[1]
            self.assertEqual(call_kwargs['base_url'], 'http://localhost:8000/v1')
            self.assertEqual(call_kwargs['api_key'], 'EMPTY')

        llm.client = MagicMock()
        llm.client.chat.completions.create.return_value = _make_completion(
            'I could not find relevant documents to answer your question.'
        )

        rag = RAGSearcher(mock_searcher, llm)
        result = rag.search_and_generate('obscure query with no hits', k=3)

        self.assertIn('query', result)
        self.assertIn('retrieved_docs', result)
        self.assertIn('answer', result)
        self.assertEqual(result['retrieved_docs'], [])


# ---------------------------------------------------------------------------
# vLLM integration smoke-test (skipped if no server is running)
# ---------------------------------------------------------------------------

@unittest.skipUnless(_vllm_reachable(), 'No vLLM server detected on localhost:8000')
class TestVLLMIntegration(unittest.TestCase):
    """Live smoke-test against a running vLLM server.

    Start a vLLM server before running:
        vllm serve <model-name> --port 8000

    These tests are automatically skipped when no server is detected.
    """

    MODEL = 'meta-llama/Llama-3.1-8B-Instruct'

    def _get_running_model(self) -> str:
        """Query the vLLM /v1/models endpoint to get the deployed model name."""
        import requests
        try:
            resp = requests.get('http://localhost:8000/v1/models', timeout=5)
            data = resp.json()
            return data['data'][0]['id']
        except Exception:
            return self.MODEL

    def test_llm_client_generate(self):
        model = self._get_running_model()
        client = LLMClient(model, backend='vllm')
        response = client.generate(
            [{'role': 'user', 'content': 'Reply with exactly one word: hello'}],
            max_tokens=10,
        )
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_rag_searcher_with_mock_search(self):
        """RAGSearcher with vLLM client and a fake single-document searcher."""
        model = self._get_running_model()
        client = LLMClient(model, backend='vllm')

        raw = json.dumps({'contents': 'Water boils at 100 °C at standard pressure.'})
        doc_mock = MagicMock()
        doc_mock.get.return_value = raw
        hit = MagicMock()
        hit.docid = 'doc1'
        hit.score = 1.0
        hit.lucene_document = doc_mock

        mock_searcher = MagicMock()
        mock_searcher.search.return_value = [hit]

        rag = RAGSearcher(mock_searcher, client)
        result = rag.search_and_generate(
            'What temperature does water boil at?', k=1, max_tokens=64
        )

        self.assertEqual(result['query'], 'What temperature does water boil at?')
        self.assertEqual(len(result['retrieved_docs']), 1)
        self.assertIsInstance(result['answer'], str)
        self.assertTrue(len(result['answer']) > 0)
        print(f"\n[vLLM integration] Answer: {result['answer']}")


if __name__ == '__main__':
    unittest.main()

#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import tempfile
import time
import unittest
import unittest.mock
import hashlib
import json
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

# Keep this test in tests/core: the REST server imports search backends including Faiss.
from pyserini.server.backend import SharedSearchBackend
from pyserini.server.errors import BadSearchRequestError
from pyserini.server.rest.app import API_VERSION, ROUTE_ERROR, app, create_app, _build_uvicorn_log_config
from pyserini.server.utils import Bm25Config, IndexConfig

# Small prebuilt TF index (see TF_INDEX_INFO["cacm"]); stable BM25 top-1 for this query.
_REST_INDEX = 'cacm'
_REST_QUERY = 'information retrieval'
_REST_TOP_DOCID = 'CACM-3134'
_REST_DOC_SUBSTRING = 'Information Storage and Retrieval'


class _FakeSearcher:
    def __init__(self):
        self.closed = False
        self.bm25 = None

    def set_bm25(self, k1, b):
        self.bm25 = (k1, b)

    def close(self):
        self.closed = True


class TestRestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Lifespan (initializes app.state.search_backend) runs on context enter.
        cls._test_client = TestClient(app)
        cls._test_client.__enter__()
        cls.client = cls._test_client

    @classmethod
    def tearDownClass(cls):
        cls._test_client.__exit__(None, None, None)

    def test_openapi_yaml(self):
        response = self.client.get('/openapi.yaml')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pyserini REST API', response.text)
        self.assertIn('/{index}/search', response.text)
        self.assertIn(f'url: /{API_VERSION}', response.text)

    def test_openapi_json_reflects_bundled_schema(self):
        response = self.client.get('/openapi.json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('components', data)
        self.assertIn('securitySchemes', data['components'])
        self.assertIn('ApiKeyAuth', data['components']['securitySchemes'])
        self.assertIn('/token', data['paths'])
        self.assertIn('202', data['paths']['/token']['post']['responses'])
        self.assertNotIn('201', data['paths']['/token']['post']['responses'])
        self.assertNotIn('409', data['paths']['/token']['post']['responses'])
        self.assertTrue(data['paths']['/token']['post']['requestBody']['required'])
        self.assertIn('TokenIssuanceRequest', data['components']['schemas'])
        self.assertIn('TokenDeliveryResponse', data['components']['schemas'])
        self.assertNotIn('TokenResponse', data['components']['schemas'])
        trace_parameter_names = {
            parameter['name'] for parameter in data['components']['parameters'].values()
        }
        self.assertEqual(trace_parameter_names, {'qid', 'question', 'run_id', 'agent', 'step'})
        expected_trace_refs = {
            f'#/components/parameters/{name}'
            for name in ('TraceQid', 'TraceQuestion', 'TraceRunId', 'TraceAgent', 'TraceStep')
        }
        search_trace_refs = {
            parameter['$ref']
            for parameter in data['paths']['/{index}/search']['get']['parameters']
            if '$ref' in parameter
        }
        document_trace_refs = {
            parameter['$ref']
            for parameter in data['paths']['/{index}/doc/{docid}']['get']['parameters']
            if '$ref' in parameter
        }
        self.assertEqual(search_trace_refs, expected_trace_refs)
        self.assertEqual(document_trace_refs, expected_trace_refs)
        search_responses = data['paths']['/{index}/search']['get']['responses']
        self.assertIn('401', search_responses)
        self.assertIn('429', search_responses)

    def test_docs_available(self):
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)

    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, msg=response.text)
        data = response.json()
        self.assertIn('openapi', data)
        self.assertEqual(data.get('openapi'), '/openapi.yaml')
        self.assertEqual(data.get('version'), API_VERSION)

    def test_search_anonymous_shape(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        data = response.json()
        self.assertEqual(data.get('api'), 'v1')
        self.assertEqual(data.get('index'), _REST_INDEX)
        self.assertEqual(data.get('query'), {'text': _REST_QUERY})
        self.assertIn('candidates', data)
        self.assertEqual(1, len(data['candidates']))
        cand = data['candidates'][0]
        self.assertEqual(cand.get('docid'), _REST_TOP_DOCID)
        self.assertEqual(cand.get('rank'), 1)
        self.assertIn('score', cand)
        self.assertIn('doc', cand)

    def test_search_repeated_request_uses_backend_cache(self):
        backend = self.client.app.state.search_backend
        backend._search_cached.cache_clear()
        with unittest.mock.patch.object(backend, '_prepare_query', wraps=backend._prepare_query) as mocked_prepare:
            r1 = self.client.get(
                f'/{API_VERSION}/{_REST_INDEX}/search',
                params={'query': _REST_QUERY, 'hits': 1, 'parse': 'true'},
            )
            r2 = self.client.get(
                f'/{API_VERSION}/{_REST_INDEX}/search',
                params={'query': _REST_QUERY, 'hits': 1, 'parse': 'true'},
            )
        self.assertEqual(r1.status_code, 200, msg=r1.text)
        self.assertEqual(r2.status_code, 200, msg=r2.text)
        self.assertEqual(mocked_prepare.call_count, 1)

    def test_search_missing_query(self):
        response = self.client.get(f'/{API_VERSION}/{_REST_INDEX}/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn('query', response.json().get('error', ''))

    def test_get_doc_parse_false_doc_is_string(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
            params={'parse': 'false'},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        doc = response.json().get('doc')
        self.assertIsInstance(doc, str)
        self.assertIn(_REST_DOC_SUBSTRING, doc)

    def test_get_doc_parse_invalid_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
            params={'parse': 'maybe'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('parse', response.json().get('error', ''))

    def test_get_doc(self):
        response = self.client.get(f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}')
        self.assertEqual(response.status_code, 200, msg=response.text)
        data = response.json()
        self.assertEqual(data.get('api'), 'v1')
        self.assertEqual(data.get('index'), _REST_INDEX)
        self.assertEqual(data.get('docid'), _REST_TOP_DOCID)
        doc = data.get('doc')
        self.assertIsNotNone(doc)
        if isinstance(doc, str):
            self.assertIn(_REST_DOC_SUBSTRING, doc)
        else:
            contents = doc.get('contents') if isinstance(doc, dict) else None
            self.assertIsNotNone(contents)
            self.assertIn(_REST_DOC_SUBSTRING, contents)

    def test_get_doc_max_doc_length_truncates_doc_when_parse_true(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
            params={'max_doc_length': '24'},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        doc = response.json()['doc']
        self.assertIsInstance(doc, str)
        self.assertLessEqual(len(doc), 24)

    def test_get_doc_max_doc_length_with_parse_false_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
            params={'parse': 'false', 'max_doc_length': '24'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('parse=true', response.json().get('error', ''))

    def test_get_doc_max_doc_length_invalid_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
            params={'max_doc_length': 'abc'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('max_doc_length', response.json().get('error', ''))

    def test_get_doc_repeated_request_uses_backend_cache(self):
        backend = self.client.app.state.search_backend
        backend._document_cached.cache_clear()
        with unittest.mock.patch.object(
            backend,
            '_bulk_fetch_and_format_documents',
            wraps=backend._bulk_fetch_and_format_documents,
        ) as mocked_bulk_fetch:
            r1 = self.client.get(
                f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
                params={'parse': 'true'},
            )
            r2 = self.client.get(
                f'/{API_VERSION}/{_REST_INDEX}/doc/{_REST_TOP_DOCID}',
                params={'parse': 'true'},
            )
        self.assertEqual(r1.status_code, 200, msg=r1.text)
        self.assertEqual(r2.status_code, 200, msg=r2.text)
        self.assertEqual(mocked_bulk_fetch.call_count, 1)

    def test_get_doc_not_found(self):
        response = self.client.get(f'/{API_VERSION}/{_REST_INDEX}/doc/does-not-exist-xyz')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.json().get('error', '').lower())
        self.assertIn('Document not found', response.json().get('error', ''))

    def test_unknown_route_404(self):
        response = self.client.get(f'/{API_VERSION}/bad/extra/route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('error'), ROUTE_ERROR)

    def test_search_hits_zero_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': 'text', 'hits': '0'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('positive', response.json().get('error', ''))

    def test_search_hits_not_integer_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': 'text', 'hits': 'not-a-number'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('integer', response.json().get('error', ''))

    def test_search_parse_invalid_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': 'text', 'parse': 'maybe'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('parse', response.json().get('error', ''))

    def test_search_empty_query_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': ''},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('query', response.json().get('error', ''))

    def test_search_bm25_k1_b_accepted(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.8', 'b': '0.3'},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        self.assertEqual(response.json()['candidates'][0].get('docid'), _REST_TOP_DOCID)

    def test_search_bm25_k1_only_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.1'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('together', response.json().get('error', ''))

    def test_search_bm25_b_only_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'b': '0.3'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('together', response.json().get('error', ''))

    def test_search_bm25_negative_k1_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '-1', 'b': '0.3'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('k1', response.json().get('error', ''))

    def test_search_bm25_b_above_one_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.8', 'b': '1.1'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('b', response.json().get('error', ''))

    def test_search_bm25_nan_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': 'nan', 'b': '0.3'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('k1', response.json().get('error', ''))

    def test_search_bm25_custom_params_change_score(self):
        default_resp = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1},
        )
        tuned_resp = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.1', 'b': '0.1'},
        )
        self.assertEqual(default_resp.status_code, 200, msg=default_resp.text)
        self.assertEqual(tuned_resp.status_code, 200, msg=tuned_resp.text)
        default_score = default_resp.json()['candidates'][0]['score']
        tuned_score = tuned_resp.json()['candidates'][0]['score']
        self.assertNotEqual(default_score, tuned_score)

    def test_search_bm25_cache_respects_different_k1_b(self):
        backend = self.client.app.state.search_backend
        backend._search_cached.cache_clear()
        r1 = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.8', 'b': '0.3'},
        )
        r2 = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': '0.1', 'b': '0.1'},
        )
        self.assertEqual(r1.status_code, 200, msg=r1.text)
        self.assertEqual(r2.status_code, 200, msg=r2.text)
        self.assertNotEqual(
            r1.json()['candidates'][0]['score'],
            r2.json()['candidates'][0]['score'],
        )

    def test_search_bm25_on_non_sparse_index_400(self):
        backend = self.client.app.state.search_backend
        fake_config = IndexConfig(name='fake-dense', index_type='faiss', searcher=object())
        with unittest.mock.patch.object(backend, '_ensure_index', return_value=fake_config):
            with self.assertRaises(BadSearchRequestError) as ctx:
                backend.search(_REST_QUERY, 'fake-dense', k1=0.8, b=0.3)
        self.assertIn('sparse', str(ctx.exception).lower())

    def test_search_bm25_k1_not_number_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'k1': 'x', 'b': '0.3'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('k1', response.json().get('error', ''))

    def test_bm25_config_pool_reuses_and_evicts_least_recently_used_idle_searcher(self):
        backend = SharedSearchBackend(bm25_searcher_cache_size=2)
        config = IndexConfig(name='fake-tf', index_type='tf')
        first = _FakeSearcher()
        second = _FakeSearcher()
        third = _FakeSearcher()
        bm25_a = Bm25Config(k1=0.1, b=0.1)
        bm25_b = Bm25Config(k1=0.2, b=0.2)
        bm25_c = Bm25Config(k1=0.3, b=0.3)

        with unittest.mock.patch.object(
            backend,
            '_build_searcher',
            side_effect=[first, second, third],
        ):
            searcher, key = backend._acquire_bm25_searcher('fake-tf', config, bm25_a)
            self.assertIs(searcher, first)
            backend._release_bm25_searcher('fake-tf', config, key)

            searcher, key = backend._acquire_bm25_searcher('fake-tf', config, bm25_b)
            self.assertIs(searcher, second)
            backend._release_bm25_searcher('fake-tf', config, key)

            searcher, key = backend._acquire_bm25_searcher('fake-tf', config, bm25_a)
            self.assertIs(searcher, first)
            backend._release_bm25_searcher('fake-tf', config, key)

            searcher, key = backend._acquire_bm25_searcher('fake-tf', config, bm25_c)
            self.assertIs(searcher, third)
            backend._release_bm25_searcher('fake-tf', config, key)

        self.assertFalse(first.closed)
        self.assertTrue(second.closed)
        self.assertFalse(third.closed)
        self.assertEqual(first.bm25, (0.1, 0.1))
        self.assertEqual(second.bm25, (0.2, 0.2))
        self.assertEqual(third.bm25, (0.3, 0.3))
        self.assertEqual(list(config.bm25_searchers.keys()), [bm25_a, bm25_c])

    def test_bm25_config_pool_preserves_active_searcher(self):
        backend = SharedSearchBackend(bm25_searcher_cache_size=1)
        config = IndexConfig(name='fake-tf', index_type='tf')
        first = _FakeSearcher()
        bm25_a = Bm25Config(k1=0.1, b=0.1)
        bm25_b = Bm25Config(k1=0.2, b=0.2)

        with unittest.mock.patch.object(
            backend,
            '_build_searcher',
            return_value=first,
        ) as build_searcher:
            searcher, key = backend._acquire_bm25_searcher('fake-tf', config, bm25_a)
            self.assertIs(searcher, first)
            with self.assertRaises(BadSearchRequestError):
                backend._acquire_bm25_searcher('fake-tf', config, bm25_b)
            backend._release_bm25_searcher('fake-tf', config, key)

        self.assertEqual(build_searcher.call_count, 1)
        self.assertFalse(first.closed)
        self.assertEqual(first.bm25, (0.1, 0.1))
        self.assertEqual(list(config.bm25_searchers.keys()), [bm25_a])

    def test_post_to_search_not_allowed_405(self):
        response = self.client.post(f'/{API_VERSION}/{_REST_INDEX}/search', params={'query': 'x'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json().get('error'), 'Only GET is supported')

    def test_unknown_index_name_400(self):
        response = self.client.get(
            f'/{API_VERSION}/__not_a_registered_prebuilt_index__/search',
            params={'query': 'text', 'hits': 1},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unable to open index', response.json().get('error', ''))

    def test_index_path_with_slashes_reaches_handler(self):
        """Multi-segment {index:path} must not 404 before backend (see routes/v1.py)."""
        token = 'nested/index/__not_openable__'
        response = self.client.get(
            f'/{API_VERSION}/{token}/search',
            params={'query': 'text', 'hits': 1},
        )
        self.assertEqual(response.status_code, 400, msg=response.text)
        err = response.json().get('error', '')
        self.assertIn('Unable to open index', err)
        self.assertIn(token, err)

    def test_index_absolute_path_via_double_slash(self):
        """Absolute paths need an empty segment after /v1/ so {index} includes a leading slash."""
        response = self.client.get(
            f'/{API_VERSION}//__no_such_root_index__/search',
            params={'query': 'text', 'hits': 1},
        )
        self.assertEqual(response.status_code, 400, msg=response.text)
        err = response.json().get('error', '')
        self.assertIn('Unable to open index', err)
        self.assertIn('/__no_such_root_index__', err)

    def test_doc_route_multi_segment_index_reaches_handler(self):
        response = self.client.get(f'/{API_VERSION}/nested/idx/doc/1')
        self.assertEqual(response.status_code, 400, msg=response.text)
        self.assertIn('Unable to open index', response.json().get('error', ''))
        self.assertIn('nested/idx', response.json().get('error', ''))

    def test_search_parse_false_doc_is_string(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'parse': 'false'},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        doc = response.json()['candidates'][0]['doc']
        self.assertIsInstance(doc, str)
        self.assertIn(_REST_DOC_SUBSTRING, doc)

    def test_search_max_doc_length_truncates_candidate_doc_when_parse_true(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'max_doc_length': '24'},
        )
        self.assertEqual(response.status_code, 200, msg=response.text)
        doc = response.json()['candidates'][0]['doc']
        self.assertIsInstance(doc, str)
        self.assertLessEqual(len(doc), 24)

    def test_search_max_doc_length_with_parse_false_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'parse': 'false', 'max_doc_length': '24'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('parse=true', response.json().get('error', ''))

    def test_search_max_doc_length_invalid_400(self):
        response = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1, 'max_doc_length': 'abc'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('max_doc_length', response.json().get('error', ''))

    def test_search_candidate_doc_matches_get_document(self):
        search_resp = self.client.get(
            f'/{API_VERSION}/{_REST_INDEX}/search',
            params={'query': _REST_QUERY, 'hits': 1},
        )
        self.assertEqual(search_resp.status_code, 200, msg=search_resp.text)
        cand = search_resp.json()['candidates'][0]
        docid = cand['docid']
        doc_resp = self.client.get(f'/{API_VERSION}/{_REST_INDEX}/doc/{docid}')
        self.assertEqual(doc_resp.status_code, 200, msg=doc_resp.text)
        self.assertEqual(cand['doc'], doc_resp.json()['doc'])

    def test_invalid_index_config_fails_startup(self):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write('indexes:\n  missing: /path/that/does/not/exist\n')
            path = f.name
        try:
            with self.assertRaises(ValueError):
                with TestClient(create_app(path)):
                    pass
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_without_api_keys_logs_warning(self):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write('indexes:\n  local: /tmp\n')
            path = f.name
        try:
            with self.assertLogs('pyserini.server.rest.app', level='WARNING') as cm:
                create_app(path, no_prebuilt_indexes=True)
            self.assertTrue(
                any('api_keys' in line and 'not authenticated' in line for line in cm.output),
                msg='\n'.join(cm.output),
            )
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_rejects_unconfigured_prebuilt_index(self):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write('indexes:\n  local: /tmp\n')
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                r = client.get(
                    f'/{API_VERSION}/msmarco-v1-passage/search',
                    params={'query': 'x', 'hits': 1},
                )
                self.assertEqual(r.status_code, 400, msg=r.text)
                self.assertIn('not configured', r.json().get('error', ''))
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_accepts_object_index_config(self):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write('indexes:\n  local:\n    path: /tmp\n    index_type: tf\n')
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                r = client.get(
                    f'/{API_VERSION}/local/search',
                    params={'query': 'x', 'hits': 1},
                )
                self.assertEqual(r.status_code, 400, msg=r.text)
                self.assertIn('Unable to open index', r.json().get('error', ''))
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_rejects_invalid_index_type(self):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write('indexes:\n  local:\n    path: /tmp\n    index_type: unknown\n')
            path = f.name
        try:
            with self.assertRaises(ValueError):
                create_app(path, no_prebuilt_indexes=True)
        finally:
            os.unlink(path)


class TestRestServerNoPrebuiltIndexesAuthenticated(unittest.TestCase):
    """``--no-prebuilt-indexes`` success path (temp YAML). See ``tests/resources/deploy_auth_test.yaml`` for manual runs."""

    @classmethod
    def setUpClass(cls):
        from pyserini.util import download_prebuilt_index

        cls._index_path = download_prebuilt_index(_REST_INDEX, verbose=False)

    def test_no_prebuilt_indexes_bearer_search_returns_200(self):
        token = 'no-prebuilt-indexes-integration-test-token'
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                denied = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                )
                self.assertEqual(denied.status_code, 401, msg=denied.text)
                ok = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                    headers={'Authorization': f'Bearer {token}'},
                )
                self.assertEqual(ok.status_code, 200, msg=ok.text)
                data = ok.json()
                self.assertEqual(data.get('index'), 'cacm_alias')
                self.assertEqual(data.get('query'), {'text': _REST_QUERY})
                self.assertEqual(len(data.get('candidates', [])), 1)
                self.assertEqual(data['candidates'][0].get('docid'), _REST_TOP_DOCID)
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_x_api_key_search_returns_200(self):
        token = 'no-prebuilt-indexes-integration-test-token-xak'
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                denied = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                )
                self.assertEqual(denied.status_code, 401, msg=denied.text)
                ok = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                    headers={'X-API-Key': token},
                )
                self.assertEqual(ok.status_code, 200, msg=ok.text)
                self.assertEqual(ok.json().get('index'), 'cacm_alias')
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_bearer_still_works_with_invalid_x_api_key(self):
        token = 'no-prebuilt-indexes-integration-test-token-both'
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                ok = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                    headers={'X-API-Key': 'stale-invalid-key', 'Authorization': f'Bearer {token}'},
                )
                self.assertEqual(ok.status_code, 200, msg=ok.text)
                self.assertEqual(ok.json().get('index'), 'cacm_alias')
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_logs_jsonl_key_fingerprint_for_authenticated_requests(self):
        token = 'no-prebuilt-indexes-integration-test-token-log'
        expected_key_id = hashlib.sha256(token.encode('utf-8')).hexdigest()[:12]
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                    ok = client.get(
                        f'/{API_VERSION}/cacm_alias/search',
                        params={
                            'query': _REST_QUERY,
                            'hits': 1,
                            'qid': 'q-123',
                            'question': 'Which document explains information retrieval?',
                            'run_id': 'run-456',
                            'agent': 'test-agent/1.0',
                            'step': 3,
                        },
                        headers={'X-API-Key': token},
                    )
                self.assertEqual(ok.status_code, 200, msg=ok.text)
                record = json.loads(cm.records[-1].getMessage())
                self.assertEqual(record.get('event'), 'request')
                self.assertEqual(record.get('auth'), 'authenticated')
                self.assertEqual(record.get('status'), 200)
                self.assertEqual(record.get('key_id'), expected_key_id)
                self.assertEqual(record.get('method'), 'GET')
                self.assertEqual(record.get('path'), f'/{API_VERSION}/cacm_alias/search')
                self.assertEqual(record.get('request_id'), ok.headers.get('X-Request-ID'))
                self.assertFalse(record.get('query_truncated'))
                self.assertEqual(record.get('qid'), 'q-123')
                self.assertEqual(record.get('question'), 'Which document explains information retrieval?')
                self.assertEqual(record.get('retrieval_query'), _REST_QUERY)
                self.assertEqual(record.get('run_id'), 'run-456')
                self.assertEqual(record.get('agent'), 'test-agent/1.0')
                self.assertEqual(record.get('step'), 3)
                self.assertFalse(record.get('question_truncated'))
                self.assertFalse(record.get('retrieval_query_truncated'))
                self.assertIn('latency_ms', record)
        finally:
            os.unlink(path)

    def test_no_prebuilt_indexes_logs_jsonl_auth_failure_in_same_request_log(self):
        token = 'no-prebuilt-indexes-integration-test-token-deny-log'
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                    denied = client.get(
                        f'/{API_VERSION}/cacm_alias/search',
                        params={'query': _REST_QUERY, 'hits': 1},
                        headers={'X-API-Key': 'bad-token'},
                    )
                self.assertEqual(denied.status_code, 401, msg=denied.text)
                record = json.loads(cm.records[-1].getMessage())
                self.assertEqual(record.get('event'), 'request')
                self.assertEqual(record.get('auth'), 'invalid')
                self.assertEqual(record.get('status'), 401)
                self.assertEqual(record.get('key_id'), hashlib.sha256(b'bad-token').hexdigest()[:12])
                self.assertEqual(record.get('request_id'), denied.headers.get('X-Request-ID'))
        finally:
            os.unlink(path)

    def test_anonymous_routes_log_jsonl_request(self):
        with TestClient(create_app()) as client:
            with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                response = client.get('/')
            self.assertEqual(response.status_code, 200, msg=response.text)
        record = json.loads(cm.records[-1].getMessage())
        self.assertEqual(record.get('event'), 'request')
        self.assertEqual(record.get('auth'), 'not_configured')
        self.assertEqual(record.get('status'), 200)
        self.assertEqual(record.get('path'), '/')
        self.assertEqual(record.get('request_id'), response.headers.get('X-Request-ID'))
        self.assertFalse(record.get('query_truncated'))
        self.assertIsNone(record.get('qid'))
        self.assertIsNone(record.get('question'))
        self.assertIsNone(record.get('retrieval_query'))
        self.assertIsNone(record.get('run_id'))
        self.assertIsNone(record.get('agent'))
        self.assertIsNone(record.get('step'))

    def test_request_id_is_server_generated_and_ignores_incoming_headers(self):
        client_request_id = 'req-test-123'
        with TestClient(create_app()) as client:
            with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                response = client.get(
                    '/',
                    headers={
                        'X-Request-ID': client_request_id,
                        'X-Correlation-ID': 'corr-test-123',
                    },
                )
            self.assertEqual(response.status_code, 200, msg=response.text)
            self.assertNotEqual(response.headers.get('X-Request-ID'), client_request_id)
        record = json.loads(cm.records[-1].getMessage())
        self.assertEqual(record.get('request_id'), response.headers.get('X-Request-ID'))

    def test_long_query_string_is_truncated_in_request_log(self):
        query = 'q=' + ('x' * 1200)
        with TestClient(create_app()) as client:
            with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                response = client.get('/?' + query)
            self.assertEqual(response.status_code, 200, msg=response.text)
        record = json.loads(cm.records[-1].getMessage())
        self.assertEqual(len(record.get('query')), 1000)
        self.assertTrue(record.get('query_truncated'))

    def test_long_question_is_truncated_in_structured_trace(self):
        question = 'q' * 9000
        with TestClient(create_app()) as client:
            with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                response = client.get('/', params={'question': question})
            self.assertEqual(response.status_code, 200, msg=response.text)
        record = json.loads(cm.records[-1].getMessage())
        self.assertEqual(len(record.get('question')), 8192)
        self.assertTrue(record.get('question_truncated'))

    def test_keep_uvicorn_logs_routes_access_to_request_log_file(self):
        config = _build_uvicorn_log_config(
            'requests.jsonl',
            keep_uvicorn_logs=True,
        )
        access_handlers = config['loggers']['uvicorn.access']['handlers']
        self.assertEqual(access_handlers, ['uvicorn_access_request_file'])
        self.assertEqual(config['handlers']['uvicorn_access_request_file']['filename'], 'requests.jsonl')


class RecordingTokenEmailSender:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.deliveries: list[dict[str, str]] = []

    def send(self, *, name: str, email: str, token: str) -> None:
        if self.fail:
            raise RuntimeError('simulated SMTP failure')
        self.deliveries.append({'name': name, 'email': email, 'token': token})


class TestRestTokenIssuance(unittest.TestCase):
    @staticmethod
    def _identity(name: str = 'Test User', email: str = 'test@example.edu') -> dict[str, str]:
        return {'name': name, 'email': email}

    @staticmethod
    def _write_config(root: str, token: str = 'existing-token') -> str:
        path = os.path.join(root, 'server.yaml')
        with open(path, 'w', encoding='utf-8') as f:
            yaml.safe_dump({'indexes': {'local': '/tmp'}, 'api_keys': [token]}, f, sort_keys=False)
        os.chmod(path, 0o600)
        return path

    @staticmethod
    def _write_pool(root: str, count: int = 3) -> str:
        path = os.path.join(root, 'lookup.json')
        entries = [
            {'token': f'{i + 1:064x}', 'name': None, 'email': None, 'issued_at': None}
            for i in range(count)
        ]
        Path(path).write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
        os.chmod(path, 0o600)
        return path

    def test_token_issuance_requires_config(self):
        with self.assertRaises(ValueError):
            create_app(
                enable_token_issuance=True,
                token_pool_path='/missing/pool.json',
                token_email_sender=RecordingTokenEmailSender(),
            )

    def test_token_issuance_requires_pool_and_email_sender(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = self._write_config(tmp)
            pool_path = self._write_pool(tmp)
            with self.assertRaisesRegex(ValueError, 'pre-generated token pool'):
                create_app(
                    config_path,
                    enable_token_issuance=True,
                    token_email_sender=RecordingTokenEmailSender(),
                )
            with self.assertRaisesRegex(ValueError, 'email sender'):
                create_app(
                    config_path,
                    enable_token_issuance=True,
                    token_pool_path=pool_path,
                )

    def test_disabled_token_issuance_returns_503(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            with TestClient(create_app(path)) as client:
                response = client.post(f'/{API_VERSION}/token', json=self._identity())
            self.assertEqual(response.status_code, 503, msg=response.text)
            self.assertNotIn('api_key', response.json())

    def test_issued_token_is_persisted_and_accepted_without_restart(self):
        existing_token = 'existing-token'
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp, existing_token)
            pool_path = self._write_pool(tmp)
            email_sender = RecordingTokenEmailSender()
            issuance_app = create_app(
                path,
                no_prebuilt_indexes=True,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=0,
                token_pool_path=pool_path,
                token_email_sender=email_sender,
            )
            self.assertFalse(issuance_app.state.accepted_api_tokens.is_valid(f'{1:064x}'))
            with TestClient(issuance_app) as client:
                denied = client.get(
                    f'/{API_VERSION}/local/search',
                    params={'query': 'test', 'hits': 1},
                )
                self.assertEqual(denied.status_code, 401, msg=denied.text)

                with self.assertLogs('pyserini.server.rest.request', level='INFO') as cm:
                    issued = client.post(f'/{API_VERSION}/token', json=self._identity())
                self.assertEqual(issued.status_code, 202, msg=issued.text)
                self.assertEqual(issued.json().get('status'), 'accepted')
                self.assertNotIn('api_key', issued.json())
                self.assertNotIn('token', issued.json())
                self.assertEqual(len(email_sender.deliveries), 1)
                token = email_sender.deliveries[0]['token']
                self.assertEqual(token, f'{1:064x}')
                self.assertEqual(email_sender.deliveries[0]['email'], 'test@example.edu')
                self.assertEqual(issued.headers.get('cache-control'), 'no-store')
                self.assertEqual(issued.headers.get('pragma'), 'no-cache')
                log_messages = '\n'.join(record.getMessage() for record in cm.records)
                self.assertNotIn(token, log_messages)
                self.assertNotIn('Test User', log_messages)
                self.assertNotIn('test@example.edu', log_messages)
                log_record = json.loads(cm.records[-1].getMessage())
                self.assertEqual(log_record.get('auth'), 'token_issuance')
                self.assertEqual(log_record.get('status'), 202)

                accepted = issuance_app.state.accepted_api_tokens
                self.assertTrue(accepted.is_valid(existing_token))
                self.assertTrue(accepted.is_valid(token))

                existing_authorized = client.get(
                    f'/{API_VERSION}/local/search',
                    params={'query': 'test', 'hits': 1},
                    headers={'X-API-Key': existing_token},
                )
                self.assertNotEqual(existing_authorized.status_code, 401, msg=existing_authorized.text)

                authorized = client.get(
                    f'/{API_VERSION}/local/search',
                    params={'query': 'test', 'hits': 1},
                    headers={'Authorization': f'Bearer {token}'},
                )
                self.assertNotEqual(authorized.status_code, 401, msg=authorized.text)

            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(persisted['api_keys'], [existing_token, token])
            self.assertEqual(
                persisted['api_key_identities'][token],
                {'name': 'Test User', 'email': 'test@example.edu'},
            )
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            pool = json.loads(Path(pool_path).read_text(encoding='utf-8'))
            self.assertEqual(pool[0]['name'], 'Test User')
            self.assertEqual(pool[0]['email'], 'test@example.edu')
            self.assertIsInstance(pool[0]['issued_at'], int)
            self.assertIsNone(pool[1]['email'])

            restarted_app = create_app(path, no_prebuilt_indexes=True)
            self.assertTrue(restarted_app.state.accepted_api_tokens.is_valid(existing_token))
            self.assertTrue(restarted_app.state.accepted_api_tokens.is_valid(token))

    def test_token_issuance_cooldown_returns_429_without_persisting_another_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            pool_path = self._write_pool(tmp)
            email_sender = RecordingTokenEmailSender()
            issuance_app = create_app(
                path,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=60,
                token_pool_path=pool_path,
                token_email_sender=email_sender,
            )
            with TestClient(issuance_app) as client:
                first = client.post(
                    f'/{API_VERSION}/token',
                    json=self._identity(name='First User', email='first@example.edu'),
                )
                second = client.post(
                    f'/{API_VERSION}/token',
                    json=self._identity(name='First User Again', email=' FIRST@EXAMPLE.EDU '),
                )
                same_ip_different_email = client.post(
                    f'/{API_VERSION}/token',
                    json=self._identity(name='Second User', email='second@example.edu'),
                )
            self.assertEqual(first.status_code, 202, msg=first.text)
            self.assertEqual(second.status_code, 429, msg=second.text)
            self.assertEqual(same_ip_different_email.status_code, 429, msg=same_ip_different_email.text)
            self.assertGreaterEqual(int(same_ip_different_email.headers.get('retry-after', '0')), 1)
            self.assertEqual(len(email_sender.deliveries), 1)
            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(len(persisted['api_keys']), 2)
            self.assertEqual(len(persisted['api_key_identities']), 1)
            self.assertEqual(
                next(iter(persisted['api_key_identities'].values())),
                {'name': 'First User', 'email': 'first@example.edu'},
            )

    def test_token_issuance_requires_valid_name_and_email(self):
        invalid_requests = [
            None,
            {},
            {'name': 'Test User'},
            {'email': 'test@example.edu'},
            self._identity(name=''),
            self._identity(email='not-an-email'),
            self._identity(email='test @example.edu'),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            issuance_app = create_app(
                path,
                enable_token_issuance=True,
                token_pool_path=self._write_pool(tmp),
                token_email_sender=RecordingTokenEmailSender(),
            )
            with TestClient(issuance_app) as client:
                responses = [client.post(f'/{API_VERSION}/token', json=payload) for payload in invalid_requests]

            self.assertTrue(all(response.status_code == 400 for response in responses))
            self.assertTrue(all('test @example.edu' not in response.text for response in responses))
            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(persisted['api_keys'], ['existing-token'])

    def test_token_issuance_cooldown_prunes_expired_clients(self):
        from pyserini.server.rest.app import TokenIssuanceCooldown

        cooldown = TokenIssuanceCooldown(10)
        cooldown.reserve('first-client', 'first@example.edu', 0)
        cooldown.reserve('second-client', 'second@example.edu', 5)
        cooldown.reserve('third-client', 'third@example.edu', 11)

        self.assertNotIn('first-client', cooldown._last_issued_by_client)
        self.assertNotIn('first@example.edu', cooldown._last_issued_by_email)
        self.assertIn('second-client', cooldown._last_issued_by_client)
        self.assertIn('second@example.edu', cooldown._last_issued_by_email)

    def test_token_issuance_cooldown_requires_both_new_ip_and_email(self):
        from pyserini.server.rest.app import TokenIssuanceCooldown

        cooldown = TokenIssuanceCooldown(60)
        first_retry, _ = cooldown.reserve('first-client', 'first@example.edu', 0)
        same_ip_retry, _ = cooldown.reserve('first-client', 'second@example.edu', 1)
        same_email_retry, _ = cooldown.reserve('second-client', 'first@example.edu', 1)
        both_new_retry, _ = cooldown.reserve('second-client', 'second@example.edu', 1)

        self.assertIsNone(first_retry)
        self.assertIsNotNone(same_ip_retry)
        self.assertIsNotNone(same_email_retry)
        self.assertIsNone(both_new_retry)

    def test_token_issuance_resends_same_lifetime_token_after_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            pool_path = self._write_pool(tmp)
            first_sender = RecordingTokenEmailSender()
            first_app = create_app(
                path,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=0,
                token_pool_path=pool_path,
                token_email_sender=first_sender,
            )
            with TestClient(first_app) as client:
                first = client.post(
                    f'/{API_VERSION}/token',
                    json=self._identity(name='First User', email='first@example.edu'),
                )
            self.assertEqual(first.status_code, 202, msg=first.text)
            first_token = first_sender.deliveries[0]['token']

            second_sender = RecordingTokenEmailSender()
            restarted_app = create_app(
                path,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=0,
                token_pool_path=pool_path,
                token_email_sender=second_sender,
            )
            with TestClient(restarted_app) as client:
                duplicate = client.post(
                    f'/{API_VERSION}/token',
                    json=self._identity(name='Renamed User', email=' FIRST@EXAMPLE.EDU '),
                )
            self.assertEqual(duplicate.status_code, 202, msg=duplicate.text)
            self.assertEqual(second_sender.deliveries[0]['token'], first_token)
            self.assertNotIn('api_key', duplicate.json())
            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(len(persisted['api_keys']), 2)
            self.assertEqual(len(persisted['api_key_identities']), 1)
            pool = json.loads(Path(pool_path).read_text(encoding='utf-8'))
            self.assertEqual(sum(entry['email'] is None for entry in pool), 2)

    def test_token_pool_exhaustion_returns_503_without_changing_auth(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            pool_path = self._write_pool(tmp, count=0)
            email_sender = RecordingTokenEmailSender()
            issuance_app = create_app(
                path,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=0,
                token_pool_path=pool_path,
                token_email_sender=email_sender,
            )
            with TestClient(issuance_app) as client:
                response = client.post(f'/{API_VERSION}/token', json=self._identity())

            self.assertEqual(response.status_code, 503, msg=response.text)
            self.assertNotIn('api_key', response.json())
            self.assertEqual(email_sender.deliveries, [])
            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(persisted['api_keys'], ['existing-token'])

    def test_email_failure_can_retry_same_claimed_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            pool_path = self._write_pool(tmp, count=1)
            email_sender = RecordingTokenEmailSender(fail=True)
            issuance_app = create_app(
                path,
                enable_token_issuance=True,
                token_issuance_cooldown_sec=60,
                token_pool_path=pool_path,
                token_email_sender=email_sender,
            )
            with TestClient(issuance_app) as client:
                failed = client.post(f'/{API_VERSION}/token', json=self._identity())
                email_sender.fail = False
                retried = client.post(f'/{API_VERSION}/token', json=self._identity())

            self.assertEqual(failed.status_code, 503, msg=failed.text)
            self.assertEqual(retried.status_code, 202, msg=retried.text)
            self.assertNotIn('api_key', retried.json())
            self.assertEqual(len(email_sender.deliveries), 1)
            persisted = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(len(persisted['api_keys']), 2)
            self.assertEqual(email_sender.deliveries[0]['token'], persisted['api_keys'][1])
            pool = json.loads(Path(pool_path).read_text(encoding='utf-8'))
            self.assertEqual(pool[0]['email'], 'test@example.edu')

    def test_get_token_endpoint_returns_post_only_405(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_config(tmp)
            issuance_app = create_app(
                path,
                enable_token_issuance=True,
                token_pool_path=self._write_pool(tmp),
                token_email_sender=RecordingTokenEmailSender(),
            )
            with TestClient(issuance_app) as client:
                response = client.get(f'/{API_VERSION}/token')
            self.assertEqual(response.status_code, 405, msg=response.text)
            self.assertEqual(response.json().get('error'), 'Only POST is supported')


class TestRestBackpressure(unittest.TestCase):
    """p99-based shedding rejects the busiest API key in the last minute (429)."""

    @classmethod
    def setUpClass(cls):
        from pyserini.util import download_prebuilt_index

        cls._index_path = download_prebuilt_index(_REST_INDEX, verbose=False)

    def test_backpressure_429_for_heaviest_api_key_when_p99_high(self):
        from pyserini.server.rest.app import RestBackpressure, _compute_token_fingerprint

        token_heavy = 'backpressure-test-token-heavy'
        token_light = 'backpressure-test-token-light'
        cfg = {
            'indexes': {'cacm_alias': self._index_path},
            'api_keys': [token_heavy, token_light],
        }
        now = time.perf_counter()
        heavy_id = _compute_token_fingerprint(token_heavy)
        light_id = _compute_token_fingerprint(token_light)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            app = create_app(path, no_prebuilt_indexes=True, load_shedding_threshold_ms=0.0)
            bp = app.state.rest_backpressure
            self.assertIsInstance(bp, RestBackpressure)
            with bp._lock:
                bp._latencies.clear()
                bp._key_hits.clear()
                for _ in range(100):
                    bp._latencies.append((now, 1000.0))
                for _ in range(50):
                    bp._key_hits.append((now, heavy_id))
                for _ in range(3):
                    bp._key_hits.append((now, light_id))

            with TestClient(app) as client:
                r_heavy = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                    headers={'Authorization': f'Bearer {token_heavy}'},
                )
                self.assertEqual(r_heavy.status_code, 429, msg=r_heavy.text)
                self.assertIn('overloaded', r_heavy.json().get('error', '').lower())
                self.assertEqual(r_heavy.headers.get('retry-after'), '1')

                r_light = client.get(
                    f'/{API_VERSION}/cacm_alias/search',
                    params={'query': _REST_QUERY, 'hits': 1},
                    headers={'Authorization': f'Bearer {token_light}'},
                )
                self.assertEqual(r_light.status_code, 200, msg=r_light.text)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()

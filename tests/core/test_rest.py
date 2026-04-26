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
import unittest
import hashlib

import yaml
from fastapi.testclient import TestClient

from pyserini.server.rest.app import API_VERSION, ROUTE_ERROR, app, create_app

# Small prebuilt TF index (see TF_INDEX_INFO["cacm"]); stable BM25 top-1 for this query.
_REST_INDEX = 'cacm'
_REST_QUERY = 'information retrieval'
_REST_TOP_DOCID = 'CACM-3134'
_REST_DOC_SUBSTRING = 'Information Storage and Retrieval'


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
        search_responses = data['paths']['/{index}/search']['get']['responses']
        self.assertIn('401', search_responses)

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

    def test_no_prebuilt_indexes_logs_key_fingerprint_for_authenticated_requests(self):
        token = 'no-prebuilt-indexes-integration-test-token-log'
        expected_key_id = hashlib.sha256(token.encode('utf-8')).hexdigest()[:12]
        cfg = {'indexes': {'cacm_alias': self._index_path}, 'api_keys': [token]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.safe_dump(cfg, f, default_flow_style=False)
            path = f.name
        try:
            with TestClient(create_app(path, no_prebuilt_indexes=True)) as client:
                with self.assertLogs('pyserini.server.rest.auth', level='INFO') as cm:
                    ok = client.get(
                        f'/{API_VERSION}/cacm_alias/search',
                        params={'query': _REST_QUERY, 'hits': 1},
                        headers={'X-API-Key': token},
                    )
                self.assertEqual(ok.status_code, 200, msg=ok.text)
                self.assertTrue(
                    any(f'auth_request' in line and f'key_id={expected_key_id}' in line for line in cm.output),
                    msg='\n'.join(cm.output),
                )
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()

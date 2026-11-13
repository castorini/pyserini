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

import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch

import yaml
from fastapi.testclient import TestClient

# As in test_rest.py, importing the REST application requires the search dependencies.
from pyserini.server.rest.app import create_app, main


class TestRestGlobalAdmission(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.config = Path(directory.name) / 'server.yaml'
        self.tokens = [f'test-token-{i}' for i in range(200)]
        self.config.write_text(yaml.safe_dump({'api_keys': self.tokens}), encoding='utf-8')
        backend_patch = patch('pyserini.server.rest.app.SharedSearchBackend')
        self.backend = backend_patch.start().return_value
        self.addCleanup(backend_patch.stop)
        self.backend.decode_path_segment.side_effect = lambda value: value
        self.backend.search.return_value = {'candidates': []}
        self.backend.get_document.return_value = {'contents': 'example'}
        clock_patch = patch('pyserini.server.admission.monotonic', return_value=100.0)
        self.clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)
        log_patch = patch('pyserini.server.rest.app._log_request_jsonl')
        self.logged = log_patch.start()
        self.addCleanup(log_patch.stop)

    def client(self, limit=None, **kwargs):
        application = create_app(str(self.config), global_requests_per_second=limit, **kwargs)
        client = TestClient(application, raise_server_exceptions=False)
        client.__enter__()
        self.addCleanup(client.__exit__, None, None, None)
        return client

    def get(self, client, token=0, path='/v1/local/search', **kwargs):
        return client.get(path, headers={'X-API-Key': self.tokens[token]}, params={'query': 'test'}, **kwargs)

    def test_many_distinct_keys_share_a_global_cap_before_latency_samples(self):
        client = self.client(30)
        with ThreadPoolExecutor(max_workers=32) as executor:
            responses = list(executor.map(lambda i: self.get(client, i), range(200)))
        statuses = [response.status_code for response in responses]
        self.assertEqual(statuses.count(200), 30)
        self.assertEqual(statuses.count(429), 170)
        self.assertEqual(self.backend.search.call_count, 30)
        for response in responses:
            self.assertIn('X-Request-ID', response.headers)
            if response.status_code == 429:
                self.assertEqual(response.headers['Retry-After'], '1')
                self.assertIn('Global request limit', response.json()['error'])

    def test_budget_is_shared_across_headers_indexes_and_routes(self):
        client = self.client(2)
        first = client.get('/v1/local/search?query=test', headers={'Authorization': f'Bearer {self.tokens[0]}'})
        second = self.get(client, 1, path='/v1/another/doc/example')
        blocked = client.get(
            '/v1/third/search?query=test',
            headers={'Authorization': f'Bearer {self.tokens[2]}', 'X-API-Key': 'invalid'},
        )
        self.assertEqual([first.status_code, second.status_code, blocked.status_code], [200, 200, 429])
        self.backend.search.assert_called_once()
        self.backend.get_document.assert_called_once()
        entry = self.logged.call_args.args[0]
        self.assertEqual(entry['auth'], 'authenticated')
        self.assertTrue(entry['global_rate_limited'])
        self.assertEqual(entry['status'], 429)
        self.assertEqual(entry['request_id'], blocked.headers['X-Request-ID'])
        self.assertNotIn(self.tokens[2], str(entry))

    def test_many_light_keys_are_capped_even_when_p99_sheds_none(self):
        client = self.client(10, load_shedding_threshold_ms=1000.0)
        backpressure = client.app.state.rest_backpressure
        now = time.perf_counter()
        for _ in range(20):
            backpressure.record_latency(5000.0, now)
        responses = [self.get(client, i) for i in range(40)]
        self.assertEqual([response.status_code for response in responses], [200] * 10 + [429] * 30)
        self.assertEqual(self.backend.search.call_count, 10)
        self.assertEqual(backpressure._max_count, 1)

    def test_authentication_and_exempt_routes_do_not_consume_budget(self):
        client = self.client(1)
        for _ in range(2):
            self.assertEqual(client.get('/v1/local/search?query=test').status_code, 401)
            self.assertEqual(client.get('/v1/local/search?query=test', headers={'X-API-Key': 'wrong'}).status_code, 401)
            for path in ('/', '/docs', '/openapi.yaml', '/openapi.json'):
                self.assertEqual(client.get(path).status_code, 200)
            self.assertEqual(client.get('/v1/token').status_code, 405)
            self.assertEqual(client.post('/v1/token', json={'name': 'Test', 'email': 'test@example.org'}).status_code, 503)
        self.assertEqual(self.get(client).status_code, 200)
        self.assertEqual(self.get(client, 1).status_code, 429)
        self.assertEqual(client.get('/v1/local/search?query=test').status_code, 401)
        self.assertEqual(client.get('/').status_code, 200)
        self.assertEqual(client.get('/docs').status_code, 200)
        self.assertEqual(client.post('/v1/token', json={'name': 'Test', 'email': 'test@example.org'}).status_code, 503)

    def test_other_client_ips_share_budget_and_apps_are_independent(self):
        client = self.client(1)
        self.assertEqual(self.get(client).status_code, 200)
        with TestClient(client.app, client=('other-client', 4567)) as other_client:
            self.assertEqual(self.get(other_client, 1).status_code, 429)
        fresh_client = self.client(1)
        self.assertEqual(self.get(fresh_client, 1).status_code, 200)

    def test_both_valid_credentials_only_consume_one_slot(self):
        client = self.client(2)
        response = client.get('/v1/local/search?query=test', headers={
            'Authorization': f'Bearer {self.tokens[0]}', 'X-API-Key': self.tokens[1],
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get(client, 2).status_code, 200)
        self.assertEqual(self.get(client, 3).status_code, 429)

    def test_rejected_requests_do_not_extend_retry_window(self):
        client = self.client(1)
        self.assertEqual(self.get(client).status_code, 200)
        self.clock.return_value = 100.5
        self.assertEqual(self.get(client, 1).status_code, 429)
        self.clock.return_value = 100.999
        self.assertEqual(self.get(client, 2).status_code, 429)
        self.clock.return_value = 101.0
        self.assertEqual(self.get(client, 3).status_code, 200)
        self.assertEqual(self.get(client, 4).status_code, 429)

    def test_authenticated_client_errors_consume_slots(self):
        for method, path, expected in (
            ('GET', '/v1/local/search', 400),
            ('GET', '/v1/no-such-route', 404),
            ('POST', '/v1/local/search?query=test', 405),
        ):
            with self.subTest(status=expected):
                client = self.client(1)
                response = client.request(method, path, headers={'X-API-Key': self.tokens[0]})
                self.assertEqual(response.status_code, expected)
                self.assertEqual(self.get(client, 1).status_code, 429)
        self.backend.search.assert_not_called()

    def test_backend_failure_consumes_slot_and_window_recovers(self):
        client = self.client(1)
        self.backend.search.side_effect = RuntimeError('backend failed')
        with patch('pyserini.server.rest.app.logger'):
            response = self.get(client)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(self.get(client, 1).status_code, 429)
        self.backend.search.assert_called_once()
        self.backend.search.side_effect = None
        self.clock.return_value = 101.0
        self.assertEqual(self.get(client, 2).status_code, 200)

    def test_global_gate_precedes_latency_shedding(self):
        client = self.client(1)
        backpressure = Mock()
        backpressure.should_shed.return_value = True
        client.app.state.rest_backpressure = backpressure
        first = self.get(client)
        blocked = self.get(client, 1)
        self.assertEqual([first.status_code, blocked.status_code], [429, 429])
        self.assertIn('overloaded', first.json()['error'])
        self.assertIn('Global request limit', blocked.json()['error'])
        backpressure.should_shed.assert_called_once()
        backpressure.record_latency.assert_not_called()
        self.backend.search.assert_not_called()

    def test_default_is_disabled_and_unconfigured_auth_is_unlimited(self):
        client = self.client()
        self.assertIsNone(client.app.state.global_request_limiter)
        self.assertEqual([self.get(client, i).status_code for i in range(60)], [200] * 60)
        with TestClient(create_app(global_requests_per_second=1)) as public_client:
            self.assertEqual([public_client.get('/v1/local/search?query=test').status_code for _ in range(3)], [200] * 3)

    def test_new_tokens_do_not_get_a_new_global_budget(self):
        client = self.client(1)
        self.assertEqual(self.get(client).status_code, 200)
        client.app.state.accepted_api_tokens.add('newly-issued-token')
        self.assertEqual(client.get('/v1/local/search?query=test', headers={'X-API-Key': 'newly-issued-token'}).status_code, 429)

    def test_invalid_python_and_cli_configuration(self):
        for value in (0, -1, True, 2.5):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'positive integer'):
                create_app(str(self.config), global_requests_per_second=value)
        for value in ('0', '-1'):
            with self.subTest(value=value), patch('sys.argv', ['rest', '--global-requests-per-second', value]):
                with self.assertRaisesRegex(SystemExit, '--global-requests-per-second must be positive'):
                    main()

    def test_cli_passes_limit_and_preserves_default(self):
        for value in (None, 25):
            args = ['rest'] if value is None else ['rest', '--global-requests-per-second', str(value)]
            with self.subTest(value=value), patch('sys.argv', args), patch('uvicorn.run') as run:
                main()
                application = run.call_args.args[0]
                limiter = application.state.global_request_limiter
                if value is None:
                    self.assertIsNone(limiter)
                else:
                    self.assertEqual([limiter.retry_after() for _ in range(value + 1)], [0] * value + [1])


if __name__ == '__main__':
    unittest.main()

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

import concurrent.futures
import json
import os
import tempfile
import unittest
from pathlib import Path

import yaml

# Keep this test in tests/core: server config imports shared server utilities that include Faiss-backed index types.
from pyserini.server.config import (
    AcceptedApiTokens,
    ApiTokenEmailAlreadyIssuedError,
    ApiTokenPoolExhaustedError,
    ApiTokenStore,
    PreGeneratedApiTokenPool,
    load_server_config,
    load_token_issuance_config,
)


class TestServerConfigParsing(unittest.TestCase):
    def test_rejects_non_mapping_yaml_root_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / 'server.yaml'
            cfg_path.write_text('- just\n- a\n- list\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                load_server_config(str(cfg_path))

    def test_rejects_non_mapping_yaml_root_scalar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / 'server.yaml'
            cfg_path.write_text('hello\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                load_server_config(str(cfg_path))

    def test_parses_string_and_object_index_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tf_dir = root / 'tf'
            dense_dir = root / 'dense'
            tf_dir.mkdir()
            dense_dir.mkdir()
            cfg_path = root / 'server.yaml'
            cfg = {
                'indexes': {
                    'tf_alias': str(tf_dir),
                    'dense_alias': {
                        'path': str(dense_dir),
                        'index_type': 'lucene_flat',
                        'base_index': 'tf_alias',
                        'encoder': 'BAAI/bge-base-en-v1.5',
                    },
                },
                'api_keys': ['k1'],
            }
            cfg_path.write_text(yaml.safe_dump(cfg), encoding='utf-8')

            indexes, api_keys = load_server_config(str(cfg_path))

            self.assertEqual(api_keys, ['k1'])
            self.assertIn('tf_alias', indexes)
            self.assertIn('dense_alias', indexes)
            self.assertEqual(indexes['tf_alias'].index_type, 'tf')
            self.assertEqual(indexes['dense_alias'].index_type, 'lucene_flat')
            self.assertEqual(indexes['dense_alias'].base_index, 'tf_alias')
            self.assertEqual(indexes['dense_alias'].encoder, 'BAAI/bge-base-en-v1.5')

    def test_rejects_unknown_index_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            idx = root / 'idx'
            idx.mkdir()
            cfg_path = root / 'server.yaml'
            cfg = {'indexes': {'bad': {'path': str(idx), 'index_type': 'unknown'}}}
            cfg_path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_server_config(str(cfg_path))

    def test_rejects_non_tf_base_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dense_a = root / 'dense_a'
            dense_b = root / 'dense_b'
            dense_a.mkdir()
            dense_b.mkdir()
            cfg_path = root / 'server.yaml'
            cfg = {
                'indexes': {
                    'dense_a': {'path': str(dense_a), 'index_type': 'lucene_flat', 'encoder': 'enc-a'},
                    'dense_b': {
                        'path': str(dense_b),
                        'index_type': 'lucene_flat',
                        'encoder': 'enc-b',
                        'base_index': 'dense_a',
                    },
                }
            }
            cfg_path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_server_config(str(cfg_path))

    def test_rejects_missing_encoder_for_dense_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            idx = root / 'idx'
            idx.mkdir()
            cfg_path = root / 'server.yaml'
            cfg = {'indexes': {'dense': {'path': str(idx), 'index_type': 'lucene_hnsw'}}}
            cfg_path.write_text(yaml.safe_dump(cfg), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_server_config(str(cfg_path))

    def test_loads_token_issuance_config_with_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg_path = root / 'server.yaml'
            cfg_path.write_text(
                yaml.safe_dump(
                    {
                        'token_issuance': {
                            'pool': 'secrets/lookup.json',
                            'cooldown_seconds': 300,
                            'smtp': {
                                'host': 'smtp.example.edu',
                                'port': 465,
                                'security': 'ssl',
                                'username': 'api@example.edu',
                                'password_file': 'secrets/smtp-password',
                                'sender': 'api@example.edu',
                                'cc': ['operator@example.edu'],
                                'timeout_seconds': 10,
                            },
                        }
                    }
                ),
                encoding='utf-8',
            )

            config = load_token_issuance_config(str(cfg_path))

            self.assertIsNotNone(config)
            self.assertEqual(config.pool_path, str((root / 'secrets/lookup.json').resolve()))
            self.assertEqual(config.smtp_password_file, str((root / 'secrets/smtp-password').resolve()))
            self.assertEqual(config.cooldown_sec, 300)
            self.assertEqual(config.smtp_host, 'smtp.example.edu')
            self.assertEqual(config.smtp_port, 465)
            self.assertEqual(config.smtp_security, 'ssl')
            self.assertEqual(config.smtp_username, 'api@example.edu')
            self.assertEqual(config.email_from, 'api@example.edu')
            self.assertEqual(config.email_cc, ('operator@example.edu',))
            self.assertEqual(config.smtp_timeout_sec, 10)

    def test_rejects_invalid_token_issuance_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            cfg_path.write_text(
                yaml.safe_dump(
                    {
                        'token_issuance': {
                            'pool': 'lookup.json',
                            'smtp': {
                                'host': 'smtp.example.edu',
                                'sender': 'api@example.edu',
                                'cc': 'operator@example.edu',
                            },
                        }
                    }
                ),
                encoding='utf-8',
            )

            with self.assertRaisesRegex(ValueError, 'smtp.cc'):
                load_token_issuance_config(str(cfg_path))

    def test_api_token_store_appends_token_and_preserves_config_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            cfg = {
                'indexes': {'local': '/tmp'},
                'api_keys': ['existing-key'],
                'api_key_identities': {
                    'existing-key': {
                        'name': 'Existing User',
                        'email': 'existing@example.edu',
                        'team': 'IR Lab',
                    }
                },
                'custom': {'keep': True},
            }
            cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding='utf-8')
            cfg_path.chmod(0o600)

            store = ApiTokenStore(str(cfg_path))
            token = store.activate('a' * 64, name='Test User', email=' Test@Example.EDU ')

            self.assertEqual(token, 'a' * 64)
            persisted = yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
            self.assertEqual(persisted['api_keys'], ['existing-key', token])
            self.assertEqual(
                persisted['api_key_identities']['existing-key'],
                cfg['api_key_identities']['existing-key'],
            )
            self.assertEqual(
                persisted['api_key_identities'][token],
                {'name': 'Test User', 'email': 'test@example.edu'},
            )
            self.assertEqual(store.token_for_email('TEST@example.edu'), token)
            self.assertIsNone(store.token_for_email('other@example.edu'))
            self.assertEqual(persisted['indexes'], cfg['indexes'])
            self.assertEqual(persisted['custom'], cfg['custom'])
            self.assertEqual(os.stat(cfg_path).st_mode & 0o777, 0o600)

    def test_api_token_store_serializes_concurrent_activation(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            cfg_path.write_text('indexes:\n  local: /tmp\napi_keys:\n  - existing-key\n', encoding='utf-8')
            store = ApiTokenStore(str(cfg_path))

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                tokens = list(
                    executor.map(
                        lambda i: store.activate(
                            f'{i + 1:064x}',
                            name=f'Test User {i}',
                            email=f'test-{i}@example.edu',
                        ),
                        range(24),
                    )
                )

            self.assertEqual(len(tokens), len(set(tokens)))
            persisted = yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
            self.assertEqual(len(persisted['api_keys']), 25)
            self.assertEqual(set(persisted['api_keys'][1:]), set(tokens))
            self.assertEqual(set(persisted['api_key_identities']), set(tokens))
            for i, token in enumerate(tokens):
                self.assertEqual(
                    persisted['api_key_identities'][token],
                    {'name': f'Test User {i}', 'email': f'test-{i}@example.edu'},
                )

    def test_api_token_store_rejects_invalid_api_keys_without_modifying_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            original = 'indexes:\n  local: /tmp\napi_keys: invalid\n'
            cfg_path.write_text(original, encoding='utf-8')

            with self.assertRaises(ValueError):
                ApiTokenStore(str(cfg_path)).activate(
                    'a' * 64,
                    name='Test User',
                    email='test@example.edu',
                )

            self.assertEqual(cfg_path.read_text(encoding='utf-8'), original)

    def test_pre_generated_pool_claims_only_exact_all_null_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            pool_path = Path(tmp) / 'lookup.json'
            entries = [
                {
                    'token': 'a' * 64,
                    'name': 'Assigned User',
                    'email': 'assigned@example.edu',
                    'issued_at': 123,
                },
                {
                    'token': 'b' * 64,
                    'name': 'Legacy Reserved User',
                    'email': None,
                    'issued_at': 123,
                },
                {
                    'token': 'f' * 64,
                    'name': 'Partially Assigned User',
                    'email': 'new@example.edu',
                    'issued_at': None,
                },
                {'token': 'e' * 64, 'name': None, 'email': None},
                {'token': 'c' * 64, 'name': None, 'email': None, 'issued_at': None},
                {'token': 'd' * 64, 'name': None, 'email': None, 'issued_at': None},
            ]
            pool_path.write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
            pool_path.chmod(0o600)
            pool = PreGeneratedApiTokenPool(str(pool_path))

            claimed = pool.claim(name='New User', email=' NEW@EXAMPLE.EDU ')
            claimed_again = pool.claim(name='Renamed User', email='new@example.edu')

            self.assertEqual(claimed, 'c' * 64)
            self.assertEqual(claimed_again, claimed)
            persisted = json.loads(pool_path.read_text(encoding='utf-8'))
            self.assertEqual(persisted[:4], entries[:4])
            self.assertEqual(persisted[4]['name'], 'New User')
            self.assertEqual(persisted[4]['email'], 'new@example.edu')
            self.assertIsInstance(persisted[4]['issued_at'], int)
            self.assertEqual(
                persisted[5],
                {'token': 'd' * 64, 'name': None, 'email': None, 'issued_at': None},
            )
            self.assertEqual(os.stat(pool_path).st_mode & 0o777, 0o600)

    def test_pre_generated_pool_exhaustion_never_creates_a_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            pool_path = Path(tmp) / 'lookup.json'
            pool_path.write_text(
                json.dumps(
                    [
                        {
                            'token': 'a' * 64,
                            'name': 'Assigned User',
                            'email': 'assigned@example.edu',
                            'issued_at': 123,
                        }
                    ]
                ),
                encoding='utf-8',
            )
            pool = PreGeneratedApiTokenPool(str(pool_path))
            before = pool_path.read_text(encoding='utf-8')

            with self.assertRaises(ApiTokenPoolExhaustedError):
                pool.claim(name='New User', email='new@example.edu')

            self.assertEqual(pool_path.read_text(encoding='utf-8'), before)

    def test_pre_generated_pool_serializes_concurrent_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            pool_path = Path(tmp) / 'lookup.json'
            entries = [
                {'token': f'{i + 1:064x}', 'name': None, 'email': None, 'issued_at': None}
                for i in range(24)
            ]
            pool_path.write_text(json.dumps(entries), encoding='utf-8')
            pool = PreGeneratedApiTokenPool(str(pool_path))

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                tokens = list(
                    executor.map(
                        lambda i: pool.claim(name=f'User {i}', email=f'user-{i}@example.edu'),
                        range(24),
                    )
                )

            self.assertEqual(len(tokens), len(set(tokens)))
            persisted = json.loads(pool_path.read_text(encoding='utf-8'))
            self.assertTrue(all(entry['name'] and entry['email'] for entry in persisted))

    def test_pre_generated_pool_rejects_duplicate_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            pool_path = Path(tmp) / 'lookup.json'
            entry = {'token': 'a' * 64, 'name': None, 'email': None, 'issued_at': None}
            pool_path.write_text(json.dumps([entry, entry]), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicates'):
                PreGeneratedApiTokenPool(str(pool_path))

    def test_api_token_store_allows_only_one_lifetime_token_per_email(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            cfg_path.write_text('indexes:\n  local: /tmp\napi_keys:\n  - existing-key\n', encoding='utf-8')
            store = ApiTokenStore(str(cfg_path))
            token = store.activate('a' * 64, name='First User', email='first@example.edu')
            after_first = cfg_path.read_text(encoding='utf-8')

            with self.assertRaises(ApiTokenEmailAlreadyIssuedError):
                store.activate('b' * 64, name='Renamed User', email=' FIRST@EXAMPLE.EDU ')

            self.assertEqual(cfg_path.read_text(encoding='utf-8'), after_first)
            persisted = yaml.safe_load(after_first)
            self.assertEqual(persisted['api_keys'], ['existing-key', token])
            self.assertEqual(len(persisted['api_key_identities']), 1)

    def test_api_token_store_rejects_invalid_identity_mapping_without_modifying_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            original = (
                'indexes:\n  local: /tmp\napi_keys:\n  - existing-key\n'
                'api_key_identities:\n  existing-key:\n    name: Existing User\n'
            )
            cfg_path.write_text(original, encoding='utf-8')

            with self.assertRaises(ValueError):
                ApiTokenStore(str(cfg_path)).activate(
                    'a' * 64,
                    name='Test User',
                    email='test@example.edu',
                )

            self.assertEqual(cfg_path.read_text(encoding='utf-8'), original)

    def test_api_token_store_requires_name_and_email_without_modifying_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / 'server.yaml'
            original = 'indexes:\n  local: /tmp\napi_keys:\n  - existing-key\n'
            cfg_path.write_text(original, encoding='utf-8')
            store = ApiTokenStore(str(cfg_path))

            with self.assertRaises(ValueError):
                store.activate('a' * 64, name='', email='test@example.edu')
            with self.assertRaises(ValueError):
                store.activate('a' * 64, name='Test User', email='')
            with self.assertRaises(ValueError):
                store.activate('', name='Test User', email='test@example.edu')

            self.assertEqual(cfg_path.read_text(encoding='utf-8'), original)

    def test_accepted_api_tokens_can_activate_new_token(self):
        accepted = AcceptedApiTokens.from_strings(['existing-key'])
        accepted.add('new-key')

        self.assertTrue(accepted.is_valid('existing-key'))
        self.assertTrue(accepted.is_valid('new-key'))
        self.assertFalse(accepted.is_valid('unknown-key'))


if __name__ == '__main__':
    unittest.main()

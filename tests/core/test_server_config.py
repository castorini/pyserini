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
import unittest
from pathlib import Path

import yaml

from pyserini.server.config import load_server_config


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


if __name__ == '__main__':
    unittest.main()

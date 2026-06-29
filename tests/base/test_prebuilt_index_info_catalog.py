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

import unittest
from collections.abc import Mapping

from pyserini.prebuilt_index_info import _PrebuiltIndexCatalog, TF_INDEX_INFO


class PrefixFilteredMapping(Mapping):
    def __init__(self, prefix, values):
        self.prefix = prefix
        self.values = values
        self.loads = 0

    def _load(self):
        self.loads += 1
        return self.values

    def __getitem__(self, key):
        return self._load()[key]

    def __iter__(self):
        return iter(self._load())

    def __len__(self):
        return len(self._load())

    def __contains__(self, key):
        if not key.startswith(self.prefix):
            return False
        return key in self._load()


class TestPrebuiltIndexInfoCatalog(unittest.TestCase):
    def test_alias_lookup_resolves_to_canonical_index(self):
        catalog = _PrebuiltIndexCatalog(
            {'canonical': {'filename': 'index.tar.gz'}},
            aliases={'alias': 'canonical'})

        self.assertEqual(catalog['alias'], catalog['canonical'])

    def test_alias_lookup_resolves_to_lazy_index(self):
        source = PrefixFilteredMapping('lazy-', {'lazy-canonical': {'filename': 'lazy.tar.gz'}})
        catalog = _PrebuiltIndexCatalog(source, aliases={'lazy-alias': 'lazy-canonical'})

        self.assertEqual(catalog['lazy-alias'], {'filename': 'lazy.tar.gz'})
        self.assertEqual(source.loads, 2)

    def test_contains_skips_unrelated_prefix_filtered_sources(self):
        source = PrefixFilteredMapping('lazy-', {'lazy-canonical': {'filename': 'lazy.tar.gz'}})
        catalog = _PrebuiltIndexCatalog({'static': {'filename': 'static.tar.gz'}}, source)

        self.assertFalse('unrelated' in catalog)
        self.assertEqual(source.loads, 0)

    def test_iteration_includes_aliases(self):
        catalog = _PrebuiltIndexCatalog(
            {'canonical': {'filename': 'index.tar.gz'}},
            aliases={'alias': 'canonical'})

        self.assertEqual(list(catalog), ['canonical', 'alias'])

    def test_tf_index_info_aliases_preserve_existing_names(self):
        self.assertEqual(TF_INDEX_INFO['robust04'], TF_INDEX_INFO['disk45'])
        self.assertEqual(TF_INDEX_INFO['msmarco-passage'], TF_INDEX_INFO['msmarco-v1-passage'])


if __name__ == '__main__':
    unittest.main()

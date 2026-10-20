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

from pyserini.prebuilt_index_info import _PrebuiltIndexCatalog, TF_INDEX_INFO, TF_INDEX_INFO_RETECO


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

    def test_reteco_track1_indexes(self):
        self.assertEqual(len(TF_INDEX_INFO_RETECO), 13)
        self.assertEqual(sum(index['documents'] for index in TF_INDEX_INFO_RETECO.values()), 1167159)
        self.assertTrue(all(name.startswith('reteco-v1.1-track1-') for name in TF_INDEX_INFO_RETECO))

        iota = TF_INDEX_INFO['reteco-v1.1-track1-iota']
        self.assertEqual(iota['filename'], 'lucene-inverted.reteco-v1.1-track1-iota.20261017.1.6.0.tar.gz')
        self.assertEqual(iota['md5'], '5fec2d2e72d29c4687ecbdbad1b8bf17')
        self.assertEqual(iota['size'], 34011796)
        self.assertEqual(iota['documents'], 9680)
        self.assertEqual(iota['total_terms'], 3184205)
        self.assertEqual(iota['unique_terms'], 336319)


if __name__ == '__main__':
    unittest.main()

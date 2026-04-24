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

import json
import unittest

from pyserini.server.document_format import (
    _convert_json_value,
    _normalize_parsed_object,
    format_lucene_document,
)


class _FakeDocument:
    """Minimal stand-in for ``pyserini.index.lucene.Document`` (only ``raw()`` is used)."""

    __slots__ = ('_raw',)

    def __init__(self, raw):
        self._raw = raw

    def raw(self):
        return self._raw


class TestConvertJsonValue(unittest.TestCase):
    def test_nested_dict_and_list_preserved_structure(self):
        value = {'a': 1, 'b': [{'c': 2}]}
        self.assertEqual(_convert_json_value(value), {'a': 1, 'b': [{'c': 2}]})

    def test_leaf_non_container_unchanged(self):
        self.assertEqual(_convert_json_value(42), 42)
        self.assertEqual(_convert_json_value('x'), 'x')


class TestNormalizeParsedObject(unittest.TestCase):
    def test_skips_id_docid_underscore_id(self):
        obj = {'id': '1', '_id': '2', 'docid': '3', 'contents': 'hello'}
        self.assertEqual(_normalize_parsed_object(obj), 'hello')

    def test_single_key_unwraps_value(self):
        self.assertEqual(_normalize_parsed_object({'contents': 'only'}), 'only')

    def test_multiple_keys_returns_dict_scalars_as_strings(self):
        out = _normalize_parsed_object({'title': 't', 'n': 7})
        self.assertEqual(out, {'title': 't', 'n': '7'})

    def test_only_skipped_fields_yields_empty_dict(self):
        self.assertEqual(_normalize_parsed_object({'id': 'x', 'docid': 'y'}), {})

    def test_nested_dict_and_list_values(self):
        obj = {'contents': {'a': 1}, 'tags': [1, {'b': 2}]}
        out = _normalize_parsed_object(obj)
        self.assertEqual(out, {'contents': {'a': 1}, 'tags': [1, {'b': 2}]})


class TestFormatLuceneDocument(unittest.TestCase):
    def test_none_document(self):
        self.assertIsNone(format_lucene_document(None, parse=True))
        self.assertIsNone(format_lucene_document(None, parse=False))

    def test_none_raw(self):
        doc = _FakeDocument(None)
        self.assertIsNone(format_lucene_document(doc, parse=True))
        self.assertIsNone(format_lucene_document(doc, parse=False))

    def test_parse_false_returns_raw_string(self):
        raw = '{"contents": "x"}'
        doc = _FakeDocument(raw)
        self.assertIs(format_lucene_document(doc, parse=False), raw)

    def test_parse_true_valid_dict_normalizes(self):
        raw = json.dumps({'contents': 'text', 'id': 'skip-me'})
        doc = _FakeDocument(raw)
        self.assertEqual(format_lucene_document(doc, parse=True), 'text')

    def test_parse_true_invalid_json_returns_raw(self):
        raw = 'not json {'
        doc = _FakeDocument(raw)
        self.assertEqual(format_lucene_document(doc, parse=True), raw)

    def test_parse_true_non_dict_json_returned_as_is(self):
        doc = _FakeDocument('[1, 2]')
        self.assertEqual(format_lucene_document(doc, parse=True), [1, 2])

        doc2 = _FakeDocument('"literal"')
        self.assertEqual(format_lucene_document(doc2, parse=True), 'literal')

    def test_parse_true_json_null(self):
        doc = _FakeDocument('null')
        self.assertIsNone(format_lucene_document(doc, parse=True))


if __name__ == '__main__':
    unittest.main()

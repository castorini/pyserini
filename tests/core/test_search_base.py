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
from unittest.mock import patch, MagicMock

from pyserini.search._base import get_bright_excluded_ids


class TestGetBrightExcludedIds(unittest.TestCase):
    """Tests for get_bright_excluded_ids (BRIGHT query excluded_ids loading)."""

    def test_non_bright_index_returns_no_filter(self):
        apply_filter, mapping = get_bright_excluded_ids("msmarco-v1-passage")
        self.assertFalse(apply_filter)
        self.assertEqual(mapping, {})

    def test_bright_other_splits_returns_no_filter(self):
        """BRIGHT splits like biology/robotics don't use excluded_ids; only aops/leetcode/theoremqa-questions do."""
        apply_filter, mapping = get_bright_excluded_ids("bright-biology")
        self.assertFalse(apply_filter)
        self.assertEqual(mapping, {})

    def test_bright_aops_returns_filter_and_mapping(self):
        with patch("datasets.load_dataset") as mock_load:
            mock_split = [
                {"id": "q1", "excluded_ids": ["d1", "d2"]},
                {"id": "q2", "excluded_ids": ["d3"]},
            ]
            mock_load.return_value = MagicMock(__getitem__=lambda self, k: mock_split)
            apply_filter, mapping = get_bright_excluded_ids("bright-aops")
        self.assertTrue(apply_filter)
        self.assertEqual(mapping, {"q1": ["d1", "d2"], "q2": ["d3"]})

    def test_bright_leetcode_returns_filter_and_mapping(self):
        with patch("datasets.load_dataset") as mock_load:
            mock_split = [{"id": "a", "excluded_ids": []}]
            mock_load.return_value = MagicMock(__getitem__=lambda self, k: mock_split)
            apply_filter, mapping = get_bright_excluded_ids("bright-leetcode")
        self.assertTrue(apply_filter)
        self.assertEqual(mapping, {"a": []})

    def test_bright_theoremqa_questions_returns_filter_and_mapping(self):
        with patch("datasets.load_dataset") as mock_load:
            mock_split = [{"id": "t1", "excluded_ids": ["doc_x"]}]
            mock_load.return_value = MagicMock(__getitem__=lambda self, k: mock_split)
            apply_filter, mapping = get_bright_excluded_ids("bright-theoremqa-questions")
        self.assertTrue(apply_filter)
        self.assertEqual(mapping, {"t1": ["doc_x"]})

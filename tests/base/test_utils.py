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

import os
import tempfile
import unittest

from pyserini.prebuilt_index_info import TF_INDEX_INFO
from pyserini.util import download_url, download_and_unpack_index, compare_trec_strings_with_tolerance, compare_trec_files_with_tolerance


class TestIterateCollection(unittest.TestCase):
    def test_cacm_prebuilt_index_download(self):
        """ Sanity check, download_url will assert file size and md5 checksum when enabled """
        info = TF_INDEX_INFO["cacm"]
        urls = info.get("urls") or []
        url = urls[0] if urls else None
        expected_size = info.get("size compressed (bytes)", None)
        expected_md5 = info.get("md5", None)

        with tempfile.TemporaryDirectory(prefix="prebuilt-index-") as directory:
            tarball_path = download_url(url, directory, md5=expected_md5, expected_size=expected_size)
            self.assertTrue(os.path.exists(tarball_path), "Downloaded tarball not found on disk.")

    def test_prebuilt_index_download_size_mismatch_raises(self):
        """Negative case: wrong expected_size should raise."""
        info = TF_INDEX_INFO["cacm"]
        urls = info.get("urls") or []
        url = urls[0] if urls else None

        with tempfile.TemporaryDirectory(prefix="prebuilt-index-") as directory:
            with self.assertRaises((AssertionError, ValueError)):
                download_url(url, directory, expected_size=1, force=True)

    def test_prebuilt_index_download_md5_mismatch_raises(self):
        """Negative case: wrong md5 should raise."""
        info = TF_INDEX_INFO["cacm"]
        urls = info.get("urls") or []
        url = urls[0] if urls else None
        expected_size = info.get("size compressed (bytes)", None)

        with tempfile.TemporaryDirectory(prefix="prebuilt-index-") as directory:
            bad_md5 = "0" * 32
            with self.assertRaises((AssertionError, ValueError)):
                download_url(url, directory, md5=bad_md5, expected_size=expected_size, force=True)

    def test_download_and_unpack_index_sanity(self):
        """
        Sanity check: rely on download_url (inside function) to validate MD5/size,
        then ensure the extracted index directory exists and is non-empty.
        """
        info = TF_INDEX_INFO["cacm"]
        url = (info.get("urls") or [None])[0]
        expected_size = info.get("size compressed (bytes)", None)
        expected_md5 = info.get("md5", None)

        with tempfile.TemporaryDirectory(prefix="prebuilt-index-") as directory:
            index_path = download_and_unpack_index(url, index_directory=directory, md5=expected_md5,
                expected_size=expected_size, prebuilt=False, verbose=False, force=True)
            self.assertTrue(os.path.isdir(index_path), f"Index path missing: {index_path}")
            self.assertGreater(len(os.listdir(index_path)), 0, "Extracted index directory is empty.")


class TestCompareTrecWithTolerance(unittest.TestCase):
    def test_compare_trec_strings_exact_match(self):
        """Test that identical TREC strings match exactly."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag",
            "q1 Q0 doc2 2 0.4 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5 runtag",
            "q1 Q0 doc2 2 0.4 runtag"
        ]
        self.assertTrue(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_within_tolerance(self):
        """Test that scores within tolerance are considered equal."""
        strings1 = [
            "q1 Q0 doc1 1 0.5000 runtag",
            "q1 Q0 doc2 2 0.4000 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.50005 runtag",  # diff = 0.00005 < 1e-4
            "q1 Q0 doc2 2 0.39995 runtag"   # diff = 0.00005 < 1e-4
        ]
        self.assertTrue(compare_trec_strings_with_tolerance(strings1, strings2, tolerance=1e-4))

    def test_compare_trec_strings_beyond_tolerance(self):
        """Test that scores beyond tolerance are considered different."""
        strings1 = [
            "q1 Q0 doc1 1 0.5000 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5002 runtag"  # diff = 0.0002 > 1e-4
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2, tolerance=1e-4))

    def test_compare_trec_strings_custom_tolerance(self):
        """Test with custom tolerance value."""
        strings1 = [
            "q1 Q0 doc1 1 0.5000 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5002 runtag"  # diff = 0.0002
        ]
        # Should pass with larger tolerance
        self.assertTrue(compare_trec_strings_with_tolerance(strings1, strings2, tolerance=1e-3))
        # Should fail with smaller tolerance
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2, tolerance=1e-5))

    def test_compare_trec_strings_different_lengths(self):
        """Test that different length lists return False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5 runtag",
            "q1 Q0 doc2 2 0.4 runtag"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_different_qid(self):
        """Test that different query IDs return False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q2 Q0 doc1 1 0.5 runtag"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_different_docid(self):
        """Test that different document IDs return False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q1 Q0 doc2 1 0.5 runtag"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_different_rank(self):
        """Test that different ranks return False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 2 0.5 runtag"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_different_runtag(self):
        """Test that different runtags return False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag1"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5 runtag2"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_whitespace_handling(self):
        """Test that whitespace is properly stripped."""
        strings1 = [
            "  q1 Q0 doc1 1 0.5 runtag  ",
            "q1 Q0 doc2 2 0.4 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5 runtag",
            "  q1 Q0 doc2 2 0.4 runtag  "
        ]
        self.assertTrue(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_empty_lists(self):
        """Test that empty lists match."""
        self.assertTrue(compare_trec_strings_with_tolerance([], []))

    def test_compare_trec_strings_invalid_score(self):
        """Test that invalid score format returns False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 invalid runtag"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_strings_different_field_count(self):
        """Test that different number of fields returns False."""
        strings1 = [
            "q1 Q0 doc1 1 0.5 runtag"
        ]
        strings2 = [
            "q1 Q0 doc1 1 0.5"
        ]
        self.assertFalse(compare_trec_strings_with_tolerance(strings1, strings2))

    def test_compare_trec_files_exact_match(self):
        """Test that identical TREC files match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            f1.write("q1 Q0 doc1 1 0.5 runtag\n")
            f1.write("q1 Q0 doc2 2 0.4 runtag\n")
            f2.write("q1 Q0 doc1 1 0.5 runtag\n")
            f2.write("q1 Q0 doc2 2 0.4 runtag\n")
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertTrue(compare_trec_files_with_tolerance(f1_path, f2_path))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_compare_trec_files_within_tolerance(self):
        """Test that files with scores within tolerance match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            f1.write("q1 Q0 doc1 1 0.5000 runtag\n")
            f2.write("q1 Q0 doc1 1 0.50005 runtag\n")  # diff = 0.00005 < 1e-4
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertTrue(compare_trec_files_with_tolerance(f1_path, f2_path, tolerance=1e-4))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_compare_trec_files_beyond_tolerance(self):
        """Test that files with scores beyond tolerance don't match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            f1.write("q1 Q0 doc1 1 0.5000 runtag\n")
            f2.write("q1 Q0 doc1 1 0.5002 runtag\n")  # diff = 0.0002 > 1e-4
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertFalse(compare_trec_files_with_tolerance(f1_path, f2_path, tolerance=1e-4))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_compare_trec_files_different_lengths(self):
        """Test that files with different number of lines don't match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            f1.write("q1 Q0 doc1 1 0.5 runtag\n")
            f2.write("q1 Q0 doc1 1 0.5 runtag\n")
            f2.write("q1 Q0 doc2 2 0.4 runtag\n")
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertFalse(compare_trec_files_with_tolerance(f1_path, f2_path))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_compare_trec_files_file_not_found(self):
        """Test that missing file returns False."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1:
            f1.write("q1 Q0 doc1 1 0.5 runtag\n")
            f1_path = f1.name
            nonexistent_path = "/nonexistent/file/path.txt"

        try:
            self.assertFalse(compare_trec_files_with_tolerance(f1_path, nonexistent_path))
            self.assertFalse(compare_trec_files_with_tolerance(nonexistent_path, f1_path))
        finally:
            os.unlink(f1_path)

    def test_compare_trec_files_empty_files(self):
        """Test that empty files match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            # Write nothing (empty files)
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertTrue(compare_trec_files_with_tolerance(f1_path, f2_path))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_compare_trec_files_whitespace_handling(self):
        """Test that whitespace in files is properly handled."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f1, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f2:
            f1.write("  q1 Q0 doc1 1 0.5 runtag  \n")
            f2.write("q1 Q0 doc1 1 0.5 runtag\n")
            f1_path = f1.name
            f2_path = f2.name

        try:
            self.assertTrue(compare_trec_files_with_tolerance(f1_path, f2_path))
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)


if __name__ == "__main__":
    unittest.main()
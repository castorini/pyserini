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
from pyserini.util import download_url, download_and_unpack_index


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


if __name__ == "__main__":
    unittest.main()
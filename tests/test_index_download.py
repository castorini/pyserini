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
import random
import shutil
import unittest

from pyserini.search.lucene import LuceneSearcher


class TestIndexDownload(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = f'tmp_{self.__class__.__name__}_{str(random.randint(0, 1000))}'

    def test_default_cache(self):
        LuceneSearcher.from_prebuilt_index('cacm')
        self.assertTrue(os.path.exists(os.path.expanduser('~/.cache/pyserini/indexes')))

    def test_custom_cache(self):
        os.environ['PYSERINI_CACHE'] = self.tmp_dir
        LuceneSearcher.from_prebuilt_index('cacm')
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'indexes')))

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
            os.environ['PYSERINI_CACHE'] = ''

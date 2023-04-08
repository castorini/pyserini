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

import requests
import unittest

from pyserini.prebuilt_index_info import TF_INDEX_INFO


class TestPrebuiltIndexes(unittest.TestCase):
    def test_tf_beir(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'beir' in key and 'lucene8' not in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    print(f'{key} {url}')
                    urls.append(url)

        # 29 each for flat and multifield
        self.assertEqual(cnt, 58)
        self._test_urls(urls)

    def test_tf_mrtydi(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'mrtydi' in key and 'lucene8' not in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    print(f'{key} {url}')
                    urls.append(url)
        print(cnt)

        # 11 languages
        self.assertEqual(cnt, 11)
        self._test_urls(urls)

    def test_tf_miracl(self):
        urls = []
        cnt = 0
        for key in TF_INDEX_INFO:
            if 'miracl' in key:
                cnt += 1
                for url in TF_INDEX_INFO[key]['urls']:
                    print(f'{key} {url}')
                    urls.append(url)
        print(cnt)

        # 18 languages including surprise
        self.assertEqual(cnt, 18)
        self._test_urls(urls)

    def _test_urls(self, urls):
        cnt = 0
        for url in urls:
            cnt += 1
            response = requests.head(url)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(cnt, len(urls))

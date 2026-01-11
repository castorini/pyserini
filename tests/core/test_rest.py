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

import unittest

from fastapi.testclient import TestClient

from pyserini.server.rest.app import app, VERSION

class TestRestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_docs_available(self):
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)
    
    def test_search(self):
        response = self.client.post(
            f"/{VERSION}/indexes/msmarco-v1-passage/search",
            json={"query": "what is a lobster roll", "hits": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("query" in list(response.json().keys()))
        self.assertTrue("candidates" in list(response.json().keys()))
        self.assertEqual(1, len(response.json().get("candidates")))
        self.assertEqual("7157707", response.json().get("candidates")[0].get("docid"))

    def test_get_doc(self):
        response = self.client.get(f"/{VERSION}/indexes/msmarco-v1-passage/documents/7157707")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("id" in list(response.json().keys()))
        self.assertTrue("contents" in list(response.json().keys()))
        self.assertTrue("Lobster Roll" in response.json().get("contents"))

    def test_index_status(self):
        response = self.client.get(f"/{VERSION}/indexes/msmarco-v1-passage/status")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("downloaded" in list(response.json().keys()))
        self.assertTrue("size_bytes" in list(response.json().keys()))
        self.assertTrue(response.json().get("downloaded"))

    def test_list_indexes(self):
        response = self.client.get(f"/{VERSION}/indexes/?index_type=tf")
        self.assertEqual(response.status_code, 200)

    def test_get_index_settings(self):
        response = self.client.get(f"/{VERSION}/indexes/msmarco-v1-passage/settings")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("efSearch" in list(response.json().keys()))
        self.assertTrue("encoder" in list(response.json().keys()))
        self.assertTrue("queryGenerator" in list(response.json().keys()))

    def test_post_index_settings(self):
        data = {"efSearch": "100", "encoder": "BgeBaseEn15Encoder", "queryGenerator": "BagOfWordsGenerator"}
        response = self.client.post(f"/{VERSION}/indexes/msmarco-v1-passage/settings", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})


if __name__ == '__main__':
    unittest.main()

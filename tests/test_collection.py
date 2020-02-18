# -*- coding: utf-8 -*-
#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import os
import shutil
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve

from pyserini.collection import pycollection
from pyserini.index import pygenerator


class TestIterateCollection(unittest.TestCase):

    def test_cacm(self):
        # We're going to append a random value to downloaded files:
        r = randint(0, 10000000)
        collection_url = 'https://github.com/castorini/anserini/blob/master/src/main/resources/cacm/cacm.tar.gz?raw=true'
        tarball_name = 'cacm{}.tar.gz'.format(r)
        collection_dir = 'collection{}/'.format(r)

        filename, headers = urlretrieve(collection_url, tarball_name)

        tarball = tarfile.open(tarball_name)
        tarball.extractall(collection_dir)
        tarball.close()

        collection = pycollection.Collection('HtmlCollection', collection_dir)
        generator = pygenerator.Generator('JsoupGenerator')

        cnt = 0
        for (i, fs) in enumerate(collection):
            for (j, doc) in enumerate(fs):
                self.assertTrue(isinstance(doc, pycollection.SourceDocument))
                parsed = generator.create_document(doc)
                docid = parsed.get('id')            # FIELD_ID
                raw = parsed.get('raw')             # FIELD_RAW
                contents = parsed.get('contents')   # FIELD_BODY
                self.assertTrue(docid != '')
                self.assertTrue(raw != '')
                self.assertTrue(contents != '')
                cnt += 1

        self.assertEqual(cnt, 3204)

        # Clean up
        os.remove(tarball_name)
        shutil.rmtree(collection_dir)


if __name__ == '__main__':
    unittest.main()

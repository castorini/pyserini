import unittest
import tarfile
import os
import shutil

from pyserini.collection import pycollection
from pyserini.index import pygenerator
from urllib.request import urlretrieve
from random import randint

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

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
import shutil
import tarfile
import unittest
from random import randint
from typing import List
from urllib.request import urlretrieve

from pyserini.search import SimpleNearestNeighborSearcher, JSimpleNearestNeighborSearcherResult


class TestSearch(unittest.TestCase):
    def setUp(self):
        # Download pre-built CACM vectors index; append a random value to avoid filename clashes.
        r = randint(0, 10000000)

        self.vectors_url = 'https://www.dropbox.com/s/p1syrnphxpb2sw2/lucene-index-vectors.cacm.tar.gz?dl=1'
        self.vectors_tarball_name = 'lucene-index-vectors.cacm-{}.tar.gz'.format(r)
        self.vectors_dir = 'vectors{}/'.format(r)

        vectors_filename, vectors_headers = urlretrieve(self.vectors_url, self.vectors_tarball_name)

        vectors_tarball = tarfile.open(self.vectors_tarball_name)
        vectors_tarball.extractall(self.vectors_dir)
        vectors_tarball.close()

        self.nnsercher = SimpleNearestNeighborSearcher(f'{self.vectors_dir}lucene-index-vectors.cacm')

    def test_nearest_neighbor(self):
        hits = self.nnsercher.search('CACM-0059')

        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0], JSimpleNearestNeighborSearcherResult))
        self.assertEqual(hits[0].id, 'CACM-0059')
        self.assertAlmostEqual(hits[0].score, 62.17443, places=5)
        self.assertEqual(hits[1].id, 'CACM-0084')
        self.assertAlmostEqual(hits[1].score, 60.90524, places=5)

        hits = self.nnsercher.multisearch('CACM-0059')

        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0][0], JSimpleNearestNeighborSearcherResult))
        self.assertEqual(hits[0][0].id, 'CACM-0059')
        self.assertAlmostEqual(hits[0][0].score, 62.17443, places=5)
        self.assertEqual(hits[0][1].id, 'CACM-0084')
        self.assertAlmostEqual(hits[0][1].score, 60.90524, places=5)

    def tearDown(self):
        os.remove(self.vectors_tarball_name)
        shutil.rmtree(self.vectors_dir)


if __name__ == '__main__':
    unittest.main()

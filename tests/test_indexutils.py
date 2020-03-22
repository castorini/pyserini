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

from pyserini.analysis import pyanalysis
from pyserini.index import pyutils
from pyserini.pyclass import JString


class TestIndexUtils(unittest.TestCase):
    def setUp(self):
        # Download pre-built CACM index; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene-index.cacm.tar.gz'
        self.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'index{}/'.format(r)

        filename, headers = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

        self.index_utils = pyutils.IndexReaderUtils('{}lucene-index.cacm'.format(self.index_dir))

    def test_terms_count(self):
        # We're going to iterate through the index and make sure we have the correct number of terms.
        self.assertEqual(sum(1 for x in self.index_utils.terms()), 14363)

    def test_terms_contents(self):
        # We're going to examine the first two index terms to make sure the statistics are correct.
        iterator = self.index_utils.terms()
        index_term = next(iterator)
        self.assertEqual(index_term.term, '0')
        self.assertEqual(index_term.df, 19)
        self.assertEqual(index_term.cf, 30)

        index_term = next(iterator)
        self.assertEqual(index_term.term, '0,1')
        self.assertEqual(index_term.df, 1)
        self.assertEqual(index_term.cf, 1)

    def test_analyze(self):
        self.assertEqual(' '.join(self.index_utils.analyze('retrieval')), 'retriev')
        self.assertEqual(' '.join(self.index_utils.analyze('rapid retrieval, space economy')),
                         'rapid retriev space economi')
        tokenizer = pyanalysis.get_lucene_analyzer(stemming=False)
        self.assertEqual(' '.join(self.index_utils.analyze('retrieval', analyzer=tokenizer)), 'retrieval')
        self.assertEqual(' '.join(self.index_utils.analyze('rapid retrieval, space economy', analyzer=tokenizer)),
                         'rapid retrieval space economy')
        # Test utf encoding:
        self.assertEqual(self.index_utils.analyze('zoölogy')[0], 'zoölog')
        self.assertEqual(self.index_utils.analyze('zoölogy', analyzer=tokenizer)[0], 'zoölogy')

    def test_term_stats(self):
        df, cf = self.index_utils.get_term_counts('retrieval')
        self.assertEqual(df, 138)
        self.assertEqual(cf, 275)

        analyzer = pyanalysis.get_lucene_analyzer(stemming=False, stopwords=False)
        df_no_stem, cf_no_stem = self.index_utils.get_term_counts('retrieval', analyzer)
        # 'retrieval' does not occur as a stemmed word, only 'retriev' does.
        self.assertEqual(df_no_stem, 0)
        self.assertEqual(cf_no_stem, 0)

        df_no_stopword, cf_no_stopword = self.index_utils.get_term_counts('on', analyzer)
        self.assertEqual(df_no_stopword, 326)
        self.assertEqual(cf_no_stopword, 443)
        

    def test_postings1(self):
        term = 'retrieval'
        postings = list(self.index_utils.get_postings_list(term))
        self.assertEqual(len(postings), 138)

        self.assertEqual(postings[0].docid, 238)
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(postings[0].docid), 'CACM-0239')
        self.assertEqual(postings[0].tf, 1)
        self.assertEqual(len(postings[0].positions), 1)

        self.assertEqual(postings[-1].docid, 3168)
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(postings[-1].docid), 'CACM-3169')
        self.assertEqual(postings[-1].tf, 1)
        self.assertEqual(len(postings[-1].positions), 1)

    def test_postings2(self):
        self.assertIsNone(self.index_utils.get_postings_list('asdf'))

        postings = list(self.index_utils.get_postings_list('retrieval', analyze=True))
        self.assertEqual(len(postings), 138)

        # If we don't analyze, then we can't find the postings list:
        self.assertIsNone(self.index_utils.get_postings_list('retrieval', analyze=False))

        # Supply the analyzed form directly, and we're good:
        postings = list(self.index_utils.get_postings_list('retriev', analyze=False))
        self.assertEqual(len(postings), 138)
        postings = list(self.index_utils.get_postings_list(self.index_utils.analyze('retrieval')[0], analyze=False))
        self.assertEqual(len(postings), 138)

        # Test utf encoding:
        self.assertEqual(self.index_utils.get_postings_list('zoölogy'), None)
        self.assertEqual(self.index_utils.get_postings_list('zoölogy', analyze=False), None)
        self.assertEqual(self.index_utils.get_postings_list('zoölogy', analyze=True), None)

    def test_doc_vector(self):
        doc_vector = self.index_utils.get_document_vector('CACM-3134')
        self.assertEqual(len(doc_vector), 94)
        self.assertEqual(doc_vector['inform'], 8)
        self.assertEqual(doc_vector['retriev'], 7)

    def test_doc_vector_matches_index(self):
        # From the document vector, look up the term frequency of "information".
        doc_vector = self.index_utils.get_document_vector('CACM-3134')
        self.assertEqual(doc_vector['inform'], 8)

        # Now look up the postings list for "information".
        term = 'information'
        postings_list = list(self.index_utils.get_postings_list(term))

        for i in range(len(postings_list)):
            # Go through the postings and find the matching document.
            if self.index_utils.convert_internal_docid_to_collection_docid(postings_list[i].docid) == 'CACM-3134':
                # The tf values should match.
                self.assertEqual(postings_list[i].tf, 8)

    def test_raw_document_contents(self):
        raw = self.index_utils.get_raw_document_contents('CACM-3134')
        self.assertTrue(isinstance(raw, str))
        lines = raw.splitlines()
        self.assertEqual(len(lines), 55)
        # Note that the raw document contents will still have HTML tags.
        self.assertEqual(lines[0], '<html>')
        self.assertEqual(lines[4], 'The Use of Normal Multiplication Tables')
        self.assertEqual(lines[29], 'rapid retrieval, space economy')

    def test_bm25_weight(self):
        self.assertAlmostEqual(self.index_utils.compute_bm25_term_weight('CACM-3134', 'inform'), 1.925014, places=5)
        self.assertAlmostEqual(self.index_utils.compute_bm25_term_weight('CACM-3134', 'retriev'), 2.496352, places=5)

    def test_docid_converstion(self):
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(1), 'CACM-0002')
        self.assertEqual(self.index_utils.convert_collection_docid_to_internal_docid('CACM-0002'), 1)
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(1000), 'CACM-1001')
        self.assertEqual(self.index_utils.convert_collection_docid_to_internal_docid('CACM-1001'), 1000)

    def test_jstring_term(self):
        self.assertEqual(self.index_utils.get_term_counts('zoölogy'), (0, 0))
        with self.assertRaises(ValueError):
            # Should fail when pyjnius has solved this internally.
            JString('zoölogy')

    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()

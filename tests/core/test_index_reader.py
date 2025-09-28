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

import heapq
import json
import os
import shutil
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

from pyserini.analysis import get_lucene_analyzer
from pyserini.index.lucene import LuceneIndexReader
from pyserini.pyclass import JString
from pyserini.search.lucene import LuceneSearcher, LuceneSimilarities
from pyserini.vectorizer import BM25Vectorizer, TfidfVectorizer


class TestIndexUtils(unittest.TestCase):
    def setUp(self):
        # Download pre-built CACM index built using Lucene 9; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene9-index.cacm.tar.gz'
        self.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'index{}/'.format(r)

        _, _ = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

        self.index_path = os.path.join(self.index_dir, 'lucene9-index.cacm')
        self.searcher = LuceneSearcher(self.index_path)
        self.index_reader = LuceneIndexReader(self.index_path)

        self.temp_folders = []

        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('core'):
            self.collection_dir = '../../collections'
            self.emoji_corpus_path = '../resources/sample_collection_json_emoji'
        else:
            self.collection_dir = 'collections'
            self.emoji_corpus_path = 'tests/resources/sample_collection_json_emoji'

    # See https://github.com/castorini/pyserini/issues/770
    # tldr -- a longstanding issue about whether we need the `encode` in `JString(my_str.encode('utf-8'))`.
    # As it turns out, the solution is to remove the `JString` wrapping, which also has performance benefits as well.
    # See:
    # - https://github.com/castorini/pyserini/pull/862
    # - https://github.com/castorini/pyserini/issues/841
    def test_doc_vector_emoji_test(self):
        index_dir = 'temp_index'
        self.temp_folders.append(index_dir)
        cmd1 = f'python -m pyserini.index.lucene -collection JsonCollection ' + \
               f'-generator DefaultLuceneDocumentGenerator ' + \
               f'-threads 1 -input {self.emoji_corpus_path} -index {index_dir} -storeDocvectors'
        _ = os.system(cmd1)
        temp_index_reader = LuceneIndexReader(index_dir)

        df, cf = temp_index_reader.get_term_counts('emoji')
        self.assertEqual(df, 1)
        self.assertEqual(cf, 1)

        df, cf = temp_index_reader.get_term_counts('🙂')
        self.assertEqual(df, 1)
        self.assertEqual(cf, 1)

        doc_vector = temp_index_reader.get_document_vector('doc1')
        self.assertEqual(doc_vector['emoji'], 1)
        self.assertEqual(doc_vector['🙂'], 1)
        self.assertEqual(doc_vector['😀'], 1)

    def test_tfidf_vectorizer_train(self):
        vectorizer = TfidfVectorizer(self.index_path, min_df=5)
        train_docs = ['CACM-0239', 'CACM-0440', 'CACM-3168', 'CACM-3169']
        train_labels = [1, 1, 0, 0]
        test_docs = ['CACM-0634', 'CACM-3134']
        train_vectors = vectorizer.get_vectors(train_docs)
        test_vectors = vectorizer.get_vectors(test_docs)
        clf = MultinomialNB()
        clf.fit(train_vectors, train_labels)
        pred = clf.predict_proba(test_vectors)
        self.assertAlmostEqual(0.49975694, pred[0][0], places=8)
        self.assertAlmostEqual(0.50024306, pred[0][1], places=8)
        self.assertAlmostEqual(0.51837413, pred[1][0], places=8)
        self.assertAlmostEqual(0.48162587, pred[1][1], places=8)

    def test_bm25_vectorizer_train(self):
        vectorizer = BM25Vectorizer(self.index_path, min_df=5)
        train_docs = ['CACM-0239', 'CACM-0440', 'CACM-3168', 'CACM-3169']
        train_labels = [1, 1, 0, 0]
        test_docs = ['CACM-0634', 'CACM-3134']
        train_vectors = vectorizer.get_vectors(train_docs)
        test_vectors = vectorizer.get_vectors(test_docs)
        clf = LogisticRegression()
        clf.fit(train_vectors, train_labels)
        pred = clf.predict_proba(test_vectors)
        self.assertAlmostEqual(0.4630, pred[0][0], places=4)
        self.assertAlmostEqual(0.5370, pred[0][1], places=4)
        self.assertAlmostEqual(0.4829, pred[1][0], places=4)
        self.assertAlmostEqual(0.5171, pred[1][1], places=4)

    def test_tfidf_vectorizer(self):
        vectorizer = TfidfVectorizer(self.index_path, min_df=5)
        result = vectorizer.get_vectors(['CACM-0239', 'CACM-0440'], norm=None)
        self.assertAlmostEqual(result[0, 190], 2.907369334264736, places=8)
        self.assertAlmostEqual(result[1, 391], 0.07516490235060004, places=8)

    def test_bm25_vectorizer(self):
        vectorizer = BM25Vectorizer(self.index_path, min_df=5)
        result = vectorizer.get_vectors(['CACM-0239', 'CACM-0440'], norm=None)
        self.assertAlmostEqual(result[0, 190], 1.7513844966888428, places=8)
        self.assertAlmostEqual(result[1, 391], 0.03765463829040527, places=8)

    def test_vectorizer_query(self):
        vectorizer = BM25Vectorizer(self.index_path, min_df=5)
        result = vectorizer.get_query_vector('this is a query to test query vector')
        self.assertEqual(result[0, 2703], 2)
        self.assertEqual(result[0, 3078], 1)
        self.assertEqual(result[0, 3204], 1)

    def test_terms_count(self):
        # We're going to iterate through the index and make sure we have the correct number of terms.
        self.assertEqual(sum(1 for x in self.index_reader.terms()), 14363)

    def test_terms_contents(self):
        # We're going to examine the first two index terms to make sure the statistics are correct.
        iterator = self.index_reader.terms()
        index_term = next(iterator)
        self.assertEqual(index_term.term, '0')
        self.assertEqual(index_term.df, 19)
        self.assertEqual(index_term.cf, 30)

        index_term = next(iterator)
        self.assertEqual(index_term.term, '0,1')
        self.assertEqual(index_term.df, 1)
        self.assertEqual(index_term.cf, 1)

    def test_analyze(self):
        self.assertEqual(' '.join(self.index_reader.analyze('retrieval')), 'retriev')
        self.assertEqual(' '.join(self.index_reader.analyze('rapid retrieval, space economy')),
                         'rapid retriev space economi')
        tokenizer = get_lucene_analyzer(stemming=False)
        self.assertEqual(' '.join(self.index_reader.analyze('retrieval', analyzer=tokenizer)), 'retrieval')
        self.assertEqual(' '.join(self.index_reader.analyze('rapid retrieval, space economy', analyzer=tokenizer)),
                         'rapid retrieval space economy')
        # Test utf encoding:
        self.assertEqual(self.index_reader.analyze('zoölogy')[0], 'zoölog')
        self.assertEqual(self.index_reader.analyze('zoölogy', analyzer=tokenizer)[0], 'zoölogy')

    def test_term_stats(self):
        df, cf = self.index_reader.get_term_counts('retrieval')
        self.assertEqual(df, 138)
        self.assertEqual(cf, 275)

        df, cf = self.index_reader.get_term_counts('information retrieval')
        self.assertEqual(df, 74)
        self.assertEqual(cf, None)

        df_no_stem, cf_no_stem = self.index_reader.get_term_counts('retrieval', analyzer=None)
        # 'retrieval' does not occur as a stemmed word, only 'retriev' does.
        self.assertEqual(df_no_stem, 0)
        self.assertEqual(cf_no_stem, 0)

        df_no_stopword, cf_no_stopword = self.index_reader.get_term_counts('on', analyzer=None)
        self.assertEqual(df_no_stopword, 326)
        self.assertEqual(cf_no_stopword, 443)

        # Should gracefully handle non-existent term.
        df, cf = self.index_reader.get_term_counts('sdgsc')
        self.assertEqual(df, 0)
        self.assertEqual(cf, 0)

    def test_postings1(self):
        term = 'retrieval'
        postings = list(self.index_reader.get_postings_list(term))
        self.assertEqual(len(postings), 138)

        self.assertEqual(postings[0].docid, 238)
        self.assertEqual(self.index_reader.convert_internal_docid_to_collection_docid(postings[0].docid), 'CACM-0239')
        self.assertEqual(postings[0].tf, 1)
        self.assertEqual(len(postings[0].positions), 1)

        self.assertEqual(postings[-1].docid, 3168)
        self.assertEqual(self.index_reader.convert_internal_docid_to_collection_docid(postings[-1].docid), 'CACM-3169')
        self.assertEqual(postings[-1].tf, 1)
        self.assertEqual(len(postings[-1].positions), 1)

    def test_postings2(self):
        self.assertIsNone(self.index_reader.get_postings_list('asdf'))

        postings = list(self.index_reader.get_postings_list('retrieval'))
        self.assertEqual(len(postings), 138)

        # If we don't analyze, then we can't find the postings list:
        self.assertIsNone(self.index_reader.get_postings_list('retrieval', analyzer=None))

        # Supply the analyzed form directly, and we're good:
        postings = list(self.index_reader.get_postings_list('retriev', analyzer=None))
        self.assertEqual(len(postings), 138)
        postings = list(self.index_reader.get_postings_list(self.index_reader.analyze('retrieval')[0], analyzer=None))
        self.assertEqual(len(postings), 138)

        # Test utf encoding:
        self.assertEqual(self.index_reader.get_postings_list('zoölogy'), None)
        self.assertEqual(self.index_reader.get_postings_list('zoölogy', analyzer=None), None)
        self.assertEqual(self.index_reader.get_postings_list('zoölogy'), None)

    def test_doc_vector(self):
        doc_vector = self.index_reader.get_document_vector('CACM-3134')
        self.assertEqual(len(doc_vector), 94)
        self.assertEqual(doc_vector['inform'], 8)
        self.assertEqual(doc_vector['retriev'], 7)

    def test_doc_vector_invalid(self):
        self.assertTrue(self.index_reader.get_document_vector('foo') is None)

    def test_doc_vector_matches_index(self):
        # From the document vector, look up the term frequency of "information".
        doc_vector = self.index_reader.get_document_vector('CACM-3134')
        self.assertEqual(doc_vector['inform'], 8)

        # Now look up the postings list for "information".
        term = 'information'
        postings_list = list(self.index_reader.get_postings_list(term))

        for i in range(len(postings_list)):
            # Go through the postings and find the matching document.
            if self.index_reader.convert_internal_docid_to_collection_docid(postings_list[i].docid) == 'CACM-3134':
                # The tf values should match.
                self.assertEqual(postings_list[i].tf, 8)

    def test_term_position(self):
        term_positions = self.index_reader.get_term_positions('CACM-3134')
        self.assertEqual(len(term_positions), 94)
        self.assertEqual(term_positions['inform'], [7,24,36,46,60,112,121,159])
        self.assertEqual(term_positions['retriev'], [10,20,44,132,160,164,172])

    def test_term_position_invalid(self):
        self.assertTrue(self.index_reader.get_term_positions('foo') is None)

    def test_term_position_matches_index(self):
        # From the term positions mapping, look up the position list of "information".
        term_positions = self.index_reader.get_term_positions('CACM-3134')
        self.assertEqual(term_positions['inform'], [7,24,36,46,60,112,121,159])

        # Now look up the postings list for "information".
        term = 'information'
        postings_list = list(self.index_reader.get_postings_list(term))

        for i in range(len(postings_list)):
            # Go through the postings and find the matching document.
            if self.index_reader.convert_internal_docid_to_collection_docid(postings_list[i].docid) == 'CACM-3134':
                # The position list should match.
                self.assertEqual(postings_list[i].positions, [7, 24, 36, 46, 60, 112, 121, 159])

    def test_doc_invalid(self):
        self.assertTrue(self.index_reader.doc('foo') is None)
        self.assertTrue(self.index_reader.doc_contents('foo') is None)
        self.assertTrue(self.index_reader.doc_raw('foo') is None)
        self.assertTrue(self.index_reader.doc_by_field('foo', 'bar') is None)

    def test_doc_raw(self):
        raw = self.index_reader.doc('CACM-3134').raw()
        self.assertTrue(isinstance(raw, str))
        lines = raw.splitlines()
        self.assertEqual(len(lines), 55)
        # Note that the raw document contents will still have HTML tags.
        self.assertEqual(lines[0], '<html>')
        self.assertEqual(lines[4], 'The Use of Normal Multiplication Tables')
        self.assertEqual(lines[29], 'rapid retrieval, space economy')

        # Now that we've verified the 'raw', check that alternative ways of fetching give the same results.
        self.assertEqual(raw, self.index_reader.doc_raw('CACM-3134'))
        self.assertEqual(raw, self.index_reader.doc('CACM-3134').raw())
        self.assertEqual(raw, self.index_reader.doc('CACM-3134').get('raw'))
        self.assertEqual(raw, self.index_reader.doc('CACM-3134').lucene_document().get('raw'))

    def test_doc_contents(self):
        contents = self.index_reader.doc('CACM-3134').contents()
        self.assertTrue(isinstance(contents, str))
        lines = contents.splitlines()
        self.assertEqual(len(lines), 48)
        self.assertEqual(lines[0], 'The Use of Normal Multiplication Tables')
        self.assertEqual(lines[47], '3134\t5\t3134')

        # Now that we've verified the 'raw', check that alternative ways of fetching give the same results.
        self.assertEqual(contents, self.index_reader.doc_contents('CACM-3134'))
        self.assertEqual(contents, self.index_reader.doc('CACM-3134').contents())
        self.assertEqual(contents, self.index_reader.doc('CACM-3134').get('contents'))
        self.assertEqual(contents, self.index_reader.doc('CACM-3134').lucene_document().get('contents'))

    def test_doc_by_field(self):
        self.assertEqual(self.index_reader.doc('CACM-3134').docid(),
                         self.index_reader.doc_by_field('id', 'CACM-3134').docid())

    def test_bm25_weight(self):
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'inform', analyzer=None, k1=1.2, b=0.75),
            1.925014, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'information', k1=1.2, b=0.75),
            1.925014, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'retriev', analyzer=None, k1=1.2, b=0.75),
            2.496352, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'retrieval', k1=1.2, b=0.75),
            2.496352, places=5)

        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'inform', analyzer=None),
            2.06514, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'information'),
            2.06514, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'retriev', analyzer=None),
            2.70038, places=5)
        self.assertAlmostEqual(
            self.index_reader.compute_bm25_term_weight('CACM-3134', 'retrieval'),
            2.70038, places=5)

        self.assertAlmostEqual(self.index_reader.compute_bm25_term_weight('CACM-3134', 'fox', analyzer=None),
                               0., places=5)
        self.assertAlmostEqual(self.index_reader.compute_bm25_term_weight('CACM-3134', 'fox'), 0., places=5)

    def test_docid_conversion(self):
        self.assertEqual(self.index_reader.convert_internal_docid_to_collection_docid(1), 'CACM-0002')
        self.assertEqual(self.index_reader.convert_collection_docid_to_internal_docid('CACM-0002'), 1)
        self.assertEqual(self.index_reader.convert_internal_docid_to_collection_docid(1000), 'CACM-1001')
        self.assertEqual(self.index_reader.convert_collection_docid_to_internal_docid('CACM-1001'), 1000)

    def test_query_doc_score_default(self):
        queries = ['information retrieval', 'databases']

        for query in queries:
            hits = self.searcher.search(query)

            # We're going to verify that the score of each hit is about the same as the output of
            # compute_query_document_score
            for i in range(0, len(hits)):
                self.assertAlmostEqual(hits[i].score,
                                       self.index_reader.compute_query_document_score(hits[i].docid, query), places=4)

    def test_query_doc_score_custom_similarity(self):
        custom_bm25 = LuceneSimilarities.bm25(0.8, 0.2)
        queries = ['information retrieval', 'databases']
        self.searcher.set_bm25(0.8, 0.2)

        for query in queries:
            hits = self.searcher.search(query)

            # We're going to verify that the score of each hit is about the same as the output of
            # compute_query_document_score
            for i in range(0, len(hits)):
                self.assertAlmostEqual(hits[i].score,
                                       self.index_reader.compute_query_document_score(
                                           hits[i].docid, query, similarity=custom_bm25), places=4)

        custom_qld = LuceneSimilarities.qld(500)
        self.searcher.set_qld(500)

        for query in queries:
            hits = self.searcher.search(query)

            # We're going to verify that the score of each hit is about the same as the output of
            # compute_query_document_score
            for i in range(0, len(hits)):
                self.assertAlmostEqual(hits[i].score,
                                       self.index_reader.compute_query_document_score(
                                           hits[i].docid, query, similarity=custom_qld), places=4)

    def test_index_stats(self):
        self.assertEqual(3204, self.index_reader.stats()['documents'])
        self.assertEqual(14363, self.index_reader.stats()['unique_terms'])

    def test_jstring_encoding(self):
        # When using pyjnius in a version prior 1.3.0, creating a JString with non-ASCII characters resulted in a
        # failure. This test simply ensures that a compatible version of pyjnius is used. More details can be found in
        # the discussion here: https://github.com/castorini/pyserini/issues/770
        JString('zoölogy')

    def test_dump_documents_BM25(self):
        file_path = os.path.join(self.collection_dir, 'cacm_documents_bm25_dump.jsonl')
        self.index_reader.dump_documents_BM25(file_path)
        dump_file = open(file_path, 'r')

        num_lines = sum(1 for line in dump_file)
        dump_file.seek(0)
        assert num_lines == self.index_reader.stats()['documents']

        def compare_searcher(query):
            """Comparing searching with LuceneSearcher to brute-force searching through documents in dump
            The scores should match.

            Parameters
            ----------
            query : str
                The query for search.
            """
            # Search through documents BM25 dump
            query_terms = self.index_reader.analyze(query, analyzer=get_lucene_analyzer())
            heap = []  # heapq implements a min-heap, we can invert the values to have a max-heap

            for line in dump_file:
                doc = json.loads(line)
                score = 0
                for term in query_terms:
                    if term in doc['vector']:
                        score += doc['vector'][term]
                heapq.heappush(heap, (-1*score, doc['id']))
            dump_file.seek(0)

            # Using LuceneSearcher instead
            hits = self.searcher.search(query)

            for i in range(0, 10):
                top = heapq.heappop(heap)
                self.assertEqual(hits[i].docid, top[1])
                self.assertAlmostEqual(hits[i].score, -1*top[0], places=3)

        compare_searcher('I am interested in articles written either by Prieve or Udo Pooch')
        compare_searcher('Performance evaluation and modelling of computer systems')
        compare_searcher('Addressing schemes for resources in networks; resource addressing in network operating systems')

        dump_file.close()
        os.remove(file_path)

    def test_quantize_weights(self):
        dump_file_path = os.path.join(self.collection_dir, 'cacm_documents_bm25_dump.jsonl')
        quantized_file_path = os.path.join(self.collection_dir, 'cacm_documents_bm25_dump_quantized.jsonl')
        self.index_reader.dump_documents_BM25(dump_file_path)
        self.index_reader.quantize_weights(dump_file_path, quantized_file_path)

        quantized_weights_file = open(quantized_file_path, 'r')

        num_lines = sum(1 for line in quantized_weights_file)
        quantized_weights_file.seek(0)
        assert num_lines == self.index_reader.stats()['documents']

        def compare_searcher_quantized(query, tolerance=1):
            """Comparing searching with LuceneSearcher to brute-force searching through documents in dump
            If the weights are quantized the scores will not match but the rankings should still roughly match.

            Parameters
            ----------
            query : str
                The query for search.
            tolerance : int
                Number of places within which rankings should match i.e. if the ranking of some document with
                searching through documents in the dump is 2, then with a tolerance of 1 the ranking of the same
                document with Lucene searcher should be between 1-3.
            """
            query_terms = self.index_reader.analyze(query, analyzer=get_lucene_analyzer())
            heap = []
            for line in quantized_weights_file:
                doc = json.loads(line)
                score = 0
                for term in query_terms:
                    if term in doc['vector']:
                        score += doc['vector'][term]
                heapq.heappush(heap, (-1*score, doc['id']))
            quantized_weights_file.seek(0)

            hits = self.searcher.search(query)

            for i in range(0, 10):
                top = heapq.heappop(heap)
                match_within_tolerance = False
                for j in range(tolerance+1):
                    match_within_tolerance = (i-j >= 0 and hits[i-j].docid == top[1]) or (hits[i+j].docid == top[1])
                    if match_within_tolerance:
                        break
                self.assertEqual(match_within_tolerance, True)

        compare_searcher_quantized('I am interested in articles written either by Prieve or Udo Pooch')
        compare_searcher_quantized('Performance evaluation and modelling of computer systems')
        compare_searcher_quantized('Addressing schemes for resources in networks; resource addressing in network operating systems')

        quantized_weights_file.close()
        os.remove(quantized_file_path)

    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)
        for f in self.temp_folders:
            shutil.rmtree(f)


if __name__ == '__main__':
    unittest.main()

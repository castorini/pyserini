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

from pyserini import analysis, search
from pyserini.index.lucene import IndexReader


class TestIndexUtilsForLucene8(unittest.TestCase):
    # This class contains the test cases from test_index_reader that require Lucene 8 backwards compatibility.
    def setUp(self):
        # Download pre-built CACM index built using Lucene 8; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene8-index.cacm.tar.gz'
        self.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'index{}/'.format(r)

        _, _ = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

        self.index_path = os.path.join(self.index_dir, 'lucene-index.cacm')
        self.searcher = search.LuceneSearcher(self.index_path)
        self.index_reader = IndexReader(self.index_path)

        self.temp_folders = []

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
        custom_bm25 = search.LuceneSimilarities.bm25(0.8, 0.2)
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

        custom_qld = search.LuceneSimilarities.qld(500)
        self.searcher.set_qld(500)

        for query in queries:
            hits = self.searcher.search(query)

            # We're going to verify that the score of each hit is about the same as the output of
            # compute_query_document_score
            for i in range(0, len(hits)):
                self.assertAlmostEqual(hits[i].score,
                                       self.index_reader.compute_query_document_score(
                                           hits[i].docid, query, similarity=custom_qld), places=4)

    def test_dump_documents_BM25(self):
        file_path = 'collections/cacm_documents_bm25_dump.jsonl'
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
            query_terms = self.index_reader.analyze(query, analyzer=analysis.get_lucene_analyzer())
            heap = [] # heapq implements a min-heap, we can invert the values to have a max-heap

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
        dump_file_path = 'collections/cacm_documents_bm25_dump.jsonl'
        quantized_file_path = 'collections/cacm_documents_bm25_dump_quantized.jsonl'
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
            query_terms = self.index_reader.analyze(query, analyzer=analysis.get_lucene_analyzer())
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

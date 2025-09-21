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
from urllib.request import urlretrieve

from pyserini.analysis import JAnalyzer, JAnalyzerUtils, Analyzer, get_lucene_analyzer
from pyserini.index.lucene import LuceneIndexReader
from pyserini.search.lucene import LuceneSearcher


class TestAnalyzers(unittest.TestCase):
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
        self.searcher = LuceneSearcher(f'{self.index_dir}lucene9-index.cacm')
        self.index_utils = LuceneIndexReader(f'{self.index_dir}lucene9-index.cacm')

    def test_different_analyzers_are_different(self):
        self.searcher.set_analyzer(get_lucene_analyzer(stemming=False))
        hits_first = self.searcher.search('information retrieval')
        self.searcher.set_analyzer(get_lucene_analyzer())
        hits_second = self.searcher.search('information retrieval')
        self.assertNotEqual(hits_first, hits_second)

    def test_analyze_with_analyzer(self):
        analyzer = get_lucene_analyzer(stemming=False)
        self.assertTrue(isinstance(analyzer, JAnalyzer))
        query = 'information retrieval'
        only_tokenization = JAnalyzerUtils.analyze(analyzer, query)
        token_list = []
        for token in only_tokenization.toArray():
            token_list.append(token)
        self.assertEqual(token_list, ['information', 'retrieval'])

    def test_analysis(self):
        # Default is Porter stemmer
        analyzer = Analyzer(get_lucene_analyzer())
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['citi', 'buse', 'run', 'time'])

        # Specify Porter stemmer explicitly
        analyzer = Analyzer(get_lucene_analyzer(stemmer='porter'))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['citi', 'buse', 'run', 'time'])

        # Specify Krovetz stemmer explicitly
        analyzer = Analyzer(get_lucene_analyzer(stemmer='krovetz'))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['city', 'bus', 'running', 'time'])

        # No stemming
        analyzer = Analyzer(get_lucene_analyzer(stemming=False))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['city', 'buses', 'running', 'time'])

        # No stopword filter, no stemming
        analyzer = Analyzer(get_lucene_analyzer(stemming=False, stopwords=False))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['city', 'buses', 'are', 'running', 'on', 'time'])

        # No stopword filter, with stemming
        analyzer = Analyzer(get_lucene_analyzer(stemming=True, stopwords=False))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('City buses are running on time.')
        self.assertEqual(tokens, ['citi', 'buse', 'ar', 'run', 'on', 'time'])

        # HuggingFace analyzer, with bert wordpiece tokenizer
        analyzer = Analyzer(get_lucene_analyzer(language="hgf_tokenizer", huggingFaceTokenizer="bert-base-uncased"))
        self.assertTrue(isinstance(analyzer, Analyzer))
        tokens = analyzer.analyze('This tokenizer generates wordpiece tokens')
        self.assertEqual(tokens, ['this', 'token', '##izer', 'generates', 'word', '##piece', 'token', '##s'])

    def test_invalid_analyzer_wrapper(self):
        # Invalid JAnalyzer, make sure we get an exception.
        with self.assertRaises(TypeError):
            Analyzer('str')

    def test_invalid_analysis(self):
        # Invalid configuration, make sure we get an exception.
        with self.assertRaises(ValueError):
            Analyzer(get_lucene_analyzer('blah'))

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)

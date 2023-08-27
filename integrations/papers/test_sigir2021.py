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

"""Integration tests for commands in Lin et al. (SIGIR 2021) paper."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score_msmarco
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder
from pyserini.hsearch import HybridSearcher
from pyserini.index import IndexReader
from pyserini.search import SimpleSearcher
from pyserini.search import get_topics, get_qrels


class TestSIGIR2021(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_figure1(self):
        """Sample code in Figure 1."""

        searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
        hits = searcher.search('what is a lobster roll?', 10)

        self.assertAlmostEqual(hits[0].score, 11.00830, delta=0.0001)
        self.assertEqual(hits[0].docid, '7157707')

        self.assertAlmostEqual(hits[9].score, 9.92200, delta=0.0001)
        self.assertEqual(hits[9].docid, '6234461')

        self.assertEqual(len(hits), 10)

    def test_figure2(self):
        """Sample code in Figure 2."""

        encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
        searcher = SimpleDenseSearcher.from_prebuilt_index('msmarco-passage-tct_colbert-hnsw', encoder)
        hits = searcher.search('what is a lobster roll')

        self.assertAlmostEqual(hits[0].score, 70.53741, delta=0.0001)
        self.assertEqual(hits[0].docid, '7157710')

        self.assertAlmostEqual(hits[9].score, 69.01737, delta=0.0001)
        self.assertEqual(hits[9].docid, '2920399')

        self.assertEqual(len(hits), 10)

    def test_figure3(self):
        """Sample code in Figure 3."""

        ssearcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
        encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco')
        dsearcher = SimpleDenseSearcher.from_prebuilt_index('msmarco-passage-tct_colbert-hnsw', encoder)
        hsearcher = HybridSearcher(dsearcher, ssearcher)

        hits = hsearcher.search('what is a lobster roll')

        self.assertAlmostEqual(hits[0].score, 71.56023, delta=0.0001)
        self.assertEqual(hits[0].docid, '7157715')

        self.assertAlmostEqual(hits[9].score, 70.07635, delta=0.0001)
        self.assertEqual(hits[9].docid, '7157708')

        self.assertEqual(len(hits), 10)

    def test_figure4(self):
        """Sample code in Figure 4."""

        topics = get_topics('msmarco-passage-dev-subset')
        qrels = get_qrels('msmarco-passage-dev-subset')

        self.assertEqual(len(topics), 6980)
        self.assertEqual(len(qrels), 6980)

        # Compute the average length of queries:
        avg_qlen = sum([len(topics[t]['title'].split()) for t in topics])/len(topics)

        # Compute the average number of relevance judgments per query:
        avg_qrels = sum([len(qrels[t]) for t in topics])/len(topics)

        self.assertAlmostEqual(avg_qlen, 5.925, delta=0.001)
        self.assertAlmostEqual(avg_qrels, 1.065, delta=0.001)

    def test_figure5(self):
        """Sample code in Figure 5."""

        # Initialize from a pre-built index:
        reader = IndexReader.from_prebuilt_index('robust04')

        terms = reader.terms()
        term = next(terms)
        self.assertEqual(term.term, '0')
        self.assertEqual(term.df, 10826)
        self.assertEqual(term.cf, 33491)

        term = next(terms)

        self.assertEqual(term.term, '0,0')
        self.assertEqual(term.df, 2)
        self.assertEqual(term.cf, 2)

        # Analyze a term:
        term = 'atomic'
        analyzed = reader.analyze(term)
        self.assertEqual(analyzed[0], 'atom')

        # Directly fetch term statistics for a term:
        df, cf = reader.get_term_counts(term)
        self.assertEqual(df, 5219)
        self.assertEqual(cf, 9144)

        # Traverse postings for a term:
        postings_list = reader.get_postings_list(term)
        self.assertEqual(len(postings_list), 5219)
        self.assertEqual(postings_list[0].docid, 432)
        self.assertEqual(postings_list[0].tf, 1)
        self.assertEqual(postings_list[0].positions, [137])
        self.assertEqual(postings_list[5218].docid, 527779)
        self.assertEqual(postings_list[5218].tf, 1)
        self.assertEqual(postings_list[5218].positions, [21])

        # Examples of manipulating document vectors:
        tf = reader.get_document_vector('LA071090-0047')
        tp = reader.get_term_positions('LA071090-0047')
        df = {
            term: (reader.get_term_counts(term, analyzer=None))[0]
            for term in tf.keys()
        }
        bm25_vector = {
            term: reader.compute_bm25_term_weight('LA071090-0047',
                                                  term,
                                                  analyzer=None)
            for term in tf.keys()
        }

        self.assertEqual(tf['hubbl'], 12)
        self.assertEqual(tp['caught'], [42, 624, 960])
        self.assertEqual(df['problem'], 82225)
        self.assertAlmostEqual(bm25_vector['hubbl'], 7.49397, delta=0.001)
        self.assertAlmostEqual(bm25_vector['earth'], 2.64872, delta=0.001)

    def test_section3_3(self):
        """Sample code in Section 3.3."""

        output_file = 'run.msmarco-passage.txt'
        self.temp_files.append(output_file)
        run_cmd = f'python -m pyserini.search --topics msmarco-passage-dev-subset \
                      --index msmarco-passage --output {output_file} \
                      --bm25 --output-format msmarco'
        status = os.system(run_cmd)
        self.assertEqual(status, 0)

        eval_cmd = f'python -m pyserini.eval.msmarco_passage_eval \
                       msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(eval_cmd)
        score = parse_score_msmarco(stdout, "MRR @10")
        self.assertAlmostEqual(score, 0.1874, delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()

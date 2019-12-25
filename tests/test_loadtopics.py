import unittest

from pyserini.search import pysearch

class TestLoadTopics(unittest.TestCase):

    def test_robust04(self):
        topics = pysearch.get_topics('robust04')
        self.assertEqual(len(topics), 250)

    def test_core17(self):
        topics = pysearch.get_topics('core17')
        self.assertEqual(len(topics), 50)

    def test_core18(self):
        topics = pysearch.get_topics('core18')
        self.assertEqual(len(topics), 50)

    def test_car15(self):
        topics = pysearch.get_topics('car17v1.5_benchmarkY1test')
        self.assertEqual(len(topics), 2125)

    def test_car20(self):
        topics = pysearch.get_topics('car17v2.0_benchmarkY1test')
        self.assertEqual(len(topics), 2254)

    def test_msmarco_doc(self):
        topics = pysearch.get_topics('msmarco_doc_dev')
        self.assertEqual(len(topics), 5193)

    def test_msmarco_passage(self):
        topics = pysearch.get_topics('msmarco_passage_dev_subset')
        self.assertEqual(len(topics), 6980)

if __name__ == '__main__':
    unittest.main()

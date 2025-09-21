import json
import unittest

from pyserini.encode import ArcticDocumentEncoder, ArcticQueryEncoder
from pyserini.search import get_topics


class TestEncodeArctic(unittest.TestCase):
    def test_arctic_doc_encoder(self):
        texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = ArcticDocumentEncoder('Snowflake/snowflake-arctic-embed-m-v1.5', device='cpu', truncate_to_256=True)
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], 0.05097485, places=4)
        self.assertAlmostEqual(vectors[0][-1], 0.04520516, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.027567765, places=4)
        self.assertAlmostEqual(vectors[2][-1], 4.9405815e-05, places=4)
    
    def test_arctic_query_encoder(self):
        pass
        #TODO: Implement test_arctic_query_encoder after beir regression incorporated


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import numpy as np

# Mock embeddings
MOCK_CORPUS_EMBEDDINGS = np.array([[0.1, 0.2, 0.3],
                                   [0.4, 0.5, 0.6],
                                   [0.7, 0.8, 0.9]])
MOCK_QUERY_EMBEDDINGS = np.array([[0.1, 0.2, 0.3]])


class TestUniIREncoder(unittest.TestCase):
    def test_uniir_corpus_encoder(self):
        try:
            from pyserini.encode.optional._uniir import UniIRCorpusEncoder
        except ImportError:
            raise ValueError("uniir-for-pyserini package is required for this test. Please run 'pip install pyserini[optional]' to install it.")

        with patch("pyserini.encode.optional._uniir.CorpusEncoder") as MockCorpus:
            mock_corpus = MagicMock()
            mock_corpus.encode.return_value = MOCK_CORPUS_EMBEDDINGS
            MockCorpus.return_value = mock_corpus

            encoder = UniIRCorpusEncoder(model_name="clip_sf_large", device="cpu")
            embeddings = encoder.encode(
                dids=["1", "2", "3"],
                img_paths=["test1.jpg", None, "test3.jpg"],
                modalitys=["image", "text", "image,text"],
                txts=[None, "test", "test"]
            )

            self.assertEqual(len(embeddings), 3)
            self.assertEqual(embeddings.shape[1], 3)
            np.testing.assert_array_equal(embeddings, MOCK_CORPUS_EMBEDDINGS)

    def test_uniir_query_encoder(self):
        try:
            from pyserini.encode.optional._uniir import UniIRQueryEncoder
        except ImportError:
            raise ValueError("uniir-for-pyserini package is required for this test. Please run 'pip install pyserini[optional]' to install it.")

        with patch("pyserini.encode.optional._uniir.QueryEncoder") as MockQuery:
            mock_query = MagicMock()
            mock_query.encode.return_value = MOCK_QUERY_EMBEDDINGS
            MockQuery.return_value = mock_query

            encoder = UniIRQueryEncoder(encoder_dir="clip_sf_large", device="cpu")
            query_embeddings = encoder.encode(
                qid=1,
                query_txt="test query",
                query_img_path="test_query.jpg",
                query_modality="image,text"
            )

            self.assertEqual(len(query_embeddings), 1)
            self.assertEqual(query_embeddings.shape[1], 3)
            np.testing.assert_array_equal(query_embeddings, MOCK_QUERY_EMBEDDINGS)

if __name__ == "__main__":
    unittest.main()

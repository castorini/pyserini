import unittest
from unittest.mock import patch

class TestUniIREncoder(unittest.TestCase):
    def test_uniir_encoder_missing_package(self):
        """Test UniIR corpus encoder fails when uniir-for-pyserini package is missing"""
        with patch.dict('sys.modules', {'uniir_for_pyserini': None}):
            from pyserini.encode.__main__ import init_encoder
            with self.assertRaises(ValueError) as context:
                init_encoder('model', 'uniir', 'cpu', 'cls', True, None, False)
            self.assertIn("uniir-for-pyserini package is not installed", str(context.exception))

    def test_uniir_query_encoder_missing_package(self):
        """Test UniIR query encoder fails when uniir-for-pyserini package is missing"""
        with patch.dict('sys.modules', {'uniir_for_pyserini': None}):
            from pyserini.search.faiss.__main__ import init_query_encoder
            with self.assertRaises(ValueError) as context:
                init_query_encoder(
                    encoder='model',
                    encoder_class='uniir',
                    tokenizer_name=None,
                    topics_name=None,
                    encoded_queries=None,
                    device='cpu',
                    max_length=512,
                    pooling='cls',
                    l2_norm=True,
                    prefix=None,
                )
            self.assertIn("uniir-for-pyserini package is not installed", str(context.exception))

    def test_uniir_encoder_with_package_available(self):
        """Test UniIR encoder works when package is available (mocked)"""
        from unittest.mock import MagicMock
        import numpy as np

        MOCK_CORPUS_EMBEDDINGS = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])
        MOCK_QUERY_EMBEDDINGS = np.array([[0.1, 0.2, 0.3]])
        
        mock_corpus_encoder = MagicMock()
        mock_corpus_encoder.encode.return_value = MOCK_CORPUS_EMBEDDINGS
        
        mock_query_encoder = MagicMock()
        mock_query_encoder.encode.return_value = MOCK_QUERY_EMBEDDINGS
        
        with patch.dict('sys.modules', {
            'uniir_for_pyserini': MagicMock(),
            'uniir_for_pyserini.pyserini_integration': MagicMock(),
            'uniir_for_pyserini.pyserini_integration.uniir_corpus_encoder': MagicMock(CorpusEncoder=lambda **kwargs: mock_corpus_encoder),
            'uniir_for_pyserini.pyserini_integration.uniir_query_encoder': MagicMock(QueryEncoder=lambda **kwargs: mock_query_encoder)
        }):
            from pyserini.encode.__main__ import init_encoder
            
            corpus_encoder = init_encoder('clip_sf_large', 'uniir', 'cpu', 'cls', True, None, True)
            self.assertIsNotNone(corpus_encoder)
            
            test_dids = ["1", "2", "3"]
            test_img_paths = ["test1.jpg", None, "test3.jpg"]
            test_txts = [None, "test", "test"]
            test_modalitys = ["image", "text", "image,text"]
              
            corpus_embeddings = corpus_encoder.encode(
                dids=test_dids,
                img_paths=test_img_paths,
                modalitys=test_modalitys,
                txts=test_txts
            )
             
            self.assertEqual(len(corpus_embeddings), 3)  
            self.assertEqual(corpus_embeddings.shape[1], 3)
            np.testing.assert_array_equal(corpus_embeddings, MOCK_CORPUS_EMBEDDINGS)

            from pyserini.search.faiss.__main__ import init_query_encoder
            query_encoder = init_query_encoder(
                encoder='clip_sf_large',
                encoder_class='uniir',
                tokenizer_name=None,
                topics_name=None,
                encoded_queries=None,
                device='cpu',
                max_length=512,
                pooling='cls',
                l2_norm=True,
                prefix=None,
            )
            self.assertIsNotNone(query_encoder)

            query_embeddings = query_encoder.encode(
                qid=1,
                query_txt="test query",
                query_img_path="test_query.jpg",
                query_modality="image,text"
            )

            self.assertEqual(len(query_embeddings), 1)
            self.assertEqual(query_embeddings.shape[1], 3)
            np.testing.assert_array_equal(query_embeddings, MOCK_QUERY_EMBEDDINGS)
  
if __name__ == '__main__':
    unittest.main()

import unittest

class TestUniIREncoderInstantiation(unittest.TestCase):
    def test_uniir_corpus_encoder_creation(self):
        from pyserini.encode.optional._uniir import UniIRCorpusEncoder
        from uniir_for_pyserini.pyserini_integration.uniir_corpus_encoder import CorpusEncoder

        encoder = UniIRCorpusEncoder(model_name="clip_sf_large", device="cpu")

        assert encoder.corpus_encoder is not None
        assert isinstance(encoder.corpus_encoder, CorpusEncoder)

    def test_uniir_query_encoder_creation(self):
        from pyserini.encode.optional._uniir import UniIRQueryEncoder
        from uniir_for_pyserini.pyserini_integration.uniir_query_encoder import QueryEncoder

        encoder = UniIRQueryEncoder(encoder_dir="clip_sf_large", device="cpu")

        assert encoder.query_encoder is not None
        assert isinstance(encoder.query_encoder, QueryEncoder)

if __name__ == "__main__":
    unittest.main()

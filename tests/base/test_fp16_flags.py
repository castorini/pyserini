import unittest
import warnings
from unittest.mock import patch

from pyserini.encode.__main__ import _warn_if_document_fp16_is_ignored
from pyserini.search.faiss import __main__ as faiss_main


class _FakeEncoder:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class _DocumentEncoderWithFp16:
    def encode(self, texts, fp16=False):
        return texts, fp16


class _DocumentEncoderWithoutFp16:
    def encode(self, texts, **kwargs):
        return texts


class Fp16FlagTests(unittest.TestCase):
    def test_query_encoder_warns_when_fp16_is_ignored(self):
        with patch.dict(
            faiss_main.query_encoder_class_map, {"auto": _FakeEncoder}, clear=False
        ):
            with self.assertWarnsRegex(UserWarning, "not implemented"):
                result = faiss_main.init_query_encoder(
                    "dummy",
                    "auto",
                    None,
                    "topics",
                    None,
                    "cpu",
                    None,
                    "cls",
                    False,
                    None,
                    fp16=True,
                )
        self.assertTrue(result.kwargs["fp16"])

    def test_supported_query_encoder_does_not_warn(self):
        with patch.dict(
            faiss_main.query_encoder_class_map, {"qwen3": _FakeEncoder}, clear=False
        ):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                faiss_main.init_query_encoder(
                    "dummy",
                    "qwen3",
                    None,
                    "topics",
                    None,
                    "cpu",
                    None,
                    "cls",
                    False,
                    None,
                    fp16=True,
                )
        self.assertFalse(
            [warning for warning in caught if "not implemented" in str(warning.message)]
        )

    def test_document_encoder_warning_uses_encode_signature(self):
        with self.assertWarnsRegex(UserWarning, "document encoder"):
            _warn_if_document_fp16_is_ignored(_DocumentEncoderWithoutFp16(), True)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            _warn_if_document_fp16_is_ignored(_DocumentEncoderWithFp16(), True)
        self.assertFalse(caught)


if __name__ == "__main__":
    unittest.main()

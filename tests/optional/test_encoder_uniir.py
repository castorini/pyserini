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

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

from pyserini.encode import AutoQueryEncoder
from tests.base.encoder.utils import assert_encode_query_cli_output, assert_query_encoder_output


EXPECTED_VALUES = [(0.01698, -0.00727, 5), (-0.44893, 0.04673, 5)]


class TestEncodeDistilBertKd(unittest.TestCase):
    def test_distilbert_kd_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco', EXPECTED_VALUES)

    def test_distilbert_kd_query_encoder_direct(self):
        encoder = AutoQueryEncoder('sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco', device='cpu')
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES)


if __name__ == '__main__':
    unittest.main()

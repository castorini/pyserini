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

import filecmp
import os
import unittest


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.output_path = 'output_test_fusion.txt'

    def test_reciprocal_rank_fusion_simple(self):
        input_paths = ['tests/resources/simple_trec_run_fusion_1.txt', 'tests/resources/simple_trec_run_fusion_2.txt']
        verify_path = 'tests/resources/simple_trec_run_rrf_verify.txt'

        qruns_str = ' '.join(input_paths)
        os.system(
            f'python -m pyserini.fusion --method rrf --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))

    def test_interpolation_fusion_simple(self):
        input_paths = ['tests/resources/simple_trec_run_fusion_1.txt', 'tests/resources/simple_trec_run_fusion_2.txt']
        verify_path = 'tests/resources/simple_trec_run_interpolation_verify.txt'

        qruns_str = ' '.join(input_paths)
        os.system(
            f'python -m pyserini.fusion --method interpolation --alpha 0.4 --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))

    def test_average_fusion_simple(self):
        input_paths = ['tests/resources/simple_trec_run_fusion_1.txt', 'tests/resources/simple_trec_run_fusion_2.txt']
        verify_path = 'tests/resources/simple_trec_run_average_verify.txt'

        qruns_str = ' '.join(input_paths)
        os.system(
            f'python -m pyserini.fusion --method average --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))

    def test_reciprocal_rank_fusion_complex(self):
        os.system('wget -q -nc https://www.dropbox.com/s/duimcackueph2co/anserini.covid-r2.abstract.qq.bm25.txt.gz')
        os.system('wget -q -nc https://www.dropbox.com/s/iswpuj9tf5pj5ei/anserini.covid-r2.full-text.qq.bm25.txt.gz')
        os.system('wget -q -nc https://www.dropbox.com/s/da7jg1ho5ubl8jt/anserini.covid-r2.paragraph.qq.bm25.txt.gz')
        os.system('wget -q -nc https://www.dropbox.com/s/wqb0vhxp98g7dxh/anserini.covid-r2.fusion1.txt.gz')
        os.system('gunzip -f anserini.covid-r2.*.txt.gz')

        txt_paths = ['anserini.covid-r2.abstract.qq.bm25.txt',
                     'anserini.covid-r2.full-text.qq.bm25.txt', 'anserini.covid-r2.paragraph.qq.bm25.txt']

        qruns_str = ' '.join(txt_paths)
        os.system(
            f'python -m pyserini.fusion --method rrf --runs {qruns_str} --output {self.output_path} --runtag reciprocal_rank_fusion_k=60')
        verify_path = 'anserini.covid-r2.fusion1.txt'
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))
        os.system('rm anserini.covid-r2.*')
    
    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == '__main__':
    unittest.main()

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

import os
import unittest

from pyserini.search import get_topics
from pyserini.search.lucene import LuceneSearcher, LuceneFlatDenseSearcher
from pyserini.search.faiss import FaissSearcher
from pyserini.encode import AutoQueryEncoder

def compare_trec_files_with_tolerance(file1_path, file2_path, tolerance=1e-4):
    """Compare two TREC files with tolerance for floating-point precision differences."""
    try:
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except FileNotFoundError:
        return False
    if len(lines1) != len(lines2):
        return False
    # Compare each line between the two files
    for i, (line1, line2) in enumerate(zip(lines1, lines2)):
        if line1.strip() != line2.strip():
            parts1 = line1.strip().split()
            parts2 = line2.strip().split()
            if len(parts1) != len(parts2):
                return False
            # parts[0]=qid, parts[1]=Q0, parts[2]=docid, parts[3]=rank, parts[4]=score, parts[5]=runtag
            if (parts1[0] == parts2[0] and parts1[1] == parts2[1] and
                parts1[2] == parts2[2] and parts1[3] == parts2[3] and
                parts1[5] == parts2[5]):
                try:
                    score1 = float(parts1[4])
                    score2 = float(parts2[4])
                    diff = abs(score1 - score2)
                    if diff > tolerance:
                        return False
                except ValueError:
                    return False
            else:
                return False
    return True

def retrieve_and_save_runs(self, searcher, topics_name, searcher_type='bm25', qids=None, test_name=None):
    """Retrieve search results and save to file."""
    topics = get_topics(topics_name)
    if qids is None:
        qids = list(topics.keys())[:5]
    
    if test_name is None:
        test_name = self._testMethodName if hasattr(self, '_testMethodName') else 'unknown_test'
    run_path = f'{test_name}_{searcher_type}.txt'
    
    with open(run_path, 'w') as run_file:
        for qid in qids:
            query = topics[qid]['title']
            if searcher_type == 'bm25':
                hits = searcher.search(query, k=10)
            else:  # dense
                raw_hits = searcher.search(query, k=20)
                hits = [h for h in raw_hits if h.docid != qid][:10]
            for rank, hit in enumerate(hits, start=1):
                run_file.write(f"{qid} Q0 {hit.docid} {rank} {hit.score:.6f} {searcher_type}_search\n")

    self.assertTrue(os.path.exists(run_path), f"{searcher_type} run file not created: {run_path}")
    return run_path

def run_fusion_on_saved_runs(self, bm25_path, dense_path, method, expected_results, runtag, extra_args='', output_path=None, qids=None):
    """Run fusion on saved run files and validate results."""
    if output_path is None:
        output_path = self.output_path
    
    qruns_str = f'{bm25_path} {dense_path}'
    cmd = f'python -m pyserini.fusion --method {method} {extra_args} --runs {qruns_str} --output {output_path} --runtag {runtag} --k 10 --depth 1000'
    os.system(cmd)
    self.assertTrue(os.path.exists(output_path), f"{method} fusion run file not created: {output_path}")

    with open(output_path, 'r') as f:
        lines = f.readlines()
    if expected_results:
        for i, (expected_qid, expected_docid, expected_rank, expected_score) in enumerate(expected_results):
            if i < len(lines):
                line = lines[i].strip()
                parts = line.split()
                self.assertEqual(len(parts), 6)
                self.assertEqual(parts[0], expected_qid)
                self.assertEqual(parts[1], 'Q0')
                self.assertEqual(parts[2], expected_docid)
                self.assertEqual(int(parts[3]), expected_rank)
                self.assertAlmostEqual(float(parts[4]), expected_score, places=4)
                self.assertEqual(parts[5], runtag)

class TestFusion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_file_dir = os.path.dirname(__file__)
        cls.resource_dir = os.path.join(os.path.dirname(test_file_dir), 'resources')
        cls.expected_results = {
            'rrf': [
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03a', 1, 0.03252247488101534),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01b', 2, 0.03200204813108039),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02b', 3, 0.03149801587301587),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03a', 4, 0.03076923076923077),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02a', 5, 0.030330882352941176),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01a', 6, 0.03007688828584351),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01b', 7, 0.03007688828584351),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03b', 8, 0.028991596638655463),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03b', 9, 0.028985507246376812),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01a', 10, 0.01639344262295082),
            ],
            'interpolation': [
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01a', 1, 149.4593505),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03a', 2, 49.1152155),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01b', 3, 44.2424875),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02b', 4, 44.1182435),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03a', 5, 41.5627015),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01b', 6, 40.811),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01a', 7, 40.463996),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02a', 8, 39.7919365),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03b', 9, 33.580975),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03b', 10, 33.2027485),
            ],
            'average': [
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01a', 1, 149.4593505),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03a', 2, 49.1152155),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01b', 3, 44.2424875),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02b', 4, 44.1182435),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03a', 5, 41.5627015),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01b', 6, 40.811),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01a', 7, 40.463996),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02a', 8, 39.7919365),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03b', 9, 33.580975),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03b', 10, 33.2027485),
            ],
            'normalize': [
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03a', 1, 1.1361973700957502),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01b', 2, 1.0801439128220096),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02b', 3, 1.0236731626672213),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con01a', 4, 1.0),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03a', 5, 0.914668969951034),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro02a', 6, 0.9023852508973691),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01a', 7, 0.39388699776179686),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro01b', 8, 0.37685087599339195),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-pro03b', 9, 0.3064502564965106),
                ('test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con03b', 10, 0.20806094221452542),
            ]
        }

    def setUp(self):
        self.output_path = 'output_test_fusion.txt'
        encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', pooling='cls', l2_norm=True, prefix='Represent this sentence for searching relevant passages:')
        self.bm25_searcher = LuceneSearcher.from_prebuilt_index('beir-v1.0.0-arguana.flat')
        self.lucene_dense_searcher = LuceneFlatDenseSearcher.from_prebuilt_index('beir-v1.0.0-arguana.bge-base-en-v1.5.flat', encoder='BgeBaseEn15')
        self.faiss_dense_searcher_normalized = FaissSearcher.from_prebuilt_index('beir-v1.0.0-arguana.bge-base-en-v1.5', encoder, True)
        self.qids = ['test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con02a']
        self.bm25_path = retrieve_and_save_runs(self, self.bm25_searcher, 'beir-v1.0.0-arguana-test', 'bm25', self.qids, "bm25")
        self.lucene_flat_dense_path = retrieve_and_save_runs(self, self.lucene_dense_searcher, 'beir-v1.0.0-arguana-test', 'lucene_flat_dense', self.qids, "lucene_flat_dense")
        self.faiss_flat_dense_normalized_path = retrieve_and_save_runs(self, self.faiss_dense_searcher_normalized, 'beir-v1.0.0-arguana-test', 'faiss_flat_dense_normalized', self.qids, "faiss_flat_dense")

    def test_reciprocal_rank_fusion_simple(self):
        input_paths = [os.path.join(self.resource_dir, 'simple_trec_run_fusion_1.txt'),
                       os.path.join(self.resource_dir, 'simple_trec_run_fusion_2.txt')]
        verify_path = os.path.join(self.resource_dir, 'simple_trec_run_rrf_verify.txt')

        qruns_str = ' '.join(input_paths)
        os.system(f'python -m pyserini.fusion --method rrf --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(compare_trec_files_with_tolerance(verify_path, self.output_path))

    def test_interpolation_fusion_simple(self):
        input_paths = [os.path.join(self.resource_dir, 'simple_trec_run_fusion_1.txt'),
                       os.path.join(self.resource_dir, 'simple_trec_run_fusion_2.txt')]
        verify_path = os.path.join(self.resource_dir, 'simple_trec_run_interpolation_verify.txt')

        qruns_str = ' '.join(input_paths)
        os.system(f'python -m pyserini.fusion --method interpolation --alpha 0.4 --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(compare_trec_files_with_tolerance(verify_path, self.output_path))

    def test_average_fusion_simple(self):
        input_paths = [os.path.join(self.resource_dir, 'simple_trec_run_fusion_1.txt'),
                       os.path.join(self.resource_dir, 'simple_trec_run_fusion_2.txt')]
        verify_path = os.path.join(self.resource_dir, 'simple_trec_run_average_verify.txt')

        qruns_str = ' '.join(input_paths)
        os.system(f'python -m pyserini.fusion --method average --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(compare_trec_files_with_tolerance(verify_path, self.output_path))

    def test_normalize_fusion_simple(self):
        input_paths = [os.path.join(self.resource_dir, 'simple_trec_run_fusion_1.txt'),
                       os.path.join(self.resource_dir, 'simple_trec_run_fusion_2.txt')]
        verify_path = os.path.join(self.resource_dir, 'simple_fusion_normalize_verify.txt')

        qruns_str = ' '.join(input_paths)
        os.system(f'python -m pyserini.fusion --method normalize --runs {qruns_str} --output {self.output_path} --runtag test')
        self.assertTrue(compare_trec_files_with_tolerance(verify_path, self.output_path))

    def test_reciprocal_rank_fusion_complex(self):
        os.system('wget -q -nc https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round2/anserini.covid-r2.abstract.qq.bm25.txt.gz')
        os.system('wget -q -nc https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round2/anserini.covid-r2.full-text.qq.bm25.txt.gz')
        os.system('wget -q -nc https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round2/anserini.covid-r2.paragraph.qq.bm25.txt.gz')
        os.system('wget -q -nc https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round2/anserini.covid-r2.fusion1.txt.gz')
        os.system('gunzip -f anserini.covid-r2.*.txt.gz')

        txt_paths = ['anserini.covid-r2.abstract.qq.bm25.txt',
                     'anserini.covid-r2.full-text.qq.bm25.txt',
                     'anserini.covid-r2.paragraph.qq.bm25.txt']

        qruns_str = ' '.join(txt_paths)
        os.system(f'python -m pyserini.fusion --method rrf --runs {qruns_str} --output {self.output_path} --runtag reciprocal_rank_fusion_k=60')
        self.assertTrue(compare_trec_files_with_tolerance('anserini.covid-r2.fusion1.txt', self.output_path))
        os.system('rm anserini.covid-r2.*')

    def test_lucene_flat_dense_rrf_fusion(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.lucene_flat_dense_path, 'rrf', self.expected_results['rrf'], 'fusion_rrf', '--rrf.k 60')

    def test_lucene_flat_dense_interpolation_fusion(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.lucene_flat_dense_path, 'interpolation', self.expected_results['interpolation'], 'fusion_interpolation', '--alpha 0.5')

    def test_lucene_flat_dense_average_fusion(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.lucene_flat_dense_path, 'average', self.expected_results['average'], 'fusion_average')

    def test_lucene_flat_dense_normalize_fusion(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.lucene_flat_dense_path, 'normalize', self.expected_results['normalize'], 'fusion_normalize')

    def test_faiss_flat_dense_rrf_fusion_normalize_distances(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.faiss_flat_dense_normalized_path, 'rrf', self.expected_results['rrf'], 'fusion_rrf', '--rrf.k 60')

    def test_faiss_flat_dense_interpolation_fusion_normalize_distances(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.faiss_flat_dense_normalized_path, 'interpolation', self.expected_results['interpolation'], 'fusion_interpolation', '--alpha 0.5')

    def test_faiss_flat_dense_average_fusion_normalize_distances(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.faiss_flat_dense_normalized_path, 'average', self.expected_results['average'], 'fusion_average')

    def test_faiss_flat_dense_normalize_fusion_normalize_distances(self):
        run_fusion_on_saved_runs(self, self.bm25_path, self.faiss_flat_dense_normalized_path, 'normalize', self.expected_results['normalize'], 'fusion_normalize')

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.unlink(self.output_path)
        if hasattr(self, 'bm25_path') and os.path.exists(self.bm25_path):
            os.unlink(self.bm25_path)
        if hasattr(self, 'lucene_flat_dense_path') and os.path.exists(self.lucene_flat_dense_path):
            os.unlink(self.lucene_flat_dense_path)
        if hasattr(self, 'faiss_flat_dense_normalized_path') and os.path.exists(self.faiss_flat_dense_normalized_path):
            os.unlink(self.faiss_flat_dense_normalized_path)

if __name__ == '__main__':
    unittest.main()

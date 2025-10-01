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

"""Integration tests for DPR model using pre-encoded queries."""

import json
import multiprocessing
import os
import unittest

from integrations.core.utils import clean_files, run_command, parse_score_qa
from pyserini.encode import QueryEncoder
from pyserini.search import get_topics


class TestDpr(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 16
        self.batch_size = self.threads * 32

        half_cores = int(multiprocessing.cpu_count() / 2)
        # If server supports more threads, then use more threads.
        # As a heuristic, use up half up available CPU cores.
        if half_cores > self.threads:
            self.threads = half_cores
            self.batch_size = half_cores * 32

    def test_dpr_nq_test_bf_otf(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-nq-test \
                             --index wikipedia-dpr-100w.dpr-multi \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.7947, delta=0.0002)

    def test_dpr_nq_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.hybrid dense  --index wikipedia-dpr-100w.dpr-multi \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr-100w \
                             fusion --alpha 1.3 \
                             run    --topics dpr-nq-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8260, places=4)

    def test_dpr_nq_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_trivia_test_bf_otf(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-trivia-test \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --index wikipedia-dpr-100w.dpr-multi \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.7887, places=4)

    def test_dpr_trivia_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.hybrid dense  --index wikipedia-dpr-100w.dpr-multi \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr-100w \
                             fusion --alpha 0.95 \
                             run    --topics dpr-trivia-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8264, places=4)

    def test_dpr_trivia_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-trivia-test')
        topics = get_topics('dpr-trivia-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_wq_test_bf_otf(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-wq-test \
                             --index wikipedia-dpr-100w.dpr-multi \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.7505, places=4)

    def test_dpr_wq_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.hybrid dense  --index wikipedia-dpr-100w.dpr-multi \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr-100w \
                             fusion --alpha 0.95 \
                             run    --topics dpr-wq-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.7712, places=4)

    def test_dpr_wq_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-wq-test')
        topics = get_topics('dpr-wq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_curated_test_bf_otf(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-curated-test \
                             --index wikipedia-dpr-100w.dpr-multi \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file} \
                                                           --regex'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8876, places=4)

    def test_dpr_curated_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.hybrid dense  --index wikipedia-dpr-100w.dpr-multi \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr-100w \
                             fusion --alpha 1.05 \
                             run    --topics dpr-curated-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file} \
                                                           --regex'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.9006, places=4)

    def test_dpr_curated_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-curated-test')
        topics = get_topics('dpr-curated-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_squad_test_bf_otf(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-squad-test \
                             --index wikipedia-dpr-100w.dpr-multi \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.5199, places=4)

    def test_dpr_squad_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.search.hybrid dense  --index wikipedia-dpr-100w.dpr-multi \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr-100w \
                             fusion --alpha 2.0 \
                             run    --topics dpr-squad-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        # This appears to be a flaky test case; previously, we were getting a score of 0.7511, per
        # https://github.com/castorini/pyserini/pull/1273/files#diff-799c2c339e1d7defa31fa1e82f9b16886269b37805376ef93f7c8afedcee574e
        # Sometimes we get 0.7512. Fix is to reduce tolerance.
        self.assertAlmostEqual(score, 0.7514, places=3)

    def test_dpr_squad_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-squad-test')
        topics = get_topics('dpr-squad-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_convert_trec_run_to_dpr_retrieval_run(self):
        trec_run_file = 'tests/resources/simple_test_run_convert_trec_run_dpr.trec'
        topics_file = 'tests/resources/simple_topics_dpr.txt'
        dpr_run_file = 'test_run.convert.trec_run.dpr.json'
        collection_path = "tests/resources/sample_collection_dense"
        topic_reader = "io.anserini.search.topicreader.DprNqTopicReader"
        index_dir = 'temp_index'

        self.temp_files.extend([dpr_run_file, index_dir])
        cmd1 = f'python -m pyserini.index.lucene -collection JsonCollection ' + \
               f'-generator DefaultLuceneDocumentGenerator ' + \
               f'-threads 1 -input {collection_path} -index {index_dir} -storeRaw'

        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics-file {topics_file} \
                                                           --topics-reader {topic_reader} \
                                                           --index {index_dir} \
                                                           --input {trec_run_file} \
                                                           --output {dpr_run_file}'
        _ = os.system(cmd1)
        _ = os.system(cmd2)

        with open(dpr_run_file) as f:
            topic_data = json.load(f)

        self.assertEqual(topic_data["0"]["answers"], ['text'])
        self.assertEqual(topic_data["0"]["question"], "what is in document three")
        self.assertEqual(topic_data["1"]["answers"], ['contents'])
        self.assertEqual(topic_data["1"]["question"], "what is document two")

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()

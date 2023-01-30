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

import argparse
import math
import os
import time
from collections import defaultdict
from string import Template

import yaml

from defs_odqa import models, evaluate_dpr_retrieval_metric_definitions
from utils import run_dpr_retrieval_eval_and_return_metric, convert_trec_run_to_dpr_retrieval_json, run_fusion, ok_str, fail_str

GARRRF_LS = ['answers','titles','sentences']
HITS_1K = set(['GarT5-RRF', 'DPR-DKRR', 'DPR-Hybrid'])

def print_results(metric, topics):
    print(f'Metric = {metric}, Topics = {topics}')
    for model in models['models']:
        print(' ' * 32, end='')
        print(f'{model:30}', end='')
        key = f'{model}'
        print(f'{table[key][metric]:7.2f}', end='\n')
    print('')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate regression matrix for GarDKRR')
    parser.add_argument('--skip-eval', action='store_true',
                        default=False, help='Skip running trec_eval.')
    parser.add_argument('--topics', choices=['tqa', 'nq'],
                        help='Topics to be run [tqa, nq]', required=True)
    parser.add_argument('--full-topk', action='store_true',
                        default=False, help='Run topk 5-1000, default is topk 5-100')
    args = parser.parse_args()
    hits = 1000 if args.full_topk else 100
    yaml_path = 'pyserini/resources/triviaqa.yaml' if args.topics == "tqa" else 'pyserini/resources/naturalquestion.yaml'
    topics = 'dpr-trivia-test' if args.topics == 'tqa' else 'nq-test'
    start = time.time()
    table = defaultdict(lambda: defaultdict(lambda: 0.0))

    with open(yaml_path) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['model_name']
            cmd_template = condition['command']

            if not args.full_topk:
                # if using topk100
                if name in HITS_1K:
                    # if running topk1000 is a must to ensure scores match with the ones in the table
                    hits = 1000
                else:
                    hits = 100

            print(f'model {name}:')
            if topics == 'nq-test' and name == 'BM25-k1_0.9_b_0.4_dpr-topics':
                topics = 'dpr-nq-test'
            elif args.topics == 'nq':
                topics = 'nq-test'
            print(f'  - Topics: {topics}')

            # running retrieval
            if name == "GarT5-RRF":
                runfile = [f'runs/run.odqa.{name}.{topics}.{i}.hits-{hits}.txt' for i in GARRRF_LS]
            else:
                runfile = [f'runs/run.odqa.{name}.{topics}.hits-{hits}.txt']

            if name != "GarT5RRF-DKRR-RRF":
                cmd = [Template(cmd_template[i]).substitute(output=runfile[i]) for i in range(len(runfile))]
                if hits == 100:
                    cmd = [i + ' --hits 100' for i in cmd]
                for i in range(len(runfile)):
                    if not os.path.exists(runfile[i]):
                        print(f'    Running: {cmd[i]}')
                        os.system(cmd[i])

            # fusion
            if 'RRF' in name:
                runs = []
                output = ''
                if name == 'GarT5-RRF':
                    runs = runfile
                    output = f'runs/run.odqa.{name}.{topics}.hits-{hits}.fusion.txt'
                elif name == 'GarT5RRF-DKRR-RRF':
                    runs = [f'runs/run.odqa.DPR-DKRR.{topics}.hits-1000.txt', f'runs/run.odqa.GarT5-RRF.{topics}.hits-1000.fusion.txt']
                    output = runfile[0].replace('.txt','.fusion.txt')
                else:
                    raise NameError('Unexpected model name')
                if not os.path.exists(output):
                    if not args.full_topk and name != 'GarT5-RRF':
                        # if using topk100, we change it back for methods that require topk1000 to generate runs
                        hits = 100
                    status = run_fusion(runs, output, hits)
                    if status != 0:
                        raise RuntimeError('fusion failed')
                runfile = [output]


            # trec conversion + evaluation
            if not args.skip_eval:
                jsonfile = runfile[0].replace('.txt', '.json')
                runfile = jsonfile.replace('.json','.txt')
                if not os.path.exists(jsonfile):
                    status = convert_trec_run_to_dpr_retrieval_json(
                        topics, 'wikipedia-dpr', runfile, jsonfile)
                    if status != 0:
                        raise RuntimeError("dpr retrieval convertion failed")
                topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-100']
                if args.full_topk:
                    topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-1000']
                score = run_dpr_retrieval_eval_and_return_metric(topk_defs, jsonfile)
            
            # comparing ground truth scores with the generated ones 
            for expected in condition['scores']:
                for metric, expected_score in expected.items():
                    if metric not in score.keys(): continue
                    if not args.skip_eval:
                        if math.isclose(score[metric], float(expected_score),abs_tol=2e-2):
                            result_str = ok_str
                        else:
                            result_str = fail_str + \
                                f' expected {expected[metric]:.4f}'
                        print(f'      {metric:7}: {score[metric]:.2f} {result_str}')
                        table[name][metric] = score[metric]
                    else:
                        table[name][metric] = expected_score

            print('')
    metric_ls = ['Top5', 'Top20', 'Top100', 'Top500', 'Top1000']
    metric_ls = metric_ls[:3] if not args.full_topk else metric_ls
    for metric in metric_ls:
        print_results(metric, topics)

    end = time.time()
    print(f'Total elapsed time: {end - start:.0f}s')

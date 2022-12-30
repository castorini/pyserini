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

from scripts.repro_matrix.defs_odqa import models, evaluate_dpr_retrieval_metric_definitions
from scripts.repro_matrix.utils import run_dpr_retrieval_eval_and_return_metric, convert_trec_run_to_dpr_retrieval_json, ok_str, fail_str


def print_results(metric, topics):
    print(f'Metric = {metric}, Topics = {topics}')
    for model in models['models']:
        print(' ' * 32, end='')
        print(f'{model:30}', end='')
        key = f'{model}'
        print(f'{table[key][topics][metric]:7.3f}', end='\n')
    print('')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate regression matrix for GarDKRR')
    parser.add_argument('--skip-eval', action='store_true',
                        default=False, help='Skip running trec_eval.')
    parser.add_argument('--topics', choices=['triviaqa', 'naturalquestion'],
                        help='Topics to be run [triviaqa, naturalquestion]', required=True)
    parser.add_argument('--full-topk', action='store_true',
                        default=False, help='Run topk 5-1000, default is topk 5-100')
    args = parser.parse_args()
    hits = 1000 if args.full_topk else 100
    yaml_path = 'pyserini/resources/triviaqa.yaml' if args.topics == "triviaqa" else 'pyserini/resources/naturalquestion.yaml'
    topics = 'dpr-trivia-test' if args.topics == 'triviaqa' else 'nq-test'
    start = time.time()
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(yaml_path) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['model_name']
            cmd_template = condition['command']

            print(f'model {name}:')
            print(f'  - Topics: {topics}')

            runfile = f'runs/run.odqa.{name}.{topics}.hits={hits}.txt'
            cmd = Template(cmd_template).substitute(output=runfile)
            if not args.full_topk:
                cmd += ' --hits 100'
            if not os.path.exists(runfile):
                print(f'    Running: {cmd}')
                os.system(cmd)

            # evaluation
            if not args.skip_eval:
                jsonfile = runfile.replace('.txt', '.json')
                if not os.path.exists(jsonfile):
                    status = convert_trec_run_to_dpr_retrieval_json(
                        topics, 'wikipedia-dpr', runfile, jsonfile)
                    if status != 0:
                        raise RuntimeError("dpr retrieval convertion failed")
                topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-100']
                if args.full_topk:
                    topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-1000']
                score = run_dpr_retrieval_eval_and_return_metric(topk_defs, jsonfile)
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
                        table[name][topics][metric] = score[metric]
                    else:
                        table[name][topics][metric] = expected_score

            print('')
    metric_ls = ['Top5', 'Top20', 'Top100', 'Top500', 'Top1000']
    metric_ls = metric_ls[:3] if not args.full_topk else metric_ls
    for metric in metric_ls:
        print_results(metric, topics)

    end = time.time()
    print(f'Total elapsed time: {end - start:.0f}s')

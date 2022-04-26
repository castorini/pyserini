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
import math
import os
import subprocess
import yaml

collection = 'msmarco-v1-passage'

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'msmarco-passage-dev-subset' : {
        'MRR@10': '-c -M 10 -m recip_rank',
        'R@1K': '-c -m recall.1000'
    },
    'dl19-passage': {
        'MAP': '-c -l 2 -m map',
        'nDCG@10': '-c -m ndcg_cut.10',
        'R@1K': '-c -l 2 -m recall.1000'
    },
    'dl20-passage': {
        'MAP': '-c -l 2 -m map',
        'nDCG@10': '-c -m ndcg_cut.10',
        'R@1K': '-c -l 2 -m recall.1000'
    }
}


def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    return stdout, stderr


def run_eval_and_return_metric(metric, eval_key, runfile):
    eval_cmd = f'python -m pyserini.eval.trec_eval {trec_eval_metric_definitions[eval_key][metric]} {eval_key} runs/{runfile}'
    #print(eval_cmd)
    eval_stdout, eval_stderr = run_command(eval_cmd)

    # TODO: This is very brittle... fix me later.
    return eval_stdout.split('\n')[-3].split('\t')[2]


with open('pyserini/resources/msmarco-v1-passage.yaml') as f:
    yaml_data = yaml.safe_load(f)
    for condition in yaml_data['conditions']:
        name = condition['name']
        display = condition['display']
        cmd_template = condition['command']

        print(f'# Running condition "{name}": {display}\n')

        #print(condition)
        for topic_set in condition['topics']:
            topic_key = topic_set['topic_key']
            eval_key = topic_set['eval_key']

            print(f'  - topic_key: {topic_key}')

            runfile = f'run.{collection}.{topic_key}.{name}.txt'
            cmd = cmd_template.replace('_R_', f'runs/{runfile}').replace('_T_', topic_key)

            if not os.path.exists(f'runs/{runfile}'):
                print(f'    Running: {cmd}')
                os.system(cmd)

            print('')
            for expected in topic_set['scores']:
                for metric in expected:
                    score = float(run_eval_and_return_metric(metric, eval_key, runfile))
                    #print(expected[metric])
                    result = ok_str if math.isclose(score, float(expected[metric])) else fail_str + f' expected {expected[metric]:.4f}'
                    print(f'    {metric:7}: {score:.4f} {result}')

            print('')

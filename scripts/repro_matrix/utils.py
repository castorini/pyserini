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

import subprocess
import os

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK]'
okish_str = '\033[94m[OKish]\033[0m'


def find_msmarco_table_topic_set_key_v1(topic_key):
    # E.g., we want to map variants like 'dl19-passage-unicoil' and 'dl19-passage' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'dev'

    return key


def find_msmarco_table_topic_set_key_v2(topic_key):
    key = ''
    if topic_key.endswith('dev') or topic_key.endswith('dev-unicoil') or topic_key.endswith('dev-unicoil-noexp'):
        key = 'dev'
    elif topic_key.endswith('dev2') or topic_key.endswith('dev2-unicoil') or topic_key.endswith('dev2-unicoil-noexp'):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'

    return key


def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    return stdout, stderr


def run_eval_and_return_metric(metric, eval_key, defs, runfile):
    eval_cmd = f'python -m pyserini.eval.trec_eval {defs} {eval_key} {runfile}'
    eval_stdout, eval_stderr = run_command(eval_cmd)

    for line in eval_stdout.split('\n'):
        parts = line.split('\t')
        if len(parts) == 3 and parts[1] == 'all':
            return round(float(parts[2]), 4)

    return 0.0

def run_dpr_retrieval_eval_and_return_metric(defs, json_file):
    """Generate dpr retrieval evaluation scores

    Args:
        defs: topk definitions (e.g., '--topk 5 20')
        json_file: dpr retrieval json file

    Returns:
        topk: a dictionary of topk scores (e.g., {"Top5": <score>})
    """    
    eval_cmd = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {json_file} {defs} '
    eval_stdout, eval_stderr = run_command(eval_cmd)
    topk = {}
    for line in eval_stdout.split('\n'):
        parts = line.split('\t')
        if len(parts) == 2 and 'accuracy' in parts[1]:
            topk.update({parts[0]:round(float(parts[1][10:])*100, 4)})
    return topk


def convert_trec_run_to_dpr_retrieval_json(topics,index,runfile,output):
    """Convert trec runfile to dpr retrieval json file

    Args:
        topics: topics field
        index: index field 
        runfile: input runfile
        output: output jsonfile

    Returns:
        dummy value: 0.0
    """    
    cmd = f"python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics {topics} --index {index} --input {runfile} --output {output}"
    os.system(cmd)
    return 0.0


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
import subprocess

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK]'
okish_str = '\033[94m[OKish]\033[0m'


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
        exit status: exit status
    """
    cmd = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics {topics} --index {index} --input {runfile} --output {output}'
    return os.system(cmd)


def run_fusion(run_ls, output, k):
    """run fusion command and return status code

    Args:
        run_ls: a list of runfile paths
        output: output path
        k: topk value

    Returns:
        status code: status code
    """
    run_files = ' '.join(run_ls)
    cmd = f'python -m pyserini.fusion --runs {run_files} --output {output} --k {k}'
    return os.system(cmd)

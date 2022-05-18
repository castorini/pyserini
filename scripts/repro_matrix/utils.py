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


def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    return stdout, stderr


def run_eval_and_return_metric(metric, eval_key, defs, runfile):
    eval_cmd = f'python -m pyserini.eval.trec_eval {defs[eval_key][metric]} {eval_key} runs/{runfile}'
    eval_stdout, eval_stderr = run_command(eval_cmd)

    for line in eval_stdout.split('\n'):
        parts = line.split('\t')
        if len(parts) == 3 and parts[1] == 'all':
            return round(float(parts[2]), 4)

    return 0.0

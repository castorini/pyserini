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
import sys
import platform

from pyserini.search import get_qrels_file
from pyserini.util import download_evaluation_script

script_path = download_evaluation_script('msmarco_doc_eval')
cmd_prefix = ['python', script_path]
args = sys.argv
if len(args) > 1:
    cmd = cmd_prefix + args[1:]
    for i in range(len(cmd)-1):
        if cmd[i] == '--judgments':
            if not os.path.exists(cmd[i+1]):
                cmd[i+1] = get_qrels_file(cmd[i + 1])
else:
    cmd = cmd_prefix
print(f'Running command: {cmd}')
shell = platform.system() == "Windows"
process = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=shell)
stdout, stderr = process.communicate()
if stderr:
    print(stderr.decode("utf-8"))
print('Results:')
print(stdout.decode("utf-8"))

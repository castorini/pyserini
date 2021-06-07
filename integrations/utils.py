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


def clean_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def run_command(cmd):
    process = subprocess.Popen(cmd.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr:
        print(stderr)
    print(stdout)
    return stdout, stderr


def parse_score(output, metric, digits=4):
    for line in output.split('\n')[::-1]:
        if metric in line:
            score = float(line.split()[-1])
            return round(score, digits)
    return None

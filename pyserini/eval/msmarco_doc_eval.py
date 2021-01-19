import os
import subprocess
import sys

from pyserini.search import get_qrels
from pyserini.util import download_evaluation_script

script_path = download_evaluation_script('msmarco_doc_eval')
cmd_prefix = ['python3', script_path]
args = sys.argv
if len(args) > 1:
    cmd = cmd_prefix + args[1:]
    for i in range(len(cmd)-1):
        if cmd[i] == '--judgments':
            if not os.path.exists(cmd[i+1]):
                cmd[i+1] = get_qrels(cmd[i+1])
else:
    cmd = cmd_prefix
print(f'Running command: {cmd}')
process = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if stderr:
    print('Results:')
    print(stderr.decode("utf-8"))
else:
    print(stdout.decode("utf-8"))

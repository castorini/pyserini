import os
import subprocess
import sys
import platform

from pyserini.search import get_qrels_file
from pyserini.util import download_evaluation_script

script_path = download_evaluation_script('msmarco_passage_eval')
cmd_prefix = ['python', script_path]
args = sys.argv
if len(args) > 1:
    cmd = cmd_prefix + args[1:]
    if not os.path.exists(cmd[-2]):
        cmd[-2] = get_qrels_file(cmd[-2])
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

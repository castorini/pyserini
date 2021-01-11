import argparse
import subprocess
from pyserini.util import download_evaluation_script

parser = argparse.ArgumentParser(description='Evaluate trec runs.')
parser.add_argument('--qrel', type=str, required=True, help="Path to qrel file")
parser.add_argument('--run', type=str, required=True, help="Path to run file")
parser.add_argument('--metrics', type=str, nargs='+', required=True, help="metrics to evaluate")
args = parser.parse_args()

script_path = download_evaluation_script('trec_eval')
cmd_prefix = ['java', '-jar', script_path]
metrics = []
for metric in args.metrics:
    metrics += ['-m', metric]
cmd_suffix = [args.qrel, args.run]
cmd = cmd_prefix + metrics + cmd_suffix
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

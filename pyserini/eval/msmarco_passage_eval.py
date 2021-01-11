import argparse
import subprocess
from pyserini.util import download_evaluation_script

parser = argparse.ArgumentParser(description='Evaluate msmarco passage runs.')
parser.add_argument('--qrel', type=str, required=True, help="Path to qrel file")
parser.add_argument('--run', type=str, required=True, help="Path to run file")
args = parser.parse_args()

script_path = download_evaluation_script('msmarco_passage_eval')
cmd = ['python3', script_path, args.qrel, args.run]
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
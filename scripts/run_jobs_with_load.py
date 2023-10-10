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

import argparse
import logging
import os
import subprocess
import time

logger = logging.getLogger('run_jobs_with_load')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s  [python] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")


def count_jobs_running(jobs):
    out = run_command('ps -ax')

    cnt = 0
    for job in lines:
        parts = job.split('>')
        if parts[0].rstrip().lstrip() in out:
            cnt += 1

    return cnt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run jobs in parallel while maintaining a target load threshold.')
    parser.add_argument('--file', type=str, default=None, help="File with commands.")
    parser.add_argument('--sleep', type=int, default=30, help="Sleep between.")
    parser.add_argument('--load', type=int, default=10, help="Target load.")
    parser.add_argument('--max-concurrent', type=int, default=2, help="Maximum number of concurrent jobs.")
    args = parser.parse_args()

    logger.info(f'Running commands in {args.file}')
    logger.info(f'Sleep interval: {args.sleep}')
    logger.info(f'Threshold load: {args.load}')

    with open(args.file) as f:
        lines = f.read().splitlines()

    for r in lines:
        if not r or r.startswith('#'):
            continue

        logger.info(f'Launching: {r}')
        os.system(r + ' &')

        while True:
            time.sleep(args.sleep)
            load = os.getloadavg()[0]
            jobs = count_jobs_running(lines)
            logger.info(f'Current status: {jobs} jobs, {load:.1f} load (threshold = {args.load}, max-concurrent = {args.max_concurrent})')
            if load < args.load and jobs < args.max_concurrent:
                break

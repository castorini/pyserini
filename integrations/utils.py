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
import shutil
import subprocess


def clean_files(files):
    for file in files:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)


def run_command(cmd, echo=False):
    process = subprocess.Popen(cmd.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr and echo:
        print(stderr)
    if echo:
        print(stdout)
    return stdout, stderr


def parse_score(output, metric, digits=4):
    """Function for parsing the output from `pyserini.eval.trec_eval`."""
    lines = output.split('\n')

    for line in lines:
        if metric in line:
            score = float(line.split()[-1])
            return round(score, digits)
    return None


def parse_score_qa(output, metric, digits=4):
    """Function for parsing the output from `pyserini.eval.evaluate_dpr_retrieval`. Currently, the implementation is
       the same as `parse_score_msmarco`, but we're keeping separate in case they diverge in the future."""
    for line in output.split('\n'):
        if metric in line:
            score = float(line.split()[-1])
            return round(score, digits)
    return None


def parse_score_msmarco(output, metric, digits=4):
    """Function for parsing the output from MS MARCO eval scripts. Currently, the implementation is the same as
       `parse_score_qa`, but we're keeping separate in case they diverge in the future."""
    for line in output.split('\n'):
        if metric in line:
            score = float(line.split()[-1])
            return round(score, digits)
    return None


def parse_score_msmarco_as_string(output, metric):
    """Function for parsing the output from MS MARCO eval scripts, but returning result as a string. This is used for
       checking results to the entire degree of precision that the script generates."""
    for line in output.split('\n'):
        if metric in line:
            return line.split()[-1]
    return None


def run_retrieval_and_return_scores(output_file, retrieval_cmd, qrels, eval_type, metrics):
    temp_files = [output_file]

    # Take the base retrieval command and append the output file name to it.
    os.system(retrieval_cmd + f' --output {output_file}')

    scores = {}
    # How we compute eval metrics depends on the `eval_type`.
    if eval_type == 'trec_eval':
        for metric in metrics:
            cmd = f'python -m pyserini.eval.trec_eval -m {metric[0]} {qrels} {output_file}'
            stdout, stderr = run_command(cmd)
            scores[metric[0]] = parse_score(stdout, metric[1])
    elif eval_type == 'msmarco_passage':
        cmd = f'python -m pyserini.eval.msmarco_passage_eval {qrels} {output_file}'
        stdout, stderr = run_command(cmd)
        scores['MRR@10'] = parse_score_msmarco(stdout, 'MRR @10')
    elif eval_type == 'msmarco_passage_string':
        cmd = f'python -m pyserini.eval.msmarco_passage_eval {qrels} {output_file}'
        stdout, stderr = run_command(cmd)
        scores['MRR@10'] = parse_score_msmarco_as_string(stdout, 'MRR @10')
    elif eval_type == 'msmarco_doc':
        cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments {qrels} --run {output_file}'
        stdout, stderr = run_command(cmd)
        scores['MRR@100'] = parse_score_msmarco(stdout, 'MRR @100')
    elif eval_type == 'msmarco_doc_string':
        cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments {qrels} --run {output_file}'
        stdout, stderr = run_command(cmd)
        scores['MRR@100'] = parse_score_msmarco_as_string(stdout, 'MRR @100')
    else:
        clean_files(temp_files)
        raise ValueError('Unknown eval_type!')

    clean_files(temp_files)

    return scores

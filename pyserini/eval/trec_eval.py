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

# Example usage:
# python -m pyserini.eval.trec_eval -c \
#   -m ndcg_cut.10 \
#   -m judged.5,10 beir-v1.0.0-arguana-test run.beir.contriever-msmarco.arguana.txt -remove-unjudged

# From Jimmy, Sept 2024 -
#
# This file has a load sequence that is very different from all the other files.
# The JVM by default in Pyserini is loaded with the option '--add-modules=jdk.incubator.vector', which triggers the
# following warning: 'WARNING: Using incubator modules: jdk.incubator.vector'
#
# I have looked extensively online and was not able to find a way to suppress that warning.
# The solution here is to start the JVM without the vector module, which isn't needed here.
# This explains the code sequence below.

import glob
import importlib.resources
import os
import platform
import subprocess
import sys
import tempfile
from typing import Any

import jnius_config
import pandas as pd

# Don't use the jdk.incubator.vector module.
jar_directory = str(importlib.resources.files("pyserini.resources.jars").joinpath(''))
jar_path = glob.glob(os.path.join(jar_directory, '*.jar'))[0]

try:
    jnius_config.add_classpath(jar_path)
except:
    # This might happen if the JVM's already been initialized. Just eat the error.
    pass

# This triggers loading of the JVM.
import jnius

# Now we can load qrels; this will trigger another attempt to reload the JVM, which won't happen because
# the JVM has already loaded.
from pyserini.search import get_qrels_file


def trec_eval(
    args, query_id=None, return_per_query_results=False
) -> float | dict[Any, float]:
    cmd_prefix = ['java', '-cp', jar_path, 'trec_eval']

    if return_per_query_results or query_id:
        assert '-q' in args, 'The "-q" is required for returning per query results.'

    # Option to discard non-judged hits in run file
    judged_docs_only = ''
    judged_result = []
    cutoffs = []

    if '-remove-unjudged' in args:
        judged_docs_only = args.pop(args.index('-remove-unjudged'))

    if any([i.startswith('judged.') for i in args]):
        # Find what position the arg is in.
        idx = [i.startswith('judged.') for i in args].index(True)
        cutoffs = args.pop(idx)
        cutoffs = list(map(int, cutoffs[7:].split(',')))
        # Get rid of the '-m' before the 'judged.xxx' option
        args.pop(idx - 1)

    temp_file = ''

    if len(args) > 1:
        if not os.path.exists(args[-2]):
            args[-2] = get_qrels_file(args[-2])
        if os.path.exists(args[-1]):
            # Convert run to trec if it's on msmarco
            with open(args[-1]) as f:
                first_line = f.readline()
            if 'Q0' not in first_line:
                temp_file = tempfile.NamedTemporaryFile(delete=False).name
                print('msmarco run detected. Converting to trec...')
                run = pd.read_csv(args[-1], sep=r'\s+', header=None, names=['query_id', 'doc_id', 'rank'])
                run['score'] = 1 / run['rank']
                run.insert(1, 'Q0', 'Q0')
                run['name'] = 'TEMPRUN'
                run.to_csv(temp_file, sep='\t', header=None, index=None)
                args[-1] = temp_file

        if not os.path.exists(args[-1]):
            print(f"The run file {args[-1]} does not exist!")
            sys.exit()
        run = pd.read_csv(args[-1], sep=r'\s+', engine='python', header=None)
        qrels = pd.read_csv(args[-2], sep=r'\s+', engine='python', header=None)

        # cast doc_id column as string
        run[0] = run[0].astype(str)
        qrels[0] = qrels[0].astype(str)

        # Discard non-judged hits
        if judged_docs_only:
            if not temp_file:
                temp_file = tempfile.NamedTemporaryFile(delete=False).name
            judged_indexes = pd.merge(run[[0, 2]].reset_index(), qrels[[0, 2]], on=[0, 2])['index']
            run = run.loc[judged_indexes]
            run.to_csv(temp_file, sep='\t', header=None, index=None)
            args[-1] = temp_file
        # Measure judged@cutoffs
        for cutoff in cutoffs:
            run_cutoff = run.groupby(0).head(cutoff)
            judged = len(pd.merge(run_cutoff[[0, 2]], qrels[[0, 2]], on=[0, 2])) / len(run_cutoff)
            metric_name = f'judged_{cutoff}'
            judged_result.append(f'{metric_name:22}\tall\t{judged:.4f}')
        cmd = cmd_prefix + args[1:]
    else:
        cmd = cmd_prefix

    # We're going to shell out to call trec_eval.
    # Obvious question here: why we *not* just call the trec_eval main (Java) class, which already wraps the executable?
    # in Java (which wraps the binaries). The answer is that the Java class explicitly calls System.exit, so we wouldn't
    # be able to do cleanup here in Python.
    shell = platform.system() == "Windows"
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
    )
    stdout, stderr = process.communicate()
    if stderr:
        print(stderr.decode("utf-8"))

    output = stdout.decode("utf-8").rstrip()
    print(output)

    for judged in judged_result:
        print(judged)

    if temp_file:
        os.remove(temp_file)

    output = output.split("\n")
    lines = {line.split("\t")[1]: float(line.split("\t")[2]) for line in output}
    if return_per_query_results:
        return lines

    if query_id:
        return lines[query_id]
    else:
        return lines["all"]


if __name__ == "__main__":
    trec_eval(sys.argv)

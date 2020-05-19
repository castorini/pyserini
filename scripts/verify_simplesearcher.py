# -*- coding: utf-8 -*-
#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import argparse
import filecmp
import os


class Group:
    def __init__(self, run_name: str, index_path: str, topics_path: str):
        self.run_name = run_name
        self.index_path = index_path
        self.topics_path = topics_path
        self.anserini_output = f'verify.anserini.{run_name}.txt'
        self.pyserini_output = f'verify.pyserini.{run_name}.txt'


def remove_output_if_exist(group: Group):
    for path in [group.anserini_output, group.pyserini_output]:
        if os.path.exists(path):
            os.remove(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Verify search results between pyserini and anserini')
    parser.add_argument('--anserini', metavar='path', required=True,
                        help='the path to anserini root')
    args = parser.parse_args()

    # config
    anserini_root = args.anserini
    indexes_root = os.path.join(anserini_root, 'indexes')
    anserini_search = os.path.join(
        anserini_root, 'target/appassembler/bin/SearchCollection -topicreader Trec -bm25')
    pyserini_search = 'python -m pyserini.search'

    # set groups
    robust04 = Group(
        run_name='robust04',
        index_path=os.path.join(
            indexes_root, 'lucene-index.robust04.pos+docvectors+raw'),
        topics_path=os.path.join(
            anserini_root, 'src/main/resources/topics-and-qrels/topics.robust04.txt')
    )

    robust05 = Group(
        run_name='robust05',
        index_path=os.path.join(
            indexes_root, 'lucene-index.robust05.pos+docvectors+raw'),
        topics_path=os.path.join(
            anserini_root, 'src/main/resources/topics-and-qrels/topics.robust05.txt')
    )

    core17 = Group(
        run_name='core17',
        index_path=os.path.join(
            indexes_root, 'lucene-index.core17.pos+docvectors+raw'),
        topics_path=os.path.join(
            anserini_root, 'src/main/resources/topics-and-qrels/topics.core17.txt')
    )

    core18 = Group(
        run_name='core18',
        index_path=os.path.join(
            indexes_root, 'lucene-index.core18.pos+docvectors+raw'),
        topics_path=os.path.join(
            anserini_root, 'src/main/resources/topics-and-qrels/topics.core18.txt')
    )

    groups = [robust04, robust05, core17, core18]
    success, failed = [], []
    # execution
    for group in groups:
        print(f'Running {group.run_name}:')
        remove_output_if_exist(group)
        anserini_cmd = f'{anserini_search} -index {group.index_path} -topics {group.topics_path} -output {group.anserini_output}'
        pyserini_cmd = f'{pyserini_search} -index {group.index_path} -topics {group.topics_path} -output {group.pyserini_output}'

        res = os.system(anserini_cmd)
        if res == 0:
            print(f'[{group.run_name}] anserini search successful')
        else:
            print(f'[{group.run_name}] anserini search successful')

        res = os.system(pyserini_cmd)
        if res == 0:
            print(f'[{group.run_name}] pyserini search successful')
        else:
            print(f'[{group.run_name}] pyserini search successful')

        res = filecmp.cmp(group.anserini_output, group.pyserini_output)
        if res is True:
            print(f'[{group.run_name}] result matches')
            success.append(group.run_name)
            remove_output_if_exist(group)
        else:
            failed.append(group.run_name)
            print(
                f'[{group.run_name}] result mismatch. {group.anserini_output} != {group.pyserini_output}')

        print('-------------------------')
        print()

    print(f'[Success] {len(success)}/{len(groups)}')
    if len(failed) > 0:
        for failed_run in failed:
            print(f'[{failed_run}] result mismatch')

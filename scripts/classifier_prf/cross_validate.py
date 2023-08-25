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
import json
import os
import pandas as pd


def get_file_extension(rm3: bool):
    return '_bm25+rm3.txt' if rm3 is True else '_bm25.txt'


def get_file_path(run_file, collection, classifier, alpha: str, rm3: bool):
    res = f'{run_file}/{collection}/{collection}_{classifier}_A{alpha}'
    return res + get_file_extension(rm3)


def get_res_file_path(run_file, collection, classifier, alpha: str, rm3: bool):
    res = f'{run_file}/scripts/classifier_prf/cv/{collection}/{collection}_{classifier}_A' + alpha
    return res + get_file_extension(rm3)


def get_trec_eval_cmd(anserini_root: str):
    return os.path.join(anserini_root, 'tools/eval/trec_eval.9.0.4/trec_eval')


def get_qrels_path(anserini_root: str, collection: str):
    return f"{anserini_root}/tools/topics-and-qrels/qrels.{collection}.txt"


def read_topics_alpha_map(anserini_root, collection, run_file, classifier, rm3: bool):
    res_paths = []

    for num in range(0, 11):
        alpha = str(num / 10)
        file_path = get_file_path(run_file, collection, classifier, alpha, rm3)
        cv_folder_path = os.path.join(
            run_file, f"scripts/classifier_prf/cv/{collection}")
        os.system(f"mkdir -p {cv_folder_path}")
        res_filename = get_res_file_path(
            run_file, collection, classifier, alpha, rm3)

        res_paths.append(res_filename)
        trec_eval_cmd = get_trec_eval_cmd(anserini_root)
        qrels_path = get_qrels_path(anserini_root, collection)
        cmd = f'{trec_eval_cmd} -q -m map -m P.30 {qrels_path} {file_path} > {res_filename}'
        res = os.system(cmd)
        if res == 0:
            print(file_path + ' run successfully!')
            print('save result in ' + res_filename)

    return res_paths


def load_in_res(res_paths):
    df = pd.read_csv(
        res_paths[0], sep='\s+', header=None,
        names=['Type', 'topicid', '0.0'], dtype={'0.0': float})
    df.set_index('topicid', inplace=True)

    for num in range(1, 11):
        dataset = pd.read_csv(
            res_paths[num], sep='\s+', header=None, names=['Type', 'topicid', 'score'],
            dtype={'topicid': str, 'score': float})
        df[str(num / 10)] = dataset.score.values

    df = df[df['Type'] == 'map'][:-1]
    df = df.drop(['Type'], axis=1)
    return df


def generate_run_file(folders, df, collection, run_file, classifier, rm3, output_path):
    highest_alpha_lst, write_lst = [], []

    with open(output_path, 'w') as target_file:
        for folder in folders:
            train_topicids = [str(topic)
                              for f in folders for topic in f if f != folder and str(topic) in df.index]
            train_df = df.loc[train_topicids, :]
            train_df.loc['Mean', :] = train_df.mean(axis=0)
            highest_alpha = train_df.iloc[-1, :].idxmax(axis=0)
            highest_alpha_lst.append(highest_alpha)

            for topic in folder:
                alpha_run_file = get_file_path(
                    run_file, collection, classifier, highest_alpha, rm3)

                with open(alpha_run_file) as fp:
                    Lines = fp.readlines()
                    for line in Lines:
                        if line.startswith(str(topic)):
                            write_lst.append(line)

        write_lst.sort(key=lambda x: (x.split(" ")[0], int(x.split(" ")[3])))
        target_file.write("".join(write_lst))

    print(highest_alpha_lst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get Best alpha score for corresponding topics')
    parser.add_argument('--anserini', metavar='path', required=True,
                        help='the path to anserini root')
    parser.add_argument('--pyserini', metavar='path', required=True,
                        help='a path to the folder json file')
    parser.add_argument('--collection', metavar='collectionsname', required=True,
                        help='one of the collectionname in robust04,robust05, core17,core18')
    parser.add_argument('--run_file', metavar='path', required=True,
                        help='the path to run files root')
    parser.add_argument('--output', metavar='path', required=True,
                        help='the path to the output file')
    parser.add_argument('--classifier', metavar='name', required=True,
                        help='one of three classifers lr or svm or lr+svm')
    parser.add_argument('-rm3', action='store_true',
                        help='use rm3 ranker')

    args = parser.parse_args()

    res_paths = read_topics_alpha_map(
        args.anserini, args.collection, args.run_file, args.classifier, args.rm3)
    clean_df = load_in_res(res_paths)
    folders_path = os.path.join(
        args.pyserini, f'scripts/classifier_prf/folds/{args.collection}.json')

    with open(folders_path) as f:
        folders = json.load(f)

    generate_run_file(folders, clean_df, args.collection,
                      args.run_file, args.classifier, args.rm3, args.output)

    print("Successfully generated a trained runfile in " + args.output)

import pandas as pd
import json
import os
import argparse


def read_topics_alpha_map(anserini_root, collection, run_file, classifier, rm3):
    res_paths = []
    for num in range(0, 11):
        alpha = str(num / 10)
        if rm3:
            file_path = f'{run_file}/{collection}/{collection}_{classifier}_A' + alpha + '_bm25+rm3.txt'
        else:
            file_path = f'{run_file}/{collection}/{collection}_{classifier}_A' + alpha + '_bm25.txt'
        res_filename = f'{run_file}/cv/{collection}/scores_{collection}_{classifier}_A' + alpha + '_bm25.txt'
        res_paths.append(res_filename)
        cmd = f'{anserini_root}/eval/trec_eval.9.0.4/trec_eval -q -m map -m P.30 {anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt {file_path} > {res_filename}'
        res = os.system(cmd)
        if (res == 0):
            print(file_path + ' run successfully!')
            print('save result in ' + res_filename)
    return res_paths


def load_in_res(res_paths):
    df = pd.read_csv(res_paths[0], sep='\s+', header=None, names=['Type', 'topicid', '0.0'], dtype={'0.0': float})
    df.set_index('topicid', inplace=True)
    for num in range(1, 11):
        dataset = pd.read_csv(res_paths[num], sep='\s+', header=None, names=['Type', 'topicid', 'score'],
                              dtype={'topicid': str, 'score': float})
        df[str(num / 10)] = dataset.score.values
    df = df[df['Type'] == 'map'][:-1]
    df = df.drop(['Type'], axis=1)
    return df


def generate_run_file(folders,df,collection, run_file, classifier, rm3, output_path):
    highest_alpha_lst = []
    write_lst = []
    with open(output_path, 'w') as target_file:
        for folder in folders:
            train_topicids = [str(topic) for folder_i in folders for topic in folder_i if folder_i != folder]
            train_df = df.loc[train_topicids, :]
            train_df.loc['Mean', :] = train_df.mean(axis=0)
            highest_alpha = train_df.iloc[-1, :].idxmax(axis=1)
            highest_alpha_lst.append(highest_alpha)
            for topic in folder:
                if rm3:
                    alpha_run_file = f'{run_file}/{collection}/{collection}_{classifier}_A' + highest_alpha + '_bm25.txt'
                else:
                    alpha_run_file = f'{run_file}/{collection}/{collection}_{classifier}_A' + highest_alpha + '_bm25+rm3.txt'
                with open(alpha_run_file) as fp:
                    Lines = fp.readlines()
                    for line in Lines:
                        # if topic ==321:
                        #     print(line,topic,line.startswith(str(topic)))
                        if line.startswith(str(topic)):
                            write_lst.append(line)
        write_lst.sort(key=lambda x: (x.split(" ")[0],int(x.split(" ")[3])))
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
    res_paths = read_topics_alpha_map(args.anserini, args.collection, args.run_file, args.classifier, args.rm3)
    clean_df = load_in_res(res_paths)
    folders_path = os.path.join(
            args.pyserini, f'scripts/classifier_prf/folds/{args.collection}.json')
    print(folders_path)
    with open(folders_path) as f:
        folders = json.load(f)
    generate_run_file(folders,clean_df,args.collection, args.run_file, args.classifier, args.rm3, args.output)
    print("Successfully generated a trained runfile in " + args.output)

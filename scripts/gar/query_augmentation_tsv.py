from email.policy import default
import argparse
from random import choices
from datasets import load_dataset
import os

def def_args(parser):
    parser.add_argument('--data_split', type=str, choices=['validation','test'], default='test')
    parser.add_argument('--dataset',type=str, choices=['nq','trivia'],default='nq')
    parser.add_argument('--output_path', type=str,
                        default='./augmented_topics.tsv', help="output txt path")
    parser.add_argument('--k', type=int, default=1,
                        help="first k augmentations to be added to the query")
    parser.add_argument('--answers', action='store_true', default=False)
    parser.add_argument('--titles', action='store_true', default=False)
    parser.add_argument('--sentences', action='store_true', default=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query augmentations.')
    def_args(parser)
    args = parser.parse_args()
    final_list = []
    json_list = []
    anserini_path = os.environ['ANSERINI']
    data_path = ''
    if args.dataset == 'nq':
        if args.data_split == 'validation':
            data_path = os.path.join(anserini_path,'src/main/resources/topics-and-qrels/topics.nq.dev.txt')
        elif args.data_split == 'test':
            data_path = os.path.join(anserini_path,'src/main/resources/topics-and-qrels/topics.nq.test.txt')
    elif args.dataset == 'trivia':
        if args.data_split == 'validation':
            data_path = os.path.join(anserini_path,'src/main/resources/topics-and-qrels/topics.dpr.trivia.dev.txt')
        elif args.data_split == 'test':
            data_path = os.path.join(anserini_path,'src/main/resources/topics-and-qrels/topics.dpr.trivia.test.txt')
    
    dataset = 'castorini/triviaqa_gar-t5_expansions' if args.dataset == 'trivia' else 'castorini/nq_gar-t5_expansions'
    with open(data_path, 'r') as file:
        file = file.readlines()
        concatenated = list(map(lambda x: x.split('\t'), file))

    data_files = {"dev":"dev/dev.jsonl", "test": "test/test.jsonl"}
    json_list = load_dataset(dataset)[args.data_split]

    for i in range(len(json_list)):
        temp_list = []
        temp2_list = []
        temp_list.append(json_list[i]['id']+'\t')
        temp_list.append(concatenated[i][0] + ' ')

        if args.answers:
            temp2_list.append(
                ' '.join(json_list[i]['predicted_answers'][:args.k]))
        if args.titles:
            temp2_list.append(
                ' '.join(json_list[i]['predicted_titles'][:args.k]))
        if args.sentences:
            temp2_list.append(
                ' '.join(json_list[i]['predicted_sentences'][:args.k]))

        final_list.append(''.join(temp_list) + ' '.join(temp2_list)+'\n')

    with open(args.output_path, 'w') as output_file:
        output_file.writelines(final_list)
    print("Done")

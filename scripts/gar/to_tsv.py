from argparse import ArgumentParser

def convert_to_tsv(query_path,answer_path=None,title_path=None,sentence_path=None):
    queries = []
    answers = []
    titles = []
    sentences = []
    output = []
    with open(query_path,'r') as f:
        queries = f.readlines()

    if answer_path:
        with open(answer_path,'r') as f:
            answers = f.readlines()
    if title_path:
        with open(title_path,'r') as f:
            titles = f.readlines()
    if sentence_path:
        with open(sentence_path,'r') as f:
            sentences = f.readlines()

    max_len = len(queries)

    for i in range(max_len):
        temp_str = str(i)+'\t' + queries[i].replace('\n','')
        if answer_path:
            temp_str += answers[i].replace('\n','')
        if title_path:
            temp_str += titles[i].replace('\n','')
        if sentence_path:
            temp_str += sentences[i].replace('\n','')
        temp_str += '\n'
        output.append(temp_str)
    return output    
    
    
if __name__ == '__main__':
    parser = ArgumentParser("This script is to convert txt files for NQ or TQA to tsv file")
    parser.add_argument('--query_path',type=str,metavar='PATH')
    parser.add_argument('--answer_path', default='',type=str,metavar='PATH')
    parser.add_argument('--title_path', default='',type=str,metavar='PATH')
    parser.add_argument('--sentence_path', default='',type=str,metavar='PATH')
    parser.add_argument('--output_path',default='runs/out.tsv',type=str,metavar='PATH')
    args = parser.parse_args()
    output = convert_to_tsv(args.query_path,answer_path=args.answer_path,title_path=args.title_path,sentence_path=args.sentence_path)
    if output:
        with open(args.output_path,'w') as f:
            f.writelines(output)
        print("Done")
    else:
        print("please provide valid input")
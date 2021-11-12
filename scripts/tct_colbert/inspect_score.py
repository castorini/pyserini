import os
import fire
import torch
from transformers import AutoTokenizer


def main(query_file='query.txt', doc_file='doc.txt',
         score_file='scores.pt', tok_ckpt='distilbert-base-uncased'):
    with open(query_file, 'r') as fh:
        query = fh.read().rstrip()
    with open(doc_file, 'r') as fh:
        doc = fh.read().rstrip()

    tokenizer = AutoTokenizer.from_pretrained(tok_ckpt)
    qry_ids = tokenizer([query])['input_ids'][0][1:]
    doc_ids = tokenizer([doc])['input_ids'][0][1:]
    qry_tokens = [tokenizer.decode(x) for x in qry_ids]
    doc_tokens = [tokenizer.decode(x) for x in doc_ids]

    scores = torch.load(score_file)
    scores = scores.squeeze(0)[:len(doc_tokens) + 1, :]
    scores = scores.T
    max_loc = torch.argmax(scores, dim=1)

    print(qry_tokens)
    print(doc_tokens)
    print(max_loc)

    # emphasis on max q-d match
    #for i in range(len(qry_tokens)):
    #    scores[i][max_loc[i]] = 1.0

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.imshow(scores.numpy(), cmap='viridis', interpolation='nearest')
    plt.yticks(
        list([i for i in range(len(qry_tokens))]),
        list([tok for tok in qry_tokens])
    )
    plt.xticks(
        list([i for i in range(len(doc_tokens))]),
        list([tok for tok in doc_tokens]),
        rotation=90
    )
    wi, hi = fig.get_size_inches()
    plt.gcf().set_size_inches(wi * 2, hi * 2)
    #plt.colorbar()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    os.environ["PAGER"] = 'cat'
    fire.Fire(main)

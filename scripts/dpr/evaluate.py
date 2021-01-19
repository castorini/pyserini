import re
import string
import argparse
import json
import numpy as np


def normalize(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def has_answers(text, answers):
    text = normalize(text)
    for ans in answers:
        ans = normalize(ans)
        if ans in text:
            return True
    return False


parser = argparse.ArgumentParser()
parser.add_argument('--retrieval', type=str, metavar='path',
                    help="Path to retrieval output file.")
args = parser.parse_args()

retrieval = json.load(open(args.retrieval))
accuracy = []
for qid in retrieval:
    answers = retrieval[qid]['answers']
    contexts = retrieval[qid]['contexts']
    has_ans = 0
    for ctx in contexts:
        text = ctx['text']
        if has_answers(text, answers):
            has_ans = 1
    accuracy.append(has_ans)
print(np.mean(accuracy))

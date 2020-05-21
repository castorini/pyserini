import re
import argparse
import enum

from pyserini.search.pysearch import get_topics, SimpleSearcher
from ..vectorizer import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def get_prf_vectors(doc_ids, vectorizer, r=10, n=100):
    train_docs = doc_ids[:r] + doc_ids[-n:]
    train_labels = [1] * r + [0] * n

    train_vectors = vectorizer.get_vectors(train_docs)
    test_vectors = vectorizer.get_vectors(doc_ids)

    return train_vectors, train_labels, test_vectors


# sort both list in decreasing order by using the list1 to compare
def sort_dual_list(list1, list2):
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    list1, list2 = [list(tuple) for tuple in tuples]

    list1.reverse()
    list2.reverse()
    return list1, list2


def normalize(scores):
    low = min(scores)
    high = max(scores)
    width = high - low

    return [(s-low)/width for s in scores]


class ClassifierType(enum.Enum):
    LR = 'lr'
    SVM = 'svm'


def get_clasifier(type: ClassifierType):
    if type == ClassifierType.LR:
        return LogisticRegression()
    elif type == ClassifierType.SVM:
        return SVC(kernel='linear', probability=True)
    else:
        return None


parser = argparse.ArgumentParser(description='Create a input schema')
parser.add_argument('-index', metavar='path', required=True,
                    help='the path to workspace')
parser.add_argument('-topics', metavar='topicsname', required=True,
                    help='topicsname')
parser.add_argument('-output', metavar='path', required=True,
                    help='path to the output file')
parser.add_argument('-rm3',  action='store_true',
                    help='use rm3 ranker')
parser.add_argument('-qld',  action='store_true',
                    help='use qld ranker')
parser.add_argument('-prf',  type=ClassifierType,
                    help='use pseudo relevance feedback ranker')
parser.add_argument('-r',  type=int, default=10,
                    help='number of positive labels in pseudo relevance feedback')
parser.add_argument('-n',  type=int, default=100,
                    help='number of negative labels in pseudo relevance feedback')
parser.add_argument('-alpha',  type=float, default=0.5,
                    help='alpha value for interpolation in pseudo relevance feedback')
args = parser.parse_args()

searcher = SimpleSearcher(args.index)
topics_dic = get_topics(args.topics)

if topics_dic == {}:
    print('Topic Not Found')
    exit()

num_topics = len(topics_dic)
vectorizer = TfidfVectorizer(args.index, min_df=5) if args.prf else None
with open(args.output, 'w') as target_file:
    for index, topic in enumerate(sorted(topics_dic.keys())):
        print(f'Topic {topic}: {index + 1}/{num_topics}')
        search = topics_dic[topic].get('title')
        hits = searcher.search(search, 1000)
        doc_ids = [hit.docid.strip() for hit in hits]
        scores = [hit.score for hit in hits]

        if args.prf and args.alpha > 0 and len(hits) > (args.r + args.n):
            # vectorize
            train_vectors, train_labels, test_vectors = get_prf_vectors(
                doc_ids, vectorizer, r=args.r, n=args.n)

            # classification
            clf = get_clasifier(args.prf)
            clf.fit(train_vectors, train_labels)
            pred = clf.predict_proba(test_vectors)
            rank_scores = normalize([p[1] for p in pred])

            # interpolation
            search_scores = normalize([hit.score for hit in hits])
            interpolated_scores = [a * args.alpha + b * (1-args.alpha)
                                   for a, b in zip(rank_scores, search_scores)]
            scores, doc_ids = sort_dual_list(interpolated_scores, doc_ids)

        tag = f'{args.prf}-A{args.alpha}' if args.prf else 'Anserini'
        for i, (doc_id, score) in enumerate(zip(doc_ids, scores)):
            target_file.write(
                f'{topic} Q0 {doc_id} {i + 1} {score:.6f} {tag}\n')

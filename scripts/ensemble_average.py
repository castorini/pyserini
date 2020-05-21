import argparse
from typing import Dict, List, Set


def get_topics(path: str) -> Set[str]:
    topics = set()
    with open(path, 'r') as f:
        for line in f:
            topic = line.strip().split(' ')[0]
            topics.add(topic)

    return topics


def get_doc_id_dict(topic: str, path: str, res=None) -> Dict[str, List[float]]:
    if res is None:
        res = {}

    with open(path, 'r') as f:
        for line in f:
            tokens = line.strip().split(' ')
            line_topic = tokens[0]
            if topic != line_topic:
                continue

            doc_id = tokens[2]
            score = float(tokens[4])
            if doc_id not in res:
                res[doc_id] = []

            res[doc_id].append(score)

    return res


# sort both list in decreasing order by using the list1 to compare
def sort_dual_list(list1, list2):
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    list1, list2 = [list(tuple) for tuple in tuples]

    list1.reverse()
    list2.reverse()
    return list1, list2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform ensemble average on two Qrun files')
    parser.add_argument('-run1', type=str, required=True,
                        help='the path to the first qrun file')
    parser.add_argument('-run2', type=str, required=True,
                        help='the path to the second qrun file')
    parser.add_argument('-out', type=str, required=True,
                        help='the path to the final output file')
    args = parser.parse_args()

    # get topics
    topics = get_topics(args.run1)
    if topics != get_topics(args.run2):
        print('Topics mismatch')
        exit()

    topics = sorted(list(topics))
    with open(args.out, 'w+') as f:
        for index, topic in enumerate(topics):
            print(f'Topic {topic}: {index+1}/{len(topics)}')
            doc_id_score_dict = get_doc_id_dict(topic, args.run1)
            doc_id_score_dict = get_doc_id_dict(
                topic, args.run2, doc_id_score_dict)

            doc_ids, scores = [], []
            for doc_id, score in doc_id_score_dict.items():
                if len(score) != 2:
                    print(f"[Topic {topic}][id {doc_id}] should have exactly 2 scores")
                avg = sum(score) / len(score)
                scores.append(avg)
                doc_ids.append(doc_id)

            scores, doc_ids = sort_dual_list(scores, doc_ids)
            for i, (score, doc_id) in enumerate(zip(scores, doc_ids)):
                f.write(f"{topic} Q0 {doc_id} {i+1} {score:.6f} ensemble_avg\n")

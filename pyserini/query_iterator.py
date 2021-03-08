import os
import json
from enum import Enum, unique

from pyserini.search import get_topics


@unique
class TopicsFormat(Enum):
    DEFAULT = 'default'
    KILT_DRQA = 'kilt-drqa'
    KILT_DPR = 'kilt-dpr'


class DefaultQueryIterator:

    PREDEFINED_ORDER = {'msmarco-doc-dev',
                        'msmarco_doc_test',
                        'msmarco-passage-dev-subset',
                        'msmarco_passage_test_subset'}

    def __init__(self, topics: dict, order=None):
        self.order = order if order else sorted(topics.keys())
        self.topics = topics

    def __iter__(self):
        for id_ in self.order:
            yield id_, self.topics[id_].get('title')

    @classmethod
    def from_topics(cls, topics_path: str):
        if os.path.exists(topics_path):
            f = open(topics_path, 'r')
            topics = json.load(f)
            f.close()
        else:
            topics = get_topics(topics_path)
        if not topics:
            raise FileNotFoundError(f'Topic {topics_path} Not Found')
        order = None
        if topics_path in DefaultQueryIterator.PREDEFINED_ORDER:
            print(f'Using pre-defined topic order for {topics_path}')
            # Lazy import:
            from pyserini.query_iterator_order_info import QUERY_IDS
            order = QUERY_IDS[topics_path]
        return cls(topics, order)


class KiltQueryIterator:

    ENT_START_TOKEN = "[START_ENT]"
    ENT_END_TOKEN = "[END_ENT]"

    def __init__(self, topics_path: str):
        self.topics_path = topics_path
        self.topics = {}

    def __iter__(self):
        with open(self.topics_path, 'r') as f:
            for line in f:
                datapoint = json.loads(line)
                self.topics[datapoint["id"]] = datapoint
                query = (
                    datapoint["input"]
                    .replace(KiltQueryIterator.ENT_START_TOKEN, "")
                    .replace(KiltQueryIterator.ENT_END_TOKEN, "")
                    .strip()
                )
                yield datapoint["id"], query

    @classmethod
    def from_topics(cls, topics_path: str):
        return cls(topics_path)


def get_query_iterator(topics_path: str, query_format: TopicsFormat):
    mapping = {
        TopicsFormat.DEFAULT: DefaultQueryIterator,
        TopicsFormat.KILT_DRQA: KiltQueryIterator,
        TopicsFormat.KILT_DPR: KiltQueryIterator
    }
    return mapping[query_format].from_topics(topics_path)

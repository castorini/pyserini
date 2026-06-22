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

"""
This module serves as the 'root' of Pyserini search capabilities, providing common functionalities across sparse
and dense retrieval.
"""

import json
import os
from pathlib import Path
from urllib.request import urlopen, urlretrieve

from pyserini.pyclass import autoclass

# Wrappers around Anserini classes
JTopicReader = autoclass('io.anserini.search.topicreader.TopicReader')

TOPICS_AND_QRELS_BASE_URL = 'https://raw.githubusercontent.com/castorini/anserini-tools/master/topics-and-qrels/'
QRELS_METADATA_FILE = '_metadata_qrels.json'
QRELS_ALIASES_METADATA_FILE = '_metadata_qrels_aliases.json'
TOPICS_METADATA_FILE = '_metadata_topics.json'

_topics_mapping = None
_qrels_mapping = None


def _load_qrels_mapping():
    with urlopen(f'{TOPICS_AND_QRELS_BASE_URL}{QRELS_METADATA_FILE}') as response:
        qrels_mapping = json.loads(response.read().decode('utf-8'))

    with urlopen(f'{TOPICS_AND_QRELS_BASE_URL}{QRELS_ALIASES_METADATA_FILE}') as response:
        qrels_aliases_mapping = json.loads(response.read().decode('utf-8'))

    for canonical_name, aliases in qrels_aliases_mapping.items():
        if canonical_name not in qrels_mapping:
            continue

        for alias in aliases:
            qrels_mapping[alias] = qrels_mapping[canonical_name]

    return qrels_mapping


def _load_topics_mapping():
    with urlopen(f'{TOPICS_AND_QRELS_BASE_URL}{TOPICS_METADATA_FILE}') as response:
        return json.loads(response.read().decode('utf-8'))


def _get_cache_base_path():
    cache_dir = os.environ.get('PYSERINI_CACHE')
    if cache_dir:
        return Path(cache_dir)

    local_cache = Path.cwd() / '.cache'
    if local_cache.is_dir():
        return local_cache / 'pyserini'

    return Path.home() / '.cache' / 'pyserini'


def _get_topics_and_qrels_cache_path():
    cache_path = _get_cache_base_path() / 'topics-and-qrels'
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


def _get_topics_mapping():
    global _topics_mapping
    if _topics_mapping is None:
        _topics_mapping = _load_topics_mapping()
    return _topics_mapping


def _get_qrels_mapping():
    global _qrels_mapping
    if _qrels_mapping is None:
        _qrels_mapping = _load_qrels_mapping()
    return _qrels_mapping


def _parse_topics(topics):
    t = {}
    for topic in topics.keySet().toArray():

        if topic.isdigit():
            # parse the keys into integers
            topic_key = int(topic)
        else:
            topic_key = topic

        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)

    return t


def get_topics(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        Topics as a dictionary
    """
    topics_mapping = _get_topics_mapping()
    if collection_name not in topics_mapping:
        raise ValueError(f'Topic {collection_name} Not Found')

    topic = topics_mapping[collection_name]
    # Yes, this is an insanely ridiculous method name.
    topics = JTopicReader.getTopicsWithStringIdsFromFileWithTopicReaderClass(topic['reader_class'], topic['path'])
    if topics is None:
        raise ValueError(f'Unable to load topic {collection_name} from {topic["path"]}!')

    return _parse_topics(topics)


def load_topics_with_reader(file, reader_class):
    # Yes, this is an insanely ridiculous method name.
    topics = JTopicReader.getTopicsWithStringIdsFromFileWithTopicReaderClass(reader_class, file)
    if topics is None:
        raise ValueError(f'Unable to initialize TopicReader {reader_class} with file {file}!')

    return _parse_topics(topics)


def get_bright_excluded_ids(index_path):
    """
    For BRIGHT splits that exclude certain docids per query (aops, leetcode, theoremqa-questions),
    load the mapping from Hugging Face once. Call this once before the search loop to avoid rate limits.

    Returns:
        dict: query_id -> excluded_ids. Empty dict means no filtering. For each topic, exclude hits
        whose docid is in the list for that topic.
    """
    if 'bright-aops' not in index_path and 'bright-leetcode' not in index_path and 'bright-theoremqa-questions' not in index_path:
        return {}
    if 'aops' in index_path:
        split = 'aops'
    elif 'leetcode' in index_path:
        split = 'leetcode'
    elif 'theoremqa-questions' in index_path:
        split = 'theoremqa_questions'
    else:
        return {}

    from datasets import load_dataset
    ds = load_dataset('xlangai/BRIGHT', 'examples')[split]
    return {q['id']: q['excluded_ids'] for q in ds}


def get_qrels_file(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    path : str
        path of the qrels file
    """
    qrels_mapping = _get_qrels_mapping()
    if collection_name in qrels_mapping:
        qrels_file = qrels_mapping[collection_name]
        target_path = _get_topics_and_qrels_cache_path() / Path(qrels_file).name
        if not target_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = target_path.with_name(f'{target_path.name}.tmp')
            urlretrieve(f'{TOPICS_AND_QRELS_BASE_URL}{qrels_file}', tmp_path)
            tmp_path.replace(target_path)
        return str(target_path)

    raise FileNotFoundError(f'no qrels file for {collection_name}')


def get_qrels(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        qrels as a dictionary
    """
    file_path = get_qrels_file(collection_name)
    qrels = {}
    with open(file_path, 'r') as f:
        for line in f:
            qid, _, docid, judgement = line.rstrip().split()
            
            if qid.isdigit():
                qrels_key = int(qid)
            else:
                qrels_key = qid
                
            if docid.isdigit():
                doc_key = int(docid)
            else:
                doc_key = docid
                
            if qrels_key in qrels:
                qrels[qrels_key][doc_key] = judgement
            else:
                qrels[qrels_key] = {doc_key: judgement}
    return qrels

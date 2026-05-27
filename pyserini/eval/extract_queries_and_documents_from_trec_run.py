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
Extract query text and raw documents for each hit in a TREC run file, writing JSONL.

Equivalent to Anserini's io.anserini.cli.ExtractQueriesAndDocumentsFromTrecRun.

Example:
    python -m pyserini.eval.extract_queries_and_documents_from_trec_run \\
        --index /path/to/index \\
        --run run.txt \\
        --topics topics.tsv \\
        --output out.jsonl
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union

from pyserini.index.lucene import LuceneIndexReader
from pyserini.search import get_topics, get_topics_with_reader

logger = logging.getLogger(__name__)

TopicMap = Dict[Union[int, str], Dict[str, str]]


def _topic_reader_class(short_or_full: str) -> str:
    """Map Anserini short name (e.g. TsvString) to TopicReader class name."""
    if '.' in short_or_full:
        return short_or_full
    return f'io.anserini.search.topicreader.{short_or_full}TopicReader'


def resolve_topics(topics: str, topic_reader: str) -> TopicMap:
    """Mirror Anserini Topics.resolve: prebuilt name vs. topics file + reader."""
    if os.path.isfile(topics):
        reader_class = _topic_reader_class(topic_reader)
        t = get_topics_with_reader(reader_class, topics)
        logger.info('Successfully loaded topics from file: %s', topics)
        return t
    t = get_topics(topics)
    logger.info('Successfully loaded topics: %s', topics)
    return t


def _get_topic_field(topics: TopicMap, qid: str, field: str) -> Optional[str]:
    if qid in topics:
        return topics[qid].get(field)
    if qid.isdigit():
        k = int(qid)
        if k in topics:
            return topics[k].get(field)
    return None


def _maybe_parse_json_document(raw: str) -> Any:
    """If raw looks like JSON, parse it; otherwise return the string (matches Anserini behavior)."""
    if not raw:
        return raw
    i = 0
    while i < len(raw) and raw[i].isspace():
        i += 1
    if i >= len(raw):
        return raw
    c = raw[i]
    if c in '{["' or c == '-' or ('0' <= c <= '9') or c in 'tfn':
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def _open_index(index: str) -> LuceneIndexReader:
    logger.info('Fetching raw documents from index: %s', index)
    try:
        if os.path.exists(index):
            return LuceneIndexReader(index)
        reader = LuceneIndexReader.from_prebuilt_index(index)
        if reader is None:
            sys.exit(1)
        return reader
    except Exception as e:
        raise ValueError(
            f'"{index}" does not appear to have a valid inverted index.'
        ) from e


def add_candidate(
    candidates: List[Dict[str, Any]],
    index_reader: LuceneIndexReader,
    docid: str,
    score: float,
) -> None:
    raw = index_reader.doc_raw(docid)
    if raw is None:
        raise ValueError(f'Raw document with docid {docid} not found in index.')
    doc = _maybe_parse_json_document(raw)
    candidates.append({'docid': docid, 'score': score, 'doc': doc})


def write_query(
    out,
    topics: TopicMap,
    topic_field: str,
    candidates: List[Dict[str, Any]],
    qid: str,
) -> List[Dict[str, Any]]:
    text = _get_topic_field(topics, qid, topic_field)
    if text is None:
        raise ValueError(f'Unable to find query for {qid}')
    record = {
        'query': {'qid': qid, 'text': text},
        'candidates': candidates,
    }
    out.write(json.dumps(record, ensure_ascii=False) + '\n')
    return []


def run(
    index: str,
    run_path: str,
    topics: str,
    topic_reader: str,
    topic_field: str,
    output_path: str,
    hits: int,
) -> None:
    topic_map = resolve_topics(topics, topic_reader)
    index_reader = _open_index(index)

    qid_count = 0
    candidates: List[Dict[str, Any]] = []
    cur_qid = ''

    with open(output_path, 'w', encoding='utf-8') as out, open(
        run_path, encoding='utf-8'
    ) as br:
        for line in br:
            parts = line.split()
            if len(parts) < 5:
                continue
            rank = int(parts[3])
            if rank > hits:
                continue
            qid = parts[0]
            if qid != cur_qid:
                if cur_qid:
                    candidates = write_query(
                        out, topic_map, topic_field, candidates, cur_qid
                    )
                    qid_count += 1
                cur_qid = qid
            add_candidate(
                candidates, index_reader, parts[2], float(parts[4])
            )

        if cur_qid:
            write_query(out, topic_map, topic_field, candidates, cur_qid)
            qid_count += 1

    logger.info('Processed %d qids.', qid_count)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(
        description='Extract queries and raw documents from a TREC run (JSONL output).'
    )
    parser.add_argument(
        '--index',
        required=True,
        help='Lucene index path or prebuilt index name (must store raw documents).',
    )
    parser.add_argument('--run', required=True, help='Path to input TREC run file.')
    parser.add_argument(
        '--topics',
        required=True,
        help='Prebuilt topics key or path to a topics file (see --topic-reader).',
    )
    parser.add_argument(
        '--topic-reader',
        default='TsvString',
        help='TopicReader short name (e.g. TsvString) or full Java class name '
        '(used only when --topics is a file).',
    )
    parser.add_argument(
        '--topic-field',
        default='title',
        help='Topic map field to use as query text (default: title).',
    )
    parser.add_argument(
        '--output', required=True, help='Output path (JSONL, one query per line).'
    )
    parser.add_argument(
        '--hits',
        type=int,
        default=100,
        metavar='num',
        help='Maximum rank per query to include (default: 100).',
    )
    args = parser.parse_args()

    try:
        run(
            args.index,
            args.run,
            args.topics,
            args.topic_reader,
            args.topic_field,
            args.output,
            args.hits,
        )
    except ValueError as e:
        logger.error('%s', e)
        sys.exit(1)


if __name__ == '__main__':
    main()

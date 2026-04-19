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
Format stored Lucene ``raw`` fields for API responses.

Mirrors ``io.anserini.cli.CliUtils.formatDocument`` used by Anserini's REST server.
"""

from __future__ import annotations

import json
from typing import Any

from pyserini.index.lucene import Document

_SKIP_FIELDS = frozenset({'id', '_id', 'docid'})


def _convert_json_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _convert_json_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_convert_json_value(x) for x in value]
    return value


def _normalize_parsed_object(obj: dict[str, Any]) -> Any:
    parsed: dict[str, Any] = {}
    for key, value in obj.items():
        if key in _SKIP_FIELDS:
            continue
        if isinstance(value, dict):
            parsed[key] = _convert_json_value(value)
        elif isinstance(value, list):
            parsed[key] = _convert_json_value(value)
        else:
            parsed[key] = str(value)
    if len(parsed) == 1:
        return next(iter(parsed.values()))
    return parsed


def format_lucene_document(document: Document | None, parse: bool) -> Any:
    if document is None:
        return None
    raw = document.raw()
    if raw is None:
        return None
    if not parse:
        return raw
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, dict):
        return _normalize_parsed_object(data)
    return data

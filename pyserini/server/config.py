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

"""YAML server config (indexes, API keys) and in-memory accepted API tokens."""

from __future__ import annotations

import hmac
from collections import OrderedDict
from collections.abc import Iterable
from pathlib import Path
from typing import Mapping

import yaml


def load_server_config(config_path: str | None) -> tuple[Mapping[str, str], list[str] | None]:
    """Load ``indexes`` path aliases and optional ``api_keys`` (list of secret strings)."""
    if not config_path or not str(config_path).strip():
        return {}, None
    path = Path(config_path)
    if not path.is_file():
        raise ValueError(f'Config file not found: {path}')

    with path.open('r', encoding='utf-8') as f:
        payload = yaml.safe_load(f)

    if not payload:
        return {}, None

    api_keys_out: list[str] | None = None
    api_keys_raw = payload.get('api_keys')
    if api_keys_raw is not None:
        if not isinstance(api_keys_raw, list):
            raise ValueError('Config "api_keys" must be a list of strings')
        parsed: list[str] = []
        for i, item in enumerate(api_keys_raw):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f'Config api_keys entry #{i} must be a non-empty string')
            parsed.append(item.strip())
        api_keys_out = parsed or None

    if 'indexes' not in payload:
        return {}, api_keys_out

    raw_indexes = payload['indexes']
    if not isinstance(raw_indexes, dict) or not raw_indexes:
        return {}, api_keys_out

    config_parent = path.resolve().parent
    aliases: OrderedDict[str, str] = OrderedDict()
    for alias, configured_path in raw_indexes.items():
        if alias is None or str(alias).strip() == '':
            raise ValueError('Index aliases in config must be non-empty')
        if configured_path is None or str(configured_path).strip() == '':
            raise ValueError(f'Index alias "{alias}" must map to a non-empty path')

        resolved = Path(configured_path)
        if not resolved.is_absolute():
            resolved = (config_parent / resolved).resolve()

        if not resolved.is_dir():
            raise ValueError(f'Index alias "{alias}" points to missing path: {resolved}')

        aliases[str(alias)] = str(resolved)
    return aliases, api_keys_out


def load_index_aliases(config_path: str | None) -> Mapping[str, str]:
    aliases, _ = load_server_config(config_path)
    return aliases


def _normalize_token_strings(raw: Iterable[str]) -> frozenset[str]:
    out: set[str] = set()
    for i, item in enumerate(raw):
        s = str(item).strip()
        if not s:
            raise ValueError(f'api_keys entry #{i} must be a non-empty string')
        out.add(s)
    return frozenset(out)


class AcceptedApiTokens:
    """Constant-time-ish membership check for high-entropy API tokens."""

    __slots__ = ('_tokens',)

    def __init__(self, tokens: frozenset[str]) -> None:
        self._tokens = tokens

    @classmethod
    def from_strings(cls, tokens: Iterable[str]) -> AcceptedApiTokens:
        return cls(_normalize_token_strings(tokens))

    def is_valid(self, token: str | None) -> bool:
        if token is None or not str(token).strip():
            return False
        t = str(token).strip()
        t_bytes = t.encode('utf-8')
        for stored in self._tokens:
            if len(stored) != len(t):
                continue
            if hmac.compare_digest(stored.encode('utf-8'), t_bytes):
                return True
        return False

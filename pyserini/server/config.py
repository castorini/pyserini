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
import os
import secrets
import stat
import tempfile
import threading
from collections import OrderedDict
from collections.abc import Iterable
from pathlib import Path
from typing import Mapping

import yaml

from pyserini.server.utils import INDEX_TYPE, IndexConfig


def _parse_indexes(raw_indexes: object, config_parent: Path) -> OrderedDict[str, IndexConfig]:
    if not isinstance(raw_indexes, dict) or not raw_indexes:
        return OrderedDict()

    parsed_indexes: OrderedDict[str, IndexConfig] = OrderedDict()
    valid_index_types = set(INDEX_TYPE.keys())

    for alias, configured in raw_indexes.items():
        alias_str = str(alias).strip() if alias is not None else ''
        if not alias_str:
            raise ValueError('Index aliases in config must be non-empty')

        if isinstance(configured, str):
            configured_path = configured
            index_type = 'tf'
            base_index = None
            encoder = None
            ef_search = None
        elif isinstance(configured, dict):
            configured_path = configured.get('path')
            index_type = configured.get('index_type', 'tf')
            base_index = configured.get('base_index')
            encoder = configured.get('encoder')
            ef_search = configured.get('ef_search')
        else:
            raise ValueError(
                f'Index alias "{alias_str}" must map to a path string or object with path/index_type fields'
            )

        if configured_path is None or str(configured_path).strip() == '':
            raise ValueError(f'Index alias "{alias_str}" must map to a non-empty path')

        if not isinstance(index_type, str) or not index_type.strip():
            raise ValueError(f'Index alias "{alias_str}" has invalid "index_type" (must be a non-empty string)')
        index_type = index_type.strip()
        if index_type not in valid_index_types:
            raise ValueError(
                f'Index alias "{alias_str}" has unsupported index_type "{index_type}" '
                f'(must be one of {sorted(valid_index_types)})'
            )

        if base_index is not None:
            if not isinstance(base_index, str) or not base_index.strip():
                raise ValueError(
                    f'Index alias "{alias_str}" has invalid "base_index" (must be a non-empty string when set)'
                )
            base_index = base_index.strip()

        if encoder is not None:
            if not isinstance(encoder, str) or not encoder.strip():
                raise ValueError(
                    f'Index alias "{alias_str}" has invalid "encoder" (must be a non-empty string when set)'
                )
            encoder = encoder.strip()
        if index_type in ('impact', 'faiss', 'lucene_flat', 'lucene_hnsw') and not encoder:
            raise ValueError(f'Index alias "{alias_str}" requires "encoder" when index_type is "{index_type}"')

        if ef_search is not None and (not isinstance(ef_search, int) or ef_search <= 0):
            raise ValueError(f'Index alias "{alias_str}" has invalid "ef_search" (must be a positive integer when set)')

        resolved = Path(configured_path)
        if not resolved.is_absolute():
            resolved = (config_parent / resolved).resolve()

        if not resolved.is_dir():
            raise ValueError(f'Index alias "{alias_str}" points to missing path: {resolved}')

        parsed_indexes[alias_str] = IndexConfig(
            name=alias_str,
            path=str(resolved),
            index_type=index_type,
            base_index=base_index,
            encoder=encoder,
            ef_search=ef_search,
        )
    for alias, local_cfg in parsed_indexes.items():
        if local_cfg.base_index is None:
            continue
        if local_cfg.base_index not in parsed_indexes:
            raise ValueError(f'Index alias "{alias}" references unknown base_index "{local_cfg.base_index}"')
        if parsed_indexes[local_cfg.base_index].index_type != 'tf':
            raise ValueError(f'Index alias "{alias}" must reference a TF base_index, got "{local_cfg.base_index}"')
    return parsed_indexes


def load_server_config(config_path: str | None) -> tuple[Mapping[str, IndexConfig], list[str] | None]:
    """Load ``indexes`` and optional ``api_keys`` (list of secret strings)."""
    if not config_path or not str(config_path).strip():
        return {}, None
    path = Path(config_path)
    if not path.is_file():
        raise ValueError(f'Config file not found: {path}')

    with path.open('r', encoding='utf-8') as f:
        payload = yaml.safe_load(f)

    if not payload:
        return {}, None
    if not isinstance(payload, dict):
        raise ValueError('Config root must be a mapping/object')

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

    parsed_indexes = _parse_indexes(payload['indexes'], path.resolve().parent)
    return parsed_indexes, api_keys_out


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

    __slots__ = ('_tokens', '_write_lock')

    def __init__(self, tokens: frozenset[str]) -> None:
        self._tokens = tokens
        self._write_lock = threading.Lock()

    @classmethod
    def from_strings(cls, tokens: Iterable[str]) -> AcceptedApiTokens:
        return cls(_normalize_token_strings(tokens))

    def is_valid(self, token: str | None) -> bool:
        if token is None or not str(token).strip():
            return False
        t = str(token).strip()
        t_bytes = t.encode('utf-8')
        tokens = self._tokens
        for stored in tokens:
            if len(stored) != len(t):
                continue
            if hmac.compare_digest(stored.encode('utf-8'), t_bytes):
                return True
        return False

    def add(self, token: str) -> None:
        """Atomically add a token to the snapshot used by request handlers."""
        normalized = _normalize_token_strings([token])
        with self._write_lock:
            self._tokens = self._tokens.union(normalized)


class ApiTokenStore:
    """Issue API tokens into the existing YAML ``api_keys`` list atomically."""

    __slots__ = ('_config_path', '_lock')

    def __init__(self, config_path: str) -> None:
        path = Path(config_path).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f'Config file not found: {path}')
        self._config_path = path
        self._lock = threading.Lock()

    @property
    def config_path(self) -> Path:
        return self._config_path

    @staticmethod
    def _load_payload(path: Path) -> tuple[dict, list[str], dict[str, dict[str, object]]]:
        with path.open('r', encoding='utf-8') as f:
            payload = yaml.safe_load(f)
        if not isinstance(payload, dict):
            raise ValueError('Config root must be a mapping/object')

        raw_keys = payload.get('api_keys')
        if raw_keys is None:
            keys: list[str] = []
        elif not isinstance(raw_keys, list):
            raise ValueError('Config "api_keys" must be a list of strings')
        else:
            keys = []
            for i, item in enumerate(raw_keys):
                if not isinstance(item, str) or not item.strip():
                    raise ValueError(f'Config api_keys entry #{i} must be a non-empty string')
                keys.append(item.strip())

        raw_identities = payload.get('api_key_identities')
        if raw_identities is None:
            identities: dict[str, dict[str, object]] = {}
        elif not isinstance(raw_identities, dict):
            raise ValueError('Config "api_key_identities" must be a mapping/object')
        else:
            identities = {}
            for raw_token, raw_identity in raw_identities.items():
                if not isinstance(raw_token, str) or not raw_token.strip():
                    raise ValueError('Config api_key_identities keys must be non-empty token strings')
                if not isinstance(raw_identity, dict):
                    raise ValueError(f'Config identity for token "{raw_token}" must be a mapping/object')
                name = raw_identity.get('name')
                email = raw_identity.get('email')
                if not isinstance(name, str) or not name.strip():
                    raise ValueError(f'Config identity for token "{raw_token}" requires a non-empty name')
                if not isinstance(email, str) or not email.strip():
                    raise ValueError(f'Config identity for token "{raw_token}" requires a non-empty email')
                identity = dict(raw_identity)
                identity['name'] = name.strip()
                identity['email'] = email.strip()
                identities[raw_token.strip()] = identity
        return payload, keys, identities

    @staticmethod
    def _write_payload(path: Path, payload: dict) -> None:
        current = path.stat()
        fd, tmp_name = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                yaml.safe_dump(payload, f, default_flow_style=False, sort_keys=False)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp_path, stat.S_IMODE(current.st_mode))
            if hasattr(os, 'chown'):
                try:
                    os.chown(tmp_path, current.st_uid, current.st_gid)
                except PermissionError:
                    # The service normally owns its config. Preserve ownership when permitted,
                    # while still supporting unprivileged test and development environments.
                    pass
            os.replace(tmp_path, path)
            try:
                dir_fd = os.open(path.parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
            except OSError:
                dir_fd = None
            if dir_fd is not None:
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
        finally:
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass

    def issue(self, *, name: str, email: str) -> str:
        """Append a 256-bit token and its user identity, then return the token."""
        normalized_name = name.strip() if isinstance(name, str) else ''
        normalized_email = email.strip() if isinstance(email, str) else ''
        if not normalized_name:
            raise ValueError('Token identity name must be a non-empty string')
        if not normalized_email:
            raise ValueError('Token identity email must be a non-empty string')
        with self._lock:
            payload, keys, identities = self._load_payload(self._config_path)
            existing = set(keys).union(identities)
            token = secrets.token_hex(32)
            while token in existing:
                token = secrets.token_hex(32)
            keys.append(token)
            identities[token] = {'name': normalized_name, 'email': normalized_email}
            payload['api_keys'] = keys
            payload['api_key_identities'] = identities
            self._write_payload(self._config_path, payload)
            return token

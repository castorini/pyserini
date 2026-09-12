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
import json
import os
import stat
import string
import tempfile
import threading
import time
from collections import OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml

from pyserini.server.token_delivery import SmtpTokenEmailSender
from pyserini.server.utils import INDEX_TYPE, IndexConfig

DEFAULT_TOKEN_ISSUANCE_COOLDOWN_SEC = 3600.0


@dataclass(frozen=True)
class TokenIssuanceConfig:
    pool_path: str
    cooldown_sec: float
    smtp_host: str
    smtp_port: int
    smtp_security: str
    smtp_username: str | None
    smtp_password_file: str | None
    email_from: str
    email_cc: tuple[str, ...]
    smtp_timeout_sec: float


def _atomic_write_text(path: Path, content: str) -> None:
    current = path.stat()
    fd, tmp_name = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, stat.S_IMODE(current.st_mode))
        if hasattr(os, 'chown'):
            try:
                os.chown(tmp_path, current.st_uid, current.st_gid)
            except PermissionError:
                pass
        os.replace(tmp_path, path)
        try:
            dir_fd = os.open(path.parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
        except OSError:
            pass
        else:
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass


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


def _load_config_payload(config_path: str | None) -> tuple[Path | None, dict]:
    if not config_path or not str(config_path).strip():
        return None, {}
    path = Path(config_path).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f'Config file not found: {path}')

    with path.open('r', encoding='utf-8') as f:
        payload = yaml.safe_load(f)

    if not payload:
        return path, {}
    if not isinstance(payload, dict):
        raise ValueError('Config root must be a mapping/object')
    return path, payload


def load_server_config(config_path: str | None) -> tuple[Mapping[str, IndexConfig], list[str] | None]:
    """Load ``indexes`` and optional ``api_keys`` (list of secret strings)."""
    path, payload = _load_config_payload(config_path)
    if path is None:
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

    parsed_indexes = _parse_indexes(payload['indexes'], path.parent)
    return parsed_indexes, api_keys_out


def _config_string(mapping: dict, key: str, section: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Config "{section}.{key}" must be a non-empty string')
    return value.strip()


def _optional_config_string(mapping: dict, key: str, section: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Config "{section}.{key}" must be a non-empty string when set')
    return value.strip()


def _config_path(value: str, parent: Path) -> str:
    path = Path(value).expanduser()
    return str(path.resolve() if path.is_absolute() else (parent / path).resolve())


def load_token_issuance_config(config_path: str | None) -> TokenIssuanceConfig | None:
    """Load optional token inventory and SMTP settings from the server config."""
    path, payload = _load_config_payload(config_path)
    if path is None or 'token_issuance' not in payload:
        return None

    raw = payload['token_issuance']
    if not isinstance(raw, dict):
        raise ValueError('Config "token_issuance" must be a mapping/object')
    unknown = set(raw) - {'pool', 'cooldown_seconds', 'smtp'}
    if unknown:
        raise ValueError(f'Unknown token_issuance config field(s): {sorted(unknown)}')

    raw_smtp = raw.get('smtp')
    if not isinstance(raw_smtp, dict):
        raise ValueError('Config "token_issuance.smtp" must be a mapping/object')
    unknown_smtp = set(raw_smtp) - {
        'host',
        'port',
        'security',
        'username',
        'password_file',
        'sender',
        'cc',
        'timeout_seconds',
    }
    if unknown_smtp:
        raise ValueError(f'Unknown token_issuance.smtp config field(s): {sorted(unknown_smtp)}')

    cooldown = raw.get('cooldown_seconds', DEFAULT_TOKEN_ISSUANCE_COOLDOWN_SEC)
    if isinstance(cooldown, bool) or not isinstance(cooldown, (int, float)) or cooldown < 0:
        raise ValueError('Config "token_issuance.cooldown_seconds" must be a non-negative number')

    port = raw_smtp.get('port', SmtpTokenEmailSender.DEFAULT_STARTTLS_PORT)
    if isinstance(port, bool) or not isinstance(port, int):
        raise ValueError('Config "token_issuance.smtp.port" must be an integer')

    timeout = raw_smtp.get('timeout_seconds', SmtpTokenEmailSender.DEFAULT_TIMEOUT_SEC)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError('Config "token_issuance.smtp.timeout_seconds" must be a number')

    cc = raw_smtp.get('cc')
    if not isinstance(cc, list) or not cc or any(not isinstance(item, str) or not item.strip() for item in cc):
        raise ValueError('Config "token_issuance.smtp.cc" must be a non-empty list of email addresses')

    pool = _config_string(raw, 'pool', 'token_issuance')
    password_file = _optional_config_string(
        raw_smtp,
        'password_file',
        'token_issuance.smtp',
    )
    return TokenIssuanceConfig(
        pool_path=_config_path(pool, path.parent),
        cooldown_sec=float(cooldown),
        smtp_host=_config_string(raw_smtp, 'host', 'token_issuance.smtp'),
        smtp_port=port,
        smtp_security=(
            _optional_config_string(raw_smtp, 'security', 'token_issuance.smtp') or 'starttls'
        ),
        smtp_username=_optional_config_string(
            raw_smtp,
            'username',
            'token_issuance.smtp',
        ),
        smtp_password_file=_config_path(password_file, path.parent) if password_file else None,
        email_from=_config_string(raw_smtp, 'sender', 'token_issuance.smtp'),
        email_cc=tuple(item.strip() for item in cc),
        smtp_timeout_sec=float(timeout),
    )


def _normalize_token_strings(raw: Iterable[str]) -> frozenset[str]:
    out: set[str] = set()
    for i, item in enumerate(raw):
        s = str(item).strip()
        if not s:
            raise ValueError(f'api_keys entry #{i} must be a non-empty string')
        out.add(s)
    return frozenset(out)


def _normalize_email(email: str) -> str:
    normalized = email.strip().casefold() if isinstance(email, str) else ''
    if not normalized:
        raise ValueError('Token identity email must be a non-empty string')
    return normalized


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


class ApiTokenEmailAlreadyIssuedError(ValueError):
    """Raised when an email address already owns an issued API token."""


class ApiTokenPoolExhaustedError(RuntimeError):
    """Raised when no unassigned pre-generated API token remains."""


class ApiTokenStore:
    """Activate pre-generated API tokens in the existing YAML config atomically."""

    __slots__ = ('_config_path', '_lock')

    def __init__(self, config_path: str) -> None:
        path = Path(config_path).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f'Config file not found: {path}')
        self._config_path = path
        self._lock = threading.Lock()

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

    def token_for_email(self, email: str) -> str | None:
        """Return the existing lifetime token for an email without changing the config."""
        normalized_email = _normalize_email(email)
        with self._lock:
            _, _, identities = self._load_payload(self._config_path)
            for token, identity in identities.items():
                if str(identity['email']).strip().casefold() == normalized_email:
                    return token
        return None

    def activate(self, token: str, *, name: str, email: str) -> str:
        """Persist a pre-generated token and identity without creating a credential."""
        normalized_token = token.strip() if isinstance(token, str) else ''
        normalized_name = name.strip() if isinstance(name, str) else ''
        normalized_email = _normalize_email(email)
        if not normalized_token:
            raise ValueError('Pre-generated API token must be a non-empty string')
        if not normalized_name:
            raise ValueError('Token identity name must be a non-empty string')
        with self._lock:
            payload, keys, identities = self._load_payload(self._config_path)
            for existing_token, identity in identities.items():
                if str(identity['email']).strip().casefold() == normalized_email:
                    if existing_token == normalized_token:
                        return existing_token
                    raise ApiTokenEmailAlreadyIssuedError('This email address already has an API token')
            if normalized_token in identities:
                raise ValueError('Pre-generated API token is already assigned to another identity')
            if normalized_token not in keys:
                keys.append(normalized_token)
            identities[normalized_token] = {'name': normalized_name, 'email': normalized_email}
            payload['api_keys'] = keys
            payload['api_key_identities'] = identities
            _atomic_write_text(
                self._config_path,
                yaml.safe_dump(payload, default_flow_style=False, sort_keys=False),
            )
            return normalized_token


class PreGeneratedApiTokenPool:
    """Claim exact all-null entries from a protected JSON token inventory."""

    TOKEN_HEX_LENGTH = 64
    __slots__ = ('_path', '_lock')

    def __init__(self, path: str) -> None:
        resolved = Path(path).expanduser().resolve()
        if not resolved.is_file():
            raise ValueError(f'Pre-generated API token pool not found: {resolved}')
        self._path = resolved
        self._lock = threading.Lock()
        self._load_entries(resolved)

    @staticmethod
    def _is_available(entry: dict[str, object]) -> bool:
        return all(field in entry and entry[field] is None for field in ('name', 'email', 'issued_at'))

    @staticmethod
    def _assigned_email(entry: dict[str, object]) -> str | None:
        name = entry.get('name')
        email = entry.get('email')
        issued_at = entry.get('issued_at')
        if not isinstance(name, str) or not name.strip():
            return None
        if not isinstance(email, str) or not email.strip() or issued_at is None:
            return None
        return email.strip().casefold()

    @classmethod
    def _load_entries(cls, path: Path) -> list[dict[str, object]]:
        with path.open('r', encoding='utf-8') as f:
            entries = json.load(f)
        if not isinstance(entries, list):
            raise ValueError('Pre-generated API token pool must be a JSON list')
        seen = set()
        normalized = []
        for index, raw_entry in enumerate(entries):
            if not isinstance(raw_entry, dict):
                raise ValueError(f'Token pool entry #{index} must be an object')
            token = raw_entry.get('token')
            if (
                not isinstance(token, str)
                or len(token) != cls.TOKEN_HEX_LENGTH
                or any(char not in string.hexdigits for char in token)
            ):
                raise ValueError(f'Token pool entry #{index} has an invalid token')
            if token in seen:
                raise ValueError(f'Token pool entry #{index} duplicates another token')
            seen.add(token)
            normalized.append(dict(raw_entry))
        return normalized

    def claim(self, *, name: str, email: str) -> str:
        """Return an existing email assignment or claim one available token."""
        normalized_name = name.strip() if isinstance(name, str) else ''
        normalized_email = _normalize_email(email)
        if not normalized_name:
            raise ValueError('Token identity name must be a non-empty string')
        with self._lock:
            entries = self._load_entries(self._path)
            for entry in entries:
                if self._assigned_email(entry) == normalized_email:
                    return str(entry['token'])
            for entry in entries:
                if self._is_available(entry):
                    entry['name'] = normalized_name
                    entry['email'] = normalized_email
                    entry['issued_at'] = int(time.time())
                    _atomic_write_text(
                        self._path,
                        json.dumps(entries, indent=2, ensure_ascii=False) + '\n',
                    )
                    return str(entry['token'])
        raise ApiTokenPoolExhaustedError('No pre-generated API tokens remain')

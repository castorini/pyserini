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

from __future__ import annotations

import copy
import hashlib


def compute_token_fingerprint(token: str | None) -> str:
    """Stable, non-reversible short identifier for request attribution logs."""
    if token is None:
        return 'missing'
    t = str(token).strip()
    if not t:
        return 'missing'
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:12]


def build_uvicorn_log_config(
    server_log_file: str | None,
    auth_log_file: str | None,
    *,
    auth_logger_name: str | list[str],
) -> dict[str, object]:
    from uvicorn.config import LOGGING_CONFIG

    config = copy.deepcopy(LOGGING_CONFIG)
    formatters = config.setdefault('formatters', {})
    handlers = config.setdefault('handlers', {})
    loggers = config.setdefault('loggers', {})

    formatters['auth'] = {
        'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }

    if server_log_file:
        handlers['server_default_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': server_log_file,
            'encoding': 'utf-8',
        }
        handlers['server_access_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'access',
            'filename': server_log_file,
            'encoding': 'utf-8',
        }
        if 'uvicorn.error' in loggers:
            loggers['uvicorn.error']['handlers'] = ['server_default_file']
        if 'uvicorn.access' in loggers:
            loggers['uvicorn.access']['handlers'] = ['server_access_file']

    if auth_log_file:
        handlers['auth_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'auth',
            'filename': auth_log_file,
            'encoding': 'utf-8',
        }
        auth_handlers = ['auth_file']
    else:
        handlers['auth_console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'auth',
            'stream': 'ext://sys.stderr',
        }
        auth_handlers = ['auth_console']

    names = [auth_logger_name] if isinstance(auth_logger_name, str) else auth_logger_name
    for name in names:
        loggers[name] = {
            'handlers': auth_handlers,
            'level': 'INFO',
            'propagate': False,
        }
    return config

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

"""Load optional YAML index aliases (same shape as Anserini ``--index-config``)."""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Mapping

import yaml


def load_index_aliases(config_path: str | None) -> Mapping[str, str]:
    if not config_path or not str(config_path).strip():
        return {}
    path = Path(config_path)
    if not path.is_file():
        raise ValueError(f'Index config file not found: {path}')

    with path.open('r', encoding='utf-8') as f:
        payload = yaml.safe_load(f)

    if not payload or 'indexes' not in payload:
        return {}

    raw_indexes = payload['indexes']
    if not isinstance(raw_indexes, dict) or not raw_indexes:
        return {}

    config_parent = path.resolve().parent
    aliases: OrderedDict[str, str] = OrderedDict()
    for alias, configured_path in raw_indexes.items():
        if alias is None or str(alias).strip() == '':
            raise ValueError('Index aliases in index config must be non-empty')
        if configured_path is None or str(configured_path).strip() == '':
            raise ValueError(f'Index alias "{alias}" must map to a non-empty path')

        resolved = Path(configured_path)
        if not resolved.is_absolute():
            resolved = (config_parent / resolved).resolve()

        if not resolved.is_dir():
            raise ValueError(f'Index alias "{alias}" points to missing path: {resolved}')

        aliases[str(alias)] = str(resolved)
    return aliases

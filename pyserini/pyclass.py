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
Module for hiding Python-Java calls via Pyjnius
"""

import os

from ._jvm import (
    configure_classpath,
    is_jvm_already_running_error,
    suppress_jvm_startup_stderr,
)

try:
    # If the environment variable isn't defined, look in the current directory.
    anserini_root = os.environ.get(
        'ANSERINI_CLASSPATH',
        os.path.join(os.path.split(__file__)[0], 'resources/jars/')
    )
    configure_classpath(anserini_root)
except Exception as e:
    # This might happen if the JVM's already been initialized. Just eat the error.
    if not is_jvm_already_running_error(e):
        raise

with suppress_jvm_startup_stderr():
    from jnius import autoclass

    # Base Java classes
    JString = autoclass('java.lang.String')
    JFloat = autoclass('java.lang.Float')
    JInt = autoclass('java.lang.Integer')
    JPath = autoclass('java.nio.file.Path')
    JPaths = autoclass('java.nio.file.Paths')
    JList = autoclass('java.util.List')
    JArrayList = autoclass('java.util.ArrayList')
    JHashMap = autoclass('java.util.HashMap')


__all__ = [
    'autoclass',
    'JString',
    'JFloat',
    'JInt',
    'JPath',
    'JPaths',
    'JList',
    'JArrayList',
    'JHashMap',
]

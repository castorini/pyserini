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

from .setup import configure_classpath, os

# If the environment variable isn't defined, look in the current directory.
configure_classpath(os.environ['ANSERINI_CLASSPATH'] if 'ANSERINI_CLASSPATH' in os.environ else
                    os.path.join(os.path.split(__file__)[0], 'resources/jars/'))

from jnius import autoclass, cast

# Base Java classes
JString = autoclass('java.lang.String')
JFloat = autoclass('java.lang.Float')
JPath = autoclass('java.nio.file.Path')
JPaths = autoclass('java.nio.file.Paths')
JList = autoclass('java.util.List')
JArrayList = autoclass('java.util.ArrayList')
JHashMap = autoclass('java.util.HashMap')

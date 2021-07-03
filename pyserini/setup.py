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
Module for adding Anserini jar to classpath for pyjnius usage
"""

import glob
import os

import jnius_config


def configure_classpath(anserini_root="."):
    """
    Parameters
    ----------
    anserini_root : str
        (Optional) path to root anserini directory.

    """
    paths = glob.glob(os.path.join(anserini_root, 'anserini-*-fatjar.jar'))
    if not paths:
        raise Exception('No matching jar file found in {}'.format(os.path.abspath(anserini_root)))

    latest = max(paths, key=os.path.getctime)
    jnius_config.add_classpath(latest)

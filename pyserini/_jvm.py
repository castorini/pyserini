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
Utilities for configuring Pyjnius before the JVM starts.
"""

import glob
import os
import sys
from contextlib import contextmanager

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
    logging_config = os.path.join(os.path.dirname(__file__), 'resources', 'jars', 'logging.properties')
    jnius_config.add_classpath(latest)
    jnius_config.add_options('--add-modules=jdk.incubator.vector')
    # Suppress "WARNING: A restricted method in java.lang.foreign.Linker has been called"
    jnius_config.add_options('--enable-native-access=ALL-UNNAMED')

    if not os.environ.get('PYSERINI_VERBOSE_JVM'):
        # Suppress "Java vector incubator API enabled; uses preferredBitSize=128"
        jnius_config.add_options(f'-Djava.util.logging.config.file={logging_config}')
        # Suppress "SLF4J(I): Connected with provider of type [org.apache.logging.slf4j.SLF4JServiceProvider]"
        jnius_config.add_options('-Dslf4j.internal.verbosity=WARN')


def is_jvm_already_running_error(exception):
    message = str(exception).lower()
    return (
        'jvm is already running' in message or
        'vm is already running' in message or
        'java virtual machine is already running' in message
    )


@contextmanager
def suppress_jvm_startup_stderr():
    if os.environ.get('PYSERINI_VERBOSE_JVM'):
        yield
        return

    sys.stderr.flush()
    saved_stderr_fd = os.dup(2)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull_fd, 2)
        yield
    finally:
        sys.stderr.flush()
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stderr_fd)
        os.close(devnull_fd)

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

import sys
import signal

from pyserini.pyclass import autoclass


def stop_server(signal, frame):
    print("Server shutting down...")
    sys.exit(0)


if __name__ == '__main__':
    args = sys.argv[1:]

    JServer = autoclass('io.anserini.server.Application')
    JServer.main(args)

    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)

    while True:
        # wait for terminating / interrupting signal
        signal.pause()

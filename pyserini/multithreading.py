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

import threading


class ThreadSafeCount:
    
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
        
    def increment(self, inc=1):
        with self.lock:
            self.value += inc
            return self.value
     
            
class Counters:
    
    def __init__(self):
        self.indexable = ThreadSafeCount()
        self.unindexable = ThreadSafeCount()
        self.skipped = ThreadSafeCount()
        self.errors = ThreadSafeCount()


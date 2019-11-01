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


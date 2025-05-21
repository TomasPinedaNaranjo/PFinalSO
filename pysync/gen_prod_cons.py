import threading
from collections import deque
from typing import Generic, TypeVar

# Define a type variable for generic elements
E = TypeVar('E')

class GenProdCons(Generic[E]):
    
    def __init__(self, size=10):
        self.size = size
        self._buffer = deque(maxlen=size)
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, element: E) -> None:

        with self._not_full:
            # Wait until the buffer is not full
            while len(self._buffer) >= self.size:
                self._not_full.wait()
            
            # Add the element to the buffer
            self._buffer.append(element)
            
            # Notify consumers that the buffer is not empty
            self._not_empty.notify()
    
    def get(self) -> E:

        with self._not_empty:
            # Wait until the buffer is not empty
            while len(self._buffer) == 0:
                self._not_empty.wait()
            
            # Remove an element from the buffer
            element = self._buffer.popleft()
            
            # Notify producers that the buffer is not full
            self._not_full.notify()
            
            return element
    
    def __len__(self) -> int:

        with self._lock:
            return len(self._buffer)
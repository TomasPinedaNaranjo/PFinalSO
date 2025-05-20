import threading
from collections import deque
from typing import Generic, TypeVar

# Define a type variable for generic elements
E = TypeVar('E')

class GenProdCons(Generic[E]):
    """
    A Generic Producer-Consumer class implementing the Producer-Consumer pattern
    for thread synchronization.
    
    This class creates a common point of communication between two threads,
    where one thread (producer) can put elements into the buffer,
    and another thread (consumer) can get elements from the buffer.
    """
    
    def __init__(self, size=10):
        """
        Initialize the Producer-Consumer with a buffer of specified size.
        
        Args:
            size (int): Size of the buffer. Default is 10.
        """
        self.size = size
        self._buffer = deque(maxlen=size)
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, element: E) -> None:
        """
        Put an element into the buffer. If the buffer is full, block until space is available.
        
        Args:
            element (E): The element to put into the buffer.
        """
        with self._not_full:
            # Wait until the buffer is not full
            while len(self._buffer) >= self.size:
                self._not_full.wait()
            
            # Add the element to the buffer
            self._buffer.append(element)
            
            # Notify consumers that the buffer is not empty
            self._not_empty.notify()
    
    def get(self) -> E:
        """
        Get an element from the buffer. If the buffer is empty, block until an item is available.
        
        Returns:
            E: The element from the buffer.
        """
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
        """
        Get the current number of elements in the buffer.
        
        Returns:
            int: The number of elements in the buffer.
        """
        with self._lock:
            return len(self._buffer)
#!/usr/bin/env python
import threading

class RendezvousDEchange:
    def __init__(self):
        self.item = None
        self.has_item = False
        self._lock = threading.Lock()
        self._exchange = threading.Condition(self._lock)

    def echanger(self, message):
        with self._exchange:
            if not self.has_item:
                self.item = message
                self.has_item = True
                self._exchange.wait()
                result = self.item
                self.has_item = False
                return result
            else:
                result = self.item
                self.item = message
                self.has_item = False
                self._exchange.notify()
                return result

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
#     rendez = RendezvousDEchage()

#     thread__1 = Thread(target=rendez.echager,args=("A", 1))
    
#     thread_2 = Thread(target=rendez.echager,args=("B", 2))
#     thread__1.start()
#     thread_2.start()
#     thread__1.join()
#     thread_2.join()
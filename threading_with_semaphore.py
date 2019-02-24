"""Prints numbers from 0 to 99 sequentially from two threads with semaphore"""

import threading
import time


class ReporterThread(threading.Thread):
    semaphore = threading.Semaphore()

    def __init__(self, first_val):
        threading.Thread.__init__(self)
        self.__data = range(first_val, 100, 2)
        self.name = 'Thread-{}'.format(first_val)

    def run(self):
        for print_item in self.__data:
            with self.semaphore:
                print('{name}: {item}'.format(name=self.name, item=print_item))
            time.sleep(0.5)


if __name__ == "__main__":
    for item in range(2):
        time.sleep(0.2)
        ReporterThread(item).start()

"""Prints numbers sequentially from two multiprocessing threads with lock"""

import multiprocessing
import time


class ReporterThread(multiprocessing.Process):
    print_lock = multiprocessing.Lock()

    def __init__(self, first_val):
        multiprocessing.Process.__init__(self)
        self.__data = range(first_val, 100, 2)
        self.name = 'Thread-{}'.format(first_val)

    def run(self):
        for print_item in self.__data:
            with self.print_lock:
                print('{name}: {item}'.format(name=self.name, item=print_item))
            time.sleep(0.5)


if __name__ == "__main__":
    thread1 = ReporterThread(0)
    thread1.start()
    time.sleep(0.2)
    thread2 = ReporterThread(1)
    thread2.start()

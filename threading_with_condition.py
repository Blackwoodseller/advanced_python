"""Prints numbers from 0 to 99 sequentially from two threads with condition"""

import threading


class ReporterThread(threading.Thread):
    def __init__(self, first_val, condition):
        threading.Thread.__init__(self)
        self.__data = range(first_val, 100, 2)
        self.name = 'Thread-{}'.format(first_val)
        self.condition = condition

    def run(self):
        for print_item in self.__data:
            with self.condition:
                self.condition.wait()
                print('{name}: {item}'.format(name=self.name, item=print_item))
                self.condition.notify()


if __name__ == "__main__":
    condition = threading.Condition()

    [ReporterThread(start_val, condition).start() for start_val in range(2)]

    with condition:
        condition.notify()

"""Prints numbers from 0 to 99 sequentially from two threads with event"""
import threading
import time


class PrintThread(threading.Thread):
    def __init__(self, first_val, print_event):
        super().__init__()
        self.name = 'Thread-{}'.format(first_val)
        self.__data = range(first_val, 101, 2)
        self.event = print_event

    def run(self):
        for print_item in self.__data:
            self.event.wait()
            self.event.clear()
            print('{name}: {item}'.format(name=self.name, item=print_item))
            self.event.set()
            time.sleep(0.5)


if __name__ == "__main__":
    my_event = threading.Event()
    my_event.set()

    thread1 = PrintThread(0, my_event)
    thread2 = PrintThread(1, my_event)

    thread1.start()
    time.sleep(0.2)
    thread2.start()

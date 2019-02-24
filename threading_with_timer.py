"""Prints numbers from 0 to 99 sequentially from two threads with timer"""

import threading
import time


def print_seq(first_val):
    """Prints numbers from first_val up to 100 with step 2"""

    for print_item in range(first_val, 101, 2):
        print('{item}'.format(item=print_item))
        time.sleep(0.2)


if __name__ == "__main__":
    thread1 = threading.Timer(interval=0.0, function=print_seq, args=(0,))
    thread1.start()

    thread2 = threading.Timer(interval=0.1, function=print_seq, args=(1,))
    thread2.start()

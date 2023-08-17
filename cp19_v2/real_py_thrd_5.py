import concurrent.futures
import queue
import random
import threading
import time


def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        queue.put(message)
        print(f"Put {message}")


def consumer(queue, event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        print(f"Got {message}")

if __name__ == "__main__":
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        event.set()

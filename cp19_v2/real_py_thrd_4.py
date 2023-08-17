import logging
import queue
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def producer(pipeline, event):
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")
    
    logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(
            "Consumer storing message: %s  (queue size=%s)",
            message,
            pipeline.qsize(),
        )

    logging.info("Consumer received EXIT event. Exiting")


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug(f"{name}:about to get from queue")
        value = self.get()
        logging.debug(f"{name}:got {value} from queue")
        return value
    
    def set_message(self, value, name):
        logging.debug(f"{name}:about to add {value} to queue")
        self.put(value)
        logging.debug(f"{name}:added to queue")




if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, 
                        datefmt="%H:%M:%S")
    pipeline = Pipeline()
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        event.set()
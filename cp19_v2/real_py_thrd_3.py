import random
import logging
from concurrent.futures import ThreadPoolExecutor
import threading


SENTINEL = object()

def producer(pipeline):
    """Pretend we're getting a message from the network"""
    for _ in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")
    
    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL)


def consumer(pipeline):
    """Pretend we're saving a number in the database."""
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)


class Pipeline:
    """
    Class to allow a single element pipeline between producer and customer.
    """

    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()  # do not allow consumption at the beginning   
    
    def get_message(self, name):
        logging.debug(f"{name}:about to acquire getlock")
        self.consumer_lock.acquire()
        logging.debug(f"{name}: have getlock")
        message = self.message
        logging.debug(f"{name}:about to release setlock")
        self.producer_lock.release()
        logging.debug("%s:setlock released")
        return message

    def set_message(self, message, name):
        logging.debug(f"{name}:about to acquire setlock")
        self.producer_lock.acquire()
        logging.debug(f"{name}:have setlock")
        self.message = message
        logging.debug(f"{name}:about to release get lock")
        self.consumer_lock.release()
        logging.debug(f"{name}:getlock released")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, 
                        datefmt="%H:%M:%S")
    pipeline = Pipeline()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
import pika
import time

from multiprocessing import Queue

from config import settings
from schemas import Message

INPUT_QUEUE_NAME = settings.QUEUE1
OUTPUT_QUEUE_NAME = settings.QUEUE2
BLACKLIST_WORDS: set[str] = set()


def filter_service(in_queue: Queue, out_queue: Queue):
    while True:
        try:
            message = in_queue.get()

            message_text_set = set(message.message_text.lower().split())
            if not message_text_set.intersection(BLACKLIST_WORDS):
                print(f"Sending the {message=} to output queue")
                out_queue.put(message)
            else:
                print(f"Blocking the {message=}")
        except Exception as e:
            print(f"Error while processing message {message=}: {str(e)}")
        
        time.sleep(0.01)


def parse_blacklist_words():
    global BLACKLIST_WORDS

    with open(settings.WORDS_BLACKLIST_PATH, mode="r") as fp:
        BLACKLIST_WORDS = set(map(lambda x: x.strip().lower(), fp.readlines()))

import time

from multiprocessing import Queue

from config import settings
from schemas import Message

INPUT_QUEUE_NAME = settings.QUEUE2
OUTPUT_QUEUE_NAME = settings.QUEUE3


def scream_service(in_queue: Queue, out_queue: Queue):
    while True:
        try:
            message = in_queue.get()
            message.message_text = message.message_text.upper()
            print(f"Sending the {message=} to output queue")
            out_queue.put(message)
        except Exception as e:
            print(f"Error while processing message {message=}: {str(e)}")
        
        time.sleep(0.01)

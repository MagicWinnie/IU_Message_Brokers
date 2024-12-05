import time

from multiprocessing import Queue

from config import settings
from schemas import Message

from services.publish.mock_publisher import MockPublisher


INPUT_QUEUE_NAME = settings.QUEUE3
publisher = MockPublisher()


def publish_service(in_queue: Queue):
    while True:
        try:
            message = in_queue.get()
            publisher.publish(message)
        except Exception as e:
            print(f"Error while processing message {message=}: {str(e)}")
        
        time.sleep(0.01)


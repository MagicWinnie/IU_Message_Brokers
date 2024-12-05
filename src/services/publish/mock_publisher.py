from services.publish.base_publisher import BasePublisher
from schemas import Message


class MockPublisher(BasePublisher):
    def publish(self, message: Message):
        print(f"published {message.message_text}")


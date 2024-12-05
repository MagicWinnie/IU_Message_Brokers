from abc import ABC, abstractmethod

from schemas import Message


class BasePublisher(ABC):
    @abstractmethod
    def publish(self, message: Message): ...
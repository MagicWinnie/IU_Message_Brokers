import json

import pika

from config import settings
from services.schemas import Message

INPUT_QUEUE_NAME = "filter2screaming"
OUTPUT_QUEUE_NAME = "screaming2publish"


def callback(ch, method, properties, body):
    try:
        message = Message(**json.loads(body))
        message.message_text = message.message_text.upper()
        print(f"Sending the {message=} to output queue")
        ch.basic_publish(
            exchange="",
            routing_key=OUTPUT_QUEUE_NAME,
            body=message.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    except Exception as e:
        print(f"Error while processing message {body=}: {str(e)}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=INPUT_QUEUE_NAME, durable=True)
    channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

    channel.basic_consume(queue=INPUT_QUEUE_NAME, on_message_callback=callback)

    print("Screaming service has started")

    channel.start_consuming()


if __name__ == "__main__":
    main()

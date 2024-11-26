import pika

from config import settings
from schemas import Message

INPUT_QUEUE_NAME = settings.QUEUE2
OUTPUT_QUEUE_NAME = settings.QUEUE3


def callback(ch, method, properties, body):
    try:
        message = Message.model_validate_json(body)
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
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=INPUT_QUEUE_NAME, durable=True)
    channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

    channel.basic_consume(queue=INPUT_QUEUE_NAME, on_message_callback=callback)

    print("Screaming service has started")

    channel.start_consuming()


if __name__ == "__main__":
    main()

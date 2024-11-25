import pika

from config import settings
from services.schemas import Message

INPUT_QUEUE_NAME = "screaming2publish"


def callback(ch, method, properties, body):
    try:
        message = Message.model_validate_json(body)
        print(f"Sending the {message=} to email")
    except Exception as e:
        print(f"Error while processing message {body=}: {str(e)}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=INPUT_QUEUE_NAME, durable=True)
    channel.basic_consume(queue=INPUT_QUEUE_NAME, on_message_callback=callback)

    print("Publish service has started")

    channel.start_consuming()


if __name__ == "__main__":
    main()

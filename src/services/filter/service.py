import pika

from config import settings
from services.schemas import Message

INPUT_QUEUE_NAME = settings.QUEUE1
OUTPUT_QUEUE_NAME = settings.QUEUE2
BLACKLIST_WORDS: set[str] = set()


def callback(ch, method, properties, body):
    try:
        message = Message.model_validate_json(body)

        message_text_set = set(message.message_text.lower().split())
        if not message_text_set.intersection(BLACKLIST_WORDS):
            print(f"Sending the {message=} to output queue")
            ch.basic_publish(
                exchange="",
                routing_key=OUTPUT_QUEUE_NAME,
                body=message.model_dump_json(),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        else:
            print(f"Blocking the {message=}")
    except Exception as e:
        print(f"Error while processing message {body=}: {str(e)}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def parse_blacklist_words():
    global BLACKLIST_WORDS

    with open(settings.WORDS_BLACKLIST_PATH, mode="r") as fp:
        BLACKLIST_WORDS = set(map(lambda x: x.strip().lower(), fp.readlines()))


def main():
    parse_blacklist_words()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=INPUT_QUEUE_NAME, durable=True)
    channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

    channel.basic_consume(queue=INPUT_QUEUE_NAME, on_message_callback=callback)

    print("Filter service has started")

    channel.start_consuming()


if __name__ == "__main__":
    main()

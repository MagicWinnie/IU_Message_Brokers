import pika
from fastapi import FastAPI, HTTPException, status

from config import settings
from schemas import Message

OUTPUT_QUEUE_NAME = settings.QUEUE1


app = FastAPI()


@app.post("/process-message")
def process_message(body: Message):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
        )
        channel = connection.channel()
        channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=OUTPUT_QUEUE_NAME,
            body=body.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        channel.close()
        connection.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish message to RabbitMQ: {str(e)}",
        )

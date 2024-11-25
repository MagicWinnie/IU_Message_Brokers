from contextlib import asynccontextmanager

import pika
from fastapi import FastAPI, HTTPException, status

from config import settings
from services.schemas import Message

OUTPUT_QUEUE_NAME = "api2filter"

connection: pika.BlockingConnection | None = None
channel: pika.adapters.blocking_connection.BlockingChannel | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    global connection, channel

    # before startup
    print("Starting RabbitMQ connection...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

    yield

    print("Stopping RabbitMQ connection...")
    # before shutdown
    if channel:
        channel.close()
    if connection:
        connection.close()


app = FastAPI(lifespan=lifespan)


@app.post("/process-message")
def process_message(body: Message):
    try:
        channel.basic_publish(
            exchange="",
            routing_key=OUTPUT_QUEUE_NAME,
            body=body.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to publish message to RabbitMQ: {str(e)}")

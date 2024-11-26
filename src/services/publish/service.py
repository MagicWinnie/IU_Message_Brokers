import smtplib
from email.mime.text import MIMEText

import pika

from config import settings
from services.schemas import Message

INPUT_QUEUE_NAME = settings.QUEUE3


def callback(ch, method, properties, body):
    try:
        message = Message.model_validate_json(body)

        print(f"Sending the {message=} to emails={settings.EMAIL_RECEIVERS}")

        msg = MIMEText(f"From user: {message.user_alias}\nMessage: {message.message_text}")
        msg["Subject"] = "Message on SoftArch from Team-24"
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = ", ".join(settings.EMAIL_RECEIVERS)

        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.ehlo(settings.SMTP_EMAIL)
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, settings.EMAIL_RECEIVERS, msg.as_string())
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

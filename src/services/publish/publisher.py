import smtplib
from email.mime.text import MIMEText

from config import settings
from schemas import Message

from services.publish.base_publisher import BasePublisher


class Publisher(BasePublisher):
    def publish(self, message: Message):
        print(f"Sending the {message=} to emails={settings.EMAIL_RECEIVERS}")

        msg = MIMEText(f"From user: {message.user_alias}\nMessage: {message.message_text}")
        msg["Subject"] = "Message on SoftArch from Team-24"
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = ", ".join(settings.EMAIL_RECEIVERS)

        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=3) as server:
            server.ehlo()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, settings.EMAIL_RECEIVERS, msg.as_string())
    
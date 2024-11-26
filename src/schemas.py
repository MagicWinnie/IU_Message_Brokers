from pydantic import BaseModel


class Message(BaseModel):
    message_text: str
    user_alias: str

from pydantic import BaseModel


class ProcessMessageRequest(BaseModel):
    message_text: str
    user_alias: str

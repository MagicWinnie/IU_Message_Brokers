from fastapi import FastAPI

from src.services.api.schemas import ProcessMessageRequest

app = FastAPI()


@app.post("/process-message")
def process_message(body: ProcessMessageRequest):
    return None

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from services.api.schemas import ProcessMessageRequest


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # before startup
    print(settings.RABBITMQ_HOST)
    yield
    # before shutdown


app = FastAPI(lifespan=lifespan)


@app.post("/process-message")
def process_message(body: ProcessMessageRequest):
    return None

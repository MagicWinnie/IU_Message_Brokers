import uvicorn

from multiprocessing import Queue, Process

from fastapi import FastAPI, HTTPException, status

from config import settings
from schemas import Message

OUTPUT_QUEUE_NAME = settings.QUEUE1


def run_api_service(out_queue):
    app = FastAPI()

    @app.post("/process-message")
    async def process_message(body: Message):
        try:
            out_queue.put(body)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to publish message: {str(e)}",
            )

    uvicorn.run(app, host="0.0.0.0", port=8932)
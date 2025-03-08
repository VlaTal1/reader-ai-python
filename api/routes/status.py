from fastapi import APIRouter
from pydantic import BaseModel

from services.rabbitmq_consumer import rabbitmq_consumer

router = APIRouter()


class StatusResponse(BaseModel):
    status: str
    rabbitmq_connected: bool


@router.get("/status", response_model=StatusResponse)
async def get_status():
    is_connected = (
            rabbitmq_consumer.connection is not None
            and not rabbitmq_consumer.connection.is_closed
    )

    return StatusResponse(
        status="ok",
        rabbitmq_connected=is_connected
    )

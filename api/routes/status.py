from fastapi import APIRouter

from models.schemas import StatusResponse

router = APIRouter()


@router.get("/status", response_model=StatusResponse)
async def get_status():
    return StatusResponse(
        status="ok",
        version="1.0.0"
    )

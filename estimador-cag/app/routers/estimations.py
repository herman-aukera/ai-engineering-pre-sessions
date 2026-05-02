from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import estimate

router = APIRouter(prefix="/api/v1", tags=["estimations"])


class EstimateRequest(BaseModel):
    transcription: str
    tier: str = "flash"  # opcional, default flash



class EstimateResponse(BaseModel):
    estimation: str
    model: str
    tier: str
    input_tokens: int
    output_tokens: int


@router.post("/estimate", response_model=EstimateResponse)
def create_estimation(request: EstimateRequest):
    result = estimate(request.transcription)
    return result
from pydantic import BaseModel
from app.models import AlgorithmEnum
from typing import Optional
from typing import Tuple


class PredictionOut(BaseModel):
    id: int
    received_photo: str
    marked_photo: str
    avg_confidence: float
    sectors_count: int
    class Config:
        orm_mode = True


class ModelOpinion(BaseModel):
    disease: str
    confidence: float
    box: Tuple[int, int, int, int]  # x1, y1, x2, y2
    model_name: str
    class Config:
        orm_mode = True
